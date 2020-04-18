import React, {Component} from 'react';

class Pose extends Component {
	state = {data: null};

	render() {
		var data = this.state.data;
		console.log(data);
		if (!data) {
			return (<p> </p>);
		}
		return (
			<div className="row mb-5">
			  <div className="col m-6 App ">
			    <h2>Translation </h2>
	            <h5>({data['translation_x'].toFixed(4)}, {data['translation_y'].toFixed(4)}, {data['translation_z'].toFixed(4)})</h5>
	          </div>
	          <div className="col m-6 App ">
			    <h2>Rotation </h2>
	            <h5>({data['rotation_x'].toFixed(4)}, {data['rotation_y'].toFixed(4)},{" "} 
	            {data['rotation_z'].toFixed(4)}, {data['rotation_w'].toFixed(4)})</h5>
	          </div>
	        </div>
			)
	}

	componentDidMount() {
		var url = this.props.resultURL;
		//var id = this.props.userID;
		console.log(url + "pose");
		fetch(url + "pose", {
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
	    	});
	    })
	    .then((data) => {
	    	console.log(data);
	    });
	}
}

export default Pose;