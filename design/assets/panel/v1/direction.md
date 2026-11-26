# The Panel 3D v1: direction (Viet Tran, 2026-11-26; 3dviz-pro-max steps 1, 2, 4, 5)

Paths are relative to `runs/jobless-roguelike/design/`.

## Step 1: intent and visual direction
- The player meets three interviewers at one light table. The joke reads first: "a black box is on your panel".
  Comic and kind (`acceptance/panel/brief.md` Tone).
- Direction A of the accepted sketch, matched shape for shape (`assets/panel/sketch/panel-sheet.png`, `body-map.md`):
  round head + cream bow (Culture Fit), square brown flat-top + glasses (Whiteboard), a plain black cube with a cream
  icon (the box). Toy-pawn toon family: Kit's toon bands, 1.6 px ink hull, Neutral tone map (`assets/juno/v1/ingame.html`).
- Viewing distances: game camera (26 m, pitch 42, yaw 20; a head is about 20 px), card views (front, 3/4, side, back),
  face close-ups at x3 of 1x.

## Step 2: hardest parts (each solved first on a small case: the blockout head-and-face render at the game camera)
1. **The face at 1x.** Pitch 42 eats the chin. The mouth must not read as a beard, the CF grin must keep skin above the
   chin line, and the forehead band must stay 4 px or more. Fix carried from the sketch: head set chin-up 8 deg, mouths
   5 u higher than Juno's. Test: blockout `ingame` face mask render, measured before the final.
2. **Arms that lie on the table.** Rigid two-bone arms; the forearm and hand rest on the top (H 230 to 240), no gap, no
   sink deeper than 3 u. Other poses (marker up, point, hand under the chin) by a two-bone reach to the sketch targets.
3. **The budget.** 2,000 visible tris for four people-sized things. Spend on the head contour and the bow / flat-top;
   cut the hidden parts (legs and chairs stay low: 5-sided tubes, plain boxes).

## Step 4: construction and joins
Route: custom geometry from the sketch's own profiles (`sketch/src/panel.py`, `juno.py`), built in Blender, exported as
one glb, rendered in three.js (Juno v1 pipeline). Join decisions:

| Join | Decision | Why |
|---|---|---|
| Skull and hair cap | **continuous skin**: one grid, the hair rows on the cap profile, a thin ink band at the hairline, skin rows below | no step or gap at the hairline; the hairline cannot hang (Juno v1 method) |
| Flat-top on the skull | **layered**: a bevelled block sunk into the cap, its front edge on the skull above the hairline | it must read as hair on top, not a hat, and never as a fringe |
| Bow, headband, bun | **layered**, sunk into the cap | accessories |
| Ears | **layered**, half sunk on the eye line | Juno method |
| Neck in the torso | **separate, sunk**; the collar fill covers the join | cheap, no seam at the game camera |
| Shoulder, elbow, wrist | **separate rigid parts** on bones: sleeve tube sunk into the torso, a ball cuff at the elbow, a ball hand | rigid poses do not pinch; the balls hide the bend |
| Forearm on the table | **contact**: the part rests on the top, ink hull marks the contact | sketch note "toon edge on the contact" |
| Marker in the hand | **separate part** in the WB mesh, on the right forearm bone | it follows the hand in every pose |
| Face marks, V-necks, pocket, glasses, cheeks | **decal cards** projected on the analytic head / torso, no ink hull | sketch: fills with no ink edge |
| Torso and table | torso runs down to the seat; the table hides the cut | the front panel hides it |

## Step 5: quality targets and tools
- Game camera: the three read apart by silhouette; forehead band 4 px or more; no beard read; scale = sketch.
- Card: views agree; no floating or crooked parts at 2x.
- Tools found (`skill/host-probe.txt`): Blender 4.3 (build), three.js r170 + Playwright (render, measure), PIL.
- Records retrieved: `skill/search.txt` (low-poly shape economy: spend tris on the contour), `skill/design-context.txt`.
  Used as guidance only; no kit is used.
