#!/usr/bin/env python3
"""
Verification script for the modular Flask chat application
Run this to verify that all components are working correctly before starting the app
"""

def test_imports():
    """Test that all modules can be imported correctly"""
    try:
        print("🧪 Testing modular structure...")
        print("-" * 50)
        
        # Test configuration
        from config import config
        print("✅ Configuration module imported successfully")
        
        # Test models
        from app.models import User, Message, ChatRoom
        print("✅ Models imported successfully")
        
        # Test services
        from app.services import ChatManager
        print("✅ Services imported successfully")
        
        # Test application factory
        from app import create_app, socketio
        print("✅ Application factory imported successfully")
        
        # Test creating a ChatManager instance
        chat_manager = ChatManager()
        print("✅ ChatManager instance created successfully")
        
        # Test user operations
        user = chat_manager.add_user("test_session_123", "test_user")
        print(f"✅ User created: {user.username}")
        
        # Test room operations
        room = chat_manager.get_or_create_room("alice", "bob")
        print(f"✅ Room created: {room.room_id}")
        
        # Test message operations
        message = chat_manager.add_message_to_room(room.room_id, "alice", "Hello Bob!")
        print(f"✅ Message added: {message.message}")
        
        # Test getting online users
        online_users = chat_manager.get_online_users()
        print(f"✅ Online users retrieved: {online_users}")
        
        print("\n🎉 All modular components are working correctly!")
        print("🚀 You can now run the application using:")
        print("   python run.py  (modular version)")
        print("   python app.py  (legacy compatibility)")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_imports()
