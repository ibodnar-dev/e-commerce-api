from pathlib import Path

from app.settings.base import SettingsBase


class E2ESettings(SettingsBase):
    log_level: str = "DEBUG"
    db_name: str = "e2e"

    @property
    def database_directory(self) -> Path:
        return Path(f"{self.project_root}/tests/e2e/data/db")

    @property
    def database_path(self) -> Path:
        return Path(f"{self.database_directory}/{self.db_name}.sqlite3")

    @property
    def database_url(self) -> str:
        return f"sqlite:///{self.database_path}"


e2e_settings = E2ESettings()
