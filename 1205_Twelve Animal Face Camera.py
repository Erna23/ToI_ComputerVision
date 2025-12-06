import cv2
import numpy as np
import mediapipe as mp
import os
import datetime
import time  # 카운트다운 시간 계산용
from PIL import Image, ImageFont, ImageDraw

# ==========================
# 1. 기본 설정
# ==========================
SMOOTH_ALPHA = 0.6
SMOOTH_ON_DEFAULT = True

# ==========================
# 2. 스티커 PNG 경로
# ==========================

PIG_PATH     = "pig.png"
DOG_PATH     = "dog.png"
CHICKEN_PATH = "chicken.png"
RAT_PATH     = "rat.png"
COW_PATH     = "cow.png"
TIGER_PATH   = "tiger.png"
RABBIT_PATH  = "rabbit.png"
SNAKE_PATH   = "snake.png"
HORSE_PATH   = "horse.png"
SHEEP_PATH   = "sheep.png"
MONKEY_PATH  = "monkey.png"
DRAGON_PATH  = "dragon.png"

# ==========================
# 3. PNG + 알파 로딩
# ==========================
def load_png_with_alpha(path):
    if not os.path.exists(path):
        # 파일이 없으면 빈 이미지 반환 (에러 방지)
        return np.zeros((100, 100, 3), dtype=np.uint8), np.zeros((100, 100), dtype=float)

    sticker = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if sticker is None:
        return np.zeros((100, 100, 3), dtype=np.uint8), np.zeros((100, 100), dtype=float)
        
    if sticker.shape[2] == 4:
        bgr = sticker[:, :, :3]
        alpha = sticker[:, :, 3] / 255.0
    else:
        bgr = sticker
        alpha = np.ones(bgr.shape[:2], dtype=float)
    return bgr, alpha

# 이미지 로딩 (예외 처리 포함)
try:
    pig_bgr, pig_alpha         = load_png_with_alpha(PIG_PATH)
    dog_bgr, dog_alpha         = load_png_with_alpha(DOG_PATH)
    chicken_bgr, chicken_alpha = load_png_with_alpha(CHICKEN_PATH)
    rat_bgr, rat_alpha         = load_png_with_alpha(RAT_PATH)
    cow_bgr, cow_alpha         = load_png_with_alpha(COW_PATH)
    tiger_bgr, tiger_alpha     = load_png_with_alpha(TIGER_PATH)
    rabbit_bgr, rabbit_alpha   = load_png_with_alpha(RABBIT_PATH)
    snake_bgr, snake_alpha     = load_png_with_alpha(SNAKE_PATH)
    horse_bgr, horse_alpha     = load_png_with_alpha(HORSE_PATH)
    sheep_bgr, sheep_alpha     = load_png_with_alpha(SHEEP_PATH)
    monkey_bgr, monkey_alpha   = load_png_with_alpha(MONKEY_PATH)
    dragon_bgr, dragon_alpha   = load_png_with_alpha(DRAGON_PATH)
except Exception as e:
    print(f"이미지 로딩 중 오류 발생: {e}")
    rat_bgr, rat_alpha = np.zeros((100,100,3), np.uint8), np.zeros((100,100), float)

# ==========================
# 4. 스티커 정보
# ==========================
STICKERS = {
    "rat": {"bgr": rat_bgr, "alpha": rat_alpha, "width_scale": 1.3, "offset_x_ratio": 0.0, "offset_y_ratio": -0.15},
    "cow": {"bgr": cow_bgr, "alpha": cow_alpha, "width_scale": 1.15, "offset_x_ratio": 0.0, "offset_y_ratio": -1.3},
    "tiger": {"bgr": tiger_bgr, "alpha": tiger_alpha, "width_scale": 1.4, "offset_x_ratio": 0.0, "offset_y_ratio": -0.5},
    "rabbit": {"bgr": rabbit_bgr, "alpha": rabbit_alpha, "width_scale": 2.7, "offset_x_ratio": 0.0, "offset_y_ratio": -0.3},
    "dragon": {"bgr": dragon_bgr, "alpha": dragon_alpha, "width_scale": 1.3, "offset_x_ratio": 0.0, "offset_y_ratio": -0.1},
    "snake": {"bgr": snake_bgr, "alpha": snake_alpha, "width_scale": 0.8, "offset_x_ratio": 1.0, "offset_y_ratio": 1.0},
    "horse": {"bgr": horse_bgr, "alpha": horse_alpha, "width_scale": 1.95, "offset_x_ratio": 0.0, "offset_y_ratio": -0.1},
    "sheep": {"bgr": sheep_bgr, "alpha": sheep_alpha, "width_scale": 1.3, "offset_x_ratio": 0.0, "offset_y_ratio": -0.05},
    "monkey": {"bgr": monkey_bgr, "alpha": monkey_alpha, "width_scale": 1.9, "offset_x_ratio": 0.0, "offset_y_ratio": -0.12},
    "dog": {"bgr": dog_bgr, "alpha": dog_alpha, "width_scale": 1.4, "offset_x_ratio": 0.0, "offset_y_ratio": -0.25},
    "pig": {"bgr": pig_bgr, "alpha": pig_alpha, "width_scale": 1.4, "offset_x_ratio": 0.0, "offset_y_ratio": -0.29},
    "chicken": {"bgr": chicken_bgr, "alpha": chicken_alpha, "width_scale": 2.7, "offset_x_ratio": 0.0, "offset_y_ratio": -0.03},
}

