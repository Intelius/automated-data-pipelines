import React, { useState, useEffect } from "react";
import NavBar from "./navbar";
import NewsDescription from "./newsDescription";
import StockGraph from "./stockGraph";
import axios from "axios";
import "./Dashboard.scss";
import {
  API_URL_ROOT,
  API_ONEMINUTE_PATH,
  API_NEWSDESCRIPTION_PATH,
} from "./apiLink.js";

const Dashboard = () => {
  //Formatting the current date to set up as the default
  let today = new Date();
  let dd = String(today.getDate()).padStart(2, "0");
  let mm = String(today.getMonth() + 1).padStart(2, "0"); //January is 0!
  let yyyy = today.getFullYear();

  const todayFormatted = yyyy + "-" + mm + "-" + dd;

  const [stock, setStock] = useState("AAL"); //For now this is the default stock until we have more stocks in the db
  const [date, setDate] = useState(todayFormatted);
  const [x, setX] = useState([]);
  const [close, setClose] = useState([]);
  const [high, setHigh] = useState([]);
  const [low, setLow] = useState([]);
  const [open, setOpen] = useState([]);
  const [volume, setVolume] = useState([]);
  const [EMA9, setEMA9] = useState([]);
  const [error, setError] = useState(false);
  const [articles, setArticles] = useState([]);
  const [limit, setLimit] = useState(8);

  useEffect(() => {
    axios
      .get(`${API_URL_ROOT}/${API_ONEMINUTE_PATH}?ticker=${stock}&date=${date}`)
      .then((response) => {
        let allClose = [];
        let allHigh = [];
        let allLow = [];
        let allOpen = [];
        let allMinute = [];
        let allVolume = [];
        let allEMA9 = [];

        const oneMinuteData = response.data.map((stock) => {
          allClose.push(stock.close);
          allHigh.push(stock.high);
          allLow.push(stock.low);
          allOpen.push(stock.open);
          allMinute.push(stock.datetime.slice(11));
          allVolume.push(stock.volume);
          allEMA9.push(stock.EMA9);
          return;
        });
        setX(allMinute);
        setClose(allClose);
        setHigh(allHigh);
        setLow(allLow);
        setOpen(allOpen);
        setVolume(allVolume);
        setEMA9(allEMA9);
      })
      .catch((e) => {
        setX("");
        setClose("");
        setHigh("");
        setLow("");
        setOpen("");
        setVolume("");
        setEMA9("");
        setLimit(8);
      });
  }, [date, stock]);

  useEffect(() => {
    axios
      .get(
        `${API_URL_ROOT}/${API_NEWSDESCRIPTION_PATH}?ticker=${stock}&day=${date}&limit=${limit}`
      )
      .then((response) => {
        let allNews = [];
        const news = response.data.map((item) => {
          allNews.push(item);
          return;
        });
        setArticles(allNews);
        setError(false);
        if (allNews.length < limit) {
          setError(true);
        }
      })
      .catch((e) => {
        setError(true);
        setArticles([]);
        setLimit(8);
      });
  }, [date, stock, limit]);

  const handleStockSelection = (event) => {
    setStock(event);
  };

  const handleDateSelection = (event) => {
    setDate(event);
  };

  const handleNewsButton = (event) => {
    if (limit === 8) {
      setLimit(12);
      return;
    } else if (limit === 12) {
      setLimit(16);
      return;
    } else {
      setLimit(8);
    }
  };

  return (
    <div>
      <div className="dashboard">
        <h1>Dair Booster Pack Project</h1>
        <div className="dashboard-navbar">
          <NavBar
            handleDateSelection={handleDateSelection}
            handleStockSelection={handleStockSelection}
            today={today}
            date={date}
            stock={stock}
          />
        </div>
        <div className="dashboard-graph">
          <StockGraph
            x={x}
            close={close}
            high={high}
            low={low}
            open={open}
            volume={volume}
            EMA9={EMA9}
          />
        </div>
      </div>
      <div className="dashboard-news">
        <NewsDescription
          articles={articles}
          handleNewsButton={handleNewsButton}
          limit={limit}
          error={error}
        />
      </div>
    </div>
  );
};

export default Dashboard;
