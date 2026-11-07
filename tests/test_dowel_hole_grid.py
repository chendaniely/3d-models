"""The hole grid (S34): a tile for each dowel size from 1/2 to 2 inches, its six holes from
0.6 mm under the size to 0.4 mm over, each engraved with its own diameter."""

from __future__ import annotations

import math
from fractions import Fraction
from pathlib import Path

import pytest

import models
from conftest import body, engraved, params

GRID = models.Model(Path(__file__).resolve().parent.parent / "models" / "dowel-hole-grid")
PLATE_MM = 256.0  # a Bambu P2S prints up to 256 mm square
OFFSETS = [-0.6, -0.4, -0.2, 0.0, 0.2, 0.4]


def label(size: Fraction) -> str:
    """The name engraved on a tile: '1/2 in', '1 in', '1 1/8 in'."""
    whole, part = divmod(size, 1)
    words = [str(whole)] if whole else []
    if part:
        words.append(f"{part.numerator}/{part.denominator}")
    return " ".join(words) + " in"


def listed_as(size: Fraction) -> str:
    """Its name in model.yml's sizes, a mixed number hyphenated so its file name reads well:
    '1-1/8 in' gives dowel-hole-grid-1-1-8in.stl."""
    return label(size).replace(" ", "-", 1) if size > 1 and size.denominator > 1 else label(size)


def test_it_is_saved_for_a_one_inch_dowel_in_steps_of_a_fifth_of_a_millimetre() -> None:
    p = params(GRID)
    assert p["dowel_d"] == pytest.approx(25.4)
    assert p["step"] == pytest.approx(0.2)


def test_its_six_holes_run_from_point_six_under_the_size_to_point_four_over() -> None:
    p = params(GRID)
    assert [p[f"h{i}"] - p["dowel_d"] for i in range(1, 7)] == pytest.approx(OFFSETS)


def test_it_comes_in_every_eighth_of_an_inch_from_a_half_to_two() -> None:
    eighths = [Fraction(k, 8) for k in range(4, 17) if k != 8]  # 1 inch is the saved size
    listed = models.sizes(GRID)
    assert list(listed) == [listed_as(size) for size in eighths]
    for size in eighths:
        changes = listed[listed_as(size)]
        assert float(changes["dowel_d"].removesuffix(" mm")) == pytest.approx(float(size) * 25.4)
        assert changes["label"] == label(size)


def test_even_the_two_inch_tile_fits_the_printers_plate() -> None:
    p = params(GRID)
    assert p["pitch"] == pytest.approx(p["h6"] + p["wall"])
    assert p["tile_l"] == pytest.approx(3 * p["pitch"] + p["wall"])
    assert p["tile_w"] == pytest.approx(2 * p["band"] + 2 * p["pitch"] + p["head"])
    pitch = 50.8 + OFFSETS[-1] + p["wall"]
    assert 3 * pitch + p["wall"] <= PLATE_MM
    assert 2 * p["band"] + 2 * pitch + p["head"] <= PLATE_MM


def test_it_is_one_closed_tile_with_its_holes_and_a_ring_hole() -> None:
    p, tile = params(GRID), body(GRID, "Tile")
    assert tile["closed"]
    low, high = tile["bbox"]["min"], tile["bbox"]["max"]
    assert [high[i] - low[i] for i in range(3)] == pytest.approx(
        [p["tile_l"], p["tile_w"], p["thick"]]
    )
    holes = sum(math.pi * (p[f"h{i}"] / 2) ** 2 for i in range(1, 7))
    ring = math.pi * (p["ring_d"] / 2) ** 2
    solid = (p["tile_l"] * p["tile_w"] - holes - ring) * p["thick"]
    engraved = solid - tile["volume_mm3"]
    assert 0 < engraved < 0.05 * p["tile_l"] * p["tile_w"] * p["engrave"]


def test_each_holes_diameter_is_engraved_just_under_it_and_clear_of_the_next() -> None:
    p = params(GRID)
    labels = {words: (x, y, height) for words, x, y, height in engraved(GRID)}
    below_top = p["band"] + p["pitch"] / 2 + p["h6"] / 2  # the top of the lower row's widest hole
    for i in range(6):
        row, col = divmod(i, 3)  # row 0 on top
        d = p[f"h{i + 1}"]
        x, y, height = labels[f"{d:.1f}"]
        centre_y = 2 * p["band"] + 1.5 * p["pitch"] if row == 0 else p["band"] + p["pitch"] / 2
        assert x == pytest.approx(p["wall"] / 2 + p["pitch"] / 2 + col * p["pitch"])
        assert 0 < centre_y - d / 2 - (y + height) <= 2.0  # just under its own hole
        if row == 0:
            assert y - below_top >= 5.0  # and well above the hole under it


def test_its_page_says_how_to_read_each_hole_and_how_to_print_it() -> None:
    meta = models.read_yml(GRID)
    assert meta["material"].startswith("PLA")
    for at, offset, hole in [("top left", "-0.6", "24.8"), ("bottom left", "0", "25.4"),
                             ("bottom right", "+0.4", "25.8")]:  # fmt: skip
        assert f"| {at} | {offset} mm | {hole} mm |" in meta["notes"]
    assert "goes through no hole" in meta["notes"]
    assert meta["print"]["Orientation"].startswith("flat")
