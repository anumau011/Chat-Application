# Development Guide - Modular Flask Chat Application

## 🏗️ **Architecture Overview**

This guide explains the modular architecture and how to extend the Flask chat application.

## 📁 **Project Structure Explained**

### **Root Level**
- `run.py` - **New main entry point** (recommended)
- `app.py` - **Legacy entry point** (backward compatibility)
- `test_modules.py` - **Verification script** for testing modules

### **Configuration (`config/`)**
```python
# config/config.py
class Config:
    SECRET_KEY = 'your-secret-key'
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
```

### **Models (`app/models/`)**
```python
# app/models/chat_models.py
class User:
    def __init__(self, session_id: str, username: str)
    def add_room(self, room_id: str)
    def to_dict(self) -> Dict

class Message:
    def __init__(self, username: str, message: str, room_id: str)
    def to_dict(self) -> Dict

class ChatRoom:
    def __init__(self, room_id: str, user1: str, user2: str)
    def add_message(self, message: Message)
    def get_messages(self) -> List[Dict]
```

### **Services (`app/services/`)**
```python
# app/services/chat_service.py
class ChatManager:
    def __init__(self)
    def add_user(self, session_id: str, username: str) -> User
    def remove_user(self, session_id: str) -> Optional[str]
    def get_or_create_room(self, user1: str, user2: str) -> ChatRoom
    def add_message_to_room(self, room_id: str, username: str, message: str)
```

### **Routes (`app/routes/`)**
```python
# app/routes/main_routes.py
def register_routes(app):
    @app.route('/')
    def index()
    
    @app.route('/api/users')
    def get_users()
    
    @app.route('/health')
    def health_check()
```

### **Events (`app/events/`)**
```python
# app/events/chat_events.py
def register_socketio_events(socketio):
    @socketio.on('connect')
    def handle_connect()
    
    @socketio.on('join_chat')
    def handle_join_chat(data)
    
    @socketio.on('send_private_message')
    def handle_send_private_message(data)
```

## 🔧 **How to Extend the Application**

### **Adding New Routes**
1. Edit `app/routes/main_routes.py`
2. Add new route functions inside `register_routes(app)`

```python
def register_routes(app):
    # Existing routes...
    
    @app.route('/api/rooms/<username>')
    def get_user_rooms(username):
        from .. import chat_manager
        rooms = chat_manager.get_user_rooms(username)
        return jsonify(rooms)
```

### **Adding New Socket Events**
1. Edit `app/events/chat_events.py`
2. Add new event handlers inside `register_socketio_events(socketio)`

```python
def register_socketio_events(socketio):
    # Existing events...
    
    @socketio.on('typing_indicator')
    def handle_typing(data):
        room_id = data.get('room_id')
        username = data.get('username')
        emit('user_typing', {'username': username}, room=room_id, include_self=False)
```

### **Adding New Models**
1. Edit `app/models/chat_models.py` or create new model files
2. Update `app/models/__init__.py` to export new models

```python
# app/models/chat_models.py
class TypingIndicator:
    def __init__(self, username: str, room_id: str):
        self.username = username
        self.room_id = room_id
        self.timestamp = datetime.now()

# app/models/__init__.py
from .chat_models import User, Message, ChatRoom, TypingIndicator
```

### **Adding New Services**
1. Create new service files in `app/services/`
2. Update `app/services/__init__.py`

```python
# app/services/notification_service.py
class NotificationService:
    def send_notification(self, user_id: str, message: str):
        # Implementation here
        pass

# app/services/__init__.py
from .chat_service import ChatManager
from .notification_service import NotificationService
```

## 🧪 **Testing**

### **Verify Modules Work**
```bash
python test_modules.py
```

### **Run Application**
```bash
# Development mode (recommended)
python run.py

# Legacy compatibility
python app.py

# With specific configuration
set FLASK_CONFIG=production
python run.py
```

## 🌍 **Environment Configuration**

### **Development**
```bash
set FLASK_CONFIG=development
python run.py
```

### **Production**
```bash
set FLASK_CONFIG=production
set SECRET_KEY=your-production-secret-key
python run.py
```

## 🛠️ **Best Practices**

### **1. Separation of Concerns**
- **Models**: Data structure and validation
- **Services**: Business logic and state management
- **Routes**: HTTP endpoints and API logic
- **Events**: Real-time communication logic

### **2. Import Guidelines**
- Use relative imports within the app package (`from .. import`)
- Import from services in routes and events
- Keep models independent

### **3. Error Handling**
- Add validation in service methods
- Emit error events for Socket.IO handlers
- Return appropriate HTTP status codes

### **4. Configuration**
- Use environment variables for sensitive data
- Keep different configs for different environments
- Use the `config` package for centralized settings

## 📈 **Scaling Considerations**

### **Database Integration**
Replace in-memory storage with a database:
```python
# app/services/chat_service.py
class ChatManager:
    def __init__(self, db_connection):
        self.db = db_connection
        # Use database instead of in-memory dictionaries
```

### **Redis for Session Management**
```python
# For production, use Redis for session storage
from flask_session import Session
import redis

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')
```

### **Load Balancing**
For multiple server instances, use Redis for Socket.IO:
```python
# app/__init__.py
socketio.init_app(app, 
    cors_allowed_origins="*",
    message_queue='redis://localhost:6379')
```

## 🔍 **Debugging**

### **Enable Debug Mode**
```bash
set FLASK_CONFIG=development
python run.py
```

### **Add Logging**
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# In your service methods
logger.debug(f"User {username} joined room {room_id}")
```

This modular structure makes the application much easier to maintain, test, and extend!
