<h1><b>CONTACT!</b></h1>

<i> The game is hosted <a href="https://contactthegame.herokuapp.com/" target="_blank">here</a>. Unfortunately, it won't always be up because of heroku's 18 hour a day up-time limit.</i>

<img src="http://gdurl.com/3RaQ" alt="Game Screenshot align="middle">

This is a web app implementation of a word game that I play with my friends. It basically revolves around word guessing and giving clever hints to your friends.

The rules are a little hard to explain, so I won't clutter this README with them. But <a href="http://forum.frontrowcrew.com/discussion/7294/learn-how-to-play-the-word-game-contact" target="_blank">here</a> is a link to the rules.

This is a <b>Flask</b> application that uses <b>Flask-SocketIO</b> to communicate with HTML5's websockets for speedy socket connections. I'm hosting it on heroku, and there were a couple of things that I needed to change from my local development to get it to work as a heroku application. They are as follows:
<ul>
  <li>Change "http" connections to "https" (in index.html)</li>
  <li>Change the port from 5000 to whatever magic number heroku gives you when you spin up the server. This part transitions automatically.</li>
  <li>Change the host from the default of '127.0.0.1' to '0.0.0.0' so that the server can be publically viewed. (in Server.py)</li>
</ul>

This game has a hard minimum of 3 players, <strike>which made testing it boring because I have no friends</strike>, and can go up to as many people as you want. Go crazy!

<h3><b>Credits</b></h3>

<ol>
<li> JK I have friends. They introduced me to this game.</li>
<li> iruul from the Front Row Crew Forum for providing an easily referrable version of the rules.</li>
<li> AlexBoulot from bypeople.com for providing a <a href="http://www.bypeople.com/threaded-chat-css/" target="_blank">complete html/css project</a> for a chat application. Front end is hard. </li>
<li> Stack-overflow and w3schools and google in general because I think I did one google search per five lines written in this project. </li>
</ol>
