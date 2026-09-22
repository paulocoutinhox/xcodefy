.DEFAULT_GOAL := help

UV ?= uv

.PHONY: help install test coverage lint format build check clean version set-version bump

help:
	@echo "xcodefy development commands"
	@echo "  make install    install the project and development tools with uv"
	@echo "  make test       run the test suite"
	@echo "  make coverage   run tests with the 100% branch coverage gate"
	@echo "  make lint       check the code"
	@echo "  make format     format and fix the code"
	@echo "  make build      build the wheel and source distribution"
	@echo "  make check      validate built distributions"
	@echo "  make clean      remove generated artifacts"
	@echo "  make version    show the project version"
	@echo "  make set-version VERSION=x.y.z   set the project version"
	@echo "  make bump PART=major|minor|patch  raise the project version"

install:
	$(UV) sync --all-groups

test:
	$(UV) run pytest

coverage:
	$(UV) run pytest --cov --cov-branch --cov-report=term-missing --cov-report=xml

lint:
	$(UV) run ruff check .
	$(UV) run ruff format --check .

format:
	$(UV) run ruff check --fix .
	$(UV) run ruff format .

build:
	rm -rf dist
	$(UV) build

check:
	$(UV) run twine check dist/*

version:
	@$(UV) version --short

set-version:
	@test -n "$(VERSION)" || { echo "usage: make set-version VERSION=x.y.z"; exit 1; }
	$(UV) version $(VERSION)

bump:
	@test -n "$(PART)" || { echo "usage: make bump PART=major|minor|patch"; exit 1; }
	$(UV) version --bump $(PART)

clean:
	rm -rf dist build htmlcov .coverage coverage.xml .pytest_cache .ruff_cache .venv
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
