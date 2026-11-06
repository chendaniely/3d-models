"""The Makefile is the front door: every target AGENTS.md names is there, and help lists it."""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS = [
    "help", "hooks", "check", "test", "test-utc", "lint", "leaks",
    "models", "models-check", "privacy", "strip", "docs",
]  # fmt: skip


def test_help_lists_every_target() -> None:
    result = subprocess.run(
        ["make", "--no-print-directory", "help"], cwd=ROOT, capture_output=True, text=True,
        check=True,
    )  # fmt: skip
    listed = {line.split()[0] for line in result.stdout.splitlines() if line.strip()}
    assert set(TARGETS) <= listed, sorted(set(TARGETS) - listed)
