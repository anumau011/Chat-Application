# HTTP routes for the chat application

from flask import render_template, jsonify

def register_routes(app):
    """Register all HTTP routes"""
    
    @app.route('/')
    def index():
        """Main chat page"""
        return render_template('index.html')
    
    @app.route('/api/users', methods=['GET'])
    def get_users():
        """Get list of online users"""
        from .. import chat_manager
        users = chat_manager.get_online_users()
        return jsonify(users)
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'service': 'Flask Private Chat'
        })
