import React from "react";
import logo from "./logo.svg";
import "./App.css";
import { Route, Switch, Link } from "react-router-dom";
import Overview from "./components/Overview";
import Picks from "./components/Picks";

// check permissions of user
function parseJwt(token) {
  // https://stackoverflow.com/questions/38552003/how-to-decode-jwt-token-in-javascript
  var base64Url = token.split(".")[1];
  var base64 = decodeURIComponent(
    atob(base64Url)
      .split("")
      .map((c) => {
        return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
      })
      .join("")
  );

  return JSON.parse(base64);
}

function App() {
  return (
    <div className="App">
      <header>
        <h2>The Football Pool</h2>
        <a href="https://the-football-pool.eu.auth0.com/authorize?audience=fbpool&response_type=token&client_id=0iNaLqH6uT9Q22PSgTKgnz8Lv7d1N5T7&redirect_uri=https://localhost://5000/login-result">
          <h5>Login or Create and Account</h5>
        </a>
      </header>
      <Overview />

      {/* should only be able to access if logged in */}
      <Route path="/picks" component={Picks} />
    </div>
  );
}

export default App;
