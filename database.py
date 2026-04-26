"""
database.py
-----------
SQLite persistence layer for the AI Resume Screening System.

Stores all screening results in a local SQLite database for:
  - History browsing and search
  - CSV/Excel export
  - Analytics and trend tracking

Tables:
  - screenings: Core screening results with scores and decisions
"""

import sqlite3
import json
import csv
import io
import os
from datetime import datetime
from typing import List, Dict, Optional
from logger import get_logger

logger = get_logger(__name__)

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenings.db")


# ── Database Setup ─────────────────────────────────────────────────────────────

def _get_connection() -> sqlite3.Connection:
    """Get a SQLite connection with row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    """Create tables if they don't exist."""
    conn = _get_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS screenings (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp       TEXT    NOT NULL DEFAULT (datetime('now')),
                candidate_name  TEXT,
                candidate_email TEXT,
                match_score     REAL    NOT NULL,
                ai_score        REAL    NOT NULL,
                decision        TEXT    NOT NULL,
                reason          TEXT,
                skill_match_pct REAL,
                matched_skills  TEXT,
                missing_skills  TEXT,
                top_keywords    TEXT,
                resume_excerpt  TEXT,
                jd_excerpt      TEXT,
                full_result     TEXT,
                notes           TEXT DEFAULT ''
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp ON screenings(timestamp DESC)
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_decision ON screenings(decision)
        """)
        conn.commit()
        logger.info(f"Database initialized at {DB_PATH}")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise
    finally:
        conn.close()


# Initialize on import
init_db()


# ── CRUD Operations ───────────────────────────────────────────────────────────

def save_screening(result: Dict) -> int:
    """
    Save a screening result to the database.

    Args:
        result: Full screening result dict from the API.

    Returns:
        int: The inserted row ID.
    """
    conn = _get_connection()
    try:
        skill_data = result.get("skill_analysis", {})
        parsed = result.get("parsed_resume", {})
        contact = parsed.get("contact", {}) if parsed else {}

        cursor = conn.execute("""
            INSERT INTO screenings (
                candidate_name, candidate_email,
                match_score, ai_score, decision, reason,
                skill_match_pct, matched_skills, missing_skills,
                top_keywords, resume_excerpt, jd_excerpt,
                full_result
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            contact.get("name", "Unknown"),
            contact.get("email", ""),
            result.get("match_score", 0),
            result.get("ai_score", 0),
            result.get("decision", ""),
            result.get("reason", ""),
            skill_data.get("skill_match_pct", 0),
            json.dumps(skill_data.get("matched_skills", [])),
            json.dumps(skill_data.get("missing_skills", [])),
            json.dumps(result.get("top_keywords", [])),
            "",  # resume_excerpt - don't store full text for privacy
            "",  # jd_excerpt
            json.dumps(result, default=str),
        ))
        conn.commit()
        row_id = cursor.lastrowid
        logger.info(f"Saved screening #{row_id}: {contact.get('name', 'Unknown')} → {result.get('decision')}")
        return row_id

    except Exception as e:
        logger.error(f"Failed to save screening: {e}")
        raise
    finally:
        conn.close()


def get_all_screenings(limit: int = 100, offset: int = 0) -> List[Dict]:
    """
    Retrieve all screenings, newest first.

    Args:
        limit: Max results to return.
        offset: Pagination offset.

    Returns:
        List of screening dicts.
    """
    conn = _get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM screenings ORDER BY timestamp DESC LIMIT ? OFFSET ?",
            (limit, offset)
        ).fetchall()
        return [_row_to_dict(r) for r in rows]
    finally:
        conn.close()


def get_screening_by_id(screening_id: int) -> Optional[Dict]:
    """Retrieve a single screening by ID."""
    conn = _get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM screenings WHERE id = ?", (screening_id,)
        ).fetchone()
        return _row_to_dict(row) if row else None
    finally:
        conn.close()


def search_screenings(query: str, limit: int = 50) -> List[Dict]:
    """
    Search screenings by name, email, or decision.
    """
    conn = _get_connection()
    try:
        search = f"%{query}%"
        rows = conn.execute("""
            SELECT * FROM screenings
            WHERE candidate_name LIKE ? OR candidate_email LIKE ? OR decision LIKE ?
            ORDER BY timestamp DESC LIMIT ?
        """, (search, search, search, limit)).fetchall()
        return [_row_to_dict(r) for r in rows]
    finally:
        conn.close()


