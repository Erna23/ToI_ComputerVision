import cv2
import numpy as np
import json
from datetime import datetime
from ultralytics import YOLO

# ==============================
# 1. 설정
# ==============================
TIGER_PATH = "tiger.png"
COW_PATH   = "cow.png"
RAT_PATH   = "rat.png"

LOG_FILENAME = "sticker_yolo_log.json"
LOG_EVERY_N_FRAMES = 5

# EMA smoothing
SMOOTH_ALPHA = 0.6
SMOOTH_ON_DEFAULT = True

# 현재 선택된 스티커 인덱스 (0: rat, 1: cow, 2: tiger)
current_sticker = 0


# ==============================
# 2. PNG + 알파 로딩
# ==============================
def load_png_with_alpha(path):
    sticker = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if sticker is None:
        raise FileNotFoundError(f"스티커 파일을 찾을 수 없습니다: {path}")

    if sticker.shape[2] == 4:
        bgr = sticker[:, :, :3]
        alpha = sticker[:, :, 3] / 255.0
    else:
        bgr = sticker
        alpha = np.ones(bgr.shape[:2], dtype=float)
    return bgr, alpha


# 이미지 로드
tiger_bgr, tiger_alpha = load_png_with_alpha(TIGER_PATH)
cow_bgr,   cow_alpha   = load_png_with_alpha(COW_PATH)
rat_bgr,   rat_alpha   = load_png_with_alpha(RAT_PATH)

# 스티커 리스트 정의 (순서: rat=0, cow=1, tiger=2)
STICKERS = [
    {
        "name": "rat",
        "bgr": rat_bgr,
        "alpha": rat_alpha,
        "width_scale": 1.31,
        "offset_x_ratio": 0.0,
        "offset_y_ratio": -0.15,
    },
    {
        "name": "cow",
        "bgr": cow_bgr,
        "alpha": cow_alpha,
        "width_scale": 1.15,
        "offset_x_ratio": 0.0,
        "offset_y_ratio": -1.3,
    },
    {
        "name": "tiger",
        "bgr": tiger_bgr,
        "alpha": tiger_alpha,
        "width_scale": 1.4,
        "offset_x_ratio": 0.0,
        "offset_y_ratio": -0.5,
    }
]


# ==============================
# 얼굴 검출 / YOLO
# ==============================
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
yolo_model = YOLO("yolov8n.pt")


# ==============================
# 3. 스티커 합성 함수
# ==============================
def overlay_sticker_bgr_alpha(base_img, sticker_bgr, sticker_alpha, x, y):
    h, w = sticker_bgr.shape[:2]
    bg_h, bg_w = base_img.shape[:2]

    x1 = int(x - w/2)
    y1 = int(y - h/2)
    x2 = x1 + w
    y2 = y1 + h

    x1_clip = max(0, x1)
    y1_clip = max(0, y1)
    x2_clip = min(bg_w, x2)
    y2_clip = min(bg_h, y2)

    if x1_clip >= x2_clip or y1_clip >= y2_clip:
        return base_img

    sticker_x1 = x1_clip - x1
    sticker_y1 = y1_clip - y1
    sticker_x2 = sticker_x1 + (x2_clip - x1_clip)
    sticker_y2 = sticker_y1 + (y2_clip - y1_clip)

    roi = base_img[y1_clip:y2_clip, x1_clip:x2_clip]
    sticker_roi = sticker_bgr[sticker_y1:sticker_y2, sticker_x1:sticker_x2]
    alpha_roi = sticker_alpha[sticker_y1:sticker_y2, sticker_x1:sticker_x2]
    alpha_3 = np.dstack([alpha_roi]*3)

    blended = (alpha_3 * sticker_roi + (1 - alpha_3) * roi).astype(np.uint8)
    base_img[y1_clip:y2_clip, x1_clip:x2_clip] = blended
    return base_img


# ==============================
# 4. 얼굴 기반 스티커 위치 계산
# ==============================
def add_mask_by_facebox(frame_bgr, prev_centers=None, smooth_on=True, alpha=0.6):
    if prev_centers is None:
        prev_centers = []

    gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.2, minNeighbors=5, minSize=(80,80)
    )

    if len(faces) == 0:
        return frame_bgr, False, 0, []

    faces = sorted(faces, key=lambda b: b[0])

    out = frame_bgr.copy()
    new_prev = []

    # -----------------------------
    # 현재 선택 스티커 1개만 적용
    # -----------------------------
    sticker = STICKERS[current_sticker]
    sbgr = sticker["bgr"]
    salpha = sticker["alpha"]
    width_scale = sticker["width_scale"]
    offset_x_ratio = sticker["offset_x_ratio"]
    offset_y_ratio = sticker["offset_y_ratio"]

    for idx, (x, y, w, h) in enumerate(faces):
        target_width = int(w * width_scale)
        sh, sw = sbgr.shape[:2]
        scale = target_width / sw
        th = int(sh * scale)

        rs_bgr = cv2.resize(sbgr, (target_width, th), interpolation=cv2.INTER_AREA)
        rs_alpha = cv2.resize(salpha, (target_width, th), interpolation=cv2.INTER_AREA)

        base_cx = x + w//2
        base_cy = int(y + h * 0.55)

        cx = base_cx + int(target_width * offset_x_ratio)
        cy = base_cy + int(th * offset_y_ratio)

        if smooth_on and idx < len(prev_centers):
            cx = int(alpha * cx + (1-alpha) * prev_centers[idx]["cx"])
            cy = int(alpha * cy + (1-alpha) * prev_centers[idx]["cy"])

        new_prev.append({"cx": cx, "cy": cy})

        out = overlay_sticker_bgr_alpha(out, rs_bgr, rs_alpha, cx, cy)

    return out, True, len(faces), new_prev


# ==============================
# 5. 웹캠 루프
# ==============================
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("웹캠을 열 수 없습니다.")

logs = []
frame_id = 0
smooth_on = SMOOTH_ON_DEFAULT
prev_centers = []

print("웹캠 시작! 1=rat, 2=cow, 3=tiger  |  s=스무딩 ON/OFF  |  q=종료")


while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_mask, face_detected, person_count, prev_centers = add_mask_by_facebox(
        frame, prev_centers, smooth_on, SMOOTH_ALPHA
    )

    cv2.imshow("StickerCam", frame_mask)

    key = cv2.waitKey(1) & 0xFF

    # --- 종료 ---
    if key == ord('q'):
        break

    # --- 스무딩 ON/OFF ---
    elif key == ord('s'):
        smooth_on = not smooth_on
        if not smooth_on:
            prev_centers = []
        print("스무딩:", smooth_on)

    # --- 스티커 변경 ---
    elif key == ord('1'):
        current_sticker = 0
        print("현재 스티커: rat")

    elif key == ord('2'):
        current_sticker = 1
        print("현재 스티커: cow")

    elif key == ord('3'):
        current_sticker = 2
        print("현재 스티커: tiger")


cap.release()
cv2.destroyAllWindows()
