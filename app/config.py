# app/config.py
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

class Settings(BaseSettings):
    SERVER_HOST: str = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", 8000))
    CORS_ORIGINS: list[str] = os.getenv("CORS_ORIGINS", "*").split(",")
    API_URL: str = os.getenv("API_URL", "http://localhost:3000/")
    MODELS_DIR: str = os.getenv("MODELS_DIR", "models")
    DEVICE: str = os.getenv("DEVICE", "cuda:0")
    WEBHOOK_ENDPOINT: str = os.getenv("WEBHOOK_ENDPOINT", "secret")
    EVENT_ENDPOINT: str = os.getenv("EVENT_ENDPOINT", "secret")
    MODELS_ENDPOINT: str = os.getenv("MODELS_ENDPOINT", "secret")

def load_config() -> Settings:
    return Settings()