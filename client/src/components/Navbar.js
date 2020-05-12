import React from "react";
import { useAuth0 } from "../react-auth0-spa";
import { Link } from "react-router-dom";

const NavBar = () => {
  const { isAuthenticated, loginWithRedirect, logout } = useAuth0();

  return (
    <div className="navbar">
      <Link to="/">Home</Link>
      {!isAuthenticated && (
        <button onClick={() => loginWithRedirect()}>Enter the pool</button>
      )}
      {isAuthenticated && <button onClick={() => logout()}>Log out</button>}

      {isAuthenticated && (
        <>
          <Link to="/picks">My Picks</Link>&nbsp;
          <Link to="/settings">Settings</Link>
        </>
      )}
    </div>
  );
};

export default NavBar;
