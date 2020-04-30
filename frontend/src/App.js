import React from "react";
import logo from "./logo.svg";
import "./App.css";
import { Route, Switch, Link } from "react-router-dom";
import Overview from "./components/Overview";
import Picks from "./components/Picks";
import { useEffect, useState } from "react";

import Navbar from "./components/Navbar";
import { useAuth0 } from "./react-auth0-spa";

function App() {
  const { user, loading } = useAuth0();
  console.log("user?", user);

  if (loading) {
    return <div>Loading...</div>;
  }
  return (
    <div className="App">
      <header>
        <h2>The Football Pool</h2>
        <Navbar />
      </header>
      <Overview />

      {/* should only be able to access if logged in */}

      <Route path="/picks" component={Picks} />
    </div>
  );
}

export default App;

// const getToken = () => {
//   console.log("local storage:", localStorage);
//   let token = localStorage.getItem("jwtToken");
//   if (!token || token === "") {
//     return;
//   } else {
//     let user = parseJwt(token);
//     setUser(user);
//   }
// };

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
