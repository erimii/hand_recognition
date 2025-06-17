
# ✋ Hand Gesture Recognition Web App

React + Flask 기반의 손 제스처 인식 웹 애플리케이션입니다.  
웹캠으로 손 모양을 인식하고, 이를 서버에 전달하여 제스처를 예측한 뒤 결과를 화면에 출력합니다.

---

## 주요 기능

- MediaPipe Hands를 활용한 실시간 손 관절 추적
- KNN 기반 제스처 예측 (Flask 서버에서 처리)
- 손 모양 인식되면 카메라 자동 종료
- 버튼 클릭 시 카메라 다시 실행되어 제스처 재인식 가능
- 제스처 결과는 UI 상에 바로 출력

---

## 사용 기술

### Frontend (React)
- React 18
- @mediapipe/hands
- JavaScript + Hooks (useRef, useEffect, useState)

### Backend (Flask)
- Flask
- Flask-CORS
- NumPy
- Scikit-learn (KNN 모델)
- Python 3.10+

---

## 주의 사항

> 학습된 KNN 모델(`knn_model.pkl`)이 필요합니다.

> `public/index.html`에는 MediaPipe의 `camera_utils.js`를 CDN으로 포함해야 합니다:

---

## 전체 흐름

1. React에서 `<video>`로 웹캠 스트림 출력
2. MediaPipe로 손 관절 21개 추적
3. 좌표 데이터를 Flask 서버로 전송
4. 서버에서 각도 계산 → KNN 모델로 제스처 예측
5. React에 결과 반환 → 카메라 종료 + 결과 표시
6. 사용자가 '다시 인식하기' 클릭 시 → 카메라 재시작

---

## 화면 예시

<img src="https://github.com/user-attachments/assets/3c6b066d-2854-4362-bc1a-cde42a6bd3ea" width="300"/>

<img src="https://github.com/user-attachments/assets/3a709f69-c886-4f13-b0cd-f636d75b7363" width="500"/>

