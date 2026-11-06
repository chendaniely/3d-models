# 3d-models Phase 1: the repo, implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking. The project's `AGENTS.md` holds every rule for running
> it (the task loop, reviews, stops, commits, pushing) and outranks this header where they differ.

**Goal:** the pipeline from a SolidCraft design to a gallery page with a 3D viewer, guarded by CI,
with the dowel fit-test coupon as its first model.

**Architecture:** designs are plain-text `.sc` files under `models/<slug>/`; `scripts/models.py`
builds each changed one with `solidcraft-cli` and judges freshness by the design's SHA-256;
`scripts/photos.py` keeps GPS data out; `scripts/gallery.py` writes a Quarto page per model, which
`website/assets/stl-viewer.js` turns into a 3D view with three.js. CI runs every check on each push
and deploys the site from `main`.

**Tech Stack:** Python 3.12+ under uv (pytest, ruff, PyYAML, Pillow), solidcraft-cli 0.30.1,
Quarto 1.11.6, three.js 0.187.0, GitHub Actions and Pages, gitleaks 8.30.1, lychee v0.24.2.

**Spec:** `docs/superpowers/specs/2026-11-05-3d-models-design.md`

**Now:** Task 1: The Python toolchain and CI, open.

***

## Global Constraints

- Python runs only through uv: `uv sync --frozen`, `uv run --frozen …`; never pip.
- `requires-python = ">=3.12"`; ruff `line-length = 100`, `target-version = "py312"`.
- Every command is a `make` target; GNU make 3.81 features only.
- solidcraft-cli 0.30.1. Designs are saved with `file.save_as`, `format: json`, `cache: false`.
- A model's folder name is lowercase words joined by hyphens; it is the page's URL.
- Quarto 1.11.6; three.js 0.187.0 from `https://cdn.jsdelivr.net/npm/three@0.187.0/`.
- The site is <https://chendaniely.github.io/3d-models/>; the repo
  <https://github.com/chendaniely/3d-models>.
- No absolute local path, private address or personal detail in any committed file; every photo's
  GPS data stripped before it's staged.
- Every commit: message in a file, `git commit -F`, staged by path, `Plan:` trailer checked.
- No hooks yet: every push waits for Dan's OK, after `make leaks` passes.

## Review Focus

1. **A design saved from the SolidCraft app in its default zip format:** `make models` builds it
   and `make models-check` judges it like a text one (Task 2,
   `test_build_and_check_take_a_design_saved_as_a_zip`).
2. **A model folder named with spaces, capitals or underscores:** `make models-check` names it,
   since the name becomes a URL (Task 2, `test_check_names_a_folder_that_cannot_be_a_url`).
3. **A model with a design but no `model.yml`:** `make docs` names it instead of crashing (Task 5,
   `test_write_names_a_model_without_a_model_yml`).
4. **A `|` in a print setting:** it stays inside its table cell (Task 5,
   `test_a_bar_in_a_print_setting_stays_inside_its_cell`).
5. **A photo from a phone, named `IMG_0001.JPG`:** the upper-case extension is checked like any
   other (Task 3, `PRINT.JPG` in `test_check_names_a_photo_with_a_gps_block`).

***

### Task 1: The Python toolchain and CI

**Tier:** 1 (the `leaks` job is a guard: if wrong, a leak passes silently) · **Scenarios:** S04,
S05

**Files:**
- Create: `pyproject.toml`, `uv.lock` (by `uv lock`), `tests/test_makefile.py`,
  `.github/workflows/ci.yml`, `.github/dependabot.yml`
- Modify: `Makefile` (whole file below), `.gitignore` (three blocks appended)

**Interfaces:**
- Consumes: nothing.
- Produces: `make test` (`uv run --frozen pytest -q`), `make test-utc`, `make lint`
  (`ruff check .` and `ruff format --check .`), `make leaks`; placeholder targets `models`,
  `models-check` (Task 2), `photos` (Task 3) and `docs` (Task 4) that fail with "not built yet";
  CI jobs `tests` and `leaks`; ruff's first-party modules `conftest`, `gallery`, `models`,
  `photos`.

- [ ] **Step 0: Record the base:** `git rev-parse HEAD > .git/TASK_BASE`.
- [ ] **Step 1: Write the uv project.**

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
# scripts/commitmsg.py is plan-driven-development's copy, kept byte-identical to the skill's.
extend-exclude = ["scripts/commitmsg.py", "website/_site", "website/.quarto"]

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]

[tool.ruff.lint.isort]
known-first-party = ["conftest", "gallery", "models", "photos"]
```

  Then `uv lock` (writes `uv.lock`) and `uv sync --frozen`. Expected: `pillow`, `pytest`,
  `pyyaml` and `ruff` installed into `.venv`.

- [ ] **Step 2: Write the failing test.**

`tests/test_makefile.py`:

```python
"""The Makefile is the front door: every target AGENTS.md names is there, and help lists it."""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS = [
    "help",
    "hooks",
    "check",
    "test",
    "test-utc",
    "lint",
    "leaks",
    "models",
    "models-check",
    "photos",
    "docs",
]


