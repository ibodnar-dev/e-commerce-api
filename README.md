# E-Commerce API

A modern e-commerce REST API built with FastAPI, featuring product catalog management with support for simple and variable products.

## Architecture

The project follows **Hexagonal Architecture** (Ports & Adapters) with clear separation of concerns:

- **Domain Layer** (`app/domain/`): Core business logic, models, and port interfaces
- **External Layer** (`app/external/`): Infrastructure implementations (database, logging, etc.)
- **API Layer** (`app/api/`): HTTP endpoints and request/response handling
- **Settings** (`app/settings/`): Configuration and environment management

## Prerequisites

- **Python 3.13+** - Required for this project
- **uv** - Fast Python package installer and resolver
- **Docker** - Required for running PostgreSQL database

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

### 5. Start the PostgreSQL database

```bash
# Start the development database using Docker Compose
make dc-up-db-dev
```

This starts a PostgreSQL 16 container with the following connection details:
- **Host**: localhost
- **Port**: 5432
- **Database**: app-dev
- **User**: app
- **Password**: app

### 6. Initialize the database

```bash
# Creates database tables
db-setup
```

### 7. Set up pre-commit hooks (optional but recommended)

```bash
pre-commit install
```

### 8. Run the API

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

# Run only unit tests (no database required)
make test-unit

# Run only integration tests (starts test database automatically)
make test-integration

# Run only e2e tests (starts test database automatically)
make test-e2e
```

**Note**: Integration and e2e tests automatically start the PostgreSQL test database container before running.

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
├── app/                              # Application code
│   ├── api/                         # API routes and endpoints
│   ├── domain/                      # Domain models and business logic
│   │   ├── models/                 # Domain entities
│   │   ├── ports/                  # Port interfaces (repositories, etc.)
│   │   └── services/               # Business logic services
│   ├── external/                    # External adapters (infrastructure)
│   │   ├── adapters/               # Concrete adapter implementations
│   │   │   ├── repositories/       # Database repository implementations
│   │   │   └── logging/            # Logging adapters
│   │   └── db/                     # Database connection and CLI tools
│   ├── settings/                    # Configuration and settings
│   └── main.py                      # FastAPI application entry point
├── infra/                           # Infrastructure configuration
│   └── docker/                      # Docker Compose files
│       └── local/                   # Local development setup
├── tests/                           # Test suite
│   ├── unit/                        # Unit tests
│   ├── integration/                 # Integration tests
│   └── e2e/                         # End-to-end tests
├── .claude/                         # Project documentation and guidelines
├── pyproject.toml                   # Project dependencies and configuration
└── Makefile                         # Common development tasks
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

- **development** (default) - PostgreSQL database on localhost:5432 (app-dev)
- **integration** - PostgreSQL test database on localhost:5433 (app-test)
- **e2e** - PostgreSQL test database on localhost:5433 (app-test)
- **qa** - PostgreSQL (configure via `APP_DB_CONNECTION_STRING`)
- **production** - PostgreSQL (configure via `APP_DB_CONNECTION_STRING`)

### Database Setup

The project uses Docker Compose to manage PostgreSQL databases for local development and testing:

- **Development database**: `postgres-dev` on port 5432 (persistent volume)
- **Test database**: `postgres-test` on port 5433 (ephemeral, uses tmpfs)

Start the databases using the Makefile commands:
```bash
# Start development database
make dc-up-db-dev

# Start test database (automatically runs before integration/e2e tests)
make dc-up-db-test
```

Or manually via docker-compose:
```bash
docker-compose -f infra/docker/local/docker-compose.yaml up postgres-dev -d
```

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
