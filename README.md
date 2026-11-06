# 3d-models

3D-printable models designed in [SolidCraft](https://solidcraft.io/), with the STL files exported
from them. Most are vibe coded: an agent builds the design and the tooling, and a person prints it
and says what works.

The first project is a wall sconce for a grow light: a 1-inch wooden dowel and printed parts, in a
Japandi style, holding a lamp 16 to 20 inches out from a corner wall.

**Gallery:** <https://chendaniely.github.io/3d-models/>. Every model has a page with a 3D view you
can turn, its picture, its measurements and print settings, and the `.stl` and `.sc` files to
download.

**Status:** Phase 1 (the build pipeline, the site and a first model) is being built on `phase-1`;
the gallery and the `make` targets below arrive when it merges.

## Using a model

Download the `.stl` from the model's page, or from `models/<slug>/` here, and slice it with your
own printer's settings; the model's page says which material, orientation and supports it needs.
The `.sc` file opens in SolidCraft, where every dimension is a named parameter you can change.

## Working on it

Every command is a `make` target; `make help` lists them.

```bash
make help     # list the targets
make models   # rebuild each changed design's STL, picture and measurements (needs SolidCraft)
make check    # everything CI runs: tests, lint, the model and photo checks, the leak scan, the site
make docs     # render the site into website/_site
```

You need [uv](https://docs.astral.sh/uv/), [Quarto](https://quarto.org/) 1.11.6,
[gitleaks](https://github.com/gitleaks/gitleaks) and, for `make models`, SolidCraft's
`solidcraft-cli` 0.30.1.

## How it's built

The design spec, the phase plans and every decision are in `docs/superpowers/`, and on the site's
[Design](https://chendaniely.github.io/3d-models/design.html) page. The rules every agent session
follows are in `AGENTS.md`.

The models are original designs. The dowel system is inspired by Lofted Goods'
[The Rail](https://loftedgoods.com/); none of their files are used here.
