# Gary 3D v1: direction (Viet Tran, 2026-11-26; 3dviz-pro-max steps 1, 2, 4, 5)

Paths are relative to `runs/jobless-roguelike/design/`.

## Step 1: intent and visual direction
- Gary brings every result. He must be the kindest, softest beat in the game: round, a bit bumbling, sincere
  (`acceptance/gary/brief.md` Role).
- Direction A of the accepted sketch, matched shape for shape (`assets/gary/sketch/gary-sheet.png`, `body-map.md`):
  a round head on a tilted egg body, a navy kepi set back on the crown, a gold cone beak, blue rigid wings with 3 finger
  feathers, a flat blue tail fan, a brown satchel on his left belly, gold legs.
- Family look: Kit's toon bands, the 1.6 px ink hull, Neutral tone map (`assets/panel/v1/ingame.html`).
- Viewing distances: the game camera (26 m, pitch 42, yaw 20; he is about 35 px tall), card views, face close-ups at
  x3 of 1x.

## Step 2: hardest parts (each solved first on a small case: the blockout, rendered at the card and game cameras)
1. **The folded wing from the front.** The sketch fold reads as hanging arms (chair call 4). Test: the blockout front
   view. Fix: the wing root moves back (Z -8 to -16), the arm runs less forward and more down, and the wing hugs the
   body side, so from the front only a thin blue edge shows at each side.
2. **The strap in the side view.** The sketch strap is a planar loop through the left hip, so the side view shows a
   low loop under the wing. Fix: a non-planar sash path through 7 key directions: the right shoulder top, the chest,
   the bag top, his left side at the wing line (H about 72, under the folded wing), the back, and back over the right
   shoulder. It is a flat ribbon on the body (no ink hull), to save triangles.
3. **The eyes against the cap at 1x.** The eyes grow 15 %; the cap must still clear them. Test: the mask render at the
   game camera (cap red, eye ink blue), measured in pixels.
4. **The budget.** 900 visible triangles. Spend on the body, head, cap and beak contour; thin the feathers (bicones of
   12 tris), the strap (a ribbon of 2 tris per segment), the cere and badge (decal fans).

## Step 4: construction and joins
Route: custom geometry from the sketch's own numbers (`sketch/src/gary.py`), built in Blender, exported as one glb,
rendered in three.js (Panel v1 pipeline). Records read: `skill/resolve-wing.txt` (a wing is a folding support
hierarchy; the feather field must stay attached through the fold), `skill/resolve-flight.txt` (the flap is an authored
key cycle, not a flight simulation). Used as guidance; no kit is used.

| Join | Decision | Why |
|---|---|---|
| Head on body | **layered, sunk** (the head ball sinks into the egg); the ink hull weight fades to 0 on the lower head | the sketch has no neck line; a continuous loft would cost the same tris and lose the sketch's ball-on-egg read |
| Cap on head | **layered**: a revolved kepi sunk 10 u into the crown, tilted back 14 deg; brim and badge on the cap | as the body map; the cap must never reach the eyes |
| Beak and cere | **layered**: a 6-sided cone sunk into the face; the cere is a decal fan | cheap; clear beak read |
| Wings at the shoulder and the wrist | **separate rigid parts** on 2 bones each (arm, hand + 3 feathers); the hand overlaps the arm | the sketch says rigid; feathers overlap the joint, so no skin is needed |
| Tail | **layered**, sunk into the back of the egg | as the sketch |
| Legs and feet | **separate rigid parts** on a leg bone each (stand, tucked) | as the sketch |
| Bag on belly | **layered** box in the body mesh; the flap is a swap (closed, open with a letter) | budget: 3 non-swap meshes |
| Strap | **decal ribbon** on the body surface, no ink hull | budget; the sash route (hardest part 2) |
| Eyes, glints, brows, lids | **decal swaps** projected on the head ball | expressions by swap |
| Envelope | **swap part**: socket 1 on the head bone (beak), socket 2 on the right hand bone (wing hold) | body map: one socket at a time |

## Step 5: quality targets and tools
- Game camera: reads as "bird plus post" (cap, beak, satchel); separates from grass and path by outline, wings, cap and
  bag; the cap clears the eyes; the eyes are visible at 1x; scale 0.5 x Kit.
- Card: views agree with the sketch; nothing floats, sinks wrongly or sticks out at 2x.
- Tools (`skill/host-probe.txt`): Blender 4.3 (build), three.js + Playwright from `concept/node_modules` (render,
  measure), PIL (sheets).
