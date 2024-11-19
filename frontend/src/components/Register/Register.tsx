import "./Register.css";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { register } from "../../services/authServices";

const institutions = [
  { id: 1, name: "Institution 1" },
  { id: 2, name: "Institution 2" },
  { id: 3, name: "Institution 3" },
];

export default function Signup() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [selectedInstitution, setSelectedInstitution] = useState(
    institutions[0].id
  );

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const formData = { username, email, password, selectedInstitution };
      const data = await register(formData);
      console.log("Login bem-sucedido:", data);

      // Redireciona o usuário após login bem-sucedido
      navigate("/dashboard");
    } catch (error) {
      alert("Error registering.");
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
            value={selectedInstitution}
            onChange={(e) => setSelectedInstitution(Number(e.target.value))}
            required
          >
            {institutions.map((institution) => (
              <option key={institution.id} value={institution.id}>
                {institution.name}
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
