.DEFAULT_GOAL = help

run:
	uv run uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 5001

run-tests:  # Run tests
	uv run python -m pytest -v

coverage-report:  # Generate coverage report
	uv run python -m pytest --cov

help:  # Display help
	@grep -E '^[a-zA-Z_-]+:.*?# .*$$' $(MAKEFILE_LIST) \
	  | sort \
	  | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[0;32m%-30s\033[0m %s\n", $$1, $$2}'
