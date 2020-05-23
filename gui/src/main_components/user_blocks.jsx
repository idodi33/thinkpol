import React, {Component} from 'react';
import UserBlock from './user_block';

class UserBlocks extends Component {
	//state = {userData: null};
	state = {IDs: null}
	render() {
		var IDs = this.state.IDs;
		if (!IDs) {
			return (<p></p>);
		}
		var userLis = [];
		console.log(this.props.APIUrl)
		for(var i = 0; i < IDs.length; i++) {
			console.log('hey');
			var li = <UserBlock key={IDs[i]} userID={IDs[i]} url={this.props.APIUrl}/>;
			userLis.push(li);
		};

		//var userData = getUserData(props.APIUrl);
		return (
		<div className='container marketing'>
	      <div className='row'>
	    	{userLis}
	      </div>
	    </div>
			);
	}

	componentDidMount() {
		var url = this.props.APIUrl;
		fetch(url + '/users', {
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
	    	var userIDs = []
	    	for (var i = 0; i < partialJsons.length; i++) {
				var userID = partialJsons[i]['user_id'].toString();
				userIDs[userIDs.length] = userID;
			}
			console.log(userIDs);
			return userIDs;
	    })
	    .then((userIDs) => {
	    	this.setState({IDs: userIDs});
	    });
	}
}


export default UserBlocks;