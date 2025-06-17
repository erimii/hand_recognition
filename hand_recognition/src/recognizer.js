import React, { useRef, useEffect, useState } from "react";
import { Hands } from "@mediapipe/hands";

function HandRecognizer() {
  const videoRef = useRef(null);
  const cameraRef = useRef(null);
  const [gesture, setGesture] = useState("");
  const [isCameraActive, setIsCameraActive] = useState(true); // 카메라 활성 상태

  // 카메라 시작 함수
  const startCamera = () => {
    if (!videoRef.current) return;

    const hands = new Hands({
      locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`,
    });

    hands.setOptions({
      maxNumHands: 1,
      modelComplexity: 1,
      minDetectionConfidence: 0.8,
      minTrackingConfidence: 0.8,
    });

    hands.onResults((results) => {
      if (
        results.multiHandLandmarks &&
        results.multiHandLandmarks.length > 0
      ) {
        const joints = results.multiHandLandmarks[0].map((lm) => [
          lm.x,
          lm.y,
          lm.z,
        ]);
        sendToServer(joints);
      }
    });

    const cam = new window.Camera(videoRef.current, {
      onFrame: async () => {
        await hands.send({ image: videoRef.current });
      },
      width: 640,
      height: 480,
    });

    cameraRef.current = cam;
    cam.start();
  };

  // 최초 실행
  useEffect(() => {
    if (!isCameraActive) return;
  
    const timer = setInterval(() => {
      if (videoRef.current) {
        clearInterval(timer);  // 준비된 시점에서 camera 시작
        startCamera();
      }
    }, 100);  // 100ms 간격으로 체크
  
    return () => clearInterval(timer);
  }, [isCameraActive]);
  
  // 제스처 결과 전송
  const sendToServer = (joints) => {
    if (gesture) return;

    fetch("http://localhost:5000/predict_gesture", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ joints }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.result) {
          setGesture(data.result);
          setIsCameraActive(false); // 카메라 비활성화
          if (cameraRef.current) {
            cameraRef.current.stop();
          }
        }
      });
  };

  // 다시 인식 버튼
  const handleReset = () => {
    setGesture("");
    setIsCameraActive(true); // 카메라 재시작
  };

  return (
    <div style={{ textAlign: "center" }}>
      <h1>손 제스처 인식 테스트</h1>

      {isCameraActive && (
        <video
          ref={videoRef}
          autoPlay
          style={{ width: 640, height: 480 }}
        />
      )}

      <h2 style={{ marginTop: "1rem" }}>
        {gesture ? `🎉 인식된 제스처: ${gesture}` : "제스처 인식 중..."}
      </h2>

      {gesture && (
        <button onClick={handleReset} style={{ marginTop: "1rem", padding: "10px 20px", fontSize: "16px" }}>
          다시 인식하기
        </button>
      )}
    </div>
  );
}

export default HandRecognizer;
