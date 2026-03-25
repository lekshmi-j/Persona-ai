# app/core/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # App
    APP_NAME: str = "PersonaAI"
    APP_ENV: str = "development"
    DEBUG: bool = True

    # CORS
    FRONTEND_URL: str = "http://localhost:3000"

    # API
    API_V1_PREFIX: str = "/api/v1"

    # DynamoDB
    DYNAMODB_ENDPOINT: str = "http://dynamodb-local:8000"
    AWS_ACCESS_KEY_ID: str = "local"
    AWS_SECRET_ACCESS_KEY: str = "local"
    AWS_REGION: str = "us-east-1"

    # JWT Auth — NEW
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()