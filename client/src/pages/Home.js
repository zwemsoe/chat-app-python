import { useState } from "react";
import { useHistory } from "react-router-dom";
import axios from "axios";

export default function Home(props) {
  const history = useHistory();
  const [joinCode, setJoinCode] = useState("");

  const logout = async () => {
    await axios.get("/api/logout");
    window.location.reload();
  };

  const joinRoom = () => {
    if (props.user) {
      history.push("/room/" + joinCode);
    }
  };

  return (
    <div>
      <div className="display-grid-center">
        <input type="text" onChange={(e) => setJoinCode(e.target.value)} />
        <button onClick={joinRoom}>Join Room</button>
        <div>
          <p>{props.user?.name}</p>
          {props.user && <button onClick={logout}>Logout</button>}
        </div>
      </div>
      {props.user && (
        <div className="display-grid-center">
          <div>Joined Rooms: </div>
        </div>
      )}
    </div>
  );
}
