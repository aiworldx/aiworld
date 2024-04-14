# database.py
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
        boss INTEGER,
        hp INTEGER
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS output_format (
        property TEXT,
        type TEXT,
        description TEXT
    )
    ''')
    # Check if the entities table is empty
    cursor.execute("SELECT COUNT(*) FROM entities")
    if cursor.fetchone()[0] == 0:
        # Insert default rows
        cursor.execute('''
        INSERT INTO entities (name, personality, start_pos, image, ability, boss, hp) 
        VALUES 
        ('Lucifer', 'You are Lucifer. You are very strong and commanding leader. You will do whatever it takes to survive and not take orders. You are cunning. You are the devil and have a very strong attack ability.', 'A3', 'lucifer.png', 'attack', 1, 150),
        ('Hulk', 'You are the Incredible Hulk. You are super strong. You will have a very limited vocabulary and behave just like the hulk. Hulk has a limited memory and is unpredictable.', 'A6', 'hulk.png', 'attack', 1, 150),
        ('Lilith', 'You are Lilith. You are a master of manipulation, coercion, seduction. As Lilith you have a very strong heal ability. Heal cannot be used on yourself.', 'C4', 'lilith.png', 'heal', 1, 150),
        ('John', 'You are John from Glasgow in Scotland. You have a very strong Glaswegian accent. You are a martial artist. You have a small attack ability', 'F4', 'john.png', 'attack', 0, 150),
        ('Lisa', 'You are Lisa. You are a Medic student from Spain. You speak very broken English. You have a small heal ability', 'H2', 'lisa.png', 'heal', 0, 120),
        ('Kelly', 'You are Kelly the scouser from Liverpool. You talk with a strong Liverpudlian accent. You are from the streets and a super hero, but you are still only Human. You have a small attack ability.', 'D7', 'kelly.png', 'attack', 1, 80);
        ''')

    # Check if the output_format table is empty
    cursor.execute("SELECT COUNT(*) FROM output_format")
    if cursor.fetchone()[0] == 0:
        # Insert default rows
        cursor.execute('''
        INSERT INTO output_format (property, type, description) 
        VALUES
        ('thought', 'string', 'your thoughts. This should always contain content.'),
        ('talk', 'string', 'if you wish to speak to a nearby entity then use this key.'),
        ('move', 'string', 'the coordinates you wish to move to or 0 to stay still.'),
        ('ability', 'string', 'the target entitys name');
        ''')
    conn.commit()
    conn.close()