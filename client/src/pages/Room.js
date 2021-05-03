import { useState, useEffect, useContext } from "react";
import { useHistory, useParams } from "react-router-dom";
import axios from "axios";
import { SocketContext } from "../SocketContext";

export default function Room(props) {
  //const history = useHistory();
  const { code } = useParams();
  const [messages, setMessages] = useState([]);
  const [message, setMessage] = useState("");
  const [users, setUsers] = useState([]);

  const socket = useContext(SocketContext);

  const fetchMessages = async () => {
    const res = await axios.get(`/api/messages/${code}`);
    setMessages(res.data.messages);
  };

  useEffect(() => {
    fetchMessages();
    props.user &&
      socket.emit("join", {
        code,
        username: props.user?.username,
        socketId: socket.id,
      });
    socket.on("new message", newMessageHandler);
    socket.on("room users", roomUsersHandler);

    return () => {
      socket.off("new message", newMessageHandler);
      socket.off("room users", roomUsersHandler);
    };
  }, []);

  const roomUsersHandler = ({ room_users }) => setUsers(room_users);

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
    <div className="display-grid-center">
      <div>
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
    </div>
  );
}
