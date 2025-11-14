from unittest.mock import Mock

from app.domain.services.product.utils import generate_sku, generate_slug


class TestGenerateSku:
    def test_returns_formatted_sku_with_sequence_value(self):
        mock_counter_repository = Mock()
        mock_counter_repository.get_next_sku_value.return_value = 1

        sku = generate_sku(counter_repository=mock_counter_repository)

        assert sku == "SKU-000001"
        mock_counter_repository.get_next_sku_value.assert_called_once()

    def test_generates_sku_with_leading_zeros(self):
        mock_counter_repository = Mock()
        mock_counter_repository.get_next_sku_value.return_value = 100

        sku = generate_sku(counter_repository=mock_counter_repository)

        assert sku == "SKU-000100"

    def test_generates_sku_with_large_numbers(self):
        mock_counter_repository = Mock()
        mock_counter_repository.get_next_sku_value.return_value = 999999

        sku = generate_sku(counter_repository=mock_counter_repository)

        assert sku == "SKU-999999"


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
