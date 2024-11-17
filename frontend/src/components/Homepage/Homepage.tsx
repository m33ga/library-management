import { useNavigate } from "react-router-dom";
import "./Homepage.css";

export default function HomePage() {
  const navigate = useNavigate();

  const handleLoginClick = () => {
    navigate("/login");
  };

  return (
    <div className="homepage">
      <h1>Bem-vindo à Biblioteca</h1>
      <button onClick={handleLoginClick}>Login</button>
    </div>
  );
}