# 3d-models: notes from the kickoff session

These notes are from 2026-11-05. They carry what the kickoff conversation found, so the spec can be
written from the repo alone. Dan's answers are on the Q&A page,
[`2026-11-05-3d-models-qa.md`](2026-11-05-3d-models-qa.md). Everything else here is the agent's
analysis, and Dan has not approved it.

## What Dan wants

- **A wooden dowel planter system for his home, in a Japandi style:** wooden dowels joined by
  3D-printed parts, in the spirit of Lofted Goods' The Rail ([loftedgoods.com](https://loftedgoods.com/),
  [designs on Thangs](https://thangs.com/designer/LoftedGoods)). The parts here are original
  designs; none of Lofted Goods' files are copied.
- **The first piece is a wall sconce for a grow light.** It goes in the corner of a room where a
  monstera and a rubber plant stand. The lamp kit is a grow bulb in a socket on a cord, and it
  must hang 16 to 20 inches (406 to 508 mm) out from the wall, so the arm is a cantilever.
- **Dan's doubt:** "i'm essentially trying to mount some kind of wall sconce setup. but not sure
  if it'll look good with 3d printed parts and dowels"
- **The repo covers more than the sconce:** every SolidCraft model Dan makes and the STL files
  exported from it (Q&A, answers 3 and 4).

## Feasibility of the sconce arm

**It's feasible.** The dowel isn't the weak point; the printed joint at the wall and the anchors
behind it are.

The worst case modelled is a 1 kg (2.2 lb) lamp at the tip of a 20-inch arm, with these
assumptions:

- a generic hardwood dowel: E = 10 GPa, bending strength 70 MPa (poplar or birch; oak is stiffer
  and stronger);
- the arm's own weight included;
- long-term sag twice the first-day sag (wood creeps under a constant load).

| Dowel | First-day sag | Long-term sag | Strength margin |
|---|---|---|---|
| 5/8" | 14 mm | about 28 mm | 5× |
| 3/4" | 7 mm | about 14 mm | 9× |
| 1" | 2 mm | about 4.5 mm | 21× |

At 2 kg, a 1-inch dowel sags about 4.3 mm on the first day, with an 11× margin. Lofted Goods' The
Rail uses a 1-inch (25 mm) dowel, so 1 inch also keeps the parts compatible with it
([The Rail](https://thangs.com/prints/designer/LoftedGoods/3d-model/The%20Rail-1144868),
[The Rail v2](https://thangs.com/designer/LoftedGoods/3d-model/The%2520Rail%2520v2-1397922)).

**The weak points, in order:**

1. **The printed wall joint carries the whole moment, about 5 N·m (44 lbf·in).** It needs:
   - a socket at least 2 inches deep;
   - a pin or bolt through the dowel;
   - PETG or ASA, not PLA, because PLA creeps under a constant load and softens around 55–60 °C
     near a warm bulb base;
   - a print orientation that doesn't pull its layers apart.
2. **The wall anchors.** In a straight cantilever, the top screw is pulled out with about 54 N
   (12 lbf) when the screws are 100 mm apart vertically, or 90 N (20 lbf) at 60 mm. A stud or a
   toggle anchor is needed; a plastic plug in drywall isn't enough.
3. **Twisting when bumped:** a flat plate with at least two screws stops it.

**Three builds:**

- **Straight cantilever:** the cleanest line, and fine with a 1-inch dowel.
- **Knee brace:** a diagonal dowel meeting the arm about 12 inches out. The anchor pull drops to
  about 17 N, at the cost of a second line.
- **Corner span:** one dowel from wall to wall across the corner, supported at both ends. It sags
  about 2 mm over a 50-inch span, but fixes the light on that diagonal.

## How it can look good

The agent's advice to Dan, not yet his decision:

- **Quiet printed parts:** matte filament in black, bone white or a clay tone; no layer lines on
  the faces you see; every edge rounded to the same radius.
- **Good wood:** oiled oak or ash, not a pale pine or poplar big-box dowel.
- **The cord:** a cloth cord in black or natural, routed on purpose.
- **The bulb matters most:** a full-spectrum white grow bulb in a shade, not a bare pink or purple
  red/blue bulb.

Glossy PLA, bulky blocks and visible screws make it look cheap.

## Tools found on this machine

- **SolidCraft**, driven through its MCP server while the app runs, so Dan watches the model being
  built.
  - The MCP `save` tool writes only into SolidCraft's own folders unless the server is started
    with `--allow-path` (Q&A, open items).
- **`solidcraft-cli`**, headless. From its `--help`:
  - `run design.sc --out part.stl` exports a design;
  - `snapshot design.sc --out shot.png` renders a picture;
  - `eval design.sc --json-out FILE` measures a design;
  - `script design.sc --out script.json` writes a design's history as a replayable script.

  A `make models` target can build the STL, a picture and the parameters for every `.sc` file.
  The format of `eval`'s output hasn't been checked yet.
- **`export`** writes STEP, 3MF, STL (binary or ASCII), OBJ and URDF.
- **Browsers can't read `.sc`.** The gallery renders each model's exported STL, for example with
  three.js' `STLLoader`, and links the `.sc` and `.stl` files for download.
- **Also installed:** Quarto 1.11.6, gitleaks 8.30.1, uv, node and gh (logged in).

## The agent's proposed next steps (not yet Dan's)

1. **The rest of kickoff,** without more questions (Dan: "oneshot the rest of the repo"):
   - the spec;
   - the root files: `AGENTS.md` from the plan-driven-development template, `CLAUDE.md`,
     `README.md`, `CHANGELOG.md`;
   - the phase plans.
2. **Phase 1, the repo itself:**
   - CI;
   - the Quarto docs site on GitHub Pages, doubling as the gallery, with a 3D viewer on each
     model's page;
   - `make models`;
   - a first model: a dowel fit-test coupon, a bar with holes at +0.2, +0.4, +0.6 and +0.8 mm over
     the dowel's diameter. The sconce needs it anyway, because dowels vary by about ±0.5 mm.
3. **Phase 2, the wall sconce:**
   - weigh the lamp and measure the corner;
   - choose the build;
   - design the wall block, the arm-tip cord holder and any brace joints;
   - make a test print and load-test it with 3× the lamp's weight for 24–48 hours;
   - install it.
