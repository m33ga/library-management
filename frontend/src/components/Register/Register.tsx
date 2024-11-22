import "./Register.css";
import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { register, getInstitutions } from "../../services/authServices";

interface Institution {
  id: number;
  name: string;
}

export default function Signup() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [institution, setInstitution] = useState<number | null>(null);
  const [institutions, setInstitutions] = useState<Institution[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchInstitutions = async () => {
      try {
        const result = await getInstitutions();
        if (result.success && result.data) {
          setInstitutions(result.data);
          if (result.data.length > 0) {
            setInstitution(result.data[0].id);
          }
        } else {
          console.error("Failed to fetch institutions:", result.error);
          setError("Failed to fetch institutions. Please try again later.");
        }
      } catch (err) {
        console.error("Error fetching institutions:", err);
        setError("An unexpected error occurred while fetching institutions.");
      }
    };

    fetchInstitutions();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!institution) {
      setError("Please select a valid institution.");
      return;
    }

    const formData = { username, email, password, institution };
    console.log("Form Data:", formData);

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
        setError(err.message);
      } else {
        setError("Erro desconhecido");
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
            value={institution || ""}
            onChange={(e) => setInstitution(Number(e.target.value))}
            required
          >
            <option value="" disabled>
              Select an institution
            </option>
            {institutions.map((inst) => (
              <option key={inst.id} value={inst.id}>
                {inst.name}
              </option>
            ))}
          </select>
        </div>
        <span>{error}</span>
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
