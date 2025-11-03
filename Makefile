.PHONY: test-e2e test-integration test-unit test-all help

help:
	@echo "Available test commands:"
	@echo "  make test-unit         - Run unit tests"
	@echo "  make test-integration  - Run integration tests (APP_ENV=integration)"
	@echo "  make test-e2e          - Run e2e tests (APP_ENV=e2e)"
	@echo "  make test-all          - Run all tests in sequence"

test-unit:
	@echo "Running unit tests..."
	pytest tests/unit -v

test-integration:
	@echo "Running integration tests with APP_ENV=integration..."
	APP_ENV=integration pytest tests/integration -v

test-e2e:
	@echo "Running e2e tests with APP_ENV=e2e..."
	APP_ENV=e2e pytest tests/e2e -v

test-all:
	@echo "Running all test suites..."
	@$(MAKE) test-unit
	@$(MAKE) test-integration
	@$(MAKE) test-e2e
