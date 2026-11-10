# Changelog

## 2026-11-09: Phase 2, the rail's parts and the store gauges

- **The rail's five parts:** wall feet, a carrier, an arm socket, an arm tip and a shade, on the
  gallery at placeholder sizes. They are designs, not yet printed or load-tested.
- **Two gauges for reading a dowel:** a taper card, and a hole grid with a tile for every 1/8 inch
  from 1/2 to 2 inches. The card and a tile up to 1 inch share a Bambu P2S's plate; they are 4 mm
  thick, with raised numbers that one filament change prints in a second colour.
- **Paused:** measuring, tuning, testing and installing the rail (Phase 2 Q&A 15). Its steps stay in
  the plan, and their scenarios are on the spec's Later list.
- **The checks:** `make privacy` looks inside a JPEG's segments and refuses more that could carry
  text; `make docs` fails if a page would load anything from another host, and the site's fonts and
  scripts are now served from the site itself.
- **Superseded:** Phase 1's wall block and cord clamp stay on the gallery, marked as replaced.

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
