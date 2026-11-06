# 3d-models Phase 2: the wall sconce, implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking. The project's `AGENTS.md` holds every rule for running
> it and outranks this header where they differ. **This plan is revised at Phase 2's start**
> against the code Phase 1 built (`AGENTS.md`, *Resume*; the skill's phase start), its listings
> run first.

**Goal:** a grow-light sconce for the plant corner, a 1-inch dowel cantilevered 16 to 20 inches
from the wall, holding Dan's Barrina grow light from a printed cord clamp, proven by a load test
before it goes up.

**Architecture:** two printed parts, each a model under `models/` built by Phase 1's pipeline: the
wall block (a plate for two screws and a 54 mm socket, pinned through the dowel) and the cord clamp
(a split ring on the dowel with a shelf the light's cord hangs from). Dan's steps (measuring,
printing, the look test, the load test, the install) are [Dan] tasks whose answers set the parts'
parameters and fill their pages.

**Tech Stack:** Phase 1's: solidcraft-cli 0.30.1, `make models`, the gallery; PETG and PLA prints;
a 1-inch hardwood dowel, an M4 bolt and nut, two #8 wood screws or toggle anchors, a 1/4-inch
steel pin.

**Spec:** `docs/superpowers/specs/2026-11-05-3d-models-design.md`

**Now:** Task 1: [Dan] Measure, weigh, and print the coupon, open.

***

## Global Constraints

- Every Phase 1 constraint holds (its plan's *Global Constraints*).
- The dowel is 1 inch (25.4 mm) (D5); the arm is a straight cantilever (D6), 16 to 20 inches
  (406 to 508 mm) out.
- The wall block's socket is at least 51 mm deep; its screws at least 100 mm apart; screws go
  into a stud or toggle anchors, never plastic plugs.
- Load-bearing parts are PETG, matte, never PLA (D9); PLA only for the look test (D8).
- The socket's `clearance` is the coupon's `step` times the dots of the hole that fit.
- Photos are stripped with `scripts/photos.py strip` before they're staged.

## Review Focus

1. **A cord thicker than the clamp's slot by more than about 1.5 mm:** the cord won't press in;
   `cord_d` is set from Dan's measurement before printing (Task 3's design step), and the test
   pins `slot_w < cord_d`.
2. **A dowel thinner than 1 inch** (a metric 25 mm dowel): the coupon's holes are all too loose;
   Task 1's answer records the dowel's measured diameter, and `dowel_d` follows it in both parts.
3. **Drywall with no stud where the block goes:** toggle anchors, never plugs (the wall block's
   page says so, and Task 6's steps).
4. **The bulb's heat at the clamp:** the clamp sits on the dowel above the cord, not at the bulb;
   PETG either way.
5. **The light's weight on a long cord swinging:** the shelf's hole is under the dowel's axis, so
   a bump swings the light, not the clamp (S14, S18).

***

### Task 1: [Dan] Measure, weigh, and print the coupon

**Tier:** none: Dan's measurements, recorded by the agent (Tier 3) · **Scenarios:** S09, S12, S18

Runs in Dan's home. **Now** reads `waiting on Dan: <the step>` until each answer is in. The steps
are asked by *Asking Dan*, one at a time.

- [ ] **1. Weigh the light:** the Barrina bulb with its socket, cord and timer, on a kitchen
  scale. The numbers assume 1 kg; above that, the agent re-runs the kickoff notes' sag and anchor
  numbers before Task 2.
- [ ] **2. Measure the cord** with calipers, just above the bulb: its diameter sets the clamp's
  `cord_d`.
- [ ] **3. Measure the dowel** with calipers, in two places: its diameter sets `dowel_d` if it
  isn't 25.4 mm.
- [ ] **4. Print the fit-test coupon** (Phase 1's model, its page's print settings) and try the
  dowel in each hole: which hole, by its dots, is the tightest it goes into by hand?
- [ ] **5. The corner:** where the block goes (height, and distance from the corner), the wall
  (drywall, plaster or other), and whether a stud is there.
- [ ] **6. Record and close.** Each answer goes on the Phase 2 Q&A page, `docs/superpowers/plans/2026-11-05-3d-models-phase-2-qa.md`, in Dan's words, committed as `docs(plan): 🤖 record <what>` with this plan's `Plan: … Task 1` line; the page gets its wrapper and Design-page line in its first commit. Then the close:

  The close, its own commit (`AGENTS.md`, *Each task's loop*, step 6), its message from
  `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 1: [Dan] Measure, weigh, and print the coupon

    <what the task built, and why, in a few lines>

    Drift: <filled at the close, or none>
    Rulings: <filled at the close, or none>
    Phase-end: <filled at the close, or none>
    Forward: <filled at the close, or none>
    Tier: 3
    Rounds: <filled at the close>
    Findings: <filled at the close, or none>

    Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 1
    Co-Authored-By: <the model's own line>
    ```

  Push once Dan has OKed it: `make leaks`, then `git push origin phase-2`.

***

### Task 2: The wall block

**Tier:** 2 · **Scenarios:** S12

**Files:**
- Create: `models/sconce-wall-block/sconce-wall-block.sc` (by SolidCraft), its built files (by
  `make models`), `models/sconce-wall-block/model.yml`, `tests/test_wall_block.py`

**Interfaces:**
- Consumes: Phase 1's `make models`, `models.Model`, `models.staleness`, `gallery.read_meta`;
  Task 1's answers (the clearance, the dowel's diameter).
- Produces: the design's parameters `dowel_d`, `clearance`, `socket_depth` (54 mm),
  `boss_wall`, `plate_t`, `plate_w`, `screw_spacing` (110 mm), `plate_h`, `screw_d`, `pin_d`,
  `socket_d`, `boss_d`; Task 3's clamp uses the same `dowel_d`.

- [ ] **Step 0: Record the base:** `git rev-parse HEAD > .git/TASK_BASE`.
- [ ] **Step 1: Write the failing tests.**

`tests/test_wall_block.py`:

```python
"""The sconce's wall block (S12): a socket deep enough, screws far enough apart."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import gallery
import models

ROOT = Path(__file__).resolve().parent.parent
WALL_BLOCK = models.Model(ROOT / "models" / "sconce-wall-block")


def params(model: models.Model) -> dict[str, float]:
    evaluation = json.loads(model.built("eval.json").read_text(encoding="utf-8"))
    return {p["name"]: p["value"] for p in evaluation["params"]}


def body(model: models.Model) -> dict:
    evaluation = json.loads(model.built("eval.json").read_text(encoding="utf-8"))
    (only,) = evaluation["bodies"]
    return only


def test_it_is_built_from_its_design_as_one_closed_body() -> None:
    assert models.staleness(WALL_BLOCK) is None
    assert body(WALL_BLOCK)["closed"]
    gallery.read_meta(WALL_BLOCK)


def test_it_fits_a_one_inch_dowel() -> None:
    assert params(WALL_BLOCK)["dowel_d"] == pytest.approx(25.4)


def test_the_wall_block_socket_is_at_least_two_inches_deep() -> None:
    assert params(WALL_BLOCK)["socket_depth"] >= 51.0


def test_the_wall_block_screws_are_at_least_100_mm_apart() -> None:
    p = params(WALL_BLOCK)
    assert p["screw_spacing"] >= 100.0
    assert p["plate_h"] > p["screw_spacing"] + p["screw_d"]


def test_the_wall_block_socket_takes_the_coupons_clearance() -> None:
    p = params(WALL_BLOCK)
    assert p["socket_d"] == pytest.approx(p["dowel_d"] + p["clearance"])
    assert any(p["clearance"] == pytest.approx(hole) for hole in (0.2, 0.4, 0.6, 0.8))


def test_the_wall_block_reaches_its_socket_depth_out_from_the_wall() -> None:
    p = params(WALL_BLOCK)
    size_x = body(WALL_BLOCK)["bbox"]["max"][0] - body(WALL_BLOCK)["bbox"]["min"][0]
    assert size_x == pytest.approx(p["plate_t"] + p["socket_depth"])
```

- [ ] **Step 2: Run them; watch them fail.** `make test`. Expected: `FileNotFoundError` for
  `models/sconce-wall-block/sconce-wall-block.eval.json`.
- [ ] **Step 3: Build the design.** Write the command script to `.git/wall-block-script.json`,
  with `clearance` set to the coupon's answer (`0.2 mm` times the dots) and `dowel_d` to the
  dowel's measured diameter if Task 1 found it isn't 25.4 mm:

```json
{
  "commands": [
    {"command": "parameters.add", "params": {"name": "dowel_d", "expression": "25.4 mm", "comment": "the arm's dowel: 1 inch"}},
    {"command": "parameters.add", "params": {"name": "clearance", "expression": "0.4 mm", "comment": "from the fit-test coupon: step times the dots of the hole that fit"}},
    {"command": "parameters.add", "params": {"name": "socket_depth", "expression": "54 mm", "comment": "at least 51 mm (2 inches), so the joint carries the arm's moment"}},
    {"command": "parameters.add", "params": {"name": "boss_wall", "expression": "6 mm", "comment": "plastic around the socket"}},
    {"command": "parameters.add", "params": {"name": "plate_t", "expression": "8 mm", "comment": "the wall plate's thickness, behind the socket"}},
    {"command": "parameters.add", "params": {"name": "plate_w", "expression": "50 mm", "comment": "the wall plate's width"}},
    {"command": "parameters.add", "params": {"name": "screw_spacing", "expression": "110 mm", "comment": "at least 100 mm between the two screws, so the top one pulls under 54 N"}},
    {"command": "parameters.add", "params": {"name": "plate_h", "expression": "screw_spacing + 30 mm", "comment": "the wall plate's height"}},
    {"command": "parameters.add", "params": {"name": "screw_d", "expression": "4.5 mm", "comment": "clearance for a #8 or 4 mm wood screw"}},
    {"command": "parameters.add", "params": {"name": "pin_d", "expression": "6.6 mm", "comment": "clearance for a 1/4 inch steel pin through boss and dowel"}},
    {"command": "parameters.add", "params": {"name": "socket_d", "expression": "dowel_d + clearance", "comment": "the socket's diameter"}},
    {"command": "parameters.add", "params": {"name": "boss_d", "expression": "socket_d + 2 * boss_wall", "comment": "the boss around the socket"}},
    {"command": "solid.box", "params": {"length": "plate_t", "width": "plate_w", "height": "plate_h", "corner": [0, "-plate_w / 2", "-plate_h / 2"], "body_name": "Wall block"}},
    {"command": "solid.cylinder", "params": {"diameter": "boss_d", "height": "plate_t + socket_depth", "base": [0, 0, 0], "axis": "X", "body_name": "Boss"}},
    {"command": "solid.combine", "params": {"target": "Wall block", "tools": ["Boss"], "operation": "join"}},
    {"command": "solid.cylinder", "params": {"diameter": "socket_d", "height": "socket_depth", "base": ["plate_t", 0, 0], "axis": "X", "body_name": "Socket"}},
    {"command": "solid.cylinder", "params": {"diameter": "pin_d", "height": "boss_d + 2 mm", "base": ["plate_t + socket_depth / 2", 0, "-boss_d / 2 - 1 mm"], "axis": "Z", "body_name": "Pin hole"}},
    {"command": "solid.cylinder", "params": {"diameter": "screw_d", "height": "plate_t", "base": [0, 0, "screw_spacing / 2"], "axis": "X", "body_name": "Top screw"}},
    {"command": "solid.cylinder", "params": {"diameter": "screw_d", "height": "plate_t", "base": [0, 0, "-screw_spacing / 2"], "axis": "X", "body_name": "Bottom screw"}},
    {"command": "solid.combine", "params": {"target": "Wall block", "tools": ["Socket", "Pin hole", "Top screw", "Bottom screw"], "operation": "cut"}},
    {"command": "file.save_as", "params": {"path": "models/sconce-wall-block/sconce-wall-block.sc", "format": "json", "cache": false}}
  ]
}
```

  Then `mkdir -p models/sconce-wall-block`,
  `solidcraft-cli run .git/wall-block-script.json --quiet` (exit 0), and `make models`. Expected:
  `building models/sconce-wall-block (missing …)`. Look at the picture: a plate with two screw
  holes, a boss with the socket and the pin hole.
- [ ] **Step 4: Write its page's text.**

`models/sconce-wall-block/model.yml`:

```yaml
title: Sconce wall block
summary: >-
  The wall end of the grow-light sconce: a plate for two screws and a deep socket that holds a
  1-inch dowel straight out from the wall, pinned through.
status: designed
material: PETG, matte (never PLA for this part)
print:
  Orientation: on its side, the socket horizontal, so the layers run along it
  Layer height: 0.2 mm
  Walls: 5
  Infill: 40% gyroid
  Supports: under the socket's mouth only
notes: |
  The arm is a straight cantilever: a 1-inch dowel, up to 20 inches long, with the light hanging
  near its end. The socket is 54 mm deep, more than the 51 mm (2 inches) the joint needs to carry
  the arm's bending moment, about 5 N·m with a 1 kg lamp at 20 inches.

  - **Screws:** two #8 or 4 mm wood screws, 110 mm apart, into a stud; or toggle anchors in
    drywall. Never plastic plugs: the top screw is pulled out with about 50 N.
  - **Pin:** a 1/4-inch steel pin through the boss and the dowel, drilled through the pin hole
    once the dowel is seated.
  - **Clearance:** the socket is the dowel plus `clearance`, taken from the fit-test coupon.
```

- [ ] **Step 5: Run the checks; they pass.** `make check`.
- [ ] **Step 6: Commit.** Write the message to `.git/COMMIT_MSG`:

```text
feat(models): 🤖 add the sconce's wall block

The sconce's arm needs a wall joint that carries about 5 N·m. The wall
block is a plate for two screws 110 mm apart and a boss with a 54 mm
socket, deeper than the 2 inches the joint needs, sized to the dowel plus
the clearance the coupon picked, with a pin hole for a 1/4-inch steel pin
through the dowel. Every dimension is a parameter; the tests hold the
socket's depth, the screws' spacing and the clearance to the spec.

The new tests failed first with: FileNotFoundError for
models/sconce-wall-block/sconce-wall-block.eval.json.

Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 2
Co-Authored-By: <the model's own line>
```

  `git add models/sconce-wall-block tests/test_wall_block.py`, then `git commit -F .git/COMMIT_MSG`, then `git log -1 --format='%(trailers)'` shows the `Plan:` line.
- [ ] **Step 7: Review, look forward, close.** Tier 2: Matt Pocock's `code-review`, two axes in two subagents; fix Critical and Important; at most one re-review, from `$(cat .git/TASK_BASE)`, with the
  picture and the page's viewer looked at. Forward: Task 4 prints this design.

  The close, its own commit (`AGENTS.md`, *Each task's loop*, step 6), its message from
  `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 2: The wall block

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

  Push once Dan has OKed it: `make leaks`, then `git push origin phase-2`.

***

### Task 3: The cord clamp

**Tier:** 2 · **Scenarios:** S18

**Files:**
- Create: `models/sconce-cord-clamp/sconce-cord-clamp.sc` (by SolidCraft), its built files,
  `models/sconce-cord-clamp/model.yml`, `tests/test_cord_clamp.py`

**Interfaces:**
- Consumes: Phase 1's pipeline; Task 1's cord diameter; Task 2's `dowel_d`.
- Produces: the design's parameters `dowel_d`, `clearance` (0.2 mm: the bolt closes the split),
  `ring_wall`, `ring_len`, `split`, `ear_t`, `ear_h`, `bolt_d` (M4), `shelf_len`, `shelf_w`,
  `shelf_t`, `under_gap`, `cord_d`, `slot_w` (`cord_d - 1 mm`), `bore_d`, `ring_d`.

- [ ] **Step 0: Record the base:** `git rev-parse HEAD > .git/TASK_BASE`.
- [ ] **Step 1: Write the failing tests.**

`tests/test_cord_clamp.py`:

```python
"""The sconce's cord clamp (S18): it grips the dowel and the cord, and clears the dowel."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import gallery
import models

ROOT = Path(__file__).resolve().parent.parent
CORD_CLAMP = models.Model(ROOT / "models" / "sconce-cord-clamp")


def params(model: models.Model) -> dict[str, float]:
    evaluation = json.loads(model.built("eval.json").read_text(encoding="utf-8"))
    return {p["name"]: p["value"] for p in evaluation["params"]}


def body(model: models.Model) -> dict:
    evaluation = json.loads(model.built("eval.json").read_text(encoding="utf-8"))
    (only,) = evaluation["bodies"]
    return only


def test_it_is_built_from_its_design_as_one_closed_body() -> None:
    assert models.staleness(CORD_CLAMP) is None
    assert body(CORD_CLAMP)["closed"]
    gallery.read_meta(CORD_CLAMP)


def test_it_fits_a_one_inch_dowel() -> None:
    assert params(CORD_CLAMP)["dowel_d"] == pytest.approx(25.4)


def test_the_cord_slot_is_narrower_than_the_cord_so_it_grips() -> None:
    p = params(CORD_CLAMP)
    assert p["slot_w"] < p["cord_d"]


def test_the_cord_shelf_clears_the_dowel_beyond_the_ring() -> None:
    p = params(CORD_CLAMP)
    assert p["under_gap"] > 0
    lowest = body(CORD_CLAMP)["bbox"]["min"][2]
    assert lowest == pytest.approx(-(p["dowel_d"] / 2 + p["under_gap"] + p["shelf_t"]))
```

- [ ] **Step 2: Run them; watch them fail.** `make test`. Expected: `FileNotFoundError` for
  `models/sconce-cord-clamp/sconce-cord-clamp.eval.json`.
- [ ] **Step 3: Build the design.** Write the command script to `.git/cord-clamp-script.json`,
  with `cord_d` set to Task 1's measured cord diameter (and `dowel_d` as Task 2 set it):

```json
{
  "commands": [
    {"command": "parameters.add", "params": {"name": "dowel_d", "expression": "25.4 mm", "comment": "the arm's dowel: 1 inch"}},
    {"command": "parameters.add", "params": {"name": "clearance", "expression": "0.2 mm", "comment": "a snug slide; the bolt closes the split to grip"}},
    {"command": "parameters.add", "params": {"name": "ring_wall", "expression": "5 mm", "comment": "plastic around the dowel"}},
    {"command": "parameters.add", "params": {"name": "ring_len", "expression": "20 mm", "comment": "the ring's length along the dowel"}},
    {"command": "parameters.add", "params": {"name": "split", "expression": "3 mm", "comment": "the gap the bolt closes"}},
    {"command": "parameters.add", "params": {"name": "ear_t", "expression": "7 mm", "comment": "each clamping ear's thickness"}},
    {"command": "parameters.add", "params": {"name": "ear_h", "expression": "10 mm", "comment": "how far the ears stand above the ring"}},
    {"command": "parameters.add", "params": {"name": "bolt_d", "expression": "4.4 mm", "comment": "clearance for an M4 bolt"}},
    {"command": "parameters.add", "params": {"name": "shelf_len", "expression": "18 mm", "comment": "how far the cord shelf reaches beyond the ring, under the dowel"}},
    {"command": "parameters.add", "params": {"name": "shelf_w", "expression": "18 mm", "comment": "the cord shelf's width"}},
    {"command": "parameters.add", "params": {"name": "shelf_t", "expression": "8 mm", "comment": "the cord shelf's thickness, below the dowel"}},
    {"command": "parameters.add", "params": {"name": "under_gap", "expression": "0.8 mm", "comment": "air between the dowel and the shelf beyond the ring"}},
    {"command": "parameters.add", "params": {"name": "cord_d", "expression": "6 mm", "comment": "the light's cord: measure it; the hole it hangs through"}},
    {"command": "parameters.add", "params": {"name": "slot_w", "expression": "cord_d - 1 mm", "comment": "the slot the cord is pressed in through: narrower than the cord, so it grips"}},
    {"command": "parameters.add", "params": {"name": "bore_d", "expression": "dowel_d + clearance", "comment": "the ring's bore"}},
    {"command": "parameters.add", "params": {"name": "ring_d", "expression": "bore_d + 2 * ring_wall", "comment": "the ring's outside diameter"}},
    {"command": "solid.cylinder", "params": {"diameter": "ring_d", "height": "ring_len", "base": [0, 0, 0], "axis": "X", "body_name": "Cord clamp"}},
    {"command": "solid.box", "params": {"length": "ring_len", "width": "split + 2 * ear_t", "height": "ring_d / 2 + ear_h - bore_d / 2", "corner": [0, "-split / 2 - ear_t", "bore_d / 2"], "body_name": "Ears"}},
    {"command": "solid.box", "params": {"length": "ring_len + shelf_len", "width": "shelf_w", "height": "shelf_t", "corner": [0, "-shelf_w / 2", "-dowel_d / 2 - under_gap - shelf_t"], "body_name": "Shelf"}},
    {"command": "solid.combine", "params": {"target": "Cord clamp", "tools": ["Ears", "Shelf"], "operation": "join"}},
    {"command": "solid.cylinder", "params": {"diameter": "bore_d", "height": "ring_len + shelf_len + 2 mm", "base": ["-1 mm", 0, 0], "axis": "X", "body_name": "Bore"}},
    {"command": "solid.box", "params": {"length": "ring_len + 2 mm", "width": "split", "height": "ring_d / 2 + ear_h + 1 mm", "corner": ["-1 mm", "-split / 2", 0], "body_name": "Split"}},
    {"command": "solid.cylinder", "params": {"diameter": "bolt_d", "height": "split + 2 * ear_t + 2 mm", "base": ["ring_len / 2", "-split / 2 - ear_t - 1 mm", "ring_d / 2 + ear_h / 2 - 1 mm"], "axis": "Y", "body_name": "Bolt hole"}},
    {"command": "solid.cylinder", "params": {"diameter": "cord_d", "height": "shelf_t + 2 mm", "base": ["ring_len + shelf_len / 2", 0, "-dowel_d / 2 - under_gap - shelf_t - 1 mm"], "axis": "Z", "body_name": "Cord hole"}},
    {"command": "solid.box", "params": {"length": "slot_w", "width": "shelf_w / 2 + 1 mm", "height": "shelf_t + 2 mm", "corner": ["ring_len + shelf_len / 2 - slot_w / 2", 0, "-dowel_d / 2 - under_gap - shelf_t - 1 mm"], "body_name": "Cord slot"}},
    {"command": "solid.combine", "params": {"target": "Cord clamp", "tools": ["Bore", "Split", "Bolt hole", "Cord hole", "Cord slot"], "operation": "cut"}},
    {"command": "file.save_as", "params": {"path": "models/sconce-cord-clamp/sconce-cord-clamp.sc", "format": "json", "cache": false}}
  ]
}
```

  Then `mkdir -p models/sconce-cord-clamp`,
  `solidcraft-cli run .git/cord-clamp-script.json --quiet` (exit 0), and `make models`. Look at
  the picture: a split ring with two ears and a bolt hole on top, and a shelf under the dowel's
  line with a round hole and a narrower slot.
- [ ] **Step 4: Write its page's text.**

`models/sconce-cord-clamp/model.yml`:

```yaml
title: Sconce cord clamp
summary: >-
  Clamps anywhere along the sconce's 1-inch dowel and holds the grow light's cord, so the light
  hangs straight below the arm at the height you set.
status: designed
material: PETG, matte
print:
  Orientation: the shelf flat on the bed, the ears up
  Layer height: 0.2 mm
  Walls: 4
  Infill: 30%
  Supports: none
notes: |
  Slide the clamp onto the dowel, set it where the light should hang, and tighten an M4 bolt and
  nut through the ears. Press the light's cord into the slot in the shelf: the slot is a
  millimetre narrower than the cord, so it grips, and the cord hangs from the round hole beyond
  it, straight below the dowel, so the light's weight can't turn the clamp. Pull the cord through
  to set the light's height.

  `cord_d` is the cord's diameter. Measure the light's cord and set it before printing; 6 mm is a
  guess.
```

- [ ] **Step 5: Run the checks; they pass.** `make check`.
- [ ] **Step 6: Commit.** Write the message to `.git/COMMIT_MSG`:

```text
feat(models): 🤖 add the sconce's cord clamp

Dan asked for a printed joint that clamps onto the dowel and holds the
grow light's cord with the light at its end (Q&A answer 11). The clamp is
a split ring tightened by an M4 bolt through two ears, so it holds anywhere
along the arm, with a shelf under the dowel: the cord presses into a slot
a millimetre narrower than itself and hangs from a hole straight below the
dowel's axis, so the light can't turn the clamp. cord_d is the measured
cord.

The new tests failed first with: FileNotFoundError for
models/sconce-cord-clamp/sconce-cord-clamp.eval.json.

Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 3
Co-Authored-By: <the model's own line>
```

  `git add models/sconce-cord-clamp tests/test_cord_clamp.py`, then `git commit -F .git/COMMIT_MSG`, then `git log -1 --format='%(trailers)'` shows the `Plan:` line.
- [ ] **Step 7: Review, look forward, close.** Tier 2: Matt Pocock's `code-review`, two axes in two subagents; fix Critical and Important; at most one re-review, from `$(cat .git/TASK_BASE)`, with the
  picture and the page's viewer looked at. Forward: Task 4 prints this design.

  The close, its own commit (`AGENTS.md`, *Each task's loop*, step 6), its message from
  `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 3: The cord clamp

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

  Push once Dan has OKed it: `make leaks`, then `git push origin phase-2`.

***

### Task 4: [Dan] The look test

**Tier:** none: Dan's verdict; the agent records it (Tier 3) · **Scenarios:** S11, S18

Runs in Dan's home: settles "not sure if it'll look good with 3d printed parts and dowels" for a
few grams of PLA (D8).

- [ ] **1. Print both parts in PLA,** in the colour the real ones will be.
- [ ] **2. Hold it up:** the wall block against the wall where it will go, the dowel in its
  socket, the clamp on the dowel with the light hanging from it. A photo helps; strip it
  (`uv run --frozen scripts/photos.py strip <file>`) before it comes near the repo.
- [ ] **3. The verdict,** asked as a scenario: A, it looks right, print it in PETG; B, it looks
  right with changes (which); C, it doesn't work, and why. Recorded with Dan's words.
  Each answer goes on the Phase 2 Q&A page, `docs/superpowers/plans/2026-11-05-3d-models-phase-2-qa.md`, in Dan's words, committed as `docs(plan): 🤖 record <what>` with this plan's `Plan: … Task 4` line; the page gets its wrapper and Design-page line in its first commit. B or C changes a design: the agent revises Tasks 2 and 3's
  listings and reopens them, a ruling logged on the Q&A page (fully vibed).
- [ ] **4. Close.**

  The close, its own commit (`AGENTS.md`, *Each task's loop*, step 6), its message from
  `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 4: [Dan] The look test

    <what the task built, and why, in a few lines>

    Drift: <filled at the close, or none>
    Rulings: <filled at the close, or none>
    Phase-end: <filled at the close, or none>
    Forward: <filled at the close, or none>
    Tier: 3
    Rounds: <filled at the close>
    Findings: <filled at the close, or none>

    Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 4
    Co-Authored-By: <the model's own line>
    ```

  Push once Dan has OKed it: `make leaks`, then `git push origin phase-2`.

***

### Task 5: [Dan] The load test

**Tier:** none: Dan runs it; the agent records it (Tier 3) · **Scenarios:** S13

- [ ] **1. Print both parts in PETG,** matte, with each page's print settings.
- [ ] **2. Set up the test** somewhere a fall breaks nothing: the wall block screwed to a stud or
  a scrap of wood clamped to a bench, the dowel pinned in it, cut to the arm's length (16 to 20
  inches), the clamp near its end.
- [ ] **3. Load it** with three times the light's weight (Task 1's answer) hanging from the
  clamp; measure the clamp's height above the floor or bench at 0, 24 and 48 hours.
- [ ] **4. The result:** the sag's growth from 0 to 48 hours, and any crack, creak or slip. Passes
  when it grows by under 3 mm and nothing cracks (S13). Recorded on the Q&A page in Dan's words;
  the agent adds a "Load test" section to the wall block's `model.yml` notes, sets both parts'
  `status: printed`, and commits:

```text
docs(models): 🤖 record the sconce's load test

<the load, the arm's length, the three heights and the result, from the
Q&A page>

Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 5
Co-Authored-By: <the model's own line>
```

  A failed test is the fifth stop's case (fully vibed, a ruling): the knee brace (S15) is
  planned in, with the reason, and Dan is told.
- [ ] **5. Close.**

  The close, its own commit (`AGENTS.md`, *Each task's loop*, step 6), its message from
  `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 5: [Dan] The load test

    <what the task built, and why, in a few lines>

    Drift: <filled at the close, or none>
    Rulings: <filled at the close, or none>
    Phase-end: <filled at the close, or none>
    Forward: <filled at the close, or none>
    Tier: 3
    Rounds: <filled at the close>
    Findings: <filled at the close, or none>

    Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 5
    Co-Authored-By: <the model's own line>
    ```

  Push once Dan has OKed it: `make leaks`, then `git push origin phase-2`.

***

### Task 6: [Dan] Install it

**Tier:** none: Dan installs it; the agent records it (Tier 3) · **Scenarios:** S14

- [ ] **1. Mount the wall block** into a stud with two #8 wood screws, or into drywall with two
  toggle anchors; never plastic plugs. The pin through the dowel; the clamp where the light
  should hang; the cord along the top of the arm and into the clamp.
- [ ] **2. Bump it:** it doesn't twist; the light swings and settles.
- [ ] **3. A photo,** stripped first: `uv run --frozen scripts/photos.py strip <file>`, then
  `make photos` passes. It goes in `models/sconce-wall-block/photos/installed.jpg`, linked from the
  wall block's notes; both parts' `status: in use`. Commit:

```text
docs(models): 🤖 the sconce is installed

<where it went, how it was fixed to the wall, and Dan's words on how it
looks>

Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 6
Co-Authored-By: <the model's own line>
```

- [ ] **4. Close.**

  The close, its own commit (`AGENTS.md`, *Each task's loop*, step 6), its message from
  `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 6: [Dan] Install it

    <what the task built, and why, in a few lines>

    Drift: <filled at the close, or none>
    Rulings: <filled at the close, or none>
    Phase-end: <filled at the close, or none>
    Forward: <filled at the close, or none>
    Tier: 3
    Rounds: <filled at the close>
    Findings: <filled at the close, or none>

    Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 6
    Co-Authored-By: <the model's own line>
    ```

  Push once Dan has OKed it: `make leaks`, then `git push origin phase-2`.

***

### Task 7: Phase end

The same nine steps as Phase 1's Task 8, each one box ending in its commit
(`docs(plan): 🤖 phase end step K: <what it did>`, with `Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Phase end`), resumed at the
first unticked box. This is the last phase: step 5 offers Dan each Later row (S15, S16, S17) by
*Asking Dan*: plan it, keep it optional, or drop it.

- [ ] **1. The final whole-branch review**
- [ ] **2. The rest of the ledger copied into the plan**
- [ ] **3. The phase-end council** (`…-phase-2-end-council.md`, with its wrapper)
- [ ] **4. The phase-end list worked through**
- [ ] **5. The forward look, and the Later rows offered to Dan**
- [ ] **6. The retro** (`…-phase-2-retro.md`, with its wrapper)
- [ ] **7. The changelog and status**
- [ ] **8. The PR:** `chore(repo): 🤖 merge Phase 2: the wall sconce`; it adds STL, PNG and photo
  files no scan can read, so it waits for Dan's look before the merge
- [ ] **9. After the merge:** the sconce's pages are live, their viewers load

***

## Phase-end list

| Source | Severity | File | Item | Status |
|---|---|---|---|---|
