from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv
import os

env_path = Path(__file__).parent.parent.parent / ".env"  # поднимаемся на 3 уровня до D:\diplom
load_dotenv(env_path)
SECRECT_KEY = os.getenv("SECRECT_KEY")

class Settings(BaseSettings):
    SECRET_KEY: str = SECRECT_KEY
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    class Config:
        env_file = ".env"

settings = Settings()