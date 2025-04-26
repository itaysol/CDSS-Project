from functools import lru_cache
from pydantic import BaseSettings, Field
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    database_url: str = Field(..., env="DATABASE_URL")

@lru_cache
def get_settings():
    return Settings()