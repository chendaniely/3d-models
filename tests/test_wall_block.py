"""The sconce's wall block (S12): a deep socket, screws far apart and hidden, the coupon's fit."""

from __future__ import annotations

from pathlib import Path

import pytest

import models
from conftest import body, params

MODELS = Path(__file__).resolve().parent.parent / "models"
WALL_BLOCK = models.Model(MODELS / "sconce-wall-block")
COUPON = models.Model(MODELS / "dowel-fit-coupon")
SCREW_HEAD_MM = 3.0  # a #8 or #10 pan or washer head, and a toggle bolt's


def test_the_block_is_one_closed_body_with_two_caps_beside_it() -> None:
    assert body(WALL_BLOCK, "Wall block")["closed"]
    assert body(WALL_BLOCK, "Cap 1")["closed"] and body(WALL_BLOCK, "Cap 2")["closed"]


def test_it_is_saved_for_one_inch_and_comes_in_three_sizes() -> None:
    assert params(WALL_BLOCK)["dowel_d"] == pytest.approx(25.4)
    assert set(models.sizes(WALL_BLOCK)) == {"3/4 in", "25 mm"}


def test_the_socket_is_at_least_two_inches_deep() -> None:
    assert params(WALL_BLOCK)["socket_depth"] >= 51.0


def test_the_screws_are_at_least_100_mm_apart() -> None:
    p = params(WALL_BLOCK)
    assert p["screw_spacing"] >= 100.0
    assert p["plate_h"] > p["screw_spacing"] + p["head_d"]


def test_each_screw_head_sinks_below_the_face_with_room_for_its_cap() -> None:
    p, cap = params(WALL_BLOCK), body(WALL_BLOCK, "Cap 1")["bbox"]
    assert p["head_depth"] >= SCREW_HEAD_MM + p["cap_h"]
    assert p["head_depth"] < p["plate_t"]
    assert cap["max"][2] - cap["min"][2] == pytest.approx(p["cap_h"])


def test_the_socket_takes_one_of_the_coupons_clearances() -> None:
    p, step = params(WALL_BLOCK), params(COUPON)["step"]
    assert p["socket_d"] == pytest.approx(p["dowel_d"] + p["clearance"])
    assert any(p["clearance"] == pytest.approx(k * step) for k in (1, 2, 3, 4))


def test_the_block_reaches_its_socket_depth_out_from_the_wall() -> None:
    p, bbox = params(WALL_BLOCK), body(WALL_BLOCK, "Wall block")["bbox"]
    assert bbox["max"][0] - bbox["min"][0] == pytest.approx(p["plate_t"] + p["socket_depth"])
