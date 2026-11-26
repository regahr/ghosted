# Ricky v1 self-check (Viet Tran, builder, 2026-11-25)

Rules: every claim names an image. A visible fault is never PASS. Rega is the gate; the chair checks at 2x first.
Paths are in `assets/ricky/v1/`.

## Counts (Fact: `ricky_build_report.json`; three.js `ingame_report.json` `visibleTris`)
| State | body | decals | mouth | Visible total | Cap |
|---|---|---|---|---|---|
| rest (grin) | 1,216 | 152 | 24 | **1,392** | 1,400 |
| phone | 1,216 | 152 | 24 | **1,392** | 1,400 |
| drain step 1 ("o") | 1,216 | 152 | 12 | **1,380** | 1,400 |

- Body by part: head + hair cap with the quiff 368, jacket 272, arms 176 + 176, legs + shoes 88, cups 48, band 60, mic 28.
- Non-swap meshes: **2** (`body`, skinned; `decals`). Swap parts: `mouth_grin`, `mouth_o`.
- Body: 0 non-manifold edges, 0 unweighted vertices, every face wound to the analytic normals.
- Blender vs three.js: mean difference 1.25/255 (3/4) and 1.36/255 (front); 0.98 % and 1.09 % of pixels differ by
  more than 40 (`compare-ingame.png`, `compare-ingame-front.png`).

## Brief requirements
| # | Requirement | Verdict | Proof |
|---|---|---|---|
| 1 | 1,400 visible triangles or fewer; at most 3 non-swap meshes | **PASS** (1,392; 2 meshes) | table above |
| 2 | Direction A bell, 2.67 heads; turnaround matches the sheet (front, 3/4, side, back); upright, symmetric mesh | **PASS, with weak points 1-4 below** | `turnaround.png`, `compare-sketch.png` |
| 3 | Palette rows only (17, 15, 25, 16, 10, 5, 22) and a neutral shade band | **PASS** | `ricky_toon.json`, `grey.png`; drain rows 11, 27, 16 |
| 4 | Headset centred over the crown, a cup on each ear point, mic from the right cup, all with ink | **PASS** | `turn-front.png`, `crops/cup-mic-right-front-x2.png`, `crops/hair-back-x2.png` |
| 5 | Tie centred under the collar, with ink | **PASS, weak point 5** | `crops/collar-knot-front-x2.png`, `crops/tie-shirt-v-front-x2.png`, `crops/close-tie.png` |
| 6 | Joins decided; no seam, crease or hook at card size | **WEAK** (points 6-7) | `direction.md` §3; `crops/shoulder-join-*`, `crops/phone-elbow-front-x2.png` |
| 7 | Hop: squash only on the bounce, as Kit | **PASS** | `hop.png` (squash, stretch +0.16 m with arms out, squash) |
| 8 | Phone: right hand to the right cup (bone) | **PASS** | `phone.png` (Blender front, 3/4, and three.js), `crops/phone-hand-cup-*.png`; hand-to-target 0.0 mm |
| 9 | Drain: suit 17 -> 11 -> 27 -> 16, legs fade, floats up, headset Ghostie swaps in; legs as own part; float node | **PASS, weak point 8** | `drain-strip.png` (three.js) |
| 10 | Game camera: a dark bell with a white V, in a greyscale lineup with Kit and the Ghosties | **PASS, weak point 9** | `lineup-grass-grey-crop-x3.png`, `lineup-path-grey-crop-x3.png` |
| 11 | Scale: 1.05 x Kit on screen | **PASS** (79 / 75 px = 1.053, both lineups) | `measure.md` |
| 12 | Hair change: no fringe; hairline above eyes and brows; quiff and row 25 kept; mic unchanged | **PASS** (hair low point 10-11 px above the eye top at 1x) | `measure.md`, `crops/gamecam-face-hair-grass.png`, `crops/gamecam-face-x3-*.png`, `crops/close-top.png` |
| 13 | Skill steps before the model: ready, direction, joins, tool outputs, blockout at the game camera | **PASS** | `ready.md`, `direction.md`, `skill/`, `blockout/` |

## Weak points still visible (Fact unless marked)
1. **Facets at 2x.** The jaw outline of the head and the 8-sided hands show their edges in the 2x crops
   (`crops/face-front-x2.png`, `crops/hand-cuff-34-x2.png`). The budget is spent (1,392 of 1,400). Kit has the same
   limit (`kit/LOCKED.md`).
2. **Arms vs the sketch.** The sheet draws an ink line down the inner side of each sleeve. In 3D the sleeve meets the
   bell and shows the inner ink only from the elbow down (`crops/shoulder-join-front-L-x2.png`). Opinion: at card size
   the arms read, but less clearly than on the sheet.
3. **Side view.** The shirt V shows as a thin white line along the front edge of the jacket
   (`turn-side.png`, `crops/arm-side-x2.png`), and the shoes read as flat brown slabs (`crops/shoes-side-x2.png`).
4. **Band gap.** The band clears the hair by 4-9 units (1.6-3.6 cm) (`ricky_build_report.json`
   `band_extra_gap_to_hair_units`). The sheet band also stands off the head. Opinion: it reads as a headset, not a
   float.
5. **Shirt V edge.** A small ink tick on the left edge of the V near the collar (`crops/close-tie.png`).
6. **Near-arm ink in 3/4.** The inner ink line of the near sleeve ends in a small blob above the cuff
   (`crops/shoulder-join-34-near-x2.png`).
7. **Decals at steep angles.** At -60° (`crops/close-headset.png`) the grin and teeth stick out past the cheek outline.
   The sheet views (0°, -35°, -90°, 180°) do not show it. **Not a PASS** in that close view.
8. **Drain end.** Step 3 still has arms and hands when the Ghostie swaps in, and the half-way phone frame swings the arm
   straight out (`phone.png`, panel 3). Both are in-between frames; Emil should check the timing.
9. **Grin at 1x.** At the game camera the dark grin under the eyes can read as a beard or moustache
   (`crops/gamecam-face-x3-grass.png`). The sheet's game-camera tile shows the same read. This is a face-design question
   for the chair or the Illustrator, not a build fault.

## Whole-picture check (2x, panel by panel)
- `turn-front.png`: symmetric; hairline above the brows; jaw facets; arms merge with the bell above the elbow.
- `turn-34.png`: near-arm ink blob; far side hair stays above the brow line.
- `turn-side.png`: flat-top band end above the hair (as the sheet's knob); white V line on the jacket front; slab shoes.
- `turn-back.png`: hair covers the back to the nape with a round edge; band and cups centred.
- `phone.png`: hand on the lower cup, mic boom in front of the hand; the elbow is a round ball, no crack.
- `hop.png`: upright; squash and stretch from the soles.
- `drain-strip.png`: colours step 17 -> 11 -> 27 -> 16; legs, shoes, mic and tie fade with their ink; no mouth in step 2.
- `lineup-*-crop-x3.png`: dark bell, white V, lilac ring; Ricky 79 px beside Kit 75 px.
