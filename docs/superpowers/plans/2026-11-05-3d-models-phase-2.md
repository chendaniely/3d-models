# 3d-models Phase 2: the wall sconce, implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking. The project's `AGENTS.md` holds every rule for running
> it and outranks this header where they differ. **This plan is revised at Phase 2's start**
> against the code Phase 1 built, its listings run first.

**Goal:** the grow-light sconce on the wall of the plant corner: a 1-inch dowel cantilevered 16
to 20 inches from the wall in Phase 1's wall block, Dan's Barrina grow light hanging from Phase
1's cord clamp, each part tuned to Dan's measurements and proven by a load test before it goes up.

**Architecture:** Phase 1 designed the parts (Q&A answer 12); this phase is Dan's measurements,
the parameter changes they call for, and his look test, load test and install, each a [Dan] task
whose answers the agent records and turns into the parts' parameters and pages.

**Tech Stack:** Phase 1's pipeline; PETG and PLA prints; a 1-inch hardwood dowel, an M6 × 50 mm
bolt and nylon-insert nut, an M4 × 30 mm bolt and nut, two #8 or #10 wood screws or 3/16-inch
toggle bolts.

**Spec:** `docs/superpowers/specs/2026-11-05-3d-models-design.md`

**Now:** Task 1: [Dan] Measure, weigh, and print the coupon, open.

***

## Global Constraints

