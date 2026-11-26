# Auntie Dot v1 self-check (Viet Tran, builder, 2026-11-26)

Rules: every claim names an image. A visible fault is never PASS. Rega is the gate; the chair checks at 2x first.
Paths are in `assets/auntie-dot/v1/`.

## Counts (Fact: `dot_build_report.json`; three.js `ingame_report.json` `visibleTris`)
| State | body | decals | eyes | mouth | card | Visible total | Cap |
|---|---|---|---|---|---|---|---|
| rest | 1,180 | 108 | 40 (open) | 12 (smile) | - | **1,340** | 1,400 |
| talk | 1,180 | 108 | 40 | 9 (open D) | - | **1,337** | 1,400 |
| card | 1,180 | 108 | 40 | 12 | 22 | **1,362** | 1,400 |
| happy | 1,180 | 108 | 16 (closed) | 12 | - | **1,316** | 1,400 |

- Body by part: head + hair + hairline ink 288, bun 60, ears 32, neck 16, pear 240, arms 144 + 144, legs + shoes 88,
  band 104, cups 64.
- Meshes: non-swap **2** (`body`, `decals`; both skinned). Swap parts: `eyes_open`, `eyes_happy`, `mouth_smile`,
  `mouth_talk`. Prop: `card` (shown only in the card beat). 7 meshes in the file.
- Body: 0 non-manifold edges, 0 faces against the analytic normals, 0 unweighted vertices; 64 open edges (the
  buried ends: neck tube, body top ring under the neck, leg tops, band ends inside the cups).
- Talk and card: the hand centre reaches the sketch target, 0.0 mm off (`dot_build_report.json`).
- Blender vs three.js: mean difference 1.19 / 255 (3/4) and 1.21 / 255 (front); 0.70 % and 0.72 % of pixels differ by
  more than 40 (`compare-ingame.png`, `compare-ingame-front.png`).

