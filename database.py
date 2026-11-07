
import sqlite3
import hashlib
import hmac

DB_NAME = "users.db"


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_database():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                prediction TEXT,
                sleep_duration REAL,
                heart_rate REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Migrate an older history table if it has no created_at column.
        columns = {
            row[1] for row in cursor.execute(
                "PRAGMA table_info(history)"
            ).fetchall()
        }

        if "created_at" not in columns:
            cursor.execute(
                "ALTER TABLE history ADD COLUMN created_at TIMESTAMP"
            )

        conn.commit()


def register_user(name, email, password):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("""
                INSERT INTO users (name, email, password)
                VALUES (?, ?, ?)
            """, (
                name.strip(),
                email.strip().lower(),
                hash_password(password)
            ))
        return True
    except sqlite3.IntegrityError:
        return False


def login_user(email, password):
    with sqlite3.connect(DB_NAME) as conn:
        row = conn.execute("""
            SELECT id, name, email, password
            FROM users
            WHERE email = ?
        """, (email.strip().lower(),)).fetchone()

    if row and hmac.compare_digest(row[3], hash_password(password)):
        return row[:3]

    return None


def save_history(email, prediction, sleep_duration, heart_rate):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            INSERT INTO history
                (email, prediction, sleep_duration, heart_rate)
            VALUES (?, ?, ?, ?)
        """, (
            email.strip().lower(),
            str(prediction),
            sleep_duration,
            heart_rate
        ))


def get_history(email):
    import pandas as pd

    with sqlite3.connect(DB_NAME) as conn:
        return pd.read_sql_query("""
            SELECT prediction, sleep_duration, heart_rate, created_at
            FROM history
            WHERE email = ?
            ORDER BY created_at DESC
        """, conn, params=(email.strip().lower(),))
