"""The arm socket (S28, S29, S13): onto the carrier's dovetail, the arm 2 inches deep, wedged."""

from __future__ import annotations

from pathlib import Path

import pytest

import models
from conftest import body, params

MODELS = Path(__file__).resolve().parent.parent / "models"
SOCKET = models.Model(MODELS / "rail-arm-socket")
CARRIER = models.Model(MODELS / "rail-carrier")
COUPON = models.Model(MODELS / "dowel-fit-coupon")
SHARED = ["wall", "r_o", "carrier_l", "dt_base", "dt_top", "dt_h", "dowel_d", "clearance"]


def test_the_socket_and_its_wedge_are_each_one_closed_body() -> None:
    assert body(SOCKET, "Arm socket")["closed"]
    assert body(SOCKET, "Arm wedge")["closed"]


def test_it_is_saved_for_one_inch_and_comes_in_three_sizes() -> None:
    assert params(SOCKET)["dowel_d"] == pytest.approx(25.4)
    assert set(models.sizes(SOCKET)) == {"3/4 in", "25 mm"}


@pytest.mark.parametrize("name", SHARED)
def test_its_slot_is_cut_for_the_carriers_dovetail(name: str) -> None:
    assert params(SOCKET)[name] == pytest.approx(params(CARRIER)[name])


def test_its_top_rests_on_the_dovetails_end() -> None:
    p, socket = params(SOCKET), body(SOCKET, "Arm socket")["bbox"]
    assert socket["min"][2] == pytest.approx(0.0)
    assert socket["max"][2] == pytest.approx(p["carrier_l"] + p["top_t"])
    assert 0 < p["fit"] < 0.5


def test_the_arm_goes_in_at_least_two_inches_with_the_coupons_clearance() -> None:
    p, step = params(SOCKET), params(COUPON)["step"]
    assert p["socket_depth"] >= 51.0
    assert p["bore_d"] == pytest.approx(p["dowel_d"] + p["clearance"])
    assert any(p["clearance"] == pytest.approx(k * step) for k in (1, 2, 3, 4))


@pytest.mark.parametrize("off", [-0.5, 0.0, 0.5])
def test_a_dowel_half_a_millimetre_off_still_seats_the_wedge_inside(off: float) -> None:
    # A dowel off its size gets the clearance the coupon picks for it (S28), and wedge_in follows
    # clearance, so the seat depends on the offset alone; the wedge pushes the arm down, so the
    # gap gains clearance / 2.
    p = params(SOCKET)
    short_of_end = (p["wedge_in"] - p["room_in"] - p["clearance"] / 2 + off) / p["taper"]
    assert 0 < short_of_end < p["socket_depth"] - 10.0


def test_the_wedges_groove_leaves_a_wall_above_it() -> None:
    p = params(SOCKET)
    deepest = p["dowel_d"] / 2 + p["room_in"] + p["socket_depth"] * p["taper"]
    assert p["boss_d"] / 2 - deepest >= 2.0
