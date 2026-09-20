.PHONY: setup metadata check build

setup:
	uv sync --locked
	npm ci --ignore-scripts

metadata:
	uv run --python 3.12 --locked --script .plicara/check.py

check: metadata
	uv lock --check
	uv run --locked python -c "import runpy; failures = runpy.run_path('tokens/build.py')['audit'](); print('\n'.join(failures) if failures else 'Token audit passed'); raise SystemExit(bool(failures))"

build:
	uv run --locked python tokens/build.py
	uv run --locked python marks/generate.py
	uv run --locked python logo/build.py
	uv run --locked python logo/export.py
