from unittest.mock import Mock

import pytest

from app.domain.models import Counter
from app.domain.models.system import CounterName
from app.domain.services.exceptions import CounterNotInitializedError
from app.domain.services.product.utils import generate_sku, generate_slug


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

    def test_raises_error_when_counter_not_initialized(self, mock_session):
        mock_result = Mock()
        mock_result.first.return_value = None

        mock_query = Mock()
        mock_query.with_for_update.return_value = mock_query
        mock_session.exec.return_value = mock_result

        with pytest.raises(CounterNotInitializedError) as exc_info:
            generate_sku(session=mock_session)

        assert str(exc_info.value) == "Product SKU counter is not initialized"


class TestGenerateSlug:
    def test_converts_spaces_to_hyphens_and_lowercase(self):
        result = generate_slug("Product Name")

        assert result == "product-name"

    def test_removes_special_characters(self):
        result = generate_slug("Product! @Name# $Test%")

        assert result == "product-name-test"

    def test_handles_mixed_case_with_numbers(self):
        result = generate_slug("Product 123 Name")

        assert result == "product-123-name"

    def test_preserves_hyphens(self):
        result = generate_slug("Pre-Owned Product")

        assert result == "pre-owned-product"

    def test_handles_multiple_consecutive_spaces(self):
        result = generate_slug("Product    Name")

        assert result == "product----name"

    def test_handles_empty_string(self):
        result = generate_slug("")

        assert result == ""

    def test_handles_only_special_characters(self):
        result = generate_slug("!@#$%^&*()")

        assert result == ""

    def test_handles_unicode_characters(self):
        result = generate_slug("Café Product")

        assert result == "café-product"
