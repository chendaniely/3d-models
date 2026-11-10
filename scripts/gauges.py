# /// script
# requires-python = ">=3.12"
# ///
"""The store gauges' design scripts: writes .git/<slug>-script.json in the repo root given as
argv[1], for the taper card and the hole grid; each, run by solidcraft-cli, saves
models/<slug>/<slug>.sc. Then `make models` builds them. Usage: uv run scripts/gauges.py .
Millimetres; each gauge lies flat, its top face at z = thick, its words and ticks standing on it,
`relief` high, so one filament change at that layer prints them in a second colour.
The card's ticks are placed here, from its windows' sizes: change those and run this again."""

import json
import math
import sys
from fractions import Fraction
from pathlib import Path


def P(name, expr, comment, unit=None):
    p = {"name": name, "expression": expr, "comment": comment}
    if unit is not None:
        p["unit"] = unit
    return {"command": "parameters.add", "params": p}


def poly(points):
    return {"command": "sketch.line", "params": {"points": points, "closed": True}}


def text(words, x, y, height, align="center", expression=False):
    p = {"at": [x, y], "height": height, "align": align}
    p["text_expression" if expression else "text"] = words
    return {"command": "sketch.text", "params": p}


def raise_up(items):
    """The words and ticks, standing `relief` high on the top face: everything above it is them.
    Each stays its own closed body, touching the top, and a slicer prints the lot as one part.
    SolidCraft joins many small solids to a body slowly, and slower with each: the card's 162
    took over half an hour, as did cutting the top away round them."""
    return [
        {"command": "sketch.create", "params": {"plane": "XY", "offset": "thick"}},
        *items,
        {"command": "sketch.finish", "params": {}},
        {
            "command": "solid.extrude",
            "params": {"distance": "relief", "operation": "new", "body_name": "Lettering"},
        },
    ]


def save(slug):
    return {
        "command": "file.save_as",
        "params": {"path": f"models/{slug}/{slug}.sc", "format": "json", "cache": False},
    }


def r(v):
    return round(v, 3)


# ---- the taper card ----------------------------------------------------------------------------

RATE, END, RIGHT, BAND, MID = 0.11, 8.0, 16.0, 15.0, 28.0
W1, W2 = (11.0, 36.0), (30.0, 55.0)
SIN_A, COS_A = (RATE / 2) / math.sqrt(1 + (RATE / 2) ** 2), 1 / math.sqrt(1 + (RATE / 2) ** 2)
# A dowel's round body reaches d/2 back and forward from its centre, which sits d/2 sin(a) past
# its contact points: it stops at its tick only where the narrow end is under LO d and the wide
# end over HI d, so the scale runs from w_n / LO to w_w / HI and no tick is out of its reach.
LO = COS_A - RATE / 2 * (1 - SIN_A)
HI = COS_A + RATE / 2 * (1 + SIN_A)
AXIS2 = BAND + W2[1] / 2
AXIS1 = BAND + W2[1] + MID + W1[1] / 2
GAP, LONG, SHORT, TICK_W = 0.4, 5.0, 3.0, 0.6
NUM_H, INCH_H = 5.0, 5.0


def x_at(d, w_n):
    """Where along the card a dowel of diameter d stops: the window there is d cos(a) wide, its
    half-angle a, so the dowel's two contact points sit on this line."""
    return END + (d * COS_A - w_n) / RATE


def half_width(x, w_n):
    return (w_n + (x - END) * RATE) / 2


def inch(frac):
    whole, rest = divmod(frac, 1)
    if rest == 0:
        return f"{whole}"
    words = f"{rest.numerator}/{rest.denominator}"
    return f"{whole} {words}" if whole else words


