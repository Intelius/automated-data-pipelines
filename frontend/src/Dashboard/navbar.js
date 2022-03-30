import React, { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

const NavBar = (props) => {
  const [startDate, setStartDate] = useState(new Date());

  const handleDateSelection = (event) => {
    //Setting up the current date as the default date

    let dd = String(event.getDate()).padStart(2, "0");
    let mm = String(event.getMonth() + 1).padStart(2, "0"); //January is 0!
    let yyyy = event.getFullYear();

    const selectedDay = yyyy + "-" + mm + "-" + dd;

    props.handleDateSelection(selectedDay);
    setStartDate(event);
  };

  const handleStockSelection = (event) => {
    props.handleStockSelection(event.target.value);
  };

  return (
    <div className="navbar">
      <div className="navbar-date">
        <p>Date: </p>
        <DatePicker
          className="navbar-date__options"
          dateFormat="yyyy-MM-dd"
          selected={startDate}
          onChange={handleDateSelection}
        />
      </div>
      <div className="navbar-stock">
        <p>Stock: </p>
        <div className="navbar-stock__options">
          <select
            className="navbar-stock__options-select"
            value={props.stock}
            onChange={handleStockSelection}
          >
            <option value="AAL">AAL</option>
            <option value="AAPL">AAPL</option>
            <option value="AMD">AMD</option>
            <option value="MSFT">MSFT</option>
            <option value="TSLA">TSLA</option>
          </select>
        </div>
      </div>
    </div>
  );
};

export default NavBar;
