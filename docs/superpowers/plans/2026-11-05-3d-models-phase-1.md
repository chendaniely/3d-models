# 3d-models Phase 1: the repo and the first models, implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking. The project's `AGENTS.md` holds every rule for running
> it (the task loop, reviews, stops, commits, pushing) and outranks this header where they differ.

**Goal:** the pipeline from a SolidCraft design to a gallery page with a 3D viewer, guarded by CI,
with three models on it: the dowel fit-test coupon and the sconce's wall block and cord clamp,
each in three dowel sizes.

**Architecture:** designs are plain-text `.sc` files under `models/<slug>/`; `scripts/models.py`
builds each changed one with `solidcraft-cli`, one STL per size, and records every file's SHA-256;
`scripts/privacy.py` keeps image metadata and home-folder paths out; `scripts/sitedocs.py` copies
the design docs into the site, Quarto's syntax escaped; `scripts/gallery.py` writes a page per
model, which `website/assets/stl-viewer.js` turns into a 3D view with a local copy of three.js.
CI runs every check on each push and deploys the site from `main`.

**Tech Stack:** Python 3.12 under uv (pytest, ruff, PyYAML, Pillow), solidcraft-cli 0.30.1,
Quarto 1.11.6, three.js 0.187.0 (copied from npm's package), GitHub Actions pinned by commit SHA,
GitHub Pages, gitleaks 8.30.1, lychee 0.24.2.

**Spec:** `docs/superpowers/specs/2026-11-05-3d-models-design.md`

**Now:** Phase end, step 1: The final whole-branch review.

***

## Global Constraints

- Python 3.12 (`.python-version`), run only through uv: `uv sync --frozen`, `uv run --frozen …`;
  never pip.
- ruff `line-length = 100`, `target-version = "py312"`; Markdown is not ruff's to format.
- Every command is a `make` target; GNU make 3.81 features only.
- solidcraft-cli 0.30.1. Designs are saved with `file.save_as`, `format: json`, `cache: false`.
- A model's folder name is lowercase words joined by hyphens, its design `<folder>.sc` alone.
- The dowel parts are saved at 1 inch (25.4 mm) and list `3/4 in` (19.05 mm) and `25 mm` as sizes
  (Q&A answer 14).
- Models, pictures and docs are CC BY-NC 4.0; code is MIT (Q&A answer 15).
- Quarto 1.11.6; three.js 0.187.0, served from `website/assets/three/`, never a CDN.
- Every CI action pinned to a full commit SHA with its version in a comment.
- The site is <https://chendaniely.github.io/3d-models/>; the repo
  <https://github.com/chendaniely/3d-models>.
- No home-folder path, private address or personal detail in any committed file; images carry no
  metadata but a colour profile.
- Every commit: message in a file, `git commit -F`, staged by path, `Plan:` trailer checked.
- No hooks yet: every push waits for `make leaks privacy models-check` to pass, and for Dan's OK,
  the request naming every binary file the push adds, unless Dan gives a standing OK, as he did
  for Phase 1's end (Phase 1 Q&A 5).

## Review Focus

1. **A design saved from the SolidCraft app in its default zip format:** it builds and checks like
   a text one (Task 2, `test_build_and_check_take_a_design_saved_as_a_zip`).
2. **A design named `Hook.sc` in `models/hook/`,** which macOS finds and Linux doesn't:
   `make models-check` names it (Task 2, `test_check_names_a_design_not_named_after_its_folder`).
3. **A commit with a new design and record but an old STL:** `make models-check` names the file
   (Task 2, `test_check_names_a_built_file_that_is_not_the_one_recorded`).
4. **`Supports: no` in a `model.yml`,** which YAML reads as false: `make docs` says to quote it
   (Task 5, the `quote the print setting` case).
5. **A phone photo, `IMG_0001.JPG`, with the camera's serial number but no GPS:** refused like a
   GPS one (Task 3, `test_check_names_a_camera_serial_without_any_gps` and `PRINT.JPG`).

***

### Task 1: The Python toolchain and CI

**Tier:** 1 (the `leaks` job is a guard: if wrong, a leak passes silently) · **Scenarios:** S04,
S05

**Files:**
- Create: `pyproject.toml`, `.python-version`, `uv.lock` (by `uv lock`), `tests/test_makefile.py`,
  `.github/workflows/ci.yml`, `.github/dependabot.yml`
- Modify: `Makefile` (whole file below), `.gitignore` (blocks appended)

**Interfaces:**
- Consumes: nothing.
- Produces: `make test` (`uv run --frozen pytest -q`), `make test-utc`, `make lint`
  (`ruff check .` and `ruff format --check .`), `make leaks` (merge commits included);
  placeholder targets `models`, `models-check` (Task 2), `privacy` (Task 3) and `docs` (Task 4)
  that fail with "not built yet"; CI jobs `tests` and `leaks`; ruff's first-party modules
  `conftest`, `gallery`, `models`, `privacy`, `sitedocs`.

- [x] **Step 0: Record the base:** `git rev-parse HEAD > .git/TASK_BASE`.
- [x] **Step 1: Write the uv project.**

`pyproject.toml`:

```toml
[project]
name = "3d-models"
version = "0.1.0"
description = "SolidCraft models, the STL files exported from them, and the tooling that builds the gallery."
requires-python = ">=3.12"
dependencies = [
    "pillow>=12.0",
    "pyyaml>=6.0",
]

[dependency-groups]
dev = [
    "pytest>=9.0",
    "ruff>=0.14",
]

[tool.uv]
package = false

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra"

[tool.ruff]
line-length = 100
target-version = "py312"
# scripts/commitmsg.py is plan-driven-development's copy, kept byte-identical to the skill's;
# Markdown is excluded because the plans quote code exactly as it is to be written.
extend-exclude = ["scripts/commitmsg.py", "*.md", "website/_site", "website/.quarto"]

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]

[tool.ruff.lint.isort]
known-first-party = ["conftest", "gallery", "models", "privacy", "sitedocs"]
```

  `.python-version` holds one line, `3.12`. Then `uv lock` (writes `uv.lock`) and
  `uv sync --frozen`. Expected: CPython 3.12, and `pillow`, `pytest`, `pyyaml` and `ruff` in
  `.venv`.

- [x] **Step 2: Write the failing test.**

`tests/test_makefile.py`:

```python
"""The Makefile is the front door: every target AGENTS.md names is there, and help lists it."""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS = [
    "help", "hooks", "check", "test", "test-utc", "lint", "leaks",
    "models", "models-check", "privacy", "docs",
]  # fmt: skip


def test_help_lists_every_target() -> None:
    result = subprocess.run(
        ["make", "--no-print-directory", "help"], cwd=ROOT, capture_output=True, text=True,
        check=True,
    )  # fmt: skip
    listed = {line.split()[0] for line in result.stdout.splitlines() if line.strip()}
    assert set(TARGETS) <= listed, sorted(set(TARGETS) - listed)
```

- [x] **Step 3: Run it; watch it fail.** `uv run --frozen pytest -q tests/test_makefile.py`.
  Expected: `AssertionError: ['models', 'models-check', 'privacy']`.
- [x] **Step 4: Write the Makefile,** the whole file:

`Makefile`:

```makefile
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
	@echo "not built yet: Phase 1, Task 2 sets it"; exit 1

models-check: ## Fail when a design has no build, a stale one, or the wrong name
	@echo "not built yet: Phase 1, Task 2 sets it"; exit 1

privacy: ## Fail on image metadata, a photo format the check can't read, or a home-folder path
	@echo "not built yet: Phase 1, Task 3 sets it"; exit 1

docs: ## Render the site into website/_site, failing on a broken link
	@echo "not built yet: Phase 1, Task 4 sets it"; exit 1

check: test test-utc lint leaks ## Everything CI runs, and the suite under UTC
```

  And append to `.gitignore`:

```text

# the site: the generated doc and model pages, and the render log
website/superpowers/
website/models/
website/.render.log

# the Playwright browser tool's screenshots and logs
.playwright-mcp/

# SolidCraft keeps the design it overwrote as <name>.sc.bak
*.sc.bak
```

- [x] **Step 5: Run the checks; they pass.** `make test`, then `make lint`. Expected: `1 passed`;
  `All checks passed!` and `files already formatted`.
- [x] **Step 6: Write CI and Dependabot.**

`.github/workflows/ci.yml`:

```yaml
# CI: the tests, lint, the model and privacy checks, the leak scan and the site, on every push to
# main or a phase branch and on every PR into main. Only main deploys the site to GitHub Pages.
# Every action is pinned to a commit SHA, its version in the comment; Dependabot keeps both current.
name: CI

on:
  push:
    branches: [main, "phase-*"]
  pull_request:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
      - uses: astral-sh/setup-uv@68559e99cc807c1eb7e9238fd43a15bba460eec2 # v10.3.3
      - run: uv sync --frozen
      - run: make test
      - run: make lint

  leaks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          fetch-depth: 0
          persist-credentials: false
      - name: Install gitleaks 8.30.1, checked against its published checksum
        run: |
          curl -sSfL -o gitleaks.tar.gz \
            https://github.com/gitleaks/gitleaks/releases/download/v8.30.1/gitleaks_8.30.1_linux_x64.tar.gz
          echo "551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb  gitleaks.tar.gz" |
            sha256sum --check --strict -
          tar -xzf gitleaks.tar.gz gitleaks
          sudo install -m 755 gitleaks /usr/local/bin/gitleaks
          rm gitleaks gitleaks.tar.gz
      - run: make leaks

```

`.github/dependabot.yml`:

```yaml
# Keep the pinned CI actions and the Python dependencies current: once a month, one PR for each.
version: 2
updates:
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: monthly
    groups:
      actions:
        patterns: ["*"]
  - package-ecosystem: uv
    directory: /
    schedule:
      interval: monthly
    groups:
      python:
        patterns: ["*"]
```

  Each action's SHA is the commit its version tag names, from
  `gh api repos/<owner>/<repo>/commits/<tag> --jq .sha`; recheck them if a tag is older than this
  plan. Check both files parse: `uv run --frozen python -c "import yaml; [yaml.safe_load(open(f))
  for f in ('.github/workflows/ci.yml', '.github/dependabot.yml')]"`. Expected: no output.
- [x] **Step 7: Run every check; they pass.** `make check`. Expected: the test twice, lint, then
  gitleaks' `no leaks found`.
- [x] **Step 8: Commit.** Write the message to `.git/COMMIT_MSG`:

```text
build(repo): 🤖 add the uv project, make test and lint, and CI

The repo had no test runner, linter or CI. This adds a uv project on
Python 3.12 (pytest, ruff, PyYAML, Pillow), sets make test, test-utc and
lint, adds placeholder targets for models, models-check, privacy and docs
that fail until their tasks, and makes make leaks scan merge commits' own
changes too. CI's tests job runs the suite and lint; its leaks job runs
gitleaks 8.30.1, checked against its published checksum, over every
commit. Every action is pinned to a commit SHA; Dependabot keeps them and
the lockfile current, one grouped PR a month each.

The new test failed first with: AssertionError: ['models',
'models-check', 'privacy'].

Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-1.md Task 1
Co-Authored-By: <the model's own line>
```

  `git add pyproject.toml .python-version uv.lock Makefile .gitignore tests/test_makefile.py .github/workflows/ci.yml .github/dependabot.yml`, then `git commit -F .git/COMMIT_MSG`, then `git log -1 --format='%(trailers)'` shows the `Plan:` line.
- [x] **Step 9: Review, look forward, close.**

  - **Review (Tier 1: Matt Pocock's `code-review`, two axes in two subagents, plus the security checklist, one line per item; at most one re-review),** from `$(cat .git/TASK_BASE)`.
  - **Forward:** Tasks 2 to 5 replace this task's placeholder targets; check their Consumes lines.
  - **Docs:** the README's command list stays true.
  - **Close,** its own commit: this task's boxes ticked, **Now** set to the next task, any
    Built differently and Ruling lines, deferred findings on the phase-end list, the spec's
    scenario statuses (`built`). The message, from `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 1: The Python toolchain and CI

    <what the task built, and why, in a few lines>

    Drift: <filled at the close, or none>
    Rulings: <filled at the close, or none>
    Phase-end: <filled at the close, or none>
    Forward: <filled at the close, or none>
    Tier: 1
    Rounds: <filled at the close>
    Findings: <filled at the close, or none>

    Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-1.md Task 1
    Co-Authored-By: <the model's own line>
    ```

  - **Push,** once Dan has OKed it, the request naming every binary file the push adds
    (`AGENTS.md`'s interim line): `make leaks privacy`, then `git push origin phase-1`.
    The task is closed once CI on the closing commit, or a later one, is green; until a
    push, the local checks are the gate.

***

### Task 2: `make models` and `make models-check`

**Tier:** 2 · **Scenarios:** S01, S02, S19

**Files:**
- Create: `scripts/models.py`, `tests/conftest.py`, `tests/test_models.py`
- Modify: `Makefile` (two recipes and the `check` line), `.github/workflows/ci.yml` (one step)

**Interfaces:**
- Consumes: Task 1's `make test`, `make lint` and the `tests` CI job.
- Produces, in `scripts/models.py`: `ROOT: Path`; `Model(folder: Path)` with `.slug -> str`,
  `.design -> Path` (`<slug>.sc`), `.built(kind: str) -> Path` (kind `"stl"`, `"png"` or
  `"eval.json"`), `.sized(size: str) -> Path` (`<slug>-<size_name>.stl`), `.record -> Path`
  (`build.json`); `size_name(size: str) -> str` (`"3/4 in"` → `"3-4in"`);
  `find_models(root: Path) -> list[Model]`; `sha256(path: Path) -> str`;
  `sizes(model: Model) -> dict[str, dict[str, str]]` (from `model.yml`'s `sizes`, raising
  `ValueError` when malformed); `outputs(model: Model) -> list[Path]`;
  `staleness(model: Model) -> str | None`; `main(argv: list[str] | None = None,
  root: Path = ROOT) -> int` with subcommands `build [SLUG ...]` and `check`. In
  `tests/conftest.py`: the fixtures `fake_cli` (returns the call log's path) and `repo` (an empty
  git repo with `models/`); `add_design(root, slug, text=...) -> Path`; and, for the model tests,
  `measured(model) -> dict`, `params(model) -> dict[str, float]`, `body(model, name) -> dict`.
  `SOLIDCRAFT_CLI` names the CLI.

- [x] **Step 0: Record the base:** `git rev-parse HEAD > .git/TASK_BASE`.
- [x] **Step 1: Write the fixtures and the failing tests.**

`tests/conftest.py`:

```python
"""Shared fixtures: scripts/ on the import path, and a fake solidcraft-cli."""

from __future__ import annotations

import json
import os
import stat
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

FAKE_CLI = """\
import json, sys
from pathlib import Path

args = sys.argv[1:]
with open(LOG, "a", encoding="utf-8") as log:
    log.write(" ".join(args) + "\\n")
if args == ["--version"]:
    print("solidcraft-cli 0.30.1")
    sys.exit(0)
design = Path(args[args.index("--in") + 1])
if b"fail" in design.read_bytes():
    print("a timeline feature failed", file=sys.stderr)
    sys.exit(1)
if args[0] in ("run", "snapshot"):
    Path(args[args.index("--out") + 1]).write_bytes(b"built from " + design.read_bytes())
elif args[0] == "eval":
    Path(args[args.index("--json-out") + 1]).write_text(json.dumps({"bodies": [], "params": []}))
"""


@pytest.fixture
def fake_cli(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point SOLIDCRAFT_CLI at a fake that writes its outputs and logs each call."""
    log = tmp_path / "cli.log"
    script = tmp_path / "fake-solidcraft-cli"
    script.write_text(f"#!{sys.executable}\nLOG = {str(log)!r}\n{FAKE_CLI}", encoding="utf-8")
    script.chmod(script.stat().st_mode | stat.S_IXUSR)
    monkeypatch.setenv("SOLIDCRAFT_CLI", os.fspath(script))
    return log


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """An empty git repo with a models/ folder."""
    root = tmp_path / "repo"
    (root / "models").mkdir(parents=True)
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    return root


def add_design(root: Path, slug: str, text: str = '{"format": "solidcraft/48"}') -> Path:
    folder = root / "models" / slug
    folder.mkdir(parents=True, exist_ok=True)
    design = folder / f"{slug}.sc"
    design.write_text(text, encoding="utf-8")
    return design


def measured(model) -> dict:
    """A model's measurements: solidcraft-cli eval's JSON, as make models wrote it."""
    return json.loads(model.built("eval.json").read_text(encoding="utf-8"))


def params(model) -> dict[str, float]:
    """A model's parameters by name, each one's value in millimetres."""
    return {p["name"]: p["value"] for p in measured(model)["params"]}


def body(model, name: str) -> dict:
    """One body of a model, by its name in the design."""
    return next(b for b in measured(model)["bodies"] if b["name"] == name)
```

`tests/test_models.py`:

```python
"""scripts/models.py: build only what changed (S01); fail on a stale build (S02); sizes (S19)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import models
from conftest import add_design

SIZES = "sizes:\n  3/4 in: {dowel_d: 19.05 mm}\n  25 mm: {dowel_d: 25 mm}\n"


def calls(log: Path) -> list[str]:
    return log.read_text(encoding="utf-8").splitlines() if log.exists() else []


def test_build_writes_each_built_file_and_records_its_hash(repo: Path, fake_cli: Path) -> None:
    design = add_design(repo, "coupon")
    assert models.main(["build"], root=repo) == 0
    folder = design.parent
    record = json.loads((folder / "build.json").read_text(encoding="utf-8"))
    assert record["design"] == "coupon.sc"
    assert record["sha256"] == models.sha256(design)
    assert record["sizes"] == {}
    assert record["solidcraft_cli"] == "solidcraft-cli 0.30.1"
    for name in ("coupon.stl", "coupon.png", "coupon.eval.json"):
        assert record["built"][name] == models.sha256(folder / name), name


def test_build_writes_an_stl_for_each_size_model_yml_lists(repo: Path, fake_cli: Path) -> None:
    design = add_design(repo, "clamp")
    (design.parent / "model.yml").write_text(SIZES, encoding="utf-8")
    assert models.main(["build"], root=repo) == 0
    for name in ("clamp-3-4in.stl", "clamp-25mm.stl"):
        assert (design.parent / name).is_file(), name
    sized = [line for line in calls(fake_cli) if line.startswith("run ") and "size.json" in line]
    assert len(sized) == 2
    record = json.loads((design.parent / "build.json").read_text(encoding="utf-8"))
    assert record["sizes"] == {"3/4 in": {"dowel_d": "19.05 mm"}, "25 mm": {"dowel_d": "25 mm"}}


def test_build_leaves_an_up_to_date_model_alone(repo: Path, fake_cli: Path) -> None:
    add_design(repo, "coupon")
    models.main(["build"], root=repo)
    before = len(calls(fake_cli))
    assert models.main(["build"], root=repo) == 0
    assert len(calls(fake_cli)) == before


def test_build_rebuilds_only_the_changed_design(repo: Path, fake_cli: Path) -> None:
    add_design(repo, "coupon")
    other = add_design(repo, "hook")
    models.main(["build"], root=repo)
    other.write_text('{"format": "solidcraft/48", "changed": true}', encoding="utf-8")
    fake_cli.unlink()
    assert models.main(["build"], root=repo) == 0
    rebuilt = {line.split("--in ")[1].split()[0] for line in calls(fake_cli) if "--in" in line}
    assert rebuilt == {str(other)}


def test_build_refuses_an_unknown_slug(repo: Path, fake_cli: Path, capsys) -> None:
    add_design(repo, "coupon")
    assert models.main(["build", "nope"], root=repo) == 2
    assert "no such model: nope" in capsys.readouterr().err


def test_a_failing_build_leaves_no_record_vouching_for_it(
    repo: Path, fake_cli: Path, capsys
) -> None:
    design = add_design(repo, "broken")
    models.main(["build"], root=repo)
    design.write_text('{"fail": true}', encoding="utf-8")
    assert models.main(["build"], root=repo) == 1
    assert "a timeline feature failed" in capsys.readouterr().err
    assert not (repo / "models" / "broken" / "build.json").exists()


def test_build_and_check_take_a_design_saved_as_a_zip(repo: Path, fake_cli: Path) -> None:
    design = add_design(repo, "hook")
    design.write_bytes(b"PK\x03\x04 a zip container, as the app saves by default")
    assert models.main(["build"], root=repo) == 0
    assert models.main(["check"], root=repo) == 0


def test_check_passes_when_every_build_matches(repo: Path, fake_cli: Path, capsys) -> None:
    add_design(repo, "coupon")
    models.main(["build"], root=repo)
    assert models.main(["check"], root=repo) == 0
    assert "1 models, every build matches its design" in capsys.readouterr().out


def test_check_names_a_design_that_changed(repo: Path, fake_cli: Path, capsys) -> None:
    design = add_design(repo, "coupon")
    models.main(["build"], root=repo)
    design.write_text('{"format": "solidcraft/48", "edited": true}', encoding="utf-8")
    assert models.main(["check"], root=repo) == 1
    err = capsys.readouterr().err
    assert "stale: models/coupon: coupon.sc changed since its last build" in err


def test_check_names_a_built_file_that_is_not_the_one_recorded(
    repo: Path, fake_cli: Path, capsys
) -> None:
    design = add_design(repo, "coupon")
    models.main(["build"], root=repo)
    (design.parent / "coupon.stl").write_bytes(b"an older export")
    assert models.main(["check"], root=repo) == 1
    assert "coupon.stl changed since build.json recorded it" in capsys.readouterr().err


def test_check_names_sizes_that_changed(repo: Path, fake_cli: Path, capsys) -> None:
    design = add_design(repo, "clamp")
    (design.parent / "model.yml").write_text(SIZES, encoding="utf-8")
    models.main(["build"], root=repo)
    (design.parent / "model.yml").write_text(SIZES.replace("25 mm}", "24 mm}"), encoding="utf-8")
    assert models.main(["check"], root=repo) == 1
    assert "model.yml's sizes changed since its last build" in capsys.readouterr().err


@pytest.mark.parametrize("missing", ["coupon.stl", "coupon.png", "coupon.eval.json", "build.json"])
def test_check_names_a_missing_built_file(repo: Path, fake_cli: Path, capsys, missing: str) -> None:
    add_design(repo, "coupon")
    models.main(["build"], root=repo)
    (repo / "models" / "coupon" / missing).unlink()
    assert models.main(["check"], root=repo) == 1
    assert f"stale: models/coupon: missing {missing}" in capsys.readouterr().err


@pytest.mark.parametrize("slug", ["Wall Hook", "wall_hook", "WallHook", "-hook"])
def test_check_names_a_folder_that_cannot_be_a_url(repo: Path, capsys, slug: str) -> None:
    add_design(repo, slug)
    assert models.main(["check"], root=repo) == 1
    assert f"stale: models/{slug}: its folder name must be lowercase words joined by hyphens" in (
        capsys.readouterr().err
    )


@pytest.mark.parametrize("name", ["Hook.sc", "hook-v2.sc"])
def test_check_names_a_design_not_named_after_its_folder(repo: Path, capsys, name: str) -> None:
    folder = repo / "models" / "hook"
    folder.mkdir()
    (folder / name).write_text("{}", encoding="utf-8")
    assert models.main(["check"], root=repo) == 1
    assert f"stale: models/hook: the design must be hook.sc alone, not {name}" in (
        capsys.readouterr().err
    )


def test_check_names_unreadable_sizes(repo: Path, capsys) -> None:
    design = add_design(repo, "clamp")
    (design.parent / "model.yml").write_text("sizes: [3/4 in]\n", encoding="utf-8")
    assert models.main(["check"], root=repo) == 1
    assert "'sizes' must map each size to parameter changes" in capsys.readouterr().err


def test_check_ignores_a_folder_without_a_design(repo: Path, capsys) -> None:
    (repo / "models" / "notes").mkdir()
    assert models.main(["check"], root=repo) == 0
    assert "0 models" in capsys.readouterr().out
```

- [x] **Step 2: Run them; watch them fail.** `make test`. Expected: a collection error,
  `ModuleNotFoundError: No module named 'models'`.
- [x] **Step 3: Write the builder.**

`scripts/models.py`:

```python
"""Build and check the models under models/.

    uv run scripts/models.py build [SLUG ...]
        rebuild each model whose design, sizes or built files changed since its build.json
        (needs solidcraft-cli)
    uv run scripts/models.py check
        fail, naming each model, when a build is missing or stale, or a design is misnamed

A model is a folder models/<slug>/ holding the design <slug>.sc. A build writes, beside it:
<slug>.stl, <slug>.png, <slug>.eval.json (solidcraft-cli eval's measurements), one STL per extra
size its model.yml lists (<slug>-<size>.stl), and build.json, which records the design's sha256,
the sizes, the CLI's version and every built file's sha256. Exporting the same design twice gives
a byte-different STL, so freshness is judged by those hashes, never by rebuilding.

SOLIDCRAFT_CLI names the CLI to run (default: solidcraft-cli); the tests point it at a fake.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SLUG = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")
PICTURE = ("--view", "iso", "--width", "1200", "--height", "900", "--no-grid", "--no-axes")


@dataclass(frozen=True)
class Model:
    folder: Path

    @property
    def slug(self) -> str:
        return self.folder.name

    @property
    def design(self) -> Path:
        return self.folder / f"{self.slug}.sc"

    def built(self, kind: str) -> Path:
        return self.folder / f"{self.slug}.{kind}"

    def sized(self, size: str) -> Path:
        return self.folder / f"{self.slug}-{size_name(size)}.stl"

    @property
    def record(self) -> Path:
        return self.folder / "build.json"


def size_name(size: str) -> str:
    """'3/4 in' -> '3-4in', '25 mm' -> '25mm': the part of a file name a size gives."""
    return re.sub(r"[^a-z0-9-]", "", size.lower().replace("/", "-").replace(" ", ""))


def find_models(root: Path) -> list[Model]:
    models_dir = root / "models"
    if not models_dir.is_dir():
        return []
    return [
        Model(folder)
        for folder in sorted(models_dir.iterdir())
        if folder.is_dir() and any(p.suffix.lower() == ".sc" for p in folder.iterdir())
    ]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sizes(model: Model) -> dict[str, dict[str, str]]:
    """The extra sizes model.yml lists: {'3/4 in': {'dowel_d': '19.05 mm'}, ...}."""
    path = model.folder / "model.yml"
    if not path.is_file():
        return {}
    meta = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    listed = meta.get("sizes") or {}
    if not isinstance(listed, dict) or not all(
        isinstance(changes, dict) and all(isinstance(v, str) for v in changes.values())
        for changes in listed.values()
    ):
        raise ValueError(
            f"models/{model.slug}/model.yml: 'sizes' must map each size to parameter changes, "
            "such as '3/4 in': {dowel_d: 19.05 mm}"
        )
    return {str(size): changes for size, changes in listed.items()}


def outputs(model: Model) -> list[Path]:
    return [model.built(k) for k in ("stl", "png", "eval.json")] + [
        model.sized(size) for size in sizes(model)
    ]


def staleness(model: Model) -> str | None:
    """Why the model needs a build, or None when its built files match its design."""
    if not SLUG.fullmatch(model.slug):
        return "its folder name must be lowercase words joined by hyphens, as the page's URL"
    designs = sorted(p.name for p in model.folder.iterdir() if p.suffix.lower() == ".sc")
    if designs != [model.design.name]:
        return f"the design must be {model.design.name} alone, not {', '.join(designs)}"
    try:
        wanted = outputs(model)
    except ValueError as error:
        return str(error)
    missing = [path.name for path in wanted if not path.is_file()]
    if not model.record.is_file():
        missing.append(model.record.name)
    if missing:
        return "missing " + ", ".join(missing)
    try:
        record = json.loads(model.record.read_text(encoding="utf-8"))
        recorded_design, recorded_sizes, built = record["sha256"], record["sizes"], record["built"]
    except (json.JSONDecodeError, KeyError, TypeError):
        return "build.json is unreadable"
    if recorded_design != sha256(model.design):
        return f"{model.design.name} changed since its last build"
    if recorded_sizes != sizes(model):
        return "model.yml's sizes changed since its last build"
    changed = [p.name for p in wanted if built.get(p.name) != sha256(p)]
    if changed:
        return f"{', '.join(changed)} changed since build.json recorded it"
    return None


def cli() -> str:
    return os.environ.get("SOLIDCRAFT_CLI", "solidcraft-cli")


def run(*args: str) -> str:
    result = subprocess.run([cli(), *args], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"{cli()} {' '.join(args)} failed:\n{result.stderr.strip()}")
    return result.stdout


def build(model: Model) -> None:
    model.record.unlink(missing_ok=True)  # a build that fails halfway leaves no record vouching
    design_hash = sha256(model.design)  # hashed first: an edit saved mid-build shows as stale
    wanted_sizes = sizes(model)
    design = str(model.design)
    run("run", "--in", design, "--out", str(model.built("stl")), "--quiet")
    run("snapshot", "--in", design, "--out", str(model.built("png")), *PICTURE)
    run("eval", "--in", design, "--json-out", str(model.built("eval.json")))
    for size, changes in wanted_sizes.items():
        script = {
            "commands": [
                {"command": "parameters.change", "params": {"name": name, "expression": value}}
                for name, value in changes.items()
            ]
        }
        with tempfile.TemporaryDirectory() as scratch:
            path = Path(scratch) / "size.json"
            path.write_text(json.dumps(script), encoding="utf-8")
            run("run", str(path), "--in", design, "--out", str(model.sized(size)), "--quiet")
    record = {
        "design": model.design.name,
        "sha256": design_hash,
        "sizes": wanted_sizes,
        "solidcraft_cli": run("--version").strip(),
        "built": {path.name: sha256(path) for path in outputs(model)},
    }
    model.record.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")


def command_build(root: Path, slugs: list[str]) -> int:
    models = find_models(root)
    unknown = sorted(set(slugs) - {m.slug for m in models})
    if unknown:
        print(f"models: no such model: {', '.join(unknown)}", file=sys.stderr)
        return 2
    chosen = [m for m in models if not slugs or m.slug in slugs]
    built = 0
    for model in chosen:
        reason = staleness(model)
        if reason is None:
            continue
        print(f"building models/{model.slug} ({reason})")
        try:
            build(model)
        except (OSError, RuntimeError, ValueError) as error:
            print(f"models: {error}", file=sys.stderr)
            return 1
        built += 1
    print(f"{built} built, {len(chosen) - built} up to date")
    return 0


def command_check(root: Path) -> int:
    models = find_models(root)
    stale = [(m, reason) for m in models if (reason := staleness(m)) is not None]
    for model, reason in stale:
        print(f"stale: models/{model.slug}: {reason}; run make models", file=sys.stderr)
    if stale:
        return 1
    print(f"{len(models)} models, every build matches its design")
    return 0


def main(argv: list[str] | None = None, root: Path = ROOT) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    build_parser = sub.add_parser("build", help="rebuild each changed model")
    build_parser.add_argument("slugs", nargs="*", metavar="SLUG")
    sub.add_parser("check", help="fail when a model's build is missing or stale")
    args = parser.parse_args(argv)
    if args.command == "build":
        return command_build(root, args.slugs)
    return command_check(root)


if __name__ == "__main__":
    sys.exit(main())
```

  In the `Makefile`, replace the two placeholder recipes, and add `models-check` to `check`:

```makefile
models: ## Rebuild each changed design's STLs, picture and measurements (needs SolidCraft)
	uv run --frozen scripts/models.py build

models-check: ## Fail when a design has no build, a stale one, or the wrong name
	uv run --frozen scripts/models.py check
```

```makefile
check: test test-utc lint models-check leaks ## Everything CI runs, and the suite under UTC
```

  In `.github/workflows/ci.yml`'s `tests` job, after `- run: make lint`, add
  `      - run: make models-check`.
- [x] **Step 4: Run the checks; they pass.** `make check`. Expected: every test passes twice,
  lint clean, `0 models, every build matches its design`, `no leaks found`.
- [x] **Step 5: Commit.** Write the message to `.git/COMMIT_MSG`:

```text
feat(models): 🤖 build changed designs and fail on a stale build

make models had nothing behind it. scripts/models.py build runs
solidcraft-cli for each model whose design, sizes or built files differ
from its build.json, writing the STL, an STL per size its model.yml lists,
the picture and the measurements beside it, and a record of every file's
SHA-256. check fails, naming each model, when a build is missing or stale,
a built file isn't the one recorded, the folder's name can't be a URL, or
the design isn't named after its folder. Freshness is by hashes because
the CLI exports a byte-different STL each run. A failing build leaves no
record. The tests run a fake CLI, named by SOLIDCRAFT_CLI.

The new tests failed first with: ModuleNotFoundError: No module named
'models'.

Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-1.md Task 2
Co-Authored-By: <the model's own line>
```

  `git add scripts/models.py tests/conftest.py tests/test_models.py Makefile .github/workflows/ci.yml`, then `git commit -F .git/COMMIT_MSG`, then `git log -1 --format='%(trailers)'` shows the `Plan:` line.
- [x] **Step 6: Review, look forward, close.**

  - **Review (Tier 2: Matt Pocock's `code-review`, two axes in two subagents; fix Critical and Important; at most one re-review),** from `$(cat .git/TASK_BASE)`.
  - **Forward:** Tasks 5 to 8 consume `find_models`, `Model`, `sizes` and the conftest helpers.
  - **Docs:** the Architecture page doesn't exist yet (Task 4 draws this as built).
  - **Close,** its own commit: this task's boxes ticked, **Now** set to the next task, any
    Built differently and Ruling lines, deferred findings on the phase-end list, the spec's
    scenario statuses (`built`). The message, from `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 2: make models and make models-check

    <what the task built, and why, in a few lines>

    Drift: <filled at the close, or none>
    Rulings: <filled at the close, or none>
    Phase-end: <filled at the close, or none>
    Forward: <filled at the close, or none>
    Tier: 2
    Rounds: <filled at the close>
    Findings: <filled at the close, or none>

    Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-1.md Task 2
    Co-Authored-By: <the model's own line>
    ```

  - **Push,** once Dan has OKed it, the request naming every binary file the push adds
    (`AGENTS.md`'s interim line): `make leaks privacy`, then `git push origin phase-1`.
    The task is closed once CI on the closing commit, or a later one, is green; until a
    push, the local checks are the gate.

***

### Task 3: The privacy guard, `make privacy`

> **Built differently** (closed 2026-11-05; commits caddfe1, e837178): `strip` keeps a PNG's
> transparency (the listing cleared it with the rest of the image's info, so a transparent PNG
> came back opaque), checks every file's format before rewriting any, prints only file names,
> and keeps the file's mode; the check names a huge or malformed image instead of raising. Found
> by the task's Standards review. The listing stays as planned.


**Tier:** 1 (if wrong, a photo shows where Dan lives, or a path names his machine) ·
**Scenarios:** S03, S21

**Files:**
- Create: `scripts/privacy.py`, `tests/test_privacy.py`
- Modify: `Makefile` (one recipe and the `check` line), `.github/workflows/ci.yml` (one step)

**Interfaces:**
- Consumes: Task 2's `repo` fixture (a git repo).
- Produces, in `scripts/privacy.py`: `committable(root: Path) -> list[Path]` (what git would
  commit), `image_problem(path: Path) -> str | None`, `path_problem(path: Path) -> str | None`,
  `problems(root: Path) -> list[tuple[Path, str]]`, `strip(path: Path) -> None`,
  `main(argv: list[str] | None = None, root: Path = ROOT) -> int` with subcommands `check` and
  `strip FILE ...`.

- [x] **Step 0: Record the base:** `git rev-parse HEAD > .git/TASK_BASE`.
- [x] **Step 1: Write the failing tests.**

`tests/test_privacy.py`:

```python
"""scripts/privacy.py: nothing that shows where Dan lives, or whose machine this is, gets in
(S03, S21)."""

from __future__ import annotations

from pathlib import Path

import pytest
from PIL import ExifTags, Image, PngImagePlugin

import privacy

HOME = "/" + "Users" + "/someone/"  # joined at runtime, so this file holds no home path itself
XMP = (
    b'<x:xmpmeta xmlns:x="adobe:ns:meta/"><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-'
    b'syntax-ns#"><rdf:Description xmlns:exif="http://ns.adobe.com/exif/1.0/" '
    b'exif:GPSLatitude="0,0.0N" exif:GPSLongitude="0,0.0E"/></rdf:RDF></x:xmpmeta>'
)


def photo(path: Path, *, gps: bool = False, orientation: int | None = None, **save) -> Path:
    """A 40x20 image, optionally with a GPS block, an EXIF orientation or other save options."""
    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (40, 20), (200, 180, 150))
    exif = image.getexif()
    if gps:
        block = exif.get_ifd(ExifTags.IFD.GPSInfo)
        block[ExifTags.GPS.GPSLatitudeRef] = "N"
        block[ExifTags.GPS.GPSLatitude] = (0.0, 0.0, 0.0)
    if orientation:
        exif[ExifTags.Base.Orientation] = orientation
    if len(exif) or gps:
        save["exif"] = exif.tobytes()  # an Exif object holding only a GPS block is dropped
    image.save(path, **save)
    return path


def check(repo: Path, capsys) -> tuple[int, str]:
    code = privacy.main(["check"], root=repo)
    return code, capsys.readouterr().err


@pytest.mark.parametrize("name", ["print.jpg", "print.png", "print.webp"])
def test_check_passes_an_image_with_no_metadata(repo: Path, capsys, name: str) -> None:
    photo(repo / "models" / "coupon" / "photos" / name)
    assert check(repo, capsys) == (0, "")


@pytest.mark.parametrize("name", ["print.jpg", "PRINT.JPG", "print.png", "print.webp"])
def test_check_names_a_photo_with_a_gps_block(repo: Path, capsys, name: str) -> None:
    photo(repo / "models" / "coupon" / "photos" / name, gps=True)
    code, err = check(repo, capsys)
    assert code == 1
    assert f"privacy: models/coupon/photos/{name}: EXIF metadata" in err


def test_check_names_a_camera_serial_without_any_gps(repo: Path, capsys) -> None:
    image = Image.new("RGB", (40, 20))
    exif = image.getexif()
    exif[ExifTags.Base.BodySerialNumber] = "12345"
    exif[ExifTags.Base.CameraOwnerName] = "someone"
    image.save(repo / "print.jpg", exif=exif)
    assert check(repo, capsys) == (1, "privacy: print.jpg: EXIF metadata\n")


@pytest.mark.parametrize(
    ("name", "save"),
    [
        ("xmp.jpg", {"xmp": XMP}),
        ("comment.jpg", {"comment": b"taken at home"}),
        ("xmp.webp", {"xmp": XMP}),
    ],
)
def test_check_names_xmp_and_comments(repo: Path, capsys, name: str, save: dict) -> None:
    photo(repo / name, **save)
    code, err = check(repo, capsys)
    assert code == 1
    assert f"privacy: {name}: metadata" in err


def test_check_names_xmp_hidden_in_a_compressed_png_chunk(repo: Path, capsys) -> None:
    info = PngImagePlugin.PngInfo()
    info.add_itxt("XML:com.adobe.xmp", XMP.decode(), zip=True)
    photo(repo / "print.png", pnginfo=info)
    code, err = check(repo, capsys)
    assert code == 1
    assert "privacy: print.png: metadata: XML:com.adobe.xmp" in err


def test_check_names_a_second_frame(repo: Path, capsys) -> None:
    frames = [Image.new("RGB", (40, 20), colour) for colour in ("red", "blue")]
    frames[0].save(repo / "turn.webp", save_all=True, append_images=frames[1:])
    assert check(repo, capsys) == (1, "privacy: turn.webp: more than one frame\n")


@pytest.mark.parametrize("name", ["IMG_0001.HEIC", "shot.heif", "clip.mov", "scan.dng", "a.gif"])
def test_check_refuses_a_format_it_cannot_read_inside(repo: Path, capsys, name: str) -> None:
    (repo / "models" / name).write_bytes(b"\x00\x00\x00\x18ftypheic")
    code, err = check(repo, capsys)
    assert code == 1
    assert f"privacy: models/{name}: a {Path(name).suffix.lower()} file" in err


def test_check_names_the_line_of_a_home_folder_path_without_printing_it(repo: Path, capsys) -> None:
    (repo / "notes.md").write_text(f"first\nsaved in {HOME}git/x\n", encoding="utf-8")
    code, err = check(repo, capsys)
    assert code == 1
    assert "privacy: notes.md: a home-folder path on line 2" in err
    assert "someone" not in err


def test_check_finds_a_home_folder_path_inside_a_binary(repo: Path, capsys) -> None:
    (repo / "part.stl").write_bytes(b"\x80\x81 exported from " + HOME.encode() + b"\xff")
    assert check(repo, capsys) == (1, "privacy: part.stl: a home-folder path inside it\n")


def test_check_skips_what_git_ignores(repo: Path, capsys) -> None:
    (repo / ".gitignore").write_text("website/_site/\n.venv/\n", encoding="utf-8")
    photo(repo / "website" / "_site" / "shot.jpg", gps=True)
    (repo / ".venv").mkdir()
    (repo / ".venv" / "paths.txt").write_text(HOME, encoding="utf-8")
    assert check(repo, capsys) == (0, "")


@pytest.mark.parametrize("name", ["print.jpg", "print.png", "print.webp"])
def test_strip_leaves_no_metadata(repo: Path, capsys, name: str) -> None:
    path = photo(repo / name, gps=True, **({"xmp": XMP} if name != "print.png" else {}))
    assert privacy.main(["strip", str(path)], root=repo) == 0
    assert privacy.image_problem(path) is None
    with Image.open(path) as image:
        assert image.size == (40, 20)


def test_strip_drops_a_jpeg_comment(repo: Path) -> None:
    path = photo(repo / "print.jpg", comment=b"taken at home")
    privacy.main(["strip", str(path)], root=repo)
    assert privacy.image_problem(path) is None


def test_strip_turns_the_photo_upright_before_dropping_its_orientation(repo: Path) -> None:
    path = photo(repo / "sideways.jpg", orientation=6)
    privacy.main(["strip", str(path)], root=repo)
    with Image.open(path) as image:
        assert image.size == (20, 40)
        assert not len(image.getexif())


def test_strip_keeps_the_colour_profile(repo: Path) -> None:
    icc = b"\x00" * 128  # Pillow keeps the bytes as given; a real profile would be parsed
    path = photo(repo / "print.png", icc_profile=icc)
    privacy.main(["strip", str(path)], root=repo)
    with Image.open(path) as image:
        assert image.info.get("icc_profile") == icc


def test_strip_refuses_a_heic(repo: Path, capsys) -> None:
    path = repo / "IMG_0001.heic"
    path.write_bytes(b"\x00")
    assert privacy.main(["strip", str(path)], root=repo) == 2
    assert "strip takes JPEG, PNG or WebP only" in capsys.readouterr().err
```

- [x] **Step 2: Run them; watch them fail.** `make test`. Expected: a collection error,
  `ModuleNotFoundError: No module named 'privacy'`.
- [x] **Step 3: Write the guard.**

`scripts/privacy.py`:

```python
"""Keep where Dan lives, and whose machine built this, out of a public repo.

    uv run scripts/privacy.py check
        fail, naming each file, when a file git would commit is an image carrying any metadata
        but a colour profile, is a photo or video format this check can't read inside, or holds
        a home-folder path (/Users/<name>/ or /home/<name>/)
    uv run scripts/privacy.py strip FILE ...
        rewrite each JPEG, PNG or WebP upright, with no metadata but its colour profile

A photo's location hides in EXIF's GPS block, in XMP text (plain or compressed), in IPTC and in
PNG text chunks; a camera's serial number and its owner's name hide beside it. Rather than hunt
for each, the check allows nothing but a colour profile and the format's own housekeeping, and
refuses the formats it can't read inside (HEIC, AVIF, RAW, video). What a photo shows (a window's
view, a street, a face) no check can see: Dan looks at each before it's staged.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
READABLE = {".jpg", ".jpeg", ".png", ".webp"}
UNREADABLE = {
    ".heic", ".heif", ".avif", ".jxl", ".gif", ".tif", ".tiff", ".bmp", ".jfif", ".mpo",
    ".dng", ".raw", ".cr2", ".cr3", ".nef", ".arw", ".orf", ".rw2",
    ".mov", ".mp4", ".m4v", ".3gp",
}  # fmt: skip
HOUSEKEEPING = {
    "icc_profile", "dpi", "jfif", "jfif_version", "jfif_unit", "jfif_density", "adobe",
    "adobe_transform", "progressive", "progression", "gamma", "srgb", "chromaticity",
    "transparency", "aspect", "interlace", "loop", "background", "timestamp", "duration",
}  # fmt: skip
JPEG_HOUSEKEEPING = {"APP0", "APP2", "APP14"}  # JFIF, the colour profile, Adobe's colour flag
HOME = re.compile(rb"/(?:Users|home)/[^/\s\"'<>()]+/")


def committable(root: Path) -> list[Path]:
    """Every file git would commit: tracked, or untracked and not ignored."""
    listed = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=root, capture_output=True, check=True,
    ).stdout.decode("utf-8").split("\0")  # fmt: skip
    return sorted({root / name for name in listed if name and (root / name).is_file()})


def image_problem(path: Path) -> str | None:
    """Why this image can't be committed, or None when it carries nothing but a colour profile."""
    suffix = path.suffix.lower()
    if suffix in UNREADABLE:
        return f"a {suffix} file, which this check can't read inside; convert it to JPEG first"
    try:
        with Image.open(path) as image:
            image.load()
            if getattr(image, "n_frames", 1) > 1:
                return "more than one frame"
            if len(image.getexif()):
                return "EXIF metadata"
            extra = sorted(set(image.info) - HOUSEKEEPING)
            markers = {marker for marker, _ in getattr(image, "applist", [])}
    except OSError as error:
        return f"unreadable as an image ({error})"
    if extra:
        return f"metadata: {', '.join(extra)}"
    if markers - JPEG_HOUSEKEEPING:
        return f"metadata segments: {', '.join(sorted(markers - JPEG_HOUSEKEEPING))}"
    return None


def path_problem(path: Path) -> str | None:
    """Where this file holds a home-folder path, or None. The path itself is never printed."""
    data = path.read_bytes()
    if not HOME.search(data):
        return None
    try:
        lines = data.decode("utf-8").splitlines()
    except UnicodeDecodeError:
        return "a home-folder path inside it"
    numbers = [str(n) for n, line in enumerate(lines, 1) if HOME.search(line.encode("utf-8"))]
    return f"a home-folder path on line {', '.join(numbers)}"


def problems(root: Path) -> list[tuple[Path, str]]:
    found = []
    for path in committable(root):
        if path.suffix.lower() in READABLE | UNREADABLE:
            reason = image_problem(path)
            if reason:
                found.append((path, reason))
        reason = path_problem(path)
        if reason:
            found.append((path, reason))
    return found


def strip(path: Path) -> None:
    with Image.open(path) as opened:
        image_format = opened.format
        icc = opened.info.get("icc_profile")
        image = ImageOps.exif_transpose(opened)
        image.load()
    image.info = {}  # Pillow writes a JPEG's comment, and EXIF or XMP, from info unless cleared
    options = {"icc_profile": icc} if icc else {}
    if image_format == "JPEG":
        options |= {"quality": 95, "subsampling": 0}
    handle, temp = tempfile.mkstemp(dir=path.parent, suffix=path.suffix)
    os.close(handle)
    try:
        image.save(temp, format=image_format, **options)
        os.replace(temp, path)
    finally:
        Path(temp).unlink(missing_ok=True)


def command_check(root: Path) -> int:
    found = problems(root)
    for path, reason in found:
        print(f"privacy: {path.relative_to(root)}: {reason}", file=sys.stderr)
    if found:
        return 1
    print("privacy: no image metadata, unreadable photo format or home-folder path")
    return 0


def command_strip(files: list[Path]) -> int:
    for path in files:
        if path.suffix.lower() not in READABLE:
            print(f"privacy: {path}: strip takes JPEG, PNG or WebP only", file=sys.stderr)
            return 2
        strip(path)
        print(f"stripped {path}")
    return 0


def main(argv: list[str] | None = None, root: Path = ROOT) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check", help="fail on image metadata, an unreadable format or a home path")
    strip_parser = sub.add_parser("strip", help="rewrite images without their metadata")
    strip_parser.add_argument("files", nargs="+", type=Path, metavar="FILE")
    args = parser.parse_args(argv)
    if args.command == "strip":
        return command_strip(args.files)
    return command_check(root)


if __name__ == "__main__":
    sys.exit(main())
```

  In the `Makefile`, replace the placeholder recipe, and add `privacy` to `check`:

```makefile
privacy: ## Fail on image metadata, a photo format the check can't read, or a home-folder path
	uv run --frozen scripts/privacy.py check
```

```makefile
check: test test-utc lint models-check privacy leaks ## Everything CI runs, and the suite under UTC
```

  In `.github/workflows/ci.yml`'s `tests` job, after `- run: make models-check`, add
  `      - run: make privacy`.
- [x] **Step 4: Run the checks; they pass.** `make check`. Expected: every test passes twice,
  `privacy: no image metadata, unreadable photo format or home-folder path`, `no leaks found`.
- [x] **Step 5: Commit.** Write the message to `.git/COMMIT_MSG`:

```text
feat(privacy): 🤖 refuse image metadata and home-folder paths

Dan's rule for this public repo is that no photo carries its location.
Hunting for GPS alone misses XMP in a compressed PNG chunk, a camera's
serial number and its owner's name, so scripts/privacy.py check allows an
image nothing but a colour profile and its format's housekeeping, refuses
the formats it can't read inside (HEIC, AVIF, RAW, video, GIF), and fails
on a home-folder path in any file git would commit, naming the line but
never printing the path. strip rewrites a JPEG, PNG or WebP upright with
no metadata but its colour profile, through a temporary file. make privacy
runs the check, and so do make check and CI; every push waits for it.

The new tests failed first with: ModuleNotFoundError: No module named
'privacy'.

Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-1.md Task 3
Co-Authored-By: <the model's own line>
```

  `git add scripts/privacy.py tests/test_privacy.py Makefile .github/workflows/ci.yml`, then `git commit -F .git/COMMIT_MSG`, then `git log -1 --format='%(trailers)'` shows the `Plan:` line.
- [x] **Step 6: Review, look forward, close.**

  - **Review (Tier 1: Matt Pocock's `code-review`, two axes in two subagents, plus the security checklist, one line per item; at most one re-review),** from `$(cat .git/TASK_BASE)`.
  - **Forward:** Tasks 6 to 8 commit SolidCraft's first real outputs, which this check scans; Phase 2's photo steps run `privacy.py strip`.
  - **Docs:** `AGENTS.md`'s docs table and the README name `privacy.py strip`; check they still do.
  - **Close,** its own commit: this task's boxes ticked, **Now** set to the next task, any
    Built differently and Ruling lines, deferred findings on the phase-end list, the spec's
    scenario statuses (`built`). The message, from `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 3: The privacy guard, make privacy

    <what the task built, and why, in a few lines>

    Drift: <filled at the close, or none>
    Rulings: <filled at the close, or none>
    Phase-end: <filled at the close, or none>
    Forward: <filled at the close, or none>
    Tier: 1
    Rounds: <filled at the close>
    Findings: <filled at the close, or none>

    Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-1.md Task 3
    Co-Authored-By: <the model's own line>
    ```

  - **Push,** once Dan has OKed it, the request naming every binary file the push adds
    (`AGENTS.md`'s interim line): `make leaks privacy`, then `git push origin phase-1`.
    The task is closed once CI on the closing commit, or a later one, is green; until a
    push, the local checks are the gate.

***

### Task 4: The docs site

> **Built differently** (closed 2026-11-05; commits 21822a8, 218d074, 26c4f5f): CI's lychee step
> extracts `lychee-x86_64-unknown-linux-gnu/lychee`, the path the release tarball really uses (the
> listing's `lychee` failed CI's first run; escaped from this task, fixed under Task 6's reopen). One
> file more,
> `website/.gitignore`, which Quarto's render writes (its own `/.quarto/` and `**/*.quarto_ipynb`
> lines) whenever it's missing; committed, as Quarto's practice, so checkouts stay clean. The
> listing stays as planned.


**Tier:** 1 (the `pages` job holds the only write permissions in CI) · **Scenarios:** S05, S06,
S10

**Files:**
- Create: `scripts/sitedocs.py`, `tests/test_site.py`, `website/_quarto.yml`,
  `website/styles.css`, `website/_diagram-zoom.html`, `website/index.qmd`,
  `website/_overview.qmd`, `website/architecture.qmd`, `website/design.qmd`,
  `website/changelog.md`, `website/how-we-work.md`
- Modify: `Makefile` (the `docs` recipe and the `check` line), `.github/workflows/ci.yml` (the
  `site` and `pages` jobs appended)

**Interfaces:**
- Consumes: Task 1's targets and CI; the docs under `docs/superpowers/`.
- Produces: `scripts/sitedocs.py`'s `escaped(text: str) -> str`, `title(text: str, fallback: str)
  -> str` and `main(argv=None, root=ROOT) -> int`, writing `website/superpowers/` (generated,
  git-ignored); `make docs` (the doc copies, the render, a failure on an unresolved link, lychee
  when installed); the pages Home, Architecture, Design, Changelog and How we work;
  `website/_overview.qmd`; CI jobs `site` (installs lychee; uploads the Pages artifact on `main`)
  and `pages`; the rule that every `.md` under `docs/superpowers/` has its line on the Design page.

- [x] **Step 0: Record the base:** `git rev-parse HEAD > .git/TASK_BASE`.
- [x] **Step 1: Write the failing tests.**

`tests/test_site.py`:

````python
"""Every doc under docs/superpowers/ reaches the site, its Quarto syntax shown, not run (S06)."""

from __future__ import annotations

from pathlib import Path

import sitedocs

ROOT = Path(__file__).resolve().parent.parent
OPEN, CLOSE = "{" * 2 + "<", ">" + "}" * 2
LISTING = f"""# A plan

````markdown
{OPEN} include /../README.md {CLOSE}

```{{mermaid}}
flowchart LR
  a --> b
```
````
"""


def write_doc(root: Path, rel: str, text: str) -> None:
    path = root / "docs" / "superpowers" / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_every_doc_is_copied_with_its_heading_as_the_title(tmp_path: Path) -> None:
    write_doc(tmp_path, "specs/a-design.md", "# A: design spec\n\nText.\n")
    write_doc(tmp_path, "plans/a-phase-1.md", "No heading.\n")
    assert sitedocs.main([], root=tmp_path) == 0
    site = tmp_path / "website" / "superpowers"
    spec = (site / "specs" / "a-design.md").read_text(encoding="utf-8")
    assert spec.startswith('---\npagetitle: "A: design spec"\n---\n\n# A: design spec')
    assert 'pagetitle: "a-phase-1"' in (site / "plans" / "a-phase-1.md").read_text("utf-8")


def test_shortcodes_and_executable_cells_are_shown_not_run(tmp_path: Path) -> None:
    write_doc(tmp_path, "plans/a-phase-1.md", LISTING)
    sitedocs.main([], root=tmp_path)
    page = (tmp_path / "website" / "superpowers" / "plans" / "a-phase-1.md").read_text("utf-8")
    assert f"{OPEN}/* include /../README.md */{CLOSE}" in page
    assert "```mermaid\n" in page
    assert "```{" not in page


def test_a_doc_that_is_gone_loses_its_page(tmp_path: Path) -> None:
    write_doc(tmp_path, "specs/a-design.md", "# A\n")
    stale = tmp_path / "website" / "superpowers" / "specs" / "old.md"
    stale.parent.mkdir(parents=True)
    stale.write_text("old", encoding="utf-8")
    sitedocs.main([], root=tmp_path)
    assert not stale.exists()


def test_every_real_doc_is_listed_on_the_design_page() -> None:
    docs = ROOT / "docs" / "superpowers"
    design = (ROOT / "website" / "design.qmd").read_text(encoding="utf-8")
    unlisted = [
        rel.as_posix()
        for rel in (p.relative_to(docs) for p in sorted(docs.rglob("*.md")))
        if f"(superpowers/{rel.as_posix()})" not in design
    ]
    assert not unlisted, f"docs missing from the Design page: {unlisted}"
````

- [x] **Step 2: Run them; watch them fail.** `make test`. Expected: a collection error,
  `ModuleNotFoundError: No module named 'sitedocs'`.
- [x] **Step 3: Write the copier and the site.**

`scripts/sitedocs.py`:

```python
"""Copy the docs under docs/superpowers/ into the site, with Quarto's own syntax shown, not run.

    uv run scripts/sitedocs.py
        write website/superpowers/<path> for every .md under docs/superpowers/ (generated and
        git-ignored), each with its first heading as the page's title

The plans quote Quarto's shortcodes and executable cells in their code listings, and Quarto
expands both even inside fenced code, so a plain include of a plan breaks the render. The copies
escape them instead: a shortcode's braces get Quarto's escape markers, and an executable cell's
fence loses its braces. The docs themselves stay as written, where conventions put them.
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OPEN, CLOSE = "{" * 2 + "<", ">" + "}" * 2  # spelt in parts, so this file is safe to quote
CELL = re.compile(r"^(\s*(?:`{3,}|~{3,}))\{([A-Za-z][\w-]*)\}", re.MULTILINE)


def escaped(text: str) -> str:
    """Quarto shows an escaped shortcode as written, and a fence without braces as code."""
    text = text.replace(OPEN, OPEN + "/*").replace(CLOSE, "*/" + CLOSE)
    return CELL.sub(r"\1\2", text)


def title(text: str, fallback: str) -> str:
    heading = next((line[2:].strip() for line in text.splitlines() if line.startswith("# ")), "")
    return heading or fallback


def main(argv: list[str] | None = None, root: Path = ROOT) -> int:
    docs = root / "docs" / "superpowers"
    out = root / "website" / "superpowers"
    shutil.rmtree(out, ignore_errors=True)
    copied = 0
    for doc in sorted(docs.rglob("*.md")):
        text = doc.read_text(encoding="utf-8")
        page = out / doc.relative_to(docs)
        page.parent.mkdir(parents=True, exist_ok=True)
        front = f"---\npagetitle: {json.dumps(title(text, doc.stem), ensure_ascii=False)}\n---\n\n"
        page.write_text(front + escaped(text), encoding="utf-8")
        copied += 1
    print(f"sitedocs: {copied} docs copied into website/superpowers/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

`website/_quarto.yml`:

```yaml
project:
  type: website
  output-dir: _site

website:
  title: "3d-models"
  description: "SolidCraft models and the STL files exported from them, with a 3D view of each."
  site-url: https://chendaniely.github.io/3d-models/
  repo-url: https://github.com/chendaniely/3d-models
  page-navigation: true
  navbar:
    left:
      - href: index.qmd
        text: Home
      - href: architecture.qmd
        text: Architecture
      - href: design.qmd
        text: Design
      - href: changelog.md
        text: Changelog
      - href: how-we-work.md
        text: How we work
    right:
      - icon: github
        href: https://github.com/chendaniely/3d-models
        aria-label: The repo on GitHub

format:
  html:
    theme: cosmo
    css: styles.css
    toc: true
    mermaid:
      theme: neutral
    include-after-body: _diagram-zoom.html
```

`website/styles.css`:

```css
/* Japandi: bone paper, charcoal ink, one clay accent, nothing glossy. */
:root {
  --bone: #f4f1ec;
  --charcoal: #2b2a28;
  --clay: #9c6b4e;
  --line: #d9d3c9;
}

body {
  background: var(--bone);
  color: var(--charcoal);
}

.navbar {
  background: var(--bone) !important;
  border-bottom: 1px solid var(--line);
}

.navbar .navbar-brand,
.navbar .nav-link {
  color: var(--charcoal) !important;
}

a {
  color: var(--clay);
}

.mermaid-zoomable {
  cursor: zoom-in;
}

.mermaid-zoom-overlay {
  position: fixed;
  inset: 0;
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: rgba(244, 241, 236, 0.97);
  cursor: zoom-out;
}

.mermaid-zoom-overlay svg {
  width: 100%;
  height: 100%;
  max-width: none !important;
}
```

`website/_diagram-zoom.html`:

```html
<script>
// Click or tap a diagram to open it full-screen; click again, or press Escape, to close it.
document.addEventListener("DOMContentLoaded", () => {
  const close = () => document.querySelector(".mermaid-zoom-overlay")?.remove();
  document.addEventListener("keydown", (event) => event.key === "Escape" && close());
  const ready = setInterval(() => {
    const diagrams = document.querySelectorAll(".cell-output-display svg, pre.mermaid svg");
    if (!diagrams.length) return;
    clearInterval(ready);
    diagrams.forEach((svg) => {
      svg.classList.add("mermaid-zoomable");
      svg.addEventListener("click", () => {
        const overlay = document.createElement("div");
        overlay.className = "mermaid-zoom-overlay";
        overlay.appendChild(svg.cloneNode(true));
        overlay.addEventListener("click", close);
        document.body.appendChild(overlay);
      });
    });
  }, 200);
  setTimeout(() => clearInterval(ready), 10000);
});
</script>
```

`website/index.qmd`:

```markdown
---
pagetitle: "3d-models"
toc: false
---

{{< include /../README.md >}}

## How it fits together

{{< include _overview.qmd >}}

Every diagram is on the [Architecture](architecture.qmd) page.
```

`website/_overview.qmd`:

````markdown
```{mermaid}
%%| fig-cap: "From a design to the gallery. Solid: built. Dashed: planned, labelled with the phase that brings it."
flowchart LR
  design["models/&lt;slug&gt;/&lt;slug&gt;.sc<br/>the design, plain-text JSON"]
  yml["model.yml<br/>title, summary, print settings"]
  build["make models<br/>solidcraft-cli on Dan's machine"]
  built["an STL per size · PNG · eval.json · build.json<br/>committed beside the design"]
  ci["CI on every push<br/>tests · lint · models-check · privacy · leaks · site"]
  gallery["make docs<br/>doc copies + Quarto"]
  modelpages["model pages + 3D viewer<br/>Phase 1, Task 5"]
  pages["GitHub Pages<br/>the gallery and its 3D viewer"]
  sconce["the wall sconce's models<br/>Phase 2"]

  design --> build --> built
  built --> ci
  design --> ci
  built -.-> modelpages
  yml -.-> modelpages
  modelpages -.-> gallery
  gallery --> pages
  sconce -.-> design

  classDef planned stroke-dasharray: 5 5
  class sconce,modelpages planned
```
````

`website/architecture.qmd`:

````markdown
---
title: "Architecture"
---

Every diagram for this project lives on this page; other pages link here. Solid parts are built;
dashed parts are planned, labelled with the phase that brings them. Click a diagram to open it
full-screen.

## Overview

{{< include _overview.qmd >}}

## Building a model

```{mermaid}
%%| fig-cap: "make models rebuilds only a model whose design, sizes or built files differ from its build record."
flowchart TD
  start["make models"] --> each{"for each models/&lt;slug&gt;/&lt;slug&gt;.sc"}
  each --> hash{"the design, its sizes and its built files<br/>match build.json?"}
  hash -- yes --> skip["left alone"]
  hash -- "no, or no build yet" --> run["solidcraft-cli run → &lt;slug&gt;.stl"]
  run --> snap["solidcraft-cli snapshot → &lt;slug&gt;.png"]
  snap --> evaluate["solidcraft-cli eval → &lt;slug&gt;.eval.json"]
  evaluate --> sized["for each extra size in model.yml:<br/>a parameter change → &lt;slug&gt;-&lt;size&gt;.stl"]
  sized --> record["build.json: every file's sha256, the sizes, the CLI's version"]
```

## Checks and the deploy

```{mermaid}
%%| fig-cap: "CI runs on every push; only main deploys."
flowchart LR
  push["a push"] --> tests["tests job<br/>make test · lint<br/>models-check · privacy"]
  push --> leaks["leaks job<br/>gitleaks over every commit, merges included"]
  push --> site["site job<br/>make docs, with lychee"]
  tests --> pagesjob{"on main?"}
  leaks --> pagesjob
  site --> pagesjob
  pagesjob -- yes --> deploy["pages job<br/>deploy to GitHub Pages"]
```
````

`website/design.qmd`:

```markdown
---
title: "Design"
---

How this project was planned, and how the build departed from the plan. Each page here is the file
under `docs/superpowers/` in the repo, shown as it is.

## Kickoff

- [The design spec](superpowers/specs/2026-11-05-3d-models-design.md)
- [Kickoff's questions and answers](superpowers/specs/2026-11-05-3d-models-qa.md)
- [Kickoff's notes: the sconce's feasibility](superpowers/specs/2026-11-05-3d-models-kickoff-notes.md)
- [The kickoff council's review](superpowers/specs/2026-11-05-3d-models-kickoff-council.md)

## Plans

- [Phase 1: the repo](superpowers/plans/2026-11-05-3d-models-phase-1.md)
- [Phase 2: the wall sconce](superpowers/plans/2026-11-05-3d-models-phase-2.md)
```

`website/changelog.md`:

```markdown
---
pagetitle: "Changelog"
---

{{< include /../CHANGELOG.md >}}
```

`website/how-we-work.md`:

```markdown
---
pagetitle: "How we work"
---

{{< include /../AGENTS.md >}}
```

  In the `Makefile`, replace the `docs` placeholder and set `check`'s final line:

```makefile
docs: ## Render the site into website/_site, failing on a broken link
	uv run --frozen scripts/sitedocs.py
	@set -o pipefail; quarto render website 2>&1 | tee website/.render.log
	@if grep -q 'Unable to resolve link target' website/.render.log; then \
	  echo "docs: an unresolved link, above"; exit 1; fi
	@if command -v lychee >/dev/null; then lychee --offline --no-progress website/_site; \
	else echo "lychee isn't installed: the offline link check runs in CI"; fi
```

```makefile
check: test test-utc lint models-check privacy leaks docs ## Everything CI runs, and the suite under UTC
```

  Append the `site` and `pages` jobs to `.github/workflows/ci.yml`:

```yaml
  site:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
      - uses: astral-sh/setup-uv@68559e99cc807c1eb7e9238fd43a15bba460eec2 # v10.3.3
      - uses: quarto-dev/quarto-actions/setup@8a96df13519ee81fd526f2dfca5962811136661b # v2.2.0
        with:
          version: 1.11.6
      - name: Install lychee 0.24.2, checked against its published checksum
        run: |
          curl -sSfL -o lychee.tar.gz \
            https://github.com/lycheeverse/lychee/releases/download/lychee-v0.24.2/lychee-x86_64-unknown-linux-gnu.tar.gz
          echo "1f4e0ef7f6554a6ed33dd7ac144fb2e1bbed98598e7af973042fc5cd43951c9a  lychee.tar.gz" |
            sha256sum --check --strict -
          tar -xzf lychee.tar.gz lychee
          sudo install -m 755 lychee /usr/local/bin/lychee
          rm lychee lychee.tar.gz
      - run: uv sync --frozen
      - run: make docs
      - if: github.ref == 'refs/heads/main' && github.event_name != 'pull_request'
        uses: actions/upload-pages-artifact@fc324d3547104276b827a68afc52ff2a11cc49c9 # v5.0.0
        with:
          path: website/_site

  pages:
    if: github.ref == 'refs/heads/main' && github.event_name != 'pull_request'
    needs: [tests, leaks, site]
    runs-on: ubuntu-latest
    permissions:
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@368f82528645a54fb793d4d04e342629a3f51346 # v5.0.1
```

- [x] **Step 4: Run the checks; they pass.** `make check`. Expected: every test passes twice,
  `sitedocs: 6 docs copied` (or more, as docs have been added), the render ending
  `Output created: _site/index.html` with no "Unable to resolve link target", and lychee's
  note that it runs in CI.
- [x] **Step 5: Commit.** Write the message to `.git/COMMIT_MSG`:

```text
feat(site): 🤖 add the Quarto docs site and its deploy

The repo had no site. website/ holds a Quarto site with Home (the README,
then the overview diagram), Architecture (every diagram, planned parts
dashed), Design (the spec, plans, Q&A pages and council reports), Changelog
and How we work, in a quiet Japandi palette. The plans quote Quarto's
shortcodes and executable cells in their listings, which Quarto expands
even inside fenced code, so scripts/sitedocs.py copies each doc into the
site with that syntax escaped, rather than including it. make docs renders
it and fails on an unresolved link. CI's site job installs lychee 0.24.2,
checked against its checksum, so make docs runs its offline link check; on
main it uploads the Pages artifact, and the pages job, the only one with
pages and id-token write, deploys it once tests, leaks and site pass.

The new tests failed first with: ModuleNotFoundError: No module named
'sitedocs'.

Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-1.md Task 4
Co-Authored-By: <the model's own line>
```

  `git add scripts/sitedocs.py tests/test_site.py website/_quarto.yml website/styles.css website/_diagram-zoom.html website/index.qmd website/_overview.qmd website/architecture.qmd website/design.qmd website/changelog.md website/how-we-work.md Makefile .github/workflows/ci.yml`, then `git commit -F .git/COMMIT_MSG`, then `git log -1 --format='%(trailers)'` shows the `Plan:` line.
- [x] **Step 6: Review, look forward, close.**

  - **Review (Tier 1: Matt Pocock's `code-review`, two axes in two subagents, plus the security checklist, one line per item; at most one re-review),** from `$(cat .git/TASK_BASE)`.
  - **Forward:** Task 5 adds the Models page, the viewer and the gallery's line in `make docs`; Task 9 sets Pages' source, without which the `pages` job fails on `main`.
  - **Docs:** the README's links point at the site; the overview's built parts are solid.
  - **Close,** its own commit: this task's boxes ticked, **Now** set to the next task, any
    Built differently and Ruling lines, deferred findings on the phase-end list, the spec's
    scenario statuses (`built`). The message, from `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 4: The docs site

    <what the task built, and why, in a few lines>

    Drift: <filled at the close, or none>
    Rulings: <filled at the close, or none>
    Phase-end: <filled at the close, or none>
    Forward: <filled at the close, or none>
    Tier: 1
    Rounds: <filled at the close>
    Findings: <filled at the close, or none>

    Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-1.md Task 4
    Co-Authored-By: <the model's own line>
    ```

  - **Push,** once Dan has OKed it, the request naming every binary file the push adds
    (`AGENTS.md`'s interim line): `make leaks privacy`, then `git push origin phase-1`.
    The task is closed once CI on the closing commit, or a later one, is green; until a
    push, the local checks are the gate.

***

### Task 5: The gallery and the 3D viewer

**Tier:** 2 · **Scenarios:** S07, S08, S19, S20

**Files:**
- Create: `scripts/gallery.py`, `tests/test_gallery.py`, `website/models.qmd`,
  `website/_stl-viewer.html`, `website/assets/stl-viewer.js`, `website/assets/three/` (five files
  from npm's `three@0.187.0`)
- Modify: `website/_quarto.yml` (resources and a navbar entry), `website/styles.css` (the
  viewer's rules), `website/_overview.qmd` (the gallery drawn as built), `Makefile` (one line in
  `docs`), `README.md` (an "Adding a model" section)

**Interfaces:**
- Consumes: Task 2's `ROOT`, `Model`, `find_models`, `sizes`; Task 4's site and `make docs`.
- Produces, in `scripts/gallery.py`: `ModelError(ValueError)`; `read_meta(model: Model) -> dict`
  (fields `title`, `summary`, `status` in `designed | printed | in use`, `material`; optional
  `print` mapping with no bare booleans, `notes`, `size`; and `sizes`, filled from
  `models.sizes`); `read_eval(model: Model) -> dict`; `photos(model: Model) -> list[Path]`;
  `page(model: Model, meta: dict, evaluation: dict) -> str`; `main(argv=None, root=ROOT) -> int`.
  On the site: `website/models/<slug>.qmd` (generated, git-ignored) and the
  `<div class="stl-viewer" data-stl="<slug>/<slug>.stl">` the viewer mounts on.

- [x] **Step 0: Record the base:** `git rev-parse HEAD > .git/TASK_BASE`.
- [x] **Step 1: Write the failing tests.**

`tests/test_gallery.py`:

```python
"""scripts/gallery.py: a card and a page per model (S07), with a 3D viewer, downloads for each size,
photos and a licence (S08, S19)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from PIL import Image

import gallery
from conftest import add_design

META = """\
title: Test hook
summary: A hook for testing.
status: printed
material: PETG
print:
  Layer height: 0.2 mm
  Infill: 20%
notes: Hang it on a dowel.
"""
SIZED = META + "size: 1 in\nsizes:\n  3/4 in: {dowel_d: 19.05 mm}\n  25 mm: {dowel_d: 25 mm}\n"

EVAL = {
    "bodies": [
        {"bbox": {"min": [0, 0, 0], "max": [40, 20, 10]}, "volume_mm3": 5000.0},
        {"bbox": {"min": [-5, 0, 0], "max": [10, 30, 5]}, "volume_mm3": 1000.0},
    ],
    "params": [{"name": "hook_w", "expression": "20 mm", "unit": "mm", "value": 20.0}],
}


def add_model(root: Path, slug: str = "hook", meta: str = META) -> Path:
    design = add_design(root, slug)
    folder = design.parent
    (folder / "model.yml").write_text(meta, encoding="utf-8")
    (folder / f"{slug}.eval.json").write_text(json.dumps(EVAL), encoding="utf-8")
    for name in (f"{slug}.stl", f"{slug}-3-4in.stl", f"{slug}-25mm.stl"):
        (folder / name).write_bytes(b"solid")
    (folder / f"{slug}.png").write_bytes(b"\x89PNG")
    return folder


def page(repo: Path, slug: str = "hook") -> str:
    assert gallery.main([], root=repo) == 0
    return (repo / "website" / "models" / f"{slug}.qmd").read_text(encoding="utf-8")


def test_write_makes_a_page_and_copies_the_files(repo: Path) -> None:
    add_model(repo)
    page(repo)
    out = repo / "website" / "models" / "hook"
    assert sorted(p.name for p in out.iterdir()) == ["hook.png", "hook.sc", "hook.stl"]


def test_the_page_is_a_card_with_a_picture_title_and_summary(repo: Path) -> None:
    add_model(repo)
    front = page(repo).split("---")[1]
    assert 'title: "Test hook"' in front
    assert 'description: "A hook for testing."' in front
    assert "image: hook/hook.png" in front


def test_the_page_has_the_viewer_the_measurements_and_the_downloads(repo: Path) -> None:
    add_model(repo)
    text = page(repo)
    assert "include-in-header: ../_stl-viewer.html" in text
    assert '::: {.stl-viewer data-stl="hook/hook.stl"' in text
    assert "| Size (x × y × z) | 45.0 × 30.0 × 10.0 mm |" in text
    assert "| Volume | 6.0 cm³ |" in text
    assert "| Weight in PETG, solid | 8 g |" in text
    assert "| `hook_w` | `20 mm` | 20 mm |" in text
    assert "| Infill | 20% |" in text
    assert "Hang it on a dowel." in text
    assert "- [hook.stl](hook/hook.stl): the mesh to slice\n" in text
    assert "- [hook.sc](hook/hook.sc)" in text
    assert "https://github.com/chendaniely/3d-models/tree/main/models/hook" in text


def test_every_page_carries_the_licence(repo: Path) -> None:
    add_model(repo)
    text = page(repo)
    assert "## Licence" in text
    assert "[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)" in text


def test_a_model_with_sizes_offers_an_stl_for_each(repo: Path) -> None:
    add_model(repo, meta=SIZED)
    text = page(repo)
    assert "- [hook.stl](hook/hook.stl): the mesh to slice, for 1 in" in text
    assert "- [hook-3-4in.stl](hook/hook-3-4in.stl): for 3/4 in" in text
    assert "- [hook-25mm.stl](hook/hook-25mm.stl): for 25 mm" in text
    assert "change `dowel_d` under Parameters" in text
    files = sorted(p.name for p in (repo / "website" / "models" / "hook").iterdir())
    assert files == ["hook-25mm.stl", "hook-3-4in.stl", "hook.png", "hook.sc", "hook.stl"]


def test_a_model_with_sizes_names_the_size_it_is_saved_at(repo: Path, capsys) -> None:
    add_model(repo, meta=SIZED.replace("size: 1 in\n", ""))
    assert gallery.main([], root=repo) == 1
    assert "'size' names the size the design is saved at" in capsys.readouterr().err


def test_photos_are_published_on_the_page(repo: Path) -> None:
    folder = add_model(repo)
    (folder / "photos").mkdir()
    Image.new("RGB", (8, 8)).save(folder / "photos" / "installed.jpg")
    text = page(repo)
    assert "## Photos\n\n![](hook/photos/installed.jpg)" in text
    assert (repo / "website" / "models" / "hook" / "photos" / "installed.jpg").is_file()


def test_write_removes_the_page_of_a_model_that_is_gone(repo: Path) -> None:
    add_model(repo)
    stale = repo / "website" / "models" / "old.qmd"
    stale.parent.mkdir(parents=True)
    stale.write_text("old", encoding="utf-8")
    page(repo)
    assert not stale.exists()


def test_a_bar_in_a_print_setting_stays_inside_its_cell(repo: Path) -> None:
    add_model(repo, meta=META.replace("Infill: 20%", "Infill: 20% | gyroid"))
    assert "| Infill | 20% \\| gyroid |" in page(repo)


@pytest.mark.parametrize(
    ("meta", "message"),
    [
        (META.replace("title: Test hook\n", ""), "'title' must be a non-empty string"),
        (META.replace("status: printed", "status: lost"), "'status' must be one of"),
        (
            META.replace("  Layer height: 0.2 mm\n  Infill: 20%", "  - Layer height 0.2 mm"),
            "'print' must map settings to values",
        ),
        (META.replace("Infill: 20%", "Supports: no"), "quote the print setting Supports"),
        (META + "notes: [unclosed\n", "isn't valid YAML"),
    ],
)
def test_write_names_a_bad_model_yml_and_writes_nothing(
    repo: Path, capsys, meta: str, message: str
) -> None:
    add_model(repo, meta=meta)
    assert gallery.main([], root=repo) == 1
    err = capsys.readouterr().err
    assert "gallery: models/hook/model.yml" in err
    assert message in err
    assert not (repo / "website" / "models").exists()


def test_write_names_a_model_without_a_model_yml(repo: Path, capsys) -> None:
    folder = add_model(repo)
    (folder / "model.yml").unlink()
    assert gallery.main([], root=repo) == 1
    assert "gallery: models/hook: no model.yml" in capsys.readouterr().err


def test_write_names_a_model_never_built(repo: Path, capsys) -> None:
    folder = add_model(repo)
    (folder / "hook.eval.json").unlink()
    assert gallery.main([], root=repo) == 1
    assert "gallery: models/hook: no hook.eval.json; run make models" in capsys.readouterr().err
```

- [x] **Step 2: Run them; watch them fail.** `make test`. Expected: a collection error,
  `ModuleNotFoundError: No module named 'gallery'`.
- [x] **Step 3: Write the gallery and the viewer.**

`scripts/gallery.py`:

```python
"""Write the site's model pages from models/.

    uv run scripts/gallery.py
        write website/models/<slug>.qmd for each model, and copy its STLs, picture, design and
        photos beside it

website/models/ is generated and git-ignored: each run empties it first, so a removed model's page
goes with it. Each model's model.yml gives its title, summary, status, material, size, print
settings and notes; its eval.json gives the measurements and parameters.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import yaml

from models import ROOT, Model, find_models, sizes

REPO_URL = "https://github.com/chendaniely/3d-models"
LICENCE = (
    "[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/): print it, change it and "
    "share it, crediting chendaniely and linking here; don't sell it or prints of it."
)
STATUSES = ("designed", "printed", "in use")
DENSITY_G_CM3 = {"PLA": 1.24, "PETG": 1.27}
PHOTOS = {".jpg", ".jpeg", ".png", ".webp"}


class ModelError(ValueError):
    """A model.yml or eval.json that can't make a page."""


def read_meta(model: Model) -> dict:
    path = model.folder / "model.yml"
    if not path.is_file():
        raise ModelError(f"models/{model.slug}: no model.yml")
    where = f"models/{model.slug}/model.yml"
    try:
        meta = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as error:
        raise ModelError(f"{where} isn't valid YAML: {error}") from error
    if not isinstance(meta, dict):
        raise ModelError(f"{where} must be a mapping of fields")
    for field in ("title", "summary", "status", "material"):
        if not isinstance(meta.get(field), str) or not meta[field].strip():
            raise ModelError(f"{where}: '{field}' must be a non-empty string")
    if meta["status"] not in STATUSES:
        raise ModelError(f"{where}: 'status' must be one of {', '.join(STATUSES)}")
    print_settings = meta.get("print", {})
    if not isinstance(print_settings, dict) or not all(
        isinstance(k, str) and isinstance(v, str | int | float) for k, v in print_settings.items()
    ):
        raise ModelError(f"{where}: 'print' must map settings to values")
    flags = [k for k, v in print_settings.items() if isinstance(v, bool)]
    if flags:
        raise ModelError(
            f"{where}: quote the print setting {', '.join(flags)}: YAML reads yes and no as true "
            "and false"
        )
    for field in ("notes", "size"):
        if not isinstance(meta.get(field, ""), str):
            raise ModelError(f"{where}: '{field}' must be text")
    try:
        meta["sizes"] = sizes(model)
    except ValueError as error:
        raise ModelError(str(error)) from error
    if meta["sizes"] and not meta.get("size"):
        raise ModelError(f"{where}: with 'sizes', 'size' names the size the design is saved at")
    return meta


def read_eval(model: Model) -> dict:
    path = model.built("eval.json")
    if not path.is_file():
        raise ModelError(f"models/{model.slug}: no {path.name}; run make models")
    return json.loads(path.read_text(encoding="utf-8"))


def photos(model: Model) -> list[Path]:
    folder = model.folder / "photos"
    if not folder.is_dir():
        return []
    return sorted(p for p in folder.iterdir() if p.suffix.lower() in PHOTOS)


def quoted(text: str) -> str:
    return json.dumps(text.strip(), ensure_ascii=False)


def cell(value: object) -> str:
    """Text for one markdown table cell: a | would end the cell, a newline the row."""
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def measurements(evaluation: dict) -> list[tuple[str, str]]:
    bodies = evaluation.get("bodies", [])
    if not bodies:
        return []
    low = [min(b["bbox"]["min"][i] for b in bodies) for i in range(3)]
    high = [max(b["bbox"]["max"][i] for b in bodies) for i in range(3)]
    size = " × ".join(f"{high[i] - low[i]:.1f}" for i in range(3))
    volume_cm3 = sum(b["volume_mm3"] for b in bodies) / 1000
    rows = [("Size (x × y × z)", f"{size} mm"), ("Volume", f"{volume_cm3:.1f} cm³")]
    rows += [
        (f"Weight in {name}, solid", f"{volume_cm3 * density:.0f} g")
        for name, density in DENSITY_G_CM3.items()
    ]
    return rows


def downloads(model: Model, meta: dict) -> list[str]:
    slug = model.slug
    lines = ["## Files", ""]
    if meta["sizes"]:
        lines.append(f"- [{slug}.stl]({slug}/{slug}.stl): the mesh to slice, for {meta['size']}")
        lines += [
            f"- [{model.sized(size).name}]({slug}/{model.sized(size).name}): for {size}"
            for size in meta["sizes"]
        ]
    else:
        lines.append(f"- [{slug}.stl]({slug}/{slug}.stl): the mesh to slice")
    lines += [
        f"- [{slug}.sc]({slug}/{slug}.sc): the SolidCraft design, every dimension a parameter",
        f"- [The model's folder on GitHub]({REPO_URL}/tree/main/models/{slug})",
        "",
    ]
    if meta["sizes"]:
        names = sorted({name for changes in meta["sizes"].values() for name in changes})
        changed = " and ".join(f"`{name}`" for name in names)
        lines += [
            "**For another size:** open the `.sc` in SolidCraft and change "
            f"{changed} under Parameters; every other dimension follows.",
            "",
        ]
    return lines


def page(model: Model, meta: dict, evaluation: dict) -> str:
    slug = model.slug
    lines = [
        "---",
        f"title: {quoted(meta['title'])}",
        f"description: {quoted(meta['summary'])}",
        f"image: {slug}/{slug}.png",
        "include-in-header: ../_stl-viewer.html",
        "---",
        "",
        f'::: {{.stl-viewer data-stl="{slug}/{slug}.stl" role="img" '
        f"aria-label={quoted('A 3D view of ' + meta['title'] + ' you can turn')}}}",
        ":::",
        "",
        f"Drag to turn it, scroll to zoom. **Status:** {meta['status']}. "
        f"**Material:** {meta['material']}.",
        "",
        f"![{meta['title']}, as SolidCraft draws it]({slug}/{slug}.png)"
        f"{{fig-alt={quoted(meta['title'] + ', seen from above at an angle')}}}",
        "",
    ]
    if meta.get("notes", "").strip():
        lines += ["## Notes", "", meta["notes"].strip(), ""]
    shots = photos(model)
    if shots:
        lines += ["## Photos", ""]
        lines += [f"![]({slug}/photos/{shot.name})" for shot in shots]
        lines.append("")
    if meta.get("print"):
        lines += ["## Printing", "", "| Setting | Value |", "|---|---|"]
        lines += [f"| {cell(key)} | {cell(value)} |" for key, value in meta["print"].items()]
        lines.append("")
    rows = measurements(evaluation)
    if rows:
        lines += ["## Measurements", "", "| | |", "|---|---|"]
        lines += [f"| {label} | {value} |" for label, value in rows]
        lines.append("")
    params = evaluation.get("params", [])
    if params:
        lines += ["## Parameters", "", "| Name | Expression | Value |", "|---|---|---|"]
        for param in params:
            value = f"{param['value']:g} {param.get('unit', '')}".strip()
            lines.append(f"| `{param['name']}` | `{param['expression']}` | {value} |")
        lines.append("")
    lines += downloads(model, meta)
    lines += ["## Licence", "", LICENCE, ""]
    return "\n".join(lines)


def main(argv: list[str] | None = None, root: Path = ROOT) -> int:
    out = root / "website" / "models"
    models = find_models(root)
    try:
        pages = [(m, read_meta(m)) for m in models]
        pages = [(m, meta, page(m, meta, read_eval(m))) for m, meta in pages]
    except ModelError as error:
        print(f"gallery: {error}", file=sys.stderr)
        return 1
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)
    for model, meta, text in pages:
        (out / f"{model.slug}.qmd").write_text(text, encoding="utf-8")
        files = out / model.slug
        files.mkdir()
        copied = [model.built("stl"), model.built("png"), model.design]
        copied += [model.sized(size) for size in meta["sizes"]]
        for source in copied:
            shutil.copy2(source, files / source.name)
        if photos(model):
            (files / "photos").mkdir()
            for shot in photos(model):
                shutil.copy2(shot, files / "photos" / shot.name)
    print(f"gallery: {len(pages)} model pages in website/models/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

`website/models.qmd`:

```markdown
---
title: "Models"
listing:
  contents: models/*.qmd
  type: grid
  sort: title
  fields: [image, title, description]
  image-height: 220px
---

Every model has a page with a 3D view you can turn, its print settings, its measurements, and the
`.stl` and `.sc` files to download.
```

`website/_stl-viewer.html`:

```html
<script type="importmap">
{
  "imports": {
    "three": "../assets/three/three.module.js",
    "three/addons/": "../assets/three/"
  }
}
</script>
<script type="module" src="../assets/stl-viewer.js"></script>
```

`website/assets/stl-viewer.js`:

```javascript
// Turns each <div class="stl-viewer" data-stl="..."> into a 3D view of that STL:
// drag to rotate, scroll to zoom, right-drag to pan. three.js 0.187.0 is served from
// website/assets/three/ (copied from npm's package), named by the page's import map.
import * as THREE from "three";
import { STLLoader } from "three/addons/STLLoader.js";
import { OrbitControls } from "three/addons/OrbitControls.js";

const BONE = 0xf4f1ec;
const OAK = 0xc9b79c;

function mount(element) {
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(window.devicePixelRatio);
  element.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(BONE);
  scene.add(new THREE.HemisphereLight(0xffffff, 0x8a8178, 2.0));

  const camera = new THREE.PerspectiveCamera(35, 1, 0.1, 10000);
  const key = new THREE.DirectionalLight(0xffffff, 1.8);
  key.position.set(1, 2, 3);
  camera.add(key); // the light follows the camera, so every side is lit as it turns
  scene.add(camera);

  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;

  const resize = () => {
    const width = element.clientWidth;
    const height = element.clientHeight || Math.round(width * 2 / 3);
    renderer.setSize(width, height);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
  };
  new ResizeObserver(resize).observe(element);
  resize();

  new STLLoader().load(
    element.dataset.stl,
    (geometry) => {
      geometry.computeVertexNormals();
      geometry.center();
      const material = new THREE.MeshStandardMaterial({ color: OAK, roughness: 0.85 });
      const mesh = new THREE.Mesh(geometry, material);
      mesh.rotation.x = -Math.PI / 2; // SolidCraft is Z-up; three.js is Y-up
      scene.add(mesh);
      const size = new THREE.Box3().setFromObject(mesh).getSize(new THREE.Vector3()).length();
      camera.near = size / 100;
      camera.far = size * 100;
      camera.position.set(size * 0.7, size * 0.6, size * 0.9);
      camera.updateProjectionMatrix();
      controls.update();
      element.dataset.loaded = "true";
    },
    undefined,
    () => {
      element.classList.add("stl-viewer-failed");
      element.textContent = "The 3D view didn't load; the picture below shows the model.";
    },
  );

  renderer.setAnimationLoop(() => {
    controls.update();
    renderer.render(scene, camera);
  });
}

document.querySelectorAll(".stl-viewer[data-stl]").forEach(mount);
```

  three.js, copied from npm's package rather than loaded from a CDN, in a scratch folder:
  `npm pack three@0.187.0`, `tar -xzf three-0.187.0.tgz`, then copy `package/build/three.module.js`,
  `package/build/three.core.js`, `package/examples/jsm/loaders/STLLoader.js`,
  `package/examples/jsm/controls/OrbitControls.js` and `package/LICENSE` into
  `website/assets/three/`. `cd website/assets/three && shasum -a 256 -c` with:

```text
613e370f76638fdef83926642bf256dc9615684922de1ce1f63a8583e5d78578  three.core.js
104f56145899722094556490d787aae0617cc2fc3382f31df02d724ea1aee341  three.module.js
a07441b8cd812faf8049741fe5e95373b19547e4038694753dfec26fe230a7eb  STLLoader.js
e7fca2fe9e7670a828af9b28084669a5909445b7f36f1f26cee9bf8f2961c32c  OrbitControls.js
8b378ebe60e2fe500158cb0ac71cb5e8b7d92953c2abcc63a0eb90499653b5bc  LICENSE
```

  Expected: five `OK` lines.

  In `website/_quarto.yml`, under `project:` after `output-dir: _site`, add:

```yaml
  resources:
    - assets/
    - models/*/
```

  and in the navbar, after Home's entry:

```yaml
      - href: models.qmd
        text: Models
```

  In `website/styles.css`, before `.mermaid-zoomable`, add:

```css
.stl-viewer {
  width: 100%;
  aspect-ratio: 3 / 2;
  border: 1px solid var(--line);
  border-radius: 6px;
  background: var(--bone);
  cursor: grab;
}

.stl-viewer-failed {
  display: flex;
  align-items: center;
  justify-content: center;
  aspect-ratio: auto;
  padding: 1rem;
  cursor: default;
}
```

  Replace `website/_overview.qmd` with:

````markdown
```{mermaid}
%%| fig-cap: "From a design to the gallery. Solid: built. Dashed: planned, labelled with the phase that brings it."
flowchart LR
  design["models/&lt;slug&gt;/&lt;slug&gt;.sc<br/>the design, plain-text JSON"]
  yml["model.yml<br/>title, summary, print settings"]
  build["make models<br/>solidcraft-cli on Dan's machine"]
  built["an STL per size · PNG · eval.json · build.json<br/>committed beside the design"]
  ci["CI on every push<br/>tests · lint · models-check · privacy · leaks · site"]
  gallery["make docs<br/>doc copies + model pages + Quarto"]
  pages["GitHub Pages<br/>the gallery and its 3D viewer"]
  sconce["the wall sconce's models<br/>Phase 2"]

  design --> build --> built
  built --> ci
  design --> ci
  built --> gallery
  yml --> gallery
  gallery --> pages
  sconce -.-> design

  classDef planned stroke-dasharray: 5 5
  class sconce planned
```
````

  The `docs` recipe in full:

```makefile
docs: ## Render the site into website/_site, failing on a broken link
	uv run --frozen scripts/sitedocs.py
	uv run --frozen scripts/gallery.py
	@set -o pipefail; quarto render website 2>&1 | tee website/.render.log
	@if grep -q 'Unable to resolve link target' website/.render.log; then \
	  echo "docs: an unresolved link, above"; exit 1; fi
	@if command -v lychee >/dev/null; then lychee --offline --no-progress website/_site; \
	else echo "lychee isn't installed: the offline link check runs in CI"; fi
```

  In `README.md`, before "## How it's built", add:

````markdown
## Adding a model

1. Make a folder `models/<slug>/`, its name lowercase words joined by hyphens: it becomes the
   page's address.
2. Save the design there as `<slug>.sc`, in SolidCraft's plain-text JSON format where you can, so
   a diff can read it (a design saved in the default zip format builds too).
3. Write `models/<slug>/model.yml`:

   ```yaml
   title: Wall hook
   summary: One sentence, shown on the gallery's card.
   status: designed          # designed, printed or in use
   material: PETG
   size: 1 in                # with sizes below: the size the design is saved at
   sizes:                    # optional: one more STL for each, by changing parameters
     3/4 in: {dowel_d: 19.05 mm}
   print:
     Orientation: flat on its back
     Supports: "no"          # quote yes and no, or YAML reads them as true and false
   notes: |
     Anything someone printing it should know.
   ```

4. `make models`, then `make check`, and commit the folder. A photo of a print goes in
   `models/<slug>/photos/`, stripped first: `uv run --frozen scripts/privacy.py strip <file>`.
````

- [x] **Step 4: Run the checks; they pass.** `make check`. Expected: every test passes twice,
  `gallery: 0 model pages in website/models/`, and the render clean but for one WARN that the
  Models listing matches no files, until Task 6 adds the coupon.
- [x] **Step 5: Commit.** Write the message to `.git/COMMIT_MSG`:

```text
feat(site): 🤖 a gallery page per model, with a 3D viewer

The site had no models. scripts/gallery.py turns each model's model.yml
and measurements into a page under website/models/ (generated,
git-ignored): its picture, notes, photos, print settings, measurements,
parameters, a download for each size with a note on which parameters to
change for another, and the CC BY-NC 4.0 licence. It copies the STLs,
picture, design and photos beside it; a bad model.yml is named and nothing
is written. The Models page lists a card per model.
website/assets/stl-viewer.js mounts a three.js 0.187.0 view on each page,
three.js served from the site itself, copied from npm's package and
checked by SHA-256, so no visitor's browser calls a CDN. The README says
how to add a model.

The new tests failed first with: ModuleNotFoundError: No module named
'gallery'.

Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-1.md Task 5
Co-Authored-By: <the model's own line>
```

  `git add scripts/gallery.py tests/test_gallery.py website/models.qmd website/_stl-viewer.html website/assets/stl-viewer.js website/assets/three website/_quarto.yml website/styles.css website/_overview.qmd Makefile README.md`, then `git commit -F .git/COMMIT_MSG`, then `git log -1 --format='%(trailers)'` shows the `Plan:` line.
- [x] **Step 6: Review, look forward, close.** The review includes the viewer seen working: once
  Task 6's coupon is in, or with a scratch model not committed, `make docs`, serve `website/_site`
  on a free local port, open a model's page, and confirm its `.stl-viewer` has
  `data-loaded="true"`, a canvas, and three.js fetched from `assets/three/`; record it under
  `Rounds:`. The security checklist gets one line for the import map.

  - **Review (Tier 2: Matt Pocock's `code-review`, two axes in two subagents; fix Critical and Important; at most one re-review),** from `$(cat .git/TASK_BASE)`.
  - **Forward:** Tasks 6 to 8's `model.yml` files must pass `read_meta`.
  - **Docs:** the overview diagram's gallery is solid; the README's gallery line stays true.
  - **Close,** its own commit: this task's boxes ticked, **Now** set to the next task, any
    Built differently and Ruling lines, deferred findings on the phase-end list, the spec's
    scenario statuses (`built`). The message, from `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 5: The gallery and the 3D viewer

    <what the task built, and why, in a few lines>

    Drift: <filled at the close, or none>
    Rulings: <filled at the close, or none>
    Phase-end: <filled at the close, or none>
    Forward: <filled at the close, or none>
    Tier: 2
    Rounds: <filled at the close>
    Findings: <filled at the close, or none>

    Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-1.md Task 5
    Co-Authored-By: <the model's own line>
    ```

  - **Push,** once Dan has OKed it, the request naming every binary file the push adds
    (`AGENTS.md`'s interim line): `make leaks privacy`, then `git push origin phase-1`.
    The task is closed once CI on the closing commit, or a later one, is green; until a
    push, the local checks are the gate.

***

### Task 6: The dowel fit-test coupon

**Tier:** 1 · **Scenarios:** S09, S19

**Files:**
- Create: `models/dowel-fit-coupon/dowel-fit-coupon.sc` (by SolidCraft), its built files (`.stl`, `-3-4in.stl`,
  `-25mm.stl`, `.png`, `.eval.json`, `build.json`, by `make models`), `models/dowel-fit-coupon/model.yml`,
  `tests/test_coupon.py`

**Interfaces:**
- Consumes: Task 2's `make models`, `Model`, `sizes` and the conftest helpers; Task 5's
  `read_meta` and the page.
- Produces: the design's parameters `dowel_d` (25.4 mm), `step` (0.2 mm), `wall`, `margin`, `bar_h`, `dot_d`, `dot_depth`, `pitch`, `bar_l`, `bar_w`, which the dowel parts' `clearance` comes from (`step` times the dots of the hole that fit).

- [x] **Step 0: Record the base:** `git rev-parse HEAD > .git/TASK_BASE`.
- [x] **Step 1: Write the failing tests.**

`tests/test_coupon.py`:

```python
"""The dowel fit-test coupon (S09): four holes at +0.2 to +0.8 mm, marked by 1 to 4 dots."""

from __future__ import annotations

import math
from pathlib import Path

import pytest

import gallery
import models
from conftest import body, params

COUPON = models.Model(Path(__file__).resolve().parent.parent / "models" / "dowel-fit-coupon")


def test_it_is_saved_for_a_one_inch_dowel_in_steps_of_a_fifth_of_a_millimetre() -> None:
    assert params(COUPON)["dowel_d"] == pytest.approx(25.4)
    assert params(COUPON)["step"] == pytest.approx(0.2)


def test_it_comes_in_three_dowel_sizes() -> None:
    assert models.sizes(COUPON) == {
        "3/4 in": {"dowel_d": "19.05 mm"},
        "25 mm": {"dowel_d": "25 mm"},
    }


def test_it_is_one_closed_body_with_four_holes_and_ten_dots() -> None:
    coupon = body(COUPON, "Coupon")
    assert coupon["closed"]
    assert coupon["face_types"]["cylinder"] == 4 + (1 + 2 + 3 + 4)


def test_its_volume_matches_holes_at_plus_point_two_to_point_eight() -> None:
    p = params(COUPON)
    box = p["bar_l"] * p["bar_w"] * p["bar_h"]
    holes = sum(
        math.pi * ((p["dowel_d"] + k * p["step"]) / 2) ** 2 * p["bar_h"] for k in (1, 2, 3, 4)
    )
    dots = 10 * math.pi * (p["dot_d"] / 2) ** 2 * p["dot_depth"]
    assert body(COUPON, "Coupon")["volume_mm3"] == pytest.approx(box - holes - dots, rel=1e-3)


def test_its_page_says_how_to_read_each_hole_and_how_to_print_it() -> None:
    meta = gallery.read_meta(COUPON)
    for dots, clearance, hole in [(1, "0.2", "25.6"), (2, "0.4", "25.8"), (3, "0.6", "26.0"),
                                  (4, "0.8", "26.2")]:  # fmt: skip
        assert f"| {dots} | +{clearance} mm | {hole} mm |" in meta["notes"]
    assert "the holes horizontal" in meta["print"]["Orientation"]
```

- [x] **Step 2: Run them; watch them fail.** `make test`. Expected: `FileNotFoundError` for
  `models/dowel-fit-coupon/dowel-fit-coupon.eval.json`.
- [x] **Step 3: Build the design.** Write SolidCraft's command script to `.git/coupon-script.json`
  (it stays out of the repo: the saved design holds the same feature tree, and
  `solidcraft-cli script` regenerates it):

```json
{
  "commands": [
    {
      "command": "parameters.add",
      "params": {
        "name": "dowel_d",
        "expression": "25.4 mm",
        "comment": "the dowel's nominal diameter: 1 inch"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "step",
        "expression": "0.2 mm",
        "comment": "clearance added per hole: hole k is dowel_d + k * step"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "wall",
        "expression": "4 mm",
        "comment": "plastic between neighbouring holes"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "margin",
        "expression": "8 mm",
        "comment": "the band along the front that carries the marker dots"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "bar_h",
        "expression": "12 mm",
        "comment": "the bar's height, so each hole is this deep"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "dot_d",
        "expression": "2 mm",
        "comment": "a marker dot's diameter"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "dot_depth",
        "expression": "0.6 mm",
        "comment": "a marker dot's depth"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "pitch",
        "expression": "dowel_d + 4 * step + wall",
        "comment": "centre to centre between holes"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "bar_l",
        "expression": "4 * pitch + wall",
        "comment": "the bar's length"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "bar_w",
        "expression": "margin + pitch",
        "comment": "the bar's width"
      }
    },
    {
      "command": "solid.box",
      "params": {
        "length": "bar_l",
        "width": "bar_w",
        "height": "bar_h",
        "body_name": "Coupon"
      }
    },
    {
      "command": "solid.cylinder",
      "params": {
        "diameter": "dowel_d + 1 * step",
        "height": "bar_h",
        "base": [
          "wall / 2 + 0.5 * pitch",
          "margin + pitch / 2",
          0
        ],
        "body_name": "Hole 1"
      }
    },
    {
      "command": "solid.cylinder",
      "params": {
        "diameter": "dot_d",
        "height": "dot_depth",
        "base": [
          "wall / 2 + 0.5 * pitch",
          "margin / 2",
          "bar_h - dot_depth"
        ],
        "body_name": "Hole 1 dot 1"
      }
    },
    {
      "command": "solid.cylinder",
      "params": {
        "diameter": "dowel_d + 2 * step",
        "height": "bar_h",
        "base": [
          "wall / 2 + 1.5 * pitch",
          "margin + pitch / 2",
          0
        ],
        "body_name": "Hole 2"
      }
    },
    {
      "command": "solid.cylinder",
      "params": {
        "diameter": "dot_d",
        "height": "dot_depth",
        "base": [
          "wall / 2 + 1.5 * pitch + -0.5 * 3 mm",
          "margin / 2",
          "bar_h - dot_depth"
        ],
        "body_name": "Hole 2 dot 1"
      }
    },
    {
      "command": "solid.cylinder",
      "params": {
        "diameter": "dot_d",
        "height": "dot_depth",
        "base": [
          "wall / 2 + 1.5 * pitch + 0.5 * 3 mm",
          "margin / 2",
          "bar_h - dot_depth"
        ],
        "body_name": "Hole 2 dot 2"
      }
    },
    {
      "command": "solid.cylinder",
      "params": {
        "diameter": "dowel_d + 3 * step",
        "height": "bar_h",
        "base": [
          "wall / 2 + 2.5 * pitch",
          "margin + pitch / 2",
          0
        ],
        "body_name": "Hole 3"
      }
    },
    {
      "command": "solid.cylinder",
      "params": {
        "diameter": "dot_d",
        "height": "dot_depth",
        "base": [
          "wall / 2 + 2.5 * pitch + -1 * 3 mm",
          "margin / 2",
          "bar_h - dot_depth"
        ],
        "body_name": "Hole 3 dot 1"
      }
    },
    {
      "command": "solid.cylinder",
      "params": {
        "diameter": "dot_d",
        "height": "dot_depth",
        "base": [
          "wall / 2 + 2.5 * pitch",
          "margin / 2",
          "bar_h - dot_depth"
        ],
        "body_name": "Hole 3 dot 2"
      }
    },
    {
      "command": "solid.cylinder",
      "params": {
        "diameter": "dot_d",
        "height": "dot_depth",
        "base": [
          "wall / 2 + 2.5 * pitch + 1 * 3 mm",
          "margin / 2",
          "bar_h - dot_depth"
        ],
        "body_name": "Hole 3 dot 3"
      }
    },
    {
      "command": "solid.cylinder",
      "params": {
        "diameter": "dowel_d + 4 * step",
        "height": "bar_h",
        "base": [
          "wall / 2 + 3.5 * pitch",
          "margin + pitch / 2",
          0
        ],
        "body_name": "Hole 4"
      }
    },
    {
      "command": "solid.cylinder",
      "params": {
        "diameter": "dot_d",
        "height": "dot_depth",
        "base": [
          "wall / 2 + 3.5 * pitch + -1.5 * 3 mm",
          "margin / 2",
          "bar_h - dot_depth"
        ],
        "body_name": "Hole 4 dot 1"
      }
    },
    {
      "command": "solid.cylinder",
      "params": {
        "diameter": "dot_d",
        "height": "dot_depth",
        "base": [
          "wall / 2 + 3.5 * pitch + -0.5 * 3 mm",
          "margin / 2",
          "bar_h - dot_depth"
        ],
        "body_name": "Hole 4 dot 2"
      }
    },
    {
      "command": "solid.cylinder",
      "params": {
        "diameter": "dot_d",
        "height": "dot_depth",
        "base": [
          "wall / 2 + 3.5 * pitch + 0.5 * 3 mm",
          "margin / 2",
          "bar_h - dot_depth"
        ],
        "body_name": "Hole 4 dot 3"
      }
    },
    {
      "command": "solid.cylinder",
      "params": {
        "diameter": "dot_d",
        "height": "dot_depth",
        "base": [
          "wall / 2 + 3.5 * pitch + 1.5 * 3 mm",
          "margin / 2",
          "bar_h - dot_depth"
        ],
        "body_name": "Hole 4 dot 4"
      }
    },
    {
      "command": "solid.combine",
      "params": {
        "target": "Coupon",
        "tools": [
          "Hole 1",
          "Hole 1 dot 1",
          "Hole 2",
          "Hole 2 dot 1",
          "Hole 2 dot 2",
          "Hole 3",
          "Hole 3 dot 1",
          "Hole 3 dot 2",
          "Hole 3 dot 3",
          "Hole 4",
          "Hole 4 dot 1",
          "Hole 4 dot 2",
          "Hole 4 dot 3",
          "Hole 4 dot 4"
        ],
        "operation": "cut"
      }
    },
    {
      "command": "file.save_as",
      "params": {
        "path": "models/dowel-fit-coupon/dowel-fit-coupon.sc",
        "format": "json",
        "cache": false
      }
    }
  ]
}
```

  From the repo's root: `mkdir -p models/dowel-fit-coupon`, then
  `solidcraft-cli run .git/coupon-script.json --quiet`. Expected: exit 0, and
  `models/dowel-fit-coupon/dowel-fit-coupon.sc` is a few KB of JSON.
- [x] **Step 4: Write its page's text.**

`models/dowel-fit-coupon/model.yml`:

```yaml
title: Dowel fit-test coupon
summary: >-
  One bar with four holes, each a little wider than the dowel, to find the clearance your printer
  and your dowel need before printing a part that holds one.
status: designed
material: PETG, or what the dowel parts will be printed in
size: 1 in
sizes:
  3/4 in: {dowel_d: 19.05 mm}
  25 mm: {dowel_d: 25 mm}
print:
  Orientation: standing on its long edge, the holes horizontal, as the sockets print
  Layer height: 0.2 mm
  Walls: 3
  Infill: 15%
  Supports: none, not even inside the holes
notes: |
  Dowels sold as one size vary by about half a millimetre, and printers print holes a little
  small, so the hole a dowel needs is found by trying it. Print the coupon for your dowel's size,
  standing on its edge: the dowel parts' sockets print with their holes horizontal, and a
  horizontal hole comes out a little smaller and less round than a vertical one. The dots beside
  each hole say how much wider than the dowel it is:

  | Dots | Clearance | For a 1-inch dowel |
  |---|---|---|
  | 1 | +0.2 mm | 25.6 mm |
  | 2 | +0.4 mm | 25.8 mm |
  | 3 | +0.6 mm | 26.0 mm |
  | 4 | +0.8 mm | 26.2 mm |

  Push the dowel into each hole. The one to use is the tightest it goes into by hand, all the way,
  without a mallet; it should hold the coupon up when you lift the dowel. Set each dowel part's
  `clearance` to that hole's: `step` times its dots. If even four dots is too tight, change `step`
  to 0.3 mm and print it again.
```

  Then `make models`. Expected: `building models/dowel-fit-coupon (missing …)` and `1 built`. Look at
  `dowel-fit-coupon.png` against the design's description in its notes.
- [x] **Step 5: Run the checks; they pass.** `make check`. Expected: every test passes twice,
  every model's build matches its design, the privacy check is clean over the new files, and the
  render lists the model's page.
- [x] **Step 6: Commit.** Write the message to `.git/COMMIT_MSG`:

```text
feat(models): 🤖 add the dowel fit-test coupon

The dowel parts need the clearance that suits a printer and its dowel,
and dowels sold as one size vary by about half a millimetre. The coupon is
one bar with four holes at the dowel plus 0.2, 0.4, 0.6 and 0.8 mm, marked
by one to four dots, every size a parameter, in STLs for 3/4 inch, 25 mm
and 1 inch. It prints on its edge, the holes horizontal, as the sockets
print. Built headless by solidcraft-cli from a command script, saved as
plain-text JSON, with its STLs, picture, measurements and record from make
models; its page says how to read the result.

The new tests failed first with: FileNotFoundError for
models/dowel-fit-coupon/dowel-fit-coupon.eval.json.

Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-1.md Task 6
Co-Authored-By: <the model's own line>
```

  `git add models/dowel-fit-coupon/dowel-fit-coupon.sc models/dowel-fit-coupon/dowel-fit-coupon.stl models/dowel-fit-coupon/dowel-fit-coupon-3-4in.stl models/dowel-fit-coupon/dowel-fit-coupon-25mm.stl models/dowel-fit-coupon/dowel-fit-coupon.png models/dowel-fit-coupon/dowel-fit-coupon.eval.json models/dowel-fit-coupon/build.json models/dowel-fit-coupon/model.yml tests/test_coupon.py`, then `git commit -F .git/COMMIT_MSG`, then `git log -1 --format='%(trailers)'` shows the `Plan:` line.
- [x] **Step 7: Review, look forward, close.** The review looks at the picture and the page's
  viewer, not the `.sc` alone. Tier 1 (the first real `solidcraft-cli` output in the repo): before staging, `make privacy` passes over the new files, and the picture is looked at.

  - **Review (Tier 1: Matt Pocock's `code-review`, two axes in two subagents, plus the security checklist, one line per item; at most one re-review),** from `$(cat .git/TASK_BASE)`.
  - **Forward:** Phase 2's first task prints this coupon; Task 7's `clearance` test reads its `step`.
  - **Docs:** the README's first-project lines; the overview diagram needs no change.
  - **Close,** its own commit: this task's boxes ticked, **Now** set to the next task, any
    Built differently and Ruling lines, deferred findings on the phase-end list, the spec's
    scenario statuses (`built`). The message, from `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 6: The dowel fit-test coupon

    <what the task built, and why, in a few lines>

    Drift: <filled at the close, or none>
    Rulings: <filled at the close, or none>
    Phase-end: <filled at the close, or none>
    Forward: <filled at the close, or none>
    Tier: 1
    Rounds: <filled at the close>
    Findings: <filled at the close, or none>

    Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-1.md Task 6
    Co-Authored-By: <the model's own line>
    ```

  - **Push,** once Dan has OKed it, the request naming every binary file the push adds
    (`AGENTS.md`'s interim line): `make leaks privacy`, then `git push origin phase-1`.
    The task is closed once CI on the closing commit, or a later one, is green; until a
    push, the local checks are the gate.

***

### Task 7: The sconce's wall block

**Tier:** 2 · **Scenarios:** S12, S19

**Files:**
- Create: `models/sconce-wall-block/sconce-wall-block.sc` (by SolidCraft), its built files (`.stl`, `-3-4in.stl`,
  `-25mm.stl`, `.png`, `.eval.json`, `build.json`, by `make models`), `models/sconce-wall-block/model.yml`,
  `tests/test_wall_block.py`

**Interfaces:**
- Consumes: Task 2's `make models`, `Model`, `sizes` and the conftest helpers; Task 5's
  `read_meta` and the page.
- Produces: the design's parameters `dowel_d`, `clearance`, `socket_depth` (54 mm), `boss_wall`, `plate_t`, `plate_w`, `screw_spacing` (110 mm), `plate_h`, `screw_d`, `head_d`, `head_depth`, `cap_h`, `bolt_d`, `socket_d`, `boss_d`; the bodies `Wall block`, `Cap 1` and `Cap 2`.

- [x] **Step 0: Record the base:** `git rev-parse HEAD > .git/TASK_BASE`.
- [x] **Step 1: Write the failing tests.**

`tests/test_wall_block.py`:

```python
"""The sconce's wall block (S12): a deep socket, screws far apart and hidden, the coupon's fit."""

from __future__ import annotations

from pathlib import Path

import pytest

import models
from conftest import body, params

MODELS = Path(__file__).resolve().parent.parent / "models"
WALL_BLOCK = models.Model(MODELS / "sconce-wall-block")
COUPON = models.Model(MODELS / "dowel-fit-coupon")
SCREW_HEAD_MM = 3.0  # a #8 or #10 pan or washer head, and a toggle bolt's


def test_the_block_is_one_closed_body_with_two_caps_beside_it() -> None:
    assert body(WALL_BLOCK, "Wall block")["closed"]
    assert body(WALL_BLOCK, "Cap 1")["closed"] and body(WALL_BLOCK, "Cap 2")["closed"]


def test_it_is_saved_for_one_inch_and_comes_in_three_sizes() -> None:
    assert params(WALL_BLOCK)["dowel_d"] == pytest.approx(25.4)
    assert set(models.sizes(WALL_BLOCK)) == {"3/4 in", "25 mm"}


def test_the_socket_is_at_least_two_inches_deep() -> None:
    assert params(WALL_BLOCK)["socket_depth"] >= 51.0


def test_the_screws_are_at_least_100_mm_apart() -> None:
    p = params(WALL_BLOCK)
    assert p["screw_spacing"] >= 100.0
    assert p["plate_h"] > p["screw_spacing"] + p["head_d"]


def test_each_screw_head_sinks_below_the_face_with_room_for_its_cap() -> None:
    p, cap = params(WALL_BLOCK), body(WALL_BLOCK, "Cap 1")["bbox"]
    assert p["head_depth"] >= SCREW_HEAD_MM + p["cap_h"]
    assert p["head_depth"] < p["plate_t"]
    assert cap["max"][2] - cap["min"][2] == pytest.approx(p["cap_h"])


def test_the_socket_takes_one_of_the_coupons_clearances() -> None:
    p, step = params(WALL_BLOCK), params(COUPON)["step"]
    assert p["socket_d"] == pytest.approx(p["dowel_d"] + p["clearance"])
    assert any(p["clearance"] == pytest.approx(k * step) for k in (1, 2, 3, 4))


def test_the_block_reaches_its_socket_depth_out_from_the_wall() -> None:
    p, bbox = params(WALL_BLOCK), body(WALL_BLOCK, "Wall block")["bbox"]
    assert bbox["max"][0] - bbox["min"][0] == pytest.approx(p["plate_t"] + p["socket_depth"])
```

- [x] **Step 2: Run them; watch them fail.** `make test`. Expected: `FileNotFoundError` for
  `models/sconce-wall-block/sconce-wall-block.eval.json`.
- [x] **Step 3: Build the design.** Write SolidCraft's command script to `.git/wall-block-script.json`
  (it stays out of the repo: the saved design holds the same feature tree, and
  `solidcraft-cli script` regenerates it):

```json
{
  "commands": [
    {
      "command": "parameters.add",
      "params": {
        "name": "dowel_d",
        "expression": "25.4 mm",
        "comment": "the arm's dowel: 1 inch as saved; the page offers 3/4 in and 25 mm"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "clearance",
        "expression": "0.4 mm",
        "comment": "added to the dowel for the socket: the coupon's hole that fit"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "socket_depth",
        "expression": "54 mm",
        "comment": "at least 51 mm (2 inches), so the joint carries the arm's moment"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "boss_wall",
        "expression": "6 mm",
        "comment": "plastic around the socket"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "plate_t",
        "expression": "10 mm",
        "comment": "the wall plate's thickness, behind the socket"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "plate_w",
        "expression": "50 mm",
        "comment": "the wall plate's width"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "screw_spacing",
        "expression": "110 mm",
        "comment": "at least 100 mm between the screws, so the top one pulls under 54 N"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "plate_h",
        "expression": "screw_spacing + 30 mm",
        "comment": "the wall plate's height"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "screw_d",
        "expression": "5 mm",
        "comment": "fits #8 and #10 wood screws and 3/16 in toggle bolts; 6.6 mm for 1/4 in"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "head_d",
        "expression": "10.5 mm",
        "comment": "the counterbore that sinks each screw's head below the face"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "head_depth",
        "expression": "5 mm",
        "comment": "the counterbore's depth: a screw head, then a cap"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "cap_h",
        "expression": "2 mm",
        "comment": "a printed cap's height, pressed in over the screw head"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "bolt_d",
        "expression": "6.6 mm",
        "comment": "clearance for an M6 bolt through the boss and the dowel"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "socket_d",
        "expression": "dowel_d + clearance",
        "comment": "the socket's diameter"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "boss_d",
        "expression": "socket_d + 2 * boss_wall",
        "comment": "the boss around the socket"
      }
    },
    {
      "command": "solid.box",
      "params": {
        "length": "plate_t",
        "width": "plate_w",
        "height": "plate_h",
        "corner": [
          0,
          "-plate_w / 2",
          "-plate_h / 2"
        ],
        "body_name": "Wall block"
      }
    },
    {
      "command": "solid.cylinder",
      "params": {
        "diameter": "boss_d",
        "height": "plate_t + socket_depth",
        "base": [
          0,
          0,
          0
        ],
        "axis": "X",
        "body_name": "Boss"
      }
    },
    {
      "command": "solid.combine",
      "params": {
        "target": "Wall block",
        "tools": [
          "Boss"
        ],
        "operation": "join"
      }
    },
    {
      "command": "solid.cylinder",
      "params": {
        "diameter": "socket_d",
        "height": "socket_depth",
        "base": [
          "plate_t",
          0,
          0
        ],
        "axis": "X",
        "body_name": "Socket"
      }
    },
    {
      "command": "solid.cylinder",
      "params": {
        "diameter": "bolt_d",
        "height": "boss_d + 2 mm",
        "base": [
          "plate_t + socket_depth / 2",
          0,
          "-boss_d / 2 - 1 mm"
        ],
        "axis": "Z",
        "body_name": "Bolt hole"
      }
    },
    {
      "command": "solid.cylinder",
      "params": {
        "diameter": "screw_d",
        "height": "plate_t",
        "base": [
          0,
          0,
          "screw_spacing / 2"
        ],
        "axis": "X",
        "body_name": "Top screw"
      }
    },
    {
      "command": "solid.cylinder",
      "params": {
        "diameter": "head_d",
        "height": "head_depth",
        "base": [
          "plate_t - head_depth",
          0,
          "screw_spacing / 2"
        ],
        "axis": "X",
        "body_name": "Top counterbore"
      }
    },
    {
      "command": "solid.cylinder",
      "params": {
        "diameter": "screw_d",
        "height": "plate_t",
        "base": [
          0,
          0,
          "-screw_spacing / 2"
        ],
        "axis": "X",
        "body_name": "Bottom screw"
      }
    },
    {
      "command": "solid.cylinder",
      "params": {
        "diameter": "head_d",
        "height": "head_depth",
        "base": [
          "plate_t - head_depth",
          0,
          "-screw_spacing / 2"
        ],
        "axis": "X",
        "body_name": "Bottom counterbore"
      }
    },
    {
      "command": "solid.combine",
      "params": {
        "target": "Wall block",
        "tools": [
          "Socket",
          "Bolt hole",
          "Top screw",
          "Top counterbore",
          "Bottom screw",
          "Bottom counterbore"
        ],
        "operation": "cut"
      }
    },
    {
      "command": "solid.cylinder",
      "params": {
        "diameter": "head_d - 0.2 mm",
        "height": "cap_h",
        "base": [
          0,
          "plate_w / 2 + 10 mm",
          "-plate_h / 2"
        ],
        "axis": "Z",
        "body_name": "Cap 1"
      }
    },
    {
      "command": "solid.cylinder",
      "params": {
        "diameter": "head_d - 0.2 mm",
        "height": "cap_h",
        "base": [
          0,
          "plate_w / 2 + 25 mm",
          "-plate_h / 2"
        ],
        "axis": "Z",
        "body_name": "Cap 2"
      }
    },
    {
      "command": "file.save_as",
      "params": {
        "path": "models/sconce-wall-block/sconce-wall-block.sc",
        "format": "json",
        "cache": false
      }
    }
  ]
}
```

  From the repo's root: `mkdir -p models/sconce-wall-block`, then
  `solidcraft-cli run .git/wall-block-script.json --quiet`. Expected: exit 0, and
  `models/sconce-wall-block/sconce-wall-block.sc` is a few KB of JSON.
- [x] **Step 4: Write its page's text.**

`models/sconce-wall-block/model.yml`:

```yaml
title: Sconce wall block
summary: >-
  The wall end of a grow-light sconce: a plate for two hidden screws and a deep socket that holds
  a dowel straight out from the wall, bolted through.
status: designed
material: PETG, matte (never PLA for this part)
size: 1 in
sizes:
  3/4 in: {dowel_d: 19.05 mm}
  25 mm: {dowel_d: 25 mm}
print:
  Orientation: on its side, a long edge of the plate on the bed, so the layers run along the socket
  Layer height: 0.2 mm
  Walls: 5
  Infill: 40% gyroid
  Supports: under the boss, along its length, from the bed only
notes: |
  The arm is a straight cantilever: a dowel up to 20 inches long, with the light hanging near its
  end. The socket is 54 mm deep, more than the 51 mm (2 inches) the joint needs to carry the arm's
  bending moment: about 5 N·m with a 1 kg light at 20 inches on a 1-inch dowel.

  - **Screws:** two, 110 mm apart: #8 or #10 wood screws into a stud, or 3/16-inch toggle bolts
    in drywall, never plastic plugs, since the top screw is pulled out with about 54 N. For
    1/4-inch toggles, set `screw_d` to 6.6 mm. Each head sinks into a counterbore, and one of the
    two printed caps beside the block presses in over it.
  - **Bolt:** an M6 × 50 mm bolt and a nylon-insert nut, down through the boss and a hole drilled
    through the seated dowel, so it can't pull out or turn.
  - **Clearance:** the socket is the dowel plus `clearance`, from the fit-test coupon.

  This is a first design, not yet printed or load-tested; its page will say when it has been.
```

  Then `make models`. Expected: `building models/sconce-wall-block (missing …)` and `1 built`. Look at
  `sconce-wall-block.png` against the design's description in its notes.
- [x] **Step 5: Run the checks; they pass.** `make check`. Expected: every test passes twice,
  every model's build matches its design, the privacy check is clean over the new files, and the
  render lists the model's page.
- [x] **Step 6: Commit.** Write the message to `.git/COMMIT_MSG`:

```text
feat(models): 🤖 add the sconce's wall block

The sconce's arm needs a wall joint that carries about 5 N·m (Q&A
answer 12 puts the dowel parts in the repo now). The wall block is a plate
for two screws 110 mm apart, their heads sunk into counterbores under
printed caps, and a boss with a 54 mm socket, deeper than the 2 inches the
joint needs, sized to the dowel plus the coupon's clearance, with a hole
for an M6 bolt through the dowel. Saved at 1 inch, with STLs for 3/4 inch
and 25 mm. The tests hold the socket's depth, the screws' spacing, the
counterbores and the clearance to the spec.

The new tests failed first with: FileNotFoundError for
models/sconce-wall-block/sconce-wall-block.eval.json.

Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-1.md Task 7
Co-Authored-By: <the model's own line>
```

  `git add models/sconce-wall-block/sconce-wall-block.sc models/sconce-wall-block/sconce-wall-block.stl models/sconce-wall-block/sconce-wall-block-3-4in.stl models/sconce-wall-block/sconce-wall-block-25mm.stl models/sconce-wall-block/sconce-wall-block.png models/sconce-wall-block/sconce-wall-block.eval.json models/sconce-wall-block/build.json models/sconce-wall-block/model.yml tests/test_wall_block.py`, then `git commit -F .git/COMMIT_MSG`, then `git log -1 --format='%(trailers)'` shows the `Plan:` line.
- [x] **Step 7: Review, look forward, close.** The review looks at the picture and the page's
  viewer, not the `.sc` alone.

  - **Review (Tier 2: Matt Pocock's `code-review`, two axes in two subagents; fix Critical and Important; at most one re-review),** from `$(cat .git/TASK_BASE)`.
  - **Forward:** Phase 2's second task sets `clearance` and `screw_d` from Dan's answers.
  - **Docs:** the README's first-project lines; the overview diagram needs no change.
  - **Close,** its own commit: this task's boxes ticked, **Now** set to the next task, any
    Built differently and Ruling lines, deferred findings on the phase-end list, the spec's
    scenario statuses (`built`). The message, from `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 7: The sconce's wall block

    <what the task built, and why, in a few lines>

    Drift: <filled at the close, or none>
    Rulings: <filled at the close, or none>
    Phase-end: <filled at the close, or none>
    Forward: <filled at the close, or none>
    Tier: 2
    Rounds: <filled at the close>
    Findings: <filled at the close, or none>

    Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-1.md Task 7
    Co-Authored-By: <the model's own line>
    ```

  - **Push,** once Dan has OKed it, the request naming every binary file the push adds
    (`AGENTS.md`'s interim line): `make leaks privacy`, then `git push origin phase-1`.
    The task is closed once CI on the closing commit, or a later one, is green; until a
    push, the local checks are the gate.

***

### Task 8: The sconce's cord clamp

**Tier:** 2 · **Scenarios:** S18, S19

**Files:**
- Create: `models/sconce-cord-clamp/sconce-cord-clamp.sc` (by SolidCraft), its built files (`.stl`, `-3-4in.stl`,
  `-25mm.stl`, `.png`, `.eval.json`, `build.json`, by `make models`), `models/sconce-cord-clamp/model.yml`,
  `tests/test_cord_clamp.py`

**Interfaces:**
- Consumes: Task 2's `make models`, `Model`, `sizes` and the conftest helpers; Task 5's
  `read_meta` and the page.
- Produces: the design's parameters `dowel_d`, `clearance` (0.2 mm), `ring_wall`, `ring_len`, `split`, `ear_t`, `ear_len`, `bolt_d` (M4), `cord_d`, `under_gap` (`cord_d + 4 mm`), `grip_d` (`cord_d - 0.6 mm`), `slot_w` (`cord_d - 1.5 mm`), `shelf_len`, `shelf_w`, `shelf_t`, `web_w`, `bore_d`, `ring_d`, `shelf_top`; the body `Cord clamp`.

- [x] **Step 0: Record the base:** `git rev-parse HEAD > .git/TASK_BASE`.
- [x] **Step 1: Write the failing tests.**

`tests/test_cord_clamp.py`:

```python
"""The sconce's cord clamp (S18): it grips the dowel and the cord, and leaves the cord a way in."""

from __future__ import annotations

from pathlib import Path

import pytest

import models
from conftest import body, params

MODELS = Path(__file__).resolve().parent.parent / "models"
CORD_CLAMP = models.Model(MODELS / "sconce-cord-clamp")
WALL_BLOCK = models.Model(MODELS / "sconce-wall-block")


def test_it_is_one_closed_body() -> None:
    assert body(CORD_CLAMP, "Cord clamp")["closed"]


def test_it_fits_the_same_dowel_as_the_wall_block_in_the_same_sizes() -> None:
    assert params(CORD_CLAMP)["dowel_d"] == pytest.approx(params(WALL_BLOCK)["dowel_d"])
    assert models.sizes(CORD_CLAMP) == models.sizes(WALL_BLOCK)


def test_the_slot_and_the_hole_are_narrower_than_the_cord_so_it_grips() -> None:
    p = params(CORD_CLAMP)
    assert p["slot_w"] < p["grip_d"] < p["cord_d"]


def test_the_cord_has_room_to_pass_under_the_dowel_to_its_hole() -> None:
    p = params(CORD_CLAMP)
    assert p["under_gap"] >= p["cord_d"] + 2


def test_the_shelf_hangs_its_gap_and_thickness_below_the_dowel() -> None:
    p = params(CORD_CLAMP)
    lowest = body(CORD_CLAMP, "Cord clamp")["bbox"]["min"][2]
    assert lowest == pytest.approx(-(p["dowel_d"] / 2 + p["under_gap"] + p["shelf_t"]))
```

- [x] **Step 2: Run them; watch them fail.** `make test`. Expected: `FileNotFoundError` for
  `models/sconce-cord-clamp/sconce-cord-clamp.eval.json`.
- [x] **Step 3: Build the design.** Write SolidCraft's command script to `.git/cord-clamp-script.json`
  (it stays out of the repo: the saved design holds the same feature tree, and
  `solidcraft-cli script` regenerates it):

```json
{
  "commands": [
    {
      "command": "parameters.add",
      "params": {
        "name": "dowel_d",
        "expression": "25.4 mm",
        "comment": "the arm's dowel: 1 inch as saved; the page offers 3/4 in and 25 mm"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "clearance",
        "expression": "0.2 mm",
        "comment": "a snug slide; the bolt closes the split to grip"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "ring_wall",
        "expression": "5 mm",
        "comment": "plastic around the dowel"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "ring_len",
        "expression": "20 mm",
        "comment": "the ring's length along the dowel"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "split",
        "expression": "3 mm",
        "comment": "the gap the bolt closes"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "ear_t",
        "expression": "6 mm",
        "comment": "each clamping ear's thickness"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "ear_len",
        "expression": "11 mm",
        "comment": "how far the ears stand out from the ring, on its side"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "bolt_d",
        "expression": "4.4 mm",
        "comment": "clearance for an M4 bolt"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "cord_d",
        "expression": "6 mm",
        "comment": "the light's cord, measured: 6 mm is a guess until it is"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "under_gap",
        "expression": "cord_d + 4 mm",
        "comment": "room under the dowel for the cord to reach the hole"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "grip_d",
        "expression": "cord_d - 0.6 mm",
        "comment": "the hole the cord hangs from: a little tight, so it grips"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "slot_w",
        "expression": "cord_d - 1.5 mm",
        "comment": "the slot the cord is pressed in through: tighter still"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "shelf_len",
        "expression": "18 mm",
        "comment": "how far the cord shelf reaches beyond the ring"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "shelf_w",
        "expression": "18 mm",
        "comment": "the cord shelf's width"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "shelf_t",
        "expression": "8 mm",
        "comment": "the cord shelf's thickness"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "web_w",
        "expression": "8 mm",
        "comment": "the web joining the ring to the shelf"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "bore_d",
        "expression": "dowel_d + clearance",
        "comment": "the ring's bore"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "ring_d",
        "expression": "bore_d + 2 * ring_wall",
        "comment": "the ring's outside diameter"
      }
    },
    {
      "command": "parameters.add",
      "params": {
        "name": "shelf_top",
        "expression": "-dowel_d / 2 - under_gap",
        "comment": "the shelf's top face, below the dowel's axis"
      }
    },
    {
      "command": "solid.cylinder",
      "params": {
        "diameter": "ring_d",
        "height": "ring_len",
        "base": [
          0,
          0,
          0
        ],
        "axis": "X",
        "body_name": "Cord clamp"
      }
    },
    {
      "command": "solid.box",
      "params": {
        "length": "ring_len",
        "width": "ring_d / 2 + ear_len - bore_d / 2",
        "height": "split + 2 * ear_t",
        "corner": [
          0,
          "bore_d / 2",
          "-split / 2 - ear_t"
        ],
        "body_name": "Ears"
      }
    },
    {
      "command": "solid.box",
      "params": {
        "length": "ring_len",
        "width": "web_w",
        "height": "-bore_d / 2 - 1 mm - shelf_top",
        "corner": [
          0,
          "-web_w / 2",
          "shelf_top"
        ],
        "body_name": "Web"
      }
    },
    {
      "command": "solid.box",
      "params": {
        "length": "ring_len + shelf_len",
        "width": "shelf_w",
        "height": "shelf_t",
        "corner": [
          0,
          "-shelf_w / 2",
          "shelf_top - shelf_t"
        ],
        "body_name": "Shelf"
      }
    },
    {
      "command": "solid.combine",
      "params": {
        "target": "Cord clamp",
        "tools": [
          "Ears",
          "Web",
          "Shelf"
        ],
        "operation": "join"
      }
    },
    {
      "command": "solid.cylinder",
      "params": {
        "diameter": "bore_d",
        "height": "ring_len + 2 mm",
        "base": [
          "-1 mm",
          0,
          0
        ],
        "axis": "X",
        "body_name": "Bore"
      }
    },
    {
      "command": "solid.box",
      "params": {
        "length": "ring_len + 2 mm",
        "width": "ring_d / 2 + ear_len + 1 mm",
        "height": "split",
        "corner": [
          "-1 mm",
          0,
          "-split / 2"
        ],
        "body_name": "Split"
      }
    },
    {
      "command": "solid.cylinder",
      "params": {
        "diameter": "bolt_d",
        "height": "split + 2 * ear_t + 2 mm",
        "base": [
          "ring_len / 2",
          "ring_d / 2 + ear_len / 2 - 0.5 mm",
          "-split / 2 - ear_t - 1 mm"
        ],
        "axis": "Z",
        "body_name": "Bolt hole"
      }
    },
    {
      "command": "solid.cylinder",
      "params": {
        "diameter": "grip_d",
        "height": "shelf_t + 2 mm",
        "base": [
          "ring_len + shelf_len / 2",
          0,
          "shelf_top - shelf_t - 1 mm"
        ],
        "axis": "Z",
        "body_name": "Cord hole"
      }
    },
    {
      "command": "solid.box",
      "params": {
        "length": "slot_w",
        "width": "shelf_w / 2 + 1 mm",
        "height": "shelf_t + 2 mm",
        "corner": [
          "ring_len + shelf_len / 2 - slot_w / 2",
          0,
          "shelf_top - shelf_t - 1 mm"
        ],
        "body_name": "Cord slot"
      }
    },
    {
      "command": "solid.combine",
      "params": {
        "target": "Cord clamp",
        "tools": [
          "Bore",
          "Split",
          "Bolt hole",
          "Cord hole",
          "Cord slot"
        ],
        "operation": "cut"
      }
    },
    {
      "command": "file.save_as",
      "params": {
        "path": "models/sconce-cord-clamp/sconce-cord-clamp.sc",
        "format": "json",
        "cache": false
      }
    }
  ]
}
```

  From the repo's root: `mkdir -p models/sconce-cord-clamp`, then
  `solidcraft-cli run .git/cord-clamp-script.json --quiet`. Expected: exit 0, and
  `models/sconce-cord-clamp/sconce-cord-clamp.sc` is a few KB of JSON.
- [x] **Step 4: Write its page's text.**

`models/sconce-cord-clamp/model.yml`:

```yaml
title: Sconce cord clamp
summary: >-
  Clamps anywhere along a dowel and holds a pendant light's cord, so the light hangs straight
  below the arm at the height you set.
status: designed
material: PETG, matte
size: 1 in
sizes:
  3/4 in: {dowel_d: 19.05 mm}
  25 mm: {dowel_d: 25 mm}
print:
  Orientation: the shelf flat on the bed, the ring above it
  Layer height: 0.2 mm
  Walls: 4
  Infill: 30%
  Supports: under the ring, from the bed only
notes: |
  Slide the clamp onto the dowel, ears to the side you see least, set it where the light should
  hang, and close the split with an M4 × 30 mm bolt and nut through the ears.

  The light's cord comes along the top of the arm, down the side of the dowel and through the gap
  under it, then presses in through the slot in the shelf and hangs from the round hole beyond it,
  straight below the dowel, so the light's weight can't turn the clamp. The slot is 1.5 mm
  narrower than the cord and the hole 0.6 mm narrower, so the cord grips; pull it through to set
  the light's height. Ease the hole's edges with a countersink bit, so a swinging light doesn't
  wear the cord.

  `cord_d` is the cord's diameter: measure yours and set it before printing; 6 mm is a guess.
  For a flat two-wire cord, the hole and slot need reshaping, not just resizing.

  This is a first design, not yet printed; its page will say when it has been.
```

  Then `make models`. Expected: `building models/sconce-cord-clamp (missing …)` and `1 built`. Look at
  `sconce-cord-clamp.png` against the design's description in its notes.
- [x] **Step 5: Run the checks; they pass.** `make check`. Expected: every test passes twice,
  every model's build matches its design, the privacy check is clean over the new files, and the
  render lists the model's page.
- [x] **Step 6: Commit.** Write the message to `.git/COMMIT_MSG`:

```text
feat(models): 🤖 add the sconce's cord clamp

Dan asked for a printed joint that clamps onto the dowel and holds the
grow light's cord with the light at its end (Q&A answer 11). The clamp is
a split ring closed by an M4 bolt through two ears on its side, so it
holds anywhere along the arm and keeps its top clear for the cord. A web
drops to a shelf a cord's width below the dowel: the cord comes under the
dowel, presses in through a slot 1.5 mm narrower than itself, and hangs
from a hole 0.6 mm narrower, straight below the dowel's axis, so it grips
and the light can't turn the clamp. cord_d is a guess until Dan measures
the cord. Saved at 1 inch, with STLs for 3/4 inch and 25 mm.

The new tests failed first with: FileNotFoundError for
models/sconce-cord-clamp/sconce-cord-clamp.eval.json.

Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-1.md Task 8
Co-Authored-By: <the model's own line>
```

  `git add models/sconce-cord-clamp/sconce-cord-clamp.sc models/sconce-cord-clamp/sconce-cord-clamp.stl models/sconce-cord-clamp/sconce-cord-clamp-3-4in.stl models/sconce-cord-clamp/sconce-cord-clamp-25mm.stl models/sconce-cord-clamp/sconce-cord-clamp.png models/sconce-cord-clamp/sconce-cord-clamp.eval.json models/sconce-cord-clamp/build.json models/sconce-cord-clamp/model.yml tests/test_cord_clamp.py`, then `git commit -F .git/COMMIT_MSG`, then `git log -1 --format='%(trailers)'` shows the `Plan:` line.
- [x] **Step 7: Review, look forward, close.** The review looks at the picture and the page's
  viewer, not the `.sc` alone.

  - **Review (Tier 2: Matt Pocock's `code-review`, two axes in two subagents; fix Critical and Important; at most one re-review),** from `$(cat .git/TASK_BASE)`.
  - **Forward:** Phase 2's second task sets `cord_d` from Dan's measurement.
  - **Docs:** the README's first-project lines; the overview diagram needs no change.
  - **Close,** its own commit: this task's boxes ticked, **Now** set to the next task, any
    Built differently and Ruling lines, deferred findings on the phase-end list, the spec's
    scenario statuses (`built`). The message, from `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 8: The sconce's cord clamp

    <what the task built, and why, in a few lines>

    Drift: <filled at the close, or none>
    Rulings: <filled at the close, or none>
    Phase-end: <filled at the close, or none>
    Forward: <filled at the close, or none>
    Tier: 2
    Rounds: <filled at the close>
    Findings: <filled at the close, or none>

    Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-1.md Task 8
    Co-Authored-By: <the model's own line>
    ```

  - **Push,** once Dan has OKed it, the request naming every binary file the push adds
    (`AGENTS.md`'s interim line): `make leaks privacy`, then `git push origin phase-1`.
    The task is closed once CI on the closing commit, or a later one, is green; until a
    push, the local checks are the gate.

***

### Task 9: [Dan] The GitHub settings

**Tier:** none: settings Dan applies on github.com, which never relax (`AGENTS.md`, *Stops*) ·
**Scenarios:** S10

Runs on <https://github.com/chendaniely/3d-models/settings>, by Dan, one step at a time, asked by
*Asking Dan*. **Now** reads `waiting on Dan: <the step>` until each is done. The agent runs the
security checklist over these settings, one line each, in the close.

- [x] **1. Pages:** Settings → Pages → Source: "GitHub Actions"; then Settings → Environments →
  `github-pages` → deployment branches: `main` only.
- [x] **2. Actions:** Settings → Actions → General: workflow permissions "Read repository
  contents"; allow only GitHub's own actions and these: `astral-sh/setup-uv`,
  `quarto-dev/quarto-actions/setup`; require actions pinned to a full commit SHA, where offered.
- [x] **3. Merge commits only:** Settings → General → Pull Requests: allow merge commits, its
  message the PR title and description; squash and rebase merging off.
- [x] **4. A ruleset on `main`:** Settings → Rules → Rulesets → New branch ruleset, target the
  default branch: require a pull request; require the status checks `tests`, `leaks` and `site`;
  block force pushes and deletion; bypass list "For pull requests only" (so the agent's pushes,
  made with Dan's login, aren't exempt). Classic branch protection instead, if rulesets aren't
  offered.
- [x] **5. The website field and topics:** the agent drafts
  `gh repo edit --homepage https://chendaniely.github.io/3d-models/ --add-topic 3d-printing
  --add-topic solidcraft --add-topic vibe-coded`; Dan runs it, or says the agent may.
- [x] **6. Close:** the agent ticks these boxes and sets **Now** to the phase end, in
  `docs(plan): 🤖 close Task 9: The GitHub settings` (every heading `none` but `Rulings:`, which
  names anything Dan chose differently, and `Rounds:`, the checklist), with this plan's `Plan:`
  line.

***

### Task 10: Phase end

Each step is one box; each ends with its commit (`docs(plan): 🤖 phase end step K: <what it
did>`, with `Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-1.md Phase end`), which ticks its box and sets **Now** to
`Phase end, step K+1: <title>.` Resume at the first unticked box; never re-run a ticked one.

- [ ] **1. The final whole-branch review:** Matt Pocock's two-axis `code-review` from
  `git merge-base main HEAD`; one fix dispatch, then one scoped re-review; a ruling on what's left.
  Each fix is its own commit.
- [ ] **2. The rest of the ledger copied into the plan:** whatever
  `.superpowers/sdd/2026-11-05-3d-models-phase-1/progress.md` holds that no closing commit
  carries, under its task.
- [ ] **3. The phase-end council:** four read-only reviewers (goal fit and scenarios,
  reliability, security, simplicity) on the whole branch; their reports committed first in
  `docs/superpowers/plans/2026-11-05-3d-models-phase-1-end-council.md`, with its Design-page line
  and nothing that quotes Quarto's syntax; each claim checked; each finding a severity and a
  decision.
- [ ] **4. The phase-end list worked through:** each item fixed in its own commit at its tier, or
  moved to the spec's Later with a reason; missing docs written; built parts solid in the diagrams.
- [ ] **5. The forward look:** Phase 2's plan rewritten to fit what was built; its listings run
  against this code where they can.
- [ ] **6. The retro:** `docs/superpowers/plans/2026-11-05-3d-models-phase-1-retro.md` (departures,
  items carried forward, metrics per tier, starting over), with its Design-page line; the retuning
  rules applied to Phase 2's tiers.
- [ ] **7. The changelog and status:** a dated `CHANGELOG.md` entry; the README's status line says
  the gallery is live; the spec's status line `Phase 1 PR open (#N)`, N filled once step 8 opens
  it.
- [ ] **8. The PR:** title `chore(repo): 🤖 merge Phase 1: the repo and the first models`; the
  body summarizes each task, the council's findings and their fate, links the retro, lists every
  file no scan can read (`git log --format= --numstat origin/main..HEAD | awk '$1 == "-" { print
  "not scanned, check by eye: " $3 }'`), and ends `Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-1.md Phase end`. Title and body in
  `.git/PR_TITLE` and `.git/PR_BODY.md`, scanned with `gitleaks stdin --redact --no-banner` before
  `gh pr create --base main --head phase-1 --title "$(cat .git/PR_TITLE)" --body-file
  .git/PR_BODY.md`. Fully vibed, the agent merges it once CI is green, with
  `gh pr merge <N> --merge --match-head-commit <sha>` and the subject
  `chore(repo): 🤖 merge Phase 1: the repo and the first models (#N)`, never `--admin`, squash,
  rebase or `--delete-branch`; but the PR adds STL and PNG files no scan can read, so it waits for
  Dan's look at them first (`AGENTS.md`, *Stops*). Ruling: Dan looked at and OKed each binary file
  by name when it was pushed (Phase 1 Q&A 2 and 3), so that wait is met for Phase 1; a phase-end
  step that adds a new binary would need his look again.
- [ ] **9. After the merge:** each model's page on <https://chendaniely.github.io/3d-models/>
  serves its sizes, and its viewer loads (S08, S10).

***

## Phase-end list

| Source | Severity | File | Item | Status |
|---|---|---|---|---|
| kickoff council, simplicity 7 | Minor | `website/_diagram-zoom.html` | kept as the skill's standard site kit; drop it if it never earns its 50 lines | open |
| kickoff council, reliability 9 | Minor | `Makefile` | lychee isn't installed on Dan's machine, so `make docs` skips it locally and only CI runs it; installing it is Dan's call | open |
| Task 6, Spec review | Minor | `models/dowel-fit-coupon/model.yml` | the STL lies flat as modelled; the page could say to stand it on its edge in the slicer, not only that it prints that way | open |
