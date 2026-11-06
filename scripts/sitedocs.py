"""Copy the docs under docs/superpowers/ into the site, with Quarto's own syntax shown, not run.

    uv run scripts/sitedocs.py
        write website/superpowers/<path> for every .md under docs/superpowers/ (generated and
        git-ignored), each with its first heading as the page's title

The plans quote Quarto's shortcodes and executable cells in their code listings, and Quarto
expands both even inside fenced code, so a plain include of a plan breaks the render. The copies
escape them instead: a shortcode's braces get Quarto's escape markers, and an executable cell's
fence loses its braces. The docs themselves stay as written, where conventions put them.
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OPEN, CLOSE = "{" * 2 + "<", ">" + "}" * 2  # spelt in parts, so this file is safe to quote
CELL = re.compile(r"^(\s*(?:`{3,}|~{3,}))\{([A-Za-z][\w-]*)\}", re.MULTILINE)


def escaped(text: str) -> str:
    """Quarto shows an escaped shortcode as written, and a fence without braces as code."""
    text = text.replace(OPEN, OPEN + "/*").replace(CLOSE, "*/" + CLOSE)
    return CELL.sub(r"\1\2", text)


def title(text: str, fallback: str) -> str:
    heading = next((line[2:].strip() for line in text.splitlines() if line.startswith("# ")), "")
    return heading or fallback


def main(argv: list[str] | None = None, root: Path = ROOT) -> int:
    docs = root / "docs" / "superpowers"
    out = root / "website" / "superpowers"
    shutil.rmtree(out, ignore_errors=True)
    copied = 0
    for doc in sorted(docs.rglob("*.md")):
        text = doc.read_text(encoding="utf-8")
        page = out / doc.relative_to(docs)
        page.parent.mkdir(parents=True, exist_ok=True)
        front = f"---\npagetitle: {json.dumps(title(text, doc.stem), ensure_ascii=False)}\n---\n\n"
        page.write_text(front + escaped(text), encoding="utf-8")
        copied += 1
    print(f"sitedocs: {copied} docs copied into website/superpowers/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
