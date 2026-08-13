from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "App Van API"
    ENVIRONMENT: str = "development"

    DATABASE_URL: str = "sqlite:///./app_van.db"

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    
    # Esta é a variável que o Pydantic estava sentindo falta:
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    PAYMENT_GATEWAY_TOKEN: Optional[str] = None
    NOTIFICATION_API_KEY: Optional[str] = None

    # O extra="ignore" é o escudo que impede esse erro de acontecer
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore" 
    )

settings = Settings()