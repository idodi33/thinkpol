import React, {Component} from 'react';

class DepthImage extends Component {
	state = {imageURL: null};

	render() {
		var imageURL = this.state.imageURL;
		console.log(imageURL);
		if (!imageURL) {
			return (<p> </p>);
		}
		return (
			  <div className="col App ">
	            <img className="rounded" src={imageURL} alt="Generic placeholder image" width="390" height="390"/>
	          </div>
			)
	}

	componentDidMount() {
		var url = this.props.resultURL;
		//var id = this.props.userID;
		console.log(url + "depth_image/data");
		fetch(url + "depth_image/data", {
		      		method: 'GET',
		      		mode:'cors',
	    })
	    .then((data) => {
	    	if (!data.ok) {
	    		console.log(data);
	    		console.log("data is not ok!");
	    	}
	    	return data.blob();
	    })
	    .then((blob) => {
	    	var url = URL.createObjectURL(blob);
	    	return url;
	    })
	    .then((url) => {
	    	this.setState({
	    		imageURL: url})
	    })
	    .then((data) => {
	    	console.log(data);
	    });
	}
}

export default DepthImage;