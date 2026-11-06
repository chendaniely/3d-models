# 3d-models: design spec

**Status:** spec approved 2026-11-05 · Phase 1 merged 746ce34 2026-11-05 · revised 2026-11-06 for the rail (Phase 2 Q&A 1 to 5), approved 2026-11-06 (Phase 2 Q&A 6) · Phase 2 in progress on `phase-2`, its start merged to `main` (#2, `7b53336`)

Kickoff's answers, with Dan's reasons in his words, are on the
[Q&A page](2026-11-05-3d-models-qa.md); the feasibility numbers behind the sconce are in the
[kickoff notes](2026-11-05-3d-models-kickoff-notes.md); the council's review and what became of
each finding are in the [kickoff council](2026-11-05-3d-models-kickoff-council.md). Dan said
"oneshot the rest of the repo", so every design call below that he didn't make himself is the
agent's, logged on the Q&A page as "decided without Dan" (D1 to D19).

## What this is, and why

A public repo of Dan's 3D-print projects: the SolidCraft designs (`.sc`), the STL files exported
from them, and a docs site that doubles as a gallery, where each model has a page with a 3D view
you can turn, its picture, its measurements and the files to download (Q&A answers 3, 4 and 6).
The projects are vibe coded: an agent builds most models and all the tooling, Dan prints them and
says what works. Others may print and adapt them, with credit, but not sell them (answer 15).

The first real project is a **grow-light rail**, made of wooden dowels and printed parts in a
Japandi style, in the corner of a room where a monstera and a rubber plant stand. A vertical dowel
rail hangs on the wall from two printed feet whose screws don't show. The light's arm, a second
dowel, rides on the rail in a sliding joint locked by a wedge, so its height adjusts and planters
can share the rail. Dan's Barrina 25 W grow bulb sits under a printed shade at the arm's tip, up to
24 inches (610 mm) from the wall (Phase 2 Q&A 1 to 3). It began as a sconce: an arm straight out of
one wall block, the light hanging by its cord from a clamp (answer 11). Phase 1 published those two
parts; Dan's changes, brought forward before anything was printed, made it the rail (Phase 2 Q&A
4). Dan's doubt, in his words: "not sure if it'll look good with 3d printed parts and dowels". His
reference is Lofted Goods' The Rail v2 and its Grow Light for the Rail, in his words: "each piece
slides into the rail and is held by a wedge piece, so it has a clean look. things then mount onto
the rail using some kind of matching joint piece. i'm hoping to have a lamp that looks like his
grow light setup but i need the light to reach out farther". The designs are original: those files
are members-only downloads with no stated licence, so none is copied, and the parts don't fit Lofted
Goods' pieces. They're published as soon as they're designed, in three dowel sizes, so others can
print them for their own dowels (answers 12 and 14).

**Success:** a visitor finds a model on the site, turns it in the viewer and downloads the STL for
their dowel; Dan adds a model by saving a `.sc`, writing its `model.yml` and running one command;
the rail holds the light, out of the way, and looks like it belongs in the room.

**Goals**

- One command, `make models`, turns every changed design into its STLs, picture and measurements.
- The site renders every model in a 3D viewer, with an STL per dowel size and the `.sc` to
  download.
- CI refuses a stale build, image metadata, a home-folder path and a leaked secret; and each push
  waits for the leak, privacy and model checks locally.
- A rail light that passes a 48-hour load test at three times the light's weight, its arm at 24
  inches, before it goes up.

**Non-goals**

- Slicer profiles or G-code: printers and slicers differ; each model page gives print settings in
  words.
- A store, accounts, comments or analytics on the site.
- Running SolidCraft in CI: it's a desktop app, so exported files are built on Dan's machine and
  committed (D2).

**Anti-goals** (it would fail even if it worked)

- Anything copied from Lofted Goods, or a page that looks like theirs.
- A photo that shows where Dan lives: no metadata, and Dan looks at each before it's staged
  (answer 5; D14).
