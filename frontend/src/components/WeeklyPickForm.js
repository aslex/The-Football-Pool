import React, { useState, useEffect } from "react";
import { useAuth0 } from "../react-auth0-spa";

export default function WeeklyPickForm(props) {
  const { getTokenSilently, user } = useAuth0();
  const [totalPoints, setTotalPoints] = useState(null);
  const [week, setWeek] = useState(null);

  useEffect(() => {
    console.log("props change!", props.games);
    setTotalPoints(props.games.length);
    setWeek(props.games[0].week);
  }, [props]);
  const handleClick = e => {
    console.log(e.target.name)
  }
  console.log("user !", user);
  console.log("total points:", totalPoints);
  const submitPicks = async (e) => {
    e.preventDefault();
    console.log("submit!");
    const token = await getTokenSilently();
    console.log(token);
    const response = await fetch(`/picks/${week}`, {
      method: "POST",
      headers: {
        authorization: `Bearer ${token}`,
      },
    });
    console.log("response", response);
  };
  const renderEachGame = props.games.map((game) => {
    return (
      <div className="game" key={game.gameId}>
        <button type="button" name={game.homeTeam} onClick={handleClick}>
          {game.homeTeam}
        </button> vs. 
        <button type="button" name={game.awayTeam} onClick={handleClick}>
          {game.awayTeam}
        </button>
        <label htmlFor={game.gameId}>
        </label>
        <input name={game.gameId} type="number" />
      </div>
    );
  });
  return (
    <div className="pick-form">
      {totalPoints && <p>total points this week: {totalPoints}</p>}
      <form onSubmit={submitPicks}>
        {renderEachGame}
        <button type="submit">Submit this week's picks</button>
      </form>
    </div>
  );
}
