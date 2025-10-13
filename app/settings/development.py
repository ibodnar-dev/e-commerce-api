from app.settings.base import SettingsBase


class DevSettings(SettingsBase):
    @property
    def database_url(self) -> str:
        return f"sqlite:///{self.project_root}/infra/db/{self.app_db_name}.sqlite3"


dev_settings = DevSettings()
