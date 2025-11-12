from enum import Enum
from typing import TypedDict


class EnvironmentConfig(TypedDict, total=False):
    log_level: str
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str


class Environment(Enum):
    development = "development"
    integration = "integration"
    e2e = "e2e"
    qa = "qa"
    production = "production"


ENVIRONMENT_OVERRIDES: dict[str, EnvironmentConfig] = {
    Environment.development.value: {
        "log_level": "DEBUG",
        "db_user": "app",
        "db_password": "app",
        "db_host": "localhost",
        "db_port": 5432,
        "db_name": "app-dev",
    },
    Environment.integration.value: {
        "log_level": "DEBUG",
        "db_user": "app",
        "db_password": "app",
        "db_host": "localhost",
        "db_port": 5433,
        "db_name": "app-test",
    },
    Environment.e2e.value: {
        "log_level": "DEBUG",
        "db_user": "app",
        "db_password": "app",
        "db_host": "localhost",
        "db_port": 5433,
        "db_name": "app-test",
    },
    Environment.qa.value: {
        "log_level": "INFO",
        # Set via environment variable APP_DB_CONNECTION_STRING
        # Example: postgresql://user:password@host:5432/ecommerce_qa
    },
    Environment.production.value: {
        "log_level": "WARNING",
    },
}
