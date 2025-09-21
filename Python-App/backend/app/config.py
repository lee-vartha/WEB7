from pydantic import BaseModel
from pydantic_settings import BaseSettings
from typing import List
import os

# defining the database url, jwt secret, jwt expiry and cors origins
class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///.//app.db"
    JWT_SECRET: str = "JWT_SECRET"
    JWT_EXPIRES_MINUTES: int = 60
    CORS_ORIGINS: str = "http://127.0.0.1:5500,http://localhost:5500"

# the value of env_file is set using os.path.join and os.path.dirname to construct the path to an .env file
# gets the directory where the current python file is located - join function combines this directory with .. (parent directory) and .env to create a path which points to an .env file a level above current files directory
# used to specify the lcoation of environment variable files in a  project which makes it easy to load config settings
    class Config:
        env_file = os.path.join(os.path.dirname(__file__), "..", ".env")

settings = Settings()