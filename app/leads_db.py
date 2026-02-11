from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime, timezone

DB_PATH = Path("data/leads.db")


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=20)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at_utc TEXT NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                subject TEXT,
                course TEXT,
                message TEXT NOT NULL,
                email_sent INTEGER NOT NULL,
                ip TEXT,
                user_agent TEXT
            )
            """
        )
        conn.commit()


def insert_lead(
    *,
    name: str,
    email: str,
    subject: str = "",
    course: str = "",
    message: str,
    email_sent: bool,
    ip: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> int:
    created_at_utc = datetime.now(timezone.utc).isoformat()

    with _connect() as conn:
        cur = conn.execute(
            """
            INSERT INTO leads (
                created_at_utc, name, email, subject, course, message,
                email_sent, ip, user_agent
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                created_at_utc,
                name,
                email,
                subject,
                course,
                message,
                1 if email_sent else 0,
                ip,
                user_agent,
            ),
        )
        conn.commit()
        return int(cur.lastrowid)


def fetch_leads(limit: int = 500) -> list[Dict[str, Any]]:
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT id, created_at_utc, name, email, subject, course, message, email_sent, ip, user_agent
            FROM leads
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]
