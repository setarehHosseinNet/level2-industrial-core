import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="heat_tracking.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS heats (
                heat_id TEXT PRIMARY KEY,
                start_time TEXT,
                status TEXT,
                position TEXT,
                last_update TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                heat_id TEXT,
                event_type TEXT,
                position TEXT,
                timestamp TEXT,
                FOREIGN KEY (heat_id) REFERENCES heats(heat_id)
            )
        """)
        self.conn.commit()

    def insert_heat(self, heat_id, start_time):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO heats (heat_id, start_time, status, position, last_update)
            VALUES (?, ?, ?, ?, ?)
        """, (heat_id, start_time, "Active", None, start_time))
        self.conn.commit()

    def update_heat_status(self, heat_id, status):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE heats SET status = ? WHERE heat_id = ?
        """, (status, heat_id))
        self.conn.commit()

    def add_event(self, heat_id, event_type, position, timestamp):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO events (heat_id, event_type, position, timestamp)
            VALUES (?, ?, ?, ?)
        """, (heat_id, event_type, position, timestamp))

        cursor.execute("""
            UPDATE heats SET position = ?, last_update = ? WHERE heat_id = ?
        """, (position, timestamp, heat_id))
        self.conn.commit()

    def close(self):
        self.conn.close()
