from pathlib import Path

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment-specific overrides."""

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
        extra="ignore",
    )
    environment: str = Field(default="development")
    log_level: str = "INFO"
    project_root: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[2])
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str

    @property
    def db_url(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql",
                host=self.db_host,
                port=self.db_port,
                username=self.db_user,
                password=self.db_password,
                path=self.db_name,
            )
        )