CURRENT_STICKER = STICKERS.get("chicken", STICKERS["rat"])

# ==========================
# 5. MediaPipe 설정
# ==========================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)

MENU_ITEMS = [
    {"pos": (50, 50), "key": "rat", "color": (0, 255, 255)},
    {"pos": (50, 80), "key": "cow", "color": (0, 200, 255)},
    {"pos": (50, 110), "key": "tiger", "color": (0, 150, 255)},
    {"pos": (50, 140), "key": "rabbit", "color": (0, 100, 255)},
    {"pos": (50, 170), "key": "dragon", "color": (0, 50, 255)},
    {"pos": (50, 200), "key": "snake", "color": (0, 0, 255)},
    {"pos": (50, 230), "key": "horse", "color": (50, 0, 255)},
    {"pos": (50, 260), "key": "sheep", "color": (100, 0, 255)},
    {"pos": (50, 290), "key": "monkey", "color": (150, 0, 255)},
    {"pos": (50, 320), "key": "dog", "color": (255, 0, 255)},
    {"pos": (50, 350), "key": "pig", "color": (255, 0, 200)},
    {"pos": (50, 380), "key": "chicken", "color": (255, 0, 150)},
]

MENU_RADIUS = 10

# ==========================
# 6. 유틸리티 함수
# ==========================
def put_text_pil(img, text, pos, size=20, color=(255, 255, 255)):
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    
    font = None
    font_candidates = [
        "C:/Windows/Fonts/malgun.ttf",       
        "C:/Windows/Fonts/arial.ttf",        
        "/System/Library/Fonts/AppleSDGothicNeo.ttc", 
        "/Library/Fonts/Arial.ttf",          
        "malgun.ttf", 
        "arial.ttf"
    ]
    
    for font_path in font_candidates:
        if os.path.exists(font_path) or (not os.path.isabs(font_path)):
            try:
                font = ImageFont.truetype(font_path, size)
                break
            except:
                continue
    
    if font is None:
        font = ImageFont.load_default()
    
    stroke_width = 2
    stroke_fill = (0, 0, 0)
    
    draw.text(pos, text, font=font, fill=color, stroke_width=stroke_width, stroke_fill=stroke_fill)
    return np.array(img_pil)

def overlay_sticker_bgr_alpha(base_img, sticker_bgr, sticker_alpha, x, y):
    h, w = sticker_bgr.shape[:2]
    bg_h, bg_w = base_img.shape[:2]
    x1 = int(x - w / 2)
    y1 = int(y - h / 2)
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

