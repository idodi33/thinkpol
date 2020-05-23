import React, {Component} from 'react';
import $ from 'jquery';
//import Math from 'mathjs';
/*class User extends Component {
	state = {};
	render() {
		return ();
	}
}*/
var quotes = ["War is peace. Freedom is slavery. Ignorance is strength.", 
"The best books... are those that tell you what you know already.",
"If you want to keep a secret, you must also hide it from yourself.",
"If you want a picture of the future, imagine a boot stamping on a human face—for ever.",
"We shall meet in the place where there is no darkness.",
"But if thought corrupts language, language can also corrupt thought.”",
"Doublethink means the power of holding two contradictory beliefs in one's mind simultaneously, and accepting both of them.",
"Until they become conscious they will never rebel, and until after they have rebelled they cannot become conscious.",
"In the face of pain there are no heroes.",
"If you loved someone, you loved him, and when you had nothing else to give, you still gave him love.",
"Perhaps a lunatic was simply a minority of one.",
"Power is in tearing human minds to pieces and putting them together again in new shapes of your own choosing.",
"Being in a minority, even in a minority of one, did not make you mad. There was truth and there was untruth, and if you clung to the truth even against the whole world, you were not mad.",
"Big Brother is Watching You.",
"It's a beautiful thing, the destruction of words.",
"Freedom is the freedom to say that two plus two make four. If that is granted, all else follows.",
"Reality exists in the human mind, and nowhere else.",
"The choice for mankind lies between freedom and happiness and for the great bulk of mankind, happiness is better.",
"I enjoy talking to you. Your mind appeals to me. It resembles my own mind except that you happen to be insane.",
"Orthodoxy means not thinking--not needing to think. Orthodoxy is unconsciousness.",
"We do not merely destroy our enemies; we change them.",
"Sanity is not statistical."]

function Header(props) {
	var randomQuote = quotes[Math.floor(Math.random() * quotes.length)]; 
	var info = props.info ? props.info : <p></p>;
	return (
		  <div className="jumbotron h-75">
		    <div className="container">
              <h1 className="display-3">Thinkpol</h1>
              <p> </p>
              <p className="font-weight-light font-italic mt-5">”{randomQuote}”</p>
              <p className="ml-4 font-weight-bold mb-5">― George Orwell, 1984</p>
              <div>{info}</div>
            </div>
          </div>
		)
}
//font-weight-light
export default Header;