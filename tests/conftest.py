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
    try:  # a design's parameters: a JSON design's "params" names, else dowel_d alone
        names = json.loads(design.read_bytes()).get("params", ["dowel_d"])
    except ValueError:
        names = ["dowel_d"]
    params = [{"name": name, "expression": "1 mm", "unit": "mm", "value": 1.0} for name in names]
    measured = {"bodies": [], "params": params}
    Path(args[args.index("--json-out") + 1]).write_text(json.dumps(measured))
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


def standing_on(model, base: str) -> list[dict]:
    """Every body but a model's base: its raised words and ticks, each its own closed body standing
    on the base's top (SolidCraft joins many small solids slowly)."""
    return [b for b in measured(model)["bodies"] if b["name"] != base]


def lettering(model) -> list[tuple[str, float, float, float]]:
    """Every text a model's design letters, raised or cut: (its words, x, y, height), from the saved
    design."""
    found = []

    def walk(node) -> None:
        if isinstance(node, dict):
            if node.get("type") == "text" and "at" in node:
                found.append((node["text"], node["at"][0], node["at"][1], node["height"]))
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(json.loads(model.design.read_text(encoding="utf-8")))
    return found
