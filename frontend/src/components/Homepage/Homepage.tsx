import React from "react";
import { useNavigate } from "react-router-dom";
import { logout } from "../../services/authServices";
import "./Homepage.css";

export default function HomePage() {
  const navigate = useNavigate();

  const handleLogout = async () => {
    const result = await logout();
    if (result.success) {
      navigate("/login");
    } else {
      alert(`Logout failed: ${result.error}`);
    }
  };

  return (
    <div className="homepage">
      <h1>Welcome</h1>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
}
