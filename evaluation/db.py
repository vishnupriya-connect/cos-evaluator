import sqlite3
import os
from datetime import datetime


DB_FILE = "data/evaluations.db"


def init_db():
    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS evaluations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        input TEXT,
        intent TEXT,
        score REAL,
        errors TEXT,
        pass_errors TEXT,
        feedback TEXT,
        suggestion TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_evaluation(result):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO evaluations (
            timestamp, input, intent, score,
            errors, pass_errors, feedback, suggestion
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.utcnow().isoformat(),
            result.get("input"),
            result.get("intent"),
            result.get("score", {}).get("final_score"),
            str(result.get("validation", {}).get("errors", [])),
            str(result.get("pass_validation", {}).get("errors", [])),
            str(result.get("feedback")),
            result.get("suggestion")
        ))

        conn.commit()
        conn.close()

    except Exception:
        # never break pipeline
        pass