from __future__ import annotations
from enum import Enum
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from urllib.parse import quote_plus
from pydantic import Field


_REPO_ROOT = Path(__file__).resolve().parents[3]
_ENV_PATH = _REPO_ROOT / ".env"

class Environment(str, Enum):
    LOCAL = "local"
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(_ENV_PATH) if _ENV_PATH.exists() else None,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    db_user: str = "admin"
    db_password: str = "my_very_secure_password_123"
    db_name: str = "smartstock_db"
    db_port: int = 5432
    db_host: str = "localhost"
    env_database_url: str | None = Field(default=None, validation_alias="DATABASE_URL")
    debug: bool = False

    # Comma-separated origins, e.g. "http://localhost:3000,https://app.example.com"
    cors_origins: str = Field(
        default="http://localhost:3000,http://127.0.0.1:3000",
        validation_alias="CORS_ORIGINS",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        raw = self.cors_origins.strip()
        if not raw:
            return []
        return [x.strip() for x in raw.split(",") if x.strip()]

    @property
    def database_url(self) -> str:
        raw = (self.env_database_url or "").strip()
        if raw and "%(" not in raw and raw.startswith("postgresql"):
            if raw.startswith("postgresql+asyncpg://"):
                return raw
            if raw.startswith("postgresql+psycopg://"):
                return raw.replace("postgresql+psycopg://", "postgresql+asyncpg://", 1)
            if raw.startswith("postgresql://"):
                return raw.replace("postgresql://", "postgresql+asyncpg://", 1)
        user = quote_plus(self.db_user)
        password = quote_plus(self.db_password)
        return (
            f"postgresql+asyncpg://{user}:{password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )
        
settings = Settings()