import React from "react";
import "./App.css";
import { Route, Routes } from "react-router-dom";
import HomePage from "./components/Homepage/Homepage";

function App() {
  return (
    <div>
      <Routes>
        {/* Directly define the HomePage as the default route */}
        <Route path="/" element={<HomePage />} />
      </Routes>
    </div>
  );
}

export default App;
