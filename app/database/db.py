import sqlite3
from datetime import datetime
from app.config import logger

DB_PATH = "matex_database.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    
    query = """
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        user_message TEXT,
        matex_response TEXT,
        emotion_sensed TEXT,
        timestamp DATETIME
    )
    """
    try:
        with get_connection() as conn:
            conn.execute(query)
            logger.info("Database initialized and tables created.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")

def save_chat(user_id, user_msg, matex_res, emotion):
    
    query = """
    INSERT INTO chat_history (user_id, user_message, matex_response, emotion_sensed, timestamp)
    VALUES (?, ?, ?, ?, ?)
    """
    try:
        with get_connection() as conn:
            conn.execute(query, (user_id, user_msg, matex_res, emotion, datetime.now()))
            conn.commit()
    except Exception as e:
        logger.error(f"Failed to save chat: {e}")

def get_user_history(user_id, limit=10):
    
    query = "SELECT user_message, matex_response, emotion_sensed FROM chat_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?"
    with get_connection() as conn:
        cursor = conn.execute(query, (user_id, limit))
        return cursor.fetchall()