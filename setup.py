from core.app import create_app
from core.settings import Config
from core.extensions import socketio
from flask_session import Session


CONFIG = Config

app = create_app(CONFIG)
Session(app)
socketio.init_app(app, manage_session=False, cors_allowed_origins="*")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port='5000')
