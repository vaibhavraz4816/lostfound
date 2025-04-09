import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''
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

def insert_item(item_type, title, description, image):
    conn = sqlite3.connect('database.db')
    conn.execute('INSERT INTO items (type, title, description, image) VALUES (?, ?, ?, ?)',
                 (item_type, title, description, image))
    conn.commit()
    conn.close()

def get_items(item_type=None):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    if item_type:
        cursor.execute('SELECT * FROM items WHERE type = ?', (item_type,))
    else:
        cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    conn.close()
    return items