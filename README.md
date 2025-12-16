# ToI_ComputerVision
Computer Vision Study &amp; Practice with Google Colab, OpenCV, VSCode

<div align="center">

# 🐭 Twelve Animal Face Camera 📸
### 십이지신 스티커 & 핸드 제스처 인터랙티브 카메라

<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white"/>
<img src="https://img.shields.io/badge/MediaPipe-00BFFF?style=flat-square&logo=google&logoColor=white"/>
<img src="https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white"/>

<br/>

<img src="assets/demo.gif" width="600">

<br/>
<br/>

**"내 얼굴에 찰떡인 십이지신 동물은?"** <br/>
손가락 제스처로 스티커를 바꾸고, 필터를 입혀 인생샷을 남겨보세요!

</div>

<br/>

## 📝 Project Overview
이 프로젝트는 **OpenCV**와 **MediaPipe**를 활용한 실시간 얼굴 인식 스티커 애플리케이션입니다.

단순한 합성을 넘어, **Hand Tracking**을 통해 마우스나 키보드 없이 **손동작만으로 UI를 제어**할 수 있는 인터랙티브한 경험을 제공합니다.

## 📱 시연 이미지

<p align="center">
  <img width="466" alt="image" src="https://github.com/user-attachments/assets/9a39e1f1-389e-4885-9a2a-2ee19cae6ebb">
  <br>
  <em>실제 앱 구동 화면입니다.</em>
</p>

## ✨ Key Features
| 기능 (Function) | 설명 (Description) |
|:---:|:---|
| **🐭 12 Zodiac Stickers** | 쥐, 소, 호랑이 등 12가지 동물 스티커가 얼굴 각도에 맞춰 자연스럽게 합성됩니다. |
| **👆 Touch UI** | 화면 좌측 메뉴와 하단 촬영 버튼을 **손가락 검지**로 터치하여 제어합니다. |
| **🎨 Live Filters** | 빈티지, 화사함, 흑백 등 7가지 다양한 색감 필터를 실시간으로 적용합니다. |
| **📸 Smart Capture** | 손가락으로 버튼을 누르거나 C 키를 누르면 3초 카운트다운 후 사진이 자동 저장됩니다. |

## 🛠️ Tech Stack

| 기술 (Tech) | 역할 (Role) |
|:---:|:---|
| **🤖 MediaPipe Face** | 얼굴 위치를 실시간으로 인식하고 스티커가 붙을 좌표(중심점)를 계산 |
| **✋ MediaPipe Hands** | 검지 손가락 끝(`INDEX_FINGER_TIP`)을 추적하여 허공 터치(가상 클릭) 구현 |
| **📷 OpenCV** | 웹캠 영상 캡처, 스티커 합성, 이미지 필터링 및 전체적인 화면 처리 |
| **🎨 Pillow (PIL)** | OpenCV에서 지원하지 않는 **텍스트**(UI 메뉴, 안내 메시지)를 깨짐 없이 렌더링 |
| **🔢 NumPy** | 투명 배경(Alpha Channel)이 있는 스티커 이미지를 자연스럽게 합성하기 위한 배열 연산 |

