import { useState } from "react";
import { useHistory } from "react-router-dom";
import axios from "axios";

export default function Login(props) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const history = useHistory();

  const handleLogin = async () => {
    const res = await axios.post("/api/login", { username, password });
    if (res.data.success) {
      props.setUser(res.data.data);
      history.push("/");
    } else {
      setError("Password doesn't match or wrong username.");
    }
  };

  return (
    <div className="display-grid-center">
      <div>
        <h1>Login</h1>
        <p style={{ color: "red" }}>{error}</p>
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
        <button onClick={handleLogin}>Login</button>
        <a href="/register">Create new account</a>
      </div>
    </div>
  );
}
