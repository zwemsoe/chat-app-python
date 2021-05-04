import { useState, useEffect, useContext } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import { SocketContext } from "../SocketContext";

export default function Room(props) {
  const { code } = useParams();
  const [messages, setMessages] = useState([]);
  const [message, setMessage] = useState("");
  const [onlineUsers, setOnlineUsers] = useState([]);
  const [notOnlineUsers, setNotOnlineUsers] = useState([]);
  const socket = useContext(SocketContext);

  const fetchMessages = async () => {
    const res = await axios.get(`/api/messages/${code}`);
    setMessages(res.data.messages);
  };

  useEffect(() => {
    fetchMessages();
    emitJoinEvent();

    socket.on("new message", newMessageHandler);
    socket.on("room users", roomUsersHandler);
    return () => {
      socket.off("new message", newMessageHandler);
      socket.off("room users", roomUsersHandler);
    };
  }, []);

  const emitJoinEvent = () => {
    socket.emit("join", {
      code,
      username: props.user?.username,
      socketId: socket.id,
    });
  };

  const roomUsersHandler = ({ online, not_online }) => {
    setOnlineUsers(online);
    setNotOnlineUsers(not_online);
  };

  const newMessageHandler = (msg) =>
    setMessages((messages) => messages.concat(msg));

  const sendMessage = () => {
    if (message) {
      socket.emit("send message", {
        message,
        code,
        username: props.user?.username,
        socketId: socket.id,
      });
    }
  };

  return (
    <div className="row">
      <div className="col-10 display-grid-center">
        <div className="row">
          <textarea
            rows="4"
            cols="50"
            placeholder="Type message"
            onChange={(e) => setMessage(e.target.value)}
          />
          <button onClick={sendMessage}>Send</button>
        </div>
        <div className="row">
          {messages.length == 0 ? (
            <p>Send first message to the room.</p>
          ) : (
            <ul>
              {messages.map((msg, i) => {
                return (
                  <p key={i} style={{ textAlign: "center" }}>
                    {msg.content}{" "}
                    <mark
                      style={{
                        backgroundColor:
                          msg.sender == props.user?.username
                            ? "dodgerblue"
                            : "lightgray",
                      }}
                    >
                      {msg.sender}
                    </mark>
                  </p>
                );
              })}
            </ul>
          )}
        </div>
      </div>
      <div className="col-2">
        <h2>Online Users</h2>
        <ul>
          {onlineUsers.map((user) => (
            <li key={user}>{user}</li>
          ))}
        </ul>
        <h2>Inactive Users</h2>
        <ul>
          {notOnlineUsers.map((user) => (
            <li key={user}>{user}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
