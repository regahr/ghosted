# Brett Bullet-Points v1 self-check (Viet Tran, builder, 2026-11-26)

Rules: every claim names an image. A visible fault is never PASS. Rega is the gate; the chair checks at 2x first.
Paths are in `assets/brett/v1/`.

## Counts (Fact: `brett_build_report.json`; three.js `ingame_report.json` `visibleTris` gives the same totals)
| State | body | decals | eyes | brows | mouth | hand swap | Visible total | Cap |
|---|---|---|---|---|---|---|---|---|
| rest / idle | 1,208 | 78 | 40 (open) | 12 | 24 (grin) | - | **1,362** | 1,400 |
| the Like | 1,208 | 78 | 28 (wink) | 12 (smug) | 24 | 18 (thumb) | **1,368** | 1,400 |
| bullets (3 fingers) | 1,208 | 78 | 40 | 12 | 13 (talk) | 36 | **1,387** | 1,400 |
| talk / lost | 1,208 | 78 | 40 | 12 | 13 / 12 | - | **1,351 / 1,350** | 1,400 |

- Body by part: head + hair cap + hairline ink 288, swoop 126, halo 120, ears 32, neck 16, vest 208, hips 50, arms
  140 + 140, legs + shoes 88.
- Meshes: non-swap **2** (`body`, `decals`; both skinned; the halo is inside `body` on its own bone). Swap parts:
  `eyes_open`, `eyes_wink`, `brows_rest`, `brows_smug`, `brows_lost`, `mouth_grin`, `mouth_talk`, `mouth_lost`,
  `thumb`, `fingers_1`, `fingers_2`, `fingers_3`. 14 meshes in `brett.glb`.
- Body: 0 non-manifold edges, 0 faces against the analytic normals, 0 unweighted vertices; 66 open edges (buried ends:
  neck tube, vest top ring round the neck, hips top, leg ends).
- Like, bullets and hips: the hand centre reaches the pose target, 0.0 mm off.
- Blender vs three.js: mean difference 1.07 / 255 (3/4) and 1.11 / 255 (front); 0.58 % and 0.61 % of pixels differ by
  more than 40 (`compare-ingame.png`, `compare-ingame-front.png`).

## Requirements
| # | Requirement | Verdict | Proof |
|---|---|---|---|
| 1 | 1,400 visible triangles or fewer in every beat, at most 3 non-swap meshes | **PASS** (max 1,387 in bullets; 2 meshes) | table above |
| 2 | Matches the sketch: direction A wedge; front / 3/4 / side / back agree; upright, symmetric but the part and swoop | **PASS with weak points 3, 7, 8, 9** | `turnaround.png`, `compare-sketch.png`, `hero.png` |
| 3 | Size 1.05 x Kit without the halo, set in the blockout, measured as Ricky (chair call 1) | **PASS** (79 / 75 px = 1.053, both lineups; H 1.235 m) | `measure.md` "Scale"; `blockout/ingame_report.json`; `blockout/blockout-sheet.png` |
| 4 | Row 7 vest, row 23 shirt, row 12 hair, row 15 skin, row 26 chinos, row 5 shoes, row 2 halo, row 22 ink; no green on the body (chair call 2) | **PASS, weak point 6** | `brett_toon.json`, `build_brett.py` `PAL`, `grey.png` |
| 5 | Halo: row 2 with an ink edge; level; follows the head; stays level under the nod (chair call 3) | **PASS** (0.000 deg from world up after the carriage) | `crops/halo-front-x2.png`, `crops/close-halo.png`, `crops/close-top.png`, `crops/gamecam-rest-x3.png`; `brett_build_report.json` `carry_*` |
| 6 | Chin up 10 deg at rest in game, turnaround neutral (chair call 4) | **PASS** | `idle.png`, `hero.png` (carriage); `turnaround.png` (neutral); `gamecam-beats-x3.png` |
| 7 | Grin: white teeth crescent, no edge, over an ink smile line, corners up; reads as a grin at 1x, not a moustache (chair call 5) | **PASS, weak point 4** | `measure.md` "The grin at 1x"; `crops/gamecam-face-hair-grass.png`, `crops/gamecam-face-x3-grass.png`, `expressions.png` |
| 8 | No grin sliver or brow tip on the side profile (chair call 6) | **FAIL** (weak point 1; two fixes tried, stopped) | `crops/face-side-x2.png`, `crops/close-face-side.png` |
| 9 | No hair notch at the far ear in 3/4 (chair call 6) | **PASS** | `crops/ear-34-far-x2.png`, `crops/ear-34b-far-x2.png`, `crops/close-ear34-far.png` |
| 10 | Hair does not cross the eyes; no fringe: forehead band >= 4 px at 1x; side hair above the eye line and behind the ears (chair rules, Rega ts 1795658703.410809) | **PASS** (gap 8-9 px; band 5-8 grass, 4-5 path; side hair 7-8 px above the eye top) | `measure.md` "Hair against the eyes"; `crops/gamecam-face-hair-*.png`, `crops/gamecam-face-x3-*.png` |
| 11 | Confident idle: hands on hips, puff = lean back 3 + rise 3 units, feet planted | **PASS, weak point 8** | `idle.png` (rest, settle, puff, side, three.js) |
| 12 | The Like: his right fist out at the side, thumb up, wink | **PASS** | `like.png`, `crops/like-hand-front-x2.png`, `crops/like-hand-34-x2.png`, `crops/gamecam-like-x3.png` |
| 13 | Bullets: his right hand counts 1-2-3, mouth open, other hand on the hip | **PASS for the pose; weak point 3 for the mouth at 1x** | `bullets.png`, `crops/bullets-hand-front-x2.png`, `crops/gamecam-bullets-x3.png` |
| 14 | Expressions: grin, talk, wink, secretly lost | **PASS** | `expressions.png` |
| 15 | Lineups with Kit, Ricky, Dot, the ATS and Ghosties; grass and path; colour and grey; x3 and 1x | **PASS, weak point 2 (collar at 1x)** | `lineup-{grass,path}{,-grey}-crop-{x3,1x}.png` |
| 16 | Silhouettes, grey, in-game render and compare | **PASS** | `silhouette-64*.png`, `grey.png`, `ingame*.png`, `compare-ingame*.png` |
| 17 | Skill steps before the model: ready, direction, joins, tool outputs, blockout at the game camera | **PASS** | `ready.md`, `direction.md`, `skill/`, `blockout/` |

