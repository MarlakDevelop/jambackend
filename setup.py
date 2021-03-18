from core.app import create_app
from core.settings import Config
from core.extensions import socketio

CONFIG = Config

app = create_app(CONFIG)
socketio.init_app(app)

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port='5000')
