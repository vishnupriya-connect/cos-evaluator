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

def fetch_recent(limit=10):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT timestamp, input, intent, score
    FROM evaluations
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return rows


def fetch_low_scores(threshold=0.5):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT input, score
    FROM evaluations
    WHERE score <= ?
    ORDER BY score ASC
    """, (threshold,))

    rows = cursor.fetchall()
    conn.close()

    return rows


def fetch_stats():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM evaluations")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(score) FROM evaluations")
    avg_score = cursor.fetchone()[0]

    cursor.execute("""
    SELECT intent, COUNT(*)
    FROM evaluations
    GROUP BY intent
    """)
    intent_dist = cursor.fetchall()

    conn.close()

    return {
        "total": total,
        "avg_score": round(avg_score or 0, 2),
        "intent_distribution": intent_dist
    }