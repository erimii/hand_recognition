import os
import numpy as np
import pickle
from sklearn.neighbors import KNeighborsClassifier

# 데이터 파일 경로 설정
csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'gesture_train.csv')

# 데이터 로드 및 모델 학습
file = np.genfromtxt(csv_path, delimiter=',')
X = file[:, :-1].astype(np.float32)
y = file[:, -1].astype(np.float32)
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X, y)

# 모델 저장하기
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'gesture_model.pkl')
with open(model_path, 'wb') as f:
    pickle.dump(knn, f)

print(f"success!!!!!! {model_path}")
