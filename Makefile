.PHONY: test lint baseline

test:
	python -m pytest -q

lint:
	python -m ruff check src tests scripts

baseline:
	python scripts/run_all.py experiments/baseline-validation.yaml