def test_help_lists_every_target() -> None:
    result = subprocess.run(
        ["make", "--no-print-directory", "help"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    listed = {line.split()[0] for line in result.stdout.splitlines() if line.strip()}
    assert set(TARGETS) <= listed, sorted(set(TARGETS) - listed)
```

- [ ] **Step 3: Run it; watch it fail.** `uv run --frozen pytest -q tests/test_makefile.py`.
  Expected: `AssertionError: ['models', 'models-check', 'photos']`.
- [ ] **Step 4: Write the Makefile,** the whole file:

`Makefile`:

```makefile
# 3d-models: the front door for agents and people. `make help` lists the targets.
# GNU make 3.81 features only, so it runs on macOS as well as Linux.

.DEFAULT_GOAL := help
SHELL := /bin/bash

.PHONY: help hooks check test test-utc lint leaks models models-check photos docs

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

leaks: ## Scan the whole git history for secrets
	gitleaks git --redact --no-banner .

models: ## Rebuild each changed design's STL, picture and measurements (needs SolidCraft)
	@echo "not built yet: Phase 1, Task 2 sets it"; exit 1

models-check: ## Fail when a design has no build or a stale one
	@echo "not built yet: Phase 1, Task 2 sets it"; exit 1

photos: ## Fail when an image in the repo carries GPS data, or is a HEIC
	@echo "not built yet: Phase 1, Task 3 sets it"; exit 1

docs: ## Render the site into website/_site, failing on a broken link
	@echo "not built yet: Phase 1, Task 4 sets it"; exit 1

check: test test-utc lint leaks ## Everything CI runs
```

  And append to `.gitignore`:

```text

# the site: the generated model pages and the render log
website/models/
website/.render.log

# the Playwright browser tool's screenshots and logs
.playwright-mcp/
```

- [ ] **Step 5: Run the checks; they pass.** `make test`, then `make lint`. Expected:
  `1 passed`; `All checks passed!` and `files already formatted`. ruff skips
  `scripts/commitmsg.py`, the skill's copy, kept byte-identical (`pyproject.toml`).
- [ ] **Step 6: Write CI and Dependabot.**

`.github/workflows/ci.yml`:

```yaml
# CI: the tests, lint, the model and photo checks, the leak scan and the site, on every push to
# main or a phase branch and on every PR into main. Only main deploys the site to GitHub Pages.
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
      - uses: actions/checkout@v7.0.1
        with:
          persist-credentials: false
      - uses: astral-sh/setup-uv@v10.3.3
      - run: uv sync --frozen
      - run: make test
      - run: make test-utc
      - run: make lint

  leaks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7.0.1
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
# Keep the pinned CI actions and the Python dependencies current, once a month.
version: 2
updates:
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: monthly
  - package-ecosystem: uv
    directory: /
    schedule:
      interval: monthly
```

  Check both parse: `uv run --frozen python -c "import yaml; [yaml.safe_load(open(f)) for f in
  ('.github/workflows/ci.yml', '.github/dependabot.yml')]"`. Expected: no output.
- [ ] **Step 7: Run every check; they pass.** `make check`. Expected: the tests twice, lint, then
  gitleaks' `no leaks found`.
- [ ] **Step 8: Commit.** Write the message to `.git/COMMIT_MSG`:

```text
build(repo): 🤖 add the uv project, make test and lint, and CI

The repo had no test runner, linter or CI. This adds a uv project
(pytest, ruff, PyYAML, Pillow), sets make test, test-utc and lint, adds
placeholder targets for models, models-check, photos and docs that fail
until their tasks, and a CI workflow whose tests job runs the suite twice
(once under TZ=UTC) and lint, and whose leaks job runs gitleaks 8.30.1,
checked against its published checksum, over the whole history.
Dependabot keeps the actions and the lockfile current.

The new test failed first with: AssertionError: ['models',
'models-check', 'photos'].

Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-1.md Task 1
Co-Authored-By: <the model's own line>
```

  `git add pyproject.toml uv.lock Makefile .gitignore tests/test_makefile.py .github/workflows/ci.yml .github/dependabot.yml`, then `git commit -F .git/COMMIT_MSG`, then `git log -1 --format='%(trailers)'` shows the `Plan:` line.
- [ ] **Step 9: Review, look forward, close.**

  - **Review (Tier 1: Matt Pocock's `code-review`, two axes in two subagents, plus the security checklist, one line per item; at most one re-review),** from `$(cat .git/TASK_BASE)`.
  - **Forward:** Tasks 2 to 5 replace this task's placeholder targets; check their Consumes lines.
  - **Docs:** the README's command list stays true (it names `make models`, `check` and `docs`).
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

  - **Push,** once Dan has OKed it (`AGENTS.md`'s interim line): `make leaks`, then
    `git push origin phase-1`. The task is closed once CI on the closing commit, or a later
    one, is green; until a push, the local checks are the gate.

***

### Task 2: `make models` and `make models-check`

**Tier:** 2 · **Scenarios:** S01, S02

**Files:**
- Create: `scripts/models.py`, `tests/conftest.py`, `tests/test_models.py`
- Modify: `Makefile` (two recipes and the `check` line), `.github/workflows/ci.yml` (one step)

**Interfaces:**
- Consumes: Task 1's `make test`, `make lint` and the `tests` CI job.
- Produces, in `scripts/models.py`: `ROOT: Path`; `Model(folder: Path)` with `.slug -> str`,
  `.design -> Path` (`<slug>.sc`), `.built(kind: str) -> Path` (`<slug>.<kind>`, kind one of
  `"stl"`, `"png"`, `"eval.json"`), `.record -> Path` (`build.json`);
  `find_models(root: Path) -> list[Model]`; `sha256(path: Path) -> str`;
  `staleness(model: Model) -> str | None`; `main(argv: list[str] | None = None, root: Path = ROOT)
  -> int` with subcommands `build [--force] [SLUG ...]` and `check`. In `tests/conftest.py`: the
  fixtures `fake_cli` (returns the call log's path) and `repo` (an empty root with `models/`), and
  `add_design(root: Path, slug: str, text: str = ...) -> Path`. `SOLIDCRAFT_CLI` names the CLI.

- [ ] **Step 0: Record the base:** `git rev-parse HEAD > .git/TASK_BASE`.
- [ ] **Step 1: Write the fixtures and the failing tests.**

`tests/conftest.py`:

```python
"""Shared fixtures: scripts/ on the import path, and a fake solidcraft-cli."""

from __future__ import annotations

import os
import stat
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
    """An empty repo root with a models/ folder."""
    root = tmp_path / "repo"
    (root / "models").mkdir(parents=True)
    return root


def add_design(root: Path, slug: str, text: str = '{"format": "solidcraft/48"}') -> Path:
    folder = root / "models" / slug
    folder.mkdir(parents=True, exist_ok=True)
    design = folder / f"{slug}.sc"
    design.write_text(text, encoding="utf-8")
    return design
```

`tests/test_models.py`:

```python
"""scripts/models.py: build only what changed (S01); fail on a stale build (S02)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import models
from conftest import add_design


def calls(log: Path) -> list[str]:
    return log.read_text(encoding="utf-8").splitlines() if log.exists() else []


def test_build_writes_each_built_file_beside_the_design(repo: Path, fake_cli: Path) -> None:
    design = add_design(repo, "coupon")
    assert models.main(["build"], root=repo) == 0
    folder = design.parent
    for name in ("coupon.stl", "coupon.png", "coupon.eval.json", "build.json"):
        assert (folder / name).is_file(), name
    record = json.loads((folder / "build.json").read_text(encoding="utf-8"))
    assert record == {
        "design": "coupon.sc",
        "sha256": models.sha256(design),
        "solidcraft_cli": "solidcraft-cli 0.30.1",
    }


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


def test_build_force_rebuilds_an_up_to_date_model(repo: Path, fake_cli: Path) -> None:
    add_design(repo, "coupon")
    models.main(["build"], root=repo)
    fake_cli.unlink()
    assert models.main(["build", "--force", "coupon"], root=repo) == 0
    assert any(line.startswith("run --in") for line in calls(fake_cli))


def test_build_refuses_an_unknown_slug(repo: Path, fake_cli: Path, capsys) -> None:
    add_design(repo, "coupon")
    assert models.main(["build", "nope"], root=repo) == 2
    assert "no such model: nope" in capsys.readouterr().err


def test_build_reports_a_failing_design(repo: Path, fake_cli: Path, capsys) -> None:
    add_design(repo, "broken", text='{"fail": true}')
    assert models.main(["build"], root=repo) == 1
    assert "a timeline feature failed" in capsys.readouterr().err
    assert not (repo / "models" / "broken" / "build.json").exists()


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


@pytest.mark.parametrize("missing", ["coupon.stl", "coupon.png", "coupon.eval.json", "build.json"])
def test_check_names_a_missing_built_file(repo: Path, fake_cli: Path, capsys, missing: str) -> None:
    add_design(repo, "coupon")
    models.main(["build"], root=repo)
    (repo / "models" / "coupon" / missing).unlink()
    assert models.main(["check"], root=repo) == 1
    assert f"stale: models/coupon: missing {missing}" in capsys.readouterr().err


def test_check_ignores_a_folder_without_a_design(repo: Path, capsys) -> None:
    (repo / "models" / "notes").mkdir()
    assert models.main(["check"], root=repo) == 0
    assert "0 models" in capsys.readouterr().out


def test_build_and_check_take_a_design_saved_as_a_zip(repo: Path, fake_cli: Path) -> None:
    design = add_design(repo, "hook")
    design.write_bytes(b"PK\x03\x04 a zip container, as the app saves by default")
    assert models.main(["build"], root=repo) == 0
    assert models.main(["check"], root=repo) == 0


@pytest.mark.parametrize("slug", ["Wall Hook", "wall_hook", "WallHook", "-hook"])
def test_check_names_a_folder_that_cannot_be_a_url(repo: Path, capsys, slug: str) -> None:
    add_design(repo, slug)
    assert models.main(["check"], root=repo) == 1
    assert f"stale: models/{slug}: its folder name must be lowercase words joined by hyphens" in (
        capsys.readouterr().err
    )
```

- [ ] **Step 2: Run them; watch them fail.** `make test`. Expected: a collection error,
  `ModuleNotFoundError: No module named 'models'`.
- [ ] **Step 3: Write the builder.**

`scripts/models.py`:

```python
"""Build, check and publish the models under models/.

    uv run scripts/models.py build [--force] [SLUG ...]
        rebuild each model whose design changed since its build.json (needs solidcraft-cli)
    uv run scripts/models.py check
        fail, naming each model, when a design has no build or a stale one

A model is a folder models/<slug>/ holding the design <slug>.sc. A build writes, beside it:
<slug>.stl, <slug>.png, <slug>.eval.json (solidcraft-cli eval's measurements) and build.json
(the design's sha256 and the CLI's version). Exporting the same design twice gives a
byte-different STL, so freshness is judged by the design's hash, never by rebuilding.

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
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILT = ("stl", "png", "eval.json")
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

    @property
    def record(self) -> Path:
        return self.folder / "build.json"


def find_models(root: Path) -> list[Model]:
    models_dir = root / "models"
    if not models_dir.is_dir():
        return []
    return [
        Model(folder)
        for folder in sorted(models_dir.iterdir())
        if folder.is_dir() and (folder / f"{folder.name}.sc").is_file()
    ]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def staleness(model: Model) -> str | None:
    """Why the model needs a build, or None when its built files match its design."""
    if not SLUG.fullmatch(model.slug):
        return "its folder name must be lowercase words joined by hyphens, as the page's URL"
    missing = [model.built(kind).name for kind in BUILT if not model.built(kind).is_file()]
    if not model.record.is_file():
        missing.append(model.record.name)
    if missing:
        return "missing " + ", ".join(missing)
    try:
        recorded = json.loads(model.record.read_text(encoding="utf-8"))["sha256"]
    except (json.JSONDecodeError, KeyError, TypeError):
        return "build.json is unreadable"
    if recorded != sha256(model.design):
        return f"{model.design.name} changed since its last build"
    return None


def cli() -> str:
    return os.environ.get("SOLIDCRAFT_CLI", "solidcraft-cli")


def run(*args: str) -> str:
    result = subprocess.run([cli(), *args], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"{cli()} {' '.join(args)} failed:\n{result.stderr.strip()}")
    return result.stdout


def build(model: Model) -> None:
    design = str(model.design)
    run("run", "--in", design, "--out", str(model.built("stl")), "--quiet")
    run("snapshot", "--in", design, "--out", str(model.built("png")), *PICTURE)
    run("eval", "--in", design, "--json-out", str(model.built("eval.json")))
    record = {
        "design": model.design.name,
        "sha256": sha256(model.design),
        "solidcraft_cli": run("--version").strip(),
    }
    model.record.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")


def command_build(root: Path, slugs: list[str], force: bool) -> int:
    models = find_models(root)
    unknown = sorted(set(slugs) - {m.slug for m in models})
    if unknown:
        print(f"models: no such model: {', '.join(unknown)}", file=sys.stderr)
        return 2
    chosen = [m for m in models if not slugs or m.slug in slugs]
    built = 0
    for model in chosen:
        reason = "forced" if force else staleness(model)
        if reason is None:
            continue
        print(f"building models/{model.slug} ({reason})")
        try:
            build(model)
        except (OSError, RuntimeError) as error:
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
    build_parser.add_argument("--force", action="store_true", help="rebuild even if up to date")
    sub.add_parser("check", help="fail when a model's build is missing or stale")
    args = parser.parse_args(argv)
    if args.command == "build":
        return command_build(root, args.slugs, args.force)
    return command_check(root)


if __name__ == "__main__":
    sys.exit(main())
```

  In the `Makefile`, replace the two placeholder recipes, and add `models-check` to `check`:

```makefile
models: ## Rebuild each changed design's STL, picture and measurements (needs SolidCraft)
	uv run --frozen scripts/models.py build

models-check: ## Fail when a design has no build or a stale one
	uv run --frozen scripts/models.py check
```

```makefile
check: test test-utc lint models-check leaks ## Everything CI runs
```

  In `.github/workflows/ci.yml`'s `tests` job, after `- run: make lint`, add
  `      - run: make models-check`.
- [ ] **Step 4: Run the checks; they pass.** `make check`. Expected: `19 passed` twice, lint
  clean, `0 models, every build matches its design`, `no leaks found`.
- [ ] **Step 5: Commit.** Write the message to `.git/COMMIT_MSG`:

```text
feat(models): 🤖 build changed designs and fail on a stale build

make models had nothing behind it. scripts/models.py build runs
solidcraft-cli for each design whose SHA-256 differs from its build.json,
writing the STL, the picture, the measurements and the record beside it;
check fails, naming each model, when a build is missing or stale, or when a
folder's name can't be a URL. Freshness is the design's hash because the
CLI exports a byte-different STL each run. The tests run a fake CLI, named
by SOLIDCRAFT_CLI, so CI needs no SolidCraft.

The new tests failed first with: ModuleNotFoundError: No module named
'models'.

Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-1.md Task 2
Co-Authored-By: <the model's own line>
```

  `git add scripts/models.py tests/conftest.py tests/test_models.py Makefile .github/workflows/ci.yml`, then `git commit -F .git/COMMIT_MSG`, then `git log -1 --format='%(trailers)'` shows the `Plan:` line.
- [ ] **Step 6: Review, look forward, close.**

  - **Review (Tier 2: Matt Pocock's `code-review`, two axes in two subagents; fix Critical and Important; at most one re-review),** from `$(cat .git/TASK_BASE)`.
  - **Forward:** Tasks 5 and 6 consume `find_models`, `Model` and `staleness`; check their listings.
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

  - **Push,** once Dan has OKed it (`AGENTS.md`'s interim line): `make leaks`, then
    `git push origin phase-1`. The task is closed once CI on the closing commit, or a later
    one, is green; until a push, the local checks are the gate.

***

### Task 3: The photo guard, `make photos`

**Tier:** 1 (if wrong, a photo leaks where Dan lives) · **Scenarios:** S03

**Files:**
- Create: `scripts/photos.py`, `tests/test_photos.py`
- Modify: `Makefile` (one recipe and the `check` line), `.github/workflows/ci.yml` (one step)

**Interfaces:**
- Consumes: Task 2's `repo` fixture.
- Produces, in `scripts/photos.py`: `images(root: Path) -> list[Path]`,
  `problem(path: Path) -> str | None`, `strip(path: Path) -> None`,
  `main(argv: list[str] | None = None, root: Path = ROOT) -> int` with subcommands `check` and
  `strip FILE ...`.

- [ ] **Step 0: Record the base:** `git rev-parse HEAD > .git/TASK_BASE`.
- [ ] **Step 1: Write the failing tests.**

`tests/test_photos.py`:

```python
"""scripts/photos.py: no image with a location gets in (S03)."""

from __future__ import annotations

from pathlib import Path

import pytest
from PIL import ExifTags, Image

import photos

XMP_WITH_GPS = (
    b'<x:xmpmeta xmlns:x="adobe:ns:meta/"><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-'
    b'syntax-ns#"><rdf:Description xmlns:exif="http://ns.adobe.com/exif/1.0/" '
    b'exif:GPSLatitude="0,0.0N" exif:GPSLongitude="0,0.0E"/></rdf:RDF></x:xmpmeta>'
)


def photo(path: Path, *, gps: bool = False, orientation: int | None = None) -> Path:
    """A 40x20 image, optionally with a GPS block and an EXIF orientation."""
    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (40, 20), (200, 180, 150))
    exif = image.getexif()
    if gps:
        block = exif.get_ifd(ExifTags.IFD.GPSInfo)
        block[ExifTags.GPS.GPSLatitudeRef] = "N"
        block[ExifTags.GPS.GPSLatitude] = (0.0, 0.0, 0.0)
    if orientation:
        exif[ExifTags.Base.Orientation] = orientation
    image.save(
        path, exif=exif.tobytes()
    )  # an Exif object holding only a GPS block is dropped from a PNG
    return path


def test_check_passes_a_clean_photo(repo: Path, capsys) -> None:
    photo(repo / "models" / "coupon" / "photos" / "print.jpg")
    assert photos.main(["check"], root=repo) == 0
    assert "1 images, none with a location" in capsys.readouterr().out


@pytest.mark.parametrize("name", ["print.jpg", "PRINT.JPG", "print.png", "print.webp"])
def test_check_names_a_photo_with_a_gps_block(repo: Path, capsys, name: str) -> None:
    photo(repo / "models" / "coupon" / "photos" / name, gps=True)
    assert photos.main(["check"], root=repo) == 1
    err = capsys.readouterr().err
    assert f"photo: models/coupon/photos/{name}: a GPS block in its EXIF" in err


def test_check_names_a_photo_with_gps_in_its_xmp(repo: Path, capsys) -> None:
    path = repo / "docs" / "install.jpg"
    path.parent.mkdir(parents=True)
    Image.new("RGB", (40, 20)).save(path, xmp=XMP_WITH_GPS)
    assert photos.main(["check"], root=repo) == 1
    assert "photo: docs/install.jpg: GPS coordinates in its metadata" in capsys.readouterr().err


@pytest.mark.parametrize("name", ["IMG_0001.HEIC", "shot.heif"])
def test_check_refuses_a_heic(repo: Path, capsys, name: str) -> None:
    (repo / "models" / name).write_bytes(b"\x00\x00\x00\x18ftypheic")
    assert photos.main(["check"], root=repo) == 1
    assert f"photo: models/{name}: a HEIC or HEIF photo; convert it to JPEG" in (
        capsys.readouterr().err
    )


def test_check_skips_the_rendered_site_and_the_venv(repo: Path) -> None:
    photo(repo / "website" / "_site" / "shot.jpg", gps=True)
    photo(repo / ".venv" / "lib" / "shot.jpg", gps=True)
    assert photos.main(["check"], root=repo) == 0


@pytest.mark.parametrize("name", ["print.jpg", "print.png", "print.webp"])
def test_strip_removes_the_location(repo: Path, name: str) -> None:
    path = photo(repo / "models" / "photos" / name, gps=True)
    assert photos.main(["strip", str(path)], root=repo) == 0
    assert photos.problem(path) is None
    with Image.open(path) as image:
        assert image.size == (40, 20)


def test_strip_removes_gps_from_the_xmp(repo: Path) -> None:
    path = repo / "install.jpg"
    Image.new("RGB", (40, 20)).save(path, xmp=XMP_WITH_GPS)
    photos.main(["strip", str(path)], root=repo)
    assert photos.problem(path) is None


def test_strip_turns_the_photo_upright_before_dropping_its_orientation(repo: Path) -> None:
    path = photo(repo / "sideways.jpg", orientation=6)
    photos.main(["strip", str(path)], root=repo)
    with Image.open(path) as image:
        assert image.size == (20, 40)
        assert ExifTags.Base.Orientation not in image.getexif()


def test_strip_refuses_a_heic(repo: Path, capsys) -> None:
    path = repo / "IMG_0001.heic"
    path.write_bytes(b"\x00")
    assert photos.main(["strip", str(path)], root=repo) == 2
    assert "strip takes JPEG, PNG or WebP only" in capsys.readouterr().err
```

- [ ] **Step 2: Run them; watch them fail.** `make test`. Expected: a collection error,
  `ModuleNotFoundError: No module named 'photos'`.
- [ ] **Step 3: Write the guard.**

`scripts/photos.py`:

```python
"""Keep photo locations out of the repo.

    uv run scripts/photos.py check
        fail, naming each file, when an image anywhere in the repo carries GPS data,
        or is a HEIC or HEIF (convert it to JPEG first: this check can't read inside one)
    uv run scripts/photos.py strip FILE ...
        rewrite each JPEG, PNG or WebP without its metadata, turned upright first

GPS data hides in two places: EXIF's GPS block, and XMP text (exif:GPSLatitude and the like).
The check reads both; strip drops all EXIF, XMP and text chunks, keeping only the colour profile.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import ExifTags, Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
READABLE = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}
UNREADABLE = {".heic", ".heif"}
SKIPPED_DIRS = {".git", ".venv", "_site", ".quarto", "node_modules", ".pytest_cache", ".ruff_cache"}
GPS_TEXT = (b"GPSLatitude", b"GPSLongitude")


def images(root: Path) -> list[Path]:
    found = []
    for path in sorted(root.rglob("*")):
        if any(part in SKIPPED_DIRS for part in path.relative_to(root).parts):
            continue
        if path.is_file() and path.suffix.lower() in READABLE | UNREADABLE:
            found.append(path)
    return found


def problem(path: Path) -> str | None:
    """Why this image can't be committed, or None when it carries no location."""
    if path.suffix.lower() in UNREADABLE:
        return "a HEIC or HEIF photo; convert it to JPEG, then run photos.py strip on it"
    raw = path.read_bytes()
    if any(marker in raw for marker in GPS_TEXT):
        return "GPS coordinates in its metadata"
    try:
        with Image.open(path) as image:
            image.load()  # a PNG may keep its EXIF after the image data
            gps = image.getexif().get_ifd(ExifTags.IFD.GPSInfo)
    except OSError as error:
        return f"unreadable as an image ({error})"
    if gps:
        return "a GPS block in its EXIF"
    return None


def strip(path: Path) -> None:
    with Image.open(path) as opened:
        image = ImageOps.exif_transpose(opened)
        image.load()
        icc = opened.info.get("icc_profile")
        image_format = opened.format
    options = {"icc_profile": icc} if icc else {}
    if image_format == "JPEG":
        options |= {"quality": 95, "subsampling": 0}
    image.save(path, format=image_format, **options)


def command_check(root: Path) -> int:
    found = [(path, reason) for path in images(root) if (reason := problem(path)) is not None]
    for path, reason in found:
        print(f"photo: {path.relative_to(root)}: {reason}", file=sys.stderr)
    if found:
        return 1
    print(f"{len(images(root))} images, none with a location")
    return 0


def command_strip(files: list[Path]) -> int:
    for path in files:
        if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            print(f"photo: {path}: strip takes JPEG, PNG or WebP only", file=sys.stderr)
            return 2
        strip(path)
        print(f"stripped {path}")
    return 0


def main(argv: list[str] | None = None, root: Path = ROOT) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check", help="fail on an image with a location, or a HEIC")
    strip_parser = sub.add_parser("strip", help="rewrite images without their metadata")
    strip_parser.add_argument("files", nargs="+", type=Path, metavar="FILE")
    args = parser.parse_args(argv)
    if args.command == "strip":
        return command_strip(args.files)
    return command_check(root)


if __name__ == "__main__":
    sys.exit(main())
```

  In the `Makefile`, replace the placeholder recipe, and add `photos` to `check`:

```makefile
photos: ## Fail when an image in the repo carries GPS data, or is a HEIC
	uv run --frozen scripts/photos.py check
```

```makefile
check: test test-utc lint models-check photos leaks ## Everything CI runs
```

  In `.github/workflows/ci.yml`'s `tests` job, after `- run: make models-check`, add
  `      - run: make photos`.
- [ ] **Step 4: Run the checks; they pass.** `make check`. Expected: `34 passed` twice, lint
  clean, `0 models, …`, `0 images, none with a location`, `no leaks found`.
- [ ] **Step 5: Commit.** Write the message to `.git/COMMIT_MSG`:

```text
feat(photos): 🤖 refuse a photo carrying GPS data, and strip one

Dan's rule for this public repo is that no photo carries its location.
scripts/photos.py check walks the repo (skipping .git, .venv and the
rendered site) and fails, naming each file, on a GPS block in a JPEG, PNG,
WebP or TIFF's EXIF, on GPS coordinates in its XMP, and on any HEIC or
HEIF, which it can't read inside. strip rewrites a JPEG, PNG or WebP
upright and without its metadata, keeping the colour profile. make photos
runs the check, and so do make check and CI.

The new tests failed first with: ModuleNotFoundError: No module named
'photos'.

Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-1.md Task 3
Co-Authored-By: <the model's own line>
```

  `git add scripts/photos.py tests/test_photos.py Makefile .github/workflows/ci.yml`, then `git commit -F .git/COMMIT_MSG`, then `git log -1 --format='%(trailers)'` shows the `Plan:` line.
- [ ] **Step 6: Review, look forward, close.**

  - **Review (Tier 1: Matt Pocock's `code-review`, two axes in two subagents, plus the security checklist, one line per item; at most one re-review),** from `$(cat .git/TASK_BASE)`.
  - **Forward:** Phase 2's install task adds the first photo; its listing runs `scripts/photos.py strip`.
  - **Docs:** the README's command list; `AGENTS.md`'s docs table already names `photos.py strip`.
  - **Close,** its own commit: this task's boxes ticked, **Now** set to the next task, any
    Built differently and Ruling lines, deferred findings on the phase-end list, the spec's
    scenario statuses (`built`). The message, from `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 3: The photo guard, make photos

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

  - **Push,** once Dan has OKed it (`AGENTS.md`'s interim line): `make leaks`, then
    `git push origin phase-1`. The task is closed once CI on the closing commit, or a later
    one, is green; until a push, the local checks are the gate.

***

### Task 4: The docs site

**Tier:** 1 (the `pages` job holds the only write permissions in CI) · **Scenarios:** S05, S06,
S10

**Files:**
- Create: `website/_quarto.yml`, `website/styles.css`, `website/_diagram-zoom.html`,
  `website/index.qmd`, `website/_overview.qmd`, `website/architecture.qmd`, `website/design.qmd`,
  `website/changelog.md`, `website/how-we-work.md`, the six wrappers under `website/superpowers/`,
  `tests/test_site.py`
- Modify: `Makefile` (the `docs` recipe and the `check` line), `tests/test_makefile.py` (one test
  appended), `.github/workflows/ci.yml` (the `site` and `pages` jobs appended)

**Interfaces:**
- Consumes: Task 1's targets and CI; the docs under `docs/superpowers/`.
- Produces: `make docs` (render, fail on an unresolved link, `lychee --offline` when installed);
  the site's pages Home, Architecture, Design, Changelog and How we work; `website/_overview.qmd`
  (the one overview diagram); CI jobs `site` (uploads the Pages artifact on `main`) and `pages`;
  the rule that every `.md` under `docs/superpowers/` has a wrapper and a Design-page line.

- [ ] **Step 0: Record the base:** `git rev-parse HEAD > .git/TASK_BASE`.
- [ ] **Step 1: Write the failing tests.**

`tests/test_site.py`:

```python
"""Every doc under docs/superpowers/ is on the site (S06)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs" / "superpowers"
SITE = ROOT / "website"


def docs() -> list[Path]:
    return sorted(path.relative_to(DOCS) for path in DOCS.rglob("*.md"))


def test_there_are_docs_to_check() -> None:
    assert docs()


def test_every_doc_has_a_wrapper_that_includes_it() -> None:
    missing = []
    for doc in docs():
        wrapper = SITE / "superpowers" / doc
        include = f"{{{{< include /../docs/superpowers/{doc.as_posix()} >}}}}"
        if not wrapper.is_file() or include not in wrapper.read_text(encoding="utf-8"):
            missing.append(f"website/superpowers/{doc.as_posix()}")
    assert not missing, f"docs without a wrapper: {missing}"


def test_every_wrapper_is_listed_on_the_design_page() -> None:
    design = (SITE / "design.qmd").read_text(encoding="utf-8")
    unlisted = [doc.as_posix() for doc in docs() if f"(superpowers/{doc.as_posix()})" not in design]
    assert not unlisted, f"docs missing from the Design page: {unlisted}"


def test_no_wrapper_is_left_without_its_doc() -> None:
    wrappers = sorted(
        p.relative_to(SITE / "superpowers") for p in (SITE / "superpowers").rglob("*.md")
    )
    orphans = [w.as_posix() for w in wrappers if not (DOCS / w).is_file()]
    assert not orphans, f"wrappers whose doc is gone: {orphans}"
```

  Append to `tests/test_makefile.py`:

```python


def test_check_runs_everything_ci_runs_but_the_build() -> None:
    line = next(
        line
        for line in (ROOT / "Makefile").read_text(encoding="utf-8").splitlines()
        if line.startswith("check:")
    )
    prerequisites = line.split(":", 1)[1].split("##")[0].split()
    assert prerequisites == ["test", "test-utc", "lint", "models-check", "photos", "leaks", "docs"]
```

- [ ] **Step 2: Run them; watch them fail.** `make test`. Expected: `docs without a wrapper`,
  `FileNotFoundError` for `website/design.qmd`, and the `check` line's prerequisites differing.
- [ ] **Step 3: Write the site.**

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
  built["STL · PNG · eval.json · build.json<br/>committed beside the design"]
  ci["CI on every push<br/>tests · lint · models-check · photos · leaks · site"]
  gallery["make docs<br/>Quarto"]
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
%%| fig-cap: "make models rebuilds only a design whose hash differs from its build record."
flowchart TD
  start["make models"] --> each{"for each models/&lt;slug&gt;/&lt;slug&gt;.sc"}
  each --> hash{"sha256 of the design<br/>= build.json's?"}
  hash -- yes --> skip["left alone"]
  hash -- "no, or no build yet" --> run["solidcraft-cli run → &lt;slug&gt;.stl"]
  run --> snap["solidcraft-cli snapshot → &lt;slug&gt;.png"]
  snap --> evaluate["solidcraft-cli eval → &lt;slug&gt;.eval.json"]
  evaluate --> record["build.json: the design's sha256, the CLI's version"]
```

## Checks and the deploy

```{mermaid}
%%| fig-cap: "CI runs on every push; only main deploys."
flowchart LR
  push["a push"] --> tests["tests job<br/>make test · test-utc · lint<br/>models-check · photos"]
  push --> leaks["leaks job<br/>gitleaks over the history"]
  push --> site["site job<br/>make docs · lychee"]
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

  The wrappers, one per doc:

`website/superpowers/specs/2026-11-05-3d-models-design.md`:

```markdown
---
pagetitle: "3d-models: design spec"
---

{{< include /../docs/superpowers/specs/2026-11-05-3d-models-design.md >}}
```

`website/superpowers/specs/2026-11-05-3d-models-qa.md`:

```markdown
---
pagetitle: "3d-models: kickoff Q&A"
---

{{< include /../docs/superpowers/specs/2026-11-05-3d-models-qa.md >}}
```

`website/superpowers/specs/2026-11-05-3d-models-kickoff-notes.md`:

```markdown
---
pagetitle: "3d-models: kickoff notes"
---

{{< include /../docs/superpowers/specs/2026-11-05-3d-models-kickoff-notes.md >}}
```

`website/superpowers/specs/2026-11-05-3d-models-kickoff-council.md`:

```markdown
---
pagetitle: "3d-models: kickoff council"
---

{{< include /../docs/superpowers/specs/2026-11-05-3d-models-kickoff-council.md >}}
```

`website/superpowers/plans/2026-11-05-3d-models-phase-1.md`:

```markdown
---
pagetitle: "3d-models: Phase 1 plan"
---

{{< include /../docs/superpowers/plans/2026-11-05-3d-models-phase-1.md >}}
```

`website/superpowers/plans/2026-11-05-3d-models-phase-2.md`:

```markdown
---
pagetitle: "3d-models: Phase 2 plan"
---

{{< include /../docs/superpowers/plans/2026-11-05-3d-models-phase-2.md >}}
```

  In the `Makefile`, replace the `docs` placeholder and set `check`'s final line:

```makefile
docs: ## Render the site into website/_site, failing on a broken link
	@set -o pipefail; quarto render website 2>&1 | tee website/.render.log
	@if grep -q 'Unable to resolve link target' website/.render.log; then \
	  echo "docs: an unresolved link, above"; exit 1; fi
	@if command -v lychee >/dev/null; then lychee --offline --no-progress website/_site; \
	else echo "lychee isn't installed: the offline link check runs in CI only"; fi
```

```makefile
check: test test-utc lint models-check photos leaks docs ## Everything CI runs
```

  Append the `site` and `pages` jobs to `.github/workflows/ci.yml`:

```yaml
  site:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7.0.1
        with:
          persist-credentials: false
      - uses: astral-sh/setup-uv@v10.3.3
      - uses: quarto-dev/quarto-actions/setup@v2.2.0
        with:
          version: 1.11.6
      - run: uv sync --frozen
      - run: make docs
      - name: Check every link inside the rendered site
        uses: lycheeverse/lychee-action@v2.9.0
        with:
          lycheeVersion: v0.24.2
          args: --offline --no-progress website/_site
          fail: true
          jobSummary: false
      - if: github.ref == 'refs/heads/main' && github.event_name != 'pull_request'
        uses: actions/upload-pages-artifact@v5.0.0
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
        uses: actions/deploy-pages@v5.0.1
```

- [ ] **Step 4: Run the checks; they pass.** `make check`. Expected: every test passes twice, the
  render ends `Output created: _site/index.html` with no "Unable to resolve link target", and
  lychee runs, or says it runs in CI only.
- [ ] **Step 5: Commit.** Write the message to `.git/COMMIT_MSG`:

```text
feat(site): 🤖 add the Quarto docs site and its deploy

The repo had no site. website/ holds a Quarto site with Home (the README,
then the overview diagram), Architecture (every diagram, planned parts
dashed), Design (a .md wrapper per doc under docs/superpowers/), Changelog
and How we work, in a quiet Japandi palette. make docs renders it and fails
on an unresolved link. CI's site job renders it and runs lychee offline;
on main it uploads the Pages artifact, and the pages job, the only one
with pages and id-token write, deploys it once tests, leaks and site pass.
make check now runs everything CI runs.

The new tests failed first with: docs without a wrapper, and
FileNotFoundError for website/design.qmd.

Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-1.md Task 4
Co-Authored-By: <the model's own line>
```

  `git add website tests/test_site.py tests/test_makefile.py Makefile .github/workflows/ci.yml`, then `git commit -F .git/COMMIT_MSG`, then `git log -1 --format='%(trailers)'` shows the `Plan:` line.
  (`git add website` stages the new folder only; check `git status --short` names no other
  path under it.)
- [ ] **Step 6: Review, look forward, close.**

  - **Review (Tier 1: Matt Pocock's `code-review`, two axes in two subagents, plus the security checklist, one line per item; at most one re-review),** from `$(cat .git/TASK_BASE)`.
  - **Forward:** Task 5 adds the Models page, the viewer and two lines to `make docs`; Task 7 sets Pages' source, without which the `pages` job fails on `main`.
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

  - **Push,** once Dan has OKed it (`AGENTS.md`'s interim line): `make leaks`, then
    `git push origin phase-1`. The task is closed once CI on the closing commit, or a later
    one, is green; until a push, the local checks are the gate.

***

### Task 5: The gallery and the 3D viewer

**Tier:** 2 · **Scenarios:** S07, S08

**Files:**
- Create: `scripts/gallery.py`, `tests/test_gallery.py`, `website/models.qmd`,
  `website/_stl-viewer.html`, `website/assets/stl-viewer.js`
- Modify: `website/_quarto.yml` (resources and a navbar entry), `website/styles.css` (the
  viewer's rules), `website/_overview.qmd` (the gallery drawn as built), `Makefile` (two lines in
  `docs`)

**Interfaces:**
- Consumes: Task 2's `ROOT`, `Model`, `find_models`; Task 4's site and `make docs`.
- Produces, in `scripts/gallery.py`: `ModelError(ValueError)`; `read_meta(model: Model) -> dict`
  (fields `title`, `summary`, `status` in `designed | printed | in use`, `material`, optional
  `print` mapping and `notes` text); `read_eval(model: Model) -> dict`;
  `page(model: Model, meta: dict, evaluation: dict) -> str`;
  `main(argv: list[str] | None = None, root: Path = ROOT) -> int` with subcommands `write` and
  `check-site`. On the site: `website/models/<slug>.qmd` (generated, git-ignored) and the
  `<div class="stl-viewer" data-stl="<slug>/<slug>.stl">` the viewer mounts on.

- [ ] **Step 0: Record the base:** `git rev-parse HEAD > .git/TASK_BASE`.
- [ ] **Step 1: Write the failing tests.**

`tests/test_gallery.py`:

```python
"""scripts/gallery.py: a card and a page per model (S07), with a 3D viewer and downloads (S08)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

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
    (folder / f"{slug}.stl").write_bytes(b"solid")
    (folder / f"{slug}.png").write_bytes(b"\x89PNG")
    return folder


def test_write_makes_a_page_and_copies_the_files(repo: Path) -> None:
    add_model(repo)
    assert gallery.main(["write"], root=repo) == 0
    out = repo / "website" / "models"
    assert (out / "hook.qmd").is_file()
    for name in ("hook.stl", "hook.png", "hook.sc"):
        assert (out / "hook" / name).is_file(), name


def test_the_page_is_a_card_with_a_picture_title_and_summary(repo: Path) -> None:
    add_model(repo)
    gallery.main(["write"], root=repo)
    text = (repo / "website" / "models" / "hook.qmd").read_text(encoding="utf-8")
    front = text.split("---")[1]
    assert 'title: "Test hook"' in front
    assert 'description: "A hook for testing."' in front
    assert "image: hook/hook.png" in front


def test_the_page_has_the_viewer_the_measurements_and_the_downloads(repo: Path) -> None:
    add_model(repo)
    gallery.main(["write"], root=repo)
    text = (repo / "website" / "models" / "hook.qmd").read_text(encoding="utf-8")
    assert "include-in-header: ../_stl-viewer.html" in text
    assert '::: {.stl-viewer data-stl="hook/hook.stl"' in text
    assert "| Size (x × y × z) | 45.0 × 30.0 × 10.0 mm |" in text
    assert "| Volume | 6.0 cm³ |" in text
    assert "| Weight in PETG, solid | 8 g |" in text
    assert "| `hook_w` | `20 mm` | 20 mm |" in text
    assert "| Infill | 20% |" in text
    assert "Hang it on a dowel." in text
    assert "- [hook.stl](hook/hook.stl)" in text
    assert "- [hook.sc](hook/hook.sc)" in text
    assert "https://github.com/chendaniely/3d-models/tree/main/models/hook" in text


def test_write_removes_the_page_of_a_model_that_is_gone(repo: Path) -> None:
    add_model(repo)
    stale = repo / "website" / "models" / "old.qmd"
    stale.parent.mkdir(parents=True)
    stale.write_text("old", encoding="utf-8")
    gallery.main(["write"], root=repo)
    assert not stale.exists()


@pytest.mark.parametrize(
    ("meta", "message"),
    [
        (META.replace("title: Test hook\n", ""), "'title' must be a non-empty string"),
        (META.replace("status: printed", "status: lost"), "'status' must be one of"),
        (
            META.replace("  Layer height: 0.2 mm\n  Infill: 20%", "  - Layer height 0.2 mm"),
            "'print' must map settings to values",
        ),
        (META + "notes: [unclosed\n", "isn't valid YAML"),
    ],
)
def test_write_names_a_bad_model_yml_and_writes_nothing(
    repo: Path, capsys, meta: str, message: str
) -> None:
    add_model(repo, meta=meta)
    assert gallery.main(["write"], root=repo) == 1
    assert "gallery: models/hook/model.yml" in (err := capsys.readouterr().err)
    assert message in err
    assert not (repo / "website" / "models").exists()


def test_write_names_a_model_never_built(repo: Path, capsys) -> None:
    folder = add_model(repo)
    (folder / "hook.eval.json").unlink()
    assert gallery.main(["write"], root=repo) == 1
    assert "gallery: models/hook: no hook.eval.json; run make models" in capsys.readouterr().err


def rendered_site(root: Path, slug: str = "hook") -> Path:
    site = root / "website" / "_site"
    (site / "assets").mkdir(parents=True)
    (site / "assets" / "stl-viewer.js").write_text("//", encoding="utf-8")
    (site / "models.html").write_text(f'<a href="models/{slug}.html">', encoding="utf-8")
    (site / "models" / slug).mkdir(parents=True)
    (site / "models" / f"{slug}.html").write_text(
        f'<div class="stl-viewer" data-stl="{slug}/{slug}.stl"></div>', encoding="utf-8"
    )
    for kind in ("stl", "png", "sc"):
        (site / "models" / slug / f"{slug}.{kind}").write_bytes(b"x")
    return site


def test_check_site_passes_a_complete_render(repo: Path) -> None:
    add_model(repo)
    rendered_site(repo)
    assert gallery.main(["check-site"], root=repo) == 0


@pytest.mark.parametrize(
    ("remove", "message"),
    [
        ("models/hook/hook.stl", "site: missing models/hook/hook.stl"),
        ("models/hook.html", "site: missing models/hook.html"),
        ("assets/stl-viewer.js", "site: missing assets/stl-viewer.js"),
    ],
)
def test_check_site_names_what_the_render_left_out(
    repo: Path, capsys, remove: str, message: str
) -> None:
    add_model(repo)
    site = rendered_site(repo)
    (site / remove).unlink()
    assert gallery.main(["check-site"], root=repo) == 1
    assert message in capsys.readouterr().err


def test_check_site_names_a_page_without_its_viewer_or_card(repo: Path, capsys) -> None:
    add_model(repo)
    site = rendered_site(repo)
    (site / "models" / "hook.html").write_text("<p>no viewer</p>", encoding="utf-8")
    (site / "models.html").write_text("<p>no cards</p>", encoding="utf-8")
    assert gallery.main(["check-site"], root=repo) == 1
    err = capsys.readouterr().err
    assert "site: missing models/hook.html's 3D viewer" in err
    assert "site: missing models.html's card for hook" in err


def test_write_names_a_model_without_a_model_yml(repo: Path, capsys) -> None:
    folder = add_model(repo)
    (folder / "model.yml").unlink()
    assert gallery.main(["write"], root=repo) == 1
    assert "gallery: models/hook: no model.yml" in capsys.readouterr().err


def test_a_bar_in_a_print_setting_stays_inside_its_cell(repo: Path) -> None:
    add_model(repo, meta=META.replace("Infill: 20%", "Infill: 20% | gyroid"))
    gallery.main(["write"], root=repo)
    text = (repo / "website" / "models" / "hook.qmd").read_text(encoding="utf-8")
    assert "| Infill | 20% \\| gyroid |" in text
```

- [ ] **Step 2: Run them; watch them fail.** `make test`. Expected: a collection error,
  `ModuleNotFoundError: No module named 'gallery'`.
- [ ] **Step 3: Write the gallery and the viewer.**

`scripts/gallery.py`:

```python
"""Write the site's model pages from models/, and check the rendered site has them.

    uv run scripts/gallery.py write
        write website/models/<slug>.qmd for each model and copy its .stl, .png and .sc beside it
    uv run scripts/gallery.py check-site
        after quarto render: fail, naming each, when a model's page or file is missing from
        website/_site

website/models/ is generated and git-ignored: write empties it first, so a removed model's page
goes with it. Each model's model.yml gives its title, summary, status, material, print settings
and notes; its eval.json gives the measurements and parameters.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import yaml

from models import ROOT, Model, find_models

REPO_URL = "https://github.com/chendaniely/3d-models"
STATUSES = ("designed", "printed", "in use")
DENSITY_G_CM3 = {"PLA": 1.24, "PETG": 1.27}
COPIED = ("stl", "png", "sc")


class ModelError(ValueError):
    """A model.yml or eval.json that can't make a page."""


def read_meta(model: Model) -> dict:
    path = model.folder / "model.yml"
    if not path.is_file():
        raise ModelError(f"models/{model.slug}: no model.yml")
    try:
        meta = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as error:
        raise ModelError(f"models/{model.slug}/model.yml isn't valid YAML: {error}") from error
    if not isinstance(meta, dict):
        raise ModelError(f"models/{model.slug}/model.yml must be a mapping of fields")
    for field in ("title", "summary", "status", "material"):
        if not isinstance(meta.get(field), str) or not meta[field].strip():
            raise ModelError(f"models/{model.slug}/model.yml: '{field}' must be a non-empty string")
    if meta["status"] not in STATUSES:
        raise ModelError(
            f"models/{model.slug}/model.yml: 'status' must be one of {', '.join(STATUSES)}"
        )
    print_settings = meta.get("print", {})
    if not isinstance(print_settings, dict) or not all(
        isinstance(k, str) and isinstance(v, str | int | float) for k, v in print_settings.items()
    ):
        raise ModelError(f"models/{model.slug}/model.yml: 'print' must map settings to values")
    if not isinstance(meta.get("notes", ""), str):
        raise ModelError(f"models/{model.slug}/model.yml: 'notes' must be text")
    return meta


def read_eval(model: Model) -> dict:
    path = model.built("eval.json")
    if not path.is_file():
        raise ModelError(f"models/{model.slug}: no {path.name}; run make models")
    return json.loads(path.read_text(encoding="utf-8"))


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
    lines += [
        "## Files",
        "",
        f"- [{slug}.stl]({slug}/{slug}.stl): the mesh to slice",
        f"- [{slug}.sc]({slug}/{slug}.sc): the SolidCraft design, every dimension a parameter",
        f"- [The model's folder on GitHub]({REPO_URL}/tree/main/models/{slug})",
        "",
    ]
    return "\n".join(lines)


def command_write(root: Path) -> int:
    out = root / "website" / "models"
    models = find_models(root)
    try:
        pages = [(m, page(m, read_meta(m), read_eval(m))) for m in models]
    except ModelError as error:
        print(f"gallery: {error}", file=sys.stderr)
        return 1
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)
    for model, text in pages:
        (out / f"{model.slug}.qmd").write_text(text, encoding="utf-8")
        files = out / model.slug
        files.mkdir()
        for kind in COPIED:
            source = model.design if kind == "sc" else model.built(kind)
            shutil.copy2(source, files / source.name)
    print(f"gallery: {len(pages)} model pages in website/models/")
    return 0


def command_check_site(root: Path) -> int:
    site = root / "website" / "_site"
    missing = []
    if not (site / "assets" / "stl-viewer.js").is_file():
        missing.append("assets/stl-viewer.js")
    listing = site / "models.html"
    listing_text = listing.read_text(encoding="utf-8") if listing.is_file() else ""
    if not listing_text:
        missing.append("models.html")
    for model in find_models(root):
        slug = model.slug
        html = site / "models" / f"{slug}.html"
        if not html.is_file():
            missing.append(f"models/{slug}.html")
        elif f'data-stl="{slug}/{slug}.stl"' not in html.read_text(encoding="utf-8"):
            missing.append(f"models/{slug}.html's 3D viewer")
        for kind in COPIED:
            if not (site / "models" / slug / f"{slug}.{kind}").is_file():
                missing.append(f"models/{slug}/{slug}.{kind}")
        if listing_text and f"models/{slug}.html" not in listing_text:
            missing.append(f"models.html's card for {slug}")
    for item in missing:
        print(f"site: missing {item}", file=sys.stderr)
    if missing:
        return 1
    print("site: every model's page, viewer and files are in website/_site")
    return 0


def main(argv: list[str] | None = None, root: Path = ROOT) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("write", help="write the model pages into website/models/")
    sub.add_parser("check-site", help="check the rendered site has every model")
    args = parser.parse_args(argv)
    if args.command == "write":
        return command_write(root)
    return command_check_site(root)


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
    "three": "https://cdn.jsdelivr.net/npm/three@0.187.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.187.0/examples/jsm/"
  }
}
</script>
<script type="module" src="../assets/stl-viewer.js"></script>
```

`website/assets/stl-viewer.js`:

```javascript
// Turns each <div class="stl-viewer" data-stl="..."> into a 3D view of that STL:
// drag to rotate, scroll to zoom, right-drag to pan. three.js comes from the page's import map.
import * as THREE from "three";
import { STLLoader } from "three/addons/loaders/STLLoader.js";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

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
  built["STL · PNG · eval.json · build.json<br/>committed beside the design"]
  ci["CI on every push<br/>tests · lint · models-check · photos · leaks · site"]
  gallery["make docs<br/>gallery pages + Quarto"]
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
	uv run --frozen scripts/gallery.py write
	@set -o pipefail; quarto render website 2>&1 | tee website/.render.log
	@if grep -q 'Unable to resolve link target' website/.render.log; then \
	  echo "docs: an unresolved link, above"; exit 1; fi
	uv run --frozen scripts/gallery.py check-site
	@if command -v lychee >/dev/null; then lychee --offline --no-progress website/_site; \
	else echo "lychee isn't installed: the offline link check runs in CI only"; fi
```

- [ ] **Step 4: Run the checks; they pass.** `make check`. Expected: every test passes twice,
  `gallery: 0 model pages in website/models/`, the render clean but for one WARN that the Models
  listing matches no files (until Task 6 adds the coupon), and
  `site: every model's page, viewer and files are in website/_site`.
- [ ] **Step 5: Commit.** Write the message to `.git/COMMIT_MSG`:

```text
feat(site): 🤖 a gallery page per model, with a 3D viewer

The site had no models. scripts/gallery.py write turns each model's
model.yml and measurements into a page under website/models/ (generated,
git-ignored) with its picture, notes, print settings, measurements,
parameters and downloads, and copies its .stl, .png and .sc beside it; a
bad model.yml is named, and nothing is written. check-site fails when the
rendered site lacks a model's page, viewer or files. The Models page lists
a card per model. website/assets/stl-viewer.js mounts a three.js 0.187.0
view, from jsDelivr through an import map, on each page's viewer div.

The new tests failed first with: ModuleNotFoundError: No module named
'gallery'.

Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-1.md Task 5
Co-Authored-By: <the model's own line>
```

  `git add scripts/gallery.py tests/test_gallery.py website/models.qmd website/_stl-viewer.html website/assets/stl-viewer.js website/_quarto.yml website/styles.css website/_overview.qmd Makefile`, then `git commit -F .git/COMMIT_MSG`, then `git log -1 --format='%(trailers)'` shows the `Plan:` line.
- [ ] **Step 6: Review, look forward, close.** The review includes the viewer seen working: with
  a model in place (Task 6's, or a scratch one not committed), `make docs`, serve
  `website/_site` on a free local port, open a model's page, and confirm its `.stl-viewer` has
  `data-loaded="true"` and a canvas; record it under `Rounds:`.

  - **Review (Tier 2: Matt Pocock's `code-review`, two axes in two subagents; fix Critical and Important; at most one re-review),** from `$(cat .git/TASK_BASE)`.
  - **Forward:** Task 6's `model.yml` must pass `read_meta`; Phase 2's models consume the same fields.
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

  - **Push,** once Dan has OKed it (`AGENTS.md`'s interim line): `make leaks`, then
    `git push origin phase-1`. The task is closed once CI on the closing commit, or a later
    one, is green; until a push, the local checks are the gate.

***

### Task 6: The first model, the dowel fit-test coupon

**Tier:** 2 · **Scenarios:** S09

**Files:**
- Create: `models/dowel-fit-coupon/dowel-fit-coupon.sc` (by SolidCraft), its built files
  (`.stl`, `.png`, `.eval.json`, `build.json`, by `make models`), `models/dowel-fit-coupon/model.yml`,
  `tests/test_coupon.py`

**Interfaces:**
- Consumes: Task 2's `make models`, `Model`, `staleness`; Task 5's `read_meta` and the page.
- Produces: the design's parameters `dowel_d` (25.4 mm), `step` (0.2 mm), `wall`, `margin`,
  `bar_h`, `dot_d`, `dot_depth`, `pitch`, `bar_l`, `bar_w`, which Phase 2's wall block takes its
  `clearance` from (`step` times the dots of the hole that fit).

- [ ] **Step 0: Record the base:** `git rev-parse HEAD > .git/TASK_BASE`.
- [ ] **Step 1: Write the failing tests.**

`tests/test_coupon.py`:

```python
"""The dowel fit-test coupon (S09): four holes at +0.2 to +0.8 mm, marked by 1 to 4 dots."""

from __future__ import annotations

import json
import math
from pathlib import Path

import pytest

import gallery
import models

ROOT = Path(__file__).resolve().parent.parent
COUPON = models.Model(ROOT / "models" / "dowel-fit-coupon")


@pytest.fixture(scope="module")
def evaluation() -> dict:
    return json.loads(COUPON.built("eval.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def params(evaluation: dict) -> dict[str, float]:
    return {p["name"]: p["value"] for p in evaluation["params"]}


def test_the_coupon_is_built_from_its_design() -> None:
    assert models.staleness(COUPON) is None


def test_it_is_for_a_one_inch_dowel_in_steps_of_a_fifth_of_a_millimetre(params) -> None:
    assert params["dowel_d"] == pytest.approx(25.4)
    assert params["step"] == pytest.approx(0.2)


def test_it_is_one_closed_body_with_four_holes_and_ten_dots(evaluation: dict) -> None:
    (body,) = evaluation["bodies"]
    assert body["closed"]
    assert body["face_types"]["cylinder"] == 4 + (1 + 2 + 3 + 4)


def test_its_volume_matches_holes_at_plus_point_two_to_point_eight(evaluation, params) -> None:
    box = params["bar_l"] * params["bar_w"] * params["bar_h"]
    holes = sum(
        math.pi * ((params["dowel_d"] + k * params["step"]) / 2) ** 2 * params["bar_h"]
        for k in range(1, 5)
    )
    dots = 10 * math.pi * (params["dot_d"] / 2) ** 2 * params["dot_depth"]
    assert evaluation["bodies"][0]["volume_mm3"] == pytest.approx(box - holes - dots, rel=1e-3)


def test_its_page_says_how_to_read_each_hole() -> None:
    notes = gallery.read_meta(COUPON)["notes"]
    for dots, hole, clearance in [
        (1, "25.6", "0.2"),
        (2, "25.8", "0.4"),
        (3, "26.0", "0.6"),
        (4, "26.2", "0.8"),
    ]:
        assert f"| {dots} | {hole} mm | +{clearance} mm |" in notes
```

- [ ] **Step 2: Run them; watch them fail.** `make test`. Expected: `FileNotFoundError` for
  `models/dowel-fit-coupon/dowel-fit-coupon.eval.json`, and `staleness` naming the missing build.
- [ ] **Step 3: Build the design.** Write SolidCraft's command script to `.git/coupon-script.json`
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
  `models/dowel-fit-coupon/dowel-fit-coupon.sc` is about 9.5 KB of JSON. Then `make models`.
  Expected: `building models/dowel-fit-coupon (missing …)` and `1 built, 0 up to date`. Look at
  `dowel-fit-coupon.png`: a bar with four holes, one to four dots in front of them.
- [ ] **Step 4: Write its page's text.**

`models/dowel-fit-coupon/model.yml`:

```yaml
title: Dowel fit-test coupon
summary: >-
  One bar with four holes, each a little wider than a 1-inch dowel, to find the clearance your
  printer and your dowel need before printing a part that holds one.
status: designed
material: PETG (PLA is fine for this test)
print:
  Orientation: flat on the bed, holes vertical
  Layer height: 0.2 mm
  Walls: 3
  Infill: 15%
  Supports: none
notes: |
  Dowels sold as 1 inch vary by about half a millimetre, and printers print holes a little
  small, so the hole a dowel needs is found by trying it. The dots beside each hole say how much
  wider than 25.4 mm it is:

  | Dots | Hole | Clearance |
  |---|---|---|
  | 1 | 25.6 mm | +0.2 mm |
  | 2 | 25.8 mm | +0.4 mm |
  | 3 | 26.0 mm | +0.6 mm |
  | 4 | 26.2 mm | +0.8 mm |

  Push the dowel into each hole. The one to use is the tightest it goes into by hand, all the way,
  without a mallet; it should hold the coupon up when you lift the dowel. Every part that holds a
  dowel takes that clearance as its `step` times the dot count. If even four dots is too tight,
  change `step` to 0.3 mm in the design and print it again.
```

- [ ] **Step 5: Run the checks; they pass.** `make check`. Expected: every test passes twice,
  `1 models, every build matches its design`, `2 images, none with a location` (the picture and
  its copy in the generated site folder), and the site's check names the coupon's page as there.
- [ ] **Step 6: Commit.** Write the message to `.git/COMMIT_MSG`:

```text
feat(models): 🤖 add the dowel fit-test coupon

The sconce's socket needs the clearance that suits Dan's dowel and
printer, and dowels sold as 1 inch vary by about half a millimetre. The
coupon is one bar with four holes at 25.4 mm plus 0.2, 0.4, 0.6 and 0.8,
marked by one to four dots, every size a parameter. Built headless by
solidcraft-cli from a command script, saved as plain-text JSON, with its
STL, picture, measurements and build record from make models; its page
says how to read the result.

The new tests failed first with: FileNotFoundError for
models/dowel-fit-coupon/dowel-fit-coupon.eval.json.

Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-1.md Task 6
Co-Authored-By: <the model's own line>
```

  `git add models/dowel-fit-coupon/dowel-fit-coupon.sc models/dowel-fit-coupon/dowel-fit-coupon.stl models/dowel-fit-coupon/dowel-fit-coupon.png models/dowel-fit-coupon/dowel-fit-coupon.eval.json models/dowel-fit-coupon/build.json models/dowel-fit-coupon/model.yml tests/test_coupon.py`, then `git commit -F .git/COMMIT_MSG`, then `git log -1 --format='%(trailers)'` shows the `Plan:` line.
- [ ] **Step 7: Review, look forward, close.** The review looks at the picture and the page's
  viewer, not the `.sc` alone.

  - **Review (Tier 2: Matt Pocock's `code-review`, two axes in two subagents; fix Critical and Important; at most one re-review),** from `$(cat .git/TASK_BASE)`.
  - **Forward:** Phase 2's first task prints this coupon; its wall block takes `clearance` from it.
  - **Docs:** the README's first-project lines; the overview diagram needs no change.
  - **Close,** its own commit: this task's boxes ticked, **Now** set to the next task, any
    Built differently and Ruling lines, deferred findings on the phase-end list, the spec's
    scenario statuses (`built`). The message, from `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 6: The first model, the dowel fit-test coupon

    <what the task built, and why, in a few lines>

    Drift: <filled at the close, or none>
    Rulings: <filled at the close, or none>
    Phase-end: <filled at the close, or none>
    Forward: <filled at the close, or none>
    Tier: 2
    Rounds: <filled at the close>
    Findings: <filled at the close, or none>

    Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-1.md Task 6
    Co-Authored-By: <the model's own line>
    ```

  - **Push,** once Dan has OKed it (`AGENTS.md`'s interim line): `make leaks`, then
    `git push origin phase-1`. The task is closed once CI on the closing commit, or a later
    one, is green; until a push, the local checks are the gate.

***

### Task 7: [Dan] The GitHub settings

**Tier:** none: settings Dan applies on github.com, which never relax (`AGENTS.md`, *Stops*) ·
**Scenarios:** S10

Runs on <https://github.com/chendaniely/3d-models/settings>, by Dan, one step at a time, asked by
*Asking Dan*. **Now** reads `waiting on Dan: <the step>` until each is done.

- [ ] **1. Pages:** Settings → Pages → Source: "GitHub Actions".
- [ ] **2. Merge commits only:** Settings → General → Pull Requests: allow merge commits, its
  message the PR title and description; squash and rebase merging off.
- [ ] **3. A ruleset on `main`:** Settings → Rules → Rulesets → New branch ruleset, target the
  default branch: require a pull request; require the status checks `tests`, `leaks` and `site`;
  block force pushes and deletion; bypass list "For pull requests only" (so the agent's pushes,
  made with Dan's login, aren't exempt). Classic branch protection instead, if rulesets aren't
  offered.
- [ ] **4. The website field and topics:** the agent drafts
  `gh repo edit --homepage https://chendaniely.github.io/3d-models/ --add-topic 3d-printing
  --add-topic solidcraft --add-topic vibe-coded`; Dan runs it, or says the agent may.
- [ ] **5. Close:** the agent ticks these boxes and sets **Now** to the phase end, in
  `docs(plan): 🤖 close Task 7: The GitHub settings` (every heading `none` but `Rulings:`, which
  names anything Dan chose differently), with this plan's `Plan:` line.

***

### Task 8: Phase end

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
  `docs/superpowers/plans/2026-11-05-3d-models-phase-1-end-council.md`, with its wrapper and
  Design-page line; each claim checked; each finding a severity and a decision.
- [ ] **4. The phase-end list worked through:** each item fixed in its own commit at its tier, or
  moved to the spec's Later with a reason; missing docs written; built parts solid in the diagrams.
- [ ] **5. The forward look:** Phase 2's plan rewritten to fit what was built; its listings run
  against this code where they can.
- [ ] **6. The retro:** `docs/superpowers/plans/2026-11-05-3d-models-phase-1-retro.md` (departures,
  items carried forward, metrics per tier, starting over), with its wrapper and Design-page line;
  the retuning rules applied to Phase 2's tiers.
- [ ] **7. The changelog and status:** a dated `CHANGELOG.md` entry; the README's status line says
  the gallery is live; the spec's status line `Phase 1 PR open (#N)`, N filled once step 8 opens
  it.
- [ ] **8. The PR:** title `chore(repo): 🤖 merge Phase 1: the repo`; the body summarizes each
  task, the council's findings and their fate, links the retro, lists every file no scan can read
  (`git log --format= --numstat origin/main..HEAD | awk '$1 == "-" { print "not scanned, check by
  eye: " $3 }'`), and ends `Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-1.md Phase end`. Title and body in `.git/PR_TITLE` and
  `.git/PR_BODY.md`, scanned with `gitleaks stdin --redact --no-banner` before
  `gh pr create --base main --head phase-1 --title "$(cat .git/PR_TITLE)" --body-file
  .git/PR_BODY.md`. Fully vibed, the agent merges it once CI is green, with
  `gh pr merge <N> --merge --match-head-commit <sha>` and the subject
  `chore(repo): 🤖 merge Phase 1: the repo (#N)`, never `--admin`, squash, rebase or
  `--delete-branch`; but the PR adds STL and PNG files no scan can read, so it waits for Dan's look
  at them first (`AGENTS.md`, *Stops*).
- [ ] **9. After the merge:** <https://chendaniely.github.io/3d-models/models/dowel-fit-coupon.html>
  serves the coupon, and its viewer loads (S08, S10).

***

## Phase-end list

| Source | Severity | File | Item | Status |
|---|---|---|---|---|
