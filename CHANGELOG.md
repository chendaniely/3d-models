# Changelog

## 2026-11-05: Phase 1, the repo and the first models

- **The pipeline:** `make models` builds each changed SolidCraft design into its STL, an STL per
  dowel size, a picture and its measurements, judging freshness by every file's SHA-256, and refuses
  a model it can't build right; `make models-check` names a stale or invalid one.
- **The privacy guard:** `make privacy` refuses any image holding more than a picture needs (in the
  working tree and in the history), photo and video formats it can't read inside, and home-folder
  paths; `make strip FILES=…` cleans a photo.
- **The site:** a Quarto gallery on GitHub Pages, a page per model with a 3D viewer (three.js, served
  from the site), an STL for 3/4-inch, 25 mm and 1-inch dowels, print settings, measurements and the
  licence; the design docs, Architecture diagrams, changelog and the agent's rules.
- **The models:** the dowel fit-test coupon, and the grow-light sconce's wall block and cord clamp,
  designed and not yet printed.
- **CI:** tests, lint, the model and privacy checks, a leak scan over every commit and the site's
  render and link check on every push; every action pinned to a commit SHA; the site deploys from
  `main`. The repo's settings: Pages, limited Actions, merge commits only, a ruleset on `main`.

## 2026-11-05: kickoff

- The repo: one public home for every 3D-print project, SolidCraft designs and the STL files
  exported from them, with a docs site that doubles as the gallery.
- The design spec, two phase plans (Phase 1: the repo, its pipeline, the dowel fit-test coupon
  and the sconce's wall block and cord clamp, each in three dowel sizes; Phase 2: tuning, testing
  and installing the grow-light wall sconce), the kickoff's Q&A page and council, and the agent's
  rules (`AGENTS.md`).
- The licences: CC BY-NC 4.0 for the models and docs, MIT for the code.
