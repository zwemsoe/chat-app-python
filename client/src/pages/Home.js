import { useState, useEffect } from "react";
import { useHistory, Link } from "react-router-dom";
import axios from "axios";

export default function Home(props) {
  const history = useHistory();
  const [joinCode, setJoinCode] = useState("");
  const [rooms, setRooms] = useState([]);

  const logout = async () => {
    await axios.get("/api/logout");
    window.location.reload();
  };

  const joinRoom = () => {
    if (props.user) {
      history.push("/room/" + joinCode);
    }
  };

  const fetchRooms = async () => {
    const res = await axios.get(`/api/rooms/${props.user.username}`);
    if (res.data.success) {
      setRooms(res.data.rooms);
    }
  };

  useEffect(() => {
    fetchRooms();
  }, []);

  const leaveRoom = async (roomcode) => {
    const res = await axios.post(`/api/leaveRoom`, {
      roomcode,
      username: props.user.username,
    });
    if (res.data.success) {
      window.location.reload();
    }
  };

  const deleteRoom = async (roomcode) => {
    const res = await axios.post(`/api/deleteRoom`, {
      roomcode,
      username: props.user.username,
    });
    if (res.data.success) {
      window.location.reload();
    }
  };

  return (
    <>
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
          <ul>
            {rooms.map((room, i) => {
              if (room.createdby !== props.user.username) {
                return (
                  <div key={room.roomcode}>
                    <a href={`/room/${room.roomcode}`}>
                      <li>{room.roomcode}</li>
                    </a>
                    <button onClick={() => leaveRoom(room.roomcode)}>
                      Leave
                    </button>
                  </div>
                );
              }
            })}
          </ul>
          <div>Your Rooms: </div>
          <ul>
            {rooms.map((room, i) => {
              if (room.createdby === props.user.username) {
                return (
                  <div key={room.roomcode}>
                    <a href={`/room/${room.roomcode}`}>
                      <li>{room.roomcode}</li>
                    </a>
                    <button onClick={() => deleteRoom(room.roomcode)}>
                      Delete
                    </button>
                  </div>
                );
              }
            })}
          </ul>
        </div>
      )}
    </>
  );
}
