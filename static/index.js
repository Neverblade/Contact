$(document).ready(function() {
    var namespace = ''
    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);

    /* Initial Name Grabbing */
    var name = prompt("Please enter your name.");
    if (name == null || name == '') {
        name = "Anonymous Cow"
    }
    socket.emit('add player', { name: name });
});