# Makefile for backend code quality tools

.PHONY: lint format check all

# Run flake8 for code quality checks
lint:
	python3 -m flake8 .

# Run black for code formatting (check only)
format-check:
	python3 -m black --check .

# Run black for code formatting (apply changes)
format:
	python3 -m black .

# Run isort for import sorting (check only)
isort-check:
	python3 -m isort --check .

# Run isort for import sorting (apply changes)
isort:
	python3 -m isort .

# Run all checks
check: lint format-check isort-check

# Apply all formatting
all: format isort