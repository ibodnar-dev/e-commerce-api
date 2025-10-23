from unittest.mock import Mock

import pytest
from sqlmodel import Session


@pytest.fixture
def mock_session():
    return Mock(spec=Session)
