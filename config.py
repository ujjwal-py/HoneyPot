from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # OpenAI
    openai_api_key: str
    openai_model: str = "gpt-4o"

    # API Security (optional at startup)
    api_key: Optional[str] = None

    # GUVI Hackathon
    guvi_callback_url: str = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

    # Server
    port: int = 8000
    environment: str = "development"

    # Database
    database_url: str = "sqlite:///./honeypot.db"

    # Redis (optional)
    redis_url: Optional[str] = None

    # Rate Limiting
    rate_limit_requests: int = 30
    rate_limit_window: int = 60

    # Conversation
    max_conversation_length: int = 20
    min_intelligence_count: int = 2
    callback_min_messages: int = 8

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
