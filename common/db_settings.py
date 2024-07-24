import sqlite3

database = "database.db"


def create_db():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT
    )
    """
    )
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY,
        username TEXT,
        name TEXT,
        surname TEXT
    )
    """
    )
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS superadmins (
        id INTEGER PRIMARY KEY,
        username TEXT,
        name TEXT,
        surname TEXT
    )
    """
    )
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS channels (
        channel_link TEXT PRIMARY KEY,
        title TEXT
    )
    """
    )
    conn.commit()
    conn.close()


def add_user(id: int, username: str):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(
        """INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)""",
        (id, username),
    )
    conn.commit()
    conn.close()


def get_all_users():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users")
    users = cursor.fetchall()
    conn.close()
    return [user[0] for user in users]



def add_admin(user_id: int, username: str, name: str, surname: str):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO admins (id, username, name, surname) VALUES (?, ?, ?, ?) 
        ON CONFLICT(id) DO UPDATE SET username=excluded.username""",
        (user_id, username, name, surname),
    )
    conn.commit()
    conn.close()


def add_superadmin(user_id: int, username: str, name: str, surname: str):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO superadmins (id, username, name, surname) VALUES (?, ?, ?, ?) 
        ON CONFLICT(id) DO UPDATE SET username=excluded.username""",
        (user_id, username, name, surname),
    )
    conn.commit()
    conn.close()


def del_admin(user_id: int):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM admins WHERE id=?""", (user_id,))
    conn.commit()
    conn.close()


def is_admin(user_id):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM admins WHERE id = ?", (user_id,))
    admin = cursor.fetchone()
    conn.close()
    return admin is not None

def is_superadmin(user_id):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM superadmins WHERE id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def get_admins():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, name, surname FROM admins")
    admins = cursor.fetchall()
    conn.close()
    return admins


def get_superadmins():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, name, surname FROM superadmins")
    superadmins = cursor.fetchall()
    conn.close()
    return superadmins


def add_channel(channel_link: str, title: str):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO channels (channel_link, title) VALUES (?, ?) 
        ON CONFLICT(channel_link) DO UPDATE SET title=excluded.title""",
        (channel_link, title),
    )
    conn.commit()
    conn.close()


def get_channels():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("SELECT channel_link, title FROM channels")
    channels = cursor.fetchall()
    conn.close()
    return channels


def del_channel(channel_link: str):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM channels WHERE channel_link=?""", (channel_link,))
    conn.commit()
    conn.close()


create_db()
