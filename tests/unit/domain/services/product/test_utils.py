from unittest.mock import Mock

import pytest

from app.domain.models import Counter
from app.domain.models.system import CounterName
from app.domain.services.exceptions import CounterNotInitializedError
from app.domain.services.product.utils import generate_sku, generate_slug


class TestGenerateSku:
    def test_increments_counter_and_returns_formatted_sku(self):
        counter = Counter(name=CounterName.product_sku_counter, current_value=5)
        mock_counter_repository = Mock()
        mock_counter_repository.find_by_name_for_update.return_value = counter

        sku = generate_sku(counter_repository=mock_counter_repository)

        assert sku == "SKU-000006"
        assert counter.current_value == 6
        mock_counter_repository.find_by_name_for_update.assert_called_once_with(
            CounterName.product_sku_counter
        )
        mock_counter_repository.save.assert_called_once_with(counter)

    def test_generates_sku_with_leading_zeros(self):
        counter = Counter(name=CounterName.product_sku_counter, current_value=99)
        mock_counter_repository = Mock()
        mock_counter_repository.find_by_name_for_update.return_value = counter

        sku = generate_sku(counter_repository=mock_counter_repository)

        assert sku == "SKU-000100"
        assert counter.current_value == 100

    def test_raises_error_when_counter_not_initialized(self):
        mock_counter_repository = Mock()
        mock_counter_repository.find_by_name_for_update.return_value = None

        with pytest.raises(CounterNotInitializedError) as exc_info:
            generate_sku(counter_repository=mock_counter_repository)

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
