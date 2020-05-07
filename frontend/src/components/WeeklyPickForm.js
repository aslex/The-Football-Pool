import React, {useState, useEffect} from "react";

export default function WeeklyPickForm(props) {
  const [totalPoints, setTotalPoints] = useState(null)
  useEffect(() => {
      console.log('props change!', props.games)
      setTotalPoints(props.games.length)
  }, [props])

  console.log('total points:', totalPoints)
  const submitPicks = () => {
    console.log("submit!");
  };
  const renderEachGame = props.games.map((game) => {
    return (
      <div className="game" key={game.gameId}>
        <label htmlFor={game.gameId}>
          {game.homeTeam} vs. {game.awayTeam}
        </label>
        <input name={game.gameId} type="number" />
      </div>
    );
  });
  return (
    <div className="pick-form">
    {totalPoints && <p>total points this week: {totalPoints}</p>}
      <form onSubmit={submitPicks}>{renderEachGame}
      <button type='submit'>Submit this week's picks</button>
      </form>
    </div>
  );
}
