import React from "react";
import MapComponent from "./components/MapComponents.js";  // ✅ Correct path

function App() {
  return (
    <div>
      <h1>HOA Navigator</h1>
      <MapComponent />  {/* ✅ Ensure this appears only once */}
    </div>
  );
}

export default App;