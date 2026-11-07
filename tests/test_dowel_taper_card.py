"""The taper card (S33): two tapered windows that read a dowel's real diameter, from 1/2 to 2
inches, where it stops, in millimetres and in inch sizes."""

from __future__ import annotations

import math
from fractions import Fraction
from pathlib import Path

import pytest

import models
from conftest import body, engraved, params

CARD = models.Model(Path(__file__).resolve().parent.parent / "models" / "dowel-taper-card")
PLATE_MM = 256.0  # a Bambu P2S prints up to 256 mm square


def reach(rate: float) -> tuple[float, float]:
    """A dowel touches the window's slanted sides where the window is d·cos(a) wide, tan(a) being
    rate / 2, and its round body reaches d/2 back and forward from its centre, which sits
    d/2·sin(a) past those points. It stops at its tick only if the window's narrow end is under
    lo·d and its wide end over hi·d."""
    a = math.atan(rate / 2)
    lo = math.cos(a) - rate / 2 * (1 - math.sin(a))
    hi = math.cos(a) + rate / 2 * (1 + math.sin(a))
    return lo, hi


def test_every_dowel_from_half_an_inch_to_two_inches_reaches_its_tick() -> None:
    p = params(CARD)
    lo, hi = reach(p["rate"])
    assert p["w1_n"] / lo <= 12.7 - 0.5  # 1/2 inch, and half a millimetre under it
    assert p["w2_w"] / hi >= 50.8 + 0.5  # 2 inches, and half a millimetre over it
    assert p["w2_n"] / lo < p["w1_w"] / hi  # the windows overlap: no size falls between them


def test_ticks_half_a_millimetre_apart_are_over_4_mm_apart_on_the_card() -> None:
    p = params(CARD)
    assert 0.5 / p["rate"] > 4.0
    assert p["len"] == pytest.approx((p["w1_w"] - p["w1_n"]) / p["rate"])
    assert p["len"] == pytest.approx((p["w2_w"] - p["w2_n"]) / p["rate"])
    assert p["cos_a"] == pytest.approx(1 / math.sqrt(1 + (p["rate"] / 2) ** 2))


def sizes_read(p: dict[str, float]) -> list[tuple[int, float, float]]:
    """Each size engraved on the card, from its saved design: (its window, the diameter it names
    in millimetres, where along the card it's centred). The small window's millimetres are above
    it, the large one's inches below it; between the windows, a whole number over 2 is the large
    window's millimetres and anything else the small one's inches."""
    found = []
    for words, x, y, _ in engraved(CARD):
        if words in ("mm", "in"):
            continue
        inches = float(sum(Fraction(w) for w in words.split())) * 25.4
        if y > p["axis1"]:
            found.append((1, float(words), x))
        elif y < p["axis2"]:
            found.append((2, inches, x))
        elif "/" not in words and float(words) > 2:
            found.append((2, float(words), x))
        else:
            found.append((1, inches, x))
    return found


def test_each_size_is_engraved_where_a_dowel_of_that_size_stops_and_can_reach() -> None:
    p = params(CARD)
    lo, hi = reach(p["rate"])
    read = sizes_read(p)
    for window, d, x in read:
        narrow, wide = p[f"w{window}_n"], p[f"w{window}_w"]
        assert x == pytest.approx(p["end"] + (d * p["cos_a"] - narrow) / p["rate"], abs=0.002)
        assert narrow / lo <= d <= wide / hi, (window, d)
    millimetres = {d for _, d, _ in read if d == round(d)}  # no eighth of an inch is whole
    eighths = {round(d / 25.4 * 8) for _, d, _ in read if d != round(d)}
    assert set(range(12, 53)) <= millimetres
    assert set(range(4, 17)) <= eighths


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
