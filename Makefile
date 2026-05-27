.PHONY: help setup test run run-build down clean

help:
	@echo "Available commands:"
	@echo "  make setup      - Install local dependencies for development"
	@echo "  make test       - Run unit and integration tests with coverage"
	@echo "  make run        - Start the project in Docker"
	@echo "  make run-build  - Rebuild containers and start the project"
	@echo "  make down       - Stop and remove Docker containers"
	@echo "  make clean      - Remove Python cache and temporary files"

setup:
	pip install -e packages/core
	pip install pytest pytest-cov

test:
	pytest tests/ -v --cov=packages/core/pdf_core

run:
	docker compose up

run-build:
	docker compose up --build

down:
	docker compose down

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -f .coverage
	@echo "Очистка завершена."