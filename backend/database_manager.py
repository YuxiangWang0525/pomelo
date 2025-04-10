import sqlite3
import hashlib

DATABASE = 'nene.db'


def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        # Create users table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        # Insert default user if table is empty
        cursor.execute('SELECT * FROM users')
        if not cursor.fetchall():
            hashed_password = hash_password('admin')
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('admin', hashed_password))

        # Create route table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS route (
                host TEXT,
                target TEXT,
                `type` VARCHAR(32)
            )
        ''')

        conn.commit()


def authenticate(username, password):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, hash_password(password)))
        user = cursor.fetchone()
    return user is not None


def update_user(new_username, new_password):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        hashed_password = hash_password(new_password)
        cursor.execute('UPDATE users SET username=?, password=? WHERE id=1', (new_username, hashed_password))
        conn.commit()


def get_route_by_host(host):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM route WHERE host=?', (host,))
        route = cursor.fetchone()
    return route

def get_proxy_target(host):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT target FROM route WHERE host=? AND type="proxy"', (host,))
        result = cursor.fetchone()
    return result[0] if result else None


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()