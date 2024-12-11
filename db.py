import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS host_password (
            id INTEGER PRIMARY KEY,
            hostname TEXT NOT NULL,
            password TEXT NOT NULL
        )
        ''')
        self.conn.commit()

    def insert_user(self, name, age):
        self.cursor.execute('INSERT INTO host_password (hostname, password) VALUES (?, ?)', (name, age))
        self.conn.commit()

    def get_user(self, user_id):
        self.cursor.execute('SELECT * FROM host_password WHERE id = ?', (user_id,))
        return self.cursor.fetchone()

    def get_all_users(self):
        self.cursor.execute('SELECT * FROM host_password')
        return self.cursor.fetchall()

    def update_user(self, user_id, name, age):
        self.cursor.execute('UPDATE host_password SET hostname = ?, password = ? WHERE id = ?', (name, age, user_id))
        self.conn.commit()

    def delete_user(self, user_id):
        self.cursor.execute('DELETE FROM host_password WHERE id = ?', (user_id,))
        self.conn.commit()