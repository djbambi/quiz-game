.PHONY: test lint format check

test:
	poetry run pytest -q

lint:
	poetry run ruff check .

format:
	poetry run ruff format .

check: lint test