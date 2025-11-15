import os

import pytest

from app.domain.models import SQLModel
from app.external.db import create_tables, default_engine
from app.external.db.connection import drop_tables
from app.settings import Environment


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    create_tables()
    SQLModel.metadata.create_all(default_engine)
    yield
    # Clean up: drop all tables after tests
    if os.environ.get("APP_ENV") == Environment.integration.value:
        drop_tables()
