# E-Commerce API

A modern e-commerce REST API built with FastAPI, featuring product catalog management with support for simple and variable products.

## Prerequisites

- **Python 3.13+** - Required for this project
- **uv** - Fast Python package installer and resolver

## Getting Started

### 1. Install uv (if not already installed)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via pip
pip install uv
```

### 2. Clone the repository

```bash
git clone <repository-url>
cd e-commerce-api
```

### 3. Install dependencies

```bash
# Creates virtual environment and installs all dependencies
uv sync
```

### 4. Activate the virtual environment

```bash
source .venv/bin/activate
```

### 5. Initialize the database

```bash
# Creates database tables
db-setup
```

This creates the SQLite database at `infra/db/app.sqlite3` with all required tables.

### 6. Set up pre-commit hooks (optional but recommended)

```bash
pre-commit install
```

### 7. Run the API

```bash
# Development mode with auto-reload
fastapi dev app/main.py

# Or using uvicorn directly
uvicorn app.main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive docs**: http://localhost:8000/docs
- **Health check**: http://localhost:8000/health

## Running Tests

The project includes a Makefile with convenient test commands:

```bash
# Run all tests (unit, integration, e2e)
make test-all

# Run only unit tests
make test-unit

# Run only integration tests
make test-integration

# Run only e2e tests
make test-e2e
```

Or use pytest directly:

```bash
# All tests
pytest

# Specific test file
pytest tests/unit/test_product_repository.py

# With coverage
pytest --cov=app --cov=external
```

## Project Structure

```
e-commerce-api/
├── app/                    # Application code
│   ├── api/               # API routes and endpoints
│   ├── domain/            # Domain models and business logic
│   ├── settings/          # Configuration and settings
│   └── main.py            # FastAPI application entry point
├── infra/                 # Infrastructure code
│   ├── db/                # Database connection and setup
│   └── repositories/      # Data access layer
├── tests/                 # Test suite
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── e2e/               # End-to-end tests
├── .claude/               # Project documentation and guidelines
├── pyproject.toml         # Project dependencies and configuration
└── Makefile               # Common development tasks
```

## Configuration

The application uses environment-based configuration. Settings can be overridden via environment variables with the `APP_` prefix:

```bash
# Example: Run with custom database
APP_DB_CONNECTION_STRING="postgresql://user:pass@localhost:5432/ecommerce" fastapi dev app/main.py

# Example: Set environment
APP_ENVIRONMENT=production fastapi dev app/main.py
```

### Environments

- **development** (default) - Uses SQLite at `infra/db/app.sqlite3`
- **integration** - Separate SQLite database for integration tests
- **e2e** - Separate SQLite database for e2e tests
- **qa** - Typically uses PostgreSQL (configure via `APP_DB_CONNECTION_STRING`)
- **production** - Uses PostgreSQL (configure via `APP_DB_CONNECTION_STRING`)

## Development Workflow

### Code Quality

The project uses:
- **Ruff** - Fast Python linter and formatter
- **Pre-commit hooks** - Automated checks before commits

```bash
# Run linter
ruff check .

# Auto-fix issues
ruff check --fix .

# Format code
ruff format .
```

### CLI Tools

```bash
# Initialize/recreate database
db-setup
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
