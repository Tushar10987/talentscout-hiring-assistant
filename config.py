"""
Configuration for TalentScout Hiring Assistant
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Application
    APP_TITLE = "TalentScout Hiring Assistant"
    APP_ICON = "🤖"
    
    # API Configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL = "llama-3.3-70b-versatile"
    
    # Database
    DATABASE_PATH = "talentscout.db"
    
    # Language Support
    SUPPORTED_LANGUAGES = {
        "English": "en",
        "Hindi": "hi",
        "Spanish": "es",
        "French": "fr",
        "German": "de"
    }
    
    DEFAULT_LANGUAGE = "English"
    DEFAULT_THEME = "dark"
    
    # Question Generation
    MIN_QUESTIONS_PER_TECH = 3
    MAX_QUESTIONS_PER_TECH = 5
    
    # Features
    ENABLE_SENTIMENT_ANALYSIS = True
    ENABLE_MULTILINGUAL = True
    ENABLE_CACHING = True
    ENABLE_ADMIN_PANEL = False
    
    # Sentiment Analysis
    SENTIMENT_POSITIVE_THRESHOLD = 0.1
    SENTIMENT_NEGATIVE_THRESHOLD = -0.1
    
    # Performance
    CACHE_TTL = 3600
    MAX_RESPONSE_TIME = 5
    
    # Privacy
    DATA_RETENTION_DAYS = 90
    
    @classmethod
    def get_language_code(cls, language: str) -> str:
        return cls.SUPPORTED_LANGUAGES.get(language, "en")
