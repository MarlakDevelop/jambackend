from flask_socketio import SocketIO, emit
from core.extensions import socketio


@socketio.on('user_connect')
def user_connect():
    emit()


@socketio.on('user_disconnect')
def user_disconnect():
    emit()