def scale(axis, w, side_mm):
    """Ticks every 0.5 mm with numbers on one edge, every 1/8 inch with fractions on the other."""
    w_n, w_w = w
    items = []
    sign = side_mm  # +1: the mm scale on the window's upper edge
    d = math.ceil(w_n / LO * 2) / 2
    while d <= w_w / HI:
        x = x_at(d, w_n)
        edge = axis + sign * half_width(x, w_n)
        length = LONG if d == int(d) else SHORT
        y0, y1 = edge + sign * GAP, edge + sign * (GAP + length)
        lo, hi = min(y0, y1), max(y0, y1)
        items.append(
            poly(
                [
                    [r(x - TICK_W / 2), r(lo)],
                    [r(x + TICK_W / 2), r(lo)],
                    [r(x + TICK_W / 2), r(hi)],
                    [r(x - TICK_W / 2), r(hi)],
                ]
            )
        )
        if d == int(d):
            base = edge + sign * (GAP + LONG + 1.5) - (NUM_H if sign < 0 else 0)
            items.append(text(str(int(d)), r(x), r(base), NUM_H))
        d += 0.5
    # inches, on the other edge
    k = math.ceil(w_n / LO / 25.4 * 8)
    while k / 8 * 25.4 <= w_w / HI:
        d_in = k / 8 * 25.4
        x = x_at(d_in, w_n)
        edge = axis - sign * half_width(x, w_n)
        y0, y1 = edge - sign * GAP, edge - sign * (GAP + LONG)
        lo, hi = min(y0, y1), max(y0, y1)
        items.append(
            poly(
                [
                    [r(x - TICK_W / 2), r(lo)],
                    [r(x + TICK_W / 2), r(lo)],
                    [r(x + TICK_W / 2), r(hi)],
                    [r(x - TICK_W / 2), r(hi)],
                ]
            )
        )
        base = edge - sign * (GAP + LONG + 1.5) - (INCH_H if sign > 0 else 0)
        items.append(text(inch(Fraction(k, 8)), r(x), r(base), INCH_H))
        k += 1
    # the units, past the wide end
    for s, word in ((sign, "mm"), (-sign, "in")):
        edge = axis + s * w_w / 2
        base = edge + s * (GAP + LONG + 1.5) - (NUM_H if s < 0 else 0)
        items.append(text(word, END + (w_w - w_n) / RATE + 3, r(base), NUM_H, align="left"))
    return items


def window(axis_name, n):
    return [
        {"command": "sketch.create", "params": {"plane": "XY", "offset": "-1 mm"}},
        poly(
            [
                ["end", f"{axis_name} - w{n}_n / 2"],
                ["end + len", f"{axis_name} - w{n}_w / 2"],
                ["end + len", f"{axis_name} + w{n}_w / 2"],
                ["end", f"{axis_name} + w{n}_n / 2"],
            ]
        ),
        {"command": "sketch.finish", "params": {}},
        {
            "command": "solid.extrude",
            "params": {"distance": "thick + 2 mm", "operation": "cut", "targets": ["Card"]},
        },
    ]


def taper_card():
    slug = "dowel-taper-card"
    cmds = [
        P("rate", str(RATE), "how much wider each window gets per millimetre along it", unit=""),
        P("w1_n", f"{W1[0]} mm", "the small window's narrow end"),
        P("w1_w", f"{W1[1]} mm", "the small window's wide end"),
        P("w2_n", f"{W2[0]} mm", "the large window's narrow end: it overlaps the small one's top"),
        P("w2_w", f"{W2[1]} mm", "the large window's wide end"),
        P("len", "(w1_w - w1_n) / rate", "each window's length; the two are the same"),
        P(
            "cos_a",
            "cos(atan(rate / 2))",
            "a dowel stops where the window is its diameter times this: the ticks sit there",
            unit="",
        ),
        P("end", f"{END} mm", "plastic past each window's narrow end"),
        P("right", f"{RIGHT} mm", "plastic past each window's wide end, where the units are"),
        P("band", f"{BAND} mm", "plastic outside each window, holding its ticks and numbers"),
        P("mid", f"{MID} mm", "plastic between the windows, holding two scales"),
        P("thick", "4 mm", "the card's thickness: stiff in hand, quick to print"),
        P(
            "relief",
            "0.8 mm",
            "how far the ticks and numbers stand off the top: "
            "a second colour from the layer above thick",
        ),
        P("card_l", "end + len + right", "the card's length"),
        P("card_w", "2 * band + w1_w + mid + w2_w", "the card's width"),
        P("axis2", "band + w2_w / 2", "the large window's centre line"),
        P("axis1", "band + w2_w + mid + w1_w / 2", "the small window's centre line"),
        {
            "command": "solid.box",
            "params": {
                "length": "card_l",
                "width": "card_w",
                "height": "thick",
                "corner": [0, 0, 0],
                "body_name": "Card",
            },
        },
        *window("axis1", 1),
        *window("axis2", 2),
        *raise_up(scale(AXIS1, W1, +1) + scale(AXIS2, W2, +1)),
        save(slug),
    ]
    return slug, cmds


