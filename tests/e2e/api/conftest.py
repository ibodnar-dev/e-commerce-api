import pytest

from app.domain.models import Counter
from app.domain.models.system import CounterName
from infra.db.connection import DefaultSession


@pytest.fixture(scope="session")
def create_product_counter(setup_db):  # noqa: ARG001
    s = DefaultSession()
    counter = Counter(name=CounterName.product_sku_counter, current_value=0)
    s.add(counter)
    s.commit()
    yield counter
