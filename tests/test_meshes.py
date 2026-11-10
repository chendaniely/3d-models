"""Every built STL, at every size, is one or more closed shells a slicer can fill: each edge is
shared by exactly two triangles (S28)."""

from __future__ import annotations

import struct
from collections import Counter
from pathlib import Path

import pytest

MODELS = Path(__file__).resolve().parent.parent / "models"
STLS = sorted(MODELS.glob("*/*.stl"))


def open_edges(path: Path) -> int:
    """How many edges of a binary STL belong to one triangle, or more than two."""
    data = path.read_bytes()
    count = struct.unpack_from("<I", data, 80)[0]
    edges: Counter = Counter()
    for i in range(count):
        values = struct.unpack_from("<12f", data, 84 + 50 * i)
        corners = [tuple(round(v, 4) for v in values[k : k + 3]) for k in (3, 6, 9)]
        for a, b in ((0, 1), (1, 2), (2, 0)):
            edges[frozenset((corners[a], corners[b]))] += 1
    return sum(1 for n in edges.values() if n != 2)


def test_the_built_stls_are_there_to_check() -> None:
    """Parametrizing over an empty list would collect nothing and pass."""
    assert STLS


@pytest.mark.parametrize("path", STLS, ids=lambda p: p.name)
def test_every_built_stl_is_watertight(path: Path) -> None:
    assert open_edges(path) == 0
