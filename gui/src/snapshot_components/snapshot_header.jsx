import React, {Component} from 'react';
import Header from '../header';
/*
class User extends Component {
	state = {};
	render() {
		return ();
	}
}*/

class SnapshotHeader extends Component {
	state = {userData: null};

	render() {
		console.log("hey");
		var data = this.state.userData;
		console.log(data);
		if (!data) {
			return (<p> </p>);
		}
		var birthDay = new Date(data['birthday'] * 1000); // convert from milliseconds
		var formattedBirthDay = birthDay.toLocaleDateString();
		var age = ~~((Date.now() - birthDay) / (31557600000));
		var gender = data['gender'];
		var dateTime = new Date(parseInt(this.props.snapshotID));
		var formattedDateTime = dateTime.toLocaleTimeString();
		var userCode = 
			<div className='App'>
			  <h2>Snapshot from {formattedDateTime}</h2>	
	          <p>User #{data['user_id']}: {data['username']}</p>
	          <p>Birthday: {formattedBirthDay} ({age} years old)</p>
	          <p>Gender: {gender}</p>
	        </div>;
		return (
			<Header info={userCode}/>
			)
	}

	componentDidMount() {
		var url = this.props.APIUrl;
		var id = this.props.userID;
		console.log(url + "/users/" + id);
		fetch(url + "/users/" + id, {
		      		method: 'GET',
		      		mode:'cors',
		      		dataType: 'json'
	    })
	    .then((data) => {
	    	if (!data.ok) {
	    		console.log(data);
	    		console.log("data is not ok!");
	    	}
	    	return data;
	    })
	    .then((data) => {
	    	var js = data.json();
	    	console.log(js);
	    	return js;
	    })
	    .then((data) => {
	    	return data[0];
	    })
	    .then((data) => {
	    	this.setState({userData: data});
	    })
	    .then((data) => {
	    	console.log(data);
	    });
	}
}

export default SnapshotHeader;