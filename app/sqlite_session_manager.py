import sqlite3
from datetime import datetime
from pathlib import Path

class SQLiteSessionManager:
    def __init__(self, db_file='sessions.db'):
        self.db_file = Path(db_file)
        self.conn = sqlite3.connect(self.db_file)
        self._init_db()

    def _init_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                tg_id TEXT PRIMARY KEY,
                user_uuid TEXT NOT NULL,
                last_active TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def add_user(self, tg_id, user_uuid):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO sessions (tg_id, user_uuid, last_active)
            VALUES (?, ?, ?)
        ''', (str(tg_id), user_uuid, datetime.now().isoformat()))
        self.conn.commit()

    def get_user(self, tg_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT user_uuid, last_active FROM sessions WHERE tg_id = ?', (str(tg_id),))
        row = cursor.fetchone()
        if row:
            return {"user_uuid": row[0], "last_active": row[1]}
        return None

    def update_last_active(self, tg_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE sessions SET last_active = ? WHERE tg_id = ?
        ''', (datetime.now().isoformat(), str(tg_id)))
        self.conn.commit()

    def delete_user(self, tg_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM sessions WHERE tg_id = ?', (str(tg_id),))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
