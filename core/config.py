import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
    FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS", "")

    # For API key rotation
    GROQ_KEYS = [k for k in [os.getenv("GROQ_API_KEY"), os.getenv("GROQ_API_KEY_BACKUP")] if k]
    GEMINI_KEYS = [k for k in [os.getenv("GEMINI_API_KEY"), os.getenv("GEMINI_API_KEY_BACKUP1"), os.getenv("GEMINI_API_KEY_BACKUP2")] if k]

settings = Settings()
