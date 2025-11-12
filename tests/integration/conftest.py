import os

import pytest

from app.domain.models import SQLModel
from app.external.db import default_engine
from app.settings import Environment


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    # Create all tables before tests
    SQLModel.metadata.create_all(default_engine)
    yield
    # Clean up: drop all tables after tests
    if os.environ.get("APP_ENV") == Environment.integration.value:
        SQLModel.metadata.drop_all(default_engine)
