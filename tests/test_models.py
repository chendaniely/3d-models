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


TYPO = SIZES.replace("{dowel_d: 25", "{dowel_dd: 25")  # a parameter the design hasn't
UNKNOWN = (
    "models: models/clamp/model.yml: size '25 mm' changes 'dowel_dd', which the design has no "
    "parameter named"
)


def test_build_refuses_a_size_changing_a_parameter_the_design_has_not(
    repo: Path, fake_cli: Path, capsys
) -> None:
    design = add_design(repo, "clamp")
    (design.parent / "model.yml").write_text(TYPO, encoding="utf-8")
    assert models.main(["build"], root=repo) == 1
    assert UNKNOWN in capsys.readouterr().err
    assert not (design.parent / "build.json").exists()


def test_check_names_a_size_changing_a_parameter_the_design_has_not(
    repo: Path, fake_cli: Path, capsys
) -> None:
    design = add_design(repo, "clamp")
    (design.parent / "model.yml").write_text(SIZES, encoding="utf-8")
    models.main(["build"], root=repo)
    (design.parent / "model.yml").write_text(TYPO, encoding="utf-8")
    assert models.main(["check"], root=repo) == 1
    assert UNKNOWN in capsys.readouterr().err
    before = len(calls(fake_cli))
    assert models.main(["build"], root=repo) == 1  # no build fixes a typo: it builds nothing
    assert UNKNOWN in capsys.readouterr().err
    assert len(calls(fake_cli)) == before


def test_build_takes_a_size_changing_a_parameter_the_design_just_gained(
    repo: Path, fake_cli: Path
) -> None:
    design = add_design(repo, "clamp")
    (design.parent / "model.yml").write_text(SIZES, encoding="utf-8")
    models.main(["build"], root=repo)
    design.write_text('{"params": ["dowel_d", "ring_d"]}', encoding="utf-8")
    (design.parent / "model.yml").write_text(SIZES + "  wide: {ring_d: 40 mm}\n", encoding="utf-8")
    assert models.main(["build"], root=repo) == 0  # the old eval.json, which lacks it, is stale
    assert models.main(["check"], root=repo) == 0


@pytest.mark.parametrize(
    ("yml", "message"),
    [
        (
            "sizes:\n  3/4 in: {dowel_d: 19.05 mm}\n  3-4 in: {dowel_d: 19 mm}\n",
            "models: models/clamp/model.yml: sizes '3/4 in' and '3-4 in' give the same file "
            "name, clamp-3-4in.stl\n",
        ),
        (
            "sizes:\n  '!!': {dowel_d: 19 mm}\n",
            "models: models/clamp/model.yml: size '!!' gives an empty file name: a size needs a "
            "letter or a digit\n",
        ),
    ],
)
def test_build_and_check_refuse_sizes_whose_file_names_collide_or_are_empty(
    repo: Path, fake_cli: Path, capsys, yml: str, message: str
) -> None:
    design = add_design(repo, "clamp")
    (design.parent / "model.yml").write_text(yml, encoding="utf-8")
    assert models.main(["check"], root=repo) == 1
    assert capsys.readouterr().err == message
    assert models.main(["build"], root=repo) == 1
    assert capsys.readouterr().err == message
    assert calls(fake_cli) == []


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
    assert f"models: models/{slug}: its folder name must be lowercase words joined by hyphens" in (
        capsys.readouterr().err
    )


@pytest.mark.parametrize("name", ["Hook.sc", "hook-v2.sc"])
def test_check_names_a_design_not_named_after_its_folder(repo: Path, capsys, name: str) -> None:
    folder = repo / "models" / "hook"
    folder.mkdir()
    (folder / name).write_text("{}", encoding="utf-8")
    assert models.main(["check"], root=repo) == 1
    assert f"models: models/hook: the design must be hook.sc alone, not {name}" in (
        capsys.readouterr().err
    )


def test_check_names_unreadable_sizes(repo: Path, capsys) -> None:
    design = add_design(repo, "clamp")
    (design.parent / "model.yml").write_text("sizes: [3/4 in]\n", encoding="utf-8")
    assert models.main(["check"], root=repo) == 1
    err = capsys.readouterr().err
    assert "models: models/clamp/model.yml: 'sizes' must map each size to parameter changes" in err
    assert "stale:" not in err


@pytest.mark.parametrize(
    ("text", "message"),
    [
        ("sizes: [unclosed\n", "models: models/clamp/model.yml isn't valid YAML: "),
        ("- a list, not fields\n", "models: models/clamp/model.yml must be a mapping of fields\n"),
    ],
)
def test_check_names_a_model_yml_it_cannot_read(
    repo: Path, capsys, text: str, message: str
) -> None:
    design = add_design(repo, "clamp")
    (design.parent / "model.yml").write_text(text, encoding="utf-8")
    assert models.main(["check"], root=repo) == 1
    err = capsys.readouterr().err
    assert message in err
    assert "stale:" not in err


def test_read_yml_reads_no_model_yml_as_no_fields(repo: Path) -> None:
    design = add_design(repo, "clamp")
    assert models.read_yml(models.Model(design.parent)) == {}


@pytest.mark.parametrize(
    ("slug", "yml", "message"),
    [
        ("Wall Hook", None, "models: models/Wall Hook: its folder name must be lowercase"),
        ("clamp", "sizes: [unclosed\n", "models: models/clamp/model.yml isn't valid YAML"),
    ],
)
def test_build_refuses_an_invalid_model_instead_of_building_it(
    repo: Path, fake_cli: Path, capsys, slug: str, yml: str | None, message: str
) -> None:
    design = add_design(repo, slug)
    if yml:
        (design.parent / "model.yml").write_text(yml, encoding="utf-8")
    assert models.main(["build"], root=repo) == 1
    assert message in capsys.readouterr().err
    assert calls(fake_cli) == []


def test_check_ignores_a_folder_without_a_design(repo: Path, capsys) -> None:
    (repo / "models" / "notes").mkdir()
    assert models.main(["check"], root=repo) == 0
    assert "0 models" in capsys.readouterr().out
