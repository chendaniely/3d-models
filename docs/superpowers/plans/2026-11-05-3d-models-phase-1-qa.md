# 3d-models Phase 1: questions and answers

Questions that came up while Phase 1 ran, each with Dan's answer in his words. Kickoff's are on the
[kickoff Q&A page](../specs/2026-11-05-3d-models-qa.md).

| # | Question | Answer | Dan's reason, in his words |
|---|---|---|---|
| 1 | Dan's changes to the sconce's parts, before Tasks 7 and 8 build them: he said, mid-run, "once you're done with everythign let me know there are some changes i want to make with the way the dowels mound and clap to the pice and screw into the wall" | Build Tasks 7 and 8 as planned first; his changes come afterwards, as a revision of both parts | No reason given (not the recommended option, which was to describe them before the build). |
| 2 | Pushing `phase-1` after Task 6: 16 commits, adding the coupon's three STLs and its PNG, which both Task 6 reviewers inspected | Pushed then, after `make leaks privacy` passed; later pushes still ask | No reason given (the recommended option). |
| 3 | Pushing `phase-1` after Task 8: the commits of Tasks 7 and 8 and the CI fix, adding the wall block's and the cord clamp's STLs (three sizes each) and PNGs, which their reviewers inspected | Pushed then, after `make leaks privacy` passed, so CI confirms the lychee fix | No reason given (the recommended option). |
| 4 | When Dan's changes to the wall block and the cord clamp go in | After the look test: the parts stay as built for Phase 1, and his changes go into Phase 2, once he has printed the PLA parts and held them up in the corner | Not the recommended option (describe them now); no reason given. |
| 5 | The rest of Phase 1 | Run it all: every push from here to the merge, the phase end, the PR and its merge, without asking again | "push merge. do the whole shebang!" |
| 6 | The GitHub settings (Task 9) | The agent applies all five with `gh`: Pages from GitHub Actions, deploying from `main` only; Actions with a read-only default token, GitHub's own actions plus setup-uv and quarto-actions only, SHA pins required; merge commits only; a ruleset on `main` (a PR, the `tests`, `leaks` and `site` checks, no force push or deletion); the website field and the topics 3d-printing, solidcraft and vibe-coded | No reason given (the recommended option). |
