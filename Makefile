# 3d-models: the front door for agents and people. `make help` lists the targets.
# GNU make 3.81 features only, so it runs on macOS as well as Linux.

.DEFAULT_GOAL := help
SHELL := /bin/bash

.PHONY: help hooks check test test-utc lint leaks models models-check privacy docs

help: ## List the targets
	@grep -E '^[a-zA-Z_-]+:.*## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*## "}; {printf "  %-13s %s\n", $$1, $$2}'

hooks: ## Install the git hooks (none are built yet)
	@echo "no hooks are installed yet: plan-driven-development's hooks aren't built"

test: ## Run the test suite
	uv run --frozen pytest -q

test-utc: ## Run the test suite under TZ=UTC
	@TZ=UTC $(MAKE) --no-print-directory test

lint: ## Lint the code: ruff check and ruff format --check
	uv run --frozen ruff check .
	uv run --frozen ruff format --check .

leaks: ## Scan the whole git history for secrets, merge commits' own changes included
	gitleaks git --redact --no-banner --log-opts="--all --full-history -m" .

models: ## Rebuild each changed design's STLs, picture and measurements (needs SolidCraft)
	uv run --frozen scripts/models.py build

models-check: ## Fail when a design has no build, a stale one, or the wrong name
	uv run --frozen scripts/models.py check

privacy: ## Fail on image metadata, a photo format the check can't read, or a home-folder path
	@echo "not built yet: Phase 1, Task 3 sets it"; exit 1

docs: ## Render the site into website/_site, failing on a broken link
	@echo "not built yet: Phase 1, Task 4 sets it"; exit 1

check: test test-utc lint models-check leaks ## Everything CI runs, and the suite under UTC
