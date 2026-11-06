# 3d-models Phase 1: retro

Phase 1 built the repo and its first models on `phase-1`, 2026-11-05: the uv toolchain and CI, `make
models`, the privacy guard, the docs site, the gallery and its 3D viewer, the dowel fit-test coupon,
the sconce's wall block and cord clamp (each in three dowel sizes), and the GitHub settings. Run
subagent-driven (kickoff Q&A answer 17), fully vibed, with Dan's standing OK for its end
(Phase 1 Q&A 5). The plan is [Phase 1's plan](2026-11-05-3d-models-phase-1.md); its end council is
[here](2026-11-05-3d-models-phase-1-end-council.md).

## 1. Departures from the plan

- **Task 3, Built differently:** `strip` kept a PNG's transparency (the listing turned a transparent
  PNG opaque), checked every file before rewriting any, printed only file names and kept the file's
  mode; found by the task's Standards review.
- **Task 4, Built differently:** Quarto's own `website/.gitignore` committed; and CI's lychee step
  extracts the path the release tarball really uses, after CI's first run failed on it (escaped
  from Task 4, fixed under Task 6's reopen).
- **The stop before Task 7:** Dan said mid-run he had changes to how the dowels mount, clamp and
  screw to the wall; the run stopped before the two parts, and he chose to build them as planned and
  change them after the look test (Phase 1 Q&A 1, 4).
- **The final whole-branch review's fixes:** the privacy check covers the history (a stripped photo
  stayed in what a push carries), symlinks, a home folder with no slash after it (from an automated
  security review) and a blob a tag points at; `models.py` reads `model.yml` safely and tells an
  invalid model from a stale one; the gallery checks its inputs before emptying its output;
  `make strip`; the overview diagram drew built parts as planned.
- **The end council's fixes (step 4):** an image may hold only what a picture needs (PNG chunks,
  nothing after a JPEG's or PNG's or WebP's end); a shallow clone fails the history check; a size
  changing a parameter the design lacks, or two sizes sharing a file name, are refused; the size
  note names `clearance`; a model's free text is escaped for Quarto; `.gitattributes` keeps
  `models/` byte-exact; CI syncs `--locked` with uv pinned.
- **Rulings** (each in its closing commit or the plan's run ledger): Tasks 7 and 8 waited for Dan;
  push requests were batched; implementers and reviewers ran on sonnet, the final review on Opus;
  the merge's wait for Dan's look at the binaries was met when he OKed each by name; Dan asked the
  agent to apply the GitHub settings, which it did with `gh`.

## 2. Items carried forward

- **To Phase 2's Task 3, before the first photo:** a JPEG segment type Pillow skips still passes the
  privacy check; a file that vanishes before it's read raises; a few model fields (print settings,
  size names, photo file names) still go into the page raw.
- **To the spec's Later:** S22 rounded edges (after the look test); S23 the viewer framing each
  model to fit; S24 a CLI-version warning, a build timeout, a streaming history scan; S25 commit and
  tag messages scanned, symlink blobs told apart in history, an image and a text path sharing bytes.
- **Dan's:** his changes to the parts (Phase 2's Task 1 asks for those he already knows); lychee
  locally; his commits' author address (a noreply address would keep it out of future commits);
  Dependabot's security updates.

## 3. Metrics per tier

Tallied from the closing commits (`git log --grep='close Task'`), the reopen, and the fixes that
name what they escaped from.

| Tier | Tasks | Reviews | Fix rounds | Findings at the task | Found later |
|---|---|---|---|---|---|
| 1 | 1, 3, 4, 6 | 8 (two axes each, the security checklist on each) | 1 (Task 3), one re-review | 1 important (Task 3), 19 minor | Task 4's lychee path (CI's first run); Task 3's history, symlink, slash-less home path and tag blob (final review, a security review, its re-review); PNG chunks and trailing bytes (end council) |
| 2 | 2, 5, 7, 8 | 8 (two axes each) | 0 | 0 important, 19 minor | Task 2's unsafe YAML (final review); size typos and file-name collisions (end council); Task 5's unchecked inputs (final review), the size note and raw free text (end council); Task 7's diagram (final review) |
| none | 9 | the security checklist over the settings | 0 | 0 | none |

Across the phase: 71 commits, 15 of them fixes; one reopen (Task 6, for Task 4's CI step); one
transient CI failure (a `setup-uv` step, green on rerun). Every Phase 1 scenario but S10 (the live
site, after the merge) is built.

## 4. Starting over

- **Run what can't run locally before the plan relies on it.** The lychee step was the one listing
  the prototype couldn't run; listing the tarball when writing it would have caught the path.
- **Scope the privacy guard as "what leaves the machine", from the start.** "What git would commit"
  missed the history, tags and symlinks; each was found later, one review at a time.
- **Read the anti-goal against the parser, not the format.** An allow-list of metadata keys trusted
  Pillow to show everything; a structural check of the file was needed.
- **Give each model task a diagram step.** The plan said the overview needed no change after the
  parts were built; it did.
- **Split a scenario at spec time when two phases prove it.** S09 and S18 claimed Phase 2's proof
  until the end council split them.
- **Ask about changes before building a part Dan will use.** He had changes in mind for the parts
  before Tasks 7 and 8 ran.

## Retuning Phase 2's tiers

- **Tier 3 reviews finding an Important in more than one task:** not met (no Tier 3 task was
  reviewed). No change.
- **Tier 1 re-reviews finding nothing:** not met (Task 3's re-review confirmed its fixes, and the
  final review's re-review found the tag-blob gap). Phase 2's Tier 1 tasks keep their re-review.
- **A bug reaching CI that a local check could have caught:** the lychee path; only lychee itself
  would have caught it, and installing it locally is Dan's call. No new check.
- **Tier 2's Standards axis finding no Important or Critical:** met (Tasks 2, 5, 7 and 8: none).
  Phase 2's Tier 2 task (Task 2, tuning the parts) runs with one reviewer under both headings; its
  plan says so.
