import React from "react";
import "./App.css";
import { Route, Routes } from "react-router-dom";
import HomePage from "./components/Homepage/Homepage";
import Login from "./components/Login/Login";

function App() {
  return (
    <div>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </div>
  );
}

export default App;
