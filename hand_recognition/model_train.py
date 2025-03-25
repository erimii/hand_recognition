import os
import pickle
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

# 현재 경로 설정 (현재 파일 위치 기준)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# 모델 파일을 저장할 경로 설정
MODEL_DIR = os.path.join(BASE_DIR, 'model')
MODEL_PATH = os.path.join(MODEL_DIR, 'knn_model.pkl')

# 학습 데이터 파일 경로 설정
DATA_DIR = os.path.join(BASE_DIR, 'data')
DATA_PATH = os.path.join(DATA_DIR, 'gesture_train.csv')

# 모델 폴더가 없으면 자동으로 생성하기
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)
    print(f"모델 폴더가 생성되었습니다: {MODEL_DIR}")

# 데이터 파일이 존재하는지 확인하기
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"데이터 파일이 존재하지 않습니다: {DATA_PATH}")

# 데이터 파일 불러오기
file = np.genfromtxt(DATA_PATH, delimiter = ',')
X = file[:, :-1].astype(np.float32)
y = file[:, -1].astype(np.float32)
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X, y)

# 학습된 모델 저장하기
try:
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(knn, f)
except Exception as e:
    print(f"모델 저장 중 오류 발생: {e}")
