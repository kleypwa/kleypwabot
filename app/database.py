import sqlite3

def init_db():
    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            user TEXT,
            text TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_message_to_db(chat_id, user, text):
    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (chat_id, user, text) VALUES (?, ?, ?)",
                   (chat_id, user, text))
    conn.commit()
    conn.close()

def get_messages_from_db(chat_id, limit):
    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user, text FROM messages WHERE chat_id = ? ORDER BY id DESC LIMIT ?", 
                   (chat_id, limit))
    messages = cursor.fetchall()
    conn.close()
    return messages