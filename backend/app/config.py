from pydantic_settings import BaseSettings, SettingsConfigDict
#BaseSettings helps load environment variables from a .env
#SettingsConfigDict is used to configure how those settings are loaded (like saying: “read from .env”)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    # Actinia config
    ACTINIA_URL: str
    ACTINIA_USER: str
    ACTINIA_PASSWORD: str

    # JWT config
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database config
    DATABASE_URL: str

    # Add the missing fields
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    # Valkey config
    VALKEY_HOST: str
    VALKEY_PORT: int
    VALKEY_PASSWORD: str

    # Additional development settings
    DEBUG: bool
    LOG_LEVEL: str
settings = Settings()