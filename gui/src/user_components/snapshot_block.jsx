import React, {Component} from 'react';

function SnapshotBlock(props) {
	var dateTime = new Date(parseInt(props.snapshotID));
	var formattedDateTime = dateTime.toLocaleTimeString();
	var url = "/users/" + props.userID + "/snapshots/" + props.snapshotID;
	/*return (
		<div className="col-md-3 bg-light">
	      <h4>Snapshot from {formattedDateTime}</h4>
	      <p><a className="btn btn-secondary" href={url} role="button">View snapshot»</a></p>
	    </div>
		)*/

	return (
		<div className="col-md-3">
		  <h1><a className="btn btn-lg btn-outline-secondary" href={url} role="button">View snapshot from {formattedDateTime} »</a></h1>
		</div>
		  )
}

export default SnapshotBlock;