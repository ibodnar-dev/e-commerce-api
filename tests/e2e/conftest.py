import os

import pytest
from fastapi.testclient import TestClient

from app.domain.models import SQLModel
from app.external.db import default_engine
from app.main import app
from app.settings.environments import Environment


@pytest.fixture(scope="session")
def setup_db():
    # Create all tables before tests
    SQLModel.metadata.create_all(default_engine)
    yield
    # Clean up: drop all tables after tests
    if os.environ.get("APP_ENV") == Environment.e2e.value:
        SQLModel.metadata.drop_all(default_engine)


@pytest.fixture(scope="session")
def test_client():
    yield TestClient(app)
