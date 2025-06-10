import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://golden_user:localpassword123@localhost:5432/golden_compass")

    # Redis
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

    # AI APIs
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")

    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")  # Korean voice

    # Media paths
    MEDIA_PATH = Path("media")
    SHORTS_PATH = MEDIA_PATH / "shorts"
    LONGFORM_PATH = MEDIA_PATH / "longform"
    THUMBNAILS_PATH = MEDIA_PATH / "thumbnails"

    # Content settings
    SHORT_DURATION = 30  # seconds
    LONGFORM_DURATION = 600  # 10 minutes

    # App settings
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-for-local-dev")
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"


settings = Settings()