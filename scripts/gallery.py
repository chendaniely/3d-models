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

from models import ROOT, Model, find_models, read_yml, sizes
from privacy import READABLE as PHOTOS
from sitedocs import escaped

REPO_URL = "https://github.com/chendaniely/3d-models"
LICENCE = (
    "[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/): print it, change it and "
    f"share it, crediting chendaniely and linking to <{REPO_URL}>; don't sell it or prints of it."
)
STATUSES = ("designed", "printed", "in use")
FREE_TEXT = ("title", "summary", "status", "material", "notes")  # escaped for Quarto, as sitedocs
DENSITY_G_CM3 = {"PLA": 1.24, "PETG": 1.27}


class ModelError(ValueError):
    """A model.yml or eval.json that can't make a page."""


def read_meta(model: Model) -> dict:
    path = model.folder / "model.yml"
    if not path.is_file():
        raise ModelError(f"models/{model.slug}: no model.yml")
    where = f"models/{model.slug}/model.yml"
    try:
        meta = read_yml(model)
    except ValueError as error:
        raise ModelError(str(error)) from error
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


def copied(model: Model, meta: dict) -> list[Path]:
    """Every built file a model's page copies beside it, photos aside."""
    files = [model.built("stl"), model.built("png"), model.design]
    return files + [model.sized(size) for size in meta["sizes"]]


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


def downloads(model: Model, meta: dict, params: set[str]) -> list[str]:
    """The Files section; params, the design's parameter names, says whether to name clearance."""
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
        fit = ""
        if "clearance" in params and "clearance" not in names:
            fit = ", and `clearance` for your printer's fit (the fit-test coupon finds it)"
        lines += [
            "**For another size:** open the `.sc` in SolidCraft and change "
            f"{changed} under Parameters{fit}; every other dimension follows.",
            "",
        ]
    return lines


def page(model: Model, meta: dict, evaluation: dict) -> str:
    meta = meta | {field: escaped(meta[field]) for field in FREE_TEXT if field in meta}
    slug = model.slug
    alt = meta["title"].replace("[", "\\[").replace("]", "\\]")  # a bracket would end it early
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
        f"![{alt}, as SolidCraft draws it]({slug}/{slug}.png)"
        f"{{fig-alt={quoted(meta['title'] + ', seen from above at an angle')}}}",
        "",
    ]
    if meta.get("notes", "").strip():
        lines += ["## Notes", "", meta["notes"].strip(), ""]
    shots = photos(model)
    if shots:
        lines += ["## Photos", ""]
        lines += [
            f"![{shot.stem.replace('-', ' ').replace('_', ' ')}]({slug}/photos/{shot.name})"
            for shot in shots
        ]
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
    lines += downloads(model, meta, {param["name"] for param in params})
    lines += ["## Licence", "", LICENCE, ""]
    return "\n".join(lines)


def main(argv: list[str] | None = None, root: Path = ROOT) -> int:
    out = root / "website" / "models"
    models = find_models(root)
    try:
        pages = [(m, read_meta(m)) for m in models]
        pages = [(m, meta, page(m, meta, read_eval(m))) for m, meta in pages]
        for model, meta, _ in pages:
            for source in copied(model, meta):
                if not source.is_file():
                    raise ModelError(f"models/{model.slug}: no {source.name}; run make models")
    except ModelError as error:
        print(f"gallery: {error}", file=sys.stderr)
        return 1
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)
    for model, meta, text in pages:
        (out / f"{model.slug}.qmd").write_text(text, encoding="utf-8")
        files = out / model.slug
        files.mkdir()
        for source in copied(model, meta):
            shutil.copy2(source, files / source.name)
        if photos(model):
            (files / "photos").mkdir()
            for shot in photos(model):
                shutil.copy2(shot, files / "photos" / shot.name)
    print(f"gallery: {len(pages)} model pages in website/models/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
