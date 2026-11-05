# 3d-models: the front door for agents and people. `make help` lists the targets.
# GNU make 3.81 features only, so it runs on macOS as well as Linux.

.DEFAULT_GOAL := help
SHELL := /bin/bash

.PHONY: help hooks check test test-utc lint leaks docs

help: ## List the targets
	@grep -E '^[a-zA-Z_-]+:.*## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*## "}; {printf "  %-10s %s\n", $$1, $$2}'

hooks: ## Install the git hooks (none are built yet)
	@echo "no hooks are installed yet: plan-driven-development's hooks aren't built"

test: ## Run the test suite
	@echo "no test command yet: the plan's CI task sets it"; exit 1

test-utc: ## Run the test suite under TZ=UTC
	@TZ=UTC $(MAKE) --no-print-directory test

lint: ## Lint the code
	@echo "no lint command yet: the plan's CI task sets it"; exit 1

leaks: ## Scan the whole git history for secrets
	gitleaks git --redact --no-banner .

docs: ## Render the docs site
	@echo "no docs site yet: the plan's site task sets it"; exit 1

check: test test-utc lint leaks docs ## Everything CI runs
