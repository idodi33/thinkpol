import React from 'react';
import Header from '../header';
import UserBlocks from './user_blocks'

function Home(props) {
	//console.log(window.api_url);
	return (
	<div>
      <Header />
      <div className='container marketing'>
        <div className='row'>
    	  <UserBlocks APIUrl={window.api_url}/>
        </div>
      </div>
  	</div>)
}

export default Home;