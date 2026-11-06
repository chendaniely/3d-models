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
