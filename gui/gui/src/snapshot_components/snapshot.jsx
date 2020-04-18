import React from 'react';
import SnapshotHeader from './snapshot_header';
import Feelings from './feelings';
import ColorImage from './color_image';
import DepthImage from './depth_image';
import Pose from './pose';

function Snapshot(props) {
	console.log("User component loaded.")
	var userID = props.match.params.userID;
  var snapshotID = props.match.params.snapshotID;
  var resultURL = 'http://127.0.0.1:5000' + "/users/" + userID + "/snapshots/" + snapshotID + "/";
	return (
	<div>
      <SnapshotHeader APIUrl={'http://127.0.0.1:5000'} userID={userID} snapshotID={snapshotID}/>
      <div className='container marketing clearfix  border border-secondary rounded'>
        <Feelings resultURL={resultURL}/>
        <Pose resultURL={resultURL}/>
        <div className='row'>
          <ColorImage resultURL={resultURL}/>
          <DepthImage resultURL={resultURL}/>
        </div>
      </div>
  	</div>)
}

export default Snapshot;