- Every Phase 1 constraint holds (its plan's *Global Constraints*).
- The arm is a straight cantilever (D6), 16 to 20 inches (406 to 508 mm) out.
- `dowel_d` stays the dowel's nominal size; the coupon's hole that fit sets `clearance`, which
  covers the dowel's own variation.
- Screws go into a stud or toggle anchors, never plastic plugs; `screw_d` fits the anchor chosen.
- Load-bearing parts are PETG, matte, never PLA (D9); PLA only for the look test (D8).
- A photo: Strip it first, `uv run --frozen scripts/privacy.py strip <file>`; then show Dan the stripped file and ask, naming it, whether anything in it shows where he lives (a window's view, a street, a house number, a face, a reflection, a screen). Only after his OK naming the file does it go under `models/<slug>/photos/`, and `make privacy` passes before it's staged.

## Review Focus

1. **A flat two-wire cord, not a round one:** a round grip won't hold it; Task 1 asks, and Task 2
   reshapes the hole and slot rather than resizing them.
2. **A metric 25 mm dowel bought in place of 1 inch:** the 25 mm coupon and the 25 mm STLs, which
   Phase 1 already exports; `clearance` from that coupon.
3. **Drywall with no stud where the block goes:** toggle anchors, load-tested in a drywall offcut
   (Task 4), never plugs.
4. **The cord slipping through the clamp over days:** the load test hangs through the cord grip
   and measures slip (Task 4, S18).
5. **A photo that shows the street outside the window:** Dan's look at each stripped photo before
   it's staged (every photo step).

***

### Task 1: [Dan] Measure, weigh, and print the coupon

**Tier:** none: Dan's measurements, recorded by the agent (Tier 3) · **Scenarios:** S09, S12, S18

Runs in Dan's home. **Now** reads `waiting on Dan: <the step>` until each answer is in. The steps
are asked by *Asking Dan*, one at a time.

- [ ] **1. Weigh the light:** the Barrina bulb with its socket, cord and timer, on a kitchen
  scale. The numbers assume 1 kg; above that, the agent re-runs the kickoff notes' sag and anchor
  numbers before Task 2.
- [ ] **2. The cord:** round or flat, and its diameter (or width and thickness) with calipers,
  just above the bulb; and what the kit's hanging system includes.
- [ ] **3. The dowel:** its nominal size as bought (1 inch, 25 mm or 3/4 inch) and its wood.
- [ ] **4. Print the coupon** for that size, standing on its edge (its page's print settings),
  and try the dowel in each hole: which hole, by its dots, is the tightest it goes into by hand?
- [ ] **5. The wall,** as measurements: the block's height from the floor and distance from the
  corner; the wall's material; a stud there or not; and so the anchor (#8 or #10 wood screws, or
  3/16- or 1/4-inch toggle bolts).
- [ ] **6. Record and close.** Each answer goes on the Phase 2 Q&A page, `docs/superpowers/plans/2026-11-05-3d-models-phase-2-qa.md`, in Dan's words, committed as `docs(plan): 🤖 record <what>` with this plan's `Plan:` line; the page gets its Design-page line in its first commit. The room is recorded as measurements (heights, distances, the wall's material), never a description of the home: the Q&A pages are published. Then the close:

  - **Review (Tier 3: a self-review under Standards and Spec, plus the mechanical checks),** from `$(cat .git/TASK_BASE)`.
  - **Forward:** Task 2 turns these answers into parameters.
  - **Docs:** none until Task 2.
  - **Close,** its own commit: this task's boxes ticked, **Now** set to the next task, any
    Built differently and Ruling lines, deferred findings on the phase-end list, the spec's
    scenario statuses (`built`). The message, from `docs/agents/close-task.txt`:

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

  - **Push,** once Dan has OKed it, the request naming every binary file the push adds
    (`AGENTS.md`'s interim line): `make leaks privacy`, then `git push origin phase-2`.
    The task is closed once CI on the closing commit, or a later one, is green; until a
    push, the local checks are the gate.

***

### Task 2: Tune the parts to Dan's answers

**Tier:** 2 · **Scenarios:** S12, S18

**Files:**
- Modify: `models/sconce-wall-block/sconce-wall-block.sc`, `models/sconce-cord-clamp/sconce-cord-clamp.sc`
  (by SolidCraft), their built files (by `make models`), their `model.yml` notes

**Interfaces:**
- Consumes: Task 1's answers; Phase 1's designs, `make models` and their tests.
- Produces: the wall block's `clearance` (the coupon's `step` times the dots that fit) and
  `screw_d` (5 mm for #8 or #10 screws and 3/16-inch toggles, 6.6 mm for 1/4-inch ones); the
  clamp's `cord_d`; if the cord is flat, a reshaped grip, its new parameters named in the close.

- [ ] **Step 0: Record the base:** `git rev-parse HEAD > .git/TASK_BASE`.
- [ ] **Step 1: The parameter changes,** one command script per part in `.git/`, each a
  `parameters.change` per answer and then the save, for example the wall block's:

```json
{
  "commands": [
    {"command": "parameters.change", "params": {"name": "clearance", "expression": "0.4 mm"}},
    {"command": "parameters.change", "params": {"name": "screw_d", "expression": "5 mm"}},
    {"command": "file.save_as", "params": {"path": "models/sconce-wall-block/sconce-wall-block.sc", "format": "json", "cache": false}}
  ]
}
```

  `solidcraft-cli run .git/<part>-tune.json --in models/<slug>/<slug>.sc --quiet`, for each part,
  with the values from Task 1's answers. A flat cord: the grip's hole and slot become a slot
  sized to the cord's width and thickness, its script in the plan before it runs (a forward
  rewrite, named under `Forward:`).
- [ ] **Step 2: Rebuild and check.** `make models`, then `make check`. Expected: both parts
  rebuilt, every test passing (the wall block's clearance is one of the coupon's; the clamp's slot
  and hole are narrower than the cord).
- [ ] **Step 3: The notes:** each part's `model.yml` notes say the values chosen and why, from the
  Q&A page.
- [ ] **Step 4: Commit.** Write the message to `.git/COMMIT_MSG`:

```text
feat(models): 🤖 tune the sconce's parts to Dan's measurements

<the clearance from the coupon's hole, the screw hole for the anchor, the
cord's diameter or shape, each with the Q&A answer it came from>

Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 2
Co-Authored-By: <the model's own line>
```

  `git add models/sconce-wall-block models/sconce-cord-clamp`, then `git commit -F .git/COMMIT_MSG`, then `git log -1 --format='%(trailers)'` shows the `Plan:` line.
- [ ] **Step 5: Review, look forward, close.**

  - **Review (Tier 2: Matt Pocock's `code-review`, two axes in two subagents; fix Critical and Important; at most one re-review),** from `$(cat .git/TASK_BASE)`.
  - **Forward:** Task 3 prints these designs.
  - **Docs:** each part's page says what it's tuned to.
  - **Close,** its own commit: this task's boxes ticked, **Now** set to the next task, any
    Built differently and Ruling lines, deferred findings on the phase-end list, the spec's
    scenario statuses (`built`). The message, from `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 2: Tune the parts to Dan's answers

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

  - **Push,** once Dan has OKed it, the request naming every binary file the push adds
    (`AGENTS.md`'s interim line): `make leaks privacy`, then `git push origin phase-2`.
    The task is closed once CI on the closing commit, or a later one, is green; until a
    push, the local checks are the gate.

***

### Task 3: [Dan] The look test

**Tier:** none: Dan's verdict, recorded by the agent; Tier 1 if a photo is committed ·
**Scenarios:** S11, S18

Settles "not sure if it'll look good with 3d printed parts and dowels" for a few grams of PLA (D8).

- [ ] **1. Print both parts in PLA,** in the colour the real ones will be, and the wall block's
  caps.
- [ ] **2. Hold it up:** the wall block against the wall where it will go, the dowel in its
  socket, the clamp on the dowel, the light's cord through the clamp and the light hanging from
  it.
- [ ] **3. The verdict, and Dan's changes,** asked as a scenario (Phase 1 Q&A 4: his changes to how
  the dowel mounts and clamps to the parts, and how the block screws to the wall, come here): A, it looks right, print it in PETG; B, it looks
  right with changes (which: edges, size, the visible bolt and screws, the ears' side); C, it
  doesn't work, and why. Recorded with Dan's words. Each answer goes on the Phase 2 Q&A page, `docs/superpowers/plans/2026-11-05-3d-models-phase-2-qa.md`, in Dan's words, committed as `docs(plan): 🤖 record <what>` with this plan's `Plan:` line; the page gets its Design-page line in its first commit. The room is recorded as measurements (heights, distances, the wall's material), never a description of the home: the Q&A pages are published. B or C changes a design: the
  agent revises Phase 1's listings for that part in this plan, reopens Task 2 for the change, and
  logs a ruling on the Q&A page (fully vibed). Rounded edges, the kickoff notes' advice, are a
  likely B: the spec's Later row S22.
- [ ] **4. A photo, if Dan wants one on the page:** Strip it first, `uv run --frozen scripts/privacy.py strip <file>`; then show Dan the stripped file and ask, naming it, whether anything in it shows where he lives (a window's view, a street, a house number, a face, a reflection, a screen). Only after his OK naming the file does it go under `models/<slug>/photos/`, and `make privacy` passes before it's staged.
- [ ] **5. Close.**

  - **Review (Tier 3: a self-review under Standards and Spec, plus the mechanical checks; with a photo, Tier 1: Matt Pocock's `code-review`, two axes in two subagents, plus the security checklist, one line per item; at most one re-review),** from `$(cat .git/TASK_BASE)`.
  - **Forward:** Task 4 prints the PETG parts.
  - **Docs:** the parts' notes say the look test passed, or what changed.
  - **Close,** its own commit: this task's boxes ticked, **Now** set to the next task, any
    Built differently and Ruling lines, deferred findings on the phase-end list, the spec's
    scenario statuses (`built`). The message, from `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 3: [Dan] The look test

    <what the task built, and why, in a few lines>

    Drift: <filled at the close, or none>
    Rulings: <filled at the close, or none>
    Phase-end: <filled at the close, or none>
    Forward: <filled at the close, or none>
    Tier: 3, or 1 with a photo
    Rounds: <filled at the close>
    Findings: <filled at the close, or none>

    Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 3
    Co-Authored-By: <the model's own line>
    ```

  - **Push,** once Dan has OKed it, the request naming every binary file the push adds
    (`AGENTS.md`'s interim line): `make leaks privacy`, then `git push origin phase-2`.
    The task is closed once CI on the closing commit, or a later one, is green; until a
    push, the local checks are the gate.

***

### Task 4: [Dan] The load test

**Tier:** none: Dan runs it; the agent records it (Tier 3) · **Scenarios:** S13, S18

- [ ] **1. Print both parts in PETG,** matte, with each page's print settings.
- [ ] **2. Set up the test** somewhere a fall breaks nothing, mounted the way it will be: into a
  stud, or with the chosen toggle anchors in an offcut of the same drywall clamped to a bench. The
  dowel, cut to the arm's length, bolted in its socket; the clamp near its end.
- [ ] **3. Load it** with three times the light's weight (Task 1's answer), hung by the light's
  cord through the clamp's grip, not from the clamp; mark the cord where it leaves the grip.
  Measure at 0, 24 and 48 hours: the clamp's height above the floor or bench, and how far the
  mark has moved.
- [ ] **4. The result:** passes when the sag grows by under 3 mm, the cord slips under 2 mm, and
  nothing cracks or pulls out (S13, S18). Recorded on the Q&A page in Dan's words; the agent adds
  a "Load test" section to the wall block's and the clamp's notes, sets both parts'
  `status: printed`, and commits:

```text
docs(models): 🤖 record the sconce's load test

<the load, the arm's length, the mounting, the three heights and slips, and
the result, from the Q&A page>

Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 4
Co-Authored-By: <the model's own line>
```

  A failed test is the fifth stop's case (fully vibed, a ruling): the knee brace (S15), a longer
  grip, or a stud mount is planned in, with the reason, and Dan is told.
- [ ] **5. Close.**

  - **Review (Tier 3: a self-review under Standards and Spec, plus the mechanical checks),** from `$(cat .git/TASK_BASE)`.
  - **Forward:** Task 5 installs what passed.
  - **Docs:** both parts' pages carry the load test.
  - **Close,** its own commit: this task's boxes ticked, **Now** set to the next task, any
    Built differently and Ruling lines, deferred findings on the phase-end list, the spec's
    scenario statuses (`built`). The message, from `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 4: [Dan] The load test

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

  - **Push,** once Dan has OKed it, the request naming every binary file the push adds
    (`AGENTS.md`'s interim line): `make leaks privacy`, then `git push origin phase-2`.
    The task is closed once CI on the closing commit, or a later one, is green; until a
    push, the local checks are the gate.

***

### Task 5: [Dan] Install it

**Tier:** none: Dan installs it; the agent records it, Tier 1 for the photo · **Scenarios:** S14

- [ ] **1. Mount the wall block** as tested: #8 or #10 wood screws into the stud, or the
  chosen toggle anchors, never plastic plugs; the caps pressed in over the screw heads; the M6
  bolt through the boss and the dowel; the clamp where the light should hang; the cord along the
  top of the arm and into the clamp.
- [ ] **2. Bump it:** it doesn't twist; the light swings and settles.
- [ ] **3. A photo:** Strip it first, `uv run --frozen scripts/privacy.py strip <file>`; then show Dan the stripped file and ask, naming it, whether anything in it shows where he lives (a window's view, a street, a house number, a face, a reflection, a screen). Only after his OK naming the file does it go under `models/<slug>/photos/`, and `make privacy` passes before it's staged. It goes in `models/sconce-wall-block/photos/installed.jpg`;
  the gallery shows it on the page. Both parts' `status: in use`. Commit:

```text
docs(models): 🤖 the sconce is installed

<how it was fixed to the wall, and Dan's words on how it looks>

Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 5
Co-Authored-By: <the model's own line>
```

- [ ] **4. Close.**

  - **Review (Tier 1: Matt Pocock's `code-review`, two axes in two subagents, plus the security checklist, one line per item; at most one re-review, over the photo),** from `$(cat .git/TASK_BASE)`.
  - **Forward:** the phase end.
  - **Docs:** the README's first-project lines say it's up.
  - **Close,** its own commit: this task's boxes ticked, **Now** set to the next task, any
    Built differently and Ruling lines, deferred findings on the phase-end list, the spec's
    scenario statuses (`built`). The message, from `docs/agents/close-task.txt`:

    ```text
    docs(plan): 🤖 close Task 5: [Dan] Install it

    <what the task built, and why, in a few lines>

    Drift: <filled at the close, or none>
    Rulings: <filled at the close, or none>
    Phase-end: <filled at the close, or none>
    Forward: <filled at the close, or none>
    Tier: 1
    Rounds: <filled at the close>
    Findings: <filled at the close, or none>

    Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Task 5
    Co-Authored-By: <the model's own line>
    ```

  - **Push,** once Dan has OKed it, the request naming every binary file the push adds
    (`AGENTS.md`'s interim line): `make leaks privacy`, then `git push origin phase-2`.
    The task is closed once CI on the closing commit, or a later one, is green; until a
    push, the local checks are the gate.

***

### Task 6: Phase end

The same nine steps as Phase 1's Task 10, each one box ending in its commit
(`docs(plan): 🤖 phase end step K: <what it did>`, with `Plan: docs/superpowers/plans/2026-11-05-3d-models-phase-2.md Phase end`), resumed at the
first unticked box. This is the last phase: step 5 offers Dan each Later row by *Asking Dan*:
plan it, keep it optional, or drop it.

- [ ] **1. The final whole-branch review**
- [ ] **2. The rest of the ledger copied into the plan**
- [ ] **3. The phase-end council** (`…-phase-2-end-council.md`, with its Design-page line)
- [ ] **4. The phase-end list worked through**
- [ ] **5. The forward look, and the Later rows offered to Dan**
- [ ] **6. The retro** (`…-phase-2-retro.md`, with its Design-page line)
- [ ] **7. The changelog and status**
- [ ] **8. The PR:** `chore(repo): 🤖 merge Phase 2: the wall sconce`; it adds STL, PNG and photo
  files no scan can read, so it waits for Dan's look before the merge
- [ ] **9. After the merge:** the sconce's pages are live, their viewers load, the photo shows

***

## Phase-end list

| Source | Severity | File | Item | Status |
|---|---|---|---|---|
