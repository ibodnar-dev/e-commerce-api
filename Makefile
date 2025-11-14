.PHONY: test-e2e test-integration test-unit test-all help

help:
	@echo "Available test commands:"
	@echo "  make test-unit         - Run unit tests"
	@echo "  make test-integration  - Run integration tests (APP_ENV=integration)"
	@echo "  make test-e2e          - Run e2e tests (APP_ENV=e2e)"
	@echo "  make test-all          - Run all tests in sequence"

dc-up-db-dev:
	@echo "Starting postgres-dev"
	docker-compose -f infra/docker/local/docker-compose.yaml up postgres-dev -d

dc-up-db-test:
	@echo "Starting postgres-dev"
	docker-compose -f infra/docker/local/docker-compose.yaml up postgres-test -d --wait

test-unit:
	@echo "Running unit tests..."
	source .venv/bin/activate && pytest tests/unit -vs

test-integration: dc-up-db-test
	@echo "Running integration tests with APP_ENV=integration..."
	source .venv/bin/activate && export APP_ENV=integration && db-setup && pytest tests/integration -v

test-e2e: dc-up-db-test
	@echo "Running e2e tests with APP_ENV=e2e..."
	source .venv/bin/activate && export APP_ENV=integration && db-setup && pytest tests/e2e -v

test-all:
	@echo "Running all test suites..."
	@$(MAKE) test-unit
	@$(MAKE) test-integration
	@$(MAKE) test-e2e
