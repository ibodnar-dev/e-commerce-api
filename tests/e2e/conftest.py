import os

import pytest
from fastapi.testclient import TestClient

from app.domain.models import SQLModel
from app.external.db import create_tables, default_engine
from app.external.db.connection import drop_tables
from app.main import app
from app.settings.environments import Environment


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    create_tables()
    SQLModel.metadata.create_all(default_engine)
    yield
    if os.environ.get("APP_ENV") == Environment.e2e.value:
        drop_tables()


@pytest.fixture(scope="session")
def test_client():
    yield TestClient(app)
