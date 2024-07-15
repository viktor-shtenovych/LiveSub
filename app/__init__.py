from flask import Flask
from config import Config
from flask_socketio import SocketIO

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from .routes import main_bp
    app.register_blueprint(main_bp)

    socketio.init_app(app, async_mode='eventlet')

    return app
