"""The rail's wall feet (S28, S14, S32): cups for the rail's ends, screws the room can't see, and
a rail that can't be lifted out of them."""

from __future__ import annotations

from pathlib import Path

import pytest

import models
from conftest import body, params

MODELS = Path(__file__).resolve().parent.parent / "models"
FEET = models.Model(MODELS / "rail-feet")
COUPON = models.Model(MODELS / "dowel-fit-coupon")
SCREW_HEAD_MM = 3.0  # a #8 or #10 pan or washer head, and a toggle bolt's


def test_two_feet_and_two_caps_each_one_closed_body() -> None:
    for name in ("Bottom foot", "Top foot", "Cap 1", "Cap 2"):
        assert body(FEET, name)["closed"]


def test_it_is_saved_for_one_inch_and_comes_in_three_sizes() -> None:
    assert params(FEET)["dowel_d"] == pytest.approx(25.4)
    assert set(models.sizes(FEET)) == {"3/4 in", "25 mm"}


def test_each_cup_takes_the_dowel_with_one_of_the_coupons_clearances() -> None:
    p, step = params(FEET), params(COUPON)["step"]
    assert p["bore_d"] == pytest.approx(p["dowel_d"] + p["clearance"])
    assert any(p["clearance"] == pytest.approx(k * step) for k in (1, 2, 3, 4))


def test_each_plate_sits_flat_on_the_wall_with_room_for_the_cord_behind_the_rail() -> None:
    p = params(FEET)
    for name in ("Bottom foot", "Top foot"):
        assert body(FEET, name)["bbox"]["min"][0] == pytest.approx(-p["standoff"])
    assert p["standoff"] - p["dowel_d"] / 2 >= p["cord_depth"]
    assert p["cord_depth"] < p["plate_t"]


def test_each_screw_sits_behind_the_rail_under_a_cap() -> None:
    p, cap = params(FEET), body(FEET, "Cap 1")["bbox"]
    assert p["head_d"] < 19.05  # narrower than even a 3/4-inch rail in front of it
    assert p["head_depth"] == pytest.approx(p["head_h"] + p["cap_h"])
    assert p["head_h"] >= SCREW_HEAD_MM
    assert p["head_depth"] < p["plate_t"]
    assert cap["max"][2] - cap["min"][2] == pytest.approx(p["cap_h"])


def test_the_rail_lifts_into_the_top_cup_past_the_bottom_cups_rim() -> None:
    p = params(FEET)
    assert p["lift_room"] > p["low_depth"]
    assert p["high_depth"] - p["insert_min"] >= p["lift_room"] + 2 * 5.0  # 5 mm either way
    top = body(FEET, "Top foot")["bbox"]
    height = p["floor_t"] + p["high_depth"] + p["tab_h"]
    assert top["max"][2] - top["min"][2] == pytest.approx(height)


def test_a_screw_up_through_the_bottom_floor_holds_the_rail_down() -> None:
    p = params(FEET)
    assert p["pin_d"] < p["dowel_d"] / 4
    assert p["floor_t"] - p["pin_head_h"] >= 2.0


def test_the_notes_give_where_the_top_screw_goes() -> None:
    p, notes = params(FEET), models.read_yml(FEET)["notes"]
    gap = (p["lift_room"] + p["high_depth"] - p["insert_min"]) / 2
    expected = p["low_depth"] + p["high_depth"] + p["tab_h"] - gap
    assert p["spacing_less"] == pytest.approx(expected)
    assert f"less {p['spacing_less']:g} mm" in notes
    assert f"within {p['spacing_tol']:g} mm" in notes
