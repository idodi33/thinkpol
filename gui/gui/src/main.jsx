import React, {Component} from 'react';
import { Switch, Route } from 'react-router-dom';

import Home from './main_components/home';
import User from './user_components/user';
import Snapshot from './snapshot_components/snapshot';
class Main extends Component {
  render() {
  	return (
    <Switch>
      <Route exact path='/' component={Home}></Route>
      <Route exact path='/users/:userID' component={User}></Route>
      <Route exact path='/users/:userID/snapshots/:snapshotID' component={Snapshot}></Route>
    </Switch>
  	);
  }


}

export default Main;
