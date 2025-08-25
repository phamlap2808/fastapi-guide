from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Ứng dụng đọc cấu hình từ biến môi trường/.env.

    - Prefix biến môi trường: APP_
    - Ví dụ: APP_DATABASE_URL, APP_DEBUG
    """

    app_name: str = "FastAPI Guide"
    api_v1_str: str = "/api/v1"
    env: str = "dev"
    debug: bool = True

    # SQLAlchemy async URL, ví dụ:
    # - Postgres: postgresql+asyncpg://user:pass@localhost:5432/dbname
    # - SQLite: sqlite+aiosqlite:///./app.db
    database_url: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_",
        case_sensitive=False,
    )


settings = Settings()


