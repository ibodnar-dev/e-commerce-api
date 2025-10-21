# Testing Guidelines

## Test Code Style

- **No docstrings**: Do not add docstrings to test functions
- **No comments**: Do not add comments in test code unless absolutely necessary
- Test function names should be self-explanatory (e.g., `test_get_product_repository_returns_sql_repository`)

## Test Organization

- Unit tests: `tests/unit/`
- Integration tests: `tests/integration/`
- Use `conftest.py` files for shared fixtures at appropriate levels

## Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run specific test file
pytest tests/unit/path/to/test_file.py
```
