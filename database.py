import sqlite3
from datetime import datetime

DB_PATH = "sales.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS phone_call(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    customer_id TEXT,
    customer_phone TEXT,
    status TEXT,
    note TEXT,
    created_at TEXT)
    """)
    conn.commit()
    conn.close()

def save_call(data:dict):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO phone_call(date, customer_id, customer_phone, status, note, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (data["date"], data["customer_id"], data["customer_phone"], data["status"], data["note"], datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
