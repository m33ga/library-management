import { useState } from "react";
import "./Login.css";
import { useNavigate } from "react-router-dom";
import { login } from "../../services/authServices";

export default function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    try {
      const formData = { email, password };
      const data = await login(formData);
      console.log("Login bem-sucedido:", data);

      // Redireciona o usuário após login bem-sucedido
      navigate("/");
    } catch (error) {
      console.log(error);
      alert("Error logging in. Check your credentials.");
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
