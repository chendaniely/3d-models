# 3d-models Phase 2: the grow-light rail, implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking. The project's `AGENTS.md` holds every rule for running
> it and outranks this header where they differ. **Rewritten at Phase 2's start** (2026-11-06)
> for the rail, from the spec as Dan revised it (Phase 2 Q&A 1 to 7), then revised after the
> [phase-start council](2026-11-05-3d-models-phase-2-start-council.md); every listing below was
> run in a scratch clone of `phase-2` before it went in.

**Goal:** Dan's grow light on a vertical dowel rail: two wall feet whose screws hide behind the
rail, a carrier wedged onto the rail with the light's arm on its dovetail, the light up to 24
inches out inside a PETG shade; each part printed in PLA and judged by eye, then in PETG and
load-tested, then installed. The parts are built first at placeholder sizes and published to the
live gallery, then retuned to Dan's measurements and published again (Q&A 9); the photo and site
gaps Phase 1 left are closed first, and two gauges, printed in PLA, measure the dowels at the
store (Q&A 11).

**Cut short (Q&A 15, 2026-11-09):** Dan paused the lamp to finish the project and design parts
afterwards. Tasks 10 to 14 are paused, unticked, and Phase 2 ends with the gauges built and the
rail's parts on the gallery at placeholder sizes; the sentence above is the goal as planned.

**Architecture:** five new models under `models/`, and two gauges, each a parametric SolidCraft design built by
Phase 1's `make models` (each dowel part in three dowel sizes, the shade and the card in one, the
hole grid in a tile per size), with a test that holds its fit and its numbers to
the spec; two Tier 1 fixes to the privacy check and the site; and Dan's tasks (measure, look test,
load test, install), whose answers the agent records and turns into parameters.

**Tech Stack:** Phase 1's pipeline (Python 3.12 under uv, solidcraft-cli 0.30.1, Quarto 1.11.6);
PLA for the look test, matte PETG for the parts and the shade; two 1-inch hardwood dowels (the
rail, up to 48 inches, and the arm, 550 mm); #8 or #10 pan-head wood screws or 3/16-inch toggle
bolts, a #6 × 3/4-inch screw, four 3 mm felt or rubber pads; Dan's Barrina 25 W grow light on its
pendant cord.

**Spec:** `docs/superpowers/specs/2026-11-05-3d-models-design.md`

**Now:** Phase end, step 8: The PR.

***

## Global Constraints

