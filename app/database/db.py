import sqlite3

conn = sqlite3.connect("chat.db", check_same_thread= False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT,
    message TEXT,
    timestamp TEXT
)
""")

conn.commit()

def save_messages(role,message,timestamp):
    cursor.execute(
        "INSERT INTO chat_history (role, message, timestamp) VALUES (?, ?, ?)",
        (role,message,timestamp)
    )
    conn.commit()
    
def get_history():
    cursor.execute("SELECT role, message, timestamp FROM chat_history")
    return cursor.fetchall()