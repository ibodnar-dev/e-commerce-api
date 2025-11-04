import os

from app.settings.base import Settings
from app.settings.environments import ENVIRONMENT_OVERRIDES, Environment


def get_settings() -> Settings:
    """Get settings with environment-specific overrides."""
    env = os.getenv("APP_ENV", Environment.development.value)
    env_overrides = ENVIRONMENT_OVERRIDES.get(
        env, ENVIRONMENT_OVERRIDES[Environment.development.value]
    )
    return Settings(**env_overrides)


# For backwards compatibility
settings = get_settings()

__all__ = ["settings", "get_settings", "Environment"]
