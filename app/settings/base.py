from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class SettingsBase(BaseSettings):
    project_root: Path = Field(default=Path(__file__).resolve().parents[1])
    app_db_name: str = "app"

    @property
    def database_url(self) -> str:
        raise NotImplementedError
