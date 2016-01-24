from flask import Flask, render_template, session
from flask.ext.socketio import SocketIO, join_room, emit
from uuid import uuid4
from Contact import Contact, Player
import random
import os

# Debugging Messages
DEBUG = True

# Server Stuff
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

id_to_name = {}
name_to_id = {}

# Game Logic Stuff
contact = Contact()


"""
Print system for debugging. Only prints when DEBUG is set to true.
"""
def debug(message):
    if debug:
        print(message)

"""
Sends all clients the updated user list information.
"""
def update_user_list():
    list = str(len(contact.players)) + '! : !'
    for player in contact.players:
        list += player.name + '! : !' + player.position + '! : !'
    emit('update user list', {'list': list}, broadcast=True)

"""
Iterates through players and locks down their submit fields if needed
"""
def update_players():
    for player in contact.players:
        bool = "FALSE"
        revealed = contact.revealed
        if player.position == Player.KING:
            if contact.game_state == Contact.STANDBY or contact.game_state == Contact.ACTIVE:
                bool = "TRUE"
            if contact.word != '':
                revealed += ' (' + contact.word + ')'
        else:
            if contact.game_state == Contact.ACTIVE:
                bool = "TRUE"
        emit('update info', {"bool": bool, 'word': player.word, 'revealed': revealed}, room=name_to_id[player.name])

"""
Updates all clients with all information.
"""
def update_clients():
    update_user_list()
    update_players()
    while contact.has_messages():
        msg = contact.read_message()
        emit('chat', {'name': "ANNOUNCER", 'msg': msg, 'king': "FALSE", "system": "TRUE"}, broadcast=True)

"""
Occurs when the user first enters the root page.
"""
@app.route('/')
def index():
    return render_template('index.html')

"""
Client submits a word to the server. Affects game-play
"""
@socketio.on('submit', namespace='/')
def submit(data):
    name = id_to_name[session['id']]
    debug(name + " submitted the word " + data["word"])
    msg = contact.submit_word(name, data["word"])
    emit('error', {'error': msg})
    update_clients()

"""
Handler: Client sends a chat message to the server.
"""
@socketio.on('chat', namespace='/')
def chat(data):
    if contact.game_state == Contact.ACTIVE:
        contact.parse_chat(data['msg'])
    name = id_to_name[session['id']]
    debug(name + " sent a chat message.")
    king = contact.find_king()
    if king is None or name != king.name:
        king = "FALSE"
    else:
        king = "TRUE"
    emit('chat', {'name': name, 'msg': data['msg'], 'king': king, "system": "FALSE"}, broadcast=True)

"""
Handler: Add a new player. Affects game-play.
"""
@socketio.on('add player', namespace='/')
def add_player(data):
    name = data['name']
    if name in id_to_name.values():
        for i in range(5):
            name += str(random.randint(0, 9))
    id_to_name[session['id']] = name
    name_to_id[name] = session['id']
    contact.add_player(name)
    debug(name + " was added to the game.")
    emit('set name', {'name': name})
    update_clients()

"""
Handler: Client connects to the server.
"""
@socketio.on('connect', namespace='/')
def connect():
    session['id'] = str(uuid4())
    join_room(session['id'])
    debug(session['id'] + " connected to the server.")

"""
Handler: Client disconnects from the server. Affects game-play.
"""
@socketio.on('disconnect', namespace='/')
def disconnect():
    if session['id'] in id_to_name:
        name = id_to_name[session['id']]
        contact.remove_player(name)
        del id_to_name[session['id']]
        del name_to_id[name]
        debug(name + " was removed from the game.")
        update_clients()
    debug(session['id'] + " disconnected.")

if __name__ == '__main__':
    debug("HELLO WORLD!")
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)