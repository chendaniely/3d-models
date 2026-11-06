# 3d-models Phase 1: the phase-end council

Four read-only reviewers, one per lens, read the whole of `phase-1` from its merge-base (`68ce9ac`)
to `b5ef98a` on 2026-11-05, after the final whole-branch review and its fixes. Their reports are
below as they gave them, shortened where they quoted file text; nothing here quotes a path or
address a probe found. The decision on each finding follows in [Decisions](#decisions), written
after these reports were committed.

## Goal fit and scenarios

0 critical, 3 important, 3 minor. Phase 1 delivers its outline row but for "the live site", which
waits for the merge (S10, step 9). Every Dan answer (kickoff 1 to 18, Phase 1 1 to 6) is honoured;
no binary changed after Dan OKed it by name.

1. **Important:** S09 and S18 say "built", but S09 is Dan printing the coupon (Phase 2, Task 1) and
   S18 the light hanging for two days (Phase 2, Task 4); S08's proof names a browser check that
   can't happen before the merge. Fix: split each into a Phase 1 part (built) and a Phase 2 part
   (planned).
2. **Important:** Q&A 12 says each page names `dowel_d` and `clearance`, but the generated "For
   another size" note names only the parameters `sizes` changes (`dowel_d`). The clamp's notes
   never mention `clearance`, and the two parts default to different values (0.2 and 0.4 mm)
   unexplained. Fix: name `clearance` in the note; one sentence in the clamp's notes.
3. **Important:** Phase 2 prints the unchanged parts in PLA and tunes them before Dan's changes are
   known, so a likely redesign means a second round. Fix: ask at Phase 2's Task 1 what he already
   knows he'll change; say plainly what the look test judges; set the coupon's `status: printed`
   once printed.
4. **Minor:** the wall block's page gives a size that includes the two caps beside it.
5. **Minor:** the viewer's first camera position crops the cord clamp's bottom edge.
6. **Minor:** the wall block's `clearance` of 0.4 mm isn't flagged as a placeholder, as the clamp's
   `cord_d` is.

## Reliability

0 critical, 2 important, 8 minor. Probed with the real `solidcraft-cli` 0.30.1 in a scratch copy;
CI green on the branch.

1. **Important:** a typo in a size's parameter name builds without error and gives the base
   geometry under the size's name (the CLI exits 0 for an unknown parameter), so the site would
   offer a wrong "3/4 in" download with every check green. Fix: check each size's parameter names
   against the design's.
2. **Important:** two sizes can write the same file (`3/4 in` and `3-4 in` both give `-3-4in.stl`),
   and a size can reduce to an empty name. Fix: reject a model whose size names collide or are
   empty.
3. **Minor:** a folder with a `model.yml` but no `.sc` is skipped without a word.
4. **Minor:** `make models-check` doesn't validate `model.yml`'s fields; only `make docs` does, so a
   bad one passes CI's tests job and fails its site job.
5. **Minor:** `uv sync --frozen` doesn't notice `pyproject.toml` drifting from `uv.lock`; CI could
   use `--locked`.
6. **Minor:** no `.gitattributes`, so a line-ending rewrite of a text `.sc`, `eval.json` or
   `build.json` on another machine changes its hash.
7. **Minor:** `make strip` refuses a HEIC with no conversion route in the README.
8. **Minor:** the privacy check can't read inside a zip-format `.sc`; the README says such a design
   builds.
9. **Minor:** the CLI version in `build.json` is never compared; a mismatch could warn.
10. **Minor:** `run()` has no timeout; the history scan holds every blob in memory (fine at today's
    size).

Fine: a no-sizes model; a failed size build leaves no record; the Ubuntu job; fork PRs; the merge
to `main` (the ruleset's three checks named as the jobs are); photo names with spaces.

## Security and privacy

0 critical, 1 important, 5 minor. **Checklist:** secrets fine; permissions fine; network exposure
fine; failing closed, a finding (1); injection, a finding (3); logging fine. Probes of
`make privacy` caught text chunks, home paths in text, binaries, a JPEG's tail, symlinks, history
and an unreadable format.

1. **Important:** a PNG with an unknown private chunk, or with bytes after its end, passes: Pillow
   ignores both, so `info` is empty. Fix: allow only a known list of PNG chunks and nothing after
   the end; for JPEG, nothing after the end marker. No photo is on the branch, so nothing leaks
   today.
2. **Minor:** only blobs are scanned for home paths, not commit messages, author lines or tag
   messages (the real history's only hits are `<name>` placeholders).
3. **Minor:** a model's free text (notes, title, status, material) goes into its page raw, so a
   `model.yml` holding raw HTML, a shortcode or an executable cell would be rendered or run. Fix:
   escape it as the doc copies are.
4. **Minor:** the commits' author address is a personal email, public in the history; Dan's choice,
   and a noreply address would avoid it for future commits.
5. **Minor:** Dependabot's security updates are off (version updates are on); a repo setting.
6. **Minor:** the uv version `setup-uv` installs isn't pinned (the lockfile's hashes still protect
   the dependencies).

Fine: no home path, host name, local path, LAN address or place in any tracked file; the PNGs carry
no metadata; the STL headers name only the model; CI and the settings (forks read-only, deploys
from `main` only, actions SHA-pinned and allow-listed, the ruleset).

## Simplicity

0 important, 10 minor. The branch is lean; the run's growth (the history scan, the invalid and
stale split, `make strip`) is each close to the simplest thing that does its job.

1. **Minor:** `path_problem` is a one-line wrapper; inline it.
2. **Minor:** the history pass's de-duplication costs six lines and a test; keep it.
3. **Minor:** `build.json`'s `design` field is never read.
4. **Minor:** `ModelError` only re-wraps `ValueError`.
5. **Minor:** `make hooks` is a no-op until the hooks exist (AGENTS.md names it).
6. **Minor:** `tests/test_makefile.py`'s target list repeats `.PHONY`.
7. **Minor:** three symlink tests and a line-ending test probe one pattern boundary; parametrize.
8. **Minor:** the JPEG-comment strip test overlaps the metadata strip test.
9. **Minor:** the zip-design test adds little beyond documenting that designs aren't parsed.
10. **Minor:** `make check` runs the suite twice locally; `test-utc` could be a flag.

## Decisions

Written after the reports above were committed.
