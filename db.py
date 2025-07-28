import sqlite3
from datetime import datetime

DB_NAME = "carwrap.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    with get_connection() as conn:
        with open("models.sql", "r", encoding="utf-8") as f:
            conn.executescript(f.read())

def add_user(tg_id, name):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO users (tg_id, name) VALUES (?, ?)", (tg_id, name))
        conn.commit()

def set_admin(tg_id):
    with get_connection() as conn:
        conn.execute("UPDATE users SET is_admin = 1 WHERE tg_id = ?", (tg_id,))
        conn.commit()

def is_admin(tg_id):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT is_admin FROM users WHERE tg_id = ?", (tg_id,))
        row = cur.fetchone()
        result = row and row[0] == 1
        print(f"is_admin check for {tg_id}: {result}")
        return result

def get_user_id(tg_id):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE tg_id = ?", (tg_id,))
        row = cur.fetchone()
        return row[0] if row else None

def add_report(user_id, date):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO reports (user_id, date) VALUES (?, ?)", (user_id, date))
        conn.commit()
        return cur.lastrowid

def add_car(report_id, plate, description, area, cost, labor_cost):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO cars (report_id, license_plate, description, area, cost, labor_cost) VALUES (?, ?, ?, ?, ?, ?)",
            (report_id, plate, description, area, cost, labor_cost)
        )
        conn.commit()

def add_photo(report_id, file_id):
    with get_connection() as conn:
        conn.execute("INSERT INTO photos (report_id, file_id) VALUES (?, ?)", (report_id, file_id))
        conn.commit()

def get_photos_by_date(date):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT file_id FROM photos 
            JOIN reports ON photos.report_id = reports.id 
            WHERE date(reports.date) = ?
        """, (date,))
        return [row[0] for row in cur.fetchall()]

def get_photos_by_month(year, month):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT file_id FROM photos 
            JOIN reports ON photos.report_id = reports.id 
            WHERE strftime('%Y', reports.date) = ? AND strftime('%m', reports.date) = ?
        """, (str(year), f"{int(month):02d}"))
        return [row[0] for row in cur.fetchall()]
