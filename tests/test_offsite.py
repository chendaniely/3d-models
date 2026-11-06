"""scripts/offsite.py: the site makes a visitor's browser fetch nothing from another host (S31)."""

from __future__ import annotations

from pathlib import Path

import pytest

import offsite

PAGE = "<html><body><p>Hi</p>{}</body></html>"


@pytest.mark.parametrize(
    ("name", "text"),
    [
        ("index.html", PAGE.format('<script src="https://cdn.example.net/mathjax.js"></script>')),
        ("index.html", PAGE.format("<LINK REL=stylesheet HREF=//fonts.example.com/css>")),
        ("index.html", PAGE.format('<link rel="preload" href="https://example.com/f.woff2">')),
        ("index.html", PAGE.format('<img alt="a>b" src=" http://example.com/pixel.gif">')),
        (
            "index.html",
            PAGE.format('<img src="a.png" srcset="a.png 1x, https://x.example/b.png 2x">'),
        ),
        (
            "index.html",
            PAGE.format('<video src="v.mp4" poster="https://example.com/p.jpg"></video>'),
        ),
        ("index.html", PAGE.format('<object data="https://example.com/x.svg"></object>')),
        ("index.html", PAGE.format('<img src="&#104;ttps://example.com/p.gif">')),
        ("index.html", PAGE.format('<div style="background: url( https://example.com/b.png )">')),
        (
            "index.html",
            PAGE.format("<style>@font-face{src:url(https://example.com/f.woff2)}</style>"),
        ),
        ("index.html", PAGE.format('<script>import("https://cdn.example.net/x.js")</script>')),
        (
            "index.html",
            PAGE.format('<meta http-equiv="refresh" content="0; url=https://example.com/">'),
        ),
        ("index.html", PAGE.format('<svg><use href="https://example.com/s.svg#i"/></svg>')),
        ("site_libs/theme.min.css", '@import"https://fonts.example.com/css2?family=Sans";'),
        ("site_libs/theme.min.css", "body{background:image-set('https://example.com/b.png' 1x)}"),
        ("site_libs/app.js", 'import { x } from "https://cdn.example.net/x.js";'),
        ("site_libs/side.js", "import 'https://cdn.example.net/side-effect.js';"),
        ("index.html", PAGE.format('<svg><script href="https://example.com/s.js"></script></svg>')),
        ("index.html", PAGE.format('<meta http-equiv="refresh" content="0;https://example.com/">')),
        ("index.html", PAGE.format('<table background="https://example.com/t.png"></table>')),
    ],
)
def test_a_load_from_another_host_is_named(tmp_path: Path, capsys, name: str, text: str) -> None:
    (tmp_path / "index.html").write_text(PAGE.format(""), encoding="utf-8")
    path = tmp_path / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    assert offsite.main([str(tmp_path)]) == 1
    assert capsys.readouterr().err == f"offsite: {name} loads something from another host\n"


def test_links_local_files_and_quiet_attributes_pass(tmp_path: Path, capsys) -> None:
    (tmp_path / "index.html").write_text(
        PAGE.format(
            '<a href="https://github.com/x">repo</a><script src="site_libs/x.js"></script>'
            '<link href="styles.css" rel="stylesheet"><img src="models/hook.png" '
            'data-src="https://example.com/lazy.png">'
            '<link rel="canonical" href="https://example.com/">'
        ),
        encoding="utf-8",
    )
    (tmp_path / "styles.css").write_text("body{background:url(b.png)}", encoding="utf-8")
    (tmp_path / "search.js").write_text('var u="https://cdn.example.net/x.js"', encoding="utf-8")
    assert offsite.main([str(tmp_path)]) == 0
    assert "loads nothing from another host" in capsys.readouterr().out


@pytest.mark.parametrize("make", [False, True])
def test_a_missing_or_empty_site_fails(tmp_path: Path, capsys, make: bool) -> None:
    site = tmp_path / "_site"
    if make:
        site.mkdir()
    assert offsite.main([str(site)]) == 1
    assert "holds no rendered pages" in capsys.readouterr().err
