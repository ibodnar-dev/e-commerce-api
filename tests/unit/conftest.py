import pytest
from unittest.mock import Mock
from sqlmodel import Session


@pytest.fixture
def mock_session():
    return Mock(spec=Session)
