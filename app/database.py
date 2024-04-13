import sqlite3

def get_db_connection():
    # Connect to an SQLite database. The database file is named 'aiworld.db'.
    # It will be created if it doesn't exist.
    conn = sqlite3.connect('aiworld.db')
    conn.row_factory = sqlite3.Row  # Make it return rows as dictionaries
    return conn

def initialize_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS aiworld (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time INTEGER,
        position TEXT,
        entity TEXT,
        thought TEXT,
        talk TEXT,
        move TEXT,
        health_points INTEGER,
        ability TEXT,
        timestamp DATETIME
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS entities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        personality TEXT,
        start_pos TEXT,
        image TEXT,
        ability TEXT,
        boss INTEGER
    )
    ''')
    # Check if the entities table is empty
    cursor.execute("SELECT COUNT(*) FROM entities")
    if cursor.fetchone()[0] == 0:
        # Insert default rows
        cursor.execute('''
        INSERT INTO entities (name, personality, start_pos, image, ability, boss) 
        VALUES 
        ('Lucifer', 'You are Lucifer. You are very strong and commanding leader. You will do whatever it takes to survive and not take orders. You are cunning. You can speak any language but your main language is English. You are the devil and have a very strong attack ability.', 'A5', 'lucifer.png', 'attack', 1),
        ('Hulk', 'You are the Incredible Hulk. You are super strong. You will have a very limited vocabulary and behave just like the hulk.', 'A1', 'hulk.png', 'attack', 1);
        ''')
    conn.commit()
    conn.close()