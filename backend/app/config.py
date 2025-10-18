from pydantic_settings import BaseSettings
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    CLOUDINARY_CLOUD_NAME: str = os.getenv("CLOUDINARY_CLOUD_NAME", "")
    CLOUDINARY_API_KEY: str = os.getenv("CLOUDINARY_API_KEY", "")
    CLOUDINARY_API_SECRET: str = os.getenv("CLOUDINARY_API_SECRET", "")
    
    FIREBASE_CREDENTIALS_PATH: str = os.getenv("FIREBASE_CREDENTIALS_PATH", "")
    
    MAX_VIDEO_SIZE_MB: int = 500
    FRAMES_PER_SECOND: int = 2
    TEMP_DIR: str = "app/data/temp"
    
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

Path(settings.TEMP_DIR).mkdir(parents=True, exist_ok=True)