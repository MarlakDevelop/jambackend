from core.app import create_app
from core.settings import Config

CONFIG = Config

app = create_app(CONFIG)

app.run(host='127.0.0.1', port='5000')