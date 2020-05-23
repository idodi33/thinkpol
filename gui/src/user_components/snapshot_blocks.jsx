import React, {Component} from 'react';
import SnapshotBlock from './snapshot_block';

class SnapshotBlocks extends Component {
	//state = {userData: null};
	state = {IDs: null}
	render() {
		var IDs = this.state.IDs;
		var userID = this.props.userID;
		if (!IDs) {
			return (<p></p>);
		}
		var snapshotLis = [];

		for(var i = 0; i < IDs.length; i++) {
			console.log('hey');
			var li = <SnapshotBlock key={IDs[i]} userID={userID} snapshotID={IDs[i]} url={this.props.APIUrl}/>;
			snapshotLis.push(li);
		};

		//var userData = getUserData(props.APIUrl);
		return (
		<div className='container marketing'>
	      <div className='row'>
	    	{snapshotLis}
	      </div>
	    </div>
			);
	}

	componentDidMount() {
		var url = this.props.APIUrl;
		var userID = this.props.userID;
		fetch(url + '/users/' + userID + '/snapshots', {
	      method: 'GET',
	      mode:'cors',
	      dataType: 'json'
	    })
	    .then((response) => {
	    	//partialJsons = data.json();
	    	return response.json();
	    })
	    .then((partialJsons) => {
	    	//console.log(partialJsons);
	    	console.log(partialJsons);
	    	return partialJsons;
	    })
	    .then((partialJsons) => {
	    	var snapshotIDs = []
	    	for (var i = 0; i < partialJsons.length; i++) {
				var snapshotID = partialJsons[i]['datetime'].toString();
				snapshotIDs[snapshotIDs.length] = snapshotID;
			}
			console.log(snapshotIDs);
			return snapshotIDs;
	    })
	    .then((snapshotIDs) => {
	    	this.setState({IDs: snapshotIDs});
	    });
	}
}


export default SnapshotBlocks;