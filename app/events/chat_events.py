# Socket.IO event handlers for chat functionality

from flask_socketio import emit, join_room, leave_room
from flask import request

def register_socketio_events(socketio):
    """Register all Socket.IO event handlers"""
    
    @socketio.on('connect')
    def handle_connect():
        """Handle client connection"""
        print(f'Client connected: {request.sid}')
        emit('connection_status', {'status': 'connected'})
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection"""
        from .. import chat_manager
        
        username = chat_manager.remove_user(request.sid)
        if username:
            # Notify all clients about user list update
            online_users = chat_manager.get_online_users()
            emit('user_list_update', online_users, broadcast=True)
            print(f'User {username} disconnected')
    
    @socketio.on('join_chat')
    def handle_join_chat(data):
        """Handle user joining the chat"""
        from .. import chat_manager
        
        username = data.get('username', '').strip()
        
        if not username:
            emit('join_error', {'message': 'Username is required'})
            return
        
        if chat_manager.user_exists(username):
            emit('join_error', {'message': 'Username already taken'})
            return
        
        # Add user to chat manager
        user = chat_manager.add_user(request.sid, username)
        
        # Send success response
        emit('join_success', {'username': username})
        
        # Broadcast updated user list to all clients
        online_users = chat_manager.get_online_users()
        emit('user_list_update', online_users, broadcast=True)
        
        print(f'User {username} joined the chat')
    
    @socketio.on('start_private_chat')
    def handle_start_private_chat(data):
        """Handle starting a private chat between two users"""
        from .. import chat_manager
        
        current_user_obj = chat_manager.get_user_by_session(request.sid)
        if not current_user_obj:
            emit('chat_error', {'message': 'User not found'})
            return
        
        current_user = current_user_obj.username
        target_user = data.get('target_user', '').strip()
        
        if not target_user or target_user == current_user:
            emit('chat_error', {'message': 'Invalid target user'})
            return
        
        # Get or create chat room
        room = chat_manager.get_or_create_room(current_user, target_user)
        room_id = room.room_id
        
        # Join the current user to the room
        join_room(room_id)
        
        # Find target user and join them to the room
        target_user_obj = chat_manager.get_user_by_username(target_user)
        if target_user_obj:
            socketio.server.enter_room(target_user_obj.session_id, room_id)
            target_user_obj.add_room(room_id)
        
        # Add room to current user's room list
        current_user_obj.add_room(room_id)
        
        # Send chat history to current user
        messages = room.get_messages()
        emit('private_chat_started', {
            'room_id': room_id,
            'target_user': target_user,
            'messages': messages
        })
        
        # Notify target user if they're online
        if target_user_obj:
            emit('private_chat_invitation', {
                'room_id': room_id,
                'from_user': current_user,
                'messages': messages
            }, room=target_user_obj.session_id)
    
    @socketio.on('send_private_message')
    def handle_send_private_message(data):
        """Handle sending a private message"""
        from .. import chat_manager
        
        current_user_obj = chat_manager.get_user_by_session(request.sid)
        if not current_user_obj:
            emit('message_error', {'message': 'User not found'})
            return
        
        room_id = data.get('room_id', '').strip()
        message_text = data.get('message', '').strip()
        
        if not room_id or not message_text:
            emit('message_error', {'message': 'Room ID and message are required'})
            return
        
        # Add message to room
        message = chat_manager.add_message_to_room(room_id, current_user_obj.username, message_text)
        
        if message:
            # Broadcast message to all users in the room
            emit('new_private_message', message.to_dict(), room=room_id)
        else:
            emit('message_error', {'message': 'Failed to send message'})
    
    @socketio.on('get_room_messages')
    def handle_get_room_messages(data):
        """Handle getting messages for a specific room"""
        from .. import chat_manager
        
        current_user_obj = chat_manager.get_user_by_session(request.sid)
        if not current_user_obj:
            emit('message_error', {'message': 'User not found'})
            return
        
        room_id = data.get('room_id', '').strip()
        if not room_id:
            emit('message_error', {'message': 'Room ID is required'})
            return
        
        messages = chat_manager.get_room_messages(room_id)
        emit('room_messages', {
            'room_id': room_id,
            'messages': messages
        })
