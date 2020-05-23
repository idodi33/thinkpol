import React, {Component} from 'react';
import man from '../images/man.png';
import woman from '../images/woman.png';
import other from '../images/other.png'
/*
class User extends Component {
	state = {};
	render() {
		return ();
	}
}*/
var imageDict = {'man': man, 'woman': woman, 'other': other};

class UserBlock extends Component {
	state = {userData: null};

	render() {
		var data = this.state.userData;
		console.log(data);
		if (!data) {
			return (<p> </p>);
		}
		var birthDay = new Date(data['birthday'] * 1000); // convert from milliseconds
		var formattedBirthDay = birthDay.toLocaleDateString();
		var age = ~~((Date.now() - birthDay) / (31557600000));
		var gender = data['gender'];
		return (
			<div className="col-lg-4 App border border-secondary rounded">
	          <img className="rounded-circle" src={imageDict[gender]} alt="Generic placeholder image" width="140" height="140"/>
	          <h2>User #{data['user_id']}: </h2>
	          <h2>{data['username']}</h2>
	          <p>Birthday: {formattedBirthDay} ({age} years old)</p>
	          <p>Gender: {gender}</p>
	          <p><a className="btn btn-outline-secondary" href={"/users/"+data['user_id']} role="button">View snapshots »</a></p>
	        </div>
			)
	}

	componentDidMount() {
		var url = this.props.url;
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

export default UserBlock;