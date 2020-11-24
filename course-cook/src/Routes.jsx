import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

import Home from "./routes/Home";
import NoMatch from "./routes/NoMatch";

function Routes() {
  return (
    <Router>
      <Switch>
        <Route exact path="/">
          <Home />
        </Route>
        <Route path="*">
          <NoMatch />
        </Route>
      </Switch>
    </Router>
  );
}

export default Routes;