# ---- the hole grid: one tile per dowel size ----------------------------------------------------

OFFSETS = (-3, -2, -1, 0, 1, 2)


def hole_grid():
    slug = "dowel-hole-grid"
    cmds = [
        P(
            "dowel_d",
            "25.4 mm",
            "the dowel size this tile checks: 1 inch as saved; the page "
            "offers every 1/8 inch from 1/2 to 2",
        ),
        P("label", "1 in", "the size's name, raised on the tile", unit="text"),
        P("step", "0.2 mm", "between one hole and the next"),
    ]
    for i, k in enumerate(OFFSETS, 1):
        sign = "+" if k >= 0 else "-"
        cmds.append(
            P(
                f"h{i}",
                f"dowel_d {sign} {abs(k)} * step",
                f"hole {i}: {k * 0.2:+.1f} mm from the size" if k else f"hole {i}: the size itself",
            )
        )
    cmds += [
        P("wall", "4 mm", "plastic between neighbouring holes"),
        P("pitch", "h6 + wall", "centre to centre between holes, along and across"),
        P("band", "8 mm", "the strip under each row where the holes' sizes stand"),
        P("head", "12 mm", "the strip along the top with the size's name and the ring hole"),
        P(
            "thick",
            "4 mm",
            "the tile's thickness, so each hole is this deep: stiff, quick to print",
        ),
        P(
            "relief",
            "0.8 mm",
            "how far the words stand off the top: a second colour from the layer above thick",
        ),
        P("ring_d", "5 mm", "the hole for a key ring, to carry the tiles together"),
        P("tile_l", "3 * pitch + wall", "the tile's length"),
        P("tile_w", "2 * band + 2 * pitch + head", "the tile's width"),
        {
            "command": "solid.box",
            "params": {
                "length": "tile_l",
                "width": "tile_w",
                "height": "thick",
                "corner": [0, 0, 0],
                "body_name": "Tile",
            },
        },
    ]
    words = []
    for i in range(6):
        row, col = divmod(i, 3)  # row 0 on top: the three smallest
        x = f"wall / 2 + pitch / 2 + {col} * pitch"
        y = "band + pitch / 2" if row == 1 else "2 * band + 1.5 * pitch"
        cmds.append(
            {
                "command": "solid.cylinder",
                "params": {
                    "diameter": f"h{i + 1}",
                    "height": "thick + 2 mm",
                    "base": [x, y, "-1 mm"],
                    "axis": "Z",
                    "operation": "cut",
                    "targets": ["Tile"],
                },
            }
        )
        base = "band - 4.7 mm" if row == 1 else "2 * band + pitch - 4.7 mm"  # 1.2 mm under its hole
        words.append(text(f"number(h{i + 1}, 1)", x, base, 5.5, expression=True))
    cmds.append(
        {
            "command": "solid.cylinder",
            "params": {
                "diameter": "ring_d",
                "height": "thick + 2 mm",
                "base": ["tile_l - wall - ring_d / 2", "tile_w - head / 2", "-1 mm"],
                "axis": "Z",
                "operation": "cut",
                "targets": ["Tile"],
            },
        }
    )
    words.append(text("label", "wall", "tile_w - head + 2.5 mm", 7, align="left", expression=True))
    cmds += raise_up(words)
    cmds.append(save(slug))
    return slug, cmds


if __name__ == "__main__":
    root = Path(sys.argv[1])
    for slug, cmds in (taper_card(), hole_grid()):
        (root / "models" / slug).mkdir(parents=True, exist_ok=True)
        out = root / ".git" / f"{slug}-script.json"
        out.write_text(json.dumps({"commands": cmds}, indent=1) + "\n")
        print(out, len(cmds))
