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
