import React, { useState, useEffect } from "react";
import WeeklyPickForm from "./WeeklyPickForm";

function Picks() {
  const [weeks, setWeeks] = useState([]);
  const [playoffWeeks, setPlayoffWeeks] = useState([]);
  const [regSeasonGames, setRegSeasonGames] = useState([]);
  const [postSeasonGames, setPostSeasonGames] = useState([]);
  const [activeWeek, setActiveWeek] = useState([]);

  function filterUniqueWeeks(val, index, self) {
    return self.indexOf(val) === index;
  }

  useEffect(() => {
    const uniqueWeeks = regSeasonGames
      .map((el) => el.week)
      .filter(filterUniqueWeeks);
    setWeeks(uniqueWeeks);

    const playoffWeekButtons = postSeasonGames
      .map((el) => el.weekName)
      .filter(filterUniqueWeeks);
    setPlayoffWeeks(playoffWeekButtons);
  }, [postSeasonGames]);

  // fetch nfl api to generate weekly forms
  const getSeason = async (e) => {
    console.log("target", e.target.innerText);
    const season = e.target.innerText;
    const seasonSchedule = await fetch(
      `http://www.nfl.com/feeds-rs/schedules/${season}`
    );
    const jsonRes = await seasonSchedule.json();
    console.log("json response", jsonRes);
    const regularSeason = jsonRes.gameSchedules.filter((game) => {
      return game.seasonType === "REG";
    });
    const postSeason = jsonRes.gameSchedules.filter((game) => {
      return game.seasonType === "POST" || game.seasonType === "PRO";
    });
    const regSeasonGames = regularSeason.map((game) => {
      return {
        seasonType: game.seasonType,
        week: game.week,
        gameId: game.gameId,
        homeTeam: game.homeDisplayName,
        awayTeam: game.visitorDisplayName,
        gameDate: game.gameDate,
        weekName: game.weekName,
      };
    });
    const postSeasonGames = postSeason.map((game) => {
      return {
        seasonType: game.seasonType,
        week: game.week,
        gameId: game.gameId,
        homeTeam: game.homeDisplayName,
        awayTeam: game.visitorDisplayName,
        gameDate: game.gameDate,
        weekName: game.weekName,
      };
    });
    setRegSeasonGames(regSeasonGames);
    setPostSeasonGames(postSeasonGames);
  };

  const getWeek = (e) => {
    const oldActiveButton = document.getElementsByClassName("active");
    if (oldActiveButton.length > 0) {
      oldActiveButton[0].classList.toggle("active");
    }
    document.getElementById(e.target.id).classList.toggle("active");

    if (e.target.id < 18) {
      const newActiveWeek = regSeasonGames.filter((game) => {
        return game.week === parseInt(e.target.id);
      });
      setActiveWeek(newActiveWeek);
    } else {
      console.log("inside else in getweek");
      const newActiveWeek = postSeasonGames.filter((game) => {
        return game.week === parseInt(e.target.id);
      });
      setActiveWeek(newActiveWeek);
    }
  };
  useEffect(() => {
    console.log("active week", activeWeek);
  }, [activeWeek]);

  const renderWeekButtons = weeks.map((week) => {
    return (
      <button
        key={`reg${week}`}
        id={week}
        className=""
        onClick={getWeek}
        type="button"
      >
        Week {week}
      </button>
    );
  });
  const renderPlayoffWeekButtons = playoffWeeks.map((week, index) => {
    return (
      <button
        key={`${index}${week}`}
        id={index + 18}
        className=""
        onClick={getWeek}
        type="button"
      >
        Week {week}
      </button>
    );
  });

  return (
    <div>
      <h4>your picks</h4>
      {}
      <button type="button" onClick={getSeason}>
        2019
      </button>
      {regSeasonGames.length > 0 && renderWeekButtons}
      {postSeasonGames.length > 0 && renderPlayoffWeekButtons}
      {activeWeek.length > 0 && <WeeklyPickForm games={activeWeek} />}
    </div>
  );
}

export default Picks;
