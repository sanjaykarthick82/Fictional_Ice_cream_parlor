import sqlite3

def create_tables():
    conn = sqlite3.connect('parlor.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS flavors (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        description TEXT,
                        is_seasonal INTEGER DEFAULT 0
                      )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS ingredients (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        quantity INTEGER DEFAULT 0)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS allergens (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS cart (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        flavor_id INTEGER,
                        FOREIGN KEY (flavor_id) REFERENCES flavors (id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS flavor_suggestions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        suggestion TEXT NOT NULL UNIQUE)''')

    cursor.execute("INSERT OR IGNORE INTO allergens (name) VALUES ('Nuts'), ('Dairy'), ('Soy')")

    cursor.executemany(
        "INSERT OR IGNORE INTO flavors (name, description, is_seasonal) VALUES (?, ?, ?)",
        [
            ('Vanilla', 'Classic Vanilla', 0),
            ('Pumpkin Spice', 'Seasonal Pumpkin flavor', 1),
            ('Chocolate', 'Rich Chocolate flavor', 0),
            ('Strawberry', 'Fresh Strawberry flavor', 0),
            ('Mango Delight', 'Seasonal Mango flavor', 1)
        ])

    cursor.executemany(
        "INSERT OR IGNORE INTO ingredients (name, quantity) VALUES (?, ?)",
        [
            ('Milk', 100),
            ('Sugar', 50),
            ('Cream', 75),
            ('Chocolate', 20),
            ('Strawberries', 30),
            ('Banana', 25),
            ('Blueberries', 15)
        ])
    conn.commit()
    conn.close()


def get_connection():
    return sqlite3.connect('parlor.db')

if __name__ == '__main__':
    create_tables()