def add_mask(frame_bgr, prev_centers=None, smooth_on=True, alpha=0.6):
    global CURRENT_STICKER
    if prev_centers is None:
        prev_centers = []
    
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    results = face_detection.process(frame_rgb)
    
    if not results.detections:
        return frame_bgr, False, 0, []

    sticker = CURRENT_STICKER
    sbgr = sticker["bgr"]
    salpha = sticker["alpha"]
    width_scale = sticker["width_scale"]
    offset_x_ratio = sticker["offset_x_ratio"]
    offset_y_ratio = sticker["offset_y_ratio"]
    
    out = frame_bgr.copy()
    new_prev = []
    
    h_frame, w_frame, _ = frame_bgr.shape

    for idx, detection in enumerate(results.detections):
        bboxC = detection.location_data.relative_bounding_box
        x = int(bboxC.xmin * w_frame)
        y = int(bboxC.ymin * h_frame)
        w = int(bboxC.width * w_frame)
        h = int(bboxC.height * h_frame)

        target_width = int(w * width_scale)
        sh, sw = sbgr.shape[:2]
        
        if sw == 0: continue
        
        scale = target_width / sw
        th = int(sh * scale)
        
        if target_width > 0 and th > 0:
            rs_bgr = cv2.resize(sbgr, (target_width, th), interpolation=cv2.INTER_AREA)
            rs_alpha = cv2.resize(salpha, (target_width, th), interpolation=cv2.INTER_AREA)
        else:
            continue

        base_cx = x + w // 2
        base_cy = int(y + h * 0.4) 
        
        cx = base_cx + int(target_width * offset_x_ratio)
        cy = base_cy + int(th * offset_y_ratio)
        
        if smooth_on and idx < len(prev_centers):
            cx = int(alpha * cx + (1 - alpha) * prev_centers[idx]["cx"])
            cy = int(alpha * cy + (1 - alpha) * prev_centers[idx]["cy"])
        
        new_prev.append({"cx": cx, "cy": cy})
        out = overlay_sticker_bgr_alpha(out, rs_bgr, rs_alpha, cx, cy)
        
    return out, True, len(results.detections), new_prev

