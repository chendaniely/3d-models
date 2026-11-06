"""Fail when the rendered site would make a visitor's browser fetch from another host.

    uv run scripts/offsite.py website/_site

A script, style sheet, font, image or frame from another host tells that host who visits, and runs
or shows whatever it serves. Links a visitor clicks are fine; only what loads by itself is named.
It reads every page's tags, inline styles and inline scripts, every style sheet, and every script's
imports. It is a tripwire for the ways a page loads things, not a proof: the phase end also looks
at the live site's network log. A missing site, or one with no pages, fails: nothing to vouch for.
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

SCHEME = r"(?:[a-z][a-z0-9+.-]*:)?//"  # http://, https://, //host, or any scheme with a host
REMOTE = re.compile(r"^\s*" + SCHEME, re.IGNORECASE)
CSS_REMOTE = re.compile(r"(?:url\(|image-set\(|@import)\s*[\"']?\s*" + SCHEME, re.IGNORECASE)
JS_REMOTE = re.compile(r"(?:\bimport\s*\(|\bfrom)\s*[\"'`]\s*" + SCHEME, re.IGNORECASE)
LOADS = {  # each tag, and the attributes that make the browser fetch by itself
    "script": ("src",),
    "img": ("src", "srcset"),
    "source": ("src", "srcset"),
    "iframe": ("src",),
    "frame": ("src",),
    "embed": ("src",),
    "object": ("data",),
    "audio": ("src",),
    "video": ("src", "poster"),
    "track": ("src",),
    "input": ("src",),
    "link": ("href", "imagesrcset"),
    "base": ("href",),
    "image": ("href", "xlink:href"),
    "use": ("href", "xlink:href"),
    "feimage": ("href", "xlink:href"),
}
QUIET_LINKS = {"alternate", "author", "bookmark", "canonical", "external", "help", "license", "me"}
REFRESH_URL = re.compile(r"url\s*=\s*['\"]?\s*" + SCHEME, re.IGNORECASE)


def remote_srcset(value: str) -> bool:
    return any(REMOTE.match(candidate) for candidate in value.split(","))


class Page(HTMLParser):
    """Collects whether a page loads anything from another host."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.found = False
        self.inside: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {name: value or "" for name, value in attrs}
        names = LOADS.get(tag, ())
        if tag == "link" and set(values.get("rel", "").lower().split()) <= QUIET_LINKS:
            names = ("imagesrcset",) if "rel" in values else names
        for name in names:
            value = values.get(name, "")
            if remote_srcset(value) if name.endswith("srcset") else REMOTE.match(value):
                self.found = True
        if CSS_REMOTE.search(values.get("style", "")):
            self.found = True
        if tag == "meta" and values.get("http-equiv", "").lower() == "refresh":
            self.found = self.found or bool(REFRESH_URL.search(values.get("content", "")))
        self.inside = tag if tag in ("style", "script") else None

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.inside = None

    def handle_data(self, data: str) -> None:
        pattern = {"style": CSS_REMOTE, "script": JS_REMOTE}.get(self.inside or "")
        if pattern and pattern.search(data):
            self.found = True

    def handle_endtag(self, tag: str) -> None:
        self.inside = None


def loads_offsite(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    suffix = path.suffix.lower()
    if suffix in (".html", ".htm", ".svg"):
        page = Page()
        page.feed(text)
        page.close()
        return page.found
    if suffix == ".css":
        return bool(CSS_REMOTE.search(text))
    if suffix in (".js", ".mjs"):
        return bool(JS_REMOTE.search(text))
    return False


def offsite(site: Path) -> list[str]:
    """Each file under site that loads something from another host, by its path in site."""
    files = sorted(path for path in site.rglob("*") if path.is_file())
    return [path.relative_to(site).as_posix() for path in files if loads_offsite(path)]


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    site = Path(args[0]) if args else Path("website/_site")
    if not site.is_dir() or not any(site.rglob("*.html")):
        print(f"offsite: {site} holds no rendered pages: render the site first", file=sys.stderr)
        return 1
    found = offsite(site)
    for name in found:
        print(f"offsite: {name} loads something from another host", file=sys.stderr)
    if found:
        return 1
    print("offsite: the site loads nothing from another host")
    return 0


if __name__ == "__main__":
    sys.exit(main())
