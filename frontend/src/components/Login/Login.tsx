import { useState } from "react";
import "./Login.css";
import { useNavigate } from "react-router-dom";
import { login } from "../../services/authServices";

export default function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState({ success: false, error: "" });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const formData = { email, password };
    try {
      const data = await login(formData);
      if (data.success) {
        console.log("Registro bem-sucedido:", data.data);
        navigate("/dashboard");
      } else {
        console.error("Erro ao registrar:", data.error);
        setError(data.error);
      }
    } catch (err) {
      console.error("Erro ao registrar:", err);
      if (err instanceof Error) {
        setError({ success: false, error: err.message });
      } else {
        setError({ success: false, error: "Erro desconhecido" });
      }
    }
  };
  return (
    <div className="login-container">
      <h2>Login</h2>
      <form className="login-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            name="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="login-button">
          Login
        </button>
        <p>
          If you don't have an account <a href="register">click here</a>
        </p>
      </form>
    </div>
  );
}
