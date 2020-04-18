import React from 'react';
import Header from '../header';
import UserBlocks from './user_blocks'

function Home(props) {
	return (
	<div>
      <Header />
      <div className='container marketing'>
        <div className='row'>
    	  <UserBlocks APIUrl={'http://127.0.0.1:5000'}/>
        </div>
      </div>
  	</div>)
}

export default Home;