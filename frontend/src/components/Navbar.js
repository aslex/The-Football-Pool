// src/components/NavBar.js

import React from "react";
import { useAuth0 } from "../react-auth0-spa";
import {Link} from 'react-router-dom'

const NavBar = () => {
  const { isAuthenticated, loginWithRedirect, logout } = useAuth0();

  return (
    <div className='navbar'>
    <Link to='/' >Home</Link>
      {!isAuthenticated && (
        <button onClick={() => loginWithRedirect()}>Log in</button>
      )}
      {isAuthenticated && <button onClick={() => logout()}>Log out</button>}
        {isAuthenticated && <Link to='/picks'>My Picks</Link>}
    </div>
  );
};

export default NavBar;
