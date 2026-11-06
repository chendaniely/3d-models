# 3d-models Phase 2: the phase-start council

Four read-only reviewers, one per lens, read Phase 2's plan as rewritten for the grow-light rail
(uncommitted, 2026-11-06), with the spec's edits, against the code Phase 1 built and the scratch
clones where every listing had been run. Their reports are below as they gave them, their headings
moved down a level. The decision on each finding follows in [Decisions](#decisions), written after
these reports were committed.

## Goal fit and scenarios

1 critical, 9 important, 9 minor.

Lens: whether each Phase 2 scenario has a task and a proof that proves it; whether the plan keeps
Dan's answers (Phase 2 Q&A 1 to 7); whether the parts as designed meet the spec's design calls;
whether Dan can build the rail from the model pages' notes alone; and whether the task closes,
scenario statuses and forward rewrites agree with each other. "Plan" is
`docs/superpowers/plans/2026-11-05-3d-models-phase-2.md` (uncommitted), "spec" is
`docs/superpowers/specs/2026-11-05-3d-models-design.md`. Geometry comes from the plan's listings
and from proto2's `*.eval.json` (the two agree).

**What I ran:** the five rail tests in proto2 (`pytest -p no:cacheprovider`, 41 passed); each
dowel part evaluated at 19.05 mm and 25 mm (`solidcraft-cli eval` with `parameters.change` on
proto2's `.sc`, output under `council/goal-fit/`; every body closed); and arithmetic on the
evaluated parameters (sight lines, screw spacing, wedge seats, the shade's gap). I looked at the
five built pictures, the `rail/shots/` views and the concept sheet Dan approved. Everything else
was read.

### Findings

#### 1. The top foot has no stop against lifting, so a carrier slid up can unhook it and the rail can lean off the wall

**Severity: Critical** (breaks a safety property, S14's "the feet stay on their screws"; the
design call Dan approved in Q&A 6 as a "hidden stop against lifting" isn't there).

**Where:** spec line 165 ("the rail's top, touching its cup, stops a bump lifting it off"); plan
lines 791 to 794 (the notes: "with the rail's top touching its cup, the foot can't lift off
again"); the test at plan lines 691 to 693.

**Why:** the top foot is printed with its keyhole slot below the entry (slot z' 14 to 26, entry at
26) and installed upside down, so the slot runs up from the entry: the foot drops 12 mm to hook on
and lifts 12 mm to unhook. The rail's top touches the cup's floor from below, so it stops the foot
dropping, not lifting. Nothing above the foot stops a lift. A likely trigger in normal use: Dan
knocks the carrier's wedge out and slides the light up to the top of the rail. The carrier's top
face (radius 12.9 to 17.9 mm) meets the cup's rim (12.9 to 16.9 mm) and pushes the foot up to the
entry, and the wedged carrier then holds it there. The arm's moment, about 7.5 N·m, puts an
outward reaction of about M/L, 6 N, on the top foot. The head is now in the 11.5 mm entry, so
the foot can move away from the wall. The bottom cup's 0.4 mm clearance over its 30 mm depth lets
a 48-inch rail's top swing out about 16 mm, and the foot needs about 7 mm to clear the head. The
rail then leans out with the light on it, held only by the bottom cup. The test at 691 to 693
(`cup_depth >= travel + 10`) shows that the foot can be fitted with the rail in its cup. It
doesn't show a stop.

**Fix:** make the stop real, as a ruling logged on the Q&A page and the spec's sentence rewritten.
There are two cheap ways. (a) Swap the fixings. Hang the *bottom* foot on the blind keyhole: the
rail, the light and the planters all sit in it and hold it down on its head. Screw the top foot
through a tab below its cup, where the rail hides the screw, and cut the top cup deeper (for
example 55 mm against the bottom's 30) so the rail goes in by pushing it up into the top cup and
then lowering it. (b) Keep the layout but add a fixing that a lift can't undo. Either way, add a
line to S14's check (Task 11, step 2): "slide a carrier up against the top foot: it doesn't
unhook."

#### 2. The light head departs from Q&A 3 and the approved design call without a ruling

**Severity: Important** (Dan's decision is changed without the logged ruling the fifth stop
requires in vibed mode).

**Where:** Q&A line 25 ("A printed shade fixed under the arm's tip"); spec lines 183 to 186 ("a
stem down to a shade fixed under it; the bulb's socket held inside"); the concept sheet's panel 7,
which Dan approved in Q&A 6 (the stem enters the shade's top, with the socket inside the shade);
the plan's Task 6 and Task 7, and Task 11 step 2 at line 2066 ("the light swings and settles").

**Why:** as designed, the lamp hangs on its cord below a 40 mm stem and swings. The shade is
clamped at the socket's shoulder, so the socket's body sits above the shade, outside it, exposed
between the stem and the shade. That is a pendant, not a shade fixed under the tip with the socket
held inside. There is a good reason for the change: a closed stem would mean threading the cord,
which its plug and timer can't pass. But the spec's design call wasn't rewritten (the uncommitted
spec diff leaves line 184 as it was), and the Q&A page has no ruling. Dan's main worry is how it
looks, so the light head is the place a silent change costs most. It also makes S11's "nothing but
the dowels and the parts shows" false: the Barrina's socket body shows.

**Fix:** either (a) design what was approved: a collar at the stem's foot that the shade's top
fixes to, with a side slot for the cord, and the socket hanging on its gripped cord inside the
shade, which is also what the "10 mm round the socket" test at line 1616 assumes; or (b) log a
ruling ("the shade hangs from the socket's ring; the lamp is a pendant under the stem"), rewrite
spec lines 183 to 186, and name it in the next briefing so Dan sees it before the look test.

#### 3. Task 1 now comes before Dan's measurements, against Q&A 4 and Q&A 6

**Severity: Important** (two explicit answers changed without a ruling, and the spec is now wrong).

**Where:** Q&A line 26 ("measuring the dowel and the bulb and printing the coupon stay first");
Q&A line 28 ("the run goes on, Dan's measurements and the coupon first"); plan line 13 ("First,
the photo and site gaps…"), line 27 (Now: Task 1), and line 67 onward; spec lines 246 and 251
("Phase 2's first task asks"). The committed plan had the measurements as Task 1.

**Why:** Task 1 needs nothing from Dan, while Task 2 waits on his coupon print and his
measurements. Each task closes before the next starts, so putting Task 1 first delays the one
thing every part waits for. Fixing the site's off-site loads quickly is a fair reason, but it
needs to be a recorded ruling. As it stands, the spec's two "first task" sentences are false.

**Fix:** swap Tasks 1 and 2, which is what Dan answered. If S31's urgency is the reason to keep
Task 1 first, log it as a ruling and send Task 2's list to Dan at the phase's start so the coupon
prints while Task 1 runs. Either way, correct spec lines 246 and 251.

#### 4. The shade's 10 mm air gap is checked only at its two ends

**Severity: Important** (S30 and the spec's "at least 10 mm from the bulb all round"; the PETG
shade is printed before the heat test could catch this).

**Where:** plan lines 1613 to 1617 (the test); 1651 to 1652 (a straight cone from `r_top` to
`r_bottom`); Task 2 step 2 at lines 559 to 560 asks only the widest diameter, the length and a
word for the shape.

**Why:** the shade's inside is a straight cone, and the gap is set only where the cone meets the
socket and the bulb's face. A PAR38-type bulb (121 mm, the guessed size) keeps its full diameter
for some distance back from its face. Measured from the shade's top, the cone's inside radius is
70.8 mm at the face (z 150), 68.3 at z 140 and 64.6 at z 125. If the bulb is 60.5 mm in radius
10 mm or 25 mm back from its face, the gap there is 7.8 mm or 4.1 mm. The flat top ring also sits
just above the LED's heatsink, the hottest part of such a bulb, and nothing checks its distance.

**Fix:** in Task 2 step 2, also ask for the bulb's diameter 10, 30 and 60 mm back from its face,
or how far back its full width runs. Make the shade's profile follow those points plus `gap` (a
revolved sketch, or a cylinder below a cone), and test the gap at each measured height and below
the top ring.

#### 5. The model pages don't say how to put the rail together

**Severity: Important** (Dan, or anyone printing from the gallery, will hit each of these gaps;
the order is only in the plan's Task 11, which isn't on the model pages).

**Where:** the notes at plan lines 783 to 797 (feet), 1017 to 1031 (carrier), 1253 to 1264
(socket), 1494 to 1507 (tip); Task 11 step 1 at lines 2060 to 2064.

**Why:** what's missing, part by part:
- **Where the top screw goes.** The keyhole is blind, so the hole can't be marked through it. From
  the parameters, the top head's final position is 10 mm below the rail's top, and the bottom
  screw is 41 mm above the rail's bottom. So the top screw goes L − 51 mm above the bottom one
  (863 mm for a 36-inch rail, 1168 mm for a 48-inch one). The rail stays in its cup over only
  about −6 to +8 mm of error in that height.
- **The cord in the bottom foot's groove before its screw goes in.** The groove is open toward the
  wall, so once the foot is screwed on it is a closed 7 × 7 mm tunnel the plug can't pass. Task 11
  even lists "the cord pressed into the groove behind it" after the screw.
- **The cord behind the rail before any carrier goes on below the light.** A mounted carrier's
  arms stop 0.3 mm from the wall and close its channel.
- **The arm's length.** Neither the socket's nor the tip's page says to cut the arm to 550 mm for
  the light at 610 mm, or how to work out another reach.
- **The tip's wedge.** The tip's notes never say how it goes in.
- **How each wedge comes out** (S29's "tapped out"). Only the carrier's thin end can be reached,
  from above. The socket's and tip's wedges have to be pulled by their protruding thick ends.

**Fix:** a "Putting it together" section, in order, on the carrier's page (or the feet's), with
one line on each other page pointing to it. Its steps: the cord into the bottom foot's groove;
the bottom screw; the top screw at L − 51 mm, using the gauge; the rail, then the top foot; the
cord behind the rail; the carriers; the socket; the arm at 550 mm; the tip and its wedge; the
clips, the stem and the shade. Task 11 step 1 then follows that section.

#### 6. The arm socket's and the tip's wedges can bottom out on an undersized dowel, and nothing tests it

**Severity: Important** (S29's "doesn't slide or turn" and S13's tilt both depend on these wedges
locking).

**Where:** Review Focus 3 at plan lines 57 to 58 says the wedge's travel covers a dowel 0.5 mm
off, but only Task 4 tests it (lines 934 to 938). The socket's and tip's values are at lines 1206
to 1208 and 1419 to 1421; their tests at 1168 to 1172 and 1395 to 1399 check only the nominal
dowel.

**Why:** both wedges seat 10 mm short of the bore's closed end, which leaves 0.4 mm of room
(`wedge_in − room_in`). Task 4's own model applied to them, at −0.5 mm, gives
(2.4 − 2.0 − 0.5) / 0.04 = −2.5 mm. The thin end hits the closed end before the wedge is tight,
and the arm or the tip is left unlocked. A closer model (the dowel resting on the bore's bottom,
with the coupon's fit) gives the same result for a dowel 0.4 mm under. That is a "1-inch" dowel
that is really 25 mm, a common case, and finding 9(a) shows Task 2 never measures the dowel.

**Fix:** seat both wedges 20 mm short (`wedge_in = room_in + 20 mm * taper`, each wedge 10 mm
longer), and give Tasks 5 and 6 the same `off` test, parametrized over −0.5, 0 and +0.5 mm, that
Task 4 has.

#### 7. The load test, as Task 10 writes it, can't be run or read for two of S13's pass marks

**Severity: Important** (S13 is the phase's gate before the install, and Dan will hit both
problems at the bench).

**Where:** plan lines 1993 to 2005; spec S13 at line 217.

**Why:**
- **The tilt mark.** "Adds under 1 mm at the tip" means 0.2 mm at the 100 mm mark (1 ÷ 4.9). Step
  4 doesn't say what to measure that with, or from what fixed reference. A ruler can't read
  0.2 mm.
- **The 12 kg.** It is to be "hung from the second carrier's dovetail", but there is nothing to
  hang it from: the planter adapter is a Later row (S16), the dovetail is open at both ends, and
  the plan prints only a second carrier. A weight hooked right on the dovetail also sits about
  24 mm off the rail's axis. A pot's centre is nearer 100 mm out, so the hook tests about a quarter
  of a planter's moment on the carrier.

**Fix:** for the tilt, name the tool: calipers or a dial gauge from a block clamped to the bench,
to the arm's underside at 100 mm, read at 0, 24 and 48 hours. For the 12 kg, print a second arm
socket with a short dowel stub and hang the weight on the stub at a stated distance (100 mm), or
say exactly where the hook goes and accept the smaller moment in the log.

#### 8. S27 was retired as "no cord clamp", but the stem's grip is one, and the load test judges it

**Severity: Important** (a factually wrong spec row, and a pass mark no scenario holds).

**Where:** spec line 224 (S27: "superseded …: no cord clamp; S29 checks the joint"); plan lines
1993 to 1995 and 2003 to 2004 (Task 10 hangs three times the weight by the cord through the grip
and passes it at "the cord slips under 2 mm"); the remedies for a failed test at lines 2019 to
2021.

**Why:** the light hangs by friction in the stem's 5.4 mm grip. That is S27's situation, and
S29's hand check of the joint doesn't cover it. The cord-slip mark sits in the plan and in no
scenario. And if the grip slips, none of the listed remedies (a longer carrier, a deeper socket,
the brace, a bigger gap) addresses it.

**Fix:** point S27 at the stem's grip ("the light hangs by its cord from the stem's grip for 48
hours: under 2 mm at the cord's mark", Phase 2, Task 10, planned) by a logged ruling, and add "a
tighter or longer grip" to Task 10's remedies.

#### 9. Task 2 doesn't measure some things the parts depend on, and its close doesn't rewrite them

**Severity: Important** (a user would hit each, and each is a forward rewrite the plan says
happens).

**Where:** plan lines 567 to 570 (steps 6 and 7) and 575 to 582 (the forward rewrites); `cord_w`
at line 733.

**Why:**
- **(a) The dowel's real diameter.** Q&A 4 says "measuring the dowel", but step 7 asks only "the
  size bought". A dowel sold as 1 inch that is really 25 mm makes every hole on the 1-inch coupon
  loose, and it's the case behind finding 6.
- **(b) The screw head's height and type.** Step 6 asks the head's diameter and the shank, but not
  the head's height or whether it's a pan head or a flat (countersunk) one. `pocket_t` (4 mm) and
  `head_gap` depend on the height, and a flat-head wood screw, the usual #8 or #10, doesn't seat in
  a keyhole.
- **(c) The bottom foot's cord groove.** `cord_w`, 7 mm, is sized for the 6 mm guess, but the
  rewrite list sends the cord's size only to Task 6's `cord_d`.
- **(d) A light over 1 kg.** This "re-runs the moment" but names no parameter to change.

**Fix:** step 7: "its diameter with calipers, in two directions; if all the coupon's 1-inch holes
are loose, use the 25 mm build". Step 6: the head's height and type, with a pan head named for the
keyhole. Add `cord_w` (Task 3), and `pocket_t` and `head_gap` (Task 3), to the close's rewrites.
Name what a heavier light changes (`carrier_l`, `socket_depth`).

#### 10. The bottom screw is hidden only from straight in front

**Severity: Important** (the anti-goal "a screw … in sight from the room"; the test's comment
claims more than it proves).

**Where:** plan line 679 (`head_d < 19.05  # hidden behind even a 3/4-inch rail`); spec lines 162
to 164.

**Why:** the counterbore's opening (10.5 mm) is on a plate face 20 mm behind the rail's axis. I
computed sight lines past the rail. The far edge of the counterbore comes into view beyond 24° off
the rail's axis with a 1-inch rail, 23° with 25 mm, and 13° with 3/4 inch. At 45° most of the
head shows. A rail in a corner is mostly seen at an angle, so in practice the screw shows, and
with the 3/4-inch STL it shows almost always.

**Fix:** a press-in printed cap over the counterbore, in the parts' colour (the wall block's
precedent: D16's "sunk under caps"), as a third body in `rail-feet`, with the test changed to
"capped". Failing that, Task 9 step 3 has Dan look from 45° on each side.

#### 11. Scenario rows and task closes don't agree

**Severity: Minor.**

**Where and why:**
- Spec line 225 maps S28 to "Tasks 3 to 7", but the shade has no dowel and Task 7's Scenarios line
  (1574) lists only S30. S28 turns `built` at Task 8 (line 1896), which builds nothing for it.
- S26 (Task 2) and S31 (Task 1) are never named `built` at their closes; the close bullets say
  only "the spec's scenario statuses".
- S12 (line 216, "Phase 2, Task 2") and S27 (line 224, "Phase 2, Task 5") cite the old plan's
  task numbers.
- Task 8's Docs bullet (1895) asks for the README's first-project lines, which the uncommitted
  README diff already wrote.
- No close mentions the spec's status line.

**Fix:** S28 "Phase 2, Tasks 3 to 6", turned `built` at Task 6's close; add "S31 built" to Task
1's Docs and "S26 built" to Task 2's; point S12 and S27 at Task 8; drop the README item from Task
8.

#### 12. An unfilled template placeholder in the Global Constraints

**Severity: Minor.** Plan line 46 reads `- A photo: {{PHOTO}}`. The photo rule does appear in Task
9 step 5 and Task 11 step 3, but the global constraint that subagents receive is empty. **Fix:**
fill it with that same rule.

#### 13. A duplicated line in Task 3's commit message

**Severity: Minor.** Plan lines 819 and 820 both read "Saved at 1 inch, with STLs for 3/4 inch and
25 mm." **Fix:** delete line 820.

#### 14. The look test doesn't say to light the bulb, or for how long

**Severity: Minor.** Plan lines 1936 to 1945. The anti-goal "a bare pink grow bulb" can only be
judged with the light on, and the shade is PLA in this test (it softens near a warm bulb).
**Fix:** step 3 adds "light on for a few minutes, no longer: does any pink show from the room?"

#### 15. 550 mm isn't 21 11/16 inches

**Severity: Minor.** Plan line 37. 550 mm is 21.65 in; the nearest sixteenth is 21 5/8 (549.3 mm).
21 11/16 is 550.9 mm, close enough to cut to, but it's the less accurate figure. **Fix:**
"21 5/8 inches (550 mm)".

#### 16. Nothing holds the cord in the keel's channel

**Severity: Minor.** Plan line 1436: the channel is 7 mm wide for a 6 mm cord, open below, with no
lip, so the cord can sag out between the stem and the first clip, under the light where it's
seen. **Fix:** narrow its mouth to snap the cord in, as the clips' loops do (`cord_d − 1 mm`).

#### 17. A spring toggle in the top foot's keyhole isn't clamped

**Severity: Minor.** Plan lines 791 to 793 and Review Focus 5 (61 to 63). A 3/16-inch spring
toggle is held tight only by its head bearing on something. With the gauge standing its head 4 mm
off, the bolt sits loose in its 1/2-inch hole. **Fix:** name a snap toggle, whose strap holds the
channel tight without the bolt, for the keyhole, or settle it with finding 1's swap, which puts a
clamped screw in the top foot.

#### 18. The coupon's notes are now wrong for two of the four dowel parts

**Severity: Minor.** `models/dowel-fit-coupon/model.yml` line 20 says "the dowel parts' sockets
print with their holes horizontal". The feet's cups and the carrier's U print vertical, which come
out closer to size, so the coupon's clearance is about 0.1 to 0.2 mm loose in them. The feet don't
mind, and the carrier's wedge takes it up (2.5 mm higher per 0.1 mm), but the sentence is wrong.
**Fix:** one line in Task 4 (or in the coupon's notes): "the feet and the carrier print their bores
upright; the coupon's clearance is a little loose there, and the wedge takes it up."

#### 19. A spec open item points at Phase 2's start and the plan doesn't address it

**Severity: Minor.** Spec lines 271 to 272 (the earlier PythonSCAD stand, "worth a look at Phase
2's start"). The rewritten plan doesn't say whether it was looked at. **Fix:** say so in the plan's
header, or move the item to the phase-end list.

### Scenario coverage

| ID | Task | Proof in the plan | Verdict |
|---|---|---|---|
| S03 | 1 | the JPEG-segment and vanished-file tests, the escaped fields | proves it |
| S31 | 1 | `test_offsite.py`; `make docs` on the real site; the live check at the phase end's step 9 | proves it (not marked `built` at Task 1's close, finding 11) |
| S26 | 2 | Dan's result on the Q&A page | fine (the dowel itself isn't measured, finding 9) |
| S28 | 3 to 6 | parameter tests at 1 inch; I evaluated the 3/4-inch and 25 mm builds and every body is closed | proves the cups and the 51 mm; the wedge margin is proved for the carrier only (finding 6) |
| S29 | 9 | Dan's hand check | fine; the notes don't say how to get the wedges out (finding 5) |
| S11 | 9 | Dan's verdict | fine; no light-on step (finding 14); the socket shows (finding 2) |
| S30 | 2, 7, 10 | the gap test at the ends; 14 h in Task 10 | the gap along the bulb isn't proved (finding 4) |
| S13 | 10 | the 48 h log | the tilt can't be read, and there's nothing to hang the 12 kg from (finding 7); the cord's slip has no scenario (finding 8) |
| S14 | 11 | Dan's bump check and a photo | the check exists, but the design fails it in one ordinary case (finding 1) |

### Fine

- **The 24-inch reach.** Wall to rail axis 30 mm, rail axis to the socket's bore end 35.5 mm, the
  arm 550 mm, minus the tip's 42 mm bore, plus the stem at 36 mm, gives 609.5 mm. Q&A 2 is kept.
- **The socket's depth** is 54 mm, at least the spec's 51 mm, and the test holds it.
- **The carrier is 110 mm long** (tested at 100 mm or more), the "longer sleeve" in Q&A 2.
- **The carrier goes on from the front.** Its mouth is the bore's width and opens toward the wall,
  its arms reach 0.3 mm from the wall (the S14 bearing), and its ±0.5 mm wedge test is
  conservative.
- **The cord is pressed in from the side** at the stem's slot, the keel and the clips' loops. From
  the eval bounding boxes and the pictures, the clips' C opens opposite its cord loop, so "snap on
  from below" is correct.
- **No bolt anywhere,** and the top foot's keyhole is blind.
- **Materials:** PETG matte on every page, and PLA only in Task 9. The shade has no dowel and
  one STL.
- **Every dowel part builds at all three sizes** with closed bodies (I ran `eval` at 19.05 mm and
  25 mm). The 41 rail tests pass in proto2 (I ran them).
- **Review Focus 2** (no shade ring) is handled by a ruling at Task 2's close.
- **Rulings:** Task 9's B and C revise and reopen a task with a ruling, and a failed load test is
  a ruling (vibed).
- **Q&A 7 is kept in every close.** Each pushes after `make leaks privacy models-check`, and the
  STLs and pictures wait for Dan's look before the merge (Task 12, step 8).
- **The diagrams:** each `class … planned` line deleted in Tasks 3 to 8 and 11 matches a node in
  the new diagrams, and the planter stays dashed (S16, Later).
- **Phase 1's parts:** Task 8 marks them superseded with links to the five rail pages, and the
  overview shows the rail built only when it is.
- **The order of the tests:** the load test comes before the install (the spec's fourth goal),
  and the look test comes before any PETG print (D8).

## Reliability

1 critical, 8 important, 12 minor.

Lens: will the parts work printed in PETG on a home printer, and will each listing apply and pass as
written, in order. Plan line numbers refer to the uncommitted
`docs/superpowers/plans/2026-11-05-3d-models-phase-2.md`. "Ran" means I ran it in my own clone
(`scratchpad/council/reliability/repo`). "Computed" means a hand model in
`scratchpad/council/reliability/mech.py`: the method is solid, but the material values are typical
ones (PETG E ≈ 1.8 GPa across layers, interlayer strength about 15 to 30 MPa; hardwood E ≈ 10 GPa;
wood creep ≈ 15 % of the elastic deflection in 48 h). "Read" means I reasoned from the listing.

### Findings

1. **Critical: the rail can be lifted, and a lifted rail frees the top foot. The rig can then fall.**
   The rail lies loose in the bottom cup. Nothing holds it down. A carrier is wedged to the rail,
   so anything that pushes a carrier, socket or planter up lifts the whole rail. That includes
   lifting a planter pot out of its holder, sliding a carrier up to change its height (which the
   design invites), or pulling the socket up its dovetail with the arm still in. As the rail rises
   it pushes the top foot up, because the rail's top touches the top cup's ceiling. After
   `travel` = 12 mm the screw head reaches the keyhole's entry (plan 731 to 732, 751).

   The arm's moment always pulls the top foot away from the wall (the rail carries it as a couple
   between the feet). So the foot comes off the head, the rail's top swings out, and the rail, the
   light, the mains cord and any planters fall forward around the bottom cup. Only about 2 kg of
   lift is needed (rail, arm, light and parts), and 18 mm of the rail is still in the bottom cup
   when this happens.

   The spec's anti-lift logic (spec 163 to 165: "the rail's top, touching its cup, stops a bump
   lifting it off") only covers a bump on the top foot itself. The plan's test (plan 691 to 693)
   and the notes (plan 793 to 794) carry the same gap. Task 11's push test (plan 2065 to 2066) might
   even pass by luck: a push at the light reverses the moment while the push lasts, but a lift at a
   planter or carrier does not.

   **Fix:** fix the rail's lower end to the bottom foot. The simplest hidden way is a #8 screw
   driven up through a countersunk hole in the bottom cup's floor into the rail's end grain, after
   the top foot is hooked on. Add a parameter and a test for that hole, a line in the notes, and a
   scenario row: "the rail lifted 20 mm at a carrier leaves both feet on their screws". The screw
   also stops the rail spinning in its cups, which helps finding 2.

   Read and computed (the top foot is pulled out by M/L; the rail is held down only by gravity).

2. **Important: a 0.3 mm gap to the wall can't stop the arm turning round the rail (S14).** The
   only thing that stops the arm turning is the carrier's two arms bearing on the wall
   (`wall_gap` 0.3 mm, plan 918 to 921, 961, 1024 to 1025). The rail turns freely in its round
   cups. Once the wedge pushes the rail to the U's front, the real gap is 0.1 mm, plus or minus the
   cups' 0.2 mm, the print's tolerance, a bowed dowel and the wall's flatness (drywall is often
   ±1 to 3 mm over 1.2 m). So at a given height the carrier either won't seat (the arms hit the
   wall) or turns freely. Computed: a 0.3 mm gap lets the light swing 10 mm sideways, 1 mm lets it
   swing 32 mm, and 2 mm lets it swing 65 mm, all with nothing pulling it back.

   **Fix:** design the arms about 1.5 mm short of the wall and give their ends something set at
   install. Self-adhesive felt or rubber bumpers, hidden behind the carrier, would do; say so in
   the notes. Lock the rail's rotation at a foot (finding 1's screw does this). Tell Dan to turn the
   rail so any bow points sideways. S14's bump test then checks it.

   Read and computed.

3. **Important: the arm socket is printed upright, so the block under the boss bends across its
   layers.** As printed ("standing on the slot's open end", plan 1248, 1252), the block below the
   boss (z 0 to 50) is a short vertical beam. The dovetail pushes it at the bottom and the arm's
   moment acts at the boss, so the bending stress runs vertically, across the layer lines.

   Computed for that section (263 mm², I = 2694 mm⁴): the bending moment at the boss's underside is
   7.9 N·m at the load test's 3× (18.1 N·m on the socket), about 19 MPa at the back face, across
   layers. That is close to PETG's interlayer strength, held for 48 h. In service at 1× it is about
   7.7 MPa, held for years, which is a creep risk.

   **Fix:** print the socket on its back face (the block's back, x = `block_x`, on the bed). Then
   the boss and bore stand vertical with no supports, the slot's flanks overhang about 20° from
   vertical, and the slot's ceiling bridges about 18.6 mm. The block's bending stays within layers,
   and what crosses layers is about 3 to 4 MPa (the boss, with a section about 5000 mm³). Change
   the model.yml's Orientation and Supports lines to match.

4. **Important: the carrier's wedge is a beam across the U's mouth, printed so it bends across its
   layers.** The wedge (plan 966 to 968, 985 to 987) bears on the arms' grooves only by two
   1.75 mm wings. Behind it, the 25.8 mm cord channel is empty, so the rail pushes the middle of a
   4.1 to 8.9 mm plate spanning about 27.5 mm. It is printed "on its long edge" (plan 1012), so
   that bending runs across its layers.

   Computed, at the top region where the moment's couple lands and the wedge is 4.6 to 5 mm thick:
   - 3×: 9 to 15 MPa, and 0.13 to 0.23 mm of deflection, which is 0.9 to 1.6 mm at the tip.
   - 1×: about 4 to 6 MPa, plus the wedge's preload, held for years.

   PETG creep at those stresses puts S13's 1 mm tilt budget (plan 2003) at risk from this one part.

   **Fix:** make the wedge thicker. `room_top` from 3.5 to about 6 mm and `wedge_top` up to match
   would make it roughly 3.5× stiffer and cut the stress by half. Check that the cord channel
   behind it stays at least `cord_d` + 1 at the carrier's bottom. Alternatively, print the wedge
   flat on its rail face; its sloped back then steps 0.2 mm every 5 mm, which a 1-in-25 wedge
   tolerates. Add a test for the wedge's minimum thickness.

5. **Important: toggle bolts don't work in the top foot's keyhole.** Review Focus 5 (plan 61 to 63)
   and the spec (spec 165 to 166) offer 3/16-inch toggle bolts for both feet. In the keyhole, the
   head must stand 4 mm proud (`head_gap`, plan 725 to 727). A spring toggle that isn't clamped
   against anything is axially loose once the gauge comes out. Its 4.8 mm shank floats in the
   1/2-inch (12.7 mm) drywall hole, about ±4 mm. And it can spin: turning the head while hooking
   the foot can unscrew the bolt from its wings, which then drop into the wall. The top foot is
   then held by nothing, which leads to the fall in finding 1.

   **Fix:** in Task 2's screws step (plan 567 to 568) and Review Focus 5, say that the top foot
   needs a stud. In drywall it needs an anchor whose nut is held in place independently of the bolt
   (a SnapToggle-type channel), with its bolt set by the gauge. Also measure the head's height,
   since `pocket_t` 4 mm fits a head no taller than 3.6 mm (`back_t` + `pocket_t` = 7.6 mm from the
   wall). Task 10 step 2 should mount the top foot the same way.

6. **Important: nowhere says where the top screw goes.** The anti-lift logic needs the rail's top
   to touch the top cup with the foot hanging. That fixes the top screw at **L − 51 mm above the
   bottom screw** (L is the rail's length), plumb above it. I derived that from `cup_h`, `tab_h`,
   `floor_t`, `entry_z` and `travel`. It holds within about +9 mm (rail too long: the foot doesn't
   drop fully) and −12 mm (rail too short: the foot can lift off by itself).

   The feet's notes (plan 791 to 794), Task 9 step 2 (plan 1936 to 1937) and Task 11 step 1 (plan
   2060 to 2064) say "the rail cut" and "the feet screwed as their notes say", but never give the
   number. **Fix:** put the formula and the tolerance in the notes, plus "cut the rail first, then
   mark the top screw", and add a test that recomputes the offset from the parameters.

   Read and computed.

7. **Important: the bottom foot's cord groove has no room to spare, and Task 2 doesn't resize it.**
   The groove (plan 747) starts at x = −31 but the plate's back is at −30, so it is
   `cord_w` − 1 = **6 mm deep** by 7 mm wide. The screw clamps that plate to the wall. A 6 mm cord
   (the guess) fills the depth exactly. A 7 mm round cord or a 7.7 × 3.9 mm flat SPT-2 cord would
   be crushed under a screwed plate, and this is a mains cord. Task 2's forward rewrites (plan 575
   to 582) resize `cord_d` in Task 6 only, never the feet's `cord_w` and `cord_y`. The feet's test
   (plan 672) checks room behind the rail, not the groove against the cord.

   **Fix:** add `cord_w` and the groove's depth to Task 2's rewrite list. Make the groove at least
   `cord_d` + 1 deep. Add a cross-part test: the feet's groove depth is at least the tip's `cord_d`
   + 1.

   Ran (I checked the cut's coordinates); the risk is read.

8. **Important: the stem grips a mains cord along 42 mm through a slot that can't flex.** The
   grip hole (`grip_d` = `cord_d` − 0.6) runs the stem's whole length, about 42 mm. The cord goes
   in through a 4.5 mm slot (`press_w` = `cord_d` − 1.5) cut 8.3 mm through a solid 22 mm stem
   (plan 1423 to 1424, 1437 to 1438). The stem can't spring open. A 6 mm cord has to be squeezed
   25 % along 42 mm to get in, and pulled through a 10 % interference to "set the height" (plan
   1498 to 1499). Phase 1's clamp gripped over 8 mm (`shelf_t`). Expect to need pliers and to
   scuff the jacket.

   **Fix:** grip over a short band (8 to 10 mm, like Phase 1's clamp) and give the rest of the
   stem a free bore of `cord_d` + 0.5. Chamfer the slot's entry. Bound how much narrower than the
   cord the slot may be in the test (plan 1383 to 1386).

9. **Important: S13's "socket tilt" reading also counts the wood's own creep, enough on its own to
   fail the 1 mm limit.** Task 10 measures the arm's drop 100 mm out, times 4.9, against the floor
   (plan 1997 to 1999), and judges it against "adds under 1 mm at the tip" (plan 2003). That
   reading includes three things:
   - **The rail's own bending under the arm's moment.** The rail sits loosely in its cups, so it
     acts as a beam supported at its two ends. Computed for a 48-inch rail at 3×: 5.2 mm at the
     light with the carrier at mid-rail, and 12.9 mm with the carrier 85 % up, where a grow light
     usually sits.
   - **The arm's own bending in its first 100 mm.** 0.33 mm there at 3×, which is 1.6 mm once
     multiplied by 4.9.
   - **What the printed parts add.**

   Wood creep in 48 h of about 15 % of those deflections gives 0.8 to 1.9 mm from the rail, plus
   about 0.25 mm from the arm. That is over the 1 mm limit before the PETG adds anything, and a
   false fail triggers a needless redesign (plan 2019 to 2021). Reading 0.2 mm at 100 mm also
   needs about 0.05 mm resolution.

   **Fix:**
   - Measure the socket's tilt against the rail at the carrier, not against the floor: calipers or
     a dial between the arm about 20 mm past the mouth and a straightedge clamped to the rail.
   - Name the tool.
   - Record the rail's length and the carrier's height.
   - In the spec (spec 180 to 182), note that the rail's bending adds 2 to 5 mm at the light at 1×
     to the arm's "about 8 mm".

10. **Minor: Task 1 Step 2's expected output is not what `make test` shows** (plan 465 to 470).
    Ran: pytest stops at the collection error (`Interrupted: 1 error during collection`). Only
    `ModuleNotFoundError: No module named 'offsite'` shows, and the JPEG, vanished-file and gallery
    tests never run. With `--continue-on-collection-errors`, all five fail exactly as the plan says.
    **Fix:** expect only the collection error, or run
    `uv run --frozen pytest -q --continue-on-collection-errors` in this step.

11. **Minor: the carrier test's ±0.5 mm check leaves out the clearance** (plan 934 to 938). It
    takes the gap at the top as `room_top − off`. The real gap is `room_top + clearance/2 − off`,
    because the wedge pushes the rail to the U's front. So at −0.5 mm the thin end really sits
    2.5 mm above the carrier's top at 0.4 mm clearance, and 7.5 mm above at 0.8, though the test
    says it "seats inside". In practice it's harmless, because the coupon picks the clearance from
    the same dowel (computed: 11 to 24 mm inside, across the coupon's clearances). **Fix:** use
    the true formula, or vary the actual fit instead of `off`.

12. **Minor: the 12 kg planter load is underspecified, and the planter carrier's grip depends on
    the wedge.** "12 kg hung from the second carrier's dovetail" (plan 1993 to 1995): with no
    second socket printed (plan 1988 to 1989), it doesn't say how, so the load's offset (and its
    moment) is open. With a small moment (load about 24 mm out), the carrier doesn't bind on the
    rail the way the arm's carrier does (offset/length ratio 0.2, versus 5 for the arm). It holds
    only by the wedge's preload, and "only tightens it" (plan 1020 to 1021) holds only if the
    wedge grips the rail better than its groove: PETG-on-wood against PETG-on-PETG plus a 0.04
    taper, which is close. **Fix:** say how the load hangs (for example a strap over the
    dovetail's top end, or a second socket with a stub at a planter's offset). Tell Dan to tap the
    wedge home with a mallet, not push it by hand. Soften the claim to "once tapped home, the
    weight tightens it".

13. **Minor: the dovetail's fit lets the arm sag about 4 mm and swing about ±1.5°.** `fit` 0.3
    (plan 1193) leaves about 0.2 mm of clearance at each flank. Computed: about 0.55 mm of play at
    the top and 0.3 mm at the bottom, over about 103 mm, is 8 mrad: the light drops about 4 mm as
    the play takes up. Sideways play comes from the cross-section alone, so the socket's length
    doesn't help. Both parts are also printed with the dovetail's ends on the bed, where the first
    layers spread (elephant's foot), so the mating entries narrow. **Fix:** a 0.5 mm chamfer at the
    dovetail's ends and the slot's mouth. Consider `fit` 0.2, or check it with a short test print.

14. **Minor: a 3/4-inch arm sags about three times as much.** At 550 mm with a 1 kg light, a
    3/4-inch arm sags about 3.2× as much as a 1-inch one (stiffness goes with d⁴): roughly 25 mm
    over time. The socket's and tip's pages (plan 1254 to 1257) offer 3/4-inch STLs with no
    warning. **Fix:** a line in their notes: for 3/4 inch, keep the arm short.

15. **Minor: nothing checks that the feet and the carrier share `standoff`.** The socket's test
    shares the dovetail's parameters with the carrier's (plan 1146 to 1151), but no test ties the
    carrier's `standoff` and `wall_gap` to the feet's `standoff`. If one changes, the arms miss the
    wall or hit it. The socket's script defines `standoff` (plan 1186) and never uses it. **Fix:**
    a carrier test against the feet's `standoff`, and drop the unused parameter.

16. **Minor: the bottom screw is hidden only from straight in front.** The test says "hidden
    behind even a 3/4-inch rail" (plan 679). Computed: the head shows past the rail's edge beyond
    about 46° from straight in front with a 1-inch rail, and beyond about 22° with a 3/4-inch rail
    (the plate is 7.3 or 10.5 mm behind the rail). In a corner, people often look from about 45°.
    The counterbore's 1.2 mm of recess helps a little. **Fix:** soften the claim, or deepen
    `head_depth`.

17. **Minor: the arm tip's supports will fill its cord channel, and the cord bends sharply into the
    stem.** Printed upright with "Supports: under the cap, from the bed only" (plan 1489, 1493),
    the keel's cord channel (open downward, 7 × 10 mm × 37 mm, plan 1436) will fill with support.
    The cord also turns 90° into the stem on a bend of about 6 mm radius. **Fix:** say "block
    support in the channel" (its 7 mm ceiling bridges) and round the corner.

18. **Minor: the notes don't say how to get the carrier's wedge out.** The carrier's wedge locks
    itself, and its thin end sits 10 to 24 mm down inside the carrier, behind the rail. "Tap the
    wedge down and out" (plan 1021 to 1022) needs a thin punch pushed down the channel from above.
    S29 checks this, so the notes should say how.

19. **Minor: Task 2's clearance rewrite leaves a wrong sentence in four pages.** Each dowel part's
    notes say "The 0.4 mm it's saved with is a placeholder" (plan 795 to 796, 1028 to 1029,
    1261 to 1262, 1504 to 1505). Task 2's rewrite of `clearance` (plan 576 to 578) should change
    that sentence too.

20. **Minor: the shade's wall thins toward the rim.** The inner and outer cones have different
    slopes (0.247 against 0.241, plan 1651 to 1652), so the wall thins from 3.1 mm at the top to
    2.1 mm at the rim, against `shade_t` 2.4. **Fix:** cut the inner cone parallel to the outer
    one.

21. **Minor: wording.**
    - The rail diagram's caption, "Dashed: planned, Phase 2" (website/architecture.qmd line 45),
      will be wrong after Task 7, when only the planter is dashed, and it is Later (S16).
    - Task 3's commit message says "Saved at 1 inch, with STLs for 3/4 inch and 25 mm." twice
      (plan 819 to 820).

### Fine

- **The wedges' geometry.** Each groove and its wedge share the 0.04 taper, and the face against
  the dowel is parallel to the dowel. Ran: sections of the carrier at z = 5 and z = 105 show the
  groove deeper at the bottom, so pushing the wedge up tightens it. At 1 in 25 every wedge locks
  itself and won't back out. On the arm's carrier the moment makes the carrier bind on the rail
  (offset/length about 5), so it doesn't slip whatever the wedge does.
- **The keyhole.** Correct with the top foot flipped: in use the entry is below the slot's end,
  the front skin is 2.4 mm, and the back layer's ligaments bend within their layers. The 4 mm gauge
  and the 3.6 mm back layer leave 0.4 mm of play.
- **The bottom foot's loads.** Computed at 3× light plus 12 kg: about 157 N of shear and 105 N of
  tension on its screw. The bridge sees about 0.6 MPa, and the tab about 1.7 MPa across layers.
  The cup floor, printed first, carries the rail's end in compression.
- **The arm in its socket and tip.** The arm socket's 54 mm and the tip's 42 mm depths, the walls
  above their wedge grooves (3.0 and 3.5 mm or more), the socket's top cap bridging the slot, and
  the clips' snap strain (about 1 %, within the layers) are all fine.
- **Printability.** The feet, the carrier (on its end), the wedges on edge with a brim, the clips
  flat, and the shade upside down (walls 13.5° from vertical, horizontal vents) all print with no
  overhang worse than about 20°.
- **The arm length.** Ran: a 550 mm arm puts the stem 609.5 mm from the wall.
- **The other sizes.** Ran: every dowel part evaluated at 19.05 mm and 25 mm has every body closed
  and no failed feature.
- **The listings, in order, in my own clone of `phase-2` with the phase-start docs copied in.**
  Ran:
  - Task 1's patch passes `git apply --check`; tests first, then code; 142 pass and lint passes.
  - Tasks 3 to 7: each test fails first with `FileNotFoundError` for its eval.json; each
    `solidcraft-cli run` exits 0; each `.sc` is byte-identical to proto2's; `make models` reports
    "building … (missing …)" and "1 built"; each part's tests pass.
  - Task 8's patch applies on top of Task 1. Its test fails with "'status' must be one of
    designed, printed, in use", then passes.
  - Every architecture or overview line that Tasks 3 to 8 delete exists. Afterwards only `planter`
    and `railup` stay dashed.
  - `make check` passes: 184 tests twice, lint, "8 models, every build matches its design",
    privacy, gitleaks, the render, and the offsite check.
- **Shared parameters.** The socket's shared dovetail parameters match the carrier's, and that test
  catches drift. CI's site job runs `make docs`, so the offsite check runs in CI.

## Security and privacy

0 critical, 4 important, 4 minor.

(Lens: security and privacy. Verified = I ran it, in my own scratch under council/security/ against proto2/proto3 code; read = by reading only.)

### Findings

1. **Important. Task 1, scripts/offsite.py (plan 176-223): it fails open and misses most ways a page loads from another host.**
   - Fails open (verified): `offsite.main(["/nonexistent/x"])` prints "loads nothing from another host" and returns 0. A missing, renamed or empty `_site` (an `output-dir` change, a render that wrote elsewhere) passes the gate. `rglob` on a missing dir yields nothing.
   - Missed (verified, 20 of 30 probes): `srcset` on img/source; `<style>` blocks (`@font-face src:url(https://..)`, `@import`); inline `style="background:url(https://..)"`; `<meta http-equiv=refresh>`; `<object data>`, `<embed src>`, `<track src>`, `<video poster>`, `<input type=image src>`; SVG `<image href>` / `<use href>`; `<base href>`; `image-set("https://..")` in CSS; an attribute value with a leading space (`src=" https://.."`); an entity-encoded scheme (`&#104;ttps://`); a `>` inside an earlier attribute (`alt="a>b" src=https://..`, because of `[^>]*`); `import()` / `fetch` / `createElement` in inline scripts; and `<script type=importmap>` (the viewer's own import map is local today, but an absolute URL there would pass). `.js`, `.svg`, `.json` and `.xml` files are never read.
   - Caught (verified): unquoted values, upper-case tags and schemes, a newline before `src`, `<link rel=preload href=//..>`, single quotes, `url(` in CSS in any case. One false positive: `data-src="https://.."` matches `\bsrc`.
   - Today's rendered site is clean (read: grep of proto2/website/_site finds no googleapis, mathjax or polyfill reference outside quarto-search's autocomplete.umd.js comment text), so nothing is broken now; the gate is what is weak, and the task's whole stated purpose is the gate.
   - Fix: (a) exit 1 when the directory is missing or holds no `.html`; (b) parse HTML with `html.parser.HTMLParser` instead of regex, and flag any absolute or protocol-relative URL in `src`, `srcset`, `poster`, `data`, `href` of `link`/`base`/`use`/`image`, and a refresh `content`; scan `<style>` text and `style=` values for `url(`/`@import`/`image-set`; (c) scan `.css`, `.js` and `.svg` bytes for `@import`/`url(` and `import ... from "http`/`import("http`; (d) match `\bsrc` only as a whole attribute name; (e) add test rows for each shape above, plus the missing-dir case. If the plan keeps a regex, say in the docstring and the commit that it is a tripwire for the known CDN shapes, not a proof; the phase-end step 9 check on the live site then matters more (a network-log look at the live pages, not only the HTML).

2. **Important. Task 1, scripts/privacy.py (plan 232-281): the JPEG allow-list still lets text through, and the module docstring/commit say otherwise.**
   - Verified on proto3's code with a 16x16 Pillow JPEG: `check` returns None (passes) for a JPEG with an extra `APP2`, `APP0` or `APP14` segment holding "taken at home 12 Elm St". Those three markers are in `JPEG_HOUSEKEEPING`, and Pillow only turns them into `info` when they carry the JFIF/ICC/Adobe magic; otherwise they sit in `applist` and the check ignores the payload. Also passes (verified): text placed inside the entropy-coded scan just before FFD9, since the walk treats everything up to the next non-stuffed FF as scan data and Pillow stops decoding when the image is complete. COM is refused (`metadata: comment`), a DNL (FFDC) is refused by the new rule, and a DRI padded with text is refused only because Pillow errors (verified).
   - So the claim in the plan's Step 3 and the docstring ("allows nothing but a colour profile and the format's own housekeeping") is not true for JPEG. The new rule closes DNL/JPGn; it does not close the commonest hiding places.
   - What the rule refuses wrongly: nothing realistic. DNL (FFDC), TEM, JPG0-13 and a stray SOI are essentially never in a real picture; DHT, DQT, DRI, SOFn, restart markers, progressive scans and a second APPn all pass (verified with a progressive, optimised JPEG).
   - Fix: in `jpeg_walk`, check each APP payload: APP0 must start `JFIF\0` and be exactly 16 bytes, once; APP2 must start `ICC_PROFILE\0` (or `MPF\0` if camera originals are expected, but `make strip` re-encodes so ICC only is enough); APP14 must be `Adobe` and 14 bytes; each at most once. Anything else is "a JPEG segment it doesn't allow (FFEx)". For DQT/DHT/SOF/DRI/SOS headers, check the declared length equals what the table parse uses (or accept this residual). For the scan tail and ICC profile text (a profile's description/copyright strings), say plainly in the docstring that the check cannot see them and `make strip` plus Dan's look are the controls. Add tests for APP2/APP0/APP14 text.

3. **Important. Task 1, scripts/gallery.py: a photo's link target is still raw (plan 152-158).**
   - Verified: proto3's gallery.py line 180 is `f"![{alt}]({slug}/photos/{shot.name})"`. The patch escapes only the alt text. A photo named with a shortcode, a space, `)` or `]` puts it unescaped in the link target; the new test (plan 352-360) asserts only the alt and the size line, and never asserts the shortcode is absent from the page (the sibling test at 346-350 does). The commit message and the plan's "photo names" claim overstate. Alt itself also leaves `[`/`]` in a stem unescaped (the title alt does escape them, so the pattern exists at gallery.py:~140).
   - Why it matters: the file name is Dan's, so this is robustness rather than attack, but a shortcode in a target is expanded by Quarto (or fails the render), and the test should hold the claim.
   - Fix: build the target with `urllib.parse.quote(shot.name)` (and the `shutil.copy2` name stays as is); escape `[`/`]` in the alt as the title does; extend the test to assert `SHORTCODE not in text` and the quoted target. Also quote the link text/target for the sized-STL lines (`model.sized(size).name` is already restricted to `[a-z0-9-]` by `size_name`, read: models.py 65-67, so those are fine).

4. **Important. Plan line 46: the Global Constraint for photos is a literal placeholder.**
   - `- A photo: {{PHOTO}}` (read). In the HEAD version of the plan this line carried the full rule ("Strip it first, `make strip` ... Only after his OK naming the file ..."). Now it says nothing, and it is the one constraint every task is meant to inherit; the rule survives only in the text of Tasks 9 and 11. A subagent building Task 8 or a fix round sees nothing on photos. It will also render as the stray text `{{PHOTO}}` on the Design page.
   - Fix: restore the HEAD wording on that line.

5. **Minor. Task 1, GONE handling: fails closed and the history step still covers the file (read; one path verified by the plan's own test).**
   - A vanished or unreadable file puts `GONE` in `found`, so `command_check` returns 1. It is excluded from `reported` only because `committed_bytes` would raise; the history pass then examines every blob under that path in full (no skip), so GONE never lets content pass. Good.
   - Remaining edges: the symlink branch of `problems()` (`committed_bytes` -> `readlink`) is outside the new `try`, and the `reported` comprehension calls `committed_bytes` for non-GONE files that might vanish after being reported; each would end as a traceback, which also fails closed (exit 1), just ugly. Also, when `path_problem` raises after `image_problem` returned a real reason, the real reason is replaced by GONE (still exit 1).
   - Fix (optional): move the symlink read inside the `try`, and build `reported` with a small `try/except OSError: continue`.

6. **Minor. Tasks 2, 9, 10, 11: the "home stays private" steps are sound but uneven.**
   - Photos (Tasks 9 and 11): strip, show the stripped file, Dan's OK naming the file, `make privacy` before staging: sound (read). Q&A 7's "STLs and pictures wait for Dan's look by name before the PR merges" is carried into Task 12 step 8.
   - The "measurements, never a description of the home: the Q&A pages are published" rule appears in Tasks 2, 9 and 10 but not in Task 11, whose commit body asks for "how it was fixed to the wall ... and Dan's words on how it looks". Add the same sentence there.
   - Tasks 2, 9 (no photo) and 10 are Tier 3, where the only automated check on published free text is gitleaks; neither it nor `privacy.py` can see a place, a neighbour or a room description. Add to their Tier 3 review line: "read the added Q&A and notes text for a place, an address, a person or a description of the home."
   - A photo's file name is published (it becomes the alt text and the URL). The plan fixes `installed.jpg`; Task 9 step 5 leaves the name open. Say "named for what it shows in the part, never the place".

7. **Minor. Tier recheck against AGENTS.md's table.**
   - Task 1: Tier 1 is right (leaks data to a public repo / third-party). Task 8: Tier 2 right (gallery code with tests). Tasks 2, 9, 10: Tier 3 right; Task 9 and 11 correctly rise to Tier 1 with a photo.
   - Tasks 3 to 7 (Tier 2): the table's Tier 1 wording is about systems, data and alerts, so a rail that holds a 25 W lamp and two watered planters over people's heads falls under Tier 2 by the letter. The plan's compensation is the load test (Task 10) and Review Focus; that is reasonable, but say so once in the plan ("physical load is covered by Task 10, not the tier") so a reviewer does not read Tier 2 as "no safety role".
   - Task 7's PETG shade at 60 degrees is a heat/fire property; same remark.

8. **Minor. Smaller points on offsite and privacy.**
   - `offsite` only runs inside `make docs`, so it gates CI's site job and thus the Pages deploy (read: ci.yml `site` job runs `make docs`); fine, but a phase branch's deploy-less run is the only check before merge, and the live check is a manual phase-end step.
   - A file with an image content but no listed suffix (`.jpe`, no extension, `.JFIF` is listed, `.pjpeg`) is never opened by `problems()`; pre-existing, mention only because Task 9/11 add the first photos.

### Security checklist (Task 1, one line per item)

- Secrets: fine. No token, key or credential is read, written or logged by either script; the new tests use only example.com/example.net URLs; leak scan unchanged.
- Permissions: fine. Neither script changes modes; `strip` still copies the mode; `GONE` also covers an unreadable file (finding 5).
- Network exposure: finding 1. The gate that stops third-party loads misses most load shapes and passes on a missing site folder; the actual current site is clean (read from the rendered proto2 site; `$web-font-path: false` and `html-math-method: plain` do remove the Google font and MathJax).
- Failing closed: findings 1 and 2. GONE and the DNL/JPGn rule fail closed; offsite on a missing dir and the APPn/scan-tail paths do not.
- Injection: finding 3. Print settings, size, size names and alt text are escaped; the photo link target is not (verified); size file names are safe (`size_name` restricts them).
- Logging: fine. Messages name the file and the marker byte only, never the text found (the new test checks that the text is not printed); offsite prints paths in `_site` only.

### Fine

- Escaping of print keys and values (`escaped` before `cell`, both orders correct), `size` in FREE_TEXT, the `for {escaped(size)}` line: read and consistent with the new tests.
- `jpeg_walk` returns the stray marker before the cut-short verdict, so a stray segment is named even in a truncated file; a zero or one length segment cannot loop forever (read).
- GONE excluded from `reported` does not skip the history check (read: history_problems iterates every blob regardless).
- Nothing in the plan, Q&A pages, spec diff or new diagrams names a home path, address, city, network address or room (grep of the diff and both pages for path, address, place and network patterns found only generic words: "kitchen scale", "the room", "a stud"). The one `/Users/<name>/` is a comment in privacy.py with a placeholder.
- The standing push OK (Q&A 7) matches AGENTS.md's push rule, and keeps STL/PNG/photo files waiting for Dan's look by name before the PR merges.

## Simplicity

0 critical, 4 important, 6 minor.

Lens: simplicity. Method: read the whole plan (all 2,140 lines), the Q&A page's item 6, the spec's lines on the
feet, keel and clips, and docs/agents/close-task.txt. I ran nothing: every finding below is from reading.
The listings themselves were already run by the brief's account, so I judge shape, not whether they work.

### Important

1. **The plan repeats text that already lives elsewhere, about 350 of its 2,140 lines (16%).**
   Plan lines: each task's "close message" block (lines 524-539, 592-607, 842-857, 1075-1090, 1306-1321,
   1549-1564, 1738-1753, 1901-1916, 1960-1975, 2032-2047, 2093-2108): 11 copies of 15 lines, about 165 lines,
   and every one of them is `docs/agents/close-task.txt` with the number changed. The same close text says
   "from `docs/agents/close-task.txt`" in the line above each block, so the copy adds nothing but drift risk.
   Also repeated: the "Push under the standing OK" bullet (10 copies, 3 lines each), the "Consumes:" paragraph
   (Tasks 3 to 7, 4 lines each, word for word), the "Close, its own commit: boxes ticked, Now set…" bullet
   (11 copies, 4 lines), the Q&A-page sentence "Each answer goes on the Phase 2 Q&A page … never a
   description of the home" (Tasks 2, 9, 10, 3 copies of about 4 lines), the photo-OK paragraph (Tasks 9 and 11),
   and the pre-written commit messages for Tasks 3 to 8 (about 12 lines each, 70 lines, which the builder will
   rewrite anyway once Task 2's values change things: Task 3's already has a duplicated line, 819-820).
   Fix: one "Every task's closing steps" section after Global Constraints holding the close pointer
   (`close-task.txt`, the Tier line varies), the push line, the Q&A-answer sentence and the photo-OK paragraph;
   each task keeps only its own `Tier`, `Forward:`, `Docs:` lines. Drop the pre-written commit bodies for a
   one-line subject plus "body: what and why, per AGENTS.md Commits" (the subject stays: it is a decision).
   Cost: a subagent dispatched on one task must be sent the shared section (AGENTS.md already says
   "these rules reach them through the plan and the dispatch"), so the dispatch template gains one paragraph.
   The one-task-one-review shape is unchanged. The plan falls to about 1,750 lines.

2. **Task 6's three cord clips are one part copied three times: 3 bodies, 18 of the 45 command lines (1447-1464),
   3 names in the test's BODIES list.** The clips are identical (same x offsets only). Fix: build one body,
   "Cord clip", and say in `print:` "Orientation: ... print three clips". Saves 12 command lines, two bodies and
   two test names; `test_every_part_prints_from_the_same_bed` and the closed-body test lose nothing.
   Cost: the spec (lines 154-155, 189) says "three cord clips ... bodies in their part's design", so this is a
   one-line spec edit (an edit to a stated design, so a fifth-stop ruling if Dan wants it asked; it changes no
   scenario outcome). If Dan wants more cut: the clips are the least load-bearing and least validated part (a
   snapping PETG ring at a 2.5 mm wall, untested until Task 9); deferring them to a Later row, with cable ties
   in the look test, would drop about 40% of Task 6's script. I would not do that unasked; the single body is
   the safe merge.

3. **Task 8 is a full 8-step task (a Tier 2 review, a close commit, a CI wait) for one line of code, one test and two
   yml banners.** It touches gallery.py (one tuple), one test, two notes paragraphs and one diagram line.
   Fix: make it the last step of Task 7 (the five rail pages must exist before the banners' links resolve, which
   is why it can't go into Task 1) and let Task 7's Tier 2 review cover it. Alternative if Dan wants it separate:
   re-tier it Tier 3 (AGENTS.md: "docs, wording, display output, configs"); the status tuple is a display
   constant. Cost of merging: Task 7's diff grows by about 30 lines and its title and Scenarios gain S12/S18.
   I considered dropping the fourth status and leaving the parts `designed` with a banner: that costs no code but
   makes the gallery list two superseded designs as live, which defeats Q&A 4's point, so don't.

4. **Tautological and copied tests add lines, not protection.** Per-part tests that cannot fail unless the script
   is mistyped to contradict itself:
   - Task 3's gauge test (696-699): `gauge height == head_gap` where `gauge_t = head_gap`, and
     `back_t < head_gap` where `back_t = head_gap - 0.4 mm`. Both hold by their own expressions.
   - `bore_d == dowel_d + clearance` (the expression, again) in Tasks 3, 4, 5, 6.
   - Identical in all four dowel tests: the saved size is 25.4 and the sizes are `{"3/4 in","25 mm"}`; the
     clearance is a multiple of the coupon's step; each body closed.
   Fix: one parametrized file, `tests/test_rail_common.py`, over `("rail-feet", ...)` with those four checks,
   created in Task 3 with one slug; Tasks 4 to 6 each add their slug (the test still fails first, with the same
   FileNotFoundError) and keep only geometry that is theirs (the carrier's wedge travel at -0.5/0/+0.5, the
   socket's dovetail match, the tip's grip, the shade's gap). Delete the gauge test and `bore_d` lines.
   Saves about 45 test lines and removes four copies of the coupon-step expression, so a change to how
   clearance is chosen (Task 2's close) is one edit. Cost: a task's test no longer lives wholly in its own file;
   the one-line slug addition goes into each task's commit and review. Also cut: `carrier_l >= 100` and
   `wall_gap < 0.5` (4.. literals asserted against literals) unless a reviewer wants them as a guard on Task 2's
   rewrite, in which case keep `carrier_l` only.

### Minor

5. **Task 1's offsite check: keep the script, trim the tests.** A grep one-liner cannot replace it:
   Quarto writes multi-line tags and a generic "loads from another host" check beats a deny-list of Google and
   jsdelivr, which the next theme change walks past. A `grep -rE 'src="https?://'` would also miss the actual
   leak, which was an `@import` inside a CSS file. So keep `offsite.py` (48 lines). Trim `test_offsite.py`
   (39 lines) from five parametrized cases to three (a script src, a protocol-relative link href, one CSS
   `@import`) plus the pass case; `img` and `url(` are the same branch of the same regex. Saves about 4 lines;
   do this only if the file is touched anyway.

6. **Task 1 does two unrelated things (photo-check gaps, escaping and a vanished file; and the off-site load).**
   Splitting would add a task loop (8 steps, close, CI), which is the larger cost, and both are Tier 1 with the
   same review. Keep as is. Noted only because the title joins them and the commit body is 15 lines.

7. **The shade's six vent cylinders (1654-1659)** are six hand-expanded lines with trig constants. If SolidCraft
   has a circular pattern, one line replaces six. I could not check the CLI, so this is a read finding: look in
   `solidcraft-cli` for a pattern command; if there is none, either use four vents or keep six. Cost: re-running
   the listing to confirm the body is still closed. A smaller vent count is the only change that needs Dan's OK
   (S30 is about 60 C, not the vent count).

8. **The `git add` lists** (lines 510, 829, 1062, 1293, 1536, 1725) name 11 files each. `git add models/rail-feet
   tests/test_rail_feet.py website/architecture.qmd` is still staging by path, never `-A` or `.`, and cannot
   drift from what `make models` writes (the shade has one STL and its list already differs). Cost: a folder
   path would also stage a stray file placed in it, which AGENTS.md's photo rule forbids until Dan has OKed
   it; folders here are new in each task and hold no photo, so the risk is nil before Task 9. Use `git status
   --short models/rail-feet` as a check before the commit.

9. **Plan prose that restates without deciding.** "Review Focus" (lines 50-63) repeats Global Constraints and
   the tests' own comments (cord never through a hole is stated in Global Constraints line 39, Review Focus 1,
   Task 6's notes, and Task 3's notes); "What it does" in Task 1 Step 3 repeats the patch comment, the commit
   body and the task intro. Keep Review Focus (it feeds the reviewers), but cut Step 3's paragraph to one
   sentence and drop the third and fourth statements of the cord rule. Saves about 15 lines.

10. **Gauge, keel and the top foot's keyhole: keep.** I looked for merges.
   - The gauge costs two script lines, one parameter, one print line and one notes bullet. It replaces a
     measurement the owner would get wrong by 1 mm (the keyhole's whole job). Only its test goes (finding 4).
   - The keel doubles as the structural bridge between the round cap and the 22 mm stem and as the cord channel;
     without it the stem meets the cap along a tangent line. It is 1 box and 1 cut. Keep.
   - Making both feet one keyhole part (so a single design, two prints) would drop the bottom foot's tab,
     screw hole, counterbore and `tab_h`, `screw_d`, `head_d`, `head_depth` and one test (about 12 lines). But
     it hangs the rail's whole load (plus two 2 kg planters, Q&A 5) on a 4 mm PETG skin over a screw head, in
     place of a screw going straight into a stud. That is a safety trade, not a simplification, so I have not
     proposed it; a Dan-level question if he wants to ask it.
   - The three STL sizes per part (12 STLs, from a premise of the project) are the larger binary cost, and
     each push waits on Dan's OK for each binary. Task 2 learns the real size, so 3/4 in and 25 mm are built
     for nothing if Dan bought 1 inch. Not touched here: S-numbers and Review Focus 4 name it.

### Proportion

2,140 lines for 5 models, 2 fixes, 4 Dan tasks and a phase end. About 460 are the SolidCraft scripts and tests
(the real content), about 130 are model.yml pages, and about 350 are the repeated process text in finding 1.
After findings 1, 2, 4 and 9 the plan is about 1,650 lines, with every decision still in it. Steps are
decisions, not transcripts, except the pre-written commit bodies (finding 1) and the `git add` file lists
(finding 8), which are transcripts of what the builder would write anyway.

### Fine (checked, sound)

- Task 1's patch is one Tier 1 task with its own tests; every hunk is tied to a stated gap. The `jpeg_walk` split
  keeps `jpeg_end`'s callers untouched.
- The five models each carry exactly the parameters their tests and notes name; I found no dead parameter
  except `gauge_t` (an alias for `head_gap`, 1 line; delete it and use `head_gap`, minor).
- Tasks 9 to 11 are three separate Dan tasks for three different questions (looks, load, install) and each
  gates the next at a cost of a few hundred grams of PLA; merging them would lose the cheap gate (D8).
- Task 2's close "Forward" list is long but each item is a real dependency from a measurement to a parameter;
  a table would read better but decides nothing new.
- `offsite.py`'s CSS pass is the only part that would have caught the Google fonts leak; keep.
