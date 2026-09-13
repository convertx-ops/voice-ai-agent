"""
Database models and utilities
"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from contextlib import contextmanager


class Database:
    def __init__(self, db_path: str = "agent_data.db"):
        self.db_path = db_path
        self.init_db()
    
    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def init_db(self):
        """Initialize database schema."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER UNIQUE NOT NULL,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    is_premium BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Conversations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    mode TEXT NOT NULL,
                    title TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            ''')
            
            # Messages table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id INTEGER NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    audio_url TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
                )
            ''')
            
            # Sessions table (for tracking active sessions)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    mode TEXT NOT NULL,
                    session_data TEXT,
                    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ended_at TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            ''')
            
            # Indexes
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_telegram ON users(telegram_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_conversations_user ON conversations(user_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_conv ON messages(conversation_id)')


class UserModel:
    def __init__(self, db: Database):
        self.db = db
    
    def create_or_update(self, telegram_id: int, username: str = None, 
                         first_name: str = None, last_name: str = None) -> int:
        """Create or update user."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if user exists
            cursor.execute("SELECT id FROM users WHERE telegram_id = ?", (telegram_id,))
            existing = cursor.fetchone()
            
            if existing:
                cursor.execute('''
                    UPDATE users 
                    SET username = COALESCE(?, username),
                        first_name = COALESCE(?, first_name),
                        last_name = COALESCE(?, last_name),
                        updated_at = CURRENT_TIMESTAMP
                    WHERE telegram_id = ?
                ''', (username, first_name, last_name, telegram_id))
                return existing['id']
            else:
                cursor.execute('''
                    INSERT INTO users (telegram_id, username, first_name, last_name)
                    VALUES (?, ?, ?, ?)
                ''', (telegram_id, username, first_name, last_name))
                return cursor.lastrowid
    
    def get_user(self, telegram_id: int) -> Optional[Dict]:
        """Get user by telegram ID."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def activate_premium(self, telegram_id: int) -> bool:
        """Activate premium subscription."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users SET is_premium = TRUE, updated_at = CURRENT_TIMESTAMP
                WHERE telegram_id = ?
            ''', (telegram_id,))
            return cursor.rowcount > 0


class ConversationModel:
    def __init__(self, db: Database):
        self.db = db
    
    def create(self, user_id: int, mode: str, title: str = None) -> int:
        """Create new conversation."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO conversations (user_id, mode, title)
                VALUES (?, ?, ?)
            ''', (user_id, mode, title))
            return cursor.lastrowid
    
    def get_user_conversations(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Get recent conversations for a user."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM conversations 
                WHERE user_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (user_id, limit))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_conversation_with_messages(self, conversation_id: int) -> Optional[Dict]:
        """Get conversation with all messages."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get conversation
            cursor.execute("SELECT * FROM conversations WHERE id = ?", (conversation_id,))
            conv_row = cursor.fetchone()
            if not conv_row:
                return None
            
            # Get messages
            cursor.execute('''
                SELECT * FROM messages 
                WHERE conversation_id = ? 
                ORDER BY timestamp ASC
            ''', (conversation_id,))
            messages = [dict(row) for row in cursor.fetchall()]
            
            result = dict(conv_row)
            result['messages'] = messages
            return result


class MessageModel:
    def __init__(self, db: Database):
        self.db = db
    
    def add_message(self, conversation_id: int, role: str, content: str, 
                    audio_url: str = None) -> int:
        """Add a message to conversation."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO messages (conversation_id, role, content, audio_url)
                VALUES (?, ?, ?, ?)
            ''', (conversation_id, role, content, audio_url))
            return cursor.lastrowid


# Initialize database
db = Database()
user_model = UserModel(db)
conversation_model = ConversationModel(db)
message_model = MessageModel(db)


def get_db_session():
    """Yield database session."""
    yield db
