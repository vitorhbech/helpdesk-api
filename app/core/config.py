from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings."""
    
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        """Configuration for the settings."""
        env_file = ".env"

settings = Settings()