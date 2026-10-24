"""
TechPulse AI - Database Module
SQLite schema and connection helper for articles, sources, verification,
summaries, digests, prompts, workflow runs, and settings.
"""

import sqlite3
import os
import json
from pathlib import Path

DB_PATH = Path(__file__).parent / "techpulse.db"

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Sources table (at least 10 trusted sources)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        type TEXT NOT NULL,
        official_url TEXT NOT NULL,
        credibility_rationale TEXT NOT NULL,
        trust_score INTEGER DEFAULT 95,
        verification_status TEXT DEFAULT 'verified',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Articles table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        abstract TEXT NOT NULL,
        content TEXT,
        url TEXT NOT NULL UNIQUE,
        source_id INTEGER,
        source_name TEXT NOT NULL,
        authors TEXT,
        category TEXT NOT NULL,
        published_at TEXT NOT NULL,
        retrieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_saved BOOLEAN DEFAULT 0,
        is_digest_candidate BOOLEAN DEFAULT 0,
        is_live_retrieved BOOLEAN DEFAULT 0,
        verification_status TEXT DEFAULT 'pending',
        FOREIGN KEY (source_id) REFERENCES sources (id)
    );
    """)

    # Verification Checks table (7-point source credibility checklist)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS verification_checks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id INTEGER NOT NULL UNIQUE,
        publisher_score INTEGER NOT NULL,
        author_score INTEGER NOT NULL,
        date_score INTEGER NOT NULL,
        evidence_score INTEGER NOT NULL,
        source_link_score INTEGER NOT NULL,
        duplicate_score INTEGER NOT NULL,
        outdated_score INTEGER NOT NULL,
        overall_score INTEGER NOT NULL,
        overall_status TEXT NOT NULL,
        checklist_json TEXT NOT NULL,
        evidence_notes TEXT NOT NULL,
        checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (article_id) REFERENCES articles (id) ON DELETE CASCADE
    );
    """)

    # Summaries table (with CSE relevance and claim checks)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS summaries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id INTEGER NOT NULL UNIQUE,
        headline TEXT NOT NULL,
        summary_text TEXT NOT NULL,
        why_it_matters_cse TEXT NOT NULL,
        key_facts_json TEXT NOT NULL,
        citations_json TEXT NOT NULL,
        claims_checked_json TEXT NOT NULL,
        is_approved BOOLEAN DEFAULT 0,
        edited_by_user BOOLEAN DEFAULT 0,
        model_used TEXT DEFAULT 'TechPulse-Heuristic-v1',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (article_id) REFERENCES articles (id) ON DELETE CASCADE
    );
    """)

    # Digest Editions table (supports 4 sample weekly editions and custom editions)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS digest_editions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        issue_number INTEGER NOT NULL UNIQUE,
        title TEXT NOT NULL,
        theme TEXT NOT NULL,
        week_date TEXT NOT NULL,
        status TEXT DEFAULT 'draft',
        draft_email_subject TEXT,
        draft_email_body TEXT,
        audio_script TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Digest Articles join table (article ordering & custom curation notes)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS digest_articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        digest_id INTEGER NOT NULL,
        article_id INTEGER NOT NULL,
        display_order INTEGER NOT NULL,
        custom_notes TEXT,
        FOREIGN KEY (digest_id) REFERENCES digest_editions (id) ON DELETE CASCADE,
        FOREIGN KEY (article_id) REFERENCES articles (id) ON DELETE CASCADE,
        UNIQUE(digest_id, article_id)
    );
    """)

    # Prompts table (7 categories)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prompts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        title TEXT NOT NULL,
        template_text TEXT NOT NULL,
        description TEXT NOT NULL,
        tags TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Workflow Runs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workflow_runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        finished_at TIMESTAMP,
        status TEXT NOT NULL,
        total_fetched INTEGER DEFAULT 0,
        total_verified INTEGER DEFAULT 0,
        total_summarized INTEGER DEFAULT 0,
        logs_json TEXT NOT NULL,
        triggered_by TEXT DEFAULT 'manual'
    );
    """)

    # User Settings table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized at:", DB_PATH)
