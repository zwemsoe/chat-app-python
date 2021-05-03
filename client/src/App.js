import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Room from "./pages/Room";
import axios from "axios";
import { useState, useEffect } from "react";
import { SocketContext, socket } from "./SocketContext";
import ProtectedRoute from "./ProtectedRoute";

function App() {
  const [user, setUser] = useState(null);

  const authenticate = async () => {
    const res = await axios.get("/api/user");
    console.log(res.data.data);
    const { data } = res.data;
    setUser(data);
  };

  useEffect(() => {
    authenticate();
  }, []);

  return (
    <Router>
      <SocketContext.Provider value={socket}>
        <Switch>
          {/* <Route exact path="/" component={() => <Home user={user} />} />
          <Route
            exact
            path="/room/:code"
            component={() => <Room user={user} />}
          />
          <Route
            exact
            path="/login"
            component={() => <Login setUser={setUser} />}
          />
          <Route exact path="/register" component={Register} /> */}
          <ProtectedRoute
            exact
            path="/"
            component={() => <Home user={user} />}
            template={"afterLogin"}
            auth={user}
          />
          <ProtectedRoute
            path="/register"
            exact
            component={Register}
            template={"beforeLogin"}
            auth={user}
          />
          <ProtectedRoute
            path="/login"
            exact
            component={() => <Login setUser={setUser} />}
            template={"beforeLogin"}
            auth={user}
          />
          <ProtectedRoute
            exact
            path="/room/:code"
            component={() => <Room user={user} />}
            template={"afterLogin"}
            auth={user}
          />
          <Route path="*" component={() => <div>PAGE NOT FOUND</div>} />
        </Switch>
      </SocketContext.Provider>
    </Router>
  );
}

export default App;
