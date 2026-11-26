# The Panel v1: self-check (Viet Tran, 2026-11-26)

Paths are relative to `runs/jobless-roguelike/design/assets/panel/v1/`. A visible fault is not a PASS.

## Skill steps run (offer is not use)
`ready.md`, `direction.md` (steps 1, 2, 4, 5: hardest parts, join decisions), `skill/search.txt`,
`skill/design-context.txt`, `skill/host-probe.txt`. Blockout first: `blockout/` (glb, renders, `blockout-sheet.png`,
`measure.json`). Hardest part 1 (the face at 1x) was tested on the blockout and failed there; it was fixed before the
final (see `measure.md`).

## Items
| # | Item | Result | Proof |
|---|---|---|---|
| 1 | Matches the accepted sketch (direction A): bow + band + bun, flat-top + glasses, black cube with a cream icon, light panel desk, chairs | PASS | `compare-sketch.png`, `turnaround.png` |
| 2 | Budget: 2,000 visible tris or fewer; 4 non-swap meshes | PASS: 1,867 game idle, 1,891 max; meshes table, cf, wb, box_body | `panel_build_report.json` |
| 3 | Scale: table top 0.733 m = 0.75 Kit; Kit-sized heads | PASS (heads 23.2 px vs sketch 21.1 px; see `measure.md`) | `measure.md` Scale |
| 4 | No fringe: band 4 px or more; nothing at the temples | PASS (4-7 px; side hair 8-11 px above the eyes) | `gamecam-face-x3.png`, `crops/face-mask-*` |
| 5 | Mouths: Ricky style or closed line; idle in game = TALK; no beard at 1x | PASS for idle, lean, grin at rest | `gamecam-face-x3.png`, `measure.md` |
| 6 | Motion: CF nod + tilt, WB marker up / click / point, box camera-off / dark / muted, all lean in | PASS (all built and rendered) | `motion.png`, `gamecam-beats.png` |
| 7 | CF grin keeps skin above the chin line at 1x (chair call 5) | **FAIL at the nod's lowest frame** (0 rows); PASS at the rest head (2 rows) | `crops/face-grass-nod-cf.png`, `crops/face-mask-grass-nod-cf.png` |
| 8 | Lineups: Kit in front, grass and path, colour and grey, x3 and 1x | PASS | `lineup-*-crop-x3.png`, `lineup-*-crop-1x.png`, `lineup-*-grey*.png` |
| 9 | The three read apart by silhouette | PASS (Opinion): round head + bow lobes; square block; low cube | `silhouette-64.png` |
| 10 | Views agree; nothing floats, sinks or sticks out (2x check) | PASS with the weak points below | `crops/*-x2.png` |

## Item 7: options for the chair (not decided by me)
1. **Grin only on the way up** (my pick): the grin shows from the nod's top to the middle; the lowest frame uses the
   talk mouth. No model change; a motion timing rule (Emil's area).
2. Make the nod shallower: -8 to 0 (not +6). Changes the body-map number.
3. Raise the grin 2 u more. It then nearly touches the eye line at card size.

## Weak points (visible, not fails)
- The mouths sit 4 u higher than the sketch. At card size the talk and grin mouths sit close under the eyes (Opinion:
  still cute, but higher than the sketch).
- Rest lines and the CF smirk are 0 px at 1x: in the tilt beat CF has no mouth in game.
- WB *click* is the same pose as "marker up" with the talk mouth; there is no thumb on the cap.
- Hands (6-sided balls) and cuffs read as hexagons at card size; the heads are 14-sided.
- Lower face toon shade is a darker band at card size (the same toon band as the cast).
- Card views are rendered in three.js (the game renderer), not with Juno's Blender toon pass: what is shown is what
  plays. The Illustrator paint-over of the blockout did not happen (not in my brief).
- Grass lineup: the set stands on the free grass corner (3.05, 5.15); a tree stands behind-right of the box.
