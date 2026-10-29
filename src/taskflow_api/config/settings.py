from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "TaskFlow API Backend"
    environment: str = "development"
    debug: bool = True

    database_url: str = "sqlite+aiosqlite:///./taskflow.db"

    api_key: str = "taskflow-secret"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()