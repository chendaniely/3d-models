"""The shade (S30, S11): PETG, turned onto the tip's stem, the lamp hanging inside it with at
least 10 mm of air all round."""

from __future__ import annotations

from pathlib import Path

import pytest

import models
from conftest import body, params

MODELS = Path(__file__).resolve().parent.parent / "models"
SHADE = models.Model(MODELS / "rail-shade")
TIP = models.Model(MODELS / "rail-arm-tip")


def test_the_shade_is_one_closed_body_in_petg() -> None:
    assert body(SHADE, "Shade")["closed"]
    assert models.read_yml(SHADE)["material"].startswith("PETG")


def test_it_leaves_at_least_10_mm_of_air_round_the_socket_and_the_bulb() -> None:
    p = params(SHADE)
    assert p["gap"] >= 10.0
    assert p["r_top"] >= p["socket_d"] / 2 + 10.0
    assert p["r_bulb"] >= p["bulb_d"] / 2 + 10.0


def test_its_cone_widens_round_the_socket_and_its_cylinder_runs_the_bulbs_length() -> None:
    p, shade = params(SHADE), body(SHADE, "Shade")["bbox"]
    assert p["shoulder_z"] == pytest.approx(p["top_t"] + p["drop"] + p["socket_l"])
    assert p["height"] - p["rim"] == pytest.approx(p["shoulder_z"] + p["bulb_l"])
    assert shade["max"][2] - shade["min"][2] == pytest.approx(p["height"])
    assert shade["max"][0] - shade["min"][0] == pytest.approx(2 * (p["r_bulb"] + p["shade_t"]))


@pytest.mark.parametrize("name", ["stem_d", "lug_w", "lug_h"])
def test_its_top_turns_onto_the_tips_stem(name: str) -> None:
    assert params(SHADE)[name] == pytest.approx(params(TIP)[name])


def test_the_lugs_sit_inside_with_room_above_the_socket() -> None:
    p = params(SHADE)
    assert 0 < p["fit"] < 1.0
    assert p["drop"] > params(TIP)["lug_t"]


def test_the_vents_open_the_top_between_the_stems_notches_and_the_wall() -> None:
    p, tip = params(SHADE), params(TIP)
    assert p["vent_r"] - p["vent_d"] / 2 > tip["stem_d"] / 2 + tip["lug_h"] + p["fit"] + 2.0
    assert p["vent_r"] + p["vent_d"] / 2 < p["r_top"] - 2.0
