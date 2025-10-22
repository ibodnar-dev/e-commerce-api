# Testing Guidelines

## Test Code Style

- **No docstrings**: Do not add docstrings to test functions
- **No comments**: Do not add comments in test code unless absolutely necessary
- Test function names should be self-explanatory (e.g., `test_get_product_repository_returns_sql_repository`)

## Test Organization

- Unit tests: `tests/unit/`
- Integration tests: `tests/integration/`
- Use `conftest.py` files for shared fixtures at appropriate levels
- **Test structure**: Create a test class for each function or class being tested
- **Test methods**: Each method in the test class should test a different case
- **Method naming**: Method names should clearly describe the case being tested (e.g., `test_increments_counter_and_returns_formatted_sku`)

## Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run specific test file
pytest tests/unit/path/to/test_file.py
```
