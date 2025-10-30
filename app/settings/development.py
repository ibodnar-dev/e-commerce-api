from pathlib import Path

from app.settings.base import SettingsBase


class DevSettings(SettingsBase):
    log_level: str = "DEBUG"

    @property
    def database_path(self) -> Path:
        return Path(f"sqlite:///{self.project_root}/infra/db/{self.app_db_name}.sqlite3")

    @property
    def database_url(self) -> str:
        return f"sqlite:///{self.database_path}"


dev_settings = DevSettings()
