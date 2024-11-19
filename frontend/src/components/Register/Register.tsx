import "./Register.css";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { register } from "../../services/authServices";

const colleges = [
  { id: 1, name: "Institution 1" },
  { id: 2, name: "Institution 2" },
  { id: 3, name: "Institution 3" },
];

export default function Signup() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [institution, setInstitution] = useState(colleges[0].id);
  const [error, setError] = useState({ success: false, error: "" });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const formData = { username, email, password, institution };
    try {
      const result = await register(formData);
      if (result.success) {
        console.log("Registro bem-sucedido:", result.data);
        navigate("/dashboard");
      } else {
        console.error("Erro ao registrar:", result.error);
        setError(result.error);
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
    <div className="signup-container">
      <h2>Sign Up</h2>
      <form className="signup-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="username">Username</label>
          <input
            type="text"
            id="username"
            name="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
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
          <label htmlFor="institution">Institution</label>
          <select
            id="institution"
            name="institution"
            value={institution}
            onChange={(e) => setInstitution(Number(e.target.value))}
            required
          >
            {colleges.map((colleges) => (
              <option key={colleges.id} value={colleges.id}>
                {colleges.name}
              </option>
            ))}
          </select>
        </div>
        <button type="submit" className="signup-button">
          Sign Up
        </button>
        <p>
          If you already have an account <a href="login">click here</a>
        </p>
      </form>
    </div>
  );
}