- A light that looks printed-and-cheap: glossy plastic, bulky blocks, a screw, bolt or nut in
  sight from the room, a bare pink grow bulb (kickoff notes, *How it can look good*).
- A load-bearing part, or the shade, printed in PLA (it creeps under a constant load and softens
  near a warm bulb).

## How it's made

- **SolidCraft 0.30.1** designs every model. Agents build models headless with `solidcraft-cli`
  from a command script, then save the design; Dan opens the same `.sc` in the app (D3).
- **Designs are saved as plain-text JSON `.sc` files** (`file.save_as` with `format: json`,
  `cache: false`): a few KB each, readable in a diff, and scanned for leaks like any text (D2).
- **Built files are committed beside their design:** the STL (binary), one more STL per size the
  model lists, the picture (PNG), the measurements (`solidcraft-cli eval`'s JSON) and a build
  record holding the SHA-256 of the design and of every built file, the sizes and the CLI's
  version. Exporting the same design twice gives a byte-different STL, so freshness is judged by
  those hashes, never by rebuilding (D2).
- **Sizes:** a model's `model.yml` may list sizes as parameter changes (`3/4 in: {dowel_d:
  19.05 mm}`); `make models` exports an STL for each from the one design (answer 14).
- **Python 3.12 under uv**, as a uv project (`pyproject.toml`, `uv.lock`, `.python-version`):
  pytest for tests, ruff for lint, PyYAML and Pillow (D10).
- **The site is Quarto 1.11.6** in `website/`, on GitHub Pages at
  <https://chendaniely.github.io/3d-models/>, deployed by CI from `main`. The design docs reach it
  as copies with Quarto's syntax escaped, since the plans quote it in their listings (D13).
- **The viewer is three.js 0.187.0** (`STLLoader`, `OrbitControls`), served from the site itself,
  copied from npm's package and checked by SHA-256 (D15).
- **Licence:** CC BY-NC 4.0 for the models, their pictures and the docs; MIT for the code
  (answer 15).

### The repo's layout

```text
models/<slug>/
  model.yml           title, summary, status, material, size, sizes, print settings, notes
  <slug>.sc           the design (plain-text JSON), the source of truth
  <slug>.stl          built by make models; <slug>-<size>.stl for each extra size
  <slug>.png          built by make models
  <slug>.eval.json    built by make models: bodies, bounding box, volume, mass, parameters
  build.json          built by make models: every file's sha256, the sizes, the CLI's version
  photos/             optional: prints and installs, stripped and looked at first