- Every Phase 1 constraint holds (its plan's *Global Constraints*).
- The rail stands vertical on two feet, up to about 48 inches long; it carries the light's arm and
  up to two small planters of about 2 kg each, watered (Phase 2 Q&A 1, 5).
- The light hangs up to 24 inches (610 mm) from the wall: with these parts, an arm cut to 550 mm
  (21 5/8 inches) puts it there (Phase 2 Q&A 2).
- From the room, no screw, bolt or nut shows (the spec's anti-goal); a screw behind the rail is
  capped, since the rail hides it only from straight in front.
- The rail can't be lifted out of its feet: a screw up through the bottom cup's floor holds it.
- The light's cord is never threaded through a hole: its plug and timer won't pass. Every part
  takes it pressed in from the side.
- Every rail part with a dowel is saved at 1 inch (25.4 mm) and lists `3/4 in` (19.05 mm) and `25 mm`
  as sizes; `clearance` is one of the coupon's (0.4 mm, a placeholder until Task 11).
- The parts and the shade are PETG, matte, never PLA (D9; Phase 2 Q&A 3); PLA only for the look
  test (D8) and the store gauges (Q&A 11).
- Screws go into a stud or toggle anchors, never plastic plugs.
- A photo: Strip it first, `make strip FILES=<file>`; then show Dan the stripped file and ask, naming it, whether anything in it shows where he lives (a window's view, a street, a house number, a face, a reflection, a screen). Only after his OK naming the file does it go under `models/<slug>/photos/`, and `make privacy` passes before it's staged.
- Each design's command script stays in `.git/`, out of the repo; the saved `.sc` holds the same
  feature tree. The gauges' generator is the exception: `scripts/gauges.py` (decided without Dan 6).
- The tiers judge the code and the docs. The parts' physical strength is proven by the load test
  (Task 13), not by a tier: a Tier 2 part task still holds a light over people's heads.

## Review Focus

1. **A cord whose plug or timer won't go through a hole:** every place the cord goes is open to
   the side (the stem's slot, the keel's mouth, the clips' loops, the bottom foot's groove, the
   carrier's channel); Task 5's test holds the slots against the cord and the cord's room behind
   the rail.
2. **A lamp bigger than the guesses:** Task 10 measures the socket and the bulb, and Task 11
   retunes the shade; Task 6's test holds 10 mm of air round each.
3. **A dowel half a millimetre over or under its size:** each wedge's travel covers it; Tasks 3, 4
   and 5 test it at -0.5, 0 and +0.5 mm.
4. **A carrier, a planter or the arm lifted:** the rail can't rise, held by the screw through the
   bottom cup's floor (Task 2's test; Task 14's check).
5. **Drywall with no stud where a foot goes:** 3/16-inch toggle bolts, which clamp each foot's
   plate; Task 10 measures the heads, and the load test (Task 13) mounts as it will be.

***

### Task 1: Close the privacy gaps, and load nothing from other hosts

**Ruling:** this run's commits, an implementer's included, carry this session's own attribution line, `Co-Authored-By: Claude Opus 5.5`, as its harness gives it; the Spec review asked whether a subagent's commit should name its own model. Costs if wrong: a trailer naming the session's model, not the subagent's.

**Tier:** 1 (if wrong, a photo of Dan's home carries what it shouldn't onto a public repo, or every
visitor is seen by a third party) · **Scenarios:** S03, S31

Phase 1's end left the photo gaps for here, before the look test's first photo (Phase 1's retro,
*Items carried forward*). After the merge, the live site turned out to load Google's fonts on every
page and, on the Models page, MathJax and a polyfill from two CDNs: each tells another host who
visits. This task closes both, as the phase-start council asked (security 1 to 3, 5).

**Files:**
- Modify: `scripts/privacy.py`, `tests/test_privacy.py`, `scripts/gallery.py`,
  `tests/test_gallery.py`, `Makefile`, `pyproject.toml`, `website/_quarto.yml`
- Create: `scripts/offsite.py`, `tests/test_offsite.py`, `website/theme.scss`
- Docs: the spec's *The commands* row for `make docs`; the Architecture page's "Checks and the
  deploy" diagram

**Interfaces:**
- Consumes: Phase 1's `privacy.jpeg_end`, `structure_problem`, `problems`, `command_check`;
  `gallery.page`, `downloads` and `sitedocs.escaped`.
- Produces: `privacy.JPEG_SEGMENTS`, `privacy.JPEG_HOUSEKEEPING_SEGMENTS`, `privacy.GONE`,
  `privacy.jpeg_walk(data) -> tuple[int | None, int | None]` (the end, and the first segment's
  marker a picture doesn't need or a housekeeping segment holding anything but its own data);
  `gallery.FREE_TEXT` with `size`; `offsite.offsite(site: Path) -> list[str]` and
  `offsite.main(argv) -> int`; `make docs` running `scripts/offsite.py website/_site` after the
  render.

- [x] **Step 0: Record the base:** `git rev-parse HEAD > .git/TASK_BASE`.
- [x] **Step 1: Write the failing tests, and Step 3's code, as one patch.** The patch below holds
  both; Step 2 runs the tests with the code held back. Write it to `.git/task2.patch`:

```diff
diff --git a/Makefile b/Makefile
index 8120773..071b11c 100644
--- a/Makefile
+++ b/Makefile
@@ -37,12 +37,13 @@ privacy: ## Fail on image metadata, a photo format the check can't read, or a ho
 strip: ## Strip a photo's metadata, then look at it: make strip FILES="a.jpg b.png"
 	uv run --frozen scripts/privacy.py strip $(FILES)
 
-docs: ## Render the site into website/_site, failing on a broken link
+docs: ## Render the site into website/_site, failing on a broken link or a load from another host
 	uv run --frozen scripts/sitedocs.py
 	uv run --frozen scripts/gallery.py
 	@set -o pipefail; quarto render website 2>&1 | tee website/.render.log
 	@if grep -q 'Unable to resolve link target' website/.render.log; then \
 	  echo "docs: an unresolved link, above"; exit 1; fi
+	uv run --frozen scripts/offsite.py website/_site
 	@if command -v lychee >/dev/null; then lychee --offline --no-progress website/_site; \
 	else echo "lychee isn't installed: the offline link check runs in CI"; fi
 
diff --git a/pyproject.toml b/pyproject.toml
index 56c570d..2aad1d0 100644
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -32,4 +32,4 @@ extend-exclude = ["scripts/commitmsg.py", "*.md", "website/_site", "website/.qua
 select = ["E", "F", "I", "B", "UP"]
 
 [tool.ruff.lint.isort]
-known-first-party = ["conftest", "gallery", "models", "privacy", "sitedocs"]
+known-first-party = ["conftest", "gallery", "models", "offsite", "privacy", "sitedocs"]
diff --git a/scripts/gallery.py b/scripts/gallery.py
index 5b59b18..edc8399 100644
--- a/scripts/gallery.py
+++ b/scripts/gallery.py
@@ -15,6 +15,7 @@ import json
 import shutil
 import sys
 from pathlib import Path
+from urllib.parse import quote
 
 from models import ROOT, Model, find_models, read_yml, sizes
 from privacy import READABLE as PHOTOS
@@ -26,7 +27,7 @@ LICENCE = (
     f"share it, crediting chendaniely and linking to <{REPO_URL}>; don't sell it or prints of it."
 )
 STATUSES = ("designed", "printed", "in use")
-FREE_TEXT = ("title", "summary", "status", "material", "notes")  # escaped for Quarto, as sitedocs
+FREE_TEXT = ("title", "summary", "status", "material", "size", "notes")  # escaped, as sitedocs
 DENSITY_G_CM3 = {"PLA": 1.24, "PETG": 1.27}
 
 
@@ -123,7 +124,7 @@ def downloads(model: Model, meta: dict, params: set[str]) -> list[str]:
     if meta["sizes"]:
         lines.append(f"- [{slug}.stl]({slug}/{slug}.stl): the mesh to slice, for {meta['size']}")
         lines += [
-            f"- [{model.sized(size).name}]({slug}/{model.sized(size).name}): for {size}"
+            f"- [{model.sized(size).name}]({slug}/{model.sized(size).name}): for {escaped(size)}"
             for size in meta["sizes"]
         ]
     else:
@@ -175,14 +176,17 @@ def page(model: Model, meta: dict, evaluation: dict) -> str:
     shots = photos(model)
     if shots:
         lines += ["## Photos", ""]
-        lines += [
-            f"![{shot.stem.replace('-', ' ').replace('_', ' ')}]({slug}/photos/{shot.name})"
-            for shot in shots
-        ]
+        for shot in shots:
+            alt = escaped(shot.stem.replace("-", " ").replace("_", " "))
+            alt = alt.replace("[", "\\[").replace("]", "\\]")  # a bracket would end it early
+            lines.append(f"![{alt}]({slug}/photos/{quote(shot.name)})")
         lines.append("")
     if meta.get("print"):
         lines += ["## Printing", "", "| Setting | Value |", "|---|---|"]
-        lines += [f"| {cell(key)} | {cell(value)} |" for key, value in meta["print"].items()]
+        lines += [
+            f"| {cell(escaped(str(key)))} | {cell(escaped(str(value)))} |"
+            for key, value in meta["print"].items()
+        ]
         lines.append("")
     rows = measurements(evaluation)
     if rows:
diff --git a/scripts/offsite.py b/scripts/offsite.py
new file mode 100644
index 0000000..eace114
--- /dev/null
+++ b/scripts/offsite.py
@@ -0,0 +1,122 @@
+"""Fail when the rendered site would make a visitor's browser fetch from another host.
+
+    uv run scripts/offsite.py website/_site
+
+A script, style sheet, font, image or frame from another host tells that host who visits, and runs
+or shows whatever it serves. Links a visitor clicks are fine; only what loads by itself is named.
+It reads every page's tags, inline styles and inline scripts, every style sheet, and every script's
+imports. It is a tripwire for the ways a page loads things, not a proof: the phase end also looks
+at the live site's network log. A missing site, or one with no pages, fails: nothing to vouch for.
+"""
+
+from __future__ import annotations
+
+import re
+import sys
+from html.parser import HTMLParser
+from pathlib import Path
+
+SCHEME = r"(?:[a-z][a-z0-9+.-]*:)?//"  # http://, https://, //host, or any scheme with a host
+REMOTE = re.compile(r"^\s*" + SCHEME, re.IGNORECASE)
+CSS_REMOTE = re.compile(r"(?:url\(|image-set\(|@import)\s*[\"']?\s*" + SCHEME, re.IGNORECASE)
+JS_REMOTE = re.compile(r"(?:\bimport\s*\(|\bfrom)\s*[\"'`]\s*" + SCHEME, re.IGNORECASE)
+LOADS = {  # each tag, and the attributes that make the browser fetch by itself
+    "script": ("src",),
+    "img": ("src", "srcset"),
+    "source": ("src", "srcset"),
+    "iframe": ("src",),
+    "frame": ("src",),
+    "embed": ("src",),
+    "object": ("data",),
+    "audio": ("src",),
+    "video": ("src", "poster"),
+    "track": ("src",),
+    "input": ("src",),
+    "link": ("href", "imagesrcset"),
+    "base": ("href",),
+    "image": ("href", "xlink:href"),
+    "use": ("href", "xlink:href"),
+    "feimage": ("href", "xlink:href"),
+}
+QUIET_LINKS = {"alternate", "author", "bookmark", "canonical", "external", "help", "license", "me"}
+REFRESH_URL = re.compile(r"url\s*=\s*['\"]?\s*" + SCHEME, re.IGNORECASE)
+
+
+def remote_srcset(value: str) -> bool:
+    return any(REMOTE.match(candidate) for candidate in value.split(","))
+
+
+class Page(HTMLParser):
+    """Collects whether a page loads anything from another host."""
+
+    def __init__(self) -> None:
+        super().__init__(convert_charrefs=True)
+        self.found = False
+        self.inside: str | None = None
+
+    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
+        values = {name: value or "" for name, value in attrs}
+        names = LOADS.get(tag, ())
+        if tag == "link" and set(values.get("rel", "").lower().split()) <= QUIET_LINKS:
+            names = ("imagesrcset",) if "rel" in values else names
+        for name in names:
+            value = values.get(name, "")
+            if remote_srcset(value) if name.endswith("srcset") else REMOTE.match(value):
+                self.found = True
+        if CSS_REMOTE.search(values.get("style", "")):
+            self.found = True
+        if tag == "meta" and values.get("http-equiv", "").lower() == "refresh":
+            self.found = self.found or bool(REFRESH_URL.search(values.get("content", "")))
+        self.inside = tag if tag in ("style", "script") else None
+
+    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
+        self.handle_starttag(tag, attrs)
+        self.inside = None
+
+    def handle_data(self, data: str) -> None:
+        pattern = {"style": CSS_REMOTE, "script": JS_REMOTE}.get(self.inside or "")
+        if pattern and pattern.search(data):
+            self.found = True
+
+    def handle_endtag(self, tag: str) -> None:
+        self.inside = None
+
+
+def loads_offsite(path: Path) -> bool:
+    text = path.read_text(encoding="utf-8", errors="replace")
+    suffix = path.suffix.lower()
+    if suffix in (".html", ".htm", ".svg"):
+        page = Page()
+        page.feed(text)
+        page.close()
+        return page.found
+    if suffix == ".css":
+        return bool(CSS_REMOTE.search(text))
+    if suffix in (".js", ".mjs"):
+        return bool(JS_REMOTE.search(text))
+    return False
+
+
+def offsite(site: Path) -> list[str]:
+    """Each file under site that loads something from another host, by its path in site."""
+    files = sorted(path for path in site.rglob("*") if path.is_file())
+    return [path.relative_to(site).as_posix() for path in files if loads_offsite(path)]
+
+
+def main(argv: list[str] | None = None) -> int:
+    args = sys.argv[1:] if argv is None else argv
+    site = Path(args[0]) if args else Path("website/_site")
+    if not site.is_dir() or not any(site.rglob("*.html")):
+        print(f"offsite: {site} holds no rendered pages: render the site first", file=sys.stderr)
+        return 1
+    found = offsite(site)
+    for name in found:
+        print(f"offsite: {name} loads something from another host", file=sys.stderr)
+    if found:
+        return 1
+    print("offsite: the site loads nothing from another host")
+    return 0
+
+
+if __name__ == "__main__":
+    sys.exit(main())
diff --git a/scripts/privacy.py b/scripts/privacy.py
index 6cb93fd..b8e384a 100644
--- a/scripts/privacy.py
+++ b/scripts/privacy.py
@@ -46,6 +46,18 @@ HOUSEKEEPING = {
     "transparency", "aspect", "interlace", "loop", "background", "timestamp", "duration",
 }  # fmt: skip
 JPEG_HOUSEKEEPING = {"APP0", "APP2", "APP14"}  # JFIF, the colour profile, Adobe's colour flag
+# the segments a picture needs, by marker: frames and their tables, scans, quantization, restart
+# intervals; and the comment and APPn segments, which Pillow reads and the metadata check names
+JPEG_SEGMENTS = (
+    (set(range(0xC0, 0xD0)) - {0xC8}) | {0xDA, 0xDB, 0xDD, 0xFE} | set(range(0xE0, 0xF0))
+)
+# the housekeeping APPn segments, by what each must start with and its fixed length (None: any,
+# and as many as the colour profile needs); anything else in one of them could be text
+JPEG_HOUSEKEEPING_SEGMENTS = {
+    0xE0: (b"JFIF\x00", 16),
+    0xE2: (b"ICC_PROFILE\x00", None),
+    0xEE: (b"Adobe", 14),
+}
 PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
 PNG_CHUNKS = {
     b"IHDR", b"PLTE", b"IDAT", b"IEND", b"tRNS", b"iCCP", b"sRGB", b"gAMA", b"cHRM", b"pHYs",
@@ -54,6 +66,7 @@ PNG_CHUNKS = {
 WEBP_CHUNKS = {b"VP8 ", b"VP8L", b"VP8X", b"ALPH", b"ICCP", b"ANIM", b"ANMF"}
 AFTER_END = "bytes after the image's end"
 CUT_SHORT = "unreadable as an image (cut short or malformed)"
+GONE = "unreadable (it went, or can't be opened, while being checked)"
 # A home folder, with or without a slash after it: the name runs to the first character a name
 # can't hold (/, a space, a quote, <, >, a bracket) or to the end, so /Users/<name>/ doesn't match.
 HOME = re.compile(rb"/(?:Users|home)/[^/\s\"'<>()]+")
@@ -90,6 +103,16 @@ def png_problem(data: bytes) -> str | None:
 def jpeg_end(data: bytes) -> int | None:
     """Where the JPEG's end-of-image marker (FFD9) ends, walking its segments and scans, so an
     FFD9 inside a segment (a thumbnail's) or a second JPEG appended isn't taken for it."""
+    return jpeg_walk(data)[0]
+
+
+def jpeg_walk(data: bytes) -> tuple[int | None, int | None]:
+    """jpeg_end's walk: where the image ends, and the first segment's marker a picture doesn't
+    need (a DNL or a JPGn), or a JFIF, ICC or Adobe segment holding anything but its own data,
+    all of which Pillow reads past. Text inside the scan's coded data, or in a colour profile's
+    own text, is out of its reach: make strip re-encodes a photo, and Dan looks at it."""
+    stray = None
+    seen: set[int] = set()
     at = 2  # past the start-of-image marker
     while at < len(data) and data[at] == 0xFF:
         while at < len(data) and data[at] == 0xFF:  # a marker may follow any number of fill bytes
@@ -98,18 +121,31 @@ def jpeg_end(data: bytes) -> int | None:
             return None
         marker, at = data[at], at + 1
         if marker == 0xD9:
-            return at
+            return at, stray
+        if marker not in JPEG_SEGMENTS and not 0xD0 <= marker <= 0xD7 and stray is None:
+            stray = marker  # TEM, a DNL, a JPGn, a reserved marker
         if 0xD0 <= marker <= 0xD7 or marker == 0x01:  # restart markers and TEM stand alone
             continue
-        at += int.from_bytes(data[at : at + 2], "big")  # the segment, its length included
+        length = int.from_bytes(data[at : at + 2], "big")  # the segment's, its length included
+        if marker in JPEG_HOUSEKEEPING_SEGMENTS and stray is None:
+            magic, fixed = JPEG_HOUSEKEEPING_SEGMENTS[marker]
+            again = fixed is not None and marker in seen
+            if (
+                again
+                or not data[at + 2 : at + length].startswith(magic)
+                or fixed not in (None, length)
+            ):
+                stray = marker
+            seen.add(marker)
+        at += length
         if marker == 0xDA:  # start of scan: its coded data runs to the next marker but a restart
             while (at := data.find(b"\xff", at)) != -1 and at + 1 < len(data):
                 if data[at + 1] != 0x00 and not 0xD0 <= data[at + 1] <= 0xD7:
                     break
                 at += 2  # a stuffed FF00, or a restart marker inside the scan
             else:
-                return None
-    return None
+                return None, stray
+    return None, stray
 
 
 def webp_problem(data: bytes) -> str | None:
@@ -131,7 +167,9 @@ def structure_problem(data: bytes) -> str | None:
     if data.startswith(PNG_SIGNATURE):
         return png_problem(data)
     if data.startswith(b"\xff\xd8"):
-        end = jpeg_end(data)
+        end, stray = jpeg_walk(data)
+        if stray is not None:
+            return f"a JPEG segment it doesn't allow (FF{stray:02X})"
         return CUT_SHORT if end is None else AFTER_END if end < len(data) else None
     if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
         return webp_problem(data)
@@ -186,17 +224,16 @@ def text_problem(data: bytes) -> str | None:
 def problems(root: Path) -> list[tuple[Path, str]]:
     found = []
     for path in committable(root):
-        if path.is_symlink():  # never followed: git commits the target's path, not the file
-            if HOME.search(committed_bytes(path)):
-                found.append((path, "a symlink to a home-folder path"))
-            continue
-        if path.suffix.lower() in READABLE | UNREADABLE:
-            reason = image_problem(path)
-            if reason:
-                found.append((path, reason))
-        reason = path_problem(path)
-        if reason:
-            found.append((path, reason))
+        try:  # a file can go, or lose its permissions, between the listing and the read
+            if path.is_symlink():  # never followed: git commits the target's path, not the file
+                linked = HOME.search(committed_bytes(path))
+                reasons = ["a symlink to a home-folder path" if linked else None]
+            else:
+                image = path.suffix.lower() in READABLE | UNREADABLE
+                reasons = [image_problem(path) if image else None, path_problem(path)]
+        except OSError:
+            reasons = [GONE]
+        found += [(path, reason) for reason in reasons if reason]
     return found
 
 
@@ -286,7 +323,13 @@ def command_check(root: Path) -> int:
             file=sys.stderr,
         )
         return 1
-    reported = {path.relative_to(root).as_posix(): committed_bytes(path) for path, _ in found}
+    reported = {}
+    for path, reason in found:
+        try:
+            if reason != GONE:
+                reported[path.relative_to(root).as_posix()] = committed_bytes(path)
+        except OSError:  # gone since: the history pass still checks every blob under its name
+            continue
     in_history = history_problems(root, reported)
     for name, sha, reason in in_history:
         print(f"privacy: {name} (in history, {sha[:7]}): {reason}", file=sys.stderr)
diff --git a/tests/test_gallery.py b/tests/test_gallery.py
index 35c1b9d..8235bf9 100644
--- a/tests/test_gallery.py
+++ b/tests/test_gallery.py
@@ -10,7 +10,9 @@ import pytest
 from PIL import Image
 
 import gallery
+import models
 from conftest import add_design
+from sitedocs import escaped
 
 META = """\
 title: Test hook
@@ -154,6 +156,24 @@ def test_the_other_free_text_comes_out_escaped(repo: Path) -> None:
     assert SHORTCODE not in page(repo)
 
 
+def test_print_settings_and_the_size_come_out_escaped(repo: Path) -> None:
+    meta = SIZED.replace("Infill: 20%", f"Infill: 20% {SHORTCODE}")
+    add_model(repo, meta=meta.replace("size: 1 in", f"size: 1 in {SHORTCODE}"))
+    assert SHORTCODE not in page(repo)
+
+
+def test_size_names_and_photo_names_come_out_escaped(repo: Path) -> None:
+    odd = f"25 mm {SHORTCODE}"
+    folder = add_model(repo, meta=SIZED.replace("  25 mm:", f'  "{odd}":'))
+    models.Model(folder).sized(odd).write_bytes(b"solid")
+    (folder / "photos").mkdir()
+    Image.new("RGB", (8, 8)).save(folder / "photos" / f"wall {SHORTCODE}.png")
+    text = page(repo)
+    assert SHORTCODE not in text
+    assert f": for 25 mm {escaped(SHORTCODE)}" in text
+    assert f"![wall {escaped(SHORTCODE)}](hook/photos/wall%20%7B%7B%3C%20meta%20title" in text
+
+
 def test_a_bracket_in_the_title_stays_inside_the_picture_s_alt_text(repo: Path) -> None:
     add_model(repo, meta=META.replace("title: Test hook", "title: Hook [v2]"))
     assert "![Hook \\[v2\\], as SolidCraft draws it](hook/hook.png)" in page(repo)
diff --git a/tests/test_offsite.py b/tests/test_offsite.py
new file mode 100644
index 0000000..a0195a5
--- /dev/null
+++ b/tests/test_offsite.py
@@ -0,0 +1,78 @@
+"""scripts/offsite.py: the site makes a visitor's browser fetch nothing from another host (S31)."""
+
+from __future__ import annotations
+
+from pathlib import Path
+
+import pytest
+
+import offsite
+
+PAGE = "<html><body><p>Hi</p>{}</body></html>"
+
+
+@pytest.mark.parametrize(
+    ("name", "text"),
+    [
+        ("index.html", PAGE.format('<script src="https://cdn.example.net/mathjax.js"></script>')),
+        ("index.html", PAGE.format("<LINK REL=stylesheet HREF=//fonts.example.com/css>")),
+        ("index.html", PAGE.format('<link rel="preload" href="https://example.com/f.woff2">')),
+        ("index.html", PAGE.format('<img alt="a>b" src=" http://example.com/pixel.gif">')),
+        (
+            "index.html",
+            PAGE.format('<img src="a.png" srcset="a.png 1x, https://x.example/b.png 2x">'),
+        ),
+        (
+            "index.html",
+            PAGE.format('<video src="v.mp4" poster="https://example.com/p.jpg"></video>'),
+        ),
+        ("index.html", PAGE.format('<object data="https://example.com/x.svg"></object>')),
+        ("index.html", PAGE.format('<img src="&#104;ttps://example.com/p.gif">')),
+        ("index.html", PAGE.format('<div style="background: url( https://example.com/b.png )">')),
+        (
+            "index.html",
+            PAGE.format("<style>@font-face{src:url(https://example.com/f.woff2)}</style>"),
+        ),
+        ("index.html", PAGE.format('<script>import("https://cdn.example.net/x.js")</script>')),
+        (
+            "index.html",
+            PAGE.format('<meta http-equiv="refresh" content="0; url=https://example.com/">'),
+        ),
+        ("index.html", PAGE.format('<svg><use href="https://example.com/s.svg#i"/></svg>')),
+        ("site_libs/theme.min.css", '@import"https://fonts.example.com/css2?family=Sans";'),
+        ("site_libs/theme.min.css", "body{background:image-set('https://example.com/b.png' 1x)}"),
+        ("site_libs/app.js", 'import { x } from "https://cdn.example.net/x.js";'),
+    ],
+)
+def test_a_load_from_another_host_is_named(tmp_path: Path, capsys, name: str, text: str) -> None:
+    (tmp_path / "index.html").write_text(PAGE.format(""), encoding="utf-8")
+    path = tmp_path / name
+    path.parent.mkdir(parents=True, exist_ok=True)
+    path.write_text(text, encoding="utf-8")
+    assert offsite.main([str(tmp_path)]) == 1
+    assert capsys.readouterr().err == f"offsite: {name} loads something from another host\n"
+
+
+def test_links_local_files_and_quiet_attributes_pass(tmp_path: Path, capsys) -> None:
+    (tmp_path / "index.html").write_text(
+        PAGE.format(
+            '<a href="https://github.com/x">repo</a><script src="site_libs/x.js"></script>'
+            '<link href="styles.css" rel="stylesheet"><img src="models/hook.png" '
+            'data-src="https://example.com/lazy.png">'
+            '<link rel="canonical" href="https://example.com/">'
+        ),
+        encoding="utf-8",
+    )
+    (tmp_path / "styles.css").write_text("body{background:url(b.png)}", encoding="utf-8")
+    (tmp_path / "search.js").write_text('var u="https://cdn.example.net/x.js"', encoding="utf-8")
+    assert offsite.main([str(tmp_path)]) == 0
+    assert "loads nothing from another host" in capsys.readouterr().out
+
+
+@pytest.mark.parametrize("make", [False, True])
+def test_a_missing_or_empty_site_fails(tmp_path: Path, capsys, make: bool) -> None:
+    site = tmp_path / "_site"
+    if make:
+        site.mkdir()
+    assert offsite.main([str(site)]) == 1
+    assert "holds no rendered pages" in capsys.readouterr().err
diff --git a/tests/test_privacy.py b/tests/test_privacy.py
index 70824ec..e92ddfc 100644
--- a/tests/test_privacy.py
+++ b/tests/test_privacy.py
@@ -356,3 +356,36 @@ def test_check_refuses_a_shallow_clone(repo: Path, capsys) -> None:
         "privacy: a shallow clone: fetch the whole history (git fetch --unshallow) "
         "so it can be checked\n",
     )
+
+
+@pytest.mark.parametrize("marker", [b"\xdc", b"\xf0"])
+def test_check_names_a_jpeg_segment_it_does_not_allow_without_printing_it(
+    repo: Path, capsys, marker: bytes
+) -> None:
+    path = photo(repo / "print.jpg")
+    text = b"taken at home"  # a DNL or a JPGn segment, which Pillow reads past
+    data = path.read_bytes()
+    path.write_bytes(
+        data[:2] + b"\xff" + marker + (len(text) + 2).to_bytes(2, "big") + text + data[2:]
+    )
+    expected = f"privacy: print.jpg: a JPEG segment it doesn't allow (FF{marker.hex().upper()})\n"
+    assert check(repo, capsys) == (1, expected)
+
+
+@pytest.mark.parametrize("marker", [b"\xe0", b"\xe2", b"\xee"])
+def test_check_names_a_housekeeping_segment_holding_text(repo: Path, capsys, marker: bytes) -> None:
+    path = photo(repo / "print.jpg")
+    text = b"taken at home"  # no JFIF, ICC or Adobe data: Pillow keeps it out of info
+    data = path.read_bytes()
+    path.write_bytes(
+        data[:2] + b"\xff" + marker + (len(text) + 2).to_bytes(2, "big") + text + data[2:]
+    )
+    expected = f"privacy: print.jpg: a JPEG segment it doesn't allow (FF{marker.hex().upper()})\n"
+    assert check(repo, capsys) == (1, expected)
+
+
+def test_check_names_a_file_that_goes_before_it_is_read(
+    repo: Path, capsys, monkeypatch: pytest.MonkeyPatch
+) -> None:
+    monkeypatch.setattr(privacy, "committable", lambda root: [root / "gone.jpg"])
+    assert check(repo, capsys) == (1, f"privacy: gone.jpg: {privacy.GONE}\n")
diff --git a/website/_quarto.yml b/website/_quarto.yml
index c4d91b3..2bb5475 100644
--- a/website/_quarto.yml
+++ b/website/_quarto.yml
@@ -32,7 +32,8 @@ website:
 
 format:
   html:
-    theme: cosmo
+    theme: [cosmo, theme.scss]
+    html-math-method: plain
     css: styles.css
     toc: true
     mermaid:
diff --git a/website/theme.scss b/website/theme.scss
new file mode 100644
index 0000000..105f782
--- /dev/null
+++ b/website/theme.scss
@@ -0,0 +1,3 @@
+/*-- scss:defaults --*/
+// No web font: a font from another host would tell it who visits (scripts/offsite.py)
+$web-font-path: false;
```

- [x] **Step 2: Run the tests; watch them fail.** Apply only the tests first:
  `git apply --include='tests/*' .git/task2.patch`, then `make test`. Expected: pytest stops while
  collecting, with `ModuleNotFoundError: No module named 'offsite'` and `Interrupted: 1 error
  during collection`.
- [x] **Step 3: The code.** `git apply --exclude='tests/*' .git/task2.patch`. What it does: the
  JPEG walk names any segment a picture doesn't need, and any JFIF, colour-profile or Adobe segment
  holding more than its own data, by its marker, as PNG chunks are named; a file that goes, or
  can't be opened, between the listing and the read is reported as `privacy.GONE`, not a
  traceback; the page escapes print settings, the size, each size's name and each photo's alt text,
  and quotes each photo's link; `make docs` fails when the rendered site would load a script, style
  sheet, font, image or frame from another host, or when there's no rendered site to check; the
  theme drops Bootswatch's web font (`$web-font-path: false`) and the pages render maths as plain
  text, so neither Google's fonts nor MathJax loads.
- [x] **Step 4: The docs.** In the spec's *The commands* table, the `make docs` row ends "…,
  fails on an unresolved link or anything it loads from another host, runs lychee where
  installed". In `website/architecture.qmd`, "Checks and the deploy", the site node reads
  `site["site job<br/>make docs: render, offsite check, lychee"]`.
- [x] **Step 5: Run the checks; they pass.** `make check`. Expected: 158 tests pass twice, lint
  passes, `offsite: the site loads nothing from another host`.
- [x] **Step 6: Commit.** Write the message to `.git/COMMIT_MSG`:

```text
fix(privacy): 🤖 refuse JPEG segments that could hold text, and load nothing off-site

Phase 1's end left three photo gaps for before the first photo: a JPEG
segment Pillow skips (a DNL or JPGn, or a JFIF, colour-profile or Adobe
segment holding something else) passed the check; a file that went
between the listing and the read raised a traceback; and print settings,
the size, size names and photo names went onto a page raw. The JPEG walk
now names those segments, a file that can't be read is reported, those
fields are escaped as the notes are, and a photo's link is quoted. Text in
the scan's coded data or a colour profile's own text stays out of reach:
make strip and Dan's look cover it.

After the merge, the live site loaded Google's fonts on every page and
MathJax and a polyfill from two CDNs on the Models page, each of which
sees every visitor. The theme drops the web font, maths renders as plain
text, and make docs now fails on anything the site would load from
another host (scripts/offsite.py), or on a site that isn't there.

The new tests failed first with: ModuleNotFoundError: No module named
'offsite', stopping the collection.

Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 1
Co-Authored-By: <the model's own line>
```

  `git add scripts/privacy.py tests/test_privacy.py scripts/gallery.py tests/test_gallery.py scripts/offsite.py tests/test_offsite.py Makefile pyproject.toml website/_quarto.yml website/theme.scss docs/superpowers/specs/2026-11-05-3d-models-design.md website/architecture.qmd`,
  then `git commit -F .git/COMMIT_MSG`, then `git log -1 --format='%(trailers)'` shows the
  `Plan:` line.
- [x] **Step 7: Review, look forward, close.**

  - **Review (Tier 1: Matt Pocock's `code-review`, two axes in two subagents, plus the security
    checklist, one line per item; at most one re-review),** from `$(cat .git/TASK_BASE)`.
  - **Forward:** the look test's photo (Task 12) is the first the check meets.
  - **Docs:** Step 4; S31 `built`, S03 stays `built`. After the merge, the phase end's step 9 looks
    at the live site's network log too.
  - **Close,** its own commit: this task's boxes ticked, **Now** set to the next task, any
    Built differently and Ruling lines, deferred findings on the phase-end list, the spec's
    scenario statuses. The message, from `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 1: Close the privacy gaps, and load nothing from other hosts

    <what the task built, and why, in a few lines>

    Drift: <filled at the close, or none>
    Rulings: <filled at the close, or none>
    Phase-end: <filled at the close, or none>
    Forward: <filled at the close, or none>
    Tier: 1
    Rounds: <filled at the close>
    Findings: <filled at the close, or none>

    Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 1
    Co-Authored-By: <the model's own line>
    ```

  - **Push** under the standing OK (Phase 2 Q&A 7): `make leaks privacy models-check`, then
    `git push origin phase-2`. The task is closed once CI on the closing commit, or a later one,
    is green.

***

### Task 2: The rail's wall feet

> **Built differently** (closed 2026-11-06; commits ee53ea2, 3144398): `head_h` is 4.2 mm, not the listing's 3 mm, and the test's least head height 4 mm, since a #8 pan head stands about 3.6 mm and a #10 about 4.1 mm and the cap couldn't seat over it (Task 2's review, Important); step 4 of the notes says the rail's lower end swings in over the bottom cup.

**Tier:** 2 · **Scenarios:** S28, S14, S32

**Files:**
- Create: `models/rail-feet/rail-feet.sc` (by SolidCraft), its built files (`rail-feet.stl`, `-3-4in.stl`, `-25mm.stl`, `.png`, `.eval.json`, `build.json`, by
  `make models`), `models/rail-feet/model.yml`, `tests/test_rail_feet.py`
- Modify: `website/architecture.qmd` (its nodes turn solid), `models/dowel-fit-coupon/model.yml` (its notes)

**Interfaces:**
- Consumes: Phase 1's `make models`, `models.Model`, `models.sizes`, `models.read_yml` and the
  conftest helpers `params`, `body` and `measured`; the coupon's `step`; the earlier rail parts'
  parameters, where its test checks them against its own. It's built at the placeholder sizes
  (Phase 2 Q&A 9); Task 11 retunes it to Task 10's measurements.
- Produces: the two feet that hold the rail off the wall, and their caps; the parameters and bodies its test names.

- [x] **Step 0: Record the base:** `git rev-parse HEAD > .git/TASK_BASE`.
- [x] **Step 1: Write the failing test.**

`tests/test_rail_feet.py`:

```python
"""The rail's wall feet (S28, S14, S32): cups for the rail's ends, screws the room can't see, and
a rail that can't be lifted out of them."""

from __future__ import annotations

from pathlib import Path

import pytest

import models
from conftest import body, params

MODELS = Path(__file__).resolve().parent.parent / "models"
FEET = models.Model(MODELS / "rail-feet")
COUPON = models.Model(MODELS / "dowel-fit-coupon")
SCREW_HEAD_MM = 3.0  # a #8 or #10 pan or washer head, and a toggle bolt's


def test_two_feet_and_two_caps_each_one_closed_body() -> None:
    for name in ("Bottom foot", "Top foot", "Cap 1", "Cap 2"):
        assert body(FEET, name)["closed"]


def test_it_is_saved_for_one_inch_and_comes_in_three_sizes() -> None:
    assert params(FEET)["dowel_d"] == pytest.approx(25.4)
    assert set(models.sizes(FEET)) == {"3/4 in", "25 mm"}


def test_each_cup_takes_the_dowel_with_one_of_the_coupons_clearances() -> None:
    p, step = params(FEET), params(COUPON)["step"]
    assert p["bore_d"] == pytest.approx(p["dowel_d"] + p["clearance"])
    assert any(p["clearance"] == pytest.approx(k * step) for k in (1, 2, 3, 4))


def test_each_plate_sits_flat_on_the_wall_with_room_for_the_cord_behind_the_rail() -> None:
    p = params(FEET)
    for name in ("Bottom foot", "Top foot"):
        assert body(FEET, name)["bbox"]["min"][0] == pytest.approx(-p["standoff"])
    assert p["standoff"] - p["dowel_d"] / 2 >= p["cord_depth"]
    assert p["cord_depth"] < p["plate_t"]


def test_each_screw_sits_behind_the_rail_under_a_cap() -> None:
    p, cap = params(FEET), body(FEET, "Cap 1")["bbox"]
    assert p["head_d"] < 19.05  # narrower than even a 3/4-inch rail in front of it
    assert p["head_depth"] == pytest.approx(p["head_h"] + p["cap_h"])
    assert p["head_h"] >= SCREW_HEAD_MM
    assert p["head_depth"] < p["plate_t"]
    assert cap["max"][2] - cap["min"][2] == pytest.approx(p["cap_h"])


def test_the_rail_lifts_into_the_top_cup_past_the_bottom_cups_rim() -> None:
    p = params(FEET)
    assert p["lift_room"] > p["low_depth"]
    assert p["high_depth"] - p["insert_min"] >= p["lift_room"] + 2 * 5.0  # 5 mm either way
    top = body(FEET, "Top foot")["bbox"]
    height = p["floor_t"] + p["high_depth"] + p["tab_h"]
    assert top["max"][2] - top["min"][2] == pytest.approx(height)


def test_a_screw_up_through_the_bottom_floor_holds_the_rail_down() -> None:
    p = params(FEET)
    assert p["pin_d"] < p["dowel_d"] / 4
    assert p["floor_t"] - p["pin_head_h"] >= 2.0


def test_the_notes_give_where_the_top_screw_goes() -> None:
    p, notes = params(FEET), models.read_yml(FEET)["notes"]
    gap = (p["lift_room"] + p["high_depth"] - p["insert_min"]) / 2
    expected = p["low_depth"] + p["high_depth"] + p["tab_h"] - gap
    assert p["spacing_less"] == pytest.approx(expected)
    assert f"less {p['spacing_less']:g} mm" in notes
    assert f"within {p['spacing_tol']:g} mm" in notes
```

- [x] **Step 2: Run it; watch it fail.** `make test`. Expected: `FileNotFoundError` for
  `models/rail-feet/rail-feet.eval.json`.
- [x] **Step 3: Build the design.** Write SolidCraft's command script to
  `.git/rail-feet-script.json` (it stays out of the repo: the saved design holds the same feature tree):

```json
{
  "commands": [
    {"command": "parameters.add", "params": {"name": "dowel_d", "expression": "25.4 mm", "comment": "the rail's and the arm's dowel: 1 inch as saved; the page offers 3/4 in and 25 mm"}},
    {"command": "parameters.add", "params": {"name": "clearance", "expression": "0.4 mm", "comment": "added to the dowel for every bore: the coupon's hole that fit"}},
    {"command": "parameters.add", "params": {"name": "bore_d", "expression": "dowel_d + clearance", "comment": "every cup's and socket's bore"}},
    {"command": "parameters.add", "params": {"name": "standoff", "expression": "32 mm", "comment": "the rail's axis from the wall: room behind it for the cord"}},
    {"command": "parameters.add", "params": {"name": "cup_wall", "expression": "4 mm", "comment": "plastic round each cup"}},
    {"command": "parameters.add", "params": {"name": "cup_od", "expression": "bore_d + 2 * cup_wall", "comment": "a cup's outside"}},
    {"command": "parameters.add", "params": {"name": "floor_t", "expression": "5 mm", "comment": "a cup's closed end"}},
    {"command": "parameters.add", "params": {"name": "low_depth", "expression": "25 mm", "comment": "how far the rail stands in the bottom cup"}},
    {"command": "parameters.add", "params": {"name": "high_depth", "expression": "64 mm", "comment": "the top cup's depth: the rail lifts into it past the bottom cup's rim"}},
    {"command": "parameters.add", "params": {"name": "insert_min", "expression": "25 mm", "comment": "the least the rail's top stays in the top cup"}},
    {"command": "parameters.add", "params": {"name": "lift_room", "expression": "low_depth + 3 mm", "comment": "how far the rail must rise to clear the bottom cup's rim"}},
    {"command": "parameters.add", "params": {"name": "plate_t", "expression": "10 mm", "comment": "the plate on the wall"}},
    {"command": "parameters.add", "params": {"name": "plate_w", "expression": "40 mm", "comment": "the plate's width"}},
    {"command": "parameters.add", "params": {"name": "tab_h", "expression": "22 mm", "comment": "each plate beyond its cup, behind the rail, where its screw goes"}},
    {"command": "parameters.add", "params": {"name": "screw_d", "expression": "5 mm", "comment": "each plate's screw hole: #8 or #10 wood screws, 3/16 in toggle bolts"}},
    {"command": "parameters.add", "params": {"name": "head_d", "expression": "10.5 mm", "comment": "the counterbore round each screw's head"}},
    {"command": "parameters.add", "params": {"name": "head_h", "expression": "3 mm", "comment": "a pan or washer head's height"}},
    {"command": "parameters.add", "params": {"name": "cap_h", "expression": "2 mm", "comment": "a printed cap's height, pressed in over the head"}},
    {"command": "parameters.add", "params": {"name": "head_depth", "expression": "head_h + cap_h", "comment": "the counterbore's depth: the head, then its cap"}},
    {"command": "parameters.add", "params": {"name": "pin_d", "expression": "4 mm", "comment": "the bottom cup's floor: a hole for a #6 screw up into the rail's end"}},
    {"command": "parameters.add", "params": {"name": "pin_head_d", "expression": "8 mm", "comment": "the counterbore under the floor for that screw's head"}},
    {"command": "parameters.add", "params": {"name": "pin_head_h", "expression": "3 mm", "comment": "that counterbore's depth"}},
    {"command": "parameters.add", "params": {"name": "cord_w", "expression": "7 mm", "comment": "the cord's groove up the back of the bottom foot"}},
    {"command": "parameters.add", "params": {"name": "cord_depth", "expression": "7 mm", "comment": "the groove's depth: at least the cord's thickness and 1 mm"}},
    {"command": "parameters.add", "params": {"name": "cord_y", "expression": "-9.5 mm", "comment": "the cord groove's centre, beside the screw"}},
    {"command": "parameters.add", "params": {"name": "spacing_less", "expression": "low_depth + high_depth + tab_h - (lift_room + high_depth - insert_min) / 2", "comment": "the top screw goes the rail's length less this above the bottom screw"}},
    {"command": "parameters.add", "params": {"name": "spacing_tol", "expression": "(high_depth - insert_min - lift_room) / 2", "comment": "how far either way the top screw may be off"}},
    {"command": "parameters.add", "params": {"name": "top_y", "expression": "70 mm", "comment": "the top foot sits beside the bottom foot, for printing"}},
    {"command": "solid.cylinder", "params": {"diameter": "cup_od", "height": "floor_t + low_depth", "base": [0, "0 mm", 0], "axis": "Z", "body_name": "Bottom foot"}},
    {"command": "solid.box", "params": {"length": "standoff - plate_t + 1 mm", "width": "cup_od - 8 mm", "height": "floor_t + low_depth", "corner": ["-standoff + plate_t - 0.5 mm", "0 mm - (cup_od - 8 mm) / 2", 0], "operation": "join", "targets": ["Bottom foot"]}},
    {"command": "solid.box", "params": {"length": "plate_t", "width": "plate_w", "height": "floor_t + low_depth + tab_h", "corner": ["-standoff", "0 mm - plate_w / 2", 0], "operation": "join", "targets": ["Bottom foot"]}},
    {"command": "solid.cylinder", "params": {"diameter": "bore_d", "height": "low_depth + 1 mm", "base": [0, "0 mm", "floor_t"], "axis": "Z", "operation": "cut", "targets": ["Bottom foot"]}},
    {"command": "solid.cylinder", "params": {"diameter": "screw_d", "height": "plate_t + 2 mm", "base": ["-standoff - 1 mm", "0 mm", "floor_t + low_depth + tab_h / 2"], "axis": "X", "operation": "cut", "targets": ["Bottom foot"]}},
    {"command": "solid.cylinder", "params": {"diameter": "head_d", "height": "head_depth + 1 mm", "base": ["-standoff + plate_t - head_depth", "0 mm", "floor_t + low_depth + tab_h / 2"], "axis": "X", "operation": "cut", "targets": ["Bottom foot"]}},
    {"command": "solid.cylinder", "params": {"diameter": "cup_od", "height": "floor_t + high_depth", "base": [0, "top_y", 0], "axis": "Z", "body_name": "Top foot"}},
    {"command": "solid.box", "params": {"length": "standoff - plate_t + 1 mm", "width": "cup_od - 8 mm", "height": "floor_t + high_depth", "corner": ["-standoff + plate_t - 0.5 mm", "top_y - (cup_od - 8 mm) / 2", 0], "operation": "join", "targets": ["Top foot"]}},
    {"command": "solid.box", "params": {"length": "plate_t", "width": "plate_w", "height": "floor_t + high_depth + tab_h", "corner": ["-standoff", "top_y - plate_w / 2", 0], "operation": "join", "targets": ["Top foot"]}},
    {"command": "solid.cylinder", "params": {"diameter": "bore_d", "height": "high_depth + 1 mm", "base": [0, "top_y", "floor_t"], "axis": "Z", "operation": "cut", "targets": ["Top foot"]}},
    {"command": "solid.cylinder", "params": {"diameter": "screw_d", "height": "plate_t + 2 mm", "base": ["-standoff - 1 mm", "top_y", "floor_t + high_depth + tab_h / 2"], "axis": "X", "operation": "cut", "targets": ["Top foot"]}},
    {"command": "solid.cylinder", "params": {"diameter": "head_d", "height": "head_depth + 1 mm", "base": ["-standoff + plate_t - head_depth", "top_y", "floor_t + high_depth + tab_h / 2"], "axis": "X", "operation": "cut", "targets": ["Top foot"]}},
    {"command": "solid.cylinder", "params": {"diameter": "pin_d", "height": "floor_t + 2 mm", "base": [0, 0, "-1 mm"], "axis": "Z", "operation": "cut", "targets": ["Bottom foot"]}},
    {"command": "solid.cylinder", "params": {"diameter": "pin_head_d", "height": "pin_head_h + 1 mm", "base": [0, 0, "-1 mm"], "axis": "Z", "operation": "cut", "targets": ["Bottom foot"]}},
    {"command": "solid.box", "params": {"length": "cord_depth + 1 mm", "width": "cord_w", "height": "floor_t + low_depth + tab_h + 2 mm", "corner": ["-standoff - 1 mm", "cord_y - cord_w / 2", "-1 mm"], "operation": "cut", "targets": ["Bottom foot"]}},
    {"command": "solid.cylinder", "params": {"diameter": "head_d - 0.1 mm", "height": "cap_h", "base": ["45 mm", "-12 mm", 0], "axis": "Z", "body_name": "Cap 1"}},
    {"command": "solid.cylinder", "params": {"diameter": "head_d - 0.1 mm", "height": "cap_h", "base": ["45 mm", "12 mm", 0], "axis": "Z", "body_name": "Cap 2"}},
    {"command": "file.save_as", "params": {"path": "models/rail-feet/rail-feet.sc", "format": "json", "cache": false}}
  ]
}
```

  From the repo's root: `mkdir -p models/rail-feet`, then
  `solidcraft-cli run .git/rail-feet-script.json --quiet`. Expected: exit 0, and
  `models/rail-feet/rail-feet.sc` is plain-text JSON.
- [x] **Step 4: Write its page's text.**

`models/rail-feet/model.yml`:

```yaml
title: Rail wall feet
summary: >-
  The two feet that hold a vertical dowel rail off the wall: a closed cup over each end of the
  rail, their screws hidden behind it under caps.
status: designed
material: PETG, matte (never PLA for these parts)
size: 1 in
sizes:
  3/4 in: {dowel_d: 19.05 mm}
  25 mm: {dowel_d: 25 mm}
print:
  Orientation: as saved, each foot on its cup's closed end (the top foot upside down); the caps flat
  Layer height: 0.2 mm
  Walls: 5
  Infill: 40% gyroid
  Supports: none
notes: |
  The rail is a dowel up to about 48 inches long, standing 32 mm off the wall so the light's cord
  can run behind it. Each foot is screwed to the wall through its plate where the rail stands in
  front of the screw, and a printed cap presses in over the head: #8 or #10 pan-head wood screws
  into a stud, or 3/16-inch toggle bolts in drywall, never plastic plugs. The top cup is deep, so
  the rail lifts into it past the bottom cup's rim; a #6 × 3/4-inch screw up through the bottom
  cup's floor into the rail's end then holds it down, so lifting a planter or the light can't
  raise it, and it can't turn.

  **Putting the rail together,** from the wall out. The light's cord goes in first, since its plug
  won't pass through a hole:

  1. Cut the rail. The top screw goes the rail's length less 77.5 mm above the bottom screw,
     plumb, within 5.5 mm either way.
  2. Press the cord into the groove up the bottom foot's back, screw the foot on, and press a cap
     in over the screw.
  3. Screw the top foot on, and press its cap in.
  4. Push the rail's top up into the top cup, swing its foot over the bottom cup, and let it down.
     Drill a 2 mm pilot into the rail's end through the floor's hole, and drive the #6 screw.
  5. Lay the cord down behind the rail before any carrier goes on below the light.
  6. Stick a 3 mm felt or rubber pad on the end of each carrier's two arms, push the carrier onto
     the rail at its height, and tap its wedge up from below with a mallet.
  7. Slide the arm socket down the carrier's dovetail, push in the arm (550 mm puts the light
     24 inches out), and tap its wedge in along the arm's top.
  8. Push the tip onto the arm's end, its stem down, and tap its wedge in.
  9. Snap the clips on under the arm; press the cord into them, into the keel and into the stem,
     and slide it in the stem's grip to set the light's height.
  10. Slide the shade up over the bulb, its notches past the stem's lugs, and turn it a quarter
      turn.

  To move a carrier, push its wedge down from above with a thin punch, through the channel behind
  the rail; pull the socket's and the tip's wedges out by their thick ends.

  - **Clearance:** the bore is the dowel plus `clearance`, from the fit-test coupon. The 0.4 mm
    it's saved with is a placeholder until the coupon is printed.

  This is a first design, not yet printed or load-tested; its page will say when it has been.
```

  Then `make models`. Expected: `building models/rail-feet (missing …)` and `1 built`. Look at
  `rail-feet.png` against the notes.
- [x] **Step 4b: The coupon's notes.** In `models/dowel-fit-coupon/model.yml`, the sentence
  "standing on its edge: the dowel parts' sockets print with their holes horizontal, and a
  horizontal hole comes out a little smaller and less round than a vertical one." becomes
  "standing on its edge: the sockets that hold an arm print with their holes horizontal, and a
  horizontal hole comes out a little smaller and less round than a vertical one. The rail's feet
  and carrier print theirs upright, a little closer to size, and their wedge or their slack takes
  that up.", its lines rewrapped at 100 characters as the file's are.
- [x] **Step 5: The diagrams.** In `website/architecture.qmd`, delete the lines `  class feet planned` ("The rail, part by part") and `  class foot planned` ("The light's cord"): the
  part is built.
- [x] **Step 6: Run the checks; they pass.** `make check`. Expected: every test passes twice,
  every model's build matches its design, the privacy and offsite checks pass, the render lists
  the model's page.
- [x] **Step 7: Commit.** Write the message to `.git/COMMIT_MSG`:

```text
feat(models): 🤖 add the two feet that hold the rail off the wall, and their caps

The rail needs holding off the wall with no screw in sight (Phase 2 Q&A 1).
Each foot is a closed cup with a plate beyond it, screwed to the wall where
the rail, once in, stands in front of the screw; a printed cap covers each
head, since the rail hides it only from straight in front. The top cup is
deep, so the rail lifts into it past the bottom cup's rim, and a screw up
through the bottom cup's floor into the rail's end holds it down: lifting a
carrier or a planter can't raise it (the phase-start council's critical
finding against keyholes). A groove up the bottom foot's back holds the
cord. The notes say how the rail goes together, and where the top screw
goes. The coupon's notes now say which parts print their bores upright.
Saved at 1 inch, with STLs for 3/4 inch and 25 mm.

The new test failed first with: FileNotFoundError for
models/rail-feet/rail-feet.eval.json.

Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 2
Co-Authored-By: <the model's own line>
```

  `git add models/rail-feet/rail-feet.sc models/rail-feet/rail-feet.stl models/rail-feet/rail-feet-3-4in.stl models/rail-feet/rail-feet-25mm.stl models/rail-feet/rail-feet.png models/rail-feet/rail-feet.eval.json models/rail-feet/build.json models/rail-feet/model.yml tests/test_rail_feet.py website/architecture.qmd models/dowel-fit-coupon/model.yml`, then `git commit -F .git/COMMIT_MSG`, then `git log -1 --format='%(trailers)'`
  shows the `Plan:` line.
- [x] **Step 8: Review, look forward, close.** The review looks at the picture and the page's
  viewer, not the `.sc` alone.

  - **Review (Tier 2, one reviewer under both headings, Standards and Spec, per Phase 1's retro;
    fix Critical and Important; at most one re-review),** from `$(cat .git/TASK_BASE)`.
  - **Forward:** Task 7 links its page; Task 8 publishes it; Task 11 retunes it; the look test
    (Task 12) prints it.
  - **Docs:** the diagrams (Step 5); S28 stays `planned` until Task 5.
  - **Close,** its own commit: this task's boxes ticked, **Now** set to the next task, any
    Built differently and Ruling lines, deferred findings on the phase-end list, the spec's
    scenario statuses. The message, from `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 2: The rail's wall feet

    <what the task built, and why, in a few lines>

    Drift: <filled at the close, or none>
    Rulings: <filled at the close, or none>
    Phase-end: <filled at the close, or none>
    Forward: <filled at the close, or none>
    Tier: 2
    Rounds: <filled at the close>
    Findings: <filled at the close, or none>

    Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 2
    Co-Authored-By: <the model's own line>
    ```

  - **Push** under the standing OK (Phase 2 Q&A 7): `make leaks privacy models-check`, then
    `git push origin phase-2`. The task is closed once CI on the closing commit, or a later one,
    is green.

***

### Task 3: The rail carrier and its wedge

> **Built differently** (closed 2026-11-06; commits 0182054, 68f412b): the test's comment on a dowel off its size says the coupon picks its clearance and `wedge_top` follows it, so the seat depends on the offset alone (Task 3's review, Important).

**Ruling:** S28's "a dowel 0.5 mm over or under" means a dowel off its size with the clearance the coupon picks for it, since the wedges' thin ends follow `clearance`; S28's wording says so. Costs if wrong: a dowel the coupon can't fit (over 0.8 mm off) isn't covered, and needs a wider coupon.

**Tier:** 2 · **Scenarios:** S28, S29, S14

**Files:**
- Create: `models/rail-carrier/rail-carrier.sc` (by SolidCraft), its built files (`rail-carrier.stl`, `-3-4in.stl`, `-25mm.stl`, `.png`, `.eval.json`, `build.json`, by
  `make models`), `models/rail-carrier/model.yml`, `tests/test_rail_carrier.py`
- Modify: `website/architecture.qmd` (its nodes turn solid)

**Interfaces:**
- Consumes: Phase 1's `make models`, `models.Model`, `models.sizes`, `models.read_yml` and the
  conftest helpers `params`, `body` and `measured`; the coupon's `step`; the earlier rail parts'
  parameters, where its test checks them against its own. It's built at the placeholder sizes
  (Phase 2 Q&A 9); Task 11 retunes it to Task 10's measurements.
- Produces: the U that pushes onto the rail from the front, and its wedge; the parameters and bodies its test names.

- [x] **Step 0: Record the base:** `git rev-parse HEAD > .git/TASK_BASE`.
- [x] **Step 1: Write the failing test.**

`tests/test_rail_carrier.py`:

```python
"""The rail carrier (S28, S29, S14): onto the rail from the front, locked by a wedge behind it."""

from __future__ import annotations

from pathlib import Path

import pytest

import models
from conftest import body, params

MODELS = Path(__file__).resolve().parent.parent / "models"
CARRIER = models.Model(MODELS / "rail-carrier")
FEET = models.Model(MODELS / "rail-feet")
COUPON = models.Model(MODELS / "dowel-fit-coupon")


def test_the_carrier_and_its_wedge_are_each_one_closed_body() -> None:
    assert body(CARRIER, "Carrier")["closed"]
    assert body(CARRIER, "Wedge")["closed"]


def test_it_is_saved_for_one_inch_and_comes_in_three_sizes() -> None:
    assert params(CARRIER)["dowel_d"] == pytest.approx(25.4)
    assert set(models.sizes(CARRIER)) == {"3/4 in", "25 mm"}


def test_the_u_takes_the_dowel_with_one_of_the_coupons_clearances() -> None:
    p, step = params(CARRIER), params(COUPON)["step"]
    assert p["bore_d"] == pytest.approx(p["dowel_d"] + p["clearance"])
    assert any(p["clearance"] == pytest.approx(k * step) for k in (1, 2, 3, 4))


def test_its_arms_stop_short_of_the_wall_by_a_pads_thickness() -> None:
    p, carrier = params(CARRIER), body(CARRIER, "Carrier")["bbox"]
    assert p["standoff"] == pytest.approx(params(FEET)["standoff"])
    assert carrier["min"][0] == pytest.approx(-(p["standoff"] - p["wall_gap"]))
    assert 1.0 <= p["wall_gap"] <= 2.0  # a 3 mm felt or rubber pad takes it up


def test_it_is_long_enough_for_the_arm_at_24_inches() -> None:
    assert params(CARRIER)["carrier_l"] >= 100.0


def test_the_wedge_holds_by_friction_and_shows_below_to_be_tapped() -> None:
    p = params(CARRIER)
    assert p["taper"] <= 0.05  # 1 in 20 or gentler: it doesn't back out
    assert p["wedge_l"] > p["carrier_l"]


@pytest.mark.parametrize("off", [-0.5, 0.0, 0.5])
def test_a_dowel_half_a_millimetre_off_still_seats_the_wedge_inside(off: float) -> None:
    p = params(CARRIER)  # the wedge pushes the rail to the U's front, so the gap gains clearance/2
    below_top = (p["wedge_top"] - p["room_top"] - p["clearance"] / 2 + off) / p["taper"]
    assert 0 < below_top < p["carrier_l"] - 10.0


def test_the_wedge_is_thick_and_wide_enough_to_span_the_mouth() -> None:
    p, wedge = params(CARRIER), body(CARRIER, "Wedge")["bbox"]
    assert wedge["max"][0] - wedge["min"][0] == pytest.approx(p["wedge_w"])
    assert p["bore_d"] < p["wedge_w"] < p["bore_d"] + 2 * p["groove_d"]
    assert p["wedge_top"] >= 5.0


def test_the_cord_fits_behind_the_wedge_down_to_the_carriers_bottom() -> None:
    assert params(CARRIER)["channel"] >= 7.0
```

- [x] **Step 2: Run it; watch it fail.** `make test`. Expected: `FileNotFoundError` for
  `models/rail-carrier/rail-carrier.eval.json`.
- [x] **Step 3: Build the design.** Write SolidCraft's command script to
  `.git/rail-carrier-script.json` (it stays out of the repo: the saved design holds the same feature tree):

```json
{
  "commands": [
    {"command": "parameters.add", "params": {"name": "dowel_d", "expression": "25.4 mm", "comment": "the rail's and the arm's dowel: 1 inch as saved; the page offers 3/4 in and 25 mm"}},
    {"command": "parameters.add", "params": {"name": "clearance", "expression": "0.4 mm", "comment": "added to the dowel for every bore: the coupon's hole that fit"}},
    {"command": "parameters.add", "params": {"name": "bore_d", "expression": "dowel_d + clearance", "comment": "every cup's and socket's bore"}},
    {"command": "parameters.add", "params": {"name": "standoff", "expression": "32 mm", "comment": "the rail's axis from the wall: room behind it for the cord"}},
    {"command": "parameters.add", "params": {"name": "wall", "expression": "5 mm", "comment": "the U's wall"}},
    {"command": "parameters.add", "params": {"name": "r_o", "expression": "bore_d / 2 + wall", "comment": "the U's outside radius"}},
    {"command": "parameters.add", "params": {"name": "wall_gap", "expression": "1.5 mm", "comment": "between the U's arms and the wall, for a felt or rubber pad on each"}},
    {"command": "parameters.add", "params": {"name": "carrier_l", "expression": "110 mm", "comment": "the carrier's height: long enough for the arm at 24 inches"}},
    {"command": "parameters.add", "params": {"name": "groove_d", "expression": "2 mm", "comment": "the wedge's groove, cut into each arm"}},
    {"command": "parameters.add", "params": {"name": "taper", "expression": "0.04", "comment": "each wedge's and its groove's slope, 1 in 25", "unit": ""}},
    {"command": "parameters.add", "params": {"name": "room_top", "expression": "4.5 mm", "comment": "the groove's depth behind the dowel at the carrier's top"}},
    {"command": "parameters.add", "params": {"name": "wedge_l", "expression": "carrier_l + 10 mm", "comment": "the wedge's length"}},
    {"command": "parameters.add", "params": {"name": "wedge_top", "expression": "room_top + clearance / 2 + 20 mm * taper", "comment": "the wedge's thin end: seated 20 mm below the top on a nominal dowel"}},
    {"command": "parameters.add", "params": {"name": "wedge_w", "expression": "bore_d + 2 * groove_d - 0.5 mm", "comment": "the wedge's width, its wings in the grooves"}},
    {"command": "parameters.add", "params": {"name": "channel", "expression": "standoff - wall_gap - dowel_d / 2 - room_top - carrier_l * taper", "comment": "the cord's channel behind the wedge, at its narrowest (the carrier's bottom)"}},
    {"command": "parameters.add", "params": {"name": "dt_base", "expression": "12 mm", "comment": "the dovetail's width where it meets the carrier"}},
    {"command": "parameters.add", "params": {"name": "dt_top", "expression": "18 mm", "comment": "the dovetail's width at its face"}},
    {"command": "parameters.add", "params": {"name": "dt_h", "expression": "6 mm", "comment": "how far the dovetail stands out"}},
    {"command": "solid.cylinder", "params": {"diameter": "2 * r_o", "height": "carrier_l", "base": [0, 0, 0], "axis": "Z", "body_name": "Carrier"}},
    {"command": "solid.box", "params": {"length": "standoff - wall_gap", "width": "2 * r_o", "height": "carrier_l", "corner": ["-standoff + wall_gap", "-r_o", 0], "operation": "join", "targets": ["Carrier"]}},
    {"command": "solid.cylinder", "params": {"diameter": "bore_d", "height": "carrier_l + 2 mm", "base": [0, 0, "-1 mm"], "axis": "Z", "operation": "cut", "targets": ["Carrier"]}},
    {"command": "solid.box", "params": {"length": "standoff + 1 mm", "width": "bore_d", "height": "carrier_l + 2 mm", "corner": ["-standoff - 1 mm", "-bore_d / 2", "-1 mm"], "operation": "cut", "targets": ["Carrier"]}},
    {"command": "sketch.create", "params": {"plane": "XZ"}},
    {"command": "sketch.line", "params": {"points": [["-dowel_d / 2 + 2 mm", "1 mm"], ["-dowel_d / 2 + 2 mm", "-carrier_l - 1 mm"], ["-dowel_d / 2 - room_top + 1 mm * taper", "-carrier_l - 1 mm"], ["-dowel_d / 2 - room_top - (carrier_l + 1 mm) * taper", "1 mm"]], "closed": true}},
    {"command": "sketch.finish", "params": {}},
    {"command": "solid.extrude", "params": {"distance": "bore_d + 2 * groove_d", "direction": "symmetric", "operation": "cut", "targets": ["Carrier"]}},
    {"command": "sketch.create", "params": {"plane": "XY"}},
    {"command": "sketch.line", "params": {"points": [["r_o - 2 mm", "-dt_base / 2"], ["r_o + dt_h", "-dt_top / 2"], ["r_o + dt_h", "dt_top / 2"], ["r_o - 2 mm", "dt_base / 2"]], "closed": true}},
    {"command": "sketch.finish", "params": {}},
    {"command": "solid.extrude", "params": {"distance": "carrier_l", "operation": "join", "targets": ["Carrier"]}},
    {"command": "sketch.create", "params": {"plane": "YZ", "offset": "40 mm"}},
    {"command": "sketch.line", "params": {"points": [["0 mm", "0 mm"], ["wedge_l", "0 mm"], ["wedge_l", "0 mm + wedge_top + wedge_l * taper"], ["0 mm", "0 mm + wedge_top"]], "closed": true}},
    {"command": "sketch.finish", "params": {}},
    {"command": "solid.extrude", "params": {"distance": "wedge_w", "operation": "new", "body_name": "Wedge"}},
    {"command": "file.save_as", "params": {"path": "models/rail-carrier/rail-carrier.sc", "format": "json", "cache": false}}
  ]
}
```

  From the repo's root: `mkdir -p models/rail-carrier`, then
  `solidcraft-cli run .git/rail-carrier-script.json --quiet`. Expected: exit 0, and
  `models/rail-carrier/rail-carrier.sc` is plain-text JSON.
- [x] **Step 4: Write its page's text.**

`models/rail-carrier/model.yml`:

```yaml
title: Rail carrier
summary: >-
  A sleeve that pushes onto the rail from the front and locks with a wedge behind the rail, with a
  dovetail on its face for the light's arm or a planter.
status: designed
material: PETG, matte (never PLA for this part)
size: 1 in
sizes:
  3/4 in: {dowel_d: 19.05 mm}
  25 mm: {dowel_d: 25 mm}
print:
  Orientation: as saved, the carrier standing on its end; the wedge flat, the face that meets the rail on the bed
  Layer height: 0.2 mm
  Walls: 5
  Infill: 40% gyroid
  Supports: none
notes: |
  The carrier is a U that opens toward the wall: push it onto the mounted rail from the front at
  the height you want, then tap the wedge up from below, into the groove behind the rail, with a
  mallet. The groove and the wedge share a 1-in-25 slope, so the wedge's face stays flat against
  the rail all the way along; once it's tapped home, the arm's weight pulling the carrier down only
  tightens it. To move it, push the wedge down from above with a thin punch, through the channel
  behind the rail.

  - **The pads:** the U's arms stop 1.5 mm short of the wall; a 3 mm self-adhesive felt or rubber
    pad on each arm's end bears on the wall, so a push at the light can't turn the arm round the
    rail. The cord runs down the channel between the arms, behind the wedge.
  - **The dovetail** on its face takes the arm socket, and later a planter adapter: either slides
    down it from above.
  - **The wedge** prints flat, so the rail bends it along its layers.
  - **Clearance:** the bore is the dowel plus `clearance`, from the fit-test coupon. The 0.4 mm
    it's saved with is a placeholder until the coupon is printed.

  See *Putting the rail together* on the [wall feet](rail-feet.html) page for the order it all
  goes up in.

  This is a first design, not yet printed or load-tested; its page will say when it has been.
```

  Then `make models`. Expected: `building models/rail-carrier (missing …)` and `1 built`. Look at
  `rail-carrier.png` against the notes.
- [x] **Step 5: The diagrams.** In `website/architecture.qmd`, delete the lines `  class carrier planned` ("The rail, part by part") and `  class behind planned` ("The light's cord"): the
  part is built.
- [x] **Step 6: Run the checks; they pass.** `make check`. Expected: every test passes twice,
  every model's build matches its design, the privacy and offsite checks pass, the render lists
  the model's page.
- [x] **Step 7: Commit.** Write the message to `.git/COMMIT_MSG`:

```text
feat(models): 🤖 add the U that pushes onto the rail from the front, and its wedge

The light's arm, and later a planter, ride on the rail in a sliding joint
locked by a wedge (Phase 2 Q&A 1). The carrier is a U open toward the wall:
it pushes onto the mounted rail from the front; its arms stop 1.5 mm short
of the wall for a felt pad each, so a push at the light can't turn it; and a
wedge tapped up from below into a groove behind the rail locks it out of
sight. Groove and wedge share a 1-in-25 slope, so the wedge's face stays
flat on the rail; it prints flat, so the rail bends it along its layers. A
dovetail on its face takes the arm socket.
Saved at 1 inch, with STLs for 3/4 inch and 25 mm.

The new test failed first with: FileNotFoundError for
models/rail-carrier/rail-carrier.eval.json.

Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 3
Co-Authored-By: <the model's own line>
```

  `git add models/rail-carrier/rail-carrier.sc models/rail-carrier/rail-carrier.stl models/rail-carrier/rail-carrier-3-4in.stl models/rail-carrier/rail-carrier-25mm.stl models/rail-carrier/rail-carrier.png models/rail-carrier/rail-carrier.eval.json models/rail-carrier/build.json models/rail-carrier/model.yml tests/test_rail_carrier.py website/architecture.qmd`, then `git commit -F .git/COMMIT_MSG`, then `git log -1 --format='%(trailers)'`
  shows the `Plan:` line.
- [x] **Step 8: Review, look forward, close.** The review looks at the picture and the page's
  viewer, not the `.sc` alone.

  - **Review (Tier 2, one reviewer under both headings, Standards and Spec, per Phase 1's retro;
    fix Critical and Important; at most one re-review),** from `$(cat .git/TASK_BASE)`.
  - **Forward:** Task 7 links its page; Task 8 publishes it; Task 11 retunes it; the look test
    (Task 12) prints it.
  - **Docs:** the diagrams (Step 5); S28 stays `planned` until Task 5.
  - **Close,** its own commit: this task's boxes ticked, **Now** set to the next task, any
    Built differently and Ruling lines, deferred findings on the phase-end list, the spec's
    scenario statuses. The message, from `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 3: The rail carrier and its wedge

    <what the task built, and why, in a few lines>

    Drift: <filled at the close, or none>
    Rulings: <filled at the close, or none>
    Phase-end: <filled at the close, or none>
    Forward: <filled at the close, or none>
    Tier: 2
    Rounds: <filled at the close>
    Findings: <filled at the close, or none>

    Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 3
    Co-Authored-By: <the model's own line>
    ```

  - **Push** under the standing OK (Phase 2 Q&A 7): `make leaks privacy models-check`, then
    `git push origin phase-2`. The task is closed once CI on the closing commit, or a later one,
    is green.

***

### Task 4: The arm socket and its wedge

> **Built differently** (closed 2026-11-06; commits 2c3782f, the notes fix after it): the notes say the 7.5 N·m includes the shade and the arm itself (Task 4's review, Minor).

**Tier:** 2 · **Scenarios:** S28, S29, S13

**Files:**
- Create: `models/rail-arm-socket/rail-arm-socket.sc` (by SolidCraft), its built files (`rail-arm-socket.stl`, `-3-4in.stl`, `-25mm.stl`, `.png`, `.eval.json`, `build.json`, by
  `make models`), `models/rail-arm-socket/model.yml`, `tests/test_rail_arm_socket.py`
- Modify: `website/architecture.qmd` (its nodes turn solid)

**Interfaces:**
- Consumes: Phase 1's `make models`, `models.Model`, `models.sizes`, `models.read_yml` and the
  conftest helpers `params`, `body` and `measured`; the coupon's `step`; the earlier rail parts'
  parameters, where its test checks them against its own. It's built at the placeholder sizes
  (Phase 2 Q&A 9); Task 11 retunes it to Task 10's measurements.
- Produces: the block that slides down the carrier's dovetail and holds the arm level; the parameters and bodies its test names.

- [x] **Step 0: Record the base:** `git rev-parse HEAD > .git/TASK_BASE`.
- [x] **Step 1: Write the failing test.**

`tests/test_rail_arm_socket.py`:

```python
"""The arm socket (S28, S29, S13): onto the carrier's dovetail, the arm 2 inches deep, wedged."""

from __future__ import annotations

from pathlib import Path

import pytest

import models
from conftest import body, params

MODELS = Path(__file__).resolve().parent.parent / "models"
SOCKET = models.Model(MODELS / "rail-arm-socket")
CARRIER = models.Model(MODELS / "rail-carrier")
COUPON = models.Model(MODELS / "dowel-fit-coupon")
SHARED = ["wall", "r_o", "carrier_l", "dt_base", "dt_top", "dt_h", "dowel_d", "clearance"]


def test_the_socket_and_its_wedge_are_each_one_closed_body() -> None:
    assert body(SOCKET, "Arm socket")["closed"]
    assert body(SOCKET, "Arm wedge")["closed"]


def test_it_is_saved_for_one_inch_and_comes_in_three_sizes() -> None:
    assert params(SOCKET)["dowel_d"] == pytest.approx(25.4)
    assert set(models.sizes(SOCKET)) == {"3/4 in", "25 mm"}


@pytest.mark.parametrize("name", SHARED)
def test_its_slot_is_cut_for_the_carriers_dovetail(name: str) -> None:
    assert params(SOCKET)[name] == pytest.approx(params(CARRIER)[name])


def test_its_top_rests_on_the_dovetails_end() -> None:
    p, socket = params(SOCKET), body(SOCKET, "Arm socket")["bbox"]
    assert socket["min"][2] == pytest.approx(0.0)
    assert socket["max"][2] == pytest.approx(p["carrier_l"] + p["top_t"])
    assert 0 < p["fit"] < 0.5


def test_the_arm_goes_in_at_least_two_inches_with_the_coupons_clearance() -> None:
    p, step = params(SOCKET), params(COUPON)["step"]
    assert p["socket_depth"] >= 51.0
    assert p["bore_d"] == pytest.approx(p["dowel_d"] + p["clearance"])
    assert any(p["clearance"] == pytest.approx(k * step) for k in (1, 2, 3, 4))


@pytest.mark.parametrize("off", [-0.5, 0.0, 0.5])
def test_a_dowel_half_a_millimetre_off_still_seats_the_wedge_inside(off: float) -> None:
    # A dowel off its size gets the clearance the coupon picks for it (S28), and wedge_in follows
    # clearance, so the seat depends on the offset alone; the wedge pushes the arm down, so the
    # gap gains clearance / 2.
    p = params(SOCKET)
    short_of_end = (p["wedge_in"] - p["room_in"] - p["clearance"] / 2 + off) / p["taper"]
    assert 0 < short_of_end < p["socket_depth"] - 10.0


def test_the_wedges_groove_leaves_a_wall_above_it() -> None:
    p = params(SOCKET)
    deepest = p["dowel_d"] / 2 + p["room_in"] + p["socket_depth"] * p["taper"]
    assert p["boss_d"] / 2 - deepest >= 2.0
```

- [x] **Step 2: Run it; watch it fail.** `make test`. Expected: `FileNotFoundError` for
  `models/rail-arm-socket/rail-arm-socket.eval.json`.
- [x] **Step 3: Build the design.** Write SolidCraft's command script to
  `.git/rail-arm-socket-script.json` (it stays out of the repo: the saved design holds the same feature tree):

```json
{
  "commands": [
    {"command": "parameters.add", "params": {"name": "dowel_d", "expression": "25.4 mm", "comment": "the rail's and the arm's dowel: 1 inch as saved; the page offers 3/4 in and 25 mm"}},
    {"command": "parameters.add", "params": {"name": "clearance", "expression": "0.4 mm", "comment": "added to the dowel for every bore: the coupon's hole that fit"}},
    {"command": "parameters.add", "params": {"name": "bore_d", "expression": "dowel_d + clearance", "comment": "every cup's and socket's bore"}},
    {"command": "parameters.add", "params": {"name": "wall", "expression": "5 mm", "comment": "the carrier's U wall (rail-carrier)"}},
    {"command": "parameters.add", "params": {"name": "r_o", "expression": "bore_d / 2 + wall", "comment": "the carrier's outside radius (rail-carrier)"}},
    {"command": "parameters.add", "params": {"name": "carrier_l", "expression": "110 mm", "comment": "the carrier's height (rail-carrier)"}},
    {"command": "parameters.add", "params": {"name": "dt_base", "expression": "12 mm", "comment": "the carrier's dovetail where it meets the carrier (rail-carrier)"}},
    {"command": "parameters.add", "params": {"name": "dt_top", "expression": "18 mm", "comment": "the carrier's dovetail at its face (rail-carrier)"}},
    {"command": "parameters.add", "params": {"name": "dt_h", "expression": "6 mm", "comment": "how far the carrier's dovetail stands out (rail-carrier)"}},
    {"command": "parameters.add", "params": {"name": "fit", "expression": "0.3 mm", "comment": "the slot's clearance round the dovetail, each side"}},
    {"command": "parameters.add", "params": {"name": "top_t", "expression": "6 mm", "comment": "the block's closed top, which rests on the dovetail's top"}},
    {"command": "parameters.add", "params": {"name": "front_t", "expression": "5 mm", "comment": "the block in front of the slot"}},
    {"command": "parameters.add", "params": {"name": "block_w", "expression": "32 mm", "comment": "the block's width"}},
    {"command": "parameters.add", "params": {"name": "block_x", "expression": "r_o + fit", "comment": "the block's back face, just clear of the carrier"}},
    {"command": "parameters.add", "params": {"name": "boss_x", "expression": "block_x + dt_h + fit + front_t", "comment": "the block's front face, where the boss starts"}},
    {"command": "parameters.add", "params": {"name": "arm_z", "expression": "70 mm", "comment": "the arm's axis above the block's bottom"}},
    {"command": "parameters.add", "params": {"name": "socket_depth", "expression": "54 mm", "comment": "how far the arm goes in: at least 51 mm (2 inches)"}},
    {"command": "parameters.add", "params": {"name": "end_t", "expression": "6 mm", "comment": "the boss's closed end, behind the arm"}},
    {"command": "parameters.add", "params": {"name": "boss_wall", "expression": "7 mm", "comment": "plastic round the arm, room above for the wedge's groove"}},
    {"command": "parameters.add", "params": {"name": "boss_d", "expression": "bore_d + 2 * boss_wall", "comment": "the boss's outside"}},
    {"command": "parameters.add", "params": {"name": "groove_w", "expression": "8 mm", "comment": "the wedge's groove along the top of the bore"}},
    {"command": "parameters.add", "params": {"name": "taper", "expression": "0.04", "comment": "each wedge's and its groove's slope, 1 in 25", "unit": ""}},
    {"command": "parameters.add", "params": {"name": "room_in", "expression": "2 mm", "comment": "the groove's depth above the dowel at the bore's end"}},
    {"command": "parameters.add", "params": {"name": "wedge_l", "expression": "socket_depth + 20 mm", "comment": "the wedge's length"}},
    {"command": "parameters.add", "params": {"name": "wedge_in", "expression": "room_in + clearance / 2 + 20 mm * taper", "comment": "the wedge's thin end: seated 20 mm short of the bore's end on a nominal dowel"}},
    {"command": "solid.box", "params": {"length": "dt_h + fit + front_t", "width": "block_w", "height": "carrier_l + top_t", "corner": ["block_x", "-block_w / 2", 0], "body_name": "Arm socket"}},
    {"command": "sketch.create", "params": {"plane": "XY", "offset": "-1 mm"}},
    {"command": "sketch.line", "params": {"points": [["r_o - 2 mm", "-dt_base / 2 - fit"], ["r_o + dt_h + fit", "-dt_top / 2 - fit"], ["r_o + dt_h + fit", "dt_top / 2 + fit"], ["r_o - 2 mm", "dt_base / 2 + fit"]], "closed": true}},
    {"command": "sketch.finish", "params": {}},
    {"command": "solid.extrude", "params": {"distance": "carrier_l + 1 mm", "operation": "cut", "targets": ["Arm socket"]}},
    {"command": "solid.cylinder", "params": {"diameter": "boss_d", "height": "end_t + socket_depth + 2 mm", "base": ["boss_x - 2 mm", 0, "arm_z"], "axis": "X", "operation": "join", "targets": ["Arm socket"]}},
    {"command": "solid.cylinder", "params": {"diameter": "bore_d", "height": "socket_depth + 1 mm", "base": ["boss_x + end_t", 0, "arm_z"], "axis": "X", "operation": "cut", "targets": ["Arm socket"]}},
    {"command": "sketch.create", "params": {"plane": "XZ"}},
    {"command": "sketch.line", "params": {"points": [["boss_x + end_t - 0.5 mm", "-arm_z - dowel_d / 2 + 2 mm"], ["boss_x + end_t + socket_depth + 1 mm", "-arm_z - dowel_d / 2 + 2 mm"], ["boss_x + end_t + socket_depth + 1 mm", "-arm_z - dowel_d / 2 - room_in - (socket_depth + 1.5 mm) * taper"], ["boss_x + end_t - 0.5 mm", "-arm_z - dowel_d / 2 - room_in"]], "closed": true}},
    {"command": "sketch.finish", "params": {}},
    {"command": "solid.extrude", "params": {"distance": "groove_w", "direction": "symmetric", "operation": "cut", "targets": ["Arm socket"]}},
    {"command": "sketch.create", "params": {"plane": "YZ", "offset": "-40 mm"}},
    {"command": "sketch.line", "params": {"points": [["0 mm", "0 mm"], ["wedge_l", "0 mm"], ["wedge_l", "0 mm + wedge_in + wedge_l * taper"], ["0 mm", "0 mm + wedge_in"]], "closed": true}},
    {"command": "sketch.finish", "params": {}},
    {"command": "solid.extrude", "params": {"distance": "groove_w - 0.4 mm", "operation": "new", "body_name": "Arm wedge"}},
    {"command": "file.save_as", "params": {"path": "models/rail-arm-socket/rail-arm-socket.sc", "format": "json", "cache": false}}
  ]
}
```

  From the repo's root: `mkdir -p models/rail-arm-socket`, then
  `solidcraft-cli run .git/rail-arm-socket-script.json --quiet`. Expected: exit 0, and
  `models/rail-arm-socket/rail-arm-socket.sc` is plain-text JSON.
- [x] **Step 4: Write its page's text.**

`models/rail-arm-socket/model.yml`:

```yaml
title: Rail arm socket
summary: >-
  Holds the light's arm level, out from the rail: it slides down the carrier's dovetail, and a wedge
  along the top of its bore locks the arm.
status: designed
material: PETG, matte (never PLA for this part)
size: 1 in
sizes:
  3/4 in: {dowel_d: 19.05 mm}
  25 mm: {dowel_d: 25 mm}
print:
  Orientation: on its back, the flat face that meets the carrier on the bed and the boss pointing up; the wedge flat, split from it in the slicer
  Layer height: 0.2 mm
  Walls: 5
  Infill: 40% gyroid
  Supports: none; the slot's far wall bridges
notes: |
  The arm is a second dowel: cut to 550 mm, it puts the light 24 inches (610 mm) from the wall.
  Its end goes 54 mm into the socket, more than the 51 mm (2 inches) the joint needs: about
  7.5 N·m with a 1 kg light at 24 inches. Tap the wedge in along the top of the arm until it's
  tight; the groove's slope matches it, so it presses the arm down along its length. Pull it out
  by its thick end.

  - **The dovetail slot** is open at the bottom and closed at the top: slide the socket down the
    carrier's dovetail until its top rests on the dovetail's end.
  - **Printed on its back,** the block under the boss bends along its layers, not across them.
  - **A 3/4-inch arm** sags about three times as much as a 1-inch one: keep it short.
  - **Clearance:** the bore is the dowel plus `clearance`, from the fit-test coupon. The 0.4 mm
    it's saved with is a placeholder until the coupon is printed.

  See *Putting the rail together* on the [wall feet](rail-feet.html) page for the order it all
  goes up in.

  This is a first design, not yet printed or load-tested; its page will say when it has been.
```

  Then `make models`. Expected: `building models/rail-arm-socket (missing …)` and `1 built`. Look at
  `rail-arm-socket.png` against the notes.
- [x] **Step 5: The diagrams.** In `website/architecture.qmd`, delete the line `  class socket planned` ("The rail, part by part"): the
  part is built.
- [x] **Step 6: Run the checks; they pass.** `make check`. Expected: every test passes twice,
  every model's build matches its design, the privacy and offsite checks pass, the render lists
  the model's page.
- [x] **Step 7: Commit.** Write the message to `.git/COMMIT_MSG`:

```text
feat(models): 🤖 add the block that slides down the carrier's dovetail and holds the arm level

The "matching joint piece" (Phase 2 Q&A 1): a block whose dovetail slot,
open at the bottom and closed at the top, slides down the carrier's dovetail
until its top rests on it; a boss holds the arm 54 mm deep, more than the
2 inches the joint needs for about 7.5 N·m at 24 inches; a wedge along the
top of the bore, its groove sloped to match, locks the arm with no bolt, and
seats inside the bore on a dowel half a millimetre over or under. Printed on
its back, so the block bends along its layers.
Saved at 1 inch, with STLs for 3/4 inch and 25 mm.

The new test failed first with: FileNotFoundError for
models/rail-arm-socket/rail-arm-socket.eval.json.

Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 4
Co-Authored-By: <the model's own line>
```

  `git add models/rail-arm-socket/rail-arm-socket.sc models/rail-arm-socket/rail-arm-socket.stl models/rail-arm-socket/rail-arm-socket-3-4in.stl models/rail-arm-socket/rail-arm-socket-25mm.stl models/rail-arm-socket/rail-arm-socket.png models/rail-arm-socket/rail-arm-socket.eval.json models/rail-arm-socket/build.json models/rail-arm-socket/model.yml tests/test_rail_arm_socket.py website/architecture.qmd`, then `git commit -F .git/COMMIT_MSG`, then `git log -1 --format='%(trailers)'`
  shows the `Plan:` line.
- [x] **Step 8: Review, look forward, close.** The review looks at the picture and the page's
  viewer, not the `.sc` alone.

  - **Review (Tier 2, one reviewer under both headings, Standards and Spec, per Phase 1's retro;
    fix Critical and Important; at most one re-review),** from `$(cat .git/TASK_BASE)`.
  - **Forward:** Task 7 links its page; Task 8 publishes it; Task 11 retunes it; the look test
    (Task 12) prints it.
  - **Docs:** the diagrams (Step 5); S28 stays `planned` until Task 5.
  - **Close,** its own commit: this task's boxes ticked, **Now** set to the next task, any
    Built differently and Ruling lines, deferred findings on the phase-end list, the spec's
    scenario statuses. The message, from `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 4: The arm socket and its wedge

    <what the task built, and why, in a few lines>

    Drift: <filled at the close, or none>
    Rulings: <filled at the close, or none>
    Phase-end: <filled at the close, or none>
    Forward: <filled at the close, or none>
    Tier: 2
    Rounds: <filled at the close>
    Findings: <filled at the close, or none>

    Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 4
    Co-Authored-By: <the model's own line>
    ```

  - **Push** under the standing OK (Phase 2 Q&A 7): `make leaks privacy models-check`, then
    `git push origin phase-2`. The task is closed once CI on the closing commit, or a later one,
    is green.

***

### Task 5: The arm tip, its wedge and the cord clips

> **Built differently** (closed 2026-11-06; commits 2d16404, 3cf3181): the stem's wide slot starts 0.25 mm above its grip band, since sharing that plane with the free bore left 16 stray triangles in the 25 mm STL; a new test, `tests/test_meshes.py`, checks every built STL is watertight; the clips go on from above, loops down, in the tip's notes and the feet's step 9 (Task 5's review, Important 1 and 2).

**Tier:** 2 · **Scenarios:** S28, S14, S27

**Files:**
- Create: `models/rail-arm-tip/rail-arm-tip.sc` (by SolidCraft), its built files (`rail-arm-tip.stl`, `-3-4in.stl`, `-25mm.stl`, `.png`, `.eval.json`, `build.json`, by
  `make models`), `models/rail-arm-tip/model.yml`, `tests/test_rail_arm_tip.py`
- Modify: `website/architecture.qmd` (its nodes turn solid)

**Interfaces:**
- Consumes: Phase 1's `make models`, `models.Model`, `models.sizes`, `models.read_yml` and the
  conftest helpers `params`, `body` and `measured`; the coupon's `step`; the earlier rail parts'
  parameters, where its test checks them against its own. It's built at the placeholder sizes
  (Phase 2 Q&A 9); Task 11 retunes it to Task 10's measurements.
- Produces: the cap on the arm's end, its stem that grips the cord and takes the shade, and three clips; the parameters and bodies its test names.

- [x] **Step 0: Record the base:** `git rev-parse HEAD > .git/TASK_BASE`.
- [x] **Step 1: Write the failing test.**

`tests/test_rail_arm_tip.py`:

```python
"""The arm's tip (S28, S14, S27): a wedged cap, a stem that grips the cord over a short band and
takes the shade on two lugs, and clips under the arm; the cord pressed in everywhere it goes."""

from __future__ import annotations

from pathlib import Path

import pytest

import models
from conftest import body, measured, params

MODELS = Path(__file__).resolve().parent.parent / "models"
TIP = models.Model(MODELS / "rail-arm-tip")
FEET = models.Model(MODELS / "rail-feet")
CARRIER = models.Model(MODELS / "rail-carrier")
COUPON = models.Model(MODELS / "dowel-fit-coupon")
BODIES = ["Arm tip", "Tip wedge", "Cord clip 1", "Cord clip 2", "Cord clip 3"]


def test_the_tip_its_wedge_and_three_clips_are_each_one_closed_body() -> None:
    for name in BODIES:
        assert body(TIP, name)["closed"]


def test_it_is_saved_for_one_inch_and_comes_in_three_sizes() -> None:
    assert params(TIP)["dowel_d"] == pytest.approx(25.4)
    assert set(models.sizes(TIP)) == {"3/4 in", "25 mm"}


def test_the_cap_takes_the_dowel_with_one_of_the_coupons_clearances() -> None:
    p, step = params(TIP), params(COUPON)["step"]
    assert p["bore_d"] == pytest.approx(p["dowel_d"] + p["clearance"])
    assert any(p["clearance"] == pytest.approx(k * step) for k in (1, 2, 3, 4))


def test_the_stem_grips_the_cord_over_a_short_band_pressed_in_from_the_side() -> None:
    p = params(TIP)
    assert p["press_w"] < p["grip_d"] < p["cord_d"] < p["slot_w"] < p["free_d"]
    assert p["cord_d"] - p["press_w"] <= 2.0  # a squeeze, not a fight
    assert 8.0 <= p["grip_l"] <= 12.0
    assert p["mouth_w"] < p["cord_d"]


def test_the_cord_has_room_behind_the_rail_wherever_it_goes() -> None:
    p = params(TIP)
    assert params(FEET)["cord_depth"] >= p["cord_d"] + 1.0
    assert params(FEET)["cord_w"] >= p["cord_d"] + 1.0
    assert params(CARRIER)["channel"] >= p["cord_d"] + 1.0


def test_every_part_prints_from_the_same_bed() -> None:
    lowest = {b["name"]: b["bbox"]["min"][2] for b in measured(TIP)["bodies"]}
    assert set(lowest) == set(BODIES)
    assert all(z == pytest.approx(lowest["Arm tip"]) for z in lowest.values())


@pytest.mark.parametrize("off", [-0.5, 0.0, 0.5])
def test_a_dowel_half_a_millimetre_off_still_seats_the_wedge_inside(off: float) -> None:
    # A dowel off its size gets the clearance the coupon picks for it (S28), and wedge_in follows
    # clearance, so the seat depends on the offset alone; the gap gains clearance / 2.
    p = params(TIP)
    short_of_end = (p["wedge_in"] - p["room_in"] - p["clearance"] / 2 + off) / p["taper"]
    assert 0 < short_of_end < p["bore_depth"] - 10.0


def test_the_wedges_groove_leaves_a_wall_above_it() -> None:
    p = params(TIP)
    deepest = p["dowel_d"] / 2 + p["room_in"] + p["bore_depth"] * p["taper"]
    assert p["cap_d"] / 2 - deepest >= 2.0
```

- [x] **Step 2: Run it; watch it fail.** `make test`. Expected: `FileNotFoundError` for
  `models/rail-arm-tip/rail-arm-tip.eval.json`.
- [x] **Step 3: Build the design.** Write SolidCraft's command script to
  `.git/rail-arm-tip-script.json` (it stays out of the repo: the saved design holds the same feature tree):

```json
{
  "commands": [
    {"command": "parameters.add", "params": {"name": "dowel_d", "expression": "25.4 mm", "comment": "the rail's and the arm's dowel: 1 inch as saved; the page offers 3/4 in and 25 mm"}},
    {"command": "parameters.add", "params": {"name": "clearance", "expression": "0.4 mm", "comment": "added to the dowel for every bore: the coupon's hole that fit"}},
    {"command": "parameters.add", "params": {"name": "bore_d", "expression": "dowel_d + clearance", "comment": "every cup's and socket's bore"}},
    {"command": "parameters.add", "params": {"name": "cap_wall", "expression": "7 mm", "comment": "plastic round the dowel, room above for the wedge's groove"}},
    {"command": "parameters.add", "params": {"name": "cap_d", "expression": "bore_d + 2 * cap_wall", "comment": "the cap's outside"}},
    {"command": "parameters.add", "params": {"name": "cap_l", "expression": "50 mm", "comment": "the cap's length along the arm"}},
    {"command": "parameters.add", "params": {"name": "bore_depth", "expression": "42 mm", "comment": "how far the arm goes into the cap"}},
    {"command": "parameters.add", "params": {"name": "groove_w", "expression": "8 mm", "comment": "the wedge's groove along the top of the bore"}},
    {"command": "parameters.add", "params": {"name": "taper", "expression": "0.04", "comment": "each wedge's and its groove's slope, 1 in 25", "unit": ""}},
    {"command": "parameters.add", "params": {"name": "room_in", "expression": "2 mm", "comment": "the groove's depth above the dowel at the bore's end"}},
    {"command": "parameters.add", "params": {"name": "wedge_l", "expression": "bore_depth + 5 mm", "comment": "the wedge's length"}},
    {"command": "parameters.add", "params": {"name": "wedge_in", "expression": "room_in + clearance / 2 + 15 mm * taper", "comment": "the wedge's thin end: seated 15 mm short of the bore's end on a nominal dowel"}},
    {"command": "parameters.add", "params": {"name": "cord_d", "expression": "6 mm", "comment": "the light's cord: a guess until it's measured"}},
    {"command": "parameters.add", "params": {"name": "free_d", "expression": "cord_d + 0.5 mm", "comment": "the stem's bore above its grip"}},
    {"command": "parameters.add", "params": {"name": "slot_w", "expression": "cord_d + 0.2 mm", "comment": "the slot into the free bore: the cord slides in"}},
    {"command": "parameters.add", "params": {"name": "grip_d", "expression": "cord_d - 0.6 mm", "comment": "the stem's grip: a hole narrower than the cord"}},
    {"command": "parameters.add", "params": {"name": "press_w", "expression": "cord_d - 1.5 mm", "comment": "the slot the cord is pressed through into the grip"}},
    {"command": "parameters.add", "params": {"name": "grip_l", "expression": "10 mm", "comment": "the grip's length, at the stem's foot"}},
    {"command": "parameters.add", "params": {"name": "keel_w", "expression": "cord_d + 6 mm", "comment": "the keel under the cap, round the cord's channel"}},
    {"command": "parameters.add", "params": {"name": "keel_z", "expression": "-(bore_d / 2 + cord_d + 4.5 mm)", "comment": "the keel's underside"}},
    {"command": "parameters.add", "params": {"name": "mouth_w", "expression": "cord_d - 1 mm", "comment": "the keel channel's mouth: the cord snaps in"}},
    {"command": "parameters.add", "params": {"name": "stem_d", "expression": "22 mm", "comment": "the stem down to the light"}},
    {"command": "parameters.add", "params": {"name": "stem_l", "expression": "40 mm", "comment": "the stem's length below the keel"}},
    {"command": "parameters.add", "params": {"name": "stem_x", "expression": "cap_l - stem_d / 2 - 3 mm", "comment": "the stem's axis along the arm"}},
    {"command": "parameters.add", "params": {"name": "foot_z", "expression": "keel_z - stem_l", "comment": "the stem's foot"}},
    {"command": "parameters.add", "params": {"name": "lug_w", "expression": "5 mm", "comment": "each lug the shade turns onto"}},
    {"command": "parameters.add", "params": {"name": "lug_h", "expression": "3 mm", "comment": "how far each lug stands out from the stem"}},
    {"command": "parameters.add", "params": {"name": "lug_t", "expression": "3 mm", "comment": "each lug's height"}},
    {"command": "parameters.add", "params": {"name": "clip_t", "expression": "8 mm", "comment": "a cord clip's length along the arm"}},
    {"command": "solid.cylinder", "params": {"diameter": "cap_d", "height": "cap_l", "base": [0, 0, 0], "axis": "X", "body_name": "Arm tip"}},
    {"command": "solid.box", "params": {"length": "cap_l", "width": "keel_w", "height": "-keel_z", "corner": [0, "-keel_w / 2", "keel_z"], "operation": "join", "targets": ["Arm tip"]}},
    {"command": "solid.cylinder", "params": {"diameter": "stem_d", "height": "stem_l + 2 mm", "base": ["stem_x", 0, "foot_z"], "axis": "Z", "operation": "join", "targets": ["Arm tip"]}},
    {"command": "solid.box", "params": {"length": "lug_w", "width": "stem_d + 2 * lug_h", "height": "lug_t", "corner": ["stem_x - lug_w / 2", "-stem_d / 2 - lug_h", "foot_z"], "operation": "join", "targets": ["Arm tip"]}},
    {"command": "solid.cylinder", "params": {"diameter": "bore_d", "height": "bore_depth + 1 mm", "base": ["-1 mm", 0, 0], "axis": "X", "operation": "cut", "targets": ["Arm tip"]}},
    {"command": "solid.box", "params": {"length": "stem_x + 1 mm", "width": "cord_d + 1 mm", "height": "cord_d + 1 mm", "corner": ["-1 mm", "-(cord_d + 1 mm) / 2", "keel_z + 2 mm"], "operation": "cut", "targets": ["Arm tip"]}},
    {"command": "solid.box", "params": {"length": "stem_x + 1 mm", "width": "mouth_w", "height": "3 mm", "corner": ["-1 mm", "-mouth_w / 2", "keel_z - 0.5 mm"], "operation": "cut", "targets": ["Arm tip"]}},
    {"command": "solid.cylinder", "params": {"diameter": "free_d", "height": "stem_l - grip_l + cord_d", "base": ["stem_x", 0, "foot_z + grip_l"], "axis": "Z", "operation": "cut", "targets": ["Arm tip"]}},
    {"command": "solid.box", "params": {"length": "stem_d / 2 + 1 mm", "width": "slot_w", "height": "stem_l - grip_l + 2 mm", "corner": ["stem_x - stem_d / 2 - 1 mm", "-slot_w / 2", "foot_z + grip_l"], "operation": "cut", "targets": ["Arm tip"]}},
    {"command": "solid.cylinder", "params": {"diameter": "grip_d", "height": "grip_l + 1.5 mm", "base": ["stem_x", 0, "foot_z - 1 mm"], "axis": "Z", "operation": "cut", "targets": ["Arm tip"]}},
    {"command": "solid.box", "params": {"length": "stem_d / 2 + 1 mm", "width": "press_w", "height": "grip_l + 1.5 mm", "corner": ["stem_x - stem_d / 2 - 1 mm", "-press_w / 2", "foot_z - 1 mm"], "operation": "cut", "targets": ["Arm tip"]}},
    {"command": "sketch.create", "params": {"plane": "XZ"}},
    {"command": "sketch.line", "params": {"points": [["-1 mm", "-dowel_d / 2 + 2 mm"], ["bore_depth + 0.5 mm", "-dowel_d / 2 + 2 mm"], ["bore_depth + 0.5 mm", "-dowel_d / 2 - room_in + 0.5 mm * taper"], ["-1 mm", "-dowel_d / 2 - room_in - (bore_depth + 1 mm) * taper"]], "closed": true}},
    {"command": "sketch.finish", "params": {}},
    {"command": "solid.extrude", "params": {"distance": "groove_w", "direction": "symmetric", "operation": "cut", "targets": ["Arm tip"]}},
    {"command": "sketch.create", "params": {"plane": "YZ", "offset": "-40 mm"}},
    {"command": "sketch.line", "params": {"points": [["0 mm", "foot_z"], ["wedge_l", "foot_z"], ["wedge_l", "foot_z + wedge_in + wedge_l * taper"], ["0 mm", "foot_z + wedge_in"]], "closed": true}},
    {"command": "sketch.finish", "params": {}},
    {"command": "solid.extrude", "params": {"distance": "groove_w - 0.4 mm", "operation": "new", "body_name": "Tip wedge"}},
    {"command": "solid.cylinder", "params": {"diameter": "dowel_d + 5 mm", "height": "clip_t", "base": ["80 mm", "-80 mm", "foot_z"], "axis": "Z", "body_name": "Cord clip 1"}},
    {"command": "solid.cylinder", "params": {"diameter": "cord_d + 5 mm", "height": "clip_t", "base": ["80 mm", "-80 mm + -(dowel_d / 2 + cord_d / 2 + 3.5 mm)", "foot_z"], "axis": "Z", "operation": "join", "targets": ["Cord clip 1"]}},
    {"command": "solid.cylinder", "params": {"diameter": "dowel_d + 0.2 mm", "height": "clip_t + 2 mm", "base": ["80 mm", "-80 mm", "foot_z - 1 mm"], "axis": "Z", "operation": "cut", "targets": ["Cord clip 1"]}},
    {"command": "solid.box", "params": {"length": "0.85 * dowel_d", "width": "dowel_d", "height": "clip_t + 2 mm", "corner": ["80 mm - 0.425 * dowel_d", "-80 mm", "foot_z - 1 mm"], "operation": "cut", "targets": ["Cord clip 1"]}},
    {"command": "solid.cylinder", "params": {"diameter": "cord_d + 0.5 mm", "height": "clip_t + 2 mm", "base": ["80 mm", "-80 mm + -(dowel_d / 2 + cord_d / 2 + 3.5 mm)", "foot_z - 1 mm"], "axis": "Z", "operation": "cut", "targets": ["Cord clip 1"]}},
    {"command": "solid.box", "params": {"length": "cord_d - 1 mm", "width": "cord_d", "height": "clip_t + 2 mm", "corner": ["80 mm - (cord_d - 1 mm) / 2", "-80 mm + -(dowel_d / 2 + cord_d / 2 + 3.5 mm) - cord_d", "foot_z - 1 mm"], "operation": "cut", "targets": ["Cord clip 1"]}},
    {"command": "solid.cylinder", "params": {"diameter": "dowel_d + 5 mm", "height": "clip_t", "base": ["120 mm", "-80 mm", "foot_z"], "axis": "Z", "body_name": "Cord clip 2"}},
    {"command": "solid.cylinder", "params": {"diameter": "cord_d + 5 mm", "height": "clip_t", "base": ["120 mm", "-80 mm + -(dowel_d / 2 + cord_d / 2 + 3.5 mm)", "foot_z"], "axis": "Z", "operation": "join", "targets": ["Cord clip 2"]}},
    {"command": "solid.cylinder", "params": {"diameter": "dowel_d + 0.2 mm", "height": "clip_t + 2 mm", "base": ["120 mm", "-80 mm", "foot_z - 1 mm"], "axis": "Z", "operation": "cut", "targets": ["Cord clip 2"]}},
    {"command": "solid.box", "params": {"length": "0.85 * dowel_d", "width": "dowel_d", "height": "clip_t + 2 mm", "corner": ["120 mm - 0.425 * dowel_d", "-80 mm", "foot_z - 1 mm"], "operation": "cut", "targets": ["Cord clip 2"]}},
    {"command": "solid.cylinder", "params": {"diameter": "cord_d + 0.5 mm", "height": "clip_t + 2 mm", "base": ["120 mm", "-80 mm + -(dowel_d / 2 + cord_d / 2 + 3.5 mm)", "foot_z - 1 mm"], "axis": "Z", "operation": "cut", "targets": ["Cord clip 2"]}},
    {"command": "solid.box", "params": {"length": "cord_d - 1 mm", "width": "cord_d", "height": "clip_t + 2 mm", "corner": ["120 mm - (cord_d - 1 mm) / 2", "-80 mm + -(dowel_d / 2 + cord_d / 2 + 3.5 mm) - cord_d", "foot_z - 1 mm"], "operation": "cut", "targets": ["Cord clip 2"]}},
    {"command": "solid.cylinder", "params": {"diameter": "dowel_d + 5 mm", "height": "clip_t", "base": ["160 mm", "-80 mm", "foot_z"], "axis": "Z", "body_name": "Cord clip 3"}},
    {"command": "solid.cylinder", "params": {"diameter": "cord_d + 5 mm", "height": "clip_t", "base": ["160 mm", "-80 mm + -(dowel_d / 2 + cord_d / 2 + 3.5 mm)", "foot_z"], "axis": "Z", "operation": "join", "targets": ["Cord clip 3"]}},
    {"command": "solid.cylinder", "params": {"diameter": "dowel_d + 0.2 mm", "height": "clip_t + 2 mm", "base": ["160 mm", "-80 mm", "foot_z - 1 mm"], "axis": "Z", "operation": "cut", "targets": ["Cord clip 3"]}},
    {"command": "solid.box", "params": {"length": "0.85 * dowel_d", "width": "dowel_d", "height": "clip_t + 2 mm", "corner": ["160 mm - 0.425 * dowel_d", "-80 mm", "foot_z - 1 mm"], "operation": "cut", "targets": ["Cord clip 3"]}},
    {"command": "solid.cylinder", "params": {"diameter": "cord_d + 0.5 mm", "height": "clip_t + 2 mm", "base": ["160 mm", "-80 mm + -(dowel_d / 2 + cord_d / 2 + 3.5 mm)", "foot_z - 1 mm"], "axis": "Z", "operation": "cut", "targets": ["Cord clip 3"]}},
    {"command": "solid.box", "params": {"length": "cord_d - 1 mm", "width": "cord_d", "height": "clip_t + 2 mm", "corner": ["160 mm - (cord_d - 1 mm) / 2", "-80 mm + -(dowel_d / 2 + cord_d / 2 + 3.5 mm) - cord_d", "foot_z - 1 mm"], "operation": "cut", "targets": ["Cord clip 3"]}},
    {"command": "file.save_as", "params": {"path": "models/rail-arm-tip/rail-arm-tip.sc", "format": "json", "cache": false}}
  ]
}
```

  From the repo's root: `mkdir -p models/rail-arm-tip`, then
  `solidcraft-cli run .git/rail-arm-tip-script.json --quiet`. Expected: exit 0, and
  `models/rail-arm-tip/rail-arm-tip.sc` is plain-text JSON.
- [x] **Step 4: Write its page's text.**

`models/rail-arm-tip/model.yml`:

```yaml
title: Rail arm tip
summary: >-
  The cap on the end of the light's arm: a wedge locks it on, its stem grips the light's cord and
  takes the shade; with three clips that hold the cord under the arm.
status: designed
material: PETG, matte (never PLA for this part)
size: 1 in
sizes:
  3/4 in: {dowel_d: 19.05 mm}
  25 mm: {dowel_d: 25 mm}
print:
  Orientation: as saved, the stem's foot on the bed; the wedge and the clips flat
  Layer height: 0.2 mm
  Walls: 5
  Infill: 40% gyroid
  Supports: under the cap, from the bed only; block them from the keel's channel, whose ceiling bridges
notes: |
  The cord is never threaded, since its plug and timer won't go through a hole: it's pressed in
  from the side everywhere it goes.

  - **The wedge:** push the tip onto the arm's end, its stem down, and tap the wedge in along the
    arm's top; pull it out by its thick end.
  - **The stem:** press the cord in through the slot at its back. A 10 mm band at the stem's foot,
    narrower than the cord, grips it and holds the light at the height you set.
  - **The lugs** at the stem's foot take the shade: its notches go past them, and a quarter turn
    holds it.
  - **The keel** under the cap carries the cord from under the arm to the stem; its mouth is
    narrower than the cord, so the cord snaps in.
  - **The clips** snap onto the arm from below, and the cord presses into the loop under each.
  - **The cord's size:** `cord_d` is a 6 mm guess until it's measured; the grip, the slots and
    the keel follow it.
  - **A 3/4-inch arm** sags about three times as much as a 1-inch one: keep it short.
  - **Clearance:** the bore is the dowel plus `clearance`, from the fit-test coupon. The 0.4 mm
    it's saved with is a placeholder until the coupon is printed.

  See *Putting the rail together* on the [wall feet](rail-feet.html) page for the order it all
  goes up in.

  This is a first design, not yet printed or load-tested; its page will say when it has been.
```

  Then `make models`. Expected: `building models/rail-arm-tip (missing …)` and `1 built`. Look at
  `rail-arm-tip.png` against the notes.
- [x] **Step 5: The diagrams.** In `website/architecture.qmd`, delete the line `  class tip planned` ("The rail, part by part") and the lines `  class stem planned`, `  class keel planned` and `  class clips planned` ("The light's cord"): the
  part is built.
- [x] **Step 6: Run the checks; they pass.** `make check`. Expected: every test passes twice,
  every model's build matches its design, the privacy and offsite checks pass, the render lists
  the model's page.
- [x] **Step 7: Commit.** Write the message to `.git/COMMIT_MSG`:

```text
feat(models): 🤖 add the cap on the arm's end, its stem that grips the cord and takes the shade, and three clips

The light hangs inside its shade under the arm's tip (Phase 2 Q&A 3): a cap
wedged onto the dowel's end, a keel under it whose mouth the cord snaps
into, and a stem down whose 10 mm band, narrower than the cord, grips it;
two lugs at the stem's foot take the shade. The cord is pressed in from the
side everywhere, since its plug and timer won't go through a hole. Three
clips snap onto the arm from below and hold the cord under it.
Saved at 1 inch, with STLs for 3/4 inch and 25 mm.

The new test failed first with: FileNotFoundError for
models/rail-arm-tip/rail-arm-tip.eval.json.

Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 5
Co-Authored-By: <the model's own line>
```

  `git add models/rail-arm-tip/rail-arm-tip.sc models/rail-arm-tip/rail-arm-tip.stl models/rail-arm-tip/rail-arm-tip-3-4in.stl models/rail-arm-tip/rail-arm-tip-25mm.stl models/rail-arm-tip/rail-arm-tip.png models/rail-arm-tip/rail-arm-tip.eval.json models/rail-arm-tip/build.json models/rail-arm-tip/model.yml tests/test_rail_arm_tip.py website/architecture.qmd`, then `git commit -F .git/COMMIT_MSG`, then `git log -1 --format='%(trailers)'`
  shows the `Plan:` line.
- [x] **Step 8: Review, look forward, close.** The review looks at the picture and the page's
  viewer, not the `.sc` alone.

  - **Review (Tier 2, one reviewer under both headings, Standards and Spec, per Phase 1's retro;
    fix Critical and Important; at most one re-review),** from `$(cat .git/TASK_BASE)`.
  - **Forward:** Task 7 links its page; Task 8 publishes it; Task 11 retunes it; the look test
    (Task 12) prints it.
  - **Docs:** the diagrams (Step 5); S28 `built`: the four dowel parts are built at all three sizes.
  - **Close,** its own commit: this task's boxes ticked, **Now** set to the next task, any
    Built differently and Ruling lines, deferred findings on the phase-end list, the spec's
    scenario statuses. The message, from `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 5: The arm tip, its wedge and the cord clips

    <what the task built, and why, in a few lines>

    Drift: <filled at the close, or none>
    Rulings: <filled at the close, or none>
    Phase-end: <filled at the close, or none>
    Forward: <filled at the close, or none>
    Tier: 2
    Rounds: <filled at the close>
    Findings: <filled at the close, or none>

    Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 5
    Co-Authored-By: <the model's own line>
    ```

  - **Push** under the standing OK (Phase 2 Q&A 7): `make leaks privacy models-check`, then
    `git push origin phase-2`. The task is closed once CI on the closing commit, or a later one,
    is green.

***

### Task 6: The shade

> **Built differently** (closed 2026-11-06; commit b706bab): the six vents go straight down through the shade's flat top, placed by a new parameter, `vent_r`, with a test holding them clear of the stem's notches and the wall. The listing's radial vents through the cone's wall left 8 edges shared by three to six slivers in the STL, at every quality SolidCraft exports, where one vent met the sloped wall: its tessellator, found by `tests/test_meshes.py` and traced by systematic debugging. Vertical vents meet only flat faces, and the STL is watertight at every quality.

**Tier:** 2 · **Scenarios:** S30, S11

**Files:**
- Create: `models/rail-shade/rail-shade.sc` (by SolidCraft), its built files (`rail-shade.stl`, `.png`, `.eval.json`, `build.json`, by
  `make models`), `models/rail-shade/model.yml`, `tests/test_rail_shade.py`
- Modify: `website/architecture.qmd` (its nodes turn solid)

**Interfaces:**
- Consumes: Phase 1's `make models`, `models.Model`, `models.sizes`, `models.read_yml` and the
  conftest helpers `params`, `body` and `measured`; the coupon's `step`; the earlier rail parts'
  parameters, where its test checks them against its own. It's built at the placeholder sizes
  (Phase 2 Q&A 9); Task 11 retunes it to Task 10's measurements.
- Produces: the PETG shade the lamp hangs inside; the parameters and bodies its test names.

- [x] **Step 0: Record the base:** `git rev-parse HEAD > .git/TASK_BASE`.
- [x] **Step 1: Write the failing test.**

`tests/test_rail_shade.py`:

```python
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
```

- [x] **Step 2: Run it; watch it fail.** `make test`. Expected: `FileNotFoundError` for
  `models/rail-shade/rail-shade.eval.json`.
- [x] **Step 3: Build the design.** Write SolidCraft's command script to
  `.git/rail-shade-script.json` (it stays out of the repo: the saved design holds the same feature tree):

```json
{
  "commands": [
    {"command": "parameters.add", "params": {"name": "socket_d", "expression": "45 mm", "comment": "the socket's body: a guess until it's measured"}},
    {"command": "parameters.add", "params": {"name": "socket_l", "expression": "60 mm", "comment": "the socket's length, its top to where the bulb starts"}},
    {"command": "parameters.add", "params": {"name": "bulb_d", "expression": "121 mm", "comment": "the bulb's widest: a guess until it's measured"}},
    {"command": "parameters.add", "params": {"name": "bulb_l", "expression": "100 mm", "comment": "the bulb's length, from the socket to its face"}},
    {"command": "parameters.add", "params": {"name": "gap", "expression": "12 mm", "comment": "air round the lamp: at least 10 mm"}},
    {"command": "parameters.add", "params": {"name": "shade_t", "expression": "2.4 mm", "comment": "the shade's wall"}},
    {"command": "parameters.add", "params": {"name": "top_t", "expression": "3 mm", "comment": "the shade's top, which rests on the stem's lugs"}},
    {"command": "parameters.add", "params": {"name": "drop", "expression": "8 mm", "comment": "the socket's top below the shade's top: the lugs, then air"}},
    {"command": "parameters.add", "params": {"name": "rim", "expression": "5 mm", "comment": "the shade's rim below the bulb's face"}},
    {"command": "parameters.add", "params": {"name": "vent_d", "expression": "8 mm", "comment": "each vent round the shade's top"}},
    {"command": "parameters.add", "params": {"name": "stem_d", "expression": "22 mm", "comment": "the tip's stem (rail-arm-tip)"}},
    {"command": "parameters.add", "params": {"name": "lug_w", "expression": "5 mm", "comment": "each lug on the stem (rail-arm-tip)"}},
    {"command": "parameters.add", "params": {"name": "lug_h", "expression": "3 mm", "comment": "how far each lug stands out (rail-arm-tip)"}},
    {"command": "parameters.add", "params": {"name": "fit", "expression": "0.4 mm", "comment": "round the stem and through the notches"}},
    {"command": "parameters.add", "params": {"name": "r_top", "expression": "socket_d / 2 + gap", "comment": "the shade's inside at its top"}},
    {"command": "parameters.add", "params": {"name": "r_bulb", "expression": "bulb_d / 2 + gap", "comment": "the shade's inside round the bulb"}},
    {"command": "parameters.add", "params": {"name": "shoulder_z", "expression": "top_t + drop + socket_l", "comment": "where the cone meets the cylinder: the bulb's start"}},
    {"command": "parameters.add", "params": {"name": "height", "expression": "shoulder_z + bulb_l + rim", "comment": "the shade's height"}},
    {"command": "solid.cylinder", "params": {"diameter": "2 * (r_top + shade_t)", "height": "top_t", "base": [0, 0, 0], "axis": "Z", "body_name": "Shade"}},
    {"command": "solid.cone", "params": {"diameter": "2 * (r_top + shade_t)", "top_diameter": "2 * (r_bulb + shade_t)", "height": "shoulder_z - top_t", "base": [0, 0, "top_t"], "axis": "Z", "operation": "join", "targets": ["Shade"]}},
    {"command": "solid.cylinder", "params": {"diameter": "2 * (r_bulb + shade_t)", "height": "height - shoulder_z", "base": [0, 0, "shoulder_z"], "axis": "Z", "operation": "join", "targets": ["Shade"]}},
    {"command": "solid.cone", "params": {"diameter": "2 * r_top", "top_diameter": "2 * r_bulb", "height": "shoulder_z - top_t", "base": [0, 0, "top_t"], "axis": "Z", "operation": "cut", "targets": ["Shade"]}},
    {"command": "solid.cylinder", "params": {"diameter": "2 * r_bulb", "height": "height - shoulder_z + 1 mm", "base": [0, 0, "shoulder_z"], "axis": "Z", "operation": "cut", "targets": ["Shade"]}},
    {"command": "solid.cylinder", "params": {"diameter": "stem_d + fit", "height": "top_t + 2 mm", "base": [0, 0, "-1 mm"], "axis": "Z", "operation": "cut", "targets": ["Shade"]}},
    {"command": "solid.box", "params": {"length": "lug_w + fit", "width": "stem_d + 2 * (lug_h + fit)", "height": "top_t + 2 mm", "corner": ["-(lug_w + fit) / 2", "-stem_d / 2 - lug_h - fit", "-1 mm"], "operation": "cut", "targets": ["Shade"]}},
    {"command": "solid.cylinder", "params": {"diameter": "vent_d", "height": "r_bulb + shade_t + 5 mm", "base": [0, 0, "top_t + vent_d / 2 + 3 mm"], "axis": [0.866025, 0.5, 0], "operation": "cut", "targets": ["Shade"]}},
    {"command": "solid.cylinder", "params": {"diameter": "vent_d", "height": "r_bulb + shade_t + 5 mm", "base": [0, 0, "top_t + vent_d / 2 + 3 mm"], "axis": [0.0, 1.0, 0], "operation": "cut", "targets": ["Shade"]}},
    {"command": "solid.cylinder", "params": {"diameter": "vent_d", "height": "r_bulb + shade_t + 5 mm", "base": [0, 0, "top_t + vent_d / 2 + 3 mm"], "axis": [-0.866025, 0.5, 0], "operation": "cut", "targets": ["Shade"]}},
    {"command": "solid.cylinder", "params": {"diameter": "vent_d", "height": "r_bulb + shade_t + 5 mm", "base": [0, 0, "top_t + vent_d / 2 + 3 mm"], "axis": [-0.866025, -0.5, 0], "operation": "cut", "targets": ["Shade"]}},
    {"command": "solid.cylinder", "params": {"diameter": "vent_d", "height": "r_bulb + shade_t + 5 mm", "base": [0, 0, "top_t + vent_d / 2 + 3 mm"], "axis": [-0.0, -1.0, 0], "operation": "cut", "targets": ["Shade"]}},
    {"command": "solid.cylinder", "params": {"diameter": "vent_d", "height": "r_bulb + shade_t + 5 mm", "base": [0, 0, "top_t + vent_d / 2 + 3 mm"], "axis": [0.866025, -0.5, 0], "operation": "cut", "targets": ["Shade"]}},
    {"command": "file.save_as", "params": {"path": "models/rail-shade/rail-shade.sc", "format": "json", "cache": false}}
  ]
}
```

  From the repo's root: `mkdir -p models/rail-shade`, then
  `solidcraft-cli run .git/rail-shade-script.json --quiet`. Expected: exit 0, and
  `models/rail-shade/rail-shade.sc` is plain-text JSON.
- [x] **Step 4: Write its page's text.**

`models/rail-shade/model.yml`:

```yaml
title: Rail light shade
summary: >-
  A shade for a grow bulb on a pendant socket: it turns onto the arm tip's stem, and the lamp hangs
  inside it, with air all round and vents round its top.
status: designed
material: PETG, matte (never PLA, since it sits by a warm bulb)
size: for a bulb up to 121 mm across
print:
  Orientation: as saved, upside down, its top on the bed
  Layer height: 0.2 mm
  Walls: 3
  Infill: 15% (only the top is solid)
  Supports: none
notes: |
  The light hangs inside the shade on its own cord, gripped in the arm tip's stem. Slide the shade
  up over the bulb and the socket, its top round the stem and its two notches past the stem's
  lugs, then turn it a quarter turn: it rests on the lugs. A cone round the socket widens to a
  cylinder round the bulb, so the shade stays at least 10 mm from the lamp everywhere, and six
  vents round its top let the heat out.

  - **Its size follows the lamp:** `socket_d`, `socket_l`, `bulb_d` and `bulb_l` are guesses
    until the Barrina is measured. Set them to your own lamp's, and the shade follows.
  - **Heat:** a 25 W bulb is more than the 9 or 10 W most printed shades are made for, so this one
    is PETG, and its gap is a parameter.

  See *Putting the rail together* on the [wall feet](rail-feet.html) page for the order it all
  goes up in.

  This is a first design, not yet printed or tested with the light on; its page will say when it
  has been.
```

  Then `make models`. Expected: `building models/rail-shade (missing …)` and `1 built`. Look at
  `rail-shade.png` against the notes.
- [x] **Step 5: The diagrams.** In `website/architecture.qmd`, delete the line `  class shade planned` ("The rail, part by part"): the
  part is built.
- [x] **Step 6: Run the checks; they pass.** `make check`. Expected: every test passes twice,
  every model's build matches its design, the privacy and offsite checks pass, the render lists
  the model's page.
- [x] **Step 7: Commit.** Write the message to `.git/COMMIT_MSG`:

```text
feat(models): 🤖 add the PETG shade the lamp hangs inside

A shade like LoftedGoods' light, for a 25 W bulb (Phase 2 Q&A 3): it turns
onto the tip's stem by two notches past its lugs, and the lamp hangs inside
it on its gripped cord. A cone round the socket widens to a cylinder round
the bulb, so it stays at least 10 mm from the lamp everywhere; six vents
round its top let the heat out. PETG, printed upside down with no supports;
its size follows the lamp's parameters.
It has no dowel, so one STL.

The new test failed first with: FileNotFoundError for
models/rail-shade/rail-shade.eval.json.

Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 6
Co-Authored-By: <the model's own line>
```

  `git add models/rail-shade/rail-shade.sc models/rail-shade/rail-shade.stl models/rail-shade/rail-shade.png models/rail-shade/rail-shade.eval.json models/rail-shade/build.json models/rail-shade/model.yml tests/test_rail_shade.py website/architecture.qmd`, then `git commit -F .git/COMMIT_MSG`, then `git log -1 --format='%(trailers)'`
  shows the `Plan:` line.
- [x] **Step 8: Review, look forward, close.** The review looks at the picture and the page's
  viewer, not the `.sc` alone.

  - **Review (Tier 2, one reviewer under both headings, Standards and Spec, per Phase 1's retro;
    fix Critical and Important; at most one re-review),** from `$(cat .git/TASK_BASE)`.
  - **Forward:** Task 7 links its page; Task 8 publishes it; Task 11 retunes it; the look test
    (Task 12) prints it.
  - **Docs:** the diagrams (Step 5); S30 stays `planned` until the load test.
  - **Close,** its own commit: this task's boxes ticked, **Now** set to the next task, any
    Built differently and Ruling lines, deferred findings on the phase-end list, the spec's
    scenario statuses. The message, from `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 6: The shade

    <what the task built, and why, in a few lines>

    Drift: <filled at the close, or none>
    Rulings: <filled at the close, or none>
    Phase-end: <filled at the close, or none>
    Forward: <filled at the close, or none>
    Tier: 2
    Rounds: <filled at the close>
    Findings: <filled at the close, or none>

    Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 6
    Co-Authored-By: <the model's own line>
    ```

  - **Push** under the standing OK (Phase 2 Q&A 7): `make leaks privacy models-check`, then
    `git push origin phase-2`. The task is closed once CI on the closing commit, or a later one,
    is green.

***

### Task 7: Mark Phase 1's parts superseded

> **Built differently** (closed 2026-11-06; commits 6e5388d, 22a3f99): the README's model example lists the fourth status too, and the overview's edge to the rail's parts is solid (Task 7's review).

**Ruling:** the controller built this task itself, without an implementer subagent: a four-file patch the plan holds whole. Costs if wrong: none the review didn't cover.

**Tier:** 2 · **Scenarios:** S12, S18 (superseded), S28

Phase 1's wall block and cord clamp stay in the repo, marked superseded, their pages pointing at
the rail's parts (Phase 2 Q&A 4). The gallery takes a fourth status for it.

**Files:**
- Modify: `scripts/gallery.py`, `tests/test_gallery.py`, `models/sconce-wall-block/model.yml`,
  `models/sconce-cord-clamp/model.yml`, `website/_overview.qmd`

**Interfaces:**
- Consumes: Task 1's `gallery.py`; Tasks 2 to 6's pages, which the notes link.
- Produces: `gallery.STATUSES` with `superseded`.

- [x] **Step 0: Record the base:** `git rev-parse HEAD > .git/TASK_BASE`.
- [x] **Step 1: The test, the code and the notes, as one patch.** Write it to `.git/task8.patch`:

```diff
diff --git a/models/sconce-cord-clamp/model.yml b/models/sconce-cord-clamp/model.yml
index e2b15fb..9cb5429 100644
--- a/models/sconce-cord-clamp/model.yml
+++ b/models/sconce-cord-clamp/model.yml
@@ -2,7 +2,7 @@ title: Sconce cord clamp
 summary: >-
   Clamps anywhere along a dowel and holds a pendant light's cord, so the light hangs straight
   below the arm at the height you set.
-status: designed
+status: superseded
 material: PETG, matte
 size: 1 in
 sizes:
@@ -15,6 +15,11 @@ print:
   Infill: 30%
   Supports: under the ring, from the bed only
 notes: |
+  **Superseded** by the grow-light rail, before anything was printed (Phase 2 Q&A 1 to 4): the
+  [wall feet](rail-feet.html), [carrier](rail-carrier.html), [arm socket](rail-arm-socket.html),
+  [arm tip](rail-arm-tip.html) and [shade](rail-shade.html). Kept for anyone who wants an arm
+  straight out of the wall.
+
   Slide the clamp onto the dowel, ears to the side you see least, set it where the light should
   hang, and close the split with an M4 × 30 mm bolt and nut through the ears. Its `clearance`,
   0.2 mm, is a slide fit the bolt closes, unlike the wall block's socket, whose clearance comes
diff --git a/models/sconce-wall-block/model.yml b/models/sconce-wall-block/model.yml
index 49967ae..23d3c0f 100644
--- a/models/sconce-wall-block/model.yml
+++ b/models/sconce-wall-block/model.yml
@@ -2,7 +2,7 @@ title: Sconce wall block
 summary: >-
   The wall end of a grow-light sconce: a plate for two hidden screws and a deep socket that holds
   a dowel straight out from the wall, bolted through.
-status: designed
+status: superseded
 material: PETG, matte (never PLA for this part)
 size: 1 in
 sizes:
@@ -15,6 +15,11 @@ print:
   Infill: 40% gyroid
   Supports: under the boss, along its length, from the bed only
 notes: |
+  **Superseded** by the grow-light rail, before anything was printed (Phase 2 Q&A 1 to 4): the
+  [wall feet](rail-feet.html), [carrier](rail-carrier.html), [arm socket](rail-arm-socket.html),
+  [arm tip](rail-arm-tip.html) and [shade](rail-shade.html). Kept for anyone who wants an arm
+  straight out of the wall.
+
   The arm is a straight cantilever: a dowel up to 20 inches long, with the light hanging near its
   end. The socket is 54 mm deep, more than the 51 mm (2 inches) the joint needs to carry the arm's
   bending moment: about 5 N·m with a 1 kg light at 20 inches on a 1-inch dowel.
diff --git a/scripts/gallery.py b/scripts/gallery.py
index edc8399..cf0c160 100644
--- a/scripts/gallery.py
+++ b/scripts/gallery.py
@@ -26,7 +26,7 @@ LICENCE = (
     "[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/): print it, change it and "
     f"share it, crediting chendaniely and linking to <{REPO_URL}>; don't sell it or prints of it."
 )
-STATUSES = ("designed", "printed", "in use")
+STATUSES = ("designed", "printed", "in use", "superseded")
 FREE_TEXT = ("title", "summary", "status", "material", "size", "notes")  # escaped, as sitedocs
 DENSITY_G_CM3 = {"PLA": 1.24, "PETG": 1.27}
 
diff --git a/tests/test_gallery.py b/tests/test_gallery.py
index 8235bf9..56e9642 100644
--- a/tests/test_gallery.py
+++ b/tests/test_gallery.py
@@ -193,6 +193,11 @@ def test_a_bar_in_a_print_setting_stays_inside_its_cell(repo: Path) -> None:
     assert "| Infill | 20% \\| gyroid |" in page(repo)
 
 
+def test_a_superseded_model_keeps_its_page_and_says_so(repo: Path) -> None:
+    add_model(repo, meta=META.replace("status: printed", "status: superseded"))
+    assert "**Status:** superseded." in page(repo)
+
+
 @pytest.mark.parametrize(
     ("meta", "message"),
     [
```

- [x] **Step 2: Run the test; watch it fail.** `git apply --include='tests/*' .git/task8.patch`,
  then `make test`. Expected: `test_a_superseded_model_keeps_its_page_and_says_so` fails, the
  gallery naming `'status' must be one of designed, printed, in use`.
- [x] **Step 3: The code and the notes.** `git apply --exclude='tests/*' .git/task8.patch`.
- [x] **Step 4: The overview diagram.** In `website/_overview.qmd`, delete the line
  `  class railparts planned`: the rail's five parts are built.
- [x] **Step 5: Run the checks; they pass.** `make check`. Expected: every test passes twice;
  the two parts' builds still match (only their pages' text changed); the render resolves the
  notes' links to the five rail pages.
- [x] **Step 6: Commit.** Write the message to `.git/COMMIT_MSG`:

```text
feat(gallery): 🤖 mark Phase 1's wall block and cord clamp superseded

Dan's changes, brought forward before anything was printed, replaced the
sconce's two parts with the rail's five (Phase 2 Q&A 1 to 4); the two stay,
for anyone who wants an arm straight out of the wall (Q&A 4). The gallery
takes a fourth status, superseded, and each part's notes point at the rail's
parts. The overview diagram shows the rail's parts built.

The new test failed first with: <the failing line from Step 2>.

Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 7
Co-Authored-By: <the model's own line>
```

  `git add scripts/gallery.py tests/test_gallery.py models/sconce-wall-block/model.yml models/sconce-cord-clamp/model.yml website/_overview.qmd`,
  then `git commit -F .git/COMMIT_MSG`, then `git log -1 --format='%(trailers)'` shows the
  `Plan:` line.
- [x] **Step 7: Review, look forward, close.**

  - **Review (Tier 2, one reviewer under both headings, Standards and Spec; fix Critical and
    Important; at most one re-review),** from `$(cat .git/TASK_BASE)`.
  - **Forward:** none.
  - **Docs:** S12 and S18 stay `superseded`; the overview diagram (Step 4).
  - **Close,** its own commit: this task's boxes ticked, **Now** set to the next task, any
    Built differently and Ruling lines, deferred findings on the phase-end list, the spec's
    scenario statuses. The message, from `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 7: Mark Phase 1's parts superseded

    <what the task built, and why, in a few lines>

    Drift: <filled at the close, or none>
    Rulings: <filled at the close, or none>
    Phase-end: <filled at the close, or none>
    Forward: <filled at the close, or none>
    Tier: 2
    Rounds: <filled at the close>
    Findings: <filled at the close, or none>

    Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 7
    Co-Authored-By: <the model's own line>
    ```

  - **Push** under the standing OK (Phase 2 Q&A 7): `make leaks privacy models-check`, then
    `git push origin phase-2`. The task is closed once CI on the closing commit, or a later one,
    is green.

***

### Task 8: Publish the parts: a mid-phase merge to `main`

**Tier:** none: a merge, gated by Dan's look at each file no scan can read (`AGENTS.md`, *Stops*;
Phase 2 Q&A 7), reviewed as Tier 3 · **Scenarios:** S07, S08, S19

Dan asked to see the rail's parts in the live gallery as soon as they're built, with the guessed
sizes, and to retune them after measuring (Phase 2 Q&A 9). Their pages already say which sizes are
placeholders. `phase-2` carries on after the merge.

- [x] **0. Record the base:** `git rev-parse HEAD > .git/TASK_BASE`.
- [x] **1. The files no scan can read, named to Dan:** every STL and PNG the merge adds, listed
  with `git diff --numstat origin/main..phase-2 | awk '$1 == "-" { print $3 }'` (eighteen: four
  for each dowel part, two for the shade). Show him each picture, and the local render's 3D views
  (`make docs`, then serve `website/_site`); ask, naming each file, whether he OKs it going out.
  His answer goes on the Phase 2 Q&A page, committed as `docs(plan): 🤖 Phase 2 Q&A <N>: <what>`
  with this plan's `Plan:` line, and pushed.
- [x] **2. The PR.** Its title, in `.git/PR_TITLE`:
  `chore(repo): 🤖 merge the rail's five parts, at placeholder sizes`. Its body, in
  `.git/PR_BODY.md`: what it carries (Tasks 1 to 7), that the sizes are placeholders until Task 11,
  and a section *Files no scan can read*, each by name, saying Dan OKed it (the Q&A answer), then
  the Claude Code line and the trailer paragraph (`Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 8` and
  `Co-Authored-By:`). Scan both: `cat .git/PR_TITLE .git/PR_BODY.md | gitleaks stdin --redact
  --no-banner`, then `gh pr create --base main --head phase-2 --title "$(cat .git/PR_TITLE)"
  --body-file .git/PR_BODY.md`.
- [x] **3. The merge,** once every check on the PR's head is green:
  `gh pr merge <N> --merge --match-head-commit "$(git rev-parse phase-2)"`, never `--admin`,
  squash, rebase or `--delete-branch`.
- [x] **4. After the merge:** CI on `main` deploys; each rail page on
  <https://chendaniely.github.io/3d-models/> answers, its viewer loads in a browser, and the live
  site loads nothing from another host (Task 1).
- [x] **5. Close.**

  - **Review (Tier 3: a self-review under Standards and Spec, plus the mechanical checks; and the
    PR's text read for a place, an address, a person or a description of the home),** from
    `$(cat .git/TASK_BASE)`.
  - **Forward:** Task 11 retunes the parts and publishes them again.
  - **Docs:** none; the spec's status line names the merge.
  - **Close,** its own commit: this task's boxes ticked, **Now** set to the next task, any
    Built differently and Ruling lines, deferred findings on the phase-end list, the spec's
    scenario statuses. The message, from `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 8: Publish the parts: a mid-phase merge to `main`

    <what the task built, and why, in a few lines>

    Drift: <filled at the close, or none>
    Rulings: <filled at the close, or none>
    Phase-end: <filled at the close, or none>
    Forward: <filled at the close, or none>
    Tier: 3
    Rounds: <filled at the close>
    Findings: <filled at the close, or none>

    Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 8
    Co-Authored-By: <the model's own line>
    ```

  - **Push** under the standing OK (Phase 2 Q&A 7): `make leaks privacy models-check`, then
    `git push origin phase-2`. The task is closed once CI on the closing commit, or a later one,
    is green.

***

### Task 9: The store gauges: a taper card and a hole grid

> **Built differently** (closed 2026-11-06; commits f51e6df, b712432, 3bbad80): the card's windows are 11 to 36 mm and 30 to 55 mm and taper 0.11 mm per mm, not the listing's 11 to 33, 31 to 53 and 0.1, and its scales run only where a dowel can reach (`LO` and `HI` in the generator): a round dowel reaches about half its diameter past where it touches the sides, so the listing's card couldn't read 2 inches, 1 1/4 or 31.4 to 32.6 mm (Task 9's review, Important). The card is 251 by 161 mm (149 since Q&A 12, Task 10's step 0a), its scales 12 to 34 and 32 to 52 mm, its ticks 4.5 mm apart. Its test reads each engraved size from the saved design and checks it sits where a dowel of that size stops and can reach (`engraved` in `tests/conftest.py`), where the listing checked `cos_a` alone (Important). The grid's `band` is 10 mm (8 since Q&A 12) and each number sits 1.2 mm under its own hole, clear of the row below, with a test; its page says the numbers are rounded to 0.1 mm and what a dowel through no hole means; `parameter_names` takes only named entries of a list, with a test (Minor).

**Tier:** 2 · **Scenarios:** S33, S34

Dan asked for a gauge to carry to the store, to read the dowels from 1/2 to 2 inches before he
buys them, printed on his Bambu P2S (a plate 256 mm square), and chose two (Phase 2 Q&A 11): a
taper card that reads any dowel's real diameter, and a hole grid of each size in 0.2 mm steps.
Both are PLA, printed flat, their words and ticks engraved 0.6 mm into the top in SolidCraft's
built-in font (its regular face: it has no bold). The grid is one tile, built for every 1/8 inch
from 1/2 to 2 inches through `sizes`, its size's name a text parameter and each hole's diameter a
`number()` of its own parameter, so each size's tile is labelled right. The question offered the
grid's holes marked by dots; each is engraved with its own diameter instead, which says more.
Neither gauge sets the parts' fit: the coupon does, on the finished dowel (decided without Dan, 3).
The controller builds this task itself from the listings below, as in Task 7, since they were
run whole in a scratch clone.

**Files:**
- Create: `models/dowel-taper-card/` and `models/dowel-hole-grid/`: each `.sc` (by SolidCraft,
  from the scripts below), `model.yml`, and its built files by `make models` (the card's `.stl`,
  `.png`, `.eval.json` and `build.json`; the grid's the same, and twelve sized STLs, from
  `dowel-hole-grid-1-2in.stl` to `dowel-hole-grid-2in.stl`); `tests/test_dowel_taper_card.py`,
  `tests/test_dowel_hole_grid.py`
- Modify: `scripts/models.py` and `tests/test_models.py` (a size may change a text parameter: the
  grid's label), `website/_overview.qmd` (the gauges' node turns solid), `README.md` (its status)

**Interfaces:**
- Consumes: Phase 1's `make models`, `models.Model`, `models.sizes`, `models.read_yml` and the
  conftest helpers `params` and `body`.
- Produces: the two gauges' pages and STLs; Task 10's step 7 reads the dowels with them.
  `models.parameter_names(model) -> set[str]`: the numbers eval.json lists and the texts only the
  design lists (SolidCraft's eval leaves text parameters out, so `make models` refused a size
  changing one).

- [x] **Step 0: Record the base:** `git rev-parse HEAD > .git/TASK_BASE`.
- [x] **Step 1: Write the failing tests.**

`tests/test_dowel_taper_card.py`:

```python
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
```

`tests/test_dowel_hole_grid.py`:

```python
"""The hole grid (S34): a tile for each dowel size from 1/2 to 2 inches, its six holes from
0.6 mm under the size to 0.4 mm over, each engraved with its own diameter."""

from __future__ import annotations

import math
from fractions import Fraction
from pathlib import Path

import pytest

import models
from conftest import body, params

GRID = models.Model(Path(__file__).resolve().parent.parent / "models" / "dowel-hole-grid")
PLATE_MM = 256.0  # a Bambu P2S prints up to 256 mm square
OFFSETS = [-0.6, -0.4, -0.2, 0.0, 0.2, 0.4]


def label(size: Fraction) -> str:
    """The name engraved on a tile: '1/2 in', '1 in', '1 1/8 in'."""
    whole, part = divmod(size, 1)
    words = [str(whole)] if whole else []
    if part:
        words.append(f"{part.numerator}/{part.denominator}")
    return " ".join(words) + " in"


def listed_as(size: Fraction) -> str:
    """Its name in model.yml's sizes, a mixed number hyphenated so its file name reads well:
    '1-1/8 in' gives dowel-hole-grid-1-1-8in.stl."""
    return label(size).replace(" ", "-", 1) if size > 1 and size.denominator > 1 else label(size)


def test_it_is_saved_for_a_one_inch_dowel_in_steps_of_a_fifth_of_a_millimetre() -> None:
    p = params(GRID)
    assert p["dowel_d"] == pytest.approx(25.4)
    assert p["step"] == pytest.approx(0.2)


def test_its_six_holes_run_from_point_six_under_the_size_to_point_four_over() -> None:
    p = params(GRID)
    assert [p[f"h{i}"] - p["dowel_d"] for i in range(1, 7)] == pytest.approx(OFFSETS)


def test_it_comes_in_every_eighth_of_an_inch_from_a_half_to_two() -> None:
    eighths = [Fraction(k, 8) for k in range(4, 17) if k != 8]  # 1 inch is the saved size
    listed = models.sizes(GRID)
    assert list(listed) == [listed_as(size) for size in eighths]
    for size in eighths:
        changes = listed[listed_as(size)]
        assert float(changes["dowel_d"].removesuffix(" mm")) == pytest.approx(float(size) * 25.4)
        assert changes["label"] == label(size)


def test_even_the_two_inch_tile_fits_the_printers_plate() -> None:
    p = params(GRID)
    assert p["pitch"] == pytest.approx(p["h6"] + p["wall"])
    assert p["tile_l"] == pytest.approx(3 * p["pitch"] + p["wall"])
    assert p["tile_w"] == pytest.approx(2 * p["band"] + 2 * p["pitch"] + p["head"])
    pitch = 50.8 + OFFSETS[-1] + p["wall"]
    assert 3 * pitch + p["wall"] <= PLATE_MM
    assert 2 * p["band"] + 2 * pitch + p["head"] <= PLATE_MM


def test_it_is_one_closed_tile_with_its_holes_and_a_ring_hole() -> None:
    p, tile = params(GRID), body(GRID, "Tile")
    assert tile["closed"]
    low, high = tile["bbox"]["min"], tile["bbox"]["max"]
    assert [high[i] - low[i] for i in range(3)] == pytest.approx(
        [p["tile_l"], p["tile_w"], p["thick"]]
    )
    holes = sum(math.pi * (p[f"h{i}"] / 2) ** 2 for i in range(1, 7))
    ring = math.pi * (p["ring_d"] / 2) ** 2
    solid = (p["tile_l"] * p["tile_w"] - holes - ring) * p["thick"]
    engraved = solid - tile["volume_mm3"]
    assert 0 < engraved < 0.05 * p["tile_l"] * p["tile_w"] * p["engrave"]


def test_its_page_says_how_to_read_each_hole_and_how_to_print_it() -> None:
    meta = models.read_yml(GRID)
    assert meta["material"].startswith("PLA")
    for at, offset, hole in [("top left", "-0.6", "24.8"), ("bottom left", "0", "25.4"),
                             ("bottom right", "+0.4", "25.8")]:  # fmt: skip
        assert f"| {at} | {offset} mm | {hole} mm |" in meta["notes"]
    assert meta["print"]["Orientation"].startswith("flat")
```

In `tests/test_models.py`, before the parametrized test of clashing sizes:

```python
def test_build_takes_a_size_changing_a_text_parameter_only_the_design_lists(
    repo: Path, fake_cli: Path
) -> None:
    # solidcraft-cli's eval lists number parameters alone; a text one is in the design's text_params
    design = add_design(
        repo, "tile", '{"params": ["dowel_d"], "text_params": [{"name": "label", "text": "1 in"}]}'
    )
    (design.parent / "model.yml").write_text(
        "sizes:\n  1/2 in: {dowel_d: 12.7 mm, label: 1/2 in}\n", encoding="utf-8"
    )
    assert models.main(["build"], root=repo) == 0
    assert (design.parent / "tile-1-2in.stl").exists()
    assert models.main(["check"], root=repo) == 0
```

- [x] **Step 2: Run them; watch them fail.** `uv run --frozen pytest -q
  tests/test_dowel_taper_card.py tests/test_dowel_hole_grid.py tests/test_models.py`. Expected:
  `13 failed, 34 passed`: nine with `FileNotFoundError` for a gauge's `.eval.json`, two with
  `KeyError: 'material'`, one listing no sizes, and the text parameter's with `assert 1 == 0`, its
  stderr "size '1/2 in' changes 'label', which the design has no parameter named".
- [x] **Step 3a: The text parameters.** In `scripts/models.py`, `unknown_parameter` takes its
  names from a new `parameter_names`; replace its head, down to its `for` line, with:

```python
def parameter_names(model: Model) -> set[str]:
    """A design's parameters: the numbers its eval.json lists, and the texts (a label it
    engraves) that only the design itself lists, under text_params."""
    measured = json.loads(model.built("eval.json").read_text(encoding="utf-8"))
    names = {param["name"] for param in measured.get("params", [])}
    try:
        design = json.loads(model.design.read_text(encoding="utf-8"))
    except ValueError:
        return names
    texts = design.get("text_params", []) if isinstance(design, dict) else []
    return names | {param["name"] for param in texts}


def unknown_parameter(model: Model, wanted: dict[str, dict[str, str]]) -> str | None:
    """The first size that changes a parameter the design doesn't have, or None. Without this,
    solidcraft-cli builds the base geometry under the size's name and exits 0."""
    names = parameter_names(model)
    for size, changes in wanted.items():
```

  Then `uv run --frozen pytest -q tests/test_models.py` passes.
- [x] **Step 3b: Build the designs.** Write this script to `.git/gauges.py`, run
  `uv run --no-project python .git/gauges.py .`, then `solidcraft-cli run
  .git/dowel-taper-card-script.json --quiet` (about two minutes: the engraving) and
  `solidcraft-cli run .git/dowel-hole-grid-script.json --quiet`; each saves its `.sc`.

```python
# /// script
# requires-python = ">=3.12"
# ///
"""The store gauges' design scripts (Phase 2, Task 9): writes .git/<slug>-script.json in the repo
root given as argv[1], for the taper card and the hole grid; each saves models/<slug>/<slug>.sc.
Millimetres; each gauge lies flat, its top face at z = thick, its words and ticks engraved there.
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


def engrave(target, items, top="thick"):
    return [
        {"command": "sketch.create", "params": {"plane": "XY", "offset": top}},
        *items,
        {"command": "sketch.finish", "params": {}},
        {
            "command": "solid.extrude",
            "params": {
                "distance": "engrave",
                "direction": "negative",
                "operation": "cut",
                "targets": [target],
            },
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

RATE, END, RIGHT, BAND, MID = 0.1, 8.0, 16.0, 20.0, 30.0
W1, W2 = (11.0, 33.0), (31.0, 53.0)
COS_A = 1 / math.sqrt(1 + (RATE / 2) ** 2)
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


def scale(axis, w, side_mm, numbers_to):
    """Ticks every 0.5 mm with numbers on one edge, every 1/8 inch with fractions on the other."""
    w_n, w_w = w
    items = []
    sign = side_mm  # +1: the mm scale on the window's upper edge
    d = math.ceil(w_n / COS_A * 2) / 2
    while d * COS_A <= w_w:
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
        if d == int(d) and d <= numbers_to:
            base = edge + sign * (GAP + LONG + 1.5) - (NUM_H if sign < 0 else 0)
            items.append(text(str(int(d)), r(x), r(base), NUM_H))
        d += 0.5
    # inches, on the other edge
    k = math.ceil(w_n / COS_A / 25.4 * 8)
    while (k / 8 * 25.4) * COS_A <= w_w:
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
        P("thick", "6 mm", "the card's thickness"),
        P("engrave", "0.6 mm", "how deep the ticks and numbers are cut"),
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
        *engrave("Card", scale(AXIS1, W1, +1, 32) + scale(AXIS2, W2, +1, 52)),
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
        P("label", "1 in", "the size's name, engraved on the tile", unit="text"),
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
        P("band", "8 mm", "the strip under each row where the holes' sizes are engraved"),
        P("head", "12 mm", "the strip along the top with the size's name and the ring hole"),
        P("thick", "6 mm", "the tile's thickness, so each hole is this deep"),
        P("engrave", "0.6 mm", "how deep the words are cut"),
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
        base = "1.2 mm" if row == 1 else "band + pitch + 1.2 mm"
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
    cmds += engrave("Tile", words)
    cmds.append(save(slug))
    return slug, cmds


if __name__ == "__main__":
    root = Path(sys.argv[1])
    for slug, cmds in (taper_card(), hole_grid()):
        (root / "models" / slug).mkdir(parents=True, exist_ok=True)
        out = root / ".git" / f"{slug}-script.json"
        out.write_text(json.dumps({"commands": cmds}, indent=1) + "\n")
        print(out, len(cmds))
```

- [x] **Step 4: Write their pages.**

`models/dowel-taper-card/model.yml`:

```yaml
title: Dowel taper card
summary: >-
  A card with two tapered windows that reads a dowel's real diameter, from 1/2 to 2 inches, in
  millimetres and in inch sizes: slide it along the dowel until it stops.
status: designed
material: PLA
print:
  Orientation: flat, as saved, the engraved face up
  Layer height: 0.2 mm
  Walls: 3
  Infill: 15%
  Supports: none
  Hole compensation: none (in Bambu Studio, X-Y hole and contour compensation both 0)
notes: |
  A dowel sold as 1 inch can be 25.0 mm, or a little oval, and sanding and a finish change it
  again by tenths of a millimetre. The card reads its real diameter, at the store or at home.

  1. **Put the dowel through** the window its size falls in, at the wide end: the narrow window
     reads 11 to 33 mm (1/2 to 1 1/4 inches), the wide one 31 to 53 mm (1 1/4 to 2 inches).
  2. **Slide the card** until the dowel touches both sides of the window. Don't push hard: the
     sides give a little, and the card then reads small.
  3. **Read the tick where it touches.** Millimetres along one side, a tick every 0.5 mm and the
     whole millimetres numbered; inch sizes along the other, every 1/8 inch. The window narrows
     0.1 mm for each millimetre along it, so ticks 0.5 mm apart are 5 mm apart on the card, and
     a tenth of a millimetre is a millimetre between them.
  4. **Turn the dowel a quarter turn** and read again: the two readings differ by how oval it is.

  A round dowel touches the window's slanted sides a little ahead of its centre, where the window
  is its diameter times 0.99875 (`cos_a`); the ticks are drawn there.

  **Check the card with a coin** before trusting it to a tenth: lay the card flat, drop a coin
  into a window and slide it until it touches both sides. A coin's diameter is set by its mint:
  a Canadian quarter is 23.88 mm, a loonie 26.5 mm and a toonie 28.0 mm; a US quarter is
  24.26 mm and a nickel 21.21 mm. A printer prints a window a little narrow, so a coin that
  reads 0.1 mm over means every reading is 0.1 mm over: take that off each one.

  The [hole grid](dowel-hole-grid.html) answers the same question in 0.2 mm steps, by the
  smallest hole a dowel goes through. Neither decides how a part fits: the
  [fit-test coupon](dowel-fit-coupon.html) does, on the finished dowel.
```

`models/dowel-hole-grid/model.yml`:

```yaml
title: Dowel hole grid
summary: >-
  A tile for each dowel size from 1/2 to 2 inches, with six holes from 0.6 mm under the size to
  0.4 mm over: the smallest hole a dowel goes through gives its real diameter, to 0.2 mm.
status: designed
material: PLA
size: 1 in
sizes:
  1/2 in: {dowel_d: 12.7 mm, label: 1/2 in}
  5/8 in: {dowel_d: 15.875 mm, label: 5/8 in}
  3/4 in: {dowel_d: 19.05 mm, label: 3/4 in}
  7/8 in: {dowel_d: 22.225 mm, label: 7/8 in}
  1-1/8 in: {dowel_d: 28.575 mm, label: 1 1/8 in}
  1-1/4 in: {dowel_d: 31.75 mm, label: 1 1/4 in}
  1-3/8 in: {dowel_d: 34.925 mm, label: 1 3/8 in}
  1-1/2 in: {dowel_d: 38.1 mm, label: 1 1/2 in}
  1-5/8 in: {dowel_d: 41.275 mm, label: 1 5/8 in}
  1-3/4 in: {dowel_d: 44.45 mm, label: 1 3/4 in}
  1-7/8 in: {dowel_d: 47.625 mm, label: 1 7/8 in}
  2 in: {dowel_d: 50.8 mm, label: 2 in}
print:
  Orientation: flat, as saved, the engraved face up, so the holes print upright, the closest to size a printer prints them
  Layer height: 0.2 mm
  Walls: 3
  Infill: 15%
  Supports: none
  Hole compensation: none (in Bambu Studio, X-Y hole and contour compensation both 0)
notes: |
  Print the tiles for the sizes you'll look at: several fit on one plate, and a key ring through
  their corner holes keeps them together. Each tile is one dowel size, its name on the top strip,
  and its six holes go up by 0.2 mm, each engraved with its own diameter:

  | Hole | From the size | For a 1-inch dowel |
  |---|---|---|
  | top left | -0.6 mm | 24.8 mm |
  | top middle | -0.4 mm | 25.0 mm |
  | top right | -0.2 mm | 25.2 mm |
  | bottom left | 0 mm | 25.4 mm |
  | bottom middle | +0.2 mm | 25.6 mm |
  | bottom right | +0.4 mm | 25.8 mm |

  Push the dowel into each hole, the smallest first. The first it goes through without forcing
  gives its diameter to 0.2 mm: a 1-inch dowel that goes through 25.2 but not 25.0 is between
  25.0 and 25.2 mm. Try again a quarter turn round: an oval dowel goes through one way and not
  the other. A dowel that goes through every hole is more than 0.6 mm under its size: try the
  tile one size down.

  Printed holes come out a little small, so the grid reads a dowel a little large: by as much as
  the [taper card](dowel-taper-card.html), checked against a coin, reads over. Neither decides
  how a part fits: the [fit-test coupon](dowel-fit-coupon.html) does, on the finished dowel.
```

- [x] **Step 5: Build them.** `make models` (about eight minutes: the card's engraving is slow to
  export, draw and measure). Look at both pictures, and at the 1/2-inch and 2-inch tiles in a
  slicer or SolidCraft: every number readable, nothing running into a hole or a window.
- [x] **Step 6: The docs.** In `website/_overview.qmd`, the edge `  built -.-> gauges` becomes
  `  built --> gauges` and the line `  class gauges planned` goes;
  in `README.md`, the status's second sentence reads "Phase 2, under way, replaces those two with
  the rail's five parts, then prints, tests and installs them; two gauges, a taper card and a hole
  grid, measure the dowels at the store first."
- [x] **Step 7: Run the checks; they pass.** `make check`. Expected: every test passes twice,
  the thirteen new ones included, and every built STL is watertight (`tests/test_meshes.py`).
- [x] **Step 8: Commit.** Write the message to `.git/COMMIT_MSG`:

```text
feat(models): 🤖 add the taper card and the hole grid, gauges for the store

Dan asked for a gauge to carry to the store, to read the dowels from 1/2
to 2 inches before buying, and chose two (Phase 2 Q&A 11). The taper
card's two windows narrow 0.1 mm for each millimetre along them, so a
dowel stops at its diameter, engraved to the half millimetre, with its
inch size on the other side; a coin checks the card. The hole grid is one
tile per eighth of an inch from 1/2 to 2, six holes 0.2 mm apart, each
engraved with its diameter; every tile fits the P2S's plate. Both are
PLA, printed flat.

The tile's name is a text parameter, which SolidCraft's eval leaves out,
so make models refused the sizes that change it: it now takes a design's
text parameters from the design itself (models.parameter_names).

The new tests failed first: 13 failed, with FileNotFoundError for each
gauge's eval.json, and "size '1/2 in' changes 'label', which the design
has no parameter named".

Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 9
Co-Authored-By: <the model's own line>
```

  `git add models/dowel-taper-card models/dowel-hole-grid tests/test_dowel_taper_card.py tests/test_dowel_hole_grid.py scripts/models.py tests/test_models.py website/_overview.qmd README.md`,
  then `git commit -F .git/COMMIT_MSG`, then `git log -1 --format='%(trailers)'` shows the
  `Plan:` line.
- [x] **Step 9: Review, look forward, close.** The review looks at the pictures and the pages too.

  - **Review (Tier 2: one reviewer under Standards and Spec, as Tasks 2 to 7 had; re-review only
    if a fix changes behaviour beyond its finding),** from `$(cat .git/TASK_BASE)`.
  - **Forward:** Task 10's step 7 uses the gauges; nothing else consumes them.
  - **Docs:** Step 6; S33 and S34 `built`; the STLs and pictures reach the live gallery with
    Task 11's publish, named to Dan there.
  - **Close,** its own commit: this task's boxes ticked, **Now** set to the next task, any
    Built differently and Ruling lines, deferred findings on the phase-end list, the spec's
    scenario statuses. The message, from `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 9: The store gauges: a taper card and a hole grid

    <what the task built, and why, in a few lines>

    Drift: <filled at the close, or none>
    Rulings: <filled at the close, or none>
    Phase-end: <filled at the close, or none>
    Forward: <filled at the close, or none>
    Tier: 2
    Rounds: <filled at the close>
    Findings: <filled at the close, or none>

    Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 9
    Co-Authored-By: <the model's own line>
    ```

  - **Push** under the standing OK (Phase 2 Q&A 7): `make leaks privacy models-check`, then
    `git push origin phase-2`. The task is closed once CI on the closing commit, or a later one,
    is green.

***

### Task 10: [Dan] Measure, weigh, and print the coupon

**Tier:** none: Dan's measurements, recorded by the agent (Tier 3) · **Scenarios:** S26, S30

> **Paused at step 0b** (Phase 2 Q&A 15, 2026-11-09): Dan paused the lamp to finish the project and design parts
> afterwards. Steps 1 to 10 weren't done and stay unticked, as they were, for when the lamp resumes.
> The gauges' own work (steps 0a and 0b) is built, and the gauges are printing.

Runs in Dan's home. **Now** reads `waiting on Dan: <the step>` until each answer is in. The steps
are asked by *Asking Dan*, one at a time, after the list. Dan's changes to the parts are settled
(Phase 2 Q&A 1 to 7), so this is measurements only; the parts are already built at placeholder
sizes (Q&A 9), and Task 11 retunes them. Start the coupon's print first (step 9): it runs while he
measures, and it's tried once the dowel is sanded and finished (decided without Dan, 3).

- [x] **0. Record the base:** `git rev-parse HEAD > .git/TASK_BASE`.
- [x] **0a. The gauges on one plate** (Q&A 12), built by the agent before Dan prints them, Tier 3
  (margins round the engraved words; the windows, the taper, the ticks and the holes don't
  change, and their tests pass as they were). In Task 9's generator, `.git/gauges.py` (its step
  3b): the card's `BAND, MID` 20.0, 30.0 become 15.0, 28.0, and the grid's `band` "10 mm" becomes
  "8 mm"; then the generator and both SolidCraft scripts run again, and `make models`. The card
  is 251 by 149 mm, the 1-inch tile 93.4 by 87.6. New tests: in `tests/test_dowel_taper_card.py`,
  `test_the_card_and_a_one_inch_tile_share_the_printers_plate` (the card's width, the tile's and
  three 5 mm gaps within 256 mm; it failed first, `assert ((161.0 + 91.6) + (3 * 5.0)) <=
  256.0`), `test_every_word_is_at_least_2_mm_inside_the_cards_long_edges` and
  `test_words_in_neighbouring_rows_are_at_least_2_mm_apart`, each word reaching from a tenth of
  its height under its baseline to a tenth over its height; in `tests/test_dowel_hole_grid.py`,
  each lower-row number 2 mm inside the tile's edge.
- [x] **0b. The gauges' numbers raised, for a second colour, and both 4 mm thick** (Q&A 13 and
  14), Tier 3 as step 0a (the windows, the taper, the ticks' places and the holes don't change).
  In `.git/gauges.py`: `engrave` becomes `raise_up`, extruding the words and ticks `relief`
  (0.8 mm) up from the top as bodies of their own (`"operation": "new"`, each named
  `Lettering`), where it cut `engrave` (0.6 mm) down; each gauge's `thick` is 4 mm, from 6. Each
  page's print settings gain a `Second colour` line: one filament change at the first layer above
  4.0 mm. `tests/conftest.py`'s `engraved` is `lettering`, and `standing_on(model, base)` gives
  the bodies above the base. New tests: `test_it_is_4_mm_thick_and_its_lettering_stands_0_8_mm_proud_on_whole_layers`,
  the grid's `test_it_is_4_mm_thick_and_its_numbers_stand_0_8_mm_proud_on_whole_layers` (each
  height a whole number of 0.2 mm layers, so the change falls between two),
  `test_only_its_ticks_and_numbers_stand_above_its_top` and the grid's
  `test_only_its_numbers_and_size_stand_above_its_top` (every other body closed, from `thick` to
  `thick + relief`, inside the base's outline); each base is `thick` tall and its volume the
  gauge less its holes, the lettering's under 5% of a full layer; each page names the change.
  They failed first: `assert 6.0 == 4.0`, `KeyError: 'relief'` and `KeyError: 'Second colour'`.
  > **Built differently** (this step): the lettering was first joined to each body, as Task 9's
  > engraving was cut. The card's 162 words and ticks still hadn't joined after over half an hour
  > (a quarter of them took 85 s, nearly all in the boolean, and each batch joined after another
  > took longer: 1.4, 7.3, then 19.2 s for ten); `solid.emboss` gave the same body as slowly, and
  > cutting the top away round them failed as one profile past about 56 words ("invalid
  > whole-source profile holes") and ran past nine minutes in three. As bodies of their own they
  > take 3 s for both gauges, and `make models` replays each design three times. A slicer prints
  > an STL's touching shells as one part; `tests/test_meshes.py` still finds every edge shared by
  > two triangles.
- [ ] **1. Weigh the light:** the Barrina with its socket, cord and timer, on a kitchen scale.
  The parts assume 1 kg; above that, the agent re-runs the carrier's and the socket's moment
  (about 7.5 N·m at 24 inches), and Task 11 lengthens `carrier_l` or `socket_depth`.
- [ ] **2. The bulb:** its widest diameter, and its length from where it meets the socket to its
  face.
- [ ] **3. The socket:** its body's widest diameter, and its length from where the cord goes in
  to where the bulb starts.
- [ ] **4. The cord:** round or flat; its diameter, or its width and thickness, just above the
  socket, with calipers.
- [ ] **5. The heat:** the bulb on for an hour, then its hottest surface with a thermometer (an
  infrared one, or a kitchen probe held against it).
- [ ] **6. The screws:** which ones (#8 or #10 wood screws into a stud, or 3/16-inch toggle
  bolts); their heads' diameter and height, and the shank's; each a pan or washer head, since a
  flat (countersunk) head won't sit in the counterbores.
- [ ] **7. The dowels,** read at the store with the taper card and the hole grid (Task 9), after
  the card's coin check: the size bought and the wood; each dowel's real diameter, twice, a
  quarter turn apart; the rail's length, up to about 48 inches, and the arm's, 550 mm for the
  light at 24 inches. Then the sanding and the finish: the grits, the finish and its coats, and
  the diameter again on the card once it's dry. Wax stays off the rail where a carrier clamps:
  the wedges hold by friction.
- [ ] **8. The wall,** as measurements: its material, and whether a stud is where the feet go.
- [ ] **9. The coupon,** printed for that size standing on its edge (its page's print settings)
  while he measures, and tried on the dowel once it's sanded and finished (decided without Dan,
  3): which hole, by its dots, is the tightest the finished dowel goes into by hand, all the way
  (S26)? If every 1-inch hole is loose, the dowel is really 25 mm: print the 25 mm coupon, and
  build the parts at 25 mm. A dowel of another size gets the coupon, and the parts, saved at its
  diameter from the card (a ruling).
- [ ] **10. Record and close.** Each answer goes on the Phase 2 Q&A page, `docs/superpowers/plans/2026-11-05-3d-models-phase-2-qa.md`, in Dan's words, committed as `docs(plan): 🤖 Phase 2 Q&A <N>: <what>` with this plan's `Plan:` line. The room is recorded as measurements (heights, distances, the wall's material), never a description of the home: the Q&A pages are published. The coupon's `model.yml` becomes `status: printed`
  (Tier 3), with the hole that fit in its notes. Then the forward rewrite, named under
  `Forward:`: Task 11's retune scripts and notes, filled in with these values, part by part:
  - `clearance` (the coupon's `step` times one more than the dots that fit: a hole looser than
    the tightest, decided without Dan, 3) in the four dowel parts, its comment saying so, and the sentence in
    each of their notes that calls 0.4 mm a placeholder;
  - the dowel: another size than 1 inch sets `dowel_d` in the four dowel parts, saved at it;
  - the screws in the feet: `screw_d` and `head_d` at least 0.4 mm over the shank's and the head's,
    and `head_h` the head's height;
  - the cord: `cord_d` in the tip, and in the feet `cord_w` and `cord_depth` at least the cord and
    1 mm (a flat cord: the tip's slots and grip reshaped, a ruling);
  - the lamp in the shade: `socket_d`, `socket_l`, `bulb_d` and `bulb_l`;
  - over 60 °C at step 5: the shade's `gap` grows, decided with Dan (the spec's design calls);
  - over 1 kg at step 1: the carrier and the socket, as step 1 says.

  The close:

  - **Review (Tier 3: a self-review under Standards and Spec, plus the mechanical checks; and the
    added Q&A and notes text read for a place, an address, a person or a description of the
    home),** from `$(cat .git/TASK_BASE)`.
  - **Forward:** Task 11's scripts and notes take these values (above).
  - **Docs:** the coupon's page says it's printed and which hole fit; S26 `built`.
  - **Close,** its own commit: this task's boxes ticked, **Now** set to the next task, any
    Built differently and Ruling lines, deferred findings on the phase-end list, the spec's
    scenario statuses. The message, from `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 10: [Dan] Measure, weigh, and print the coupon

    <what the task built, and why, in a few lines>

    Drift: <filled at the close, or none>
    Rulings: <filled at the close, or none>
    Phase-end: <filled at the close, or none>
    Forward: <filled at the close, or none>
    Tier: 3
    Rounds: <filled at the close>
    Findings: <filled at the close, or none>

    Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 10
    Co-Authored-By: <the model's own line>
    ```

  - **Push** under the standing OK (Phase 2 Q&A 7): `make leaks privacy models-check`, then
    `git push origin phase-2`. The task is closed once CI on the closing commit, or a later one,
    is green.

***

### Task 11: Retune the parts to Dan's measurements, and publish them again

**Tier:** 2 · **Scenarios:** S28, S26, S30

> **Paused, not built** (Phase 2 Q&A 15, 2026-11-09): Task 10's measurements never came, so the five parts stay at
> their placeholder sizes. The steps stay unticked, as they were, for when the lamp resumes.

**Files:**
- Modify: the five rail designs (`models/rail-*/rail-*.sc`, by SolidCraft), their built files (by
  `make models`), their `model.yml` notes

**Interfaces:**
- Consumes: Task 10's answers; Tasks 2 to 6's designs and tests; Task 8's publishing steps.
- Produces: the five parts at Dan's sizes, live again.

- [ ] **Step 0: Record the base:** `git rev-parse HEAD > .git/TASK_BASE`.
- [ ] **Step 1: The parameter changes,** one command script per part, `.git/<slug>-retune.json`,
  each a `parameters.change` per value Task 10's close names for that part, then the save. Task
  9's close writes each script here, its values filled in (a forward rewrite); the shape, for the
  feet:

```json
{
  "commands": [
    {"command": "parameters.change", "params": {"name": "clearance", "expression": "<the coupon's>"}},
    {"command": "parameters.change", "params": {"name": "screw_d", "expression": "<the shank's + 0.4 mm>"}},
    {"command": "parameters.change", "params": {"name": "head_d", "expression": "<the head's + 0.4 mm>"}},
    {"command": "parameters.change", "params": {"name": "head_h", "expression": "<the head's height>"}},
    {"command": "parameters.change", "params": {"name": "cord_w", "expression": "<the cord + 1 mm>"}},
    {"command": "parameters.change", "params": {"name": "cord_depth", "expression": "<the cord + 1 mm>"}},
    {"command": "file.save_as", "params": {"path": "models/rail-feet/rail-feet.sc", "format": "json", "cache": false}}
  ]
}
```

  `solidcraft-cli run .git/<slug>-retune.json --in models/<slug>/<slug>.sc --quiet`, for each
  part.
- [ ] **Step 2: The notes:** each page's placeholder sentences give the measured values instead
  (the clearance, the cord, the lamp), and the feet's *Putting the rail together* its new numbers
  (its test holds them to the parameters).
- [ ] **Step 3: Rebuild and check.** `make models`, then `make check`. Expected: the five parts
  rebuilt, every test passing at the new values.
- [ ] **Step 4: Commit.** Write the message to `.git/COMMIT_MSG`:

```text
feat(models): 🤖 retune the rail's parts to Dan's measurements

<each value changed, with the Q&A answer it came from>

Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 11
Co-Authored-By: <the model's own line>
```

  `git add` each changed file under `models/rail-feet`, `models/rail-carrier`,
  `models/rail-arm-socket`, `models/rail-arm-tip` and `models/rail-shade`, by path, then
  `git commit -F .git/COMMIT_MSG`, then `git log -1 --format='%(trailers)'` shows the `Plan:` line.
- [ ] **Step 5: Publish again,** as Task 8's steps 1 to 4 do, its PR titled
  `chore(repo): 🤖 merge the rail's parts, retuned to Dan's measurements`.
- [ ] **Step 6: Review, look forward, close.**

  - **Review (Tier 2, one reviewer under both headings, Standards and Spec; fix Critical and
    Important; at most one re-review),** from `$(cat .git/TASK_BASE)`.
  - **Forward:** the look test (Task 12) prints these.
  - **Docs:** each page gives its measured values; S28 stays `built`; S26 `built` at Task 10.
  - **Close,** its own commit: this task's boxes ticked, **Now** set to the next task, any
    Built differently and Ruling lines, deferred findings on the phase-end list, the spec's
    scenario statuses. The message, from `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 11: Retune the parts to Dan's measurements, and publish them again

    <what the task built, and why, in a few lines>

    Drift: <filled at the close, or none>
    Rulings: <filled at the close, or none>
    Phase-end: <filled at the close, or none>
    Forward: <filled at the close, or none>
    Tier: 2
    Rounds: <filled at the close>
    Findings: <filled at the close, or none>

    Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 11
    Co-Authored-By: <the model's own line>
    ```

  - **Push** under the standing OK (Phase 2 Q&A 7): `make leaks privacy models-check`, then
    `git push origin phase-2`. The task is closed once CI on the closing commit, or a later one,
    is green.

***

### Task 12: [Dan] The look test

**Tier:** none: Dan's verdict, recorded by the agent; Tier 1 if a photo is committed ·
**Scenarios:** S11, S29

> **Paused, not done** (Phase 2 Q&A 15, 2026-11-09): the look test waits with the lamp. The steps stay unticked.

Settles "not sure if it'll look good with 3d printed parts and dowels" for a few hundred grams of
PLA (D8), and the joint by hand.

- [ ] **0. Record the base:** `git rev-parse HEAD > .git/TASK_BASE`.
- [ ] **1. Print the five parts in PLA,** in the colour the real ones will be, each with its
  page's print settings: the feet and their caps, the carrier and its wedge, the arm socket and its
  wedge, the tip with its wedge and clips, and the shade.
- [ ] **2. Put it together** where it will go, in the order the wall feet's page gives
  (*Putting the rail together*), the feet screwed as they will be (PLA holds a look test, not a
  light for days).
- [ ] **3. The joint by hand (S29):** does the carrier stay put when pushed down and twisted;
  does the arm socket sit on the dovetail without rocking (if it rocks, Task 4's `fit` goes to
  0.2 mm, a ruling); do the wedges come out as the notes say; and does anything show but the dowels
  and the parts? Then the light on for a few minutes, no longer (the shade is PLA here): does any
  pink show from the room?
- [ ] **4. The verdict,** asked as a scenario: A, it looks right, print it in PETG; B, it looks
  right with changes (which: the edges, a part's size, the shade's shape, the colour); C, it doesn't
  work, and why. Each answer goes on the Phase 2 Q&A page, `docs/superpowers/plans/2026-11-05-3d-models-phase-2-qa.md`, in Dan's words, committed as `docs(plan): 🤖 Phase 2 Q&A <N>: <what>` with this plan's `Plan:` line. The room is recorded as measurements (heights, distances, the wall's material), never a description of the home: the Q&A pages are published. B or C changes a design: the agent revises that part's listing in this
  plan, reopens its task, and logs a ruling on the Q&A page (fully vibed). Rounded edges are a
  likely B: the spec's Later row S22.
- [ ] **5. A photo, if Dan wants one on a page,** named for what it shows of the parts, never
  the place: Strip it first, `make strip FILES=<file>`; then show Dan the stripped file and ask, naming it, whether anything in it shows where he lives (a window's view, a street, a house number, a face, a reflection, a screen). Only after his OK naming the file does it go under `models/<slug>/photos/`, and `make privacy` passes before it's staged.
- [ ] **6. Close.**

  - **Review (Tier 3: a self-review under Standards and Spec, plus the mechanical checks, and the
    added text read for a place, an address, a person or a description of the home; with a photo,
    Tier 1: Matt Pocock's `code-review`, two axes in two subagents, plus the security checklist,
    one line per item; at most one re-review),** from `$(cat .git/TASK_BASE)`.
  - **Forward:** Task 13 prints the PETG parts.
  - **Docs:** each part's notes say the look test passed, or what changed; S11 and S29 `built`.
  - **Close,** its own commit: this task's boxes ticked, **Now** set to the next task, any
    Built differently and Ruling lines, deferred findings on the phase-end list, the spec's
    scenario statuses. The message, from `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 12: [Dan] The look test

    <what the task built, and why, in a few lines>

    Drift: <filled at the close, or none>
    Rulings: <filled at the close, or none>
    Phase-end: <filled at the close, or none>
    Forward: <filled at the close, or none>
    Tier: 3, or 1 with a photo
    Rounds: <filled at the close>
    Findings: <filled at the close, or none>

    Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 12
    Co-Authored-By: <the model's own line>
    ```

  - **Push** under the standing OK (Phase 2 Q&A 7): `make leaks privacy models-check`, then
    `git push origin phase-2`. The task is closed once CI on the closing commit, or a later one,
    is green.

***

### Task 13: [Dan] The load test

**Tier:** none: Dan runs it; the agent records it (Tier 3) · **Scenarios:** S13, S27, S30

> **Paused, not done** (Phase 2 Q&A 15, 2026-11-09): the load test waits with the lamp. The steps stay unticked.

- [ ] **0. Record the base:** `git rev-parse HEAD > .git/TASK_BASE`.
- [ ] **1. Print the five parts in PETG,** matte, with each page's print settings, and a second
  carrier, its wedge, and a second arm socket and its wedge.
- [ ] **2. Set it up** somewhere a fall breaks nothing, mounted the way it will be: into a stud,
  or with the chosen toggle bolts in an offcut of the same drywall clamped to a bench; the rail in
  its feet and screwed down through the bottom cup's floor; the arm (550 mm) on its carrier, the
  tip on its end; the second socket on the second carrier, a 150 mm stub of dowel wedged in it.
  Every wedge tapped home with a mallet. Note the rail's length and each carrier's height.
- [ ] **3. Load it:** three times the light's weight (Task 10's answer) hung from the tip by the
  light's cord through the stem's grip, not from the tip; 12 kg (three times two watered small
  planters) hung from the stub 100 mm out from the carrier. Mark the cord where it leaves the grip,
  and each carrier's top edge on the rail.
- [ ] **4. Measure at 0, 24 and 48 hours:**
  - the tip's height above the floor or the bench;
  - the arm's tilt at its socket: clamp a straightedge to the rail at the carrier, and with a dial
    indicator or calipers reading 0.01 mm, measure from it to the arm's underside 100 mm past the
    socket's mouth. Its growth times 3.4 is its share of the light's drop (the light is about 3.4
    times as far from the carrier). The rail's own bending, 2 to 5 mm at the light, falls out of
    this reading, since the straightedge moves with the rail;
  - how far each carrier has slipped from its mark;
  - how far the cord has slipped (S27).
- [ ] **5. The heat (S30):** the light on for 14 hours, the timer's longest, inside its PETG
  shade: the shade's hottest point with the thermometer, and whether it softened, warped or
  discoloured.
- [ ] **6. The result:** passes when the arm's tilt at its socket adds under 1 mm at the light,
  neither carrier slips 2 mm, the tip's total sag grows by under 5 mm, the cord slips under 2 mm,
  nothing cracks or pulls out, and the shade stays under 60 °C (S13, S27, S30). Each answer goes on the Phase 2 Q&A page, `docs/superpowers/plans/2026-11-05-3d-models-phase-2-qa.md`, in Dan's words, committed as `docs(plan): 🤖 Phase 2 Q&A <N>: <what>` with this plan's `Plan:` line. The room is recorded as measurements (heights, distances, the wall's material), never a description of the home: the Q&A pages are published. The
  agent adds a "Load test" section to each part's notes, sets each part's `status: printed`, and
  commits:

```text
docs(models): 🤖 record the rail's load test

<the loads, the arm's length, the mounting, the readings at 0, 24 and 48
hours, the shade's temperature, and the result, from the Q&A page>

Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 13
Co-Authored-By: <the model's own line>
```

  A failed test is the fifth stop's case (fully vibed, a ruling): a longer carrier, a deeper
  socket, a tighter or longer grip, the knee brace (S15), or a bigger gap round the lamp is planned
  in, with the reason, and Dan is told.
- [ ] **7. Close.**

  - **Review (Tier 3: a self-review under Standards and Spec, plus the mechanical checks, and the
    added text read for a place, an address, a person or a description of the home),** from
    `$(cat .git/TASK_BASE)`.
  - **Forward:** Task 14 installs what passed.
  - **Docs:** each part's page carries the load test; S13, S27 and S30 `built`.
  - **Close,** its own commit: this task's boxes ticked, **Now** set to the next task, any
    Built differently and Ruling lines, deferred findings on the phase-end list, the spec's
    scenario statuses. The message, from `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 13: [Dan] The load test

    <what the task built, and why, in a few lines>

    Drift: <filled at the close, or none>
    Rulings: <filled at the close, or none>
    Phase-end: <filled at the close, or none>
    Forward: <filled at the close, or none>
    Tier: 3
    Rounds: <filled at the close>
    Findings: <filled at the close, or none>

    Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 13
    Co-Authored-By: <the model's own line>
    ```

  - **Push** under the standing OK (Phase 2 Q&A 7): `make leaks privacy models-check`, then
    `git push origin phase-2`. The task is closed once CI on the closing commit, or a later one,
    is green.

***

### Task 14: [Dan] Install it

**Tier:** none: Dan installs it; the agent records it, Tier 1 for the photo · **Scenarios:** S14, S32

> **Paused, not done** (Phase 2 Q&A 15, 2026-11-09): the install waits with the lamp. The steps stay unticked.

- [ ] **0. Record the base:** `git rev-parse HEAD > .git/TASK_BASE`.
- [ ] **1. Mount it** as tested, in the order the wall feet's page gives (*Putting the rail
  together*): its numbers (where the top screw goes, the arm's length) are the parts' own.
- [ ] **2. Bump it:** a push at the light, sideways and up, doesn't turn the arm round the rail;
  lifting a carrier, the arm or a planter doesn't raise the rail (S32); the light swings and
  settles.
- [ ] **3. A photo:** Strip it first, `make strip FILES=<file>`; then show Dan the stripped file and ask, naming it, whether anything in it shows where he lives (a window's view, a street, a house number, a face, a reflection, a screen). Only after his OK naming the file does it go under `models/<slug>/photos/`, and `make privacy` passes before it's staged. It goes in `models/rail-carrier/photos/installed.jpg`; the
  gallery shows it on the page. Each part's `status: in use`. Each answer goes on the Phase 2 Q&A page, `docs/superpowers/plans/2026-11-05-3d-models-phase-2-qa.md`, in Dan's words, committed as `docs(plan): 🤖 Phase 2 Q&A <N>: <what>` with this plan's `Plan:` line. The room is recorded as measurements (heights, distances, the wall's material), never a description of the home: the Q&A pages are published. Commit:

```text
docs(models): 🤖 the grow-light rail is installed

<how it was fixed to the wall, the rail's length, and Dan's words on how it
looks>

Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 14
Co-Authored-By: <the model's own line>
```

- [ ] **4. The overview diagram.** In `website/_overview.qmd`, delete the line
  `  class railup planned`: it's up.
- [ ] **5. Close.**

  - **Review (Tier 1: Matt Pocock's `code-review`, two axes in two subagents, plus the security
    checklist, one line per item; at most one re-review, over the photo),** from
    `$(cat .git/TASK_BASE)`.
  - **Forward:** the phase end.
  - **Docs:** the README's first-project lines say it's up; S14 and S32 `built`.
  - **Close,** its own commit: this task's boxes ticked, **Now** set to the next task, any
    Built differently and Ruling lines, deferred findings on the phase-end list, the spec's
    scenario statuses. The message, from `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 14: [Dan] Install it

    <what the task built, and why, in a few lines>

    Drift: <filled at the close, or none>
    Rulings: <filled at the close, or none>
    Phase-end: <filled at the close, or none>
    Forward: <filled at the close, or none>
    Tier: 1
    Rounds: <filled at the close>
    Findings: <filled at the close, or none>

    Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 14
    Co-Authored-By: <the model's own line>
    ```

  - **Push** under the standing OK (Phase 2 Q&A 7): `make leaks privacy models-check`, then
    `git push origin phase-2`. The task is closed once CI on the closing commit, or a later one,
    is green.

***

### Task 15: Phase end

The same nine steps as Phase 1's Task 10, each one box ending in its commit
(`docs(plan): 🤖 phase end step K: <what it did>`, with `Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Phase end`), resumed at the
first unticked box. This is the last phase planned: step 5 offers Dan each Later row by *Asking
Dan*: plan it, keep it optional, or drop it.

- [x] **1. The final whole-branch review**
- [x] **2. The rest of the ledger copied into the plan**
- [x] **3. The phase-end council** (`…-phase-2-end-council.md`, with its Design-page line)
- [x] **4. The phase-end list worked through**
- [x] **5. The forward look, and the Later rows offered to Dan**
- [x] **6. The retro** (`…-phase-2-retro.md`, with its Design-page line)
- [x] **7. The changelog and status**
- [ ] **8. The PR:** `chore(repo): 🤖 merge Phase 2: the rail's parts and the store gauges (#N)`; it
  adds the gauges' 16 STL and PNG files, which no scan can read, so it waits for Dan's look at each
  before the merge
- [ ] **9. After the merge:** the gauges' pages are live, their viewers load, and the live site
  loads nothing from another host, checked in the browser's network log too

***

## Phase-end list

| Source | Severity | File | Item | Status |
|---|---|---|---|---|
| Phase start, goal fit 19 | Minor | spec, *Open items* | The PythonSCAD grow-light stand from 2026-10-16 ("worth a look at Phase 2's start") wasn't looked at: the rail's design came from Dan's references | Later: the spec's *Open items* keeps it, and the rail is paused |
| Phase start, security 8 | Minor | `scripts/privacy.py` | A photo with a suffix the check doesn't list (`.jpe`, `.pjpeg`, none) is never opened; the look test adds the first photos | Later, S37: no photo is in the repo yet, and the look test that adds the first is paused |
| Task 1, Standards 2 | Minor | `scripts/offsite.py` | An `iframe`'s `srcdoc` (HTML with its own tags) isn't parsed | Later, S36 |
| Task 1, Standards 3 and 4 | Minor | `scripts/offsite.py` | A URL a browser normalises (a backslash for a slash, a tab inside the scheme, `https:/host`) or CSS escapes and comments (`u\72l(`, `url(/**/…)`) pass; none can come from Quarto's output | Later, S36 |
| Task 1, Spec 2 | Minor | `scripts/offsite.py` | A script's `fetch(` or `importScripts(`, an import map, and JSON files aren't read; the phase end's network-log look covers them | Later, S36 |
| Task 2, review | Minor | `models/rail-feet` | 0.75 mm of plastic between the cord's groove and each screw's counterbore | Later, S35 |
| Task 2, review | Minor | `models/rail-feet` | The caps hold by a press fit alone, with no catch; the look test (Task 12) checks them | Later, S35 |
| Task 2, review | Minor | `tests/test_rail_feet.py` | The test holds the parameters, not the built cuts: a design with the floor's hole or the groove deleted would pass | Later, S35 |
| Task 3, review | Minor | `tests/test_rail_carrier.py` | The groove's and the wedge's shared slope is held by the parameter alone, not the built geometry | Later, S35 |
| Task 3, review | Minor | `models/rail-carrier` | `channel` is measured at the carrier's bottom; the wedge's tail below it is thicker, leaving about 7.7 mm to the pads' plane | Later, S35 |
| Task 3, review | Minor | `models/rail-carrier` | The wedge meets the round rail on a line; a face hollowed to the dowel's radius would add contact; the load test (Task 13) shows whether it's needed | Later, S35 |
| Task 3, review | Minor | `models/rail-carrier` | Literals outside the parameters (the wedge's 20 mm seat, its 40 mm offset); "three sizes" in a test name counts the saved one | Later, S35 |
| Task 4, review | Minor | `models/rail-arm-socket` | The slot's flanks aren't parallel to the dovetail's: the side gap is 0.3 mm at the base, 0.19 mm at the tip; the look test (Task 12) checks the fit | Later, S35 |
| Task 4, review | Minor | `models/rail-arm-socket` | The boss is wider than the block, so printed on its back it leaves a 3.9 mm ledge the notes' "Supports: none" doesn't mention | Later, S35 |
| Task 4, review | Minor | `tests/test_rail_arm_socket.py` | The groove's wall is measured from the dowel's top, not the bore's (0.2 mm apart) | Later, S35 |
| Task 5, review | Minor | `models/rail-arm-tip/model.yml` | "Supports from the bed only" can't reach inside the cap's horizontal bore, whose arch prints unsupported | Later, S35 |
| Task 5, review | Minor | `models/rail-arm-tip` | The clips' rings ignore `clearance`, and are three copied blocks with literals | Later, S35 |
| Task 5, review | Minor | `tests/test_rail_arm_tip.py` | The test holds the cord's sizes, not its built path through the keel and the stem | Later, S35 |
| Task 5, review | Minor | `models/rail-arm-tip` | 1.5 mm of plastic between the keel's channel and the bore | Later, S35 |
| Task 6, review | Minor | `tests/test_rail_shade.py` | The gap is tested radially; across the cone's slope it is a little less (about 10 mm at a 12 mm radial gap) | Later, S35 |
| Task 6, review | Minor | `tests/test_rail_shade.py` | The notches' fit round the stem's lugs is untested | Later, S35 |
| Task 6, review | Minor | `models/rail-shade` | Its picture shows the open rim, not the top with its notches and vents | Later, S35 |
| Task 6, review | Minor | `models/rail-shade/model.yml` | The notes don't say the shade needs a bed about 155 mm across | Later, S35 |
| Task 7, review | Minor | `models/sconce-*/model.yml` | The superseded notes cite "Phase 2 Q&A 1 to 4" on a public gallery page, reachable only through the Design page | Later, S37: the link is honest, and that Q&A is clean |
| Task 9, review | Minor | `models/dowel-taper-card`, `models/dowel-hole-grid` | Whether 0.6 mm ticks and 5 to 7 mm engraved numbers in the built-in font's regular face print legibly with a 0.4 mm nozzle is a judgement; Dan's first print (Task 10) shows it | Later, S38 |
| Final review, Spec 1 | Minor | `tests/test_rail_*.py` | S28's parts are tested at 1 inch; the other sizes are held only as closed meshes (the outlines and the feet's volume were seen to change with size, by hand) | Later, S35 |
| Final review, re-check | Minor | `tests/test_dowel_hole_grid.py` | Each size's tile is measured by its outline, which follows from its widest hole; no hole's own diameter is measured | Later, S37 |
| Final review, Standards | Minor | `scripts/privacy.py:109` | `jpeg_walk` returns two positional optionals, which helped hide its bug; a NamedTuple would name them | Later, S37 |
| Final review, Standards | Minor | `scripts/privacy.py:48,56` | The same three APPn segments are listed twice, by name and by marker | Later, S37 |
| Final review, Standards | Minor | `scripts/gallery.py:154,181` | The same bracket escaping twice in one function | Later, S37 |
| Final review, Standards | Minor | `tests/` | Repeated setup: `PLATE_MM` and `LAYER_MM` twice, near-copy tests in the two gauges, the rail's clearance and wedge checks, two identical bodies in `test_privacy.py`; `standing_on` might read better as `bodies_except` | Later, S37 |
| Council, reliability 2 | Minor | `scripts/models.py` | `build()` doesn't check an output is a whole STL before recording it; `make check` still catches an empty one | Later, S37 |
| Council, reliability 4 to 6 | Minor | `tests/conftest.py`, `scripts/models.py`, `scripts/gallery.py` | The fake CLI never changes a text parameter; `invalid()` says only "stale" once a design changes; a viewer's `data-stl` file isn't checked | Later, S37 |
| Council, security 2 | Minor | `scripts/privacy.py` | An STL's 80-byte header isn't checked; today each holds only `SolidCraft STL <slug>` | Later, S37 |
