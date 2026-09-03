import sqlite3
import json


DB_NAME = "studytwin.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            code TEXT,
            debugging_score INTEGER,
            complexity_score INTEGER,
            complexity TEXT,
            issues TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_submission(
    user_id,
    code,
    debugging_score,
    complexity_score,
    complexity,
    issues
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO submissions
        (
            user_id,
            code,
            debugging_score,
            complexity_score,
            complexity,
            issues
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        code,
        debugging_score,
        complexity_score,
        complexity,
        json.dumps(issues)
    ))

    conn.commit()
    conn.close()


def get_history(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            debugging_score,
            complexity_score,
            complexity,
            issues,
            created_at
        FROM submissions
        WHERE user_id = ?
        ORDER BY created_at ASC
    """, (user_id,))

    rows = cursor.fetchall()

    conn.close()

    return rows