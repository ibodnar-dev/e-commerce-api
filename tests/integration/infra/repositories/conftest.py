import pytest

from app.external.adapters.repositories import SQLCounterRepository
from app.external.db import DefaultSession


@pytest.fixture(scope="class")
def db_session():
    yield DefaultSession()


@pytest.fixture(scope="class")
def counter_repository(db_session):
    yield SQLCounterRepository(session=db_session)
    db_session.rollback()
