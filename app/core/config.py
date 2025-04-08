from typing import Optional, List
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    
    Defaults are set for development. Override with environment variables
    or .env file for different environments.
    """
    # Application
    APP_NAME: str = "E-Commerce API"
    API_PREFIX: str = ""
    DEBUG: bool = True
    VERSION: str = "1.0.0"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE_PATH: str = "logs/api.log"
    LOKI_URL: Optional[str] = "http://localhost:3100/loki/api/v1/push"
    LOKI_ENABLED: bool = True
    
    # Monitoring
    METRICS_ENABLED: bool = True
    METRICS_PATH: str = "/metrics"
    MONITORING_NAMESPACE: str = "api"
    
    # Database (for future use)
    DB_URL: Optional[str] = None
    DB_MAX_CONNECTIONS: int = 10
    DB_CONNECT_RETRY: int = 3
    
    # Cache (for future use)
    CACHE_URL: Optional[str] = None
    CACHE_EXPIRY_SECONDS: int = 300
    
    # Security (for future use)
    SECRET_KEY: str = "development_secret_key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    AUTH_ENABLED: bool = False
    
    # Default media paths
    STATIC_DIR: str = "static"
    MEDIA_DIR: str = "media"
    
    # Other
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings as a singleton
    
    Using lru_cache to avoid reloading the settings for each call
    """
    return Settings()


settings = get_settings()


def get_environment_name() -> str:
    """Helper to get current environment name"""
    return settings.ENVIRONMENT