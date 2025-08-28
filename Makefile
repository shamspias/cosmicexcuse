.PHONY: help clean test coverage lint format install dev-install docs build publish-test publish

help:
	@echo "Available commands:"
	@echo "  make install       Install package"
	@echo "  make dev-install   Install with dev dependencies"
	@echo "  make test          Run tests"
	@echo "  make coverage      Run tests with coverage"
	@echo "  make lint          Run linters"
	@echo "  make format        Format code"
	@echo "  make docs          Build documentation"
	@echo "  make clean         Clean build artifacts"
	@echo "  make build         Build distribution packages"
	@echo "  make publish-test  Publish to Test PyPI"
	@echo "  make publish       Publish to PyPI"

install:
	pip install -e .

dev-install:
	pip install -r requirements-dev.txt
	pip install -e .
	pre-commit install

test:
	pytest tests/ -v

coverage:
	pytest tests/ --cov=cosmicexcuse --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated in htmlcov/index.html"

lint:
	isort --check-only cosmicexcuse tests
	black --check cosmicexcuse tests
	flake8 cosmicexcuse tests
	mypy cosmicexcuse --ignore-missing-imports

format:
	isort cosmicexcuse tests
	black cosmicexcuse tests

docs:
	cd docs && make clean && make html
	@echo "Documentation built in docs/_build/html/"

clean:
	rm -rf build dist *.egg-info
	rm -rf .pytest_cache .coverage htmlcov .mypy_cache
	rm -rf docs/_build
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*~" -delete

build: clean
	python -m build
	twine check dist/*

publish-test: build
	@echo "Uploading to Test PyPI..."
	twine upload --repository testpypi dist/*

publish: build
	@echo "Uploading to PyPI..."
	twine upload dist/*

# Development shortcuts
fix: format
	@echo "Code formatted successfully!"

check: lint test
	@echo "All checks passed!"

all: format lint test coverage docs build
	@echo "All tasks completed!"

# Installation helpers
deps:
	pip install -r requirements-dev.txt

update-deps:
	pip install --upgrade pip setuptools wheel
	pip install --upgrade -r requirements-dev.txt
