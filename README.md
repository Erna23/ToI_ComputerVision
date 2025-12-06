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

## ✨ Key Features
| 기능 (Function) | 설명 (Description) |
|:---:|:---|
| **🐭 12 Zodiac Stickers** | 쥐, 소, 호랑이 등 12가지 동물 스티커가 얼굴 각도에 맞춰 자연스럽게 합성됩니다. |
| **👆 Touch UI** | 화면 좌측 메뉴와 하단 촬영 버튼을 **손가락 검지**로 터치하여 제어합니다. |
| **🎨 Live Filters** | 빈티지, 화사함, 흑백 등 7가지 다양한 색감 필터를 실시간으로 적용합니다. |
| **📸 Smart Capture** | 손가락으로 버튼을 누르면 3초 카운트다운 후 사진이 자동 저장됩니다. |

## 🛠️ Tech Stack
- **Language**: Python 3.11+
- **Computer Vision**: OpenCV (`cv2`), MediaPipe (Face Detection, Hands)
- **Image Processing**: NumPy, PIL (한글 폰트 지원)
<p align="center"> <img src="https://img.shields.io/badge/MediaPipe-Face%20Detection-orange?logo=google" /> <img src="https://img.shields.io/badge/MediaPipe-Hands-orange?logo=google" /> <img src="https://img.shields.io/badge/OpenCV-4.x-green?logo=opencv" /> <img src="https://img.shields.io/badge/Pillow-PIL-blue" /> <img src="https://img.shields.io/badge/NumPy-Array%20Ops-lightgrey?logo=numpy" /> </p> <table> <tr> <th>기술</th> <th>역할</th> </tr> <tr> <td><strong>MediaPipe Face Detection</strong></td> <td>얼굴 위치 인식 및 스티커 기준 좌표 계산</td> </tr> <tr> <td><strong>MediaPipe Hands</strong></td> <td>검지손가락 위치 추적 및 가상 버튼 클릭 처리</td> </tr> <tr> <td><strong>OpenCV</strong></td> <td>웹캠 캡처, 스티커 합성, 필터 처리, UI 렌더링</td> </tr> <tr> <td><strong>Pillow</strong></td> <td>한글 포함 텍스트 렌더링 (UI 요소)</td> </tr> <tr> <td><strong>NumPy</strong></td> <td>알파 블렌딩 및 이미지 배열 연산</td> </tr> </table>

