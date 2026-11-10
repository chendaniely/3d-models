"""Build and check the models under models/.

    uv run scripts/models.py build [SLUG ...]
        rebuild each model whose design, sizes or built files changed since its build.json
        (needs solidcraft-cli); refuse, building nothing, while a model is invalid
    uv run scripts/models.py check
        fail, naming each model, when it is invalid (a folder name that can't be a URL, no
        design, a misnamed or extra design, a model.yml or sizes it can't read, sizes giving one
        file name or none, a size changing a parameter the design hasn't: no build fixes these)
        or stale (a build is missing or doesn't match its design: make models fixes it)

A model is a folder models/<slug>/ holding the design <slug>.sc; a folder holding anything but
hidden files (Finder's .DS_Store) and no design is named as invalid. A build writes, beside it:
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
        if folder.is_dir() and any(not p.name.startswith(".") for p in folder.iterdir())
    ]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_yml(model: Model) -> dict:
    """model.yml's fields, {} when there's no model.yml; a ValueError, naming it, when it can't
    be read as a mapping of fields."""
    path = model.folder / "model.yml"
    if not path.is_file():
        return {}
    where = f"models/{model.slug}/model.yml"
    try:
        meta = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        raise ValueError(f"{where} isn't valid YAML: {error}") from error
    if meta is None:
        return {}
    if not isinstance(meta, dict):
        raise ValueError(f"{where} must be a mapping of fields")
    return meta


def sizes(model: Model) -> dict[str, dict[str, str]]:
    """The extra sizes model.yml lists: {'3/4 in': {'dowel_d': '19.05 mm'}, ...}."""
    listed = read_yml(model).get("sizes") or {}
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


def clashing_sizes(model: Model, wanted: dict[str, dict[str, str]]) -> str | None:
    """Sizes whose file name is empty, or the same as another's ('3/4 in' and '3-4 in'), named;
    or None. Either would build one size's STL over another's, or as <slug>-.stl."""
    by_name: dict[str, list[str]] = {}
    for size in wanted:
        by_name.setdefault(size_name(size), []).append(size)
    where = f"models/{model.slug}/model.yml"
    for name, group in sorted(by_name.items()):
        listed = " and ".join(f"'{size}'" for size in group)
        noun, verb = ("size", "gives") if len(group) == 1 else ("sizes", "give")
        if not name:  # sorted first
            return (
                f"{where}: {noun} {listed} {verb} an empty file name: a size needs a letter or a "
                "digit"
            )
        if len(group) > 1:
            return f"{where}: sizes {listed} give the same file name, {model.slug}-{name}.stl"
    return None


def parameter_names(model: Model) -> set[str]:
    """A design's parameters: the numbers its eval.json lists, and the texts (a label it
    engraves) that only the design itself lists, under text_params."""
    measured = json.loads(model.built("eval.json").read_text(encoding="utf-8"))
    names = {param["name"] for param in measured.get("params", [])}
    try:
        design = json.loads(model.design.read_text(encoding="utf-8"))
    except ValueError:
        return names
    texts = design.get("text_params") if isinstance(design, dict) else None
    if not isinstance(texts, list):
        return names
    named = [text.get("name") for text in texts if isinstance(text, dict)]
    return names | {name for name in named if isinstance(name, str)}


def unknown_parameter(model: Model, wanted: dict[str, dict[str, str]]) -> str | None:
    """The first size that changes a parameter the design doesn't have, or None. Without this,
    solidcraft-cli builds the base geometry under the size's name and exits 0."""
    names = parameter_names(model)
    for size, changes in wanted.items():
        for name in changes:
            if name not in names:
                return (
                    f"models/{model.slug}/model.yml: size '{size}' changes '{name}', which the "
                    "design has no parameter named"
                )
    return None


def measured_now(model: Model) -> bool:
    """Whether build.json vouches for the design as it is now, so its eval.json measured it; a
    design changed since may have gained the parameter a size changes, and its build checks."""
    try:
        record = json.loads(model.record.read_text(encoding="utf-8"))
        return record["sha256"] == sha256(model.design) and model.built("eval.json").is_file()
    except (OSError, json.JSONDecodeError, KeyError, TypeError):
        return False


def invalid(model: Model) -> str | None:
    """What's wrong with the model that no build can fix, starting with where, or None."""
    where = f"models/{model.slug}"
    if not SLUG.fullmatch(model.slug):
        return (
            f"{where}: its folder name must be lowercase words joined by hyphens, as the page's URL"
        )
    designs = sorted(p.name for p in model.folder.iterdir() if p.suffix.lower() == ".sc")
    if not designs:
        return f"{where}: no design: save it as {model.design.name}"
    if designs != [model.design.name]:
        return f"{where}: the design must be {model.design.name} alone, not {', '.join(designs)}"
    try:
        wanted = sizes(model)
    except ValueError as error:
        return str(error)
    clash = clashing_sizes(model, wanted)
    if clash:
        return clash
    if measured_now(model):
        try:
            return unknown_parameter(model, wanted)
        except (json.JSONDecodeError, KeyError, TypeError, AttributeError):
            return None  # an eval.json it can't read: staleness names it against build.json
    return None


def staleness(model: Model) -> str | None:
    """Why a valid model needs a build, or None when its built files match its design."""
    wanted = outputs(model)
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
    reason = unknown_parameter(model, wanted_sizes)
    if reason:
        raise ValueError(reason)
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
    refused = [reason for m in chosen if (reason := invalid(m)) is not None]
    for reason in refused:
        print(f"models: {reason}", file=sys.stderr)
    if refused:
        return 1
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
    broken = {m.slug: reason for m in models if (reason := invalid(m)) is not None}
    for reason in broken.values():
        print(f"models: {reason}", file=sys.stderr)
    valid = [m for m in models if m.slug not in broken]
    stale = [(m, reason) for m in valid if (reason := staleness(m)) is not None]
    for model, reason in stale:
        print(f"stale: models/{model.slug}: {reason}; run make models", file=sys.stderr)
    if broken or stale:
        return 1
    print(f"{len(models)} models, every build matches its design")
    return 0


def main(argv: list[str] | None = None, root: Path = ROOT) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    build_parser = sub.add_parser("build", help="rebuild each changed model")
    build_parser.add_argument("slugs", nargs="*", metavar="SLUG")
    sub.add_parser("check", help="fail when a model is invalid, or its build missing or stale")
    args = parser.parse_args(argv)
    if args.command == "build":
        return command_build(root, args.slugs)
    return command_check(root)


if __name__ == "__main__":
    sys.exit(main())
