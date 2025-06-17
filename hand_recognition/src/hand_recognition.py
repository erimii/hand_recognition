import os
import cv2
import mediapipe as mp
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from flask import Flask, jsonify, request
from flask_cors import CORS
import pickle
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
    exit()

rsp = {
        0:'rock', 5 : 'paper', 9: 'scissors', 10:'ok'
    }

@app.route('/predict_gesture', methods=['POST'])
def predict_gesture():
    data = request.get_json()
    joint = np.array(data['joints'])  # (21, 3)

    try:
        v1 = joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19], :]
        v2 = joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], :]
        v = v2 - v1
        v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

        angle = np.arccos(np.einsum('nt,nt->n',
                    v[[0,1,2,4,5,6,8,9,10,12,13,14,16,17,18],:], 
                    v[[1,2,3,5,6,7,9,10,11,13,14,15,17,18,19],:]))
        angle = np.degrees(angle)
        X_pred = np.array([angle], dtype=np.float32)

        result = knn.predict(X_pred)
        gesture = rsp[int(result[0])]
        print(f"인식된 제스처: {gesture}")
        return jsonify({"result": gesture})
    except Exception as e:
        print("예측 오류:", e)
        return jsonify({"result": "error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
