import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT = int(os.getenv("APP_PORT", 10000))
    CACHE_TTL = int(os.getenv("CACHE_TTL", 3600))  # 1 hour
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

config = Config()
