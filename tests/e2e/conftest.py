import pytest
from fastapi.testclient import TestClient

from app.domain.models import SQLModel
from app.main import app
from app.settings import settings
from infra.db import default_engine


@pytest.fixture(scope="session")
def setup_db():
    SQLModel.metadata.create_all(default_engine)
    yield
    for item in settings.database_directory.iterdir():
        item.unlink()


@pytest.fixture(scope="session")
def test_client():
    yield TestClient(app)
