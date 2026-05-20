from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings."""
    
    DATABASE_URL: str = ""
    SECRET_KEY: str = "super-secret-key-for-dev-only"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(env_file=(".env", ".env.test"),
        env_file_encoding="utf-8",
        extra="ignore")

settings = Settings()