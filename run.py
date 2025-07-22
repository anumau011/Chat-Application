#!/usr/bin/env python3
"""
Flask Private Chat Application
Main entry point for the modular chat application
"""

import os
from app import create_app, socketio

def main():
    """Main function to run the application"""
    # Get configuration from environment or use default
    config_name = os.environ.get('FLASK_CONFIG', 'development')
    
    # Create Flask app
    app = create_app(config_name)
    
    # Get configuration
    host = app.config.get('HOST', '0.0.0.0')
    port = app.config.get('PORT', 5000)
    debug = app.config.get('DEBUG', True)
    
    print(f"🚀 Starting Flask Private Chat Application")
    print(f"📍 Server running on: http://{host}:{port}")
    print(f"🔧 Environment: {config_name}")
    print(f"🐛 Debug mode: {debug}")
    print("-" * 50)
    
    # Run the application
    socketio.run(app, debug=debug, host=host, port=port)

if __name__ == '__main__':
    main()
