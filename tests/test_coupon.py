"""The dowel fit-test coupon (S09): four holes at +0.2 to +0.8 mm, marked by 1 to 4 dots."""

from __future__ import annotations

import math
from pathlib import Path

import pytest

import gallery
import models
from conftest import body, params

COUPON = models.Model(Path(__file__).resolve().parent.parent / "models" / "dowel-fit-coupon")


def test_it_is_saved_for_a_one_inch_dowel_in_steps_of_a_fifth_of_a_millimetre() -> None:
    assert params(COUPON)["dowel_d"] == pytest.approx(25.4)
    assert params(COUPON)["step"] == pytest.approx(0.2)


def test_it_comes_in_three_dowel_sizes() -> None:
    assert models.sizes(COUPON) == {
        "3/4 in": {"dowel_d": "19.05 mm"},
        "25 mm": {"dowel_d": "25 mm"},
    }


def test_it_is_one_closed_body_with_four_holes_and_ten_dots() -> None:
    coupon = body(COUPON, "Coupon")
    assert coupon["closed"]
    assert coupon["face_types"]["cylinder"] == 4 + (1 + 2 + 3 + 4)


def test_its_volume_matches_holes_at_plus_point_two_to_point_eight() -> None:
    p = params(COUPON)
    box = p["bar_l"] * p["bar_w"] * p["bar_h"]
    holes = sum(
        math.pi * ((p["dowel_d"] + k * p["step"]) / 2) ** 2 * p["bar_h"] for k in (1, 2, 3, 4)
    )
    dots = 10 * math.pi * (p["dot_d"] / 2) ** 2 * p["dot_depth"]
    assert body(COUPON, "Coupon")["volume_mm3"] == pytest.approx(box - holes - dots, rel=1e-3)


def test_its_page_says_how_to_read_each_hole_and_how_to_print_it() -> None:
    meta = gallery.read_meta(COUPON)
    for dots, clearance, hole in [(1, "0.2", "25.6"), (2, "0.4", "25.8"), (3, "0.6", "26.0"),
                                  (4, "0.8", "26.2")]:  # fmt: skip
        assert f"| {dots} | +{clearance} mm | {hole} mm |" in meta["notes"]
    assert "the holes horizontal" in meta["print"]["Orientation"]
