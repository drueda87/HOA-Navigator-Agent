import React from "react";
import MapComponent from "./components/MapComponents.js";  // ✅ Correct path
import hoaIcon from "./components/hoa-icon.png"; // ✅ Import image

function App() {
  return (
    <div>
      <header className="hoa-header">
        <img src={hoaIcon} alt="HOA Icon" className="hoa-icon" />
        <h1 className="hoa-title">HOA Navigator</h1>
      </header>
      <MapComponent />
    </div>
  );
}

export default App;