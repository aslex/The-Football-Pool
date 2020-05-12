import React, { useState, useEffect } from "react";
import { useAuth0 } from "../react-auth0-spa";

export default function WeeklyPickForm(props) {
  const { getTokenSilently, user } = useAuth0();
  const [totalPoints, setTotalPoints] = useState(null);
  const [week, setWeek] = useState(null);
  const [picks, setPicks] = useState({})

  useEffect(() => {
    console.log("props change!", props.games);
    setTotalPoints(props.games.length);
    setWeek(props.games[0].week);
  }, [props]);

  const handleClick = e => {
    const team = e.target.name
    const game = e.target.id.split(' ')[0]
    console.log('game id', game)
    // document.getElementById(e.target.id).classList.toggle('active')
    console.log('game object exists?', picks[game])
    if(picks[game]){
      console.log('IF')
      const updatedPick = {[game]:{selection: team}}
      setPicks(prevPicks => {return {...prevPicks, ...updatedPick } } )
      // setPicks([...picks, picks[game].selection = team])
    }else{
      console.log('ELSE')
      const pick = {
       [game]: {
          selection: team
        }
      }
      setPicks( picks => {return {...picks, ...pick } })
      // setPicks([...picks, pick])
    }
  }
  // console.log("user !", user);
  // console.log("total points:", totalPoints);
  console.log('picks added to state ?!', picks)
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
        <button type="button" className={
          picks[game.gameId] && picks[game.gameId].selection == game.homeTeam ? 'game-button active' : 'game-button'} id={`${game.gameId} ${game.homeTeam}`} name={game.homeTeam} onClick={handleClick}>
          {game.homeTeam}
        </button> vs. 
        <button type="button" className={picks[game.gameId] && picks[game.gameId].selection == game.awayTeam ? 'game-button active' : 'game-button'} id={`${game.gameId} ${game.awayTeam}`} name={game.awayTeam} onClick={handleClick}>
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
