# Data models for the chat application

from datetime import datetime
from typing import List, Dict, Optional

class User:
    """User model for chat application"""
    
    def __init__(self, session_id: str, username: str):
        self.session_id = session_id
        self.username = username
        self.rooms: List[str] = []
        self.connected_at = datetime.now()
    
    def add_room(self, room_id: str):
        """Add a room to user's room list"""
        if room_id not in self.rooms:
            self.rooms.append(room_id)
    
    def remove_room(self, room_id: str):
        """Remove a room from user's room list"""
        if room_id in self.rooms:
            self.rooms.remove(room_id)
    
    def to_dict(self) -> Dict:
        """Convert user to dictionary"""
        return {
            'session_id': self.session_id,
            'username': self.username,
            'rooms': self.rooms,
            'connected_at': self.connected_at.isoformat()
        }

class Message:
    """Message model for chat application"""
    
    def __init__(self, username: str, message: str, room_id: str):
        self.username = username
        self.message = message
        self.room_id = room_id
        self.timestamp = datetime.now().strftime('%H:%M:%S')
        self.created_at = datetime.now()
    
    def to_dict(self) -> Dict:
        """Convert message to dictionary"""
        return {
            'username': self.username,
            'message': self.message,
            'timestamp': self.timestamp,
            'room_id': self.room_id
        }

class ChatRoom:
    """Chat room model for managing private conversations"""
    
    def __init__(self, room_id: str, user1: str, user2: str):
        self.room_id = room_id
        self.user1 = user1
        self.user2 = user2
        self.messages: List[Message] = []
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
    
    def add_message(self, message: Message):
        """Add a message to the room"""
        self.messages.append(message)
        self.last_activity = datetime.now()
        
        # Keep only last 100 messages
        if len(self.messages) > 100:
            self.messages.pop(0)
    
    def get_messages(self) -> List[Dict]:
        """Get all messages in the room as dictionaries"""
        return [message.to_dict() for message in self.messages]
    
    def has_user(self, username: str) -> bool:
        """Check if user is part of this room"""
        return username in [self.user1, self.user2]
    
    def get_other_user(self, username: str) -> Optional[str]:
        """Get the other user in the room"""
        if username == self.user1:
            return self.user2
        elif username == self.user2:
            return self.user1
        return None
