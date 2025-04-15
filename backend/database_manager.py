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
                type VARCHAR(32),
                accesskey TEXT
            )
        ''')

        # Insert default route if table is empty
        cursor.execute('SELECT * FROM route')
        if not cursor.fetchall():
            cursor.execute('INSERT INTO route (host, target, type, accesskey) VALUES (?, ?, ?, ?)',
                           ('localhost:5000', 'http://example.com', 'proxy', 'default_access_key'))

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


def update_route(host, target, route_type):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE route SET target=?, type=? WHERE host=?',
                       (target, route_type, host))
        conn.commit()
        return True


def get_all_routes():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM route')
        routes = cursor.fetchall()
    return routes


def add_route(host, target, route_type, accesskey=None):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO route (host, target, type, accesskey) VALUES (?, ?, ?, ?)',
                           (host, target, route_type, accesskey))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False


def delete_route(host):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM route WHERE host=?', (host,))
        conn.commit()
        return True


def validate_webhook_accesskey(host, accesskey):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM route WHERE host=? AND accesskey=?', (host, accesskey))
        route = cursor.fetchone()
    return route is not None


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()