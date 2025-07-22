# Application factory for the Flask chat application

from flask import Flask
from flask_socketio import SocketIO
from config import config
from app.services import ChatManager

# Global instances
socketio = SocketIO()
chat_manager = ChatManager()

def create_app(config_name='default'):
    """Application factory function"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Register routes
    from app.routes import register_routes
    register_routes(app)
    
    # Register Socket.IO events
    from app.events import register_socketio_events
    register_socketio_events(socketio)
    
    return app
