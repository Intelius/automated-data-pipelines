import React from "react";
import Plotly from "plotly.js-finance-dist";

const StockGraph = (props) => {
  const { x, close, high, low, open, volume, EMA9 } = props;
  let maxVolume = Math.max(...volume);
  let minVolume = Math.min(...volume);
  //   let maxPrice = Math.max(...high, ...EMA9);
  //   let minPrice = Math.min(...low, ...EMA9);
  let maxPrice = Math.max(...high);
  let minPrice = Math.min(...low);

  //setting up the candlestick chart to display one minute market data
  let trace1 = {
    x: x,
    close: close,
    decreasing: { line: { color: "#EC1C24" } },
    high: high,
    increasing: { line: { color: "#0BDA51" } },
    line: { color: "rgba(31,119,180,1)" },
    low: low,
    open: open,
    type: "candlestick",
    xaxis: "x",
    yaxis: "y2", //adding another axis so it can display with the volume one.
    xperiod: 150000.0,
    xperiodalignment: "end",
    name: "Market Price",
  };
  //   setting up the line chart to display EMA9 data
  let trace2 = {
    type: "scatter",
    mode: "lines",
    name: "EMA9",
    x: x,
    y: EMA9,
    line: { color: "black" },
    xaxis: "x",
    yaxis: "y2", //adding another axis so it can display with the volume one.
    xperiodalignment: "end",
  };
  //   setting up the bar chart to display volume data
  let trace3 = {
    marker: { color: "#007bff" },
    x: x,
    y: volume,
    type: "bar",
    opacity: 0.4,
    xaxis: "x",
    yaxis: "y",
    xperiodalignment: "end",
    name: "Volume",
  };
  //combining all the charts to be displayed
  let data = [trace1, trace2, trace3];
  //   let data = [trace1, trace3];

  //for information about layout, please refer: https://plotly.com/python/reference/#layout
  let layout = {
    plot_bgcolor: "#F8F8F8",
    paper_bgcolor: "#F8F8F8",
    dragmode: "zoom",
    margin: {
      r: 10,
      t: 25,
      b: 60,
      l: 60,
    },
    bargap: 0,
    height: 500,
    hovermode: "x unified", //Determines the mode of hover interactions.
    xaxis: {
      anchor: "y",
      domain: [0.0, 0.94],
      rangeslider: {
        visible: false,
      },
      showgrid: true,
      dtick: 30,
      fixedrange: false,
    },
    yaxis: {
      anchor: "x",
      domain: [0.0, 1.0],
      range: [minVolume, maxVolume * 10],
      visible: false,
    },
    yaxis2: {
      anchor: "x",
      overlaying: "y",
      showgrid: false,
      side: "left",
      title: {
        text: "Price",
      },
      range: [minPrice * 0.98, maxPrice * 1.01],
    },
  };

  Plotly.react("myDiv", data, layout);

  return (
    <div className="stock-graph">
      <h3>Market Data Candlestick Chart</h3>
      <div id="myDiv"></div>
    </div>
  );
};

export default StockGraph;
