"""The taper card (S33): two tapered windows that read a dowel's real diameter, from 1/2 to 2
inches, where it stops, in millimetres and in inch sizes."""

from __future__ import annotations

import math
from fractions import Fraction
from itertools import pairwise
from pathlib import Path

import pytest

import models
from conftest import body, lettering, params, standing_on

CARD = models.Model(Path(__file__).resolve().parent.parent / "models" / "dowel-taper-card")
GRID = models.Model(Path(__file__).resolve().parent.parent / "models" / "dowel-hole-grid")
PLATE_MM = 256.0  # a Bambu P2S prints up to 256 mm square
SPACING_MM = 5.0  # room a slicer keeps between two parts, and here off the plate's edges too
LAYER_MM = 0.2  # the page's layer height: the colour change falls between two layers


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


def test_the_built_millimetre_ticks_sit_half_a_millimetre_of_dowel_apart() -> None:
    """S33, from the ticks themselves: each starts 0.4 mm off its window's edge, and 0.5 mm of dowel
    is 0.5 cos_a / rate along the card."""
    p = params(CARD)
    step = 0.5 * p["cos_a"] / p["rate"]
    boxes = [each["bbox"] for each in standing_on(CARD, "Card")]
    thin = [b for b in boxes if b["max"][0] - b["min"][0] == pytest.approx(0.6, abs=1e-3)]
    for window, count in ((1, 45), (2, 41)):  # 12 to 34 mm and 32 to 52 mm, every 0.5 mm
        along = []
        for b in thin:
            x = (b["min"][0] + b["max"][0]) / 2
            half = (p[f"w{window}_n"] + (x - p["end"]) * p["rate"]) / 2
            if b["min"][1] == pytest.approx(p[f"axis{window}"] + half + 0.4, abs=0.01):
                along.append(x)
        along.sort()
        assert len(along) == count
        assert [b - a for a, b in pairwise(along)] == pytest.approx([step] * (count - 1), abs=0.003)


def sizes_read(p: dict[str, float]) -> list[tuple[int, float, float]]:
    """Each size lettered on the card, from its saved design: (its window, the diameter it names
    in millimetres, where along the card it's centred). The small window's millimetres are above
    it, the large one's inches below it; between the windows, a whole number over 2 is the large
    window's millimetres and anything else the small one's inches."""
    found = []
    for words, x, y, _ in lettering(CARD):
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


def test_each_size_is_marked_where_a_dowel_of_that_size_stops_and_can_reach() -> None:
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


def test_only_its_ticks_and_numbers_stand_above_its_top() -> None:
    """So one filament change at the first layer above the top prints all of them, and nothing
    else, in a second colour (Phase 2 Q&A 13)."""
    p, raised = params(CARD), standing_on(CARD, "Card")
    assert len(raised) > 100  # each digit, slash and tick its own body
    for each in raised:
        low, high = each["bbox"]["min"], each["bbox"]["max"]
        assert each["closed"]
        assert low[2] == pytest.approx(p["thick"])
        assert high[2] == pytest.approx(p["thick"] + p["relief"])
        assert 0 <= low[0] and high[0] <= p["card_l"] and 0 <= low[1] and high[1] <= p["card_w"]


def test_it_is_4_mm_thick_and_its_lettering_stands_0_8_mm_proud_on_whole_layers() -> None:
    """Thin enough to print quickly and stiff enough in hand (Phase 2 Q&A 14); its ticks and
    numbers stand on its top, so one filament change there prints them in a second colour (Q&A
    13)."""
    p = params(CARD)
    assert p["thick"] == pytest.approx(4.0)
    assert p["relief"] == pytest.approx(0.8)
    for height in (p["thick"], p["relief"]):
        assert height / LAYER_MM == pytest.approx(round(height / LAYER_MM))


def test_the_card_and_a_one_inch_tile_share_the_printers_plate() -> None:
    """Dan prints both at once (Phase 2 Q&A 12): the card along the plate, the tile beside it."""
    card, tile = params(CARD), params(GRID)
    assert tile["dowel_d"] == pytest.approx(25.4)  # the grid as saved is the 1-inch tile
    assert card["card_w"] + tile["tile_w"] + 3 * SPACING_MM <= PLATE_MM
    assert tile["tile_l"] + 2 * SPACING_MM <= PLATE_MM


def word_box(y: float, height: float) -> tuple[float, float]:
    """How far a word reaches across the card, from its baseline: a fraction's slash
    dips a little under it, an i's dot rises a little over its height."""
    return y - 0.1 * height, y + 1.1 * height


def test_every_word_is_at_least_2_mm_inside_the_cards_long_edges() -> None:
    p = params(CARD)
    for words, _, y, height in lettering(CARD):
        low, high = word_box(y, height)
        assert low >= 2.0 and high <= p["card_w"] - 2.0, words


def test_words_in_neighbouring_rows_are_at_least_2_mm_apart() -> None:
    """Between the windows, the large one's millimetres rise toward the small one's inches; a
    narrower strip there must not run one row into the other."""
    found = lettering(CARD)
    for words, x, y, height in found:
        for other, x2, y2, height2 in found:
            # within 20 mm along (the widest word, 1 7/8, is about 16 mm), and over 2 mm above:
            # another row, since a row's own words step about 0.5 mm from one to the next
            if abs(x - x2) < 20 and y2 > y + 2.0:
                assert word_box(y2, height2)[0] - word_box(y, height)[1] >= 2.0, (words, other)


def test_its_volume_is_the_card_less_its_windows_plus_its_raised_lettering() -> None:
    p = params(CARD)
    windows = p["len"] * (p["w1_n"] + p["w1_w"] + p["w2_n"] + p["w2_w"]) / 2 * p["thick"]
    solid = p["card_l"] * p["card_w"] * p["thick"] - windows
    assert body(CARD, "Card")["volume_mm3"] == pytest.approx(solid, rel=1e-4)
    raised = sum(each["volume_mm3"] for each in standing_on(CARD, "Card"))
    assert 0 < raised < 0.05 * p["card_l"] * p["card_w"] * p["relief"]


def test_its_page_says_how_to_read_it_and_to_check_it_with_a_coin() -> None:
    meta = models.read_yml(CARD)
    assert meta["material"].startswith("PLA")
    for words in ("touches both sides", "a quarter turn", "23.88 mm", "24.26 mm"):
        assert words in meta["notes"]
    assert meta["print"]["Orientation"].startswith("flat")
    second = meta["print"]["Second colour"]
    assert "one filament change" in second and f"{params(CARD)['thick']:.1f} mm" in second
