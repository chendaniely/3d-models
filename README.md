# 3d-models

3D-printable models designed in [SolidCraft](https://solidcraft.io/), with the STL files exported
from them. Most are vibe coded: an agent builds the design and the tooling, and a person prints it
and says what works.

The first project is a grow-light rail: 1-inch wooden dowels and printed parts, in a Japandi style.
A vertical rail stands on two wall feet with no screw in sight, and an arm wedged onto it holds the
light up to 24 inches out from a corner wall, under a printed shade.

**Gallery:** <https://chendaniely.github.io/3d-models/>. Every model has a page with a 3D view you
can turn, its picture, its measurements and print settings, and the `.stl` and `.sc` files to
download.

**Status:** Phase 1 has merged: the gallery is live, with the fit-test coupon and the sconce's
wall block and cord clamp. Phase 2, under way, replaces those two with the rail's five parts, then
prints, tests and installs them.

## Using a model

Download the `.stl` from the model's page, or from `models/<slug>/` here, and slice it with your
own printer's settings; the model's page says which material, orientation and supports it needs.
The dowel parts come in STLs for 3/4-inch, 25 mm and 1-inch dowels. The `.sc` file opens in
SolidCraft, where every dimension is a named parameter you can change, the dowel's diameter
included.

## Working on it

Every command is a `make` target; `make help` lists them.

```bash
make help     # list the targets
make models   # rebuild each changed design's STL, picture and measurements (needs SolidCraft)
make check    # everything CI runs: tests, lint, the model and privacy checks, the leak scan, the site
make docs     # render the site into website/_site
```

You need [uv](https://docs.astral.sh/uv/), [Quarto](https://quarto.org/) 1.11.6,
[gitleaks](https://github.com/gitleaks/gitleaks) and, for `make models`, SolidCraft's
`solidcraft-cli` 0.30.1.

## Adding a model

1. Make a folder `models/<slug>/`, its name lowercase words joined by hyphens: it becomes the
   page's address.
2. Save the design there as `<slug>.sc`, in SolidCraft's plain-text JSON format: a diff can read
   it, and the privacy check reads only plain-text designs (one saved in the default zip format
   builds too, but nothing checks inside it).
3. Write `models/<slug>/model.yml`:

   ```yaml
   title: Wall hook
   summary: One sentence, shown on the gallery's card.
   status: designed          # designed, printed, in use or superseded
   material: PETG
   size: 1 in                # with sizes below: the size the design is saved at
   sizes:                    # optional: one more STL for each, by changing parameters
     3/4 in: {dowel_d: 19.05 mm}
   print:
     Orientation: flat on its back
     Supports: "no"          # quote yes and no, or YAML reads them as true and false
   notes: |
     Anything someone printing it should know.
   ```

4. `make models`, then `make check`, and commit the folder. A photo of a print goes in
   `models/<slug>/photos/` as a JPEG, PNG or WebP. Convert a HEIC to JPEG first (on a Mac,
   `sips -s format jpeg IMG_0001.HEIC --out IMG_0001.jpg`), then strip it with
   `make strip FILES=<file>`; then look at the photo for anything that shows where you live (a
   window's view, a street, a house number, a face, a reflection, a screen) before committing it.

## How it's built

The design spec, the phase plans and every decision are in `docs/superpowers/`, and on the site's
[Design](https://chendaniely.github.io/3d-models/design.html) page. The rules every agent session
follows are in `AGENTS.md`.

The models are original designs. The dowel system is inspired by Lofted Goods'
[The Rail](https://loftedgoods.com/); none of their files are used here.

## Licence

The models, their pictures and the docs are
[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/): print them, change them and share
them, crediting chendaniely and linking here, but don't sell them or prints of them
(`LICENSE-MODELS.md`). The code is MIT (`LICENSE`).
