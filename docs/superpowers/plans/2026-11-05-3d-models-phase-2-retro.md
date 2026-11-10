# 3d-models Phase 2: retro

Phase 2 ran on `phase-2`, 2026-11-06 to 2026-11-09: the rail's five parts, at placeholder sizes, two
store gauges, and the privacy and off-site checks, run subagent-driven and fully vibed. It ended
early: with the gauges printing and no measurement taken, Dan paused the lamp to finish the project
and design parts next (Q&A 15). So the rail was never measured, printed, tested or installed. The
plan is [Phase 2's plan](2026-11-05-3d-models-phase-2.md); its end council is
[here](2026-11-05-3d-models-phase-2-end-council.md).

## 1. Departures from the plan

- **The biggest: Tasks 10 to 14 weren't done.** Dan's call (Q&A 15); decided without Dan 5 reads it
  as all five tasks, since each waits on the one before, and takes the full phase end.
- **The order changed mid-phase.** Measure first became publish first, retune later (Q&A 9), so the
  five parts went to the gallery at guessed sizes (#3). The retune never came.
- **Two gauges were added** (Q&A 11, Task 9), then trimmed to share a plate, their numbers raised
  for a second colour and both made 4 mm thick (Q&A 12 to 14, Task 10's steps 0a and 0b).
- **Built differently,** each noted at its task's head: the feet's screw-head depth (Task 2); a
  comment and S28's wording for a dowel off its size (Task 3); the socket's notes (Task 4); the
  stem's slot, for a watertight tip (Task 5); the shade's vents (Task 6); the README's status list
  (Task 7); the card's windows and scales (Task 9); the raised lettering as separate bodies, since
  joining 162 small solids hadn't finished after half an hour (Task 10).
- **Rulings:** decided without Dan 1 to 6, on the Q&A page: the feet's fixing, S27, the coupon on
  the finished dowel, the card's scales, the pause's reach, and the gauges' generator in the repo.

## 2. Items carried forward

- **Paused with the lamp (Later):** S11, S13, S14, S26, S27, S29, S30, S32, and S35, which holds the
  rail's parked review findings. Tasks 10 to 14 stay in the plan, unticked.
- **Optional (Later), kept so by Dan (Q&A 16):** S15, S16, S17, S22, S23, S24, S25, S36, S37, S38.
- **The printed gauges:** whether the ticks read clearly, and the coin check, are S38.

## 3. Metrics per tier

Tallied from the closing commits, and the fixes that name what they escaped from.

| Tier | Tasks | Reviews | Fix rounds | Findings at the task | Found later |
|---|---|---|---|---|---|
| 1 | 1 | 2 (two axes, with the security checklist) | 1, one re-review | 2 important, 10 minor | the JPEG walker's crash on fill bytes (final review) |
| 2 | 2, 3, 4, 5, 6, 7, 9 | 7 (one reviewer under both headings) | 6 | 7 important, 28 minor | the hole grid's advice on a dowel out of range, S33's and S34's proofs (Task 9); the shade's 10 mm claim (Task 6); the feet's placeholders (Task 2) (final review) |
| 3 | 8, 10 | 2 self-reviews | 1 | 1 important (Task 10: where a prime tower goes) | none |
| none | 11, 12, 13, 14 | none: paused, nothing built | 0 | 0 | none |

Across the phase: 70 commits to the start of this retro, 7 of them fixes; no reopen, and no red CI
on a closing commit. The final review found 3 important in Standards and 3 in Spec, all fixed or
re-rated. The council raised 8 important: 2 were fixed (the generator, an empty
glob in a test), 2 were step 7's own work, 2 were re-rated minor when checked, and 2 were wrong, as
were 2 minors.

## 4. Starting over

- **Build what a measurement needs after the measurement.** Five parts at guessed sizes reached the
  gallery and were never tuned. The gauges, which Dan could use at once, came last and got printed
  first.
- **Keep a design's generator in the repo from the day it computes anything.** The card's ticks
  come from a script that sat in `.git/` until the council found it.
- **Try a tool's slow path early.** One small experiment on joining many solids would have saved
  the half-hour builds and three failed routes.
- **Run the real slicer before saying how a print behaves.** A headless slice caught the prime
  tower sitting under the tile, which the page had put there.
- **Fetch `main` before comparing against it.** Mid-phase merges left the local `main` behind, and
  a reviewer counted 18 files already published as new.

## Retuning the next phase's tiers

No later phase is planned, so nothing changes yet; these hold for the next plan.

- Tier 3 found an Important in one task only: the tier stays.
- Tier 1's one re-review found nothing, but a Tier 1 bug escaped to the final review: keep it.
- No bug reached CI that a local check could have caught, so no check is added.
- Tier 2 already runs one reviewer under both headings; that found 7 important, so it stays.
