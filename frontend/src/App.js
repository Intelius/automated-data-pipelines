import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Page404 from "./Error/Page404";
import Dashboard from "./Dashboard/Dashboard.js";

class App extends React.Component {
  render() {
    return (
      <div id="main">
        <Router>
          <Routes>
            <Route exact path="/" element={<Dashboard />} />
            <Route path="*" element={<Page404 />} />
          </Routes>
        </Router>
      </div>
    );
  }
}

export default App;
