"""Environment-specific configuration overrides."""

from enum import Enum
from pathlib import Path
from typing import TypedDict


class EnvironmentConfig(TypedDict, total=False):
    """Type hints for environment configuration."""

    log_level: str
    db_name: str
    db_relative_path: Path
    db_connection_string: str


class Environment(Enum):
    development = "development"
    integration = "integration"
    e2e = "e2e"
    qa = "qa"
    production = "production"


ENVIRONMENT_OVERRIDES: dict[str, EnvironmentConfig] = {
    Environment.development.value: {
        "log_level": "DEBUG",
        "db_name": "app",
        "db_relative_path": Path("infra/db"),
    },
    Environment.integration.value: {
        "log_level": "DEBUG",
        "db_name": "integration",
        "db_relative_path": Path("tests/integration/data/db"),
    },
    Environment.e2e.value: {
        "log_level": "DEBUG",
        "db_name": "e2e",
        "db_relative_path": Path("tests/e2e/data/db"),
    },
    Environment.qa.value: {
        "log_level": "INFO",
        # PostgreSQL example - set via environment variable APP_DB_CONNECTION_STRING
        # or uncomment and configure here:
        # "db_connection_string": "postgresql://user:password@host:5432/ecommerce_qa",
    },
    Environment.production.value: {
        "log_level": "WARNING",
        # PostgreSQL example - set via environment variable APP_DB_CONNECTION_STRING
        # or uncomment and configure here:
        # "db_connection_string": "postgresql://user:password@host:5432/ecommerce",
    },
}
