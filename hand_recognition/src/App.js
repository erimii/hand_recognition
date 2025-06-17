import React, { useState, useEffect } from 'react';
import HandRecognizer from "./recognizer";

function App() {

  return (
    <div className="App">
      <h1>손 제스처 인식 테스트</h1>
      <HandRecognizer />
    </div>

  );
}

export default App;
