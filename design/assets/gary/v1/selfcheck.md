# Gary v1: self-check (Viet Tran, 2026-11-26)

Paths are relative to `runs/jobless-roguelike/design/assets/gary/v1/`. A visible fault is not a PASS.

## Skill steps run (offer is not use)
`ready.md`, `direction.md` (steps 1, 2, 4, 5: hardest parts, join decisions), `skill/search.txt`,
`skill/design-context.txt`, `skill/host-probe.txt`, `skill/resolve-wing.txt`, `skill/resolve-flight.txt`.
Blockout first: `blockout/` (glb, turn views, lineups). Hardest part 1 (the folded wing from the front) was tested on the
blockout: the first fold sank into the body and showed as broken patches in the side view; the wing was moved out to
11 u off the body before the final.

## Items
| # | Item | Result | Proof |
|---|---|---|---|
| 1 | Matches the accepted sketch (direction A): round head, egg body, navy kepi, gold beak, blue wings and tail, satchel, strap, gold legs | PASS, with weak points 2 and 3 | `compare-sketch.png`, `compare-ingame.png`, `turnaround.png` |
| 2 | Budget: 900 visible tris or fewer; 3 non-swap meshes | PASS: max 886 (sorry), rest 832; body, wing_R, wing_L | `gary_build_report.json`, `measure.md` |
| 3 | Scale 0.5 x Kit; wingspan 1.06 x Kit | PASS: 35-36 px vs Kit 75 px; span 1.032 m = 1.056 x Kit, 80 px | `measure.md` |
| 4 | Eyes 15 % bigger; the cap never covers the eyes | PASS: cap 3-5 px clear in all renders | `measure.md`, `gamecam-face-x6.png` |
| 5 | Face: eyes + brows only, a clear beak, no mouth | PASS | `expressions.png` |
| 6 | Folded wings tucked back and in: no "hanging arms" from the front | PASS | `turnaround.png` front, `crops/turn-front-x2.png` |
| 7 | Strap is not a low loop in the side view | PASS: it crosses his left side at the wing line | `turnaround.png` side, `crops/turn-side-x2.png` |
| 8 | Flight flap keys: up 50, level 5, down -35; legs tucked; pitch 10; letter in the beak | PASS | `flight.png` |
| 9 | Delivery beats: land hop, hold letter, sorry tilt, happy hop (and fly off) | PASS | `beats.png`, `gamecam-beats.png` |
| 10 | Expressions: rest, happy, sorry, oops | PASS | `expressions.png` |
| 11 | Silhouettes, grey render, in-game render | PASS | `silhouette-64.png`, `grey.png`, `ingame.png`, `hero.png` |
| 12 | Lineups with Kit and the cast, grass and path, colour and grey, x3 and 1x | PASS | `lineup-*.png`, `lineup-*-crop-x3.png`, `lineup-*-crop-1x.png`, `lineup-*-grey*.png` |
| 13 | Separates from grass and path at the game camera | PASS (Opinion): ink outline, navy cap, blue wings, brown bag | `gamecam-beats.png`, `lineup-*-grey-crop-x3.png` |
| 14 | Eyes read at 1x | **WEAK, not a PASS** (weak point 1) | `gamecam-face-x6.png` |
| 15 | Views agree; nothing floats or sticks out (2x check) | PASS with weak points 2-4 | `crops/*-x2.png` |

## Weak points (open)
1. **The eyes at 1x are only just visible.** They are 2.6-2.8 px tall by geometry, but only 1-2 px of pure eye ink
   survive anti-aliasing; they read as two dark dots beside the beak. Options for the chair (not decided by me):
   1. Grow the eyes another 15 % (about 3.0 px). The brows must then go up 2 u more; the cap still clears by about 2 px.
      My pick.
   2. Keep them; the face reads in the card and close-up views, and at 1x the read is "cap + beak".
   3. Add a cream eye ring (a white ring round each eye) for contrast. It costs about 24 tris (budget left: 14 at the
      sorry beat), so a strap or tail cut is needed.
2. **The back of the neck has a small waist.** In the back and side views the neck blend shows a step with two short
   ink ticks (`crops/turn-back-x2.png`). It does not show at the game camera.
3. **The folded wing is smaller than the sketch's in the side view.** This is the price of the chair's "tuck back and
   in" call (`turnaround.png` side vs `compare-sketch.png`).
4. **The head and body still show facets at card size** (10-sided rings, to stay under 900). They do not show at the
   game camera.

## Pass 2 (Rega card 9, "a bit awkward, and 2"), 2026-11-26
The files from before the pass are in `../v1-pre-pass/`. Proof: `satchel-pass2.png` (before and after: front, 3/4, side, plus
close-ups), `crops/satchel-front.png`, `crops/satchel-34.png`, `crops/satchel-side.png`, `gamecam-beats.png` (x3),
`gamecam-face-x6.png`, `measure.md` "Pass 2".

| Item | Result |
|---|---|
| Eyes +15 % (option 2), brows +2 u, cap clears the eyes | PASS: 3.0-3.2 px geometric; cap clear 3-4 px |
| Eyes read at 1x | still WEAK on grass (1-2 px of pure ink); better on the path |
| The strap joins the bag at both ends | PASS in the front and 3/4 views. Side view: WEAK. The outer end goes down into the bag under the folded wing, so from the side the strap seems to stop at the wing's front edge. |
| The bag sits snug on the body curve, wrapped and tilted, not a floating slab | PASS (front, 3/4, side) |
| The flap has a soft, rounded edge | PASS |
| Budget 900 | PASS: max 896 |
