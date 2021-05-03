import { useState } from "react";
import { useHistory } from "react-router-dom";
import axios from "axios";

export default function Register(props) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [error, setError] = useState("");
  const history = useHistory();

  const handleRegister = async () => {
    const res = await axios.post("/api/register", { username, password, name });
    if (res.data.success) {
      history.push("/login");
    } else {
      setError("User already exists");
    }
  };

  return (
    <div className="display-grid-center">
      <div>
        <h1>Register</h1>
        <p style={{ color: "red" }}>{error}</p>
        <input
          type="text"
          placeholder="Name"
          onChange={(e) => setName(e.target.value)}
        />
        <input
          type="text"
          placeholder="Username"
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={handleRegister}>Register</button>
      </div>
    </div>
  );
}
