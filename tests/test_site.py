"""Every doc under docs/superpowers/ reaches the site, its Quarto syntax shown, not run (S06)."""

from __future__ import annotations

from pathlib import Path

import sitedocs

ROOT = Path(__file__).resolve().parent.parent
OPEN, CLOSE = "{" * 2 + "<", ">" + "}" * 2
LISTING = f"""# A plan

````markdown
{OPEN} include /../README.md {CLOSE}

```{{mermaid}}
flowchart LR
  a --> b
```
````
"""


def write_doc(root: Path, rel: str, text: str) -> None:
    path = root / "docs" / "superpowers" / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_every_doc_is_copied_with_its_heading_as_the_title(tmp_path: Path) -> None:
    write_doc(tmp_path, "specs/a-design.md", "# A: design spec\n\nText.\n")
    write_doc(tmp_path, "plans/a-phase-1.md", "No heading.\n")
    assert sitedocs.main([], root=tmp_path) == 0
    site = tmp_path / "website" / "superpowers"
    spec = (site / "specs" / "a-design.md").read_text(encoding="utf-8")
    assert spec.startswith('---\npagetitle: "A: design spec"\n---\n\n# A: design spec')
    assert 'pagetitle: "a-phase-1"' in (site / "plans" / "a-phase-1.md").read_text("utf-8")


def test_shortcodes_and_executable_cells_are_shown_not_run(tmp_path: Path) -> None:
    write_doc(tmp_path, "plans/a-phase-1.md", LISTING)
    sitedocs.main([], root=tmp_path)
    page = (tmp_path / "website" / "superpowers" / "plans" / "a-phase-1.md").read_text("utf-8")
    assert f"{OPEN}/* include /../README.md */{CLOSE}" in page
    assert "```mermaid\n" in page
    assert "```{" not in page


def test_a_doc_that_is_gone_loses_its_page(tmp_path: Path) -> None:
    write_doc(tmp_path, "specs/a-design.md", "# A\n")
    stale = tmp_path / "website" / "superpowers" / "specs" / "old.md"
    stale.parent.mkdir(parents=True)
    stale.write_text("old", encoding="utf-8")
    sitedocs.main([], root=tmp_path)
    assert not stale.exists()


def test_every_real_doc_is_listed_on_the_design_page() -> None:
    docs = ROOT / "docs" / "superpowers"
    design = (ROOT / "website" / "design.qmd").read_text(encoding="utf-8")
    unlisted = [
        rel.as_posix()
        for rel in (p.relative_to(docs) for p in sorted(docs.rglob("*.md")))
        if f"(superpowers/{rel.as_posix()})" not in design
    ]
    assert not unlisted, f"docs missing from the Design page: {unlisted}"
