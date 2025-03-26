import os
from dotenv import load_dotenv
from pydantic import BaseSettings

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    """Application settings."""
    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")
    DEFAULT_MODEL: str = os.environ.get("DEFAULT_MODEL", "gpt-4")
    REPO_PATH: str = os.environ.get("REPO_PATH", "repo")
    
    class Config:
        env_file = ".env"

# Create settings instance
settings = Settings()
