from unittest.mock import Mock

from app.domain.models import Counter
from app.domain.models.system import CounterName
from app.domain.services.product.utils import generate_sku


class TestGenerateSku:

    def test_increments_counter_and_returns_formatted_sku(self, mock_session):
        counter = Counter(name=CounterName.PRODUCT_SKU_COUNTER, current_value=5)

        mock_result = Mock()
        mock_result.first.return_value = counter

        mock_query = Mock()
        mock_query.with_for_update.return_value = mock_query
        mock_session.exec.return_value = mock_result

        sku = generate_sku(session=mock_session)

        assert sku == "SKU-000006"
        assert counter.current_value == 6
        mock_session.add.assert_called_once_with(counter)
        mock_session.flush.assert_called_once()

    def test_generates_sku_with_leading_zeros(self, mock_session):
        counter = Counter(name=CounterName.PRODUCT_SKU_COUNTER, current_value=99)

        mock_result = Mock()
        mock_result.first.return_value = counter

        mock_query = Mock()
        mock_query.with_for_update.return_value = mock_query
        mock_session.exec.return_value = mock_result

        sku = generate_sku(session=mock_session)

        assert sku == "SKU-000100"
        assert counter.current_value == 100
