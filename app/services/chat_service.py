# Chat manager service for handling chat operations

from typing import Dict, List, Optional
from ..models import User, Message, ChatRoom

class ChatManager:
    """Service class for managing chat operations"""
    
    def __init__(self):
        self.connected_users: Dict[str, User] = {}  # {session_id: User}
        self.chat_rooms: Dict[str, ChatRoom] = {}   # {room_id: ChatRoom}
        self.username_to_session: Dict[str, str] = {}  # {username: session_id}
    
    def add_user(self, session_id: str, username: str) -> User:
        """Add a new user to the chat"""
        user = User(session_id, username)
        self.connected_users[session_id] = user
        self.username_to_session[username] = session_id
        return user
    
    def remove_user(self, session_id: str) -> Optional[str]:
        """Remove a user from the chat"""
        if session_id in self.connected_users:
            user = self.connected_users[session_id]
            username = user.username
            del self.connected_users[session_id]
            if username in self.username_to_session:
                del self.username_to_session[username]
            return username
        return None
    
    def get_user_by_session(self, session_id: str) -> Optional[User]:
        """Get user by session ID"""
        return self.connected_users.get(session_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        session_id = self.username_to_session.get(username)
        if session_id:
            return self.connected_users.get(session_id)
        return None
    
    def get_online_users(self) -> List[str]:
        """Get list of online usernames"""
        return list(self.username_to_session.keys())
    
    def create_room_id(self, user1: str, user2: str) -> str:
        """Create a consistent room ID for two users"""
        return f"room_{min(user1, user2)}_{max(user1, user2)}"
    
    def get_or_create_room(self, user1: str, user2: str) -> ChatRoom:
        """Get existing room or create new one for two users"""
        room_id = self.create_room_id(user1, user2)
        
        if room_id not in self.chat_rooms:
            self.chat_rooms[room_id] = ChatRoom(room_id, user1, user2)
        
        return self.chat_rooms[room_id]
    
    def add_message_to_room(self, room_id: str, username: str, message_text: str) -> Optional[Message]:
        """Add a message to a specific room"""
        if room_id in self.chat_rooms:
            message = Message(username, message_text, room_id)
            self.chat_rooms[room_id].add_message(message)
            return message
        return None
    
    def get_room_messages(self, room_id: str) -> List[Dict]:
        """Get messages for a specific room"""
        if room_id in self.chat_rooms:
            return self.chat_rooms[room_id].get_messages()
        return []
    
    def user_exists(self, username: str) -> bool:
        """Check if username already exists"""
        return username in self.username_to_session
    
    def get_user_rooms(self, username: str) -> List[str]:
        """Get all rooms for a user"""
        user = self.get_user_by_username(username)
        return user.rooms if user else []
