from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    TL_API_KEY: str = Field(..., env="TL_API_KEY")
    TWELVELABS_API_KEY: str = Field(..., env="TWELVELABS_API_KEY")
    GEMINI_API_KEY: str = Field(..., env="GEMINI_API_KEY")
    ELEVENLABS_API_KEY: str = Field(..., env="ELEVENLABS_API_KEY")
    
    CLOUDINARY_CLOUD_NAME: str = Field(..., env="CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY: str = Field(..., env="CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET: str = Field(..., env="CLOUDINARY_API_SECRET")
    
    FIREBASE_CREDENTIALS_PATH: str = Field(..., env="FIREBASE_CREDENTIALS_PATH")
    
    BACKEND_URL: str = Field(default="http://localhost:8000", env="BACKEND_URL")
    FRONTEND_URL: str = Field(default="http://localhost:5173", env="FRONTEND_URL")
    DEBUG: bool = Field(default=True, env="DEBUG")
    
    MAX_VIDEO_SIZE_MB: int = Field(default=500, env="MAX_VIDEO_SIZE_MB")
    FRAMES_PER_SECOND: int = Field(default=2, env="FRAMES_PER_SECOND")
    TEMP_DIR: str = Field(default="app/data/temp", env="TEMP_DIR")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

Path(settings.TEMP_DIR).mkdir(parents=True, exist_ok=True)
