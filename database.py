import streamlit as st
import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path
from config import Config

class Database:
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or Config.DATABASE_PATH
        self._init_database()
    
    def _init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS candidates (
                session_id TEXT PRIMARY KEY,
                name TEXT,
                email TEXT,
                phone TEXT,
                experience INTEGER,
                position TEXT,
                location TEXT,
                tech_stack TEXT,
                language TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                questions TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES candidates(session_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sentiment_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                average_polarity REAL,
                average_subjectivity REAL,
                overall_label TEXT,
                trend TEXT,
                emotional_state TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES candidates(session_id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_candidate(self, session_id: str, data: Dict):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO candidates 
            (session_id, name, email, phone, experience, position, location, tech_stack, language)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session_id,
            data.get('name'),
            data.get('email'),
            data.get('phone'),
            data.get('experience'),
            data.get('position'),
            data.get('location'),
            data.get('tech'),
            data.get('language', 'English')
        ))
        
        conn.commit()
        conn.close()
    
    def save_questions(self, session_id: str, questions: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO questions (session_id, questions)
            VALUES (?, ?)
        """, (session_id, questions))
        
        conn.commit()
        conn.close()
    
    def save_sentiment(self, session_id: str, sentiment_data: Dict):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO sentiment_analysis 
            (session_id, average_polarity, average_subjectivity, overall_label, trend, emotional_state)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            session_id,
            sentiment_data.get('average_polarity'),
            sentiment_data.get('average_subjectivity'),
            sentiment_data.get('overall_label'),
            sentiment_data.get('trend'),
            sentiment_data.get('emotional_state')
        ))
        
        conn.commit()
        conn.close()
    
    def get_candidate(self, session_id: str) -> Optional[Dict]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM candidates WHERE session_id = ?", (session_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        return dict(row) if row else None
    
    def get_all_candidates(self, limit: int = 100) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM candidates ORDER BY created_at DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        
        conn.close()
        
        return [dict(row) for row in rows]
    
    def export_to_json(self, session_id: str) -> str:
        candidate = self.get_candidate(session_id)
        
        if not candidate:
            return json.dumps({"error": "Candidate not found"})
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT questions FROM questions WHERE session_id = ?", (session_id,))
        questions_row = cursor.fetchone()
        
        cursor.execute("SELECT * FROM sentiment_analysis WHERE session_id = ?", (session_id,))
        sentiment_row = cursor.fetchone()
        
        conn.close()
        
        export_data = {
            "candidate": candidate,
            "questions": questions_row['questions'] if questions_row else None,
            "sentiment": dict(sentiment_row) if sentiment_row else None
        }
        
        return json.dumps(export_data, indent=2, default=str)
    
    def get_statistics(self) -> Dict:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM candidates")
        total_candidates = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM questions")
        completed = cursor.fetchone()[0]
        
        cursor.execute("SELECT AVG(experience) FROM candidates")
        avg_experience = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            "total_candidates": total_candidates,
            "completed_screenings": completed,
            "average_experience": round(avg_experience, 1)
        }
    
    def cleanup_old_data(self, days: int = None):
        if days is None:
            days = Config.DATA_RETENTION_DAYS
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM candidates WHERE created_at < ?", (cutoff_date,))
        
        conn.commit()
        conn.close()
