#!/usr/bin/env python3
"""
Flask Private Chat Application - Legacy Entry Point
This file maintains backward compatibility with the original app.py structure.
For the modular version, use run.py instead.
"""

from app import create_app, socketio
import os

if __name__ == '__main__':
    # Create the app using the application factory
    config_name = os.environ.get('FLASK_CONFIG', 'development')
    app = create_app(config_name)
    
    # Run the application (legacy compatibility)
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)


