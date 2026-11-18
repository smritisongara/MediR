import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory: C:\Users\hp\Desktop\MediR
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file if it exists
load_dotenv(BASE_DIR / ".env")

class Config:
    """Application configuration settings for MediR AI."""
    APP_NAME = "MediR"
    APP_TAGLINE = "Understand Better. Communicate Better. Live Better."
    BASE_DIR = BASE_DIR
    
    SECRET_KEY = os.getenv("SECRET_KEY", "medir-hackathon-secure-session-key-2025")
    
    # Uploads configuration
    UPLOAD_FOLDER = BASE_DIR / "uploads"
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32 MB max upload limit (supports short videos)
    ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "webp", "mp4", "webm", "mov"}
    
    # Database configuration
    DATABASE_DIR = BASE_DIR / "database"
    DATABASE_PATH = DATABASE_DIR / "medir.db"
    
    # AI Keys (Optional - Intelligent Offline Fallback active if absent)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")
    
    # Server configuration
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", 5000))
    DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")

# Ensure required directories exist
Config.UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
Config.DATABASE_DIR.mkdir(parents=True, exist_ok=True)