# ==========================
# 7. 필터 함수
# ==========================
def apply_color_filter(frame, filter_type="none"):
    if filter_type == "none":
        return frame
    elif filter_type == "version1":
        frame_float = frame.astype(np.float32)
        frame_float = (frame_float - 128) * 1.2 + 128
        b, g, r = cv2.split(frame_float)
        b = b * 0.9 + 20
        g = g * 1.0 + 10
        r = r * 0.9 + 15
        merged = cv2.merge([b, g, r])
        merged = np.clip(merged, 0, 255).astype(np.uint8)
        merged = cv2.GaussianBlur(merged, (3,3), 0)
        return merged
    elif filter_type == "version2":
        img = frame.astype(np.float32)
        denoised = cv2.bilateralFilter(img, d=5, sigmaColor=35, sigmaSpace=35)
        blur = cv2.GaussianBlur(denoised, (0, 0), sigmaX=1.0)
        sharp = cv2.addWeighted(denoised, 1.85, blur, -0.85, 0)
        b, g, r = cv2.split(sharp)
        r *= 1.10
        g *= 0.98
        b *= 0.99
        b = np.clip(b, 0, 255)
        g = np.clip(g, 0, 255)
        r = np.clip(r, 0, 255)
        pink = cv2.merge([b, g, r]).astype(np.uint8)
        hsv = cv2.cvtColor(pink, cv2.COLOR_BGR2HSV).astype(np.float32)
        h, s, v = cv2.split(hsv)
        s *= 1.06
        v *= 1.12
        h = (h + 0.4) % 180
        s = np.clip(s, 0, 255)
        v = np.clip(v, 0, 255)
        bright = cv2.cvtColor(cv2.merge([h, s, v]).astype(np.uint8), cv2.COLOR_HSV2BGR)
        gamma = 0.94
        lut = np.array([((i / 255.0) ** gamma) * 255 for i in range(256)]).astype("uint8")
        bright_clean = cv2.LUT(bright, lut)
        out = cv2.addWeighted(bright_clean, 0.93, frame, 0.07, 0)
        return out
    elif filter_type == "version3":
        h, w = frame.shape[:2]
        scale = 0.5
        small = cv2.resize(frame, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
        sh, sw = small.shape[:2]
        blurred = cv2.GaussianBlur(small, (9, 9), 0)
        mask = np.zeros((sh, sw), dtype=np.float32)
        center_x, center_y = sw // 2, sh // 2
        radius = int(min(sw, sh) * 0.45)
        cv2.circle(mask, (center_x, center_y), radius, 1.0, -1)
        mask = cv2.GaussianBlur(mask, (0, 0), sigmaX=20, sigmaY=20)
        mask_3 = cv2.merge([mask, mask, mask])
        mix_small = small.astype(np.float32) * mask_3 + blurred.astype(np.float32) * (1 - mask_3)
        mix_small = np.clip(mix_small, 0, 255).astype(np.uint8)
        bright = cv2.addWeighted(mix_small, 1.05, np.zeros_like(mix_small), 0, 5)
        vintage = cv2.resize(bright, (w, h), interpolation=cv2.INTER_LINEAR)
        return vintage
    elif filter_type == "gray":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    elif filter_type == "bright":
        frame = cv2.convertScaleAbs(frame, alpha=1.1, beta=10)
        overlay = np.full(frame.shape, (200, 200, 255), dtype='uint8') 
        return cv2.addWeighted(frame, 0.9, overlay, 0.1, 0)
    elif filter_type == "warm":
        overlay = np.full(frame.shape, (50, 100, 255), dtype='uint8') 
        return cv2.addWeighted(frame, 0.8, overlay, 0.2, 0)
    else:
        return frame

current_filter = "none"

# ==========================
# 8. 웹캠 루프
# ==========================
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("웹캠을 열 수 없습니다.")
prev_centers = []
smooth_on = SMOOTH_ON_DEFAULT
cv2.namedWindow("StickerCam", cv2.WINDOW_NORMAL)

# 사진 저장 폴더 생성
if not os.path.exists("captured_images"):
    os.makedirs("captured_images")

# 카운트다운 관련 변수
COUNTDOWN_SECONDS = 3
countdown_active = False
countdown_start_time = 0.0
last_trigger_time = 0.0
TRIGGER_COOLDOWN = 1.0  # 재촬영 방지 쿨타임

print("웹캠 실행!")
print("   - [스페이스바] 또는 [c]: 카운트다운 촬영")
print("   - [화면 하단 버튼]: 손으로 눌러서 촬영")
print("   - [f]: 필터 변경")
print("   - [1~=]: 스티커 변경")
print("   - [s]: 부드러운 움직임 토글")
print("   - [ESC]: 종료")

saved_message_timer = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    h_frame, w_frame = frame.shape[:2]
    
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # 📸 카메라 버튼 설정 (화면 하단 중앙)
    CAMERA_RADIUS = 30
    camera_btn_pos = (w_frame // 2, h_frame - 60)

    # 손 검출 (메뉴 & 카메라 버튼용)
    hands_results = hands.process(frame_rgb)
    finger_tip = None
    if hands_results.multi_hand_landmarks:
        for hand_landmarks in hands_results.multi_hand_landmarks:
            lm = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            finger_tip = (int(lm.x * w_frame), int(lm.y * h_frame))
            break
            
    # 터치 이벤트 처리
    if finger_tip:
        fx, fy = finger_tip
        
        # 1. 왼쪽 스티커 메뉴 확인
        for item in MENU_ITEMS:
            mx, my = item["pos"]
            dist = np.linalg.norm(np.array([fx, fy]) - np.array([mx, my]))
            if dist < MENU_RADIUS + 10: 
                CURRENT_STICKER = STICKERS[item["key"]]
        
        # 2. 카메라 버튼 확인
        cx, cy = camera_btn_pos
        dist_cam = np.linalg.norm(np.array([fx, fy]) - np.array([cx, cy]))
        now = time.time()
        
        # 버튼을 눌렀고, 카운트다운 중이 아니고, 쿨타임이 지났다면
        if dist_cam < CAMERA_RADIUS and not countdown_active and (now - last_trigger_time > TRIGGER_COOLDOWN):
            countdown_active = True
            countdown_start_time = now
            last_trigger_time = now
            print("카운트다운 시작!")

    # 얼굴 인식 및 스티커 합성
    frame_mask, face_detected, face_cnt, prev_centers = add_mask(frame, prev_centers, smooth_on, SMOOTH_ALPHA)
    
    # 메뉴 점 표시 & 텍스트 출력
    for item in MENU_ITEMS:
        mx, my = item["pos"]
        cv2.circle(frame_mask, (mx, my), MENU_RADIUS, item["color"], -1)
        frame_mask = put_text_pil(frame_mask, item["key"], (mx + 25, my - 10), size=24, color=(255, 255, 255))

    # 필터 적용
    frame_filtered = apply_color_filter(frame_mask, current_filter)

    # 카메라 버튼 그리기 (검은 원 + 흰 테두리)
    cv2.circle(frame_filtered, camera_btn_pos, CAMERA_RADIUS, (0, 0, 0), -1)
    cv2.circle(frame_filtered, camera_btn_pos, CAMERA_RADIUS - 4, (255, 255, 255), 2)

    # 손가락 위치 표시
    if finger_tip:
        cv2.circle(frame_filtered, finger_tip, 6, (0, 255, 0), -1)
        cv2.circle(frame_filtered, finger_tip, 6, (255, 255, 255), 2)

    # 제목 그리기
    frame_filtered = put_text_pil(frame_filtered, "TWELVE ANIMAL CAMERA", (180, 40), size=30, color=(255, 255, 255))

    # 카운트다운 로직
    if countdown_active:
        elapsed = time.time() - countdown_start_time
        remaining = COUNTDOWN_SECONDS - int(elapsed)

        if remaining >= 1:
            # 카운트다운 숫자 표시 (크고 선명하게)
            text = str(remaining)
            font = cv2.FONT_HERSHEY_SIMPLEX
            scale = 4.0
            thickness = 10
            text_size, _ = cv2.getTextSize(text, font, scale, thickness)
            text_w, text_h = text_size
            tx = (w_frame - text_w) // 2
            ty = (h_frame + text_h) // 2

            # 검은색 숫자 카운트다운
           cv2.putText(frame_filtered, text, (tx, ty), font, scale, (0, 0, 0), thickness)
        else:
            # 카운트다운 종료 -> 저장
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"captured_images/photo_{timestamp}.jpg"
            
            # 카운트다운 숫자가 없는 깨끗한 이미지 저장을 위해 필터만 적용된 상태를 저장할 수도 있지만,
            # 현재 프레임 흐름상 여기서는 UI(메뉴점 등)가 포함된 이미지를 저장함.
            # UI 없이 저장하고 싶으면 frame_mask에 필터만 적용한 것을 별도로 저장해야 함.
            # 여기서는 편의상 현재 화면(버튼 등 포함)을 저장.
            cv2.imwrite(filename, frame_filtered)
            print(f"사진 저장됨: {filename}")
            
            countdown_active = False
            saved_message_timer = 30  # "Saved!" 메시지 띄우기

    # 사진 저장 완료 메시지
    if saved_message_timer > 0:
        frame_filtered = put_text_pil(frame_filtered, "Saved!", (w_frame//2 - 100, h_frame//2), size=60, color=(0, 255, 0))
        saved_message_timer -= 1

    cv2.imshow("StickerCam", frame_filtered)

    # 키 입력 처리
    key = cv2.waitKey(1) & 0xFF
    if key == 27: # ESC
        break
    elif key == 32: # Spacebar (즉시 저장)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"captured_images/photo_{timestamp}.jpg"
        cv2.imwrite(filename, frame_filtered)
        print(f"사진 저장됨: {filename}")
        saved_message_timer = 30 
    
    elif key == ord('c'): # 키보드 'c'로도 카운트다운 시작
        if not countdown_active:
            countdown_active = True
            countdown_start_time = time.time()
            last_trigger_time = time.time()

    elif key == ord("s"):
        smooth_on = not smooth_on
        if not smooth_on:
            prev_centers = []
    elif key == ord("1"): CURRENT_STICKER = STICKERS["rat"]
    elif key == ord("2"): CURRENT_STICKER = STICKERS["cow"]
    elif key == ord("3"): CURRENT_STICKER = STICKERS["tiger"]
    elif key == ord("4"): CURRENT_STICKER = STICKERS["rabbit"]
    elif key == ord("5"): CURRENT_STICKER = STICKERS["dragon"]
    elif key == ord("6"): CURRENT_STICKER = STICKERS["snake"]
    elif key == ord("7"): CURRENT_STICKER = STICKERS["horse"]
    elif key == ord("8"): CURRENT_STICKER = STICKERS["sheep"]
    elif key == ord("9"): CURRENT_STICKER = STICKERS["monkey"]
    elif key == ord("0"): CURRENT_STICKER = STICKERS["dog"]
    elif key == ord("-"): CURRENT_STICKER = STICKERS["pig"]
    elif key == ord("="): CURRENT_STICKER = STICKERS["chicken"]
    elif key == ord("f"): 
        filters = ["none", "version1", "version2", "version3", "gray", "bright", "warm"]
        idx = filters.index(current_filter)
        current_filter = filters[(idx + 1) % len(filters)]
        print(f"필터 변경 → {current_filter}")

cap.release()
cv2.destroyAllWindows()
