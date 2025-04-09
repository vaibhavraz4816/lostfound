import sqlite3

def init_db():
    conn = sqlite3.connect('items.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            title TEXT,
            description TEXT,
            image TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_item(type, title, description, image):
    conn = sqlite3.connect('items.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (type, title, description, image) VALUES (?, ?, ?, ?)",
                   (type, title, description, image))
    conn.commit()
    conn.close()

def get_items(type):
    conn = sqlite3.connect('items.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE type = ?", (type,))
    items = cursor.fetchall()
    conn.close()
    return items
