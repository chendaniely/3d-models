# 3d-models: the kickoff council

Four read-only reviewers, one per lens, read the spec, the Q&A page, the kickoff notes, both phase
plans and `AGENTS.md` on 2026-11-05, at `4043c9a` (since amended to `5b56278` for security finding
F4). Their reports are below as they gave them, shortened only where they quoted file text, with
two redactions: F4 names no place, and nothing here quotes Quarto's include shortcode or a
brace-fenced cell (reliability finding 1 explains why). The session's check of each claim, and the
decision on each finding, follow in [Decisions](#decisions), written after the reports were
committed.

## Goal fit and scenarios

0 critical, 8 important, 4 minor.

1. **Important:** the cord clamp (Phase 2 plan, Task 3; spec, Phase 2's design calls). Beyond the
   ring the shelf sits only 0.8 mm under the dowel, the cord hole straight under its axis: with the
   dowel running past the clamp, a 6 mm cord along the arm can't reach the hole, so the clamp works
   only at the dowel's tip. Once in the hole, which is the cord's own size, only friction holds it.
   Sharp printed edges rub the mains cord as the light swings. The ears and bolt sit on top, where
   Task 6 routes the cord. Fix: the shelf at least `cord_d` plus about 4 mm below the dowel; a real
   grip; chamfered cord edges; the ears on the side; ask whether the cord is round or flat, and what
   the kit's hanging system includes.
2. **Important:** S18's proof doesn't test slipping; the load test hangs the load "from the clamp",
   not through the cord grip. Fix: hang three times the light's weight by the cord, record slip at
   0, 24 and 48 hours, and name that in S18's proof.
3. **Important:** the coupon prints with its holes vertical, the socket and the clamp's bore
   horizontal; horizontal holes print smaller and out of round, so the coupon's clearance would be
   too tight. Fix: print the coupon on its long edge, holes horizontal.
4. **Important:** Phase 2's tests hardcode values Task 1 changes: `dowel_d == 25.4`, and a
   clearance from 0.2 to 0.8 that fails if Dan follows the coupon page's "step 0.3" advice. Fix:
   assert the clamp's `dowel_d` equals the wall block's, and the clearance is the coupon's `step`
   times k, read from the coupon's measurements.
5. **Important:** nothing protects the "visible screws" anti-goal, and the drafts break it: screw
   holes straight through the plate face, the pin's ends on the boss, the clamp's bolt on top, no
   uniform edge radius. Fix: counterbored screw holes with a cover, a capped pin, a recessed bolt
   and a nut trap, one fillet parameter; visible hardware part of the look test's verdict.
6. **Important:** answer 5 says photos are stripped "before they're committed", but the guard runs
   after: `make check` after the commits, pushes gated only by `make leaks`, CI after the push to a
   public repo; S03's "strip fixes it" leaves the original in history. Fix: `make leaks photos`
   before every push, and reword S03.
7. **Important:** no licence: a public gallery of downloads is all rights reserved by default.
   Dan's call.
8. **Important:** the wall block's print settings: on its side, the 54 mm boss hangs unsupported, so
   "supports under the socket's mouth only" is wrong; a 4.5 mm `screw_d` takes #8 screws but not
   the 3/16- or 1/4-inch bolts of heavy toggles.
9. **Minor:** S10 can only be proven after the merge (Phase 1's phase end, step 9); S11 to S14 and
   S18 name no task.
10. **Minor:** D11 says the check covers "a JPEG or PNG under models/"; the code checks every image
    in the repo.
11. **Minor:** S13 says "a 20-inch dowel"; Task 5 tests the arm's length, 16 to 20 inches.
12. **Minor:** the Success line says a model needs "a .sc and one command", but a page needs a
    `model.yml`; give a template in the README.

Fine: answers 3, 4, 6, 7, 9, 10 and 11 each have a delivering task; D1 to D10 and D12 match Dan's
words; S01, S02, S05 to S09 and S11 have adequate proofs.

## Reliability

1 critical, 7 important, 5 minor. Each claim was checked in scratch copies.

1. **Critical:** Phase 1, Task 4, `make docs` on the real docs. Quarto 1.11.6 expands include
   shortcodes even inside fenced code, and the Phase 1 plan quotes them in its listings: the render
   fails with "Include directive failed", one wrapper including itself. With those escaped, the
   nested mermaid listings fail next ("You must use the .qmd extension for documents with
   executable code"). The prototype passed only because its plan files were one-line stubs. The
   same hazard applies to council reports and retros. Fix: keep the docs literal and have a
   pre-render step write escaped copies; a test that fails on an unescaped shortcode or cell.
2. **Important:** `build.json` records only the design's hash, so a commit with a new design and
   record but an old STL, picture or measurements passes `models-check`, and the site serves the
   stale STL. Fix: record each built file's sha256 too.
3. **Important:** on case-insensitive macOS, `models/hook/Hook.sc` is built and checked; on Linux
   CI it's skipped, so the model quietly drops off the site. Fix: `check` fails on any `.sc` not
   named exactly `<folder>/<folder>.sc`.
4. **Important:** Phase 2's install photo, "linked from the notes", is never published: the gallery
   copies only the STL, picture and design, and Quarto doesn't warn on a missing image. Fix: copy
   `photos/`, with a test.
5. **Important:** the coupon's clearance is relative to nominal 25.4 mm holes; setting `dowel_d` to
   a measured 25.1 mm and keeping that clearance makes the socket 0.3 mm too tight. Fix: socket =
   nominal + the clearance of the hole that fit.
6. **Important:** the coupon calibrates vertical holes, the socket prints horizontal; and on its
   side the whole boss hangs above the bed, so the supports line is wrong.
7. **Important:** the clamp's cord hole is exactly `cord_d`, so nothing grips the cord vertically,
   and the load test never loads it through the cord.
8. **Important:** a 4.5 mm `screw_d` passes only the smallest toggles (about 30 lb ultimate in
   half-inch drywall, under a 4:1 margin at the top screw's 54 N); 3/16-inch toggles need about
   5 mm. A drywall install is never load-tested. Fix: size `screw_d` to a named anchor; with no stud,
   load-test that anchor in a drywall offcut.
9. **Minor:** no `.python-version`, so local runs 3.14 and CI the runner's Python; lychee never ran
   locally. Fix: pin Python; install lychee so `make check` runs it.
10. **Minor:** PyYAML turns `Supports: no` into False, shown as "False". Fix: reject booleans.
11. **Minor:** partial writes: `build --force` keeps a matching record over half-written outputs;
    the design is hashed after the CLI runs; `strip` overwrites in place. Fix: delete the record
    and hash first; `strip` writes a temp file, then replaces.
12. **Minor:** Task 6 expects "2 images", but `photos` runs before `docs`, so a first run prints 1.
13. **Minor:** the wall block's vertical pin is loose and held by nothing, so it can drop out. Fix:
    a pin secured with a nut or clip.

Fine: every pinned action tag exists; the gitleaks checksum matches; lychee-action v2.9.0 accepts
v0.24.2; Task 5's zero-model render passes; the Makefile's grep matches Quarto's wording; the
prototype's scripts and tests are byte-identical to the plan's listings.

## Security

0 critical, 5 important, 3 minor.

**Checklist:** secrets fine (no CI secrets, `persist-credentials: false`, gitleaks `--redact`);
permissions fine (`contents: read` at the top, `pages: write` and `id-token: write` only on
`pages`, on `main`, never a PR); network exposure a finding (F6); failing closed a finding (F1);
injection fine (argv lists, no untrusted expressions in `run:`, `pull_request` not
`pull_request_target`, `yaml.safe_load`); logging fine.

**Tiers:** Phase 1's Task 6 to Tier 1 (the first real `solidcraft-cli` output, never inspected, its
binaries unscannable); Phase 2's Tasks 4 and 6 to Tier 1 when a photo is committed; Task 5's import
map gets a checklist line; the rest as planned.

- **F1 Important:** the photo check fails open. A PNG with GPS in a compressed iTXt chunk passes; a
  JPEG with a body serial number, owner name, artist and an XMP city passes, since only GPS is
  checked; `strip` keeps a JPEG's comment; AVIF, JXL, GIF, DNG and raw, JFIF, MOV and MP4, an MPO's
  second frame and the EXIF thumbnail are never examined. Fix: allow no metadata but a colour
  profile, a single frame; refuse every other image or video extension; clear the image's info
  before saving; a test per case.
- **F2 Important:** nobody reviews what a photo shows: a window's view, the street, house numbers,
  faces, reflections, screens. Fix: before staging, show Dan the stripped file with that list and
  get an OK naming the file; every push-OK request lists the binaries it adds; Q&A answers about
  the room recorded as measurements, since the Q&A pages are published.
- **F3 Important:** the "no absolute local path" constraint is never checked, and gitleaks' default
  rules don't flag home-folder paths. Fix: a `make check` and CI step that searches tracked text,
  and the PNG and STL bytes, for home-folder paths; Task 6 inspects the outputs before staging.
- **F4 Important:** the photo tests' made-up GPS values are a real city-level point, which next to
  the anti-goal reads as Dan's location; only in unpushed `4043c9a`. Fix: made-up coordinates such
  as 0°, 0°; Dan decides on rewriting `4043c9a`.
- **F5 Important:** every action is pinned by tag; a moved tag could rewrite the site before the
  upload. Fix: full commit SHAs with a version comment, kept current by Dependabot; the settings
  task requires SHA pins.
- **F6 Minor:** the jsDelivr modules have no integrity check, and visitors' addresses go to a third
  party. Fix: vendor the four files, or an import-map `integrity` block.
- **F7 Minor:** gitleaks' default log passes no `-m`, so merge commits' own changes go unscanned.
  Fix: `--log-opts` with `-m`.
- **F8 Minor:** the settings task: a branch rule on the `github-pages` environment, a read-only
  default workflow token, an allow-list of actions.

## Simplicity

2 important, 8 minor.

1. **Important:** the site is checked three times: `gallery.py check-site` with its fixture and
   tests, the render log's grep, and lychee twice (the Makefile's branch, which never fires in CI,
   and the CI action). Fix: cut `check-site`; install lychee in CI before `make docs`, and drop the
   action.
2. **Important:** the wall block isn't designed for the look test it's meant to settle: square
   edges and screw heads facing the room. Fix: counterbored screw holes with printed caps, rounded
   edges if the script can make them.
3. **Minor:** per-model tests repeat `make check`'s staleness and `model.yml` checks; the `params`
   and `body` helpers are copied three times; the 25.4 mm tests fight Review Focus 2.
4. **Minor:** `test_check_runs_everything_ci_runs_but_the_build` compares the `check:` line with a
   copy of itself; the four placeholder targets exist only so a test passes.
5. **Minor:** CI's `make test-utc` repeats `make test`, since runners use UTC.
6. **Minor:** Dependabot's `uv` entry opens monthly PRs Dan must merge; keep `github-actions` only,
   grouped.
7. **Minor:** the diagram zoom is about 50 lines no scenario asks for.
8. **Minor:** `models.py build --force` is called by no target or scenario.
9. **Minor:** the clamp's cord tab could sit straight under the ring.
10. **Minor:** each task repeats a 25-line close block; one line per task would do.

Sound: hash-based freshness, the import map, generated git-ignored model pages, the photo guard's
scope, the [Dan] tasks as separate gates.

## Decisions

Written after the reports above were committed.
