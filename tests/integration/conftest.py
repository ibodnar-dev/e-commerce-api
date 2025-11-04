import os

import pytest

from app.domain.models import SQLModel
from app.settings import Environment, settings
from infra.db import default_engine


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    settings.db_absolute_path.mkdir(parents=True, exist_ok=True)
    SQLModel.metadata.create_all(default_engine)
    yield
    if os.environ.get("APP_ENV") == Environment.integration.value:
        for item in settings.db_absolute_path.iterdir():
            item.unlink()
