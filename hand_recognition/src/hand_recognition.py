# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 16:24:14 2025

@author: Admin
"""


import os
import cv2
import mediapipe as mp
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from flask import Flask, jsonify, request
from flask_cors import CORS
import pickle  # pickle을 사용해 모델 파일 불러오기
import time

app = Flask(__name__)
CORS(app)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '../model/knn_model.pkl')

# 모델 불러오기
try:
    with open(MODEL_PATH, 'rb') as f:
        knn = pickle.load(f)

except Exception as e:
    print(f"모델 불러오기 오류 발생: {e}")
    exit()  # 모델을 불러오지 못하면 프로그램 종료

@app.route('/hand-recognition', methods=['POST'])
def hand_recognition():
    rsp = {
        0:'rock', 5 : 'paper', 9: 'scissors', 10:'ok'
    }

    # 인식 지속 시간 설정 (초)
    REQUIRED_DURATION = 3.0  
    last_gesture = None
    start_time = None

    # mediapipe 사용하기
    # 손 찾기 관련 기능 불러오기
    mp_hands = mp.solutions.hands
    # 손 그려주는 기능 불러오기
    mp_drawing = mp.solutions.drawing_utils
    # 손 찾기 관련 세부 설정
    hands = mp_hands.Hands(
        max_num_hands = 1, # 탐지할 최대 손의 갯수
        model_complexity=0,
        min_detection_confidence = 0.7, # 표시할 손의 최소 정확도
        min_tracking_confidence = 0.7 # 표시할 관절의 최소 정확도
    )

    video = cv2.VideoCapture(0)
    if not video.isOpened():
        return jsonify({"error": "카메라를 열 수 없습니다."})
    
    while video.isOpened() :
        # ret: 프레임 제대로 읽었는지 T/F img: 현재 프레임을 읽어서 저장
        ret, img = video.read()
        # 이미지 좌우 반전
        img = cv2.flip(img,1)
        # 파이썬이 인식 잘 하도록 BGR → RGB로 변경
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # 손 탐지하기(특짐정 추출)
        result = hands.process(img)

        # 다시 BGR 형식으로 변환
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # 연결에 문제 있으면 프로그램 종료
        if not ret :
            break

        # 찾은 손 표시하기
        if result.multi_hand_landmarks is not None :
            # print(result.multi_hand_landmarks)
            # 이미지에 손 표현하기
            for res in result.multi_hand_landmarks :
                joint = np.zeros((21, 3)) # 21개 관절, xyz값 저장할 3차원 배열 생성
                
                # 모든 관절 좌표값 저장
                for j, lm in enumerate(res.landmark) :
                    # 각 관절의 상대적인 좌표값 (0~1 범위)
                    # 예를 들어 joint[0]은 손목 위치(Wrist) 를 의미하고 (x, y, z) 로 저장
                    joint[j] = [lm.x, lm.y, lm.z]
                
                # 손의 관절 간 연결을 표현하기 위해 번호 배열 정의
                v1 = joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19],:]
                v2 = joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],:]
                v = v2 - v1 # 뼈의 값(x, y, z좌표값 → 벡터값)
                # 유클리디안 길이로 변환(피타고라스)
                # 정규화
                v = v / np.linalg.norm(v, axis = 1)[:, np.newaxis]

                # 뼈의 값으로 뼈 사이의 각도 구하기, 변화값이 큰 15개
                angle = np.arccos(np.einsum('nt,nt->n',
                    v[[0,1,2,4,5,6,8,9,10,12,13,14,16,17,18],:], 
                    v[[1,2,3,5,6,7,9,10,11,13,14,15,17,18,19],:]))
                # radian 각도를 degree 각도로 변경하기
                angle = np.degrees(angle)

                # 구한 각도를 knn 모델에 예측시키기
                # 학습을 위한 타입 변경(2차원 array)
                X_pred = np.array([angle], dtype = np.float32)
                
                try:
                    results = knn.predict(X_pred)
                    idx = int(results[0])  # 배열의 첫 번째 값 추출 후 변환
                    
                    # 인식된 제스쳐 표현하기
                    img_x = img.shape[1]
                    img_y = img.shape[0]
                    hand_x = res.landmark[0].x
                    hand_y = res.landmark[0].y
                    # 가위, 바위, 보, 오케이 동작 인식하기
                    if idx in rsp.keys() :
                        cv2.putText(img, text = rsp[idx].upper(),
                                org = (int(hand_x * img_x), int(hand_y * img_y)+20),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 255, 255), thickness=2
                            )
                    mp_drawing.draw_landmarks(img, res, mp_hands.HAND_CONNECTIONS)

                    if idx in rsp.keys():  # 인식된 손 모양이 rsp에 있는 경우만 실행
                        current_gesture = rsp[idx]
                        
                        # 동일한 손 모양이 지속되면 시간을 측정하기 시작
                        if last_gesture == current_gesture:
                            if start_time is None:  # 타이머가 설정되지 않은 경우 설정
                                start_time = time.time()
                            elif time.time() - start_time >= REQUIRED_DURATION:
                                print(f"{current_gesture} finish!! ")
                                video.release()
                                cv2.destroyAllWindows()
                                with app.app_context():  # Flask 앱 컨텍스트 활성화
                                    return jsonify({"result": current_gesture, "index": idx})
                        else:
                            # 새로운 손 모양이 인식된 경우 타이머 초기화
                            last_gesture = current_gesture
                            start_time = time.time()  # 새로운 손 모양으로 타이머 리셋
                        
                except Exception as e:
                    print(f"error : {e}")
                    continue
                
        k = cv2.waitKey(30)
        if k == ord('q') :
            break
        cv2.imshow('hand', img)

    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    app.run(port=5000)
