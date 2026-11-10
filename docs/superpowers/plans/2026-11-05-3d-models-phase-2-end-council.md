# 3d-models Phase 2: the phase-end council

Four read-only reviewers, one per lens, read `phase-2` from the Phase 1 merge (`746ce34`) to
`3ba27fa` on 2026-11-09, after the final whole-branch review and its fixes. The phase ended early:
Dan paused the lamp, so Tasks 10 to 14 were closed as paused and their scenarios moved to the spec's
Later (Phase 2 Q&A 15). The reports are below as they gave them, shortened where they quoted file
text. The decision on each finding follows in [Decisions](#decisions), written after these reports
were committed.

## Goal fit and scenarios

0 critical, 3 important, 4 minor. The branch delivers the cut-short Phase 2: gauges built, the
rail's parts at placeholder sizes, Phase 1's parts superseded, Q&A 15 reflected in the spec's Later
rows, the diagrams and the plan's header. S01 to S10, S12, S18 to S21, S28, S31, S33 and S34 hold up
against the files read. Nothing was built without being asked.

1. **Important:** `models/rail-*/model.yml`: the rail pages say "a placeholder until the coupon is
   printed", but none says the part is unprinted, untested and paused, and the parts carry a lamp
   and planters over people's heads. Fix: one sentence in each part's notes.
2. **Important:** `README.md`: "Phase 2, ending now" is true only until the merge, and the intro
   describes the finished lamp. Fix: say it merged with the lamp paused, and what comes next.
3. **Important:** `CHANGELOG.md` has no Phase 2 entry (step 7 is open). It must record the pause
   and the five parts, not a rail tested and installed.
4. **Minor:** `README.md`: `make models` needs `solidcraft-cli` 0.30.1, but it doesn't say how a
   design saved in the app becomes `<slug>.sc`, that `.sc.bak` and `.eval.json` appear beside a
   build, or that `make hooks` installs nothing yet.
5. **Minor:** spec S33: status `built` while its proof says the coin check isn't done.
6. **Minor:** the plan's Global Constraints and Review Focus still cite Tasks 10 to 14 as live; the
   plan's Cut short note covers this.
7. **Minor:** Phase-end rows that wait on the look and load tests should be marked paused.

## Reliability

0 critical, 3 important, 4 minor. Sizes and CI are fine; the findings are build and test hardening.

1. **Important:** `scripts/models.py`, `run`: `subprocess.run` has no timeout, so a pathological
   boolean or a many-shell model with raised text hangs `make models` with no output.
2. **Important:** `build()` never checks what the CLI produced: an exit 0 with an empty or
   non-manifold STL is hashed into `build.json` and passes `models-check`. Fix: check each output's
   size is `84 + 50n` before recording it.
3. **Important:** `tests/test_meshes.py` can pass while checking nothing: `STLS` is globbed at
   import, so an empty glob collects no tests; it assumes binary STL; and rounding to 4 decimals
   can split or merge vertices on a new design.
4. **Minor:** `tests/conftest.py`'s fake CLI never exercises `parameters.change` on a text
   parameter. Check once by hand, the first time a text parameter is sized.
5. **Minor:** `invalid()` skips the unknown-parameter check once a design changes, so CI only says
   "stale"; the error surfaces on `make models`.
6. **Minor:** a viewer's `data-stl` attribute is checked by neither lychee nor `offsite.py`.
7. **Minor:** `ci.yml`: `cancel-in-progress` is on for `main`, so a second push cancels a deploy in
   flight; the last push still wins.

Fine: ordering and locale (listings sorted, no timestamps, `.gitattributes` keeps `models/` byte
exact); `pages` needs the tests, the leak scan and the site, so a stale build can't deploy; sizes
(tracked files 43 MB, the largest STL 9.6 MB, more than 20 times under both GitHub limits).

## Security and privacy

0 critical, 1 important, 1 new minor. `make privacy` and `make leaks` pass.

| Checklist | Result |
|---|---|
| Secrets | fine: CI uses none, none in the diff |
| Permissions | fine: `contents: read` by default, only the `pages` job can write, actions pinned to a SHA, downloads checked against a SHA-256 |
| Network exposure | fine: `scripts/offsite.py` runs in `make docs` and fails on a remote load; its gaps are on the Phase-end list |
| Failing closed | fine: `offsite.py` fails on a missing site, and both scans run on the full history |
| Injection | fine: no shell built from model data, Mermaid bundled, the render code not audited line by line |
| Logging | fine: file paths only, leak findings redacted |

Binaries: each STL's 80-byte header is `SolidCraft STL <slug>` alone, and each PNG holds only IHDR,
IDAT and IEND. Published text: no city, address, person or description of the home. No task is
under-tiered.

1. **Important:** Task 15's step 8 says the merge adds the gauges' 16 files; it adds 34, with 18
   under the rail's five models. Fix: correct the count and list all 34.
2. **Minor:** `scripts/privacy.py` reads image metadata but not STL headers, and the leak scan
   skips binaries, so a future tool could write a path or a username there. Fix: check each header
   is `SolidCraft STL <slug>`.
3. **Minor:** the superseded pages cite Q&A numbers (already on the Phase-end list).

## Simplicity

0 critical, 1 important, 5 minor.

1. **Important:** `.git/gauges.py`, the gauges' generator, is lost to a fresh clone: 312 lines
   inside `.git/`, on one disk. The card's 162 ticks and the grid's holes come from it, and no one
   can sensibly hand-edit its output. Fix: commit it, and say the `.sc` is generated from it.
2. **Minor:** `scripts/privacy.py` is 367 lines of hand-written image parsing, with no photo in the
   repo yet. It could drop the history scan and WebP.
3. **Minor:** `scripts/offsite.py` could shrink to a grep for remote URLs. Don't extend it further.
4. **Minor:** a new design needs several built files before `make check` passes, as intended, and
   `.sc.bak` files aren't in `.gitignore`.
5. **Minor:** `make check` runs the suite twice, once under `TZ=UTC`.
6. **Minor:** CI repeats `make check` as three jobs, which is fine for parallelism.

## Decisions

Each claim was checked against the code before it was decided. Severities are the session's.

| Finding | What the check found | Severity | Decision |
|---|---|---|---|
| Goal fit 1 | Wrong: all five pages say "a first design, not yet printed or load-tested" (the shade: "tested with the light on") | none | no change |
| Goal fit 2 | True | Important | step 7 |
| Goal fit 3 | True | Important | step 7 |
| Goal fit 4 | Mostly wrong: the README names the CLI and its version, and *Adding a model* says how a design is saved | Minor | no change |
| Goal fit 5 | True | Minor | fixed, `389ac9f` |
| Goal fit 6 | True, and the plan's Cut short note covers it | Minor | no change |
| Goal fit 7 | True | Minor | step 4, Later S35 |
| Reliability 1 | True, already the spec's Later S24 | Minor | Later, S24 |
| Reliability 2 | Partly: `build()` doesn't check, but `make check` reads every STL in the tree, so an empty one fails before a push | Minor | Later, S37 |
| Reliability 3 | The empty glob is true; an ASCII STL can't pass (the parse fails), and the rounding is theoretical | Minor | fixed, `2639777` |
| Reliability 4 to 6 | True | Minor | Later, S37 |
| Reliability 7 | True, and the last push wins | Minor | no change |
| Security 1 | Wrong: counted from a local `main` that's behind. `origin/main` already has the rail's 18, which Dan OKed by name (Q&A 10); the merge adds the gauges' 16 | none | no change |
| Security 2 | True | Minor | Later, S37 |
| Security 3 | Already listed | Minor | Later, S37 |
| Simplicity 1 | True | Important | fixed, `7bf9ddb`; decided without Dan 6 |
| Simplicity 2 | A judgement: nothing else stops a photo's location going public, on a public repo, and the history scan is the guard against a past slip | Minor | no change |
| Simplicity 3 | A judgement: small and stable, and it's not extended | Minor | no change |
| Simplicity 4 | Wrong about `.sc.bak`: `.gitignore` has it. The built files before a pass are intended | none | no change |
| Simplicity 5 | True, and `AGENTS.md` requires the second run | Minor | no change |
| Simplicity 6 | Says it's fine | none | no change |
