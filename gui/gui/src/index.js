import React from 'react';
import ReactDOM from 'react-dom';
import 'core-js'
import App from './App';
import './index.css';
import 'bootstrap/dist/css/bootstrap.css';
import { BrowserRouter } from 'react-router-dom';

ReactDOM.render((
  <BrowserRouter>
    <App />
  </BrowserRouter>
  ), document.getElementById('root')
);

/*
ReactDOM.render(
  <div>
    <Header />
    <div className='container marketing'>
      <div className='row'>
    	<Users APIUrl={'http://127.0.0.1:5000'}/>
      </div>
    </div>
  </div>,
  document.getElementById('root')
);
*/