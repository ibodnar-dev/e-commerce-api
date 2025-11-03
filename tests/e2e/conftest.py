import os

import pytest
from fastapi.testclient import TestClient

from app.domain.models import SQLModel
from app.main import app
from app.settings import settings
from app.settings.environments import Environment
from infra.db import default_engine


@pytest.fixture(scope="session")
def setup_db():
    SQLModel.metadata.create_all(default_engine)
    yield
    if os.environ.get("APP_ENV") == Environment.e2e.value:
        for item in settings.db_absolute_path.iterdir():
            item.unlink()


@pytest.fixture(scope="session")
def test_client():
    yield TestClient(app)
