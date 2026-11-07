"""The taper card (S33): two tapered windows that read a dowel's real diameter, from 1/2 to 2
inches, where it stops, in millimetres and in inch sizes."""

from __future__ import annotations

import math
from pathlib import Path

import pytest

import models
from conftest import body, params

CARD = models.Model(Path(__file__).resolve().parent.parent / "models" / "dowel-taper-card")
PLATE_MM = 256.0  # a Bambu P2S prints up to 256 mm square


def test_its_windows_read_every_dowel_from_half_an_inch_to_two_inches() -> None:
    p = params(CARD)
    assert p["w1_n"] <= 12.7 - 1.0  # 1/2 inch, a millimetre in from the narrow end
    assert p["w2_w"] >= 50.8 + 1.0  # 2 inches, a millimetre in from the wide end
    assert p["w2_n"] < p["w1_w"]  # they overlap, so no size falls between them


def test_a_tenth_of_a_millimetre_is_a_millimetre_along_each_window() -> None:
    p = params(CARD)
    assert p["rate"] == pytest.approx(0.1)
    assert p["len"] == pytest.approx((p["w1_w"] - p["w1_n"]) / p["rate"])
    assert p["len"] == pytest.approx((p["w2_w"] - p["w2_n"]) / p["rate"])


def test_its_ticks_sit_where_a_round_dowel_touches_the_slanted_sides() -> None:
    p = params(CARD)
    assert p["cos_a"] == pytest.approx(1 / math.sqrt(1 + (p["rate"] / 2) ** 2))


def test_it_is_one_closed_card_that_fits_the_printers_plate() -> None:
    p, card = params(CARD), body(CARD, "Card")
    assert card["closed"]
    low, high = card["bbox"]["min"], card["bbox"]["max"]
    assert [high[i] - low[i] for i in range(3)] == pytest.approx(
        [p["card_l"], p["card_w"], p["thick"]]
    )
    assert p["card_l"] <= PLATE_MM and p["card_w"] <= PLATE_MM


def test_its_volume_is_the_card_less_its_windows_and_a_shallow_engraving() -> None:
    p = params(CARD)
    windows = p["len"] * (p["w1_n"] + p["w1_w"] + p["w2_n"] + p["w2_w"]) / 2 * p["thick"]
    solid = p["card_l"] * p["card_w"] * p["thick"] - windows
    engraved = solid - body(CARD, "Card")["volume_mm3"]
    assert 0 < engraved < 0.05 * p["card_l"] * p["card_w"] * p["engrave"]


def test_its_page_says_how_to_read_it_and_to_check_it_with_a_coin() -> None:
    meta = models.read_yml(CARD)
    assert meta["material"].startswith("PLA")
    for words in ("touches both sides", "a quarter turn", "23.88 mm", "24.26 mm"):
        assert words in meta["notes"]
    assert meta["print"]["Orientation"].startswith("flat")
