import os

env = os.getenv("APP_ENV", "development")

if env == "e2e":
    from .e2e import e2e_settings as settings
else:
    from .development import dev_settings as settings

__all__ = ["settings"]
