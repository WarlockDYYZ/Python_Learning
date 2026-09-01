from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Short URL Service"
    DEBUG: bool = False
    BASE_URL: str = "http://localhost:8000"
    DATABASE_URL: str = "mysql+aiomysql://root:password@localhost:3306/short_url"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()