import React from "react";
import { useState, useEffect } from "react";
import { useAuth0 } from "../react-auth0-spa";
import { Fragment } from "react";
import axios from "axios";
import history from "../utils/history";

export default function Settings() {
  const { loading, user, getTokenSilently } = useAuth0();

  const [nickname, setNickname] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();

    const token = await getTokenSilently();
    const userId = user.sub.split("|")[1];

    // const token = await fetch("https://fbpool.auth0.com/api/v2/", {
    //   headers: {
    //     authorization: accessToken,

    //   },
    // });
    console.log("TOKEN", token);
    try {
      const res = await fetch(`/users/${userId}`, {
        headers: {
          "content-type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: {
          nickname: nickname,
        },
        method: "PATCH",
      });

      const jsonRes = await res.json();
      console.log("response", jsonRes);
    } catch (error) {
      console.log("error", error);
    }
    history.push("/");
  }
  const handleChange = (e) => {
    setNickname(e.target.value);
  };

  if (loading || !user) {
    return <div>Loading...</div>;
  }
  return (
    <Fragment>
      <h4>Change your nickname</h4>
      <form onSubmit={(e) => handleSubmit(e)}>
        <input
          type="text"
          id="nickname"
          name="nickname"
          placeholder={
            (user.user_metadata && user.user_metadata.nickname) || user.nickname
          }
          onChange={handleChange}
        />
        <button type="submit">let's go</button>
      </form>
    </Fragment>
  );
}
