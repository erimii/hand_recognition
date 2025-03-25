import React, { useState, useEffect } from 'react';

function App() {
  const [gesture, setGesture] = useState(null);  // 손 모양 데이터 저장
  const [loading, setLoading] = useState(true);   // 로딩 상태 표시

  useEffect(() => {
    console.log("📢 useEffect 호출됨 - 데이터 요청 시도 중...");
    const fetchGesture = async () => {
      try {
        const response = await fetch('http://localhost:5000/hand-recognition', {  // Flask 서버 URL
          method: 'POST'
        });

        const data = await response.json();  // JSON 데이터 파싱

        if (data.result) {
          setGesture(data);  // 손 모양 데이터 저장
          console.log("받아온 데이터:", data);  // 콘솔로 데이터 확인
        }
        setLoading(false);
      } catch (error) {
        console.error('오류 발생:', error);
        setLoading(false);
      }
    };

    fetchGesture();  // React 앱이 시작되면 데이터를 가져옴
  }, []);  // 빈 배열을 사용하여 컴포넌트가 마운트될 때 한 번만 실행

  return (
    <div className="App">
      <h1>손 제스처 인식 시스템</h1>
      
      {loading && <p>카메라 실행 중...</p>}
      
      {gesture && (
        <div>
          <h2>인식된 동작: {gesture.result}</h2>
          <p>동작 인덱스: {gesture.index}</p>
        </div>
      )}
    </div>
  );
}

export default App;
