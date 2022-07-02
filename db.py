import sqlite3


def ensure_connection(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('users.db') as conn:
            res = func(*args, conn=conn, **kwargs)
            return res

    return inner


@ensure_connection
def init_db(conn, force: bool = False):
    c = conn.cursor()
    if force:
        c.execute('DROP TABLE IF EXISTS users')
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            telegram_id INTEGER NOT NULL UNIQUE,
            group_id INTEGER NOT NULL
        )
    ''')
    conn.commit()


@ensure_connection
def add_new_user(conn, telegram_id, group_id):
    c = conn.cursor()
    c.execute('INSERT INTO users (telegram_id, group_id) VALUES (?,?)', (telegram_id, group_id))
    conn.commit()


@ensure_connection
def get_user_group(conn, telegram_id):
    c = conn.cursor()
    c.execute('SELECT group_id FROM users WHERE telegram_id = ?', (telegram_id,))
    return c.fetchone()[0]

@ensure_connection
def edit_user_group(conn, telegram_id, group_id):
    c = conn.cursor()
    c.execute('UPDATE users SET group_id = ? WHERE telegram_id = ?', (group_id, telegram_id))
    conn.commit()

@ensure_connection
def check_exists_user(conn, telegram_id):
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
    if c.fetchone() is None:
        return False
    return True