scripts/models.py     build | check
scripts/privacy.py    check | strip: image metadata, unreadable formats, home-folder paths
scripts/sitedocs.py   the design docs copied into the site, Quarto's syntax escaped
scripts/gallery.py    the model pages
website/              the Quarto site; website/superpowers/ and website/models/ are generated
tests/                pytest
```

### The commands

| Target | What it does |
|---|---|
| `make models` | rebuilds each model whose design, sizes or built files differ from its `build.json` (needs SolidCraft) |
| `make models-check` | fails, naming each model, when a build is missing or stale, or the model is invalid: a folder name that can't be a URL, no design or a misnamed one, a `model.yml` or sizes it can't read, sizes giving one file name or none, a size changing a parameter the design hasn't |
| `make privacy` | fails, naming each file, on image metadata (a chunk the picture doesn't need, or bytes after its end, included), a photo format it can't read inside, or a home-folder path, in anything git would commit and in every file the history holds; fails in a shallow clone; `make strip` fixes an image |
| `make strip FILES=…` | rewrites each JPEG, PNG or WebP named upright, with no metadata but its colour profile; then you look at it |
| `make leaks` | gitleaks over every commit, merges included |
| `make test`, `make test-utc`, `make lint` | pytest; pytest under `TZ=UTC`; ruff check and format check |
| `make docs` | copies the docs, writes the model pages, renders the site, fails on an unresolved link or anything it loads from another host, runs lychee where installed |
| `make check` | test, test-utc, lint, models-check, privacy, leaks, docs |
| `make hooks` | installs nothing: no hooks yet |
| `make help` | lists the targets |

While the repo has no hooks, every push waits for `make leaks privacy models-check` to pass, and
for Dan's OK unless Dan gives a standing OK, as he did for Phase 1's end (Phase 1 Q&A 5;
`AGENTS.md`).

### The site

Home (the README, then the overview diagram), **Models** (a card per model: picture, title,
summary), one page per model (the 3D viewer, the picture, notes, photos, print settings,
measurements, parameters, a download per size with a note on which parameters to change, the
licence), Architecture (every diagram), Design (the spec, plans, Q&A pages and council reports),
Changelog, and How we work (`AGENTS.md`). Diagrams by link only:
[Architecture](https://chendaniely.github.io/3d-models/architecture.html).

## Outline

| Phase | Goal | Done means |
|---|---|---|
| 1: the repo and the first models | the pipeline from design to gallery, guarded by CI, with the coupon and the sconce's parts designed | the live site turns the coupon, the wall block and the cord clamp in 3D and downloads each in three sizes; CI runs every check |
| 2: the grow-light rail | the rail's parts designed from Dan's answers, sized to his measurements, judged by eye, proven by a load test at 24 inches, and installed | the rail and the light are on the wall after a passed load test, the parts' pages saying so; Phase 1's wall block and cord clamp are marked superseded |

### The rail's design calls

Dan's answers (Phase 2 Q&A 1 to 4) are marked with their number; every other call is the agent's,
for Dan to approve with this revision, and each can be revisited at the look test. The rough
concept they describe was drawn for Dan on 2026-11-06, before this revision; the plan's parts
replace it.

- **The parts** (the agent's): five models under `models/`: `rail-feet` (both feet and their two
  caps, printed together), `rail-carrier`, `rail-arm-socket`, `rail-arm-tip` (with three cord
  clips) and `rail-shade`; each wedge, the caps and the clips are bodies in their part's design,
  as the wall block's caps are.
- **The rail** (Q&A 1, 5): a vertical dowel, its length Dan's cut, up to about 48 inches, held at
  each end by a wall foot; it carries the light's arm and up to two small planters, about 2 kg
  each when watered.
- **The wall feet** (the agent's; ruled at the phase start, Phase 2 Q&A, decided without Dan 1): a
  closed cup over each end of the rail; a bridge standing the rail 32 mm off the wall, far enough
  for the cord behind it. Each foot is screwed through its plate where the rail, once in, stands in
  front of the screw, and a printed cap covers the head, since the rail hides it only from straight
  in front. The top cup is deep, so the rail lifts into it past the bottom cup's rim; a screw up
  through the bottom cup's floor into the rail's end then holds it down, so lifting a carrier, the
  arm or a planter can't raise it (S32), and it can't turn. The screws are the wall block's (D16):
  #8 or #10 pan-head wood screws into a stud, or 3/16-inch toggle bolts. A groove up the bottom
  foot's back holds the cord. Sized for the light and two small planters (Q&A 5).
- **The rail carrier** (Q&A 1; its shape the agent's): a C-shaped sleeve open toward the wall,
  pushed onto the rail from the front while the rail is up, so pieces can be added or moved
  without taking the rail down; a wedge pushed up from below into the open back, between the rail
  and the sleeve, locks it, out of sight. Its face carries a dovetail running up and down. Long
  enough to hold the arm at 24 inches without slipping or rocking (S13, S29). Its arms stop 1.5 mm
  short of the wall, and a 3 mm felt or rubber pad on each bears on it, so a sideways bump at the
  light doesn't turn the arm round the rail (S14); a gap of 0.3 mm with no pad would let a real
  wall's unevenness turn it (the phase-start council). The wedge prints flat, so the rail bends it
  along its layers. If a wedge can't hold a C-shape, the carrier slides on from the rail's end
  before the rail goes up, a ruling logged on Phase 2's Q&A page.
- **The arm socket** (Q&A 1's "matching joint piece"; its shape the agent's): slides down onto the
  carrier's dovetail, so the same carrier can take a planter adapter later (S16); holds the arm
  level in a socket at least 51 mm deep, locked by its own wedge, so no bolt shows. Every wedge
  seats inside its part on a dowel half a millimetre over or under (S28).
- **The arm** (Q&A 2): a second dowel of the rail's size, the light's centre up to 24 inches
  (610 mm) from the wall. With a 1 kg light, a 1-inch arm sags about 8 mm at 24 inches over time
  (D5's 4.5 mm at 20 inches, times 1.73), and the rail, bending between its feet, adds 2 to 5 mm
  at the light; the load test measures what the printed joints add on their own (S13).
- **The arm tip and the shade** (Q&A 3; their shape the agent's): a cap on the arm's end with a
  stem down to a shade fixed under it: the shade's top turns onto two lugs at the stem's foot, and
  the lamp hangs inside it on its own cord, which a short band in the stem grips (S27). A cone
  round the socket widens to a cylinder round the bulb, so the shade's wall is at least 10 mm from
  the lamp everywhere; vents at its top. Its size waits on Dan's measurement of the socket and the
  bulb. If the bulb's hottest surface is over 60 °C after an hour on, the gap grows or the
  material changes, decided with Dan.
- **The cord** (the agent's): from the socket up the stem, along the arm's underside in printed
  clips, round the joint and down behind the rail, held by the bottom foot's groove. It is pressed
  in from the side everywhere it goes, since its plug and timer won't pass a hole.
- **No hardware in sight:** from the room, no screw, bolt or nut shows (the anti-goal).
- **Sizes and fit:** every part saved at 1 inch (25.4 mm), with STLs for 3/4 inch and 25 mm
  (answer 14); `dowel_d` and `clearance` parameters in each; `clearance` is the coupon's hole that
  fit (S26), and each wedge is sized from it.
- **A look test first** (D8): every part printed in PLA and held up with the rail, the arm and the
  light, before any PETG print (S11); rounded edges wait for its verdict (D18, S22).
- **PETG, matte,** for every load-bearing part and the shade (D9; Q&A 3); each part printed so its
  layers run along its load.
- **Phase 1's wall block and cord clamp** (Q&A 4): kept in the repo, their status `superseded`,
  their pages pointing at the rail's parts.

## Scenarios

| ID | Situation | Expected | Phase and task | Proof | Status |
|---|---|---|---|---|---|
| S01 | Dan saves a new or changed `.sc` under `models/<slug>/` and runs `make models` | its STLs, picture, measurements and build record appear beside it; unchanged models are left alone | Phase 1, Task 2 | `tests/test_models.py` | built |
| S02 | a design changes and `make models` isn't run, or a built file isn't the one recorded | `make check` and CI fail, naming the model and why | Phase 1, Task 2 | `tests/test_models.py` | built |
| S03 | an image with any metadata but a colour profile, or a HEIC, video or RAW file, is added anywhere in the repo, or is still in a commit the history holds | `make privacy` fails, naming it, before the push it would go out in, the history's copies included; `make strip` fixes a JPEG, PNG or WebP | Phase 1, Task 3; Phase 2, Task 1 | `tests/test_privacy.py` | built |
| S04 | a commit carries a secret | `make leaks` and CI's leaks job fail, merge commits included | Phase 1, Task 1 | CI's `leaks` job | built |
| S05 | a push to `phase-1` | CI runs the tests, lint, the model and privacy checks, the leak scan and the site's render and offline link check | Phase 1, Tasks 1 to 4 | a green CI run | built |
| S06 | a doc under `docs/superpowers/` quotes Quarto's syntax, or isn't on the Design page | it renders as text; a doc missing from the Design page fails `make check` | Phase 1, Task 4 | `tests/test_site.py` | built |
| S07 | a visitor opens the site's Models page | a card per model, with its picture, title and summary, linking to its page | Phase 1, Task 5 | `tests/test_gallery.py` | built |
| S08 | a visitor opens a model's page | the STL turns in a 3D viewer (drag to rotate, scroll to zoom); the picture, notes, photos, measurements and print settings are there; the files download | Phase 1, Task 5 | `tests/test_gallery.py`; the live page checked in a browser after the merge (Phase 1, Task 10, step 9) | built |
| S09 | Dan is about to print the coupon (Phase 1's part; printing it is S26) | each hole is marked by its clearance in dots, and the page says how to print it and read the result | Phase 1, Task 6 | `tests/test_coupon.py` | built |
| S10 | `main` gets a merge | CI deploys the site to Pages | Phase 1, Task 10, step 9 | the live URL serves the new build | built |
| S11 | Dan holds the PLA look-test parts up in the corner: the feet on the rail, the carrier and arm socket on it, the arm, the shade and the light | he decides whether it looks right, before any PETG is printed; nothing but the dowels and the parts shows | Phase 2, Task 11 | Dan's verdict on Phase 2's Q&A page | planned |
| S12 | the wall block's parameters change | the socket stays at least 51 mm deep, the screws at least 100 mm apart and sunk under caps, the clearance one of the coupon's | Phase 1, Task 7; Phase 2, Task 7 | `tests/test_wall_block.py` | superseded (Phase 2 Q&A 4): Phase 1's part, kept |
| S13 | the PETG rail parts hold for 48 hours, mounted as they will be: the arm at 24 inches with three times the light's weight at its tip, and a second carrier with 12 kg hung from it (three times two watered small planters) | the arm's tilt at its socket adds under 1 mm at the tip, neither carrier slips 2 mm on the rail, the tip's total sag, the wood's creep included, grows by under 5 mm, and nothing cracks or pulls out | Phase 2, Task 12 | the load-test log on the parts' pages | planned |
| S14 | the rail light is installed and bumped | the arm doesn't turn on the rail or droop, the feet stay on their screws, and the cord runs along the arm and down behind the rail | Phase 2, Task 13 | Dan's check, with a photo he has looked at | planned |
| S18 | the cord clamp is designed to hold the light by its cord (Phase 1's part; the two days' hang is S27) | the slot and the hole are narrower than the cord, so it grips, and the cord has room to pass under the dowel to its hole | Phase 1, Task 8; Phase 2, Task 7 | `tests/test_cord_clamp.py` | superseded (Phase 2 Q&A 4): Phase 1's part, kept |
| S19 | someone with a 3/4-inch or 25 mm dowel opens a dowel part's page | an STL for their size, and a note on which parameters to change for any other | Phase 1, Tasks 2, 5 to 8 | `tests/test_models.py`, `tests/test_gallery.py` | built |
| S20 | someone downloads a model | the page says it's CC BY-NC 4.0: print, adapt and share with credit, not for sale | Phase 1, Task 5 | `tests/test_gallery.py` | built |
| S21 | a file holding a home-folder path is about to be committed | `make privacy` names the file and line, never the path | Phase 1, Task 3 | `tests/test_privacy.py` | built |
| S26 | Dan prints the coupon on its edge and tries his dowel in each hole (S09's Phase 2 part) | the hole his dowel goes into by hand, all the way, gives the dowel parts' `clearance` | Phase 2, Task 9 | his result on Phase 2's Q&A page | planned |
| S27 | the light hangs by its cord from the arm tip's stem for 48 hours, three times its weight (ruled at the phase start: the stem's grip is a cord clamp; Phase 2 Q&A, decided without Dan 2) | the cord slips under 2 mm at its mark | Phase 2, Task 12 | the load test's slip measurements | planned |
| S28 | a rail part is built at 3/4 inch, 25 mm or 1 inch | each cup and socket takes its dowel with the coupon's clearance, the carrier's open back takes the rail, its wedge fills the gap, the arm's socket is at least 51 mm deep, and each wedge seats inside on a dowel 0.5 mm over or under | Phase 2, Tasks 2 to 5 | the parts' tests | planned |
| S29 | Dan pushes the carrier onto the mounted rail, slides the arm socket down its dovetail and pushes both wedges in | the joint doesn't slide or turn by hand, comes apart when the wedges are tapped out, and no bolt or screw shows | Phase 2, Task 11 | Dan's check on Phase 2's Q&A page | planned |
| S30 | the light runs for 14 hours, the timer's longest, inside the PETG shade | the shade doesn't soften, warp or discolour, and is nowhere hotter than 60 °C | Phase 2, Tasks 9 and 12 | the temperatures in the load-test log | planned |
| S31 | a visitor opens any page of the site | their browser fetches nothing from another host: no web font, script or style sheet | Phase 2, Task 1 | `tests/test_offsite.py`; `make docs` | built |
| S32 | someone lifts a carrier, the arm or a planter on the mounted rail | the rail doesn't rise, and both feet stay on the wall | Phase 2, Tasks 2 and 13 | `tests/test_rail_feet.py` (the floor's screw); Dan's check at the install | planned |

### Later

| ID | Situation | Expected | Kind | Why it waits |
|---|---|---|---|---|
| S15 | the load test fails, or the sag looks wrong | a knee-brace kit: a diagonal dowel meeting the arm about 12 inches out | optional | only needed if the straight arm fails (D6) |
| S16 | Dan wants a wall planter or a second arm on the rail | a planter adapter or a second arm socket slides onto a rail carrier's dovetail | optional | after the rail proves the joint |
| S17 | Dan saves a design from the app in its default zip format | `make models-check` warns, so designs stay plain text | optional | the first app-saved design shows whether it's needed |
| S22 | the look test calls the square edges cheap | every visible edge rounded to one radius, a parameter | optional | a fillet picked by its edge's position may break the size exports; the look test decides (D18) |
| S23 | a visitor opens a model's page | the viewer frames the whole model to fit; today its first view crops the cord clamp's bottom edge | optional | a cosmetic crop (Phase 1 end council, goal fit 5) |
| S24 | a build runs on another CLI version or hangs, or the history grows large | a warning when `build.json`'s CLI version isn't the one installed, a timeout on each CLI call, and a history scan that streams its blobs | optional | today's size and one machine (reliability 9, 10) |
| S25 | a home-folder path reaches a commit or tag message, a symlink's blob sits in the history, or an image and a text path share one blob | commit and tag messages scanned for home paths, a symlink's blob told apart from a file's, and each path of a shared blob checked as its kind | optional | no hits today, and contrived (security 2; the phase-end list's b and e) |

## Open items and risks

- **[Dan] The light's weight, its cord and the wall.** The numbers assume 1 kg; one listing gives
  the Barrina kit, cord and timer included, as 1.7 lb (0.77 kg). The clamp's `cord_d` is a 6 mm
  guess, and the cord may be flat. Phase 2's measuring task (Task 9) asks.
- **[Dan] SolidCraft's save folder:** add this repo to the SolidCraft MCP server's `--allow-path`
  so live sessions can save here. Headless builds don't need it.
- **[Dan] The bulb:** its diameter, height and socket, its weight with its cord and timer, and its
  hottest surface after an hour on; the shade's size and the load test wait on them (Phase 2's
  measuring task, Task 9). His changes to the parts are settled (Phase 2 Q&A 1 to 4).
- **[Dan] His commits' author address:** the commits carry his personal email, public in the
  history; a GitHub noreply address would keep it out of future commits (Phase 1 end council,
  security 4).
- **[Dan] Dependabot's security updates:** off, while its version updates are on; turning them
  on is a repo setting outside the five he OKed (Phase 1 Q&A 6; Phase 1 end council, security
  5).
- **GitHub settings:** applied in Phase 1's Task 9, with Dan's OK (Phase 1 Q&A 6): Pages from
  GitHub Actions, Actions limited and SHA-pinned, merge commits only, a ruleset on `main`.
- **Binary files can't be leak-scanned:** STL and PNG files are listed in each phase PR for Dan to
  check by eye, so a PR that adds them waits for him even though the mode is fully vibed. Ruling:
  Dan looked at and OKed each binary file by name when it was pushed (Phase 1 Q&A 2 and 3), so the
  wait for his look at a PR's binaries is met for Phase 1; a phase-end step that adds a new binary
  would need his look again.
- **No hooks yet:** plan-driven-development's hooks and leak check aren't built, so every push waits
  for `make leaks privacy models-check` to pass, and for Dan's OK unless Dan gives a standing OK,
  as he did for Phase 1's end (Phase 1 Q&A 5).
- **lychee runs in CI only:** it isn't installed on Dan's machine, and running a downloaded copy
  was refused in this session; installing it locally is Dan's call (Phase 1's phase-end list).
- **The parts are untested designs** until Phase 2's look and load tests; their pages say so.
- **Prior work outside this repo:** a PythonSCAD grow-light stand from 2026-10-16 in Dan's
  `~/temp/pythonscad_lamp`; not used here, but worth a look at Phase 2's start.

## Revisions

- 2026-11-05: one repo for every 3D-print project, named `3d-models`, public, with the docs site as
  the gallery; GitHub created by the agent (Q&A answers 3 to 7, `68ce9ac`).
- 2026-11-05: everything reaches `main` through Phase 1's PR; the mode is fully vibed (Q&A answers 9
  and 10, `76c6b8c`, `6e0bf3e`).
- 2026-11-05: the light hangs from a printed clamp on the dowel, holding its cord, in place of an end
  cap (Q&A answer 11, `88bc417`).
- 2026-11-05: the dowel parts are designed in Phase 1 and published with a dowel-size parameter;
  the test GPS values replaced before any push (Q&A answers 12 and 13, `0abe755`).
- 2026-11-05: ready-made STLs for 3/4 inch, 25 mm and 1 inch (Q&A answer 14, `351878b`).
- 2026-11-05: CC BY-NC 4.0 for the models, pictures and docs, MIT for the code (Q&A answer 15,
  `647e01f`).
- 2026-11-05: the spec and both plans approved as written (Q&A answer 16).
- 2026-11-05: Dan's changes to the wall block and the cord clamp wait for the PLA look test, in
  Phase 2; a standing push OK, and the merge, for Phase 1's end (Phase 1 Q&A 4 and 5, `9e47ad4`).
- 2026-11-05: the GitHub settings applied by the agent (Phase 1 Q&A 6, `c0fec70`).
- 2026-11-06: the sconce becomes a grow-light rail: a vertical rail on two wall feet with hidden
  screws, the arm on a sliding joint locked by a wedge, the light up to 24 inches out under a PETG
  shade, designed now in Phase 2; Phase 1's two parts kept, superseded (Phase 2 Q&A 1 to 4,
  `684a776` to `09a9f55`).
- 2026-11-06: the rail carries two small planters too, up to about 48 inches long; the load test
  judges what the printed parts add (the arm's tilt at its socket, the carriers' slip) and gives
  the tip's total sag a looser 5 mm, after the builder check found the wood's own creep could use
  up a 3 mm limit (Phase 2 Q&A 5).
- 2026-11-06: the revision approved as written (Phase 2 Q&A 6).
- 2026-11-06: everything on `phase-2` merged to `main` mid-phase, so Dan can see it rendered (Phase 2
  Q&A 8, `4e15845`; #2).
- 2026-11-06: the rail's parts are built at placeholder sizes and published first, then retuned to
  Dan's measurements and published again (Phase 2 Q&A 9).
