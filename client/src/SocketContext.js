import { createContext } from "react";
import ioClient from "socket.io-client";

const url = "http://localhost:5000";
export const socket = ioClient(url, {});
export const SocketContext = createContext(socket);
