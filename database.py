import sqlite3

conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER,
    full_name TEXT,
    phone TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER,
    message TEXT
)
""")

conn.commit()


def save_user(telegram_id, name):
    cursor.execute("INSERT INTO users (telegram_id, full_name) VALUES (?, ?)", (telegram_id, name))
    conn.commit()


def save_phone(telegram_id, phone):
    cursor.execute("UPDATE users SET phone=? WHERE telegram_id=?", (phone, telegram_id))
    conn.commit()


def save_request(telegram_id, message):
    cursor.execute("INSERT INTO requests (telegram_id, message) VALUES (?, ?)", (telegram_id, message))
    conn.commit()


def get_users_count():
    cursor.execute("SELECT COUNT(*) FROM users")
    return cursor.fetchone()[0]
