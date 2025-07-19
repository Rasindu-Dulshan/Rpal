.PHONY: test lint run clean

test:
	pytest -v --cov=src tests/

lint:
	flake8 src/ tests/
	black --check src/ tests/

format:
	black src/ tests/

run:
	python src/main.py samples/factorial.rpal

clean:
	rm -rf __pycache__ .pytest_cache .coverage
