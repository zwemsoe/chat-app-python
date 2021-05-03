from flask_cors import CORS
from flask import Flask
from db import DB
from datetime import timedelta
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
app.secret_key = "skfgjkrjhvovirlf324837"
app.config['SECRET_KEY'] = "skfgjkrjhvovirlf324837"
app.permanent_session_lifetime = timedelta(minutes=60)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

config = {
    "DB_HOST": "localhost",
    "DB_USERNAME": "postgres",
    "DB_PASSWORD": "chatdbpython",
    "DB_DATABASE": "chatdb",
}

db = DB(config)
db.connect()

from controllers import userController
from controllers import roomController
# REST endpoints
app.add_url_rule('/api/login', 'login', userController.login, methods=['POST'])
app.add_url_rule('/api/register', 'register', userController.register, methods=['POST'])
app.add_url_rule('/api/user', 'authuser', userController.authuser, methods=['GET'])
app.add_url_rule('/api/logout', 'logout', userController.logout, methods=['GET'])

app.add_url_rule('/api/messages/<roomcode>', 'fetchOldMessages', roomController.fetchOldMessages, methods=['GET'])

# SOCKET event-controllers
socketio.on_event('join', roomController.joinRoom)
socketio.on_event('send message', roomController.sendMessage)


if __name__ == '__main__':
    socketio.run(app)
