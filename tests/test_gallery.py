"""scripts/gallery.py: a card and a page per model (S07), with a 3D viewer, downloads for each size,
photos and a licence (S08, S19)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from PIL import Image

import gallery
import models
from conftest import add_design
from sitedocs import escaped

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
    assert "crediting chendaniely and linking to <https://github.com/chendaniely/3d-models>" in text


def test_a_model_with_sizes_offers_an_stl_for_each(repo: Path) -> None:
    add_model(repo, meta=SIZED)
    text = page(repo)
    assert "- [hook.stl](hook/hook.stl): the mesh to slice, for 1 in" in text
    assert "- [hook-3-4in.stl](hook/hook-3-4in.stl): for 3/4 in" in text
    assert "- [hook-25mm.stl](hook/hook-25mm.stl): for 25 mm" in text
    assert "change `dowel_d` under Parameters; every other dimension follows." in text
    files = sorted(p.name for p in (repo / "website" / "models" / "hook").iterdir())
    assert files == ["hook-25mm.stl", "hook-3-4in.stl", "hook.png", "hook.sc", "hook.stl"]


def test_the_size_note_names_clearance_when_the_design_has_it(repo: Path) -> None:
    folder = add_model(repo, meta=SIZED)
    clearance = {"name": "clearance", "expression": "0.4 mm", "unit": "mm", "value": 0.4}
    evaluation = EVAL | {"params": [*EVAL["params"], clearance]}
    (folder / "hook.eval.json").write_text(json.dumps(evaluation), encoding="utf-8")
    assert (
        "**For another size:** open the `.sc` in SolidCraft and change `dowel_d` under "
        "Parameters, and `clearance` for your printer's fit (the fit-test coupon finds it); "
        "every other dimension follows."
    ) in page(repo)


def test_a_model_with_sizes_names_the_size_it_is_saved_at(repo: Path, capsys) -> None:
    add_model(repo, meta=SIZED.replace("size: 1 in\n", ""))
    assert gallery.main([], root=repo) == 1
    assert "'size' names the size the design is saved at" in capsys.readouterr().err


def test_photos_are_published_on_the_page(repo: Path) -> None:
    folder = add_model(repo)
    (folder / "photos").mkdir()
    Image.new("RGB", (8, 8)).save(folder / "photos" / "installed.jpg")
    text = page(repo)
    assert "## Photos\n\n![installed](hook/photos/installed.jpg)" in text
    assert (repo / "website" / "models" / "hook" / "photos" / "installed.jpg").is_file()


def test_each_photo_s_alt_text_is_its_name_in_words(repo: Path) -> None:
    folder = add_model(repo)
    (folder / "photos").mkdir()
    Image.new("RGB", (8, 8)).save(folder / "photos" / "on_the-wall.png")
    assert "![on the wall](hook/photos/on_the-wall.png)" in page(repo)


SHORTCODE = "{" * 2 + "< meta title >" + "}" * 2  # spelt in parts, so a plan can quote this file


def test_notes_holding_a_shortcode_and_a_cell_fence_come_out_escaped(repo: Path) -> None:
    notes = f"notes: |\n  See {SHORTCODE}.\n\n  ```{{python}}\n  print(1)\n  ```\n"
    add_model(repo, meta=META.replace("notes: Hang it on a dowel.\n", notes))
    text = page(repo)
    assert SHORTCODE not in text
    assert "See " + "{" * 2 + "</* meta title */>" + "}" * 2 + "." in text
    assert "```{python}" not in text
    assert "```python\nprint(1)\n```" in text


def test_the_other_free_text_comes_out_escaped(repo: Path) -> None:
    meta = META.replace("title: Test hook", f"title: Hook {SHORTCODE}")
    meta = meta.replace("summary: A hook for testing.", f"summary: A hook, {SHORTCODE}.")
    meta = meta.replace("material: PETG", f"material: PETG {SHORTCODE}")
    add_model(repo, meta=meta)
    assert SHORTCODE not in page(repo)


def test_print_settings_and_the_size_come_out_escaped(repo: Path) -> None:
    meta = SIZED.replace("Infill: 20%", f"Infill: 20% {SHORTCODE}")
    add_model(repo, meta=meta.replace("size: 1 in", f"size: 1 in {SHORTCODE}"))
    assert SHORTCODE not in page(repo)


def test_size_names_and_photo_names_come_out_escaped(repo: Path) -> None:
    odd = f"25 mm {SHORTCODE}"
    folder = add_model(repo, meta=SIZED.replace("  25 mm:", f'  "{odd}":'))
    models.Model(folder).sized(odd).write_bytes(b"solid")
    (folder / "photos").mkdir()
    Image.new("RGB", (8, 8)).save(folder / "photos" / f"wall {SHORTCODE}.png")
    text = page(repo)
    assert SHORTCODE not in text
    assert f": for 25 mm {escaped(SHORTCODE)}" in text
    assert f"![wall {escaped(SHORTCODE)}](hook/photos/wall%20%7B%7B%3C%20meta%20title" in text


def test_a_bracket_in_a_photo_s_name_stays_inside_its_alt_text(repo: Path) -> None:
    folder = add_model(repo)
    (folder / "photos").mkdir()
    Image.new("RGB", (8, 8)).save(folder / "photos" / "on the wall [v2].png")
    assert "![on the wall \\[v2\\]](hook/photos/on%20the%20wall%20%5Bv2%5D.png)" in page(repo)


def test_a_bracket_in_the_title_stays_inside_the_picture_s_alt_text(repo: Path) -> None:
    add_model(repo, meta=META.replace("title: Test hook", "title: Hook [v2]"))
    assert "![Hook \\[v2\\], as SolidCraft draws it](hook/hook.png)" in page(repo)


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


@pytest.mark.parametrize(
    ("meta", "missing"),
    [(META, "hook.stl"), (META, "hook.png"), (META, "hook.sc"), (SIZED, "hook-25mm.stl")],
)
def test_write_names_a_missing_built_file_and_keeps_the_old_pages(
    repo: Path, capsys, meta: str, missing: str
) -> None:
    folder = add_model(repo, meta=meta)
    (folder / missing).unlink()
    if missing == "hook.sc":
        (folder / "hook-old.sc").write_text("{}", encoding="utf-8")  # still a model folder
    old = repo / "website" / "models" / "old.qmd"
    old.parent.mkdir(parents=True)
    old.write_text("old", encoding="utf-8")
    assert gallery.main([], root=repo) == 1
    assert f"gallery: models/hook: no {missing}; run make models" in capsys.readouterr().err
    assert old.exists()