## Brief requirements
| # | Requirement | Verdict | Proof |
|---|---|---|---|
| 1 | 1,400 visible triangles or fewer, at most 3 non-swap meshes | **PASS** (1,340 rest, 1,362 card beat; 2 meshes) | table above |
| 2 | Matches the sketch: direction A cottage loaf, front / 3/4 / side / back agree; upright, symmetric | **PASS, with weak points 1-5** | `turnaround.png`, `compare-sketch.png`, `hero.png` |
| 3 | Palette rows only (11, 23, 15, 22, 27, 5; card 23 / 24 / 13); neutral grey shade band | **PASS, weak point 6** | `dot_toon.json`, `grey.png` |
| 4 | Hairline has an ink edge; the side hairline curves down behind the ear (chair call 2) | **PASS** | `crops/hairline-ear-side-x2.png`, `crops/close-ear.png`, `crops/hair-34-x2.png`, `crops/close-nape.png` |
| 5 | Smile small and curved; at 1x not a moustache or beard (chair call 3) | **PASS, weak point 7** | `measure.md` "The smile read"; `crops/gamecam-face-x3-grass.png`, `crops/gamecam-face-hair-grass.png`, `expressions.png` |
| 6 | Skill card: row 23 face, row 13 disc, row 24 edge, in her right hand (chair call 4) | **PASS** | `card.png`, `crops/card-hand-front-x2.png`, `crops/close-card.png`, `crops/gamecam-card-x3.png` |
| 7 | Headset: band round the neck, a cup on each collarbone, no mic, row 27 (chair call 5) | **PASS, weak point 8** | `crops/close-headset.png`, `crops/band-back-x2.png`, `crops/cup-right-front-x2.png` |
| 8 | Size 0.9 x Kit on screen, set in the blockout, measured as Ricky and the ATS (chair call 6) | **PASS** (68 / 75 px = 0.907 at Kit's spot, both lineups; 0.98 m) | `measure.md` "Scale"; `blockout/ingame_report.json` |
| 9 | Hair and bun do not cross the eyes at the game camera | **PASS** (hair low point 8-9 px above the eye top at 1x) | `measure.md`; `crops/gamecam-face-hair-grass.png`, `crops/gamecam-face-hair-path.png` |
| 10 | Idle sway +-4 deg about the feet, head lags 2 deg, feet planted | **PASS** | `sway.png` (Blender -4 / 0 / +4 and three.js) |
| 11 | Talk: head tilt 8 deg, her right hand up, mouth open | **PASS, weak point 2** | `talk.png`, `crops/talk-hand-front-x2.png`, `crops/gamecam-talk-x3.png` |
| 12 | Card: right arm forward with the card, 2 deg lean | **PASS** | `card.png` (front, half-way, 3/4, side, three.js) |
| 13 | Greyscale lineup with Kit, Ricky, a Ghostie and the ATS, on grass and path, colour and grey, x3 and 1x | **PASS** | `lineup-{grass,path}{,-grey}-crop-{x3,1x}.png` |
| 14 | Skill steps before the model: ready, direction, joins, tool outputs, blockout at the game camera | **PASS** | `ready.md`, `direction.md`, `skill/`, `blockout/` |

## Weak points still visible (Fact unless marked)
1. **Facets at 2x.** The jaw and cheek outline, the 8-sided hands and the 10-sided bun show their corners in the
   close views (`crops/face-front-x2.png`, `crops/hands-front-x2.png`, `hero.png`). There is 38-60 triangles of room
   left; Kit and Ricky have the same limit.
2. **Talk arm vs the sketch.** The bones keep one length, and the forearm is long (it wraps the belly at rest). So in
   the talk pose the elbow sits low, inside the body side, and the arm reads as one straight tube from the side up to
   the hand, not the sketch's bent elbow (`talk.png` panel 1; sketch `dot-sheet.png` TALK). The hand lands exactly on
   the sketch point. Opinion: it reads as a wave; a bent elbow would need a shorter forearm and a new rest pose.
3. **Hands meet the sleeves.** The sketch shows a small gap between each sleeve end and the hand ball. I closed it
   (the sleeve end sinks into the hand) so no hand floats (`crops/hands-front-x2.png`). Deliberate change.
4. **Side and 3/4 decals.** The near pocket is stretched on the side of the pear in 3/4 (`turn-34.png`), because the
   decals are projected from the front (Ricky method).
5. **Small ink ticks.** A short ink tick where each upper sleeve enters the body, a double ink line along the near
   sleeve in 3/4 (`crops/shoulder-join-34-near-x2.png`, `crops/shoulder-join-front-L-x2.png`), and small hooks where
   the ear outline meets the head outline in 3/4 (`crops/hairline-ear-34-x2.png`).
6. **Hair colour under the light.** Row 23 renders as about (245, 224, 194) on the lit side, warmer than the flat
   sketch white (255, 248, 238), because of Kit's warm sun and hemi light (`turn-front.png`). The Ghosties' row 16 gets
   the same shift. Not a palette change.
7. **Smile at 1x is faint.** 5-7 px, 2 px under the eyes, mean luma 52-76 against skin 135. It is not dark, so it
   does not read as a moustache, but at 1x the face reads mainly as two eyes (`crops/gamecam-face-x3-grass.png`).
8. **Band ends.** Each band end shows as a small square tab on top of its cup with a little ink notch
   (`crops/cup-right-front-x2.png`). The sketch draws a tab there too.
9. **Talk in-between.** At half-way the raised arm passes in front of the chest, near the far cup (`talk.png`
   panel 2). It does not cut into the body; Emil should check the timing.

## Whole-picture check (2x, panel by panel)
- `turn-front.png`: symmetric; one ink hairline above the brows; buttons and placket centred; cups on the
  collarbones; jaw facets; shoulder ink ticks.
- `turn-34.png`: hairline runs behind the ear; stretched near pocket; double ink line on the near sleeve.
- `turn-side.png`: round ear; hairline from the forehead behind the ear to the nape; the band shows as a flat lilac
  strip over the shoulder (as the sketch side view); folded hands in front of the belly.
- `turn-back.png`: hair covers the back to the nape; band across the nape; no stray lines.
- `sway.png`, `talk.png`, `card.png`, `expressions.png`: as above; no part floats, no clipping seen.
- `lineup-*-crop-x3.png`: white dome and bun, peach face, two lilac discs, purple pear; Dot is the shortest figure.

## Fixes made during this build (each seen once, fixed once)
- Hair overhang drew a second thin ink line above the hairline (both renderers) -> hair thins to the skin, ink band
  carries the edge (`direction.md` §3).
- Thin hull lines across the back hair (quads split two ways) -> the body is triangulated in the build.
- Diamond-shaped ears in the side view -> ears built with their axis pointing out.
- A pale gap under each shoe -> shoes raised 2.5 units.
- Placket line broken by the body facets -> lifted to 1.2 units.
- Grass lineup spot under the tree -> moved to (-2.5, 5.6) (`ready.md` item 19).
