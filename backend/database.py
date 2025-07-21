import sqlite3
import json
from datetime import datetime

DB_NAME = "applications.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT,
            resume_text TEXT,
            jd_text TEXT,
            match_score REAL,
            matched_keywords TEXT,
            missing_keywords TEXT,
            created_at TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_application(company_name, resume, jd, match_score, matched, missing):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO applications (company_name, resume_text, jd_text, match_score, matched_keywords, missing_keywords, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        company_name,
        resume,
        jd,
        match_score,
        json.dumps(matched),
        json.dumps(missing),
        datetime.utcnow()
    ))
    conn.commit()
    conn.close()
