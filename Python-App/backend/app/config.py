from pydantic import BaseModel
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///.//app.db"
    JWT_SECRET: str = "JWT_SECRET"
    JWT_EXPIRES_MINUTES: int = 60
    CORS_ORIGINS: str = "http://127.0.0.1:5500,http://localhost:5500"

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), "..", ".env")

settings = Settings()