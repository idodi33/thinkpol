import React from 'react';
import UserHeader from './user_header';
import SnapshotBlocks from './snapshot_blocks';
function User(props) {
	console.log("User component loaded.")
	var userID = props.match.params.userID;
	return (
	<div>
      <UserHeader APIUrl={'http://127.0.0.1:5000'} userID={userID}/>
      <div className='container marketing'>
        <div className='row'>
    	  <SnapshotBlocks APIUrl={'http://127.0.0.1:5000'} userID={userID}/>
        </div>
      </div>
  	</div>)
}

export default User;