def delete_screening(screening_id: int) -> bool:
    """Delete a screening by ID."""
    conn = _get_connection()
    try:
        cursor = conn.execute("DELETE FROM screenings WHERE id = ?", (screening_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def clear_all_screenings() -> int:
    """Delete all screenings. Returns count deleted."""
    conn = _get_connection()
    try:
        cursor = conn.execute("DELETE FROM screenings")
        conn.commit()
        count = cursor.rowcount
        logger.info(f"Cleared {count} screenings from database.")
        return count
    finally:
        conn.close()


def get_screening_stats() -> Dict:
    """
    Get aggregate statistics for the dashboard.
    """
    conn = _get_connection()
    try:
        total = conn.execute("SELECT COUNT(*) FROM screenings").fetchone()[0]
        shortlisted = conn.execute(
            "SELECT COUNT(*) FROM screenings WHERE decision = 'SHORTLISTED'"
        ).fetchone()[0]
        rejected = total - shortlisted

        avg_match = conn.execute(
            "SELECT AVG(match_score) FROM screenings"
        ).fetchone()[0] or 0

        avg_ai = conn.execute(
            "SELECT AVG(ai_score) FROM screenings"
        ).fetchone()[0] or 0

        return {
            "total_screenings": total,
            "shortlisted": shortlisted,
            "rejected": rejected,
            "shortlist_rate": round((shortlisted / total * 100) if total else 0, 1),
            "avg_match_score": round(avg_match, 2),
            "avg_ai_score": round(avg_ai, 2),
        }
    finally:
        conn.close()


# ── Export ─────────────────────────────────────────────────────────────────────

def export_to_csv() -> str:
    """
    Export all screenings to CSV format.

    Returns:
        str: CSV string content.
    """
    conn = _get_connection()
    try:
        rows = conn.execute(
            "SELECT id, timestamp, candidate_name, candidate_email, "
            "match_score, ai_score, decision, reason, skill_match_pct, "
            "matched_skills, missing_skills, top_keywords, notes "
            "FROM screenings ORDER BY timestamp DESC"
        ).fetchall()

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "ID", "Timestamp", "Candidate Name", "Email",
            "Match Score (%)", "AI Score (%)", "Decision", "Reason",
            "Skill Match (%)", "Matched Skills", "Missing Skills",
            "Top Keywords", "Notes"
        ])

        for row in rows:
            writer.writerow([
                row["id"], row["timestamp"], row["candidate_name"],
                row["candidate_email"], row["match_score"], row["ai_score"],
                row["decision"], row["reason"], row["skill_match_pct"],
                row["matched_skills"], row["missing_skills"],
                row["top_keywords"], row["notes"],
            ])

        csv_content = output.getvalue()
        logger.info(f"Exported {len(rows)} screenings to CSV.")
        return csv_content
    finally:
        conn.close()


# ── Helpers ────────────────────────────────────────────────────────────────────

def _row_to_dict(row: sqlite3.Row) -> Dict:
    """Convert a sqlite3.Row to a plain dict with JSON parsed fields."""
    d = dict(row)
    for key in ("matched_skills", "missing_skills", "top_keywords"):
        if d.get(key):
            try:
                d[key] = json.loads(d[key])
            except (json.JSONDecodeError, TypeError):
                pass
    # Don't return full_result in list queries (too large)
    d.pop("full_result", None)
    return d


# ─── Pro Analytics & Ranking (Pro) ─────────────────────────────────────────────

def get_top_candidates(limit: int = 10) -> List[Dict]:
    """
    Retrieve the overall highest-performing candidates in the system.
    """
    conn = _get_connection()
    try:
        rows = conn.execute("""
            SELECT id, candidate_name, match_score, ai_score, decision, skill_match_pct, timestamp
            FROM screenings
            WHERE decision = 'SHORTLISTED'
            ORDER BY match_score DESC, ai_score ASC
            LIMIT ?
        """, (limit,)).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_skill_distribution() -> Dict:
    """
    Analyses across all screenings to find the most common missing and matched skills.
    This provides 'Market Intelligence' for recruiters.
    """
    conn = _get_connection()
    try:
        rows = conn.execute("SELECT matched_skills, missing_skills FROM screenings").fetchall()
        
        matched_counter = Counter()
        missing_counter = Counter()
        
        for row in rows:
            try:
                ms = json.loads(row["matched_skills"])
                miss = json.loads(row["missing_skills"])
                for s in ms: matched_counter[s] += 1
                for s in miss: missing_counter[s] += 1
            except Exception:
                continue
                
        return {
            "top_matched_skills": dict(matched_counter.most_common(10)),
            "top_missing_skills": dict(missing_counter.most_common(10)),
            "total_screenings_analyzed": len(rows)
        }
    finally:
        conn.close()

from collections import Counter
