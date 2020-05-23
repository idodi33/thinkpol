import React, {Component} from 'react';
import happiness1 from '../images/happiness1.png';
import happiness2 from '../images/happiness2.png';
import happiness3 from '../images/happiness3.png';
import happiness4 from '../images/happiness4.png';
import happiness5 from '../images/happiness5.png';
import exhaustion1 from '../images/exhaustion1.png';
import exhaustion2 from '../images/exhaustion2.png';
import exhaustion3 from '../images/exhaustion3.png';
import exhaustion4 from '../images/exhaustion4.png';
import exhaustion5 from '../images/exhaustion5.png';
import hunger1 from '../images/hunger1.png';
import hunger2 from '../images/hunger2.png';
import hunger3 from '../images/hunger3.png';
import hunger4 from '../images/hunger4.png';
import hunger5 from '../images/hunger5.png';
import thirst1 from '../images/thirst1.png';
import thirst2 from '../images/thirst2.png';
import thirst3 from '../images/thirst3.png';
import thirst4 from '../images/thirst4.png';
import thirst5 from '../images/thirst5.png';

var happinessImages = [happiness1, happiness2, happiness3, happiness4, happiness5];
var exhaustionImages = [exhaustion1, exhaustion2, exhaustion3, exhaustion4, exhaustion5];
var hungerImages = [hunger1, hunger2, hunger3, hunger4, hunger5];
var thirstImages = [thirst1, thirst2, thirst3, thirst4, thirst5];
var imageLists = {
	'happiness': happinessImages, 
	'exhaustion': exhaustionImages,
	'hunger': hungerImages, 
	'thirst': thirstImages
};

class Feelings extends Component {
	state = {happinessImage: null, exhaustionImage: null, hungerImage: null, thirstImage: null};

	render() {
		var data = this.state.data;
		console.log(data);
		if (!data) {
			return (<p> </p>);
		}
		return (
			<div className="row mb-5">
			  <div className="col App ">
			    <h2>Happiness </h2>
	            <img className="rounded-circle" src={this.state.happinessImage} alt="Generic placeholder image" width="140" height="140"/>
	          </div>
	          <div className="col App ">
			    <h2>Exhaustion </h2>
	            <img className="rounded-circle" src={this.state.exhaustionImage} alt="Generic placeholder image" width="140" height="140"/>
	          </div>
	          <div className="col App ">
			    <h2>Hunger </h2>
	            <img className="rounded-circle" src={this.state.hungerImage} alt="Generic placeholder image" width="140" height="140"/>
	          </div>
	          <div className="col App ">
			    <h2>Thirst </h2>
	            <img className="rounded-circle" src={this.state.thirstImage} alt="Generic placeholder image" width="140" height="140"/>
	          </div>
	        </div>
			)
	}

	componentDidMount() {
		var url = this.props.resultURL;
		//var id = this.props.userID;
		console.log(url + "feelings");
		fetch(url + "feelings", {
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
	    .then((newData) => {
	    	this.setState({
	    		data: newData,
	    		happinessImage: this.chooseImage(newData, 'happiness'),
	    		exhaustionImage: this.chooseImage(newData, 'exhaustion'),
	    		hungerImage: this.chooseImage(newData, 'hunger'),
	    		thirstImage: this.chooseImage(newData, 'thirst')
	    	});
	    })
	    .then((data) => {
	    	console.log(data);
	    });
	}

	chooseImage(data, feeling) {
		var value = data[feeling];
		// We need to turn the -1 to 1 scale to a 0 to 5 scale to choose an image.
		var scaledValue = Math.floor((((value + 1.0) * 5.0) / 2.0));
		console.log(scaledValue);
		return (imageLists[feeling])[scaledValue];
	}
}

export default Feelings;