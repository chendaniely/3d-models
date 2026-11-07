# 3d-models Phase 2: questions and answers

Questions that came up in Phase 2, each with Dan's answer in his words. Phase 1's are on
[Phase 1's Q&A page](2026-11-05-3d-models-phase-1-qa.md), kickoff's on the
[kickoff Q&A page](../specs/2026-11-05-3d-models-qa.md).

## Dan's changes to the parts (2026-11-06)

After Phase 1 merged, Dan brought his changes to how the dowel mounts forward, before anything is
printed. His reference is LoftedGoods' Rail v2 and its Grow Light for the Rail, on Thangs, in his
words: "each piece slides into the rail and is held by a wedge piece, so it has a clean look.
things then mount onto the rail using some kind of matching joint piece. i'm hoping to have a lamp
that looks like his grow light setup but i need the light to reach out farther". Both of those
models are members-only downloads, and neither page states a licence, so this project's parts are
its own design using the same ideas (wall feet, a wedge, a sliding joint), not his files, and they
won't fit his pieces. His light asks for 9 or 10 W bulbs; Dan's Barrina is 25 W.

The batch: (1) what the light's arm attaches to; (2) how far out the light reaches; (3) a printed
shade or the bare bulb; (4) when the redesign happens.

| # | Question | Answer | Dan's reason, in his words |
|---|---|---|---|
| 1 | Scenario: Dan hangs the light above his plants. What does its arm attach to? | A vertical dowel rail on two wall feet whose screws are hidden, like LoftedGoods'; the light's arm attaches with a slide-on joint locked by a wedge, so its height adjusts, and planters can share the rail. Not chosen: the arm straight out of one wall foot (today's layout, restyled), or a horizontal rail along the wall | The recommended option; his reason is his message above. |
| 2 | Scenario: Dan cuts the arm's dowel and slides the light's joint onto the rail. How far from the wall should the light hang? | Up to 24 inches (about 60 cm), past the spec's 16 to 20: the joint gets a longer sleeve to resist the extra pull, and the load test is done at 24 inches. Not chosen: 16 to 20 inches as the spec says (the recommended option), or about 12 inches | Not the recommended option; no reason given. |
| 3 | Scenario: the arm is up and Dan looks at the end where the light is. What does he see? | A printed shade fixed under the arm's tip, like LoftedGoods': the bulb inside it with an air gap of at least 10 mm and vents at the top, printed in PETG for the 25 W bulb's heat, the cord running back along the arm to the rail; its size waits on Dan's measurement of the bulb (Task 1). Not chosen: the bare bulb hanging on its cord from a slide-on hanger, or the socket held rigid under the tip with no shade | The recommended option; no reason given beyond his message above ("a lamp that looks like his grow light setup"). |
| 4 | Scenario: Phase 2 starts tomorrow. When does the rail redesign happen? | Now, in Phase 2, replacing Phase 1 Q&A 4's "after the look test": Phase 2's plan is rewritten at its start; measuring the dowel and the bulb and printing the coupon stay first; the wall feet, the sliding joint and its wedge, the arm's tip and the shade replace "tune the parts"; then the look test, a load test at 24 inches and the install. Phase 1's wall block and cord clamp stay in the repo, marked superseded. Not chosen: a look test of today's parts first, or a Phase 3 of its own | The recommended option; no reason given. |
| 5 | Scenario: the rail is on the wall and the light is up. What else hangs on it, and how long is the rail? (The spec's builder check asked: the feet were sized for the light alone.) | The light and up to two small planters, about 2 kg each when watered, on a rail up to about 48 inches held by two feet; the feet are sized for that total, and the load test hangs it. Not chosen: the light alone on a 36-inch rail, or a rail up to 72 inches with several planters and a third foot | The recommended option; no reason given. |
| 6 | Scenario: Dan has read the revised spec (`796dbb1`, `62d8997`) and the agent's calls listed for him: seven `rail-` parts; the feet's closed cups, keyholes, depth gauge and hidden stop against lifting; the carrier on from the front with its wedge behind the rail, or from the rail's end if that can't hold; the arm socket 51 mm deep with its own wedge; the shade's 10 mm gap, vents and 60 °C rule (S30); the load test's marks (S13); Phase 1's parts kept, superseded. What happens next? | Approved as written: Phase 2's plan is rewritten for the rail at its start, its council reads it, and the run goes on, Dan's measurements and the coupon first. Not chosen: changing something first, or measuring before approving | The recommended option; no reason given. |
| 7 | Scenario: `phase-2` has 8 unpushed doc commits, and Phase 2 will add many more. How should pushes work this phase? | A standing OK: every commit pushed to `phase-2` from now until Phase 2's merge, each after `make leaks privacy models-check` passes; the phase's STLs and pictures still wait for Dan's look by name before its PR merges. Not chosen: asking at each push, or holding everything to the phase's end | The recommended option; no reason given. |
| 8 | Before Task 1 starts, Dan asked for everything on `phase-2` to reach `main` (his instruction, not a scenario question) | A mid-phase PR from `phase-2` into `main`, merged once CI is green: the spec, the Q&A page, the rewritten plan, the council and the new diagrams go live on the site; no binary file goes with it. `phase-2` carries on afterwards, and the phase still ends with its own PR | "let's currently make sure everythign is on main before we build the next phase. so i can view everythign rendered" |
| 9 | Scenario: Dan wants to see the rail's five parts rendered (he asked: "did you redesign the part? i dont' see anythign udpated in the website"). When should they reach the live gallery? | Publish now, retune later: the five parts are built at the guessed sizes, their pages saying which are placeholders, and merged to `main` as soon as they're built; his measurements then retune and rebuild them, and they're published again. Answer 4's measure-first order changes: the privacy task, the five parts, the superseded status, a mid-phase merge, then his measurements and the retune. Not chosen: measuring first and publishing right after building (the recommended option), or only at the phase end | Not the recommended option; no reason given beyond his question above. |
| 10 | Scenario: the 18 files no scan can read (18: 13 STLs and 5 pictures of the rail's five parts, at placeholder sizes) are about to go to the public gallery (Task 8). Does Dan OK them going out? | OK, all 18, by name: `rail-arm-socket-25mm.stl`, `rail-arm-socket-3-4in.stl`, `rail-arm-socket.png`, `rail-arm-socket.stl`, `rail-arm-tip-25mm.stl`, `rail-arm-tip-3-4in.stl`, `rail-arm-tip.png`, `rail-arm-tip.stl`, `rail-carrier-25mm.stl`, `rail-carrier-3-4in.stl`, `rail-carrier.png`, `rail-carrier.stl`, `rail-feet-25mm.stl`, `rail-feet-3-4in.stl`, `rail-feet.png`, `rail-feet.stl`, `rail-shade.png`, `rail-shade.stl`. Each STL's header holds only "SolidCraft STL" and its model's name; the pictures are renders with no metadata. Not chosen: some held back, or all held | The recommended option; no reason given. |

## The store gauges (2026-11-06)

Before buying the dowels, Dan asked for a gauge to carry to the store, in his words: "[two
hardware stores near him] has a few dowel sizes, can we create a small thing grid that i can take
to the store and measure all of them? for tollerances. we only need the larger-ish sizes from half
inch to 2 in really. and the printer i have is a bambu p2s printer." (The stores' names and
neighbourhood are left out of this public page.) His Bambu P2S prints up to 256 mm square, so a
row of 2-inch holes at several clearances doesn't fit on one plate. He then asked: "i do plan to
sand and apply finishing to the dowels in the final setup. would that change the
thickness/tolerances when i'm measuring?" The agent's answer: yes, by tenths of a millimetre both
ways (sanding takes about 0.1 to 0.3 mm off the diameter, a film finish adds about 0.05 to 0.1 mm
a coat, and a dowel's diameter moves by about 0.1 to 0.25 mm between a dry winter and a damp
summer), so the store measures, and the fit is tested after the finishing (decided without Dan,
3).

The batch: (11) what kind of gauge goes to the store.

| # | Question | Answer | Dan's reason, in his words |
|---|---|---|---|
| 11 | Scenario: at the store Dan pulls out a dowel labelled 1 inch that's really 25.1 mm and a bit oval; at home he sands and finishes it, then wants to know how much it changed. Which gauge is in his pocket? | Both, as two models he prints: a taper card, one plate with two tapered windows, 12 to 32 mm and 31 to 52 mm, read in millimetres and in inch sizes where the dowel stops, checked against a coin; and a hole grid, each inch size from 1/2 to 2 inches with holes from 0.6 mm under to 0.4 mm over in 0.2 mm steps, marked by dots, on several bed-sized plates. Not chosen: one hole per size, each exactly its label | The recommended option (the taper card), and the hole grid as well: "let's make models for both i'll print both the taper card and hole grid" |

## The gauges before printing (2026-11-07)

Before printing them, Dan opened the taper card's and the hole grid's STLs in his slicer: "i'm
looking at the dowdel-hole grid stl file and the taper card. there's a lot of whitespace in the
print, can we reduce the whitespace so i can print both of them on 1 plate on my bambu p2s? they
currently ALMOST fit on 1 plate". The card was 251 by 161 mm and the 1-inch tile 93.4 by 91.6 mm:
side by side, 252.6 mm of the plate's 256, with no room for the slicer's spacing. While the trim
built, he asked about the numbers and the gauges' thickness (13 and 14).

| # | Question | Answer | Dan's reason, in his words |
|---|---|---|---|
| 12 | Dan asked for the taper card and a hole-grid tile to fit on one plate (his instruction, not a scenario question) | The card's bands outside its windows go from 20 to 15 mm and the strip between them from 30 to 28 mm, so it is 251 by 149 mm; each tile's strips under its rows of holes go from 10 to 8 mm, so the 1-inch tile is 93.4 by 87.6 mm. The card and the 1-inch tile fit across the P2S's 256 mm plate 5 mm apart and 5 mm from its front and back edges, the tile at the back left, clear of the printer's wrapping-detection zone at the back, right of centre (Bambu Studio's P2S profile: x 153 to 216 mm, y 235 to 256). The windows, the taper, the ticks and the holes don't change; every word stays at least 2 mm inside the card's edges and from the next row of words, and each hole's number 2 mm inside the tile's edge (Task 10, step 0a) | "there's a lot of whitespace in the print, can we reduce the whitespace so i can print both of them on 1 plate on my bambu p2s? they currently ALMOST fit on 1 plate" |
| 13 | Dan asked whether the numbers are good enough cut into the top, and for them raised, so a second colour can print them with one colour change at most (his instruction, not a scenario question) | The agent's view: cut 0.6 mm into one colour, the numbers show only where light catches their edges, which a store's overhead lights do poorly; it's the colour, more than the height, that makes them easy to read. So every tick, number and name stands 0.8 mm (four 0.2 mm layers) on the top face, and nothing else rises above it: one filament change at the first layer above the top prints all of them in a second colour, white on a black gauge, and without it they print in one colour. Not offered: the lettering in a file of its own, to give its own filament, which a change by layer doesn't need, with an AMS or without (Task 10, step 0b) | "for the numbers on the top, do you think they're okay with it just inset? can we make them proud with an option to let the proud parts be a different color? e.g., i can print the guide in black and use white for the proud numbering. also build it to minimize color changes, i should only need 1 color change if needed" |
| 14 | Dan asked for the gauges as thin as stiff enough allows, to print faster (his instruction, not a scenario question) | Both 4 mm thick, from 6, under their 0.8 mm of lettering. A printed slab's stiffness comes mostly from its solid top and bottom layers (about 1.0 and 0.6 mm in Bambu's standard profile), so at 4 mm the card keeps about four-fifths of its stiffness in its own plane, where a dowel pushes a window's sides apart, and about two-fifths across it, still rigid in the hand at 251 mm long; each gauge prints 10 fewer of its 22 sparse layers. 3 mm would keep about a fifth across the plane: a card that flexes as it's held. A thinner window also pinches a tilted dowel less, so it reads closer to true, and a 4 mm hole still gives a clean go or no-go (Task 10, step 0b) | "think about the thickness (z axis) of the parts as well. let's optimize so they are stiff enough but also thin enough so it prints faster" |

## Decided without Dan

The mode is fully vibed, so a change to one of Dan's decisions or an approved design call is ruled
on, logged here, and named in the next briefing.

| # | Decision | Why | What it costs if wrong |
|---|---|---|---|
| 1 | The wall feet have no keyhole and no depth gauge, which the calls Dan approved in answer 6 listed. Each foot is screwed through its plate where the rail stands in front of the screw, under a printed cap; the top cup is deep, so the rail lifts into it past the bottom cup's rim; and a screw up through the bottom cup's floor into the rail's end holds the rail down. | The phase-start council found a keyhole only stops a foot dropping. Lifting a carrier or a planter raised the rail, pushed the top foot up off its screw, and the rail could then lean off the wall with the light on it (critical: goal fit 1, reliability 1). | Two small round caps show behind the rail, where a keyhole showed nothing; the look test (Task 9) judges them. |
| 2 | Scenario S27 proves the arm tip's stem: the light hangs by its cord from the stem's grip for 48 hours, at three times its weight, and slips under 2 mm. | Answer 4 retired S27 with the cord clamp, but the stem's grip is a cord clamp too, and the load test already judges it (goal fit 8). | Nothing: it restores a check. |
| 3 | The coupon is tried on the dowel after Dan sands and finishes it, not before, and the parts' `clearance` is one coupon step looser than the tightest hole the finished dowel goes into by hand; the coupon's page and S26 say so. | Dan plans to sand and finish the dowels (above): the fit that matters is the finished dowel's, and a dowel swells in damp weather. The carrier and the arm socket lock with wedges, which take up a hole a little loose; nothing takes up one too tight. | A joint a step looser than it needs to be, its wedge pushed a little further in; the load test shows whether it holds. |
| 4 | The taper card's scales read 12 to 34 mm and 32 to 52 mm, its windows tapering 0.11 mm per mm, not the 12 to 32 and 31 to 52 at 0.1 that answer 11 described. | A round dowel reaches about half its diameter past where it touches the window's sides, so the first card couldn't read 2 inches or 1 1/4 (Task 9's review); the windows had to run past their scales, and a steeper taper keeps the card on the P2S's plate. | Ticks 4.5 mm apart where 5 were described; a tenth of a millimetre is still about a millimetre between them. |
