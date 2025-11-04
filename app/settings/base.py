from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment-specific overrides."""

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
        extra="ignore",
    )
    environment: str = Field(default="development")
    project_root: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[2])
    db_connection_string: str | None = None
    db_name: str = "app"
    db_relative_path: Path | None = None
    log_level: str = "INFO"

    @property
    def db_absolute_path(self) -> Path | None:
        return self.db_relative_path.resolve() if self.db_relative_path else None

    @property
    def database_path(self) -> Path | None:
        return self.db_absolute_path / f"{self.db_name}.sqlite3" if self.db_absolute_path else None

    @property
    def database_url(self) -> str | None:
        """Get the database connection URL.
        If db_connection_string is set (e.g., for PostgreSQL), uses that directly.
        Otherwise, constructs an SQLite URL
        """
        if self.db_connection_string:
            return self.db_connection_string
        return f"sqlite:///{self.database_path}"
