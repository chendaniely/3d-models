# 3d-models: the front door for agents and people. `make help` lists the targets.
# GNU make 3.81 features only, so it runs on macOS as well as Linux.

.DEFAULT_GOAL := help
SHELL := /bin/bash

.PHONY: help hooks check test test-utc lint leaks models models-check privacy strip docs

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
	uv run --frozen scripts/privacy.py check

strip: ## Strip a photo's metadata, then look at it: make strip FILES="a.jpg b.png"
	uv run --frozen scripts/privacy.py strip $(FILES)

docs: ## Render the site into website/_site, failing on a broken link
	uv run --frozen scripts/sitedocs.py
	uv run --frozen scripts/gallery.py
	@set -o pipefail; quarto render website 2>&1 | tee website/.render.log
	@if grep -q 'Unable to resolve link target' website/.render.log; then \
	  echo "docs: an unresolved link, above"; exit 1; fi
	@if command -v lychee >/dev/null; then lychee --offline --no-progress website/_site; \
	else echo "lychee isn't installed: the offline link check runs in CI"; fi

check: test test-utc lint models-check privacy leaks docs ## Everything CI runs, and the suite under UTC
