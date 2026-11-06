"""The rail carrier (S28, S29, S14): onto the rail from the front, locked by a wedge behind it."""

from __future__ import annotations

from pathlib import Path

import pytest

import models
from conftest import body, params

MODELS = Path(__file__).resolve().parent.parent / "models"
CARRIER = models.Model(MODELS / "rail-carrier")
FEET = models.Model(MODELS / "rail-feet")
COUPON = models.Model(MODELS / "dowel-fit-coupon")


def test_the_carrier_and_its_wedge_are_each_one_closed_body() -> None:
    assert body(CARRIER, "Carrier")["closed"]
    assert body(CARRIER, "Wedge")["closed"]


def test_it_is_saved_for_one_inch_and_comes_in_three_sizes() -> None:
    assert params(CARRIER)["dowel_d"] == pytest.approx(25.4)
    assert set(models.sizes(CARRIER)) == {"3/4 in", "25 mm"}


def test_the_u_takes_the_dowel_with_one_of_the_coupons_clearances() -> None:
    p, step = params(CARRIER), params(COUPON)["step"]
    assert p["bore_d"] == pytest.approx(p["dowel_d"] + p["clearance"])
    assert any(p["clearance"] == pytest.approx(k * step) for k in (1, 2, 3, 4))


def test_its_arms_stop_short_of_the_wall_by_a_pads_thickness() -> None:
    p, carrier = params(CARRIER), body(CARRIER, "Carrier")["bbox"]
    assert p["standoff"] == pytest.approx(params(FEET)["standoff"])
    assert carrier["min"][0] == pytest.approx(-(p["standoff"] - p["wall_gap"]))
    assert 1.0 <= p["wall_gap"] <= 2.0  # a 3 mm felt or rubber pad takes it up


def test_it_is_long_enough_for_the_arm_at_24_inches() -> None:
    assert params(CARRIER)["carrier_l"] >= 100.0


def test_the_wedge_holds_by_friction_and_shows_below_to_be_tapped() -> None:
    p = params(CARRIER)
    assert p["taper"] <= 0.05  # 1 in 20 or gentler: it doesn't back out
    assert p["wedge_l"] > p["carrier_l"]


@pytest.mark.parametrize("off", [-0.5, 0.0, 0.5])
def test_a_dowel_half_a_millimetre_off_still_seats_the_wedge_inside(off: float) -> None:
    p = params(CARRIER)  # the wedge pushes the rail to the U's front, so the gap gains clearance/2
    below_top = (p["wedge_top"] - p["room_top"] - p["clearance"] / 2 + off) / p["taper"]
    assert 0 < below_top < p["carrier_l"] - 10.0


def test_the_wedge_is_thick_and_wide_enough_to_span_the_mouth() -> None:
    p, wedge = params(CARRIER), body(CARRIER, "Wedge")["bbox"]
    assert wedge["max"][0] - wedge["min"][0] == pytest.approx(p["wedge_w"])
    assert p["bore_d"] < p["wedge_w"] < p["bore_d"] + 2 * p["groove_d"]
    assert p["wedge_top"] >= 5.0


def test_the_cord_fits_behind_the_wedge_down_to_the_carriers_bottom() -> None:
    assert params(CARRIER)["channel"] >= 7.0
