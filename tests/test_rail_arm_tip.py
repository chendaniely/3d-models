"""The arm's tip (S28, S14, S27): a wedged cap, a stem that grips the cord over a short band and
takes the shade on two lugs, and clips under the arm; the cord pressed in everywhere it goes."""

from __future__ import annotations

from pathlib import Path

import pytest

import models
from conftest import body, measured, params

MODELS = Path(__file__).resolve().parent.parent / "models"
TIP = models.Model(MODELS / "rail-arm-tip")
FEET = models.Model(MODELS / "rail-feet")
CARRIER = models.Model(MODELS / "rail-carrier")
COUPON = models.Model(MODELS / "dowel-fit-coupon")
BODIES = ["Arm tip", "Tip wedge", "Cord clip 1", "Cord clip 2", "Cord clip 3"]


def test_the_tip_its_wedge_and_three_clips_are_each_one_closed_body() -> None:
    for name in BODIES:
        assert body(TIP, name)["closed"]


def test_it_is_saved_for_one_inch_and_comes_in_three_sizes() -> None:
    assert params(TIP)["dowel_d"] == pytest.approx(25.4)
    assert set(models.sizes(TIP)) == {"3/4 in", "25 mm"}


def test_the_cap_takes_the_dowel_with_one_of_the_coupons_clearances() -> None:
    p, step = params(TIP), params(COUPON)["step"]
    assert p["bore_d"] == pytest.approx(p["dowel_d"] + p["clearance"])
    assert any(p["clearance"] == pytest.approx(k * step) for k in (1, 2, 3, 4))


def test_the_stem_grips_the_cord_over_a_short_band_pressed_in_from_the_side() -> None:
    p = params(TIP)
    assert p["press_w"] < p["grip_d"] < p["cord_d"] < p["slot_w"] < p["free_d"]
    assert p["cord_d"] - p["press_w"] <= 2.0  # a squeeze, not a fight
    assert 8.0 <= p["grip_l"] <= 12.0
    assert p["mouth_w"] < p["cord_d"]


def test_the_cord_has_room_behind_the_rail_wherever_it_goes() -> None:
    p = params(TIP)
    assert params(FEET)["cord_depth"] >= p["cord_d"] + 1.0
    assert params(FEET)["cord_w"] >= p["cord_d"] + 1.0
    assert params(CARRIER)["channel"] >= p["cord_d"] + 1.0


def test_every_part_prints_from_the_same_bed() -> None:
    lowest = {b["name"]: b["bbox"]["min"][2] for b in measured(TIP)["bodies"]}
    assert set(lowest) == set(BODIES)
    assert all(z == pytest.approx(lowest["Arm tip"]) for z in lowest.values())


@pytest.mark.parametrize("off", [-0.5, 0.0, 0.5])
def test_a_dowel_half_a_millimetre_off_still_seats_the_wedge_inside(off: float) -> None:
    # A dowel off its size gets the clearance the coupon picks for it (S28), and wedge_in follows
    # clearance, so the seat depends on the offset alone; the gap gains clearance / 2.
    p = params(TIP)
    short_of_end = (p["wedge_in"] - p["room_in"] - p["clearance"] / 2 + off) / p["taper"]
    assert 0 < short_of_end < p["bore_depth"] - 10.0


def test_the_wedges_groove_leaves_a_wall_above_it() -> None:
    p = params(TIP)
    deepest = p["dowel_d"] / 2 + p["room_in"] + p["bore_depth"] * p["taper"]
    assert p["cap_d"] / 2 - deepest >= 2.0