## Weak points still visible (Fact unless marked)
1. **Side profile ticks (chair call 6 not met).** In the pure side view the near brow, eye and the grin corner show
   as small marks on and just past the face outline (`crops/face-side-x2.png`). Root cause: the face decals sit on
   the analytic head surface, which is up to about 1 unit outside the 16-column, 4-band facets, so near the profile
   they stand proud of the mesh and draw over the ink hull. Tried (each once): (a) project the marks onto the real
   facets: every mark that spanned a facet ridge sank and broke up; (b) skin rings at fixed face rows so no mark
   spans a ridge: the rows crossed the temple rings and folded faces. Stopped by the "no blind iterations" rule.
   Not visible at the game camera. Options for Rega:
   1. accept it (side card view only);
   2. **my pick:** add one face column each side and one skin ring under the eyes so the facets follow the analytic
      surface (about +70 triangles), paid for by a 4-sided halo tube (-24), 6-sided swoop (-18) and 6-sided hands
      (-28);
   3. bake the face marks into a small texture on the head (a new method for this family).
2. **Collar wedges.** A small dark ink wedge sits at the top corner of each collar wing, where the wing fan crosses
   the steep shoulder shelf (vest r 14 to 38 in 3 units). At the game camera x3 the collar reads as a small dark bow
   under the chin (`crops/gamecam-rest-x3.png`, `crops/collar-front-x2.png`, `hero.png`). Tried: thinner wing ink
   (better), wing strips (worse: lost the tip, the vest showed through); stopped. Options: drop the wing ink; move the
   collar down off the shelf (y >= 156); or model the two wings as small 3D flaps (about +16 triangles).
3. **Bullets mouth at 1x.** The open talk mouth is a dark fill; at the game camera it is a dark mark under the eyes
   that can read as a goatee (`crops/gamecam-bullets-x3.png`). Opinion: show it only on each bullet pop, or use a
   smaller mouth with a wider teeth band.
4. **Grin at 1x.** It touches the eyes (0-1 px gap) and the ink line mostly drops out (1-4 px), so it reads as a light
   crescent. Light, not dark, so not a beard (`measure.md`).
5. **Facets at 2x.** Jaw, 7-sided sleeves and hands, the 12 x 5 halo and the hair cap edge show their corners in close
   views (`hero.png`, `crops/close-hands.png`). The V ribs show small gaps (`crops/collar-front-x2.png`).
6. **Colour under the light.** The row 7 vest renders more orange-red than the flat sketch swatch under Kit's warm
   light (`turn-front.png` vs `../sketch/brett-sheet.png`); the same shift as Dot's hair. Not a palette change.
7. **Changes from the sketch, on purpose:** the front hairline is y 56 (sketch 62) and the swoop root is 6 up and 4
   back, for the chair's no-fringe rule (`build_brett.py` `HAIRLINE`, `WAVE3`). The swoop still rolls forward over
   the crown as in the sheet's side view.
8. **Idle elbows.** The bones keep one length, so the hands-on-hips elbows stand out less wide than the sketch's
   idle (`idle.png` vs `../sketch/crops/sheet-idle.png`). I moved the fist target to (46, 240, 12) to open them a bit.
9. **Back of the head.** The back hair is a big smooth dome to the nape; the back hairline is straight with small
   corners at the columns (`crops/hair-back-x2.png`). The sketch back is the same shape.

## Whole-picture check (2x, panel by panel)
- `turn-front.png`: symmetric apart from the part and the swoop; ring level and centred; collar wedges (weak point 2).
- `turn-34.png`, `turn-34b.png`: hairline above the ears, then behind them; no ear notch; collar wedge on the near side.
- `turn-side.png`: brow / eye / grin ticks at the profile (weak point 1); swoop rolls forward and up; ring level.
- `turn-back.png`: hair dome to the nape, ears out, no stray lines.
- `idle.png`, `like.png`, `bullets.png`, `expressions.png`: no part floats, no clipping seen; the thumb and fingers sit
  on the fist; the ring stays level in every pose.
- `lineup-*-crop-x3.png`: clear of every other character; reads as ring, blond roll, red wedge.

## Fixes made during this build (each seen once, fixed once)
- Over budget (1,450 rest, 1,499 bullets) -> fewer vest bands, 2-ring legs, 7-sided swoop and sleeves, 10-column hips,
  capless thumb and fingers.
- Collar marks above y 150 collapsed to the axis (the vest profile has r 0 there) -> a mark surface never narrower
  than r 26 above y 156.
- The shirt V's single fan sank under the vest facets (a red diamond) -> the V is built as two strips.
- Pointed hands -> 3 latitude rings.
- Neck ink ring at the vest -> the neck and the vest top ring fade their outline weight to 0 (Kit's `outline_wc`).
- Lineup spot: (-3.05, 6.45) touched the ATS, (-3.8, 3.9) a Ghostie -> (-3.45, 4.4).
