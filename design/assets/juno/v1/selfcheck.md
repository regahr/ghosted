# Juno the barista v1 self-check (Viet Tran, builder, 2026-11-26)

Rules: every claim names an image. A visible fault is never PASS. Rega is the gate; the chair checks at 2x first.
Paths are in `assets/juno/v1/`.

## Counts (Fact: `juno_build_report.json`; three.js `ingame_report.json` `visibleTris` gives the same totals)
| Beat | body | decals | eyes | brows | mouth | cup (+ line) | marker | Visible | Cap |
|---|---|---|---|---|---|---|---|---|---|
| rest / hand over / wave 1, 3 / handover (dry) | 978 | 170 | 40 | 12 | 8 | 178 | - | **1,386** | 1,400 |
| wave 2 (talk) / rest + talk | 978 | 170 | 40 | 12 | 18 | 178 | - | **1,396** | 1,400 |
| writing (eyes down) | 978 | 170 | 16 | 12 | 8 | 178 | 16 | **1,378** | 1,400 |
| rest + laugh | 978 | 170 | 16 | 12 | 24 | 178 | - | **1,378** | 1,400 |

- Body by part: head + cap + hairline ink 224, puff 64, scrunchie 48, ears 32, neck 16, hourglass with the tie band
  294, bow + tails 56, arms 78 + 78, legs + shoes 88. The cup is 50 triangles; its line is 128.
- Meshes: non-swap **2** (`body`, `decals`; both skinned). Swap parts: `eyes_open`, `eyes_happy`, `eyes_down`,
  `brows_rest`, `brows_dry`, `mouth_smile`, `mouth_laugh`, `mouth_talk`, `mouth_smirk`, `cup_rest`, `cup_hand`,
  `cup_wave`, `cup_write`, `marker`. 16 meshes in `juno.glb`; one cup is visible at a time.
- Body: 0 non-manifold edges, 0 faces against the analytic normals, 0 unweighted vertices; 98 open edges (buried ends:
  neck tube, body top ring, sleeve roots, leg ends, bow tails).
- Every hand reaches its pose target, 0.0 mm off (write right hand 0.11 mm).
- Blender vs three.js: mean difference 1.03 / 255 (3/4) and 1.09 / 255 (front); 0.53 % and 0.58 % of pixels differ by
  more than 40 (`compare-ingame.png`, `compare-ingame-front.png`).

## Requirements
| # | Requirement | Verdict | Proof |
|---|---|---|---|
| 1 | 1,400 visible triangles or fewer in every beat (chair call 2) | **PASS** (max 1,396, wave 2 / talk) | table above |
| 2 | Matches the sketch: direction A hourglass, puff, apron, cup; front / 3/4 / side / back agree; upright, symmetric at rest | **PASS with weak points 3, 4** | `turnaround.png`, `compare-sketch.png`, `crops/compare-*.png`, `hero.png` |
| 3 | Size 1.0 x Kit counting the puff, set in the blockout (chair call 1) | **PASS** (75 / 75 px = 1.000 on grass and path; H 1.10 m) | `measure.md` "Scale"; `blockout/blockout-sheet.png`; `blockout/ingame_report.json` |
| 4 | Palette rows 5, 6, 7, 25, 15, 26, 23, 22; row 7 accents only (chair call 3) | **PASS** | `juno_toon.json`, `build_juno.py` `PAL`, `grey.png`, `turnaround.png` |
| 5 | Cup: white with a lid; "You are not a PDF." hand-drawn ink polylines, no font; readable at card size; just a cup in game (chair call 4) | **PASS** | `cup-closeup.png`, `cup-card.png`, `cup-card-small.png`, `crops/close-cup.png`; `gamecam-beats-x3.png` |
| 6 | No skin sliver at the forehead edge in 3/4 (chair call 5) | **PASS** | `crops/forehead-34-x2.png`, `crops/forehead-34b-x2.png`, `crops/close-forehead-34.png`, `crops/close-forehead-34b.png` |
| 7 | Side-profile ticks: allowed known limit (chair call 5) | **known limit, present** (eye and smile tips at the profile) | `crops/face-side-x2.png`, `crops/close-face-side.png` |
| 8 | No fringe: forehead band >= 4 px at 1x; nothing down the temples beside the eyes (bible) | **PASS** (5-7 px every column, every expression; side hair 9-10 px above the eye top) | `measure.md`; `crops/gamecam-face-mask-*.png`, `gamecam-face-x3.png` |
| 9 | Rest mouth = closed smile line; laugh and talk = Ricky style (chair call 6, bible) | **PASS** at card size | `expressions.png`, `crops/close-face.png` |
| 10 | No beard read at 1x (chair call 6) | **PASS** (largest mouth 6 x 2 px, 3-5 px under the eyes); **weak point 1** for the smile's own read | `measure.md` "The mouth at 1x"; `gamecam-face-x3.png` |
| 11 | Hand over: her right arm forward, cup on the palm, other hand at her side, smile | **PASS** | `hand-over.png`, `crops/handover-cup-front-x2.png`, `crops/handover-cup-side-x2.png`, `crops/close-handover.png` |
| 12 | Small wave: her right hand up by the shoulder, 3 frames, cup in the left hand | **PASS, weak point 5** | `wave.png`, `crops/wave-hand-x2.png`, `crops/close-wave.png` |
| 13 | Writing: cup up at the chest in the left hand leaning back 10, marker in the right, head down 14, eyes down; then the hand over | **PASS** | `writing.png`, `crops/write-cup-marker-x2.png`, `crops/close-write.png` |
| 14 | Expressions: rest, laugh, talk, dry, writing | **PASS** | `expressions.png` |
| 15 | Lineups with Kit, Ricky, Dot, Brett, the ATS and Ghosties; grass and path; colour and grey; x3 and 1x | **PASS** | `lineup-{grass,path}{,-grey}-crop-{x3,1x}.png`, `lineup-*.png` |
| 16 | Silhouettes, grey, in-game render and compare | **PASS** | `silhouette-64*.png`, `grey.png`, `ingame*.png`, `compare-ingame*.png` |
| 17 | Skill steps before the model: ready, direction, joins, tool outputs, blockout at the game camera | **PASS** | `ready.md`, `direction.md`, `skill/`, `blockout/` |

## Weak points still visible (Fact unless marked)
1. **The rest smile does not resolve at 1x.** The smile and the dry smirk are 0-1 px at the game camera, so her face
   reads as brows and two eyes (`gamecam-face-x3.png`). Not a beard read, but close to the Ghostie's "no mouth" cue
   (Opinion). Tried twice (3.0 then 3.6 units, 1 px; 4.8 units, 2 px and too heavy at card size); stopped by the
   "no blind iterations" rule. Options for Rega:
   1. accept it (the sketch's own 1x estimate was sub-pixel too; laugh and talk do show);
   2. **my pick:** at the game camera use the talk mouth as her idle face (a small dark open mouth, 2-3 px at 1x, no
      beard read measured; it may still be too small to help), and keep the closed smile for the card and dialogue views; 0 triangles, a game-state choice;
   3. a slightly larger closed smile drawn lower on the chin (needs a sketch change).
2. **Shoulder seam.** Where the sleeve tube enters the body, the ink hull draws a short broken line at the armpit and
   shoulder top (`crops/close-shoulder.png`, `crops/shoulder-join-34-x2.png`). The sketch has a seam there; the broken
   ink is a 3D artefact. Same join as Brett and Dot.
3. **The puff is 8-sided** and reads a little smaller and flatter than the sketch's round ball in the front view
   (`crops/compare-front.png`, `crops/puff-front-x2.png`). More sides cost 16-32 triangles; the budget has 4 left.
4. **Changes from the sketch, on purpose:** the apron skirt's bottom edge is straight at the hem line (a curved edge
   left brown wedges at the corners on the faceted flare); the scrunchie is a full thin ring at the puff base, so a
   red line shows across the front of the puff, where the sketch shows only small red bits at the sides
   (`turnaround.png`, `crops/puff-front-x2.png`).
5. **Wave arm.** The bones keep one length (upper 36, forearm 58 units), so in the wave the forearm is longer than the
   sketch's wave panel and the arm reads straighter (`wave.png` vs `../sketch/juno-sheet.png` "A SMALL WAVE").
6. **Small ticks.** The far ear in 3/4 has a small hair notch at its back edge (`crops/ear-34-far-x2.png`); the skirt
   hem shows short ink ticks at the body's column corners (`crops/skirt-hem-34-x2.png`).
7. **At rest the red tie is hidden** by the hands and the cup at the game camera; it shows in the other beats
   (`gamecam-beats-x3.png`). This is the sketch's pose.

## Whole-picture check (2x, panel by panel)
- `turn-front.png`: symmetric; puff centred; apron, pocket, cup centred; scrunchie line across the puff base (weak 4).
- `turn-34.png`, `turn-34b.png`: hairline clean; no forehead sliver; far ear notch (weak 6).
- `turn-side.png`: eye and smile ticks at the profile (allowed, chair call 5); cup in front of the apron; bow at the back.
- `turn-back.png`: hair dome to the nape; bow and tails centred on the tie.
- `hand-over.png`, `wave.png`, `writing.png`: no part floats; the cup sits on the palm / in the left hand; the marker
  touches the cup front; the free arm hangs at her side.
- `expressions.png`: clean shapes; laugh and talk in Ricky style.
- `lineup-*-crop-x3.png`: clear of every other character.

## Fixes made during this build (each seen once, fixed once)
- Over budget (1,456 in talk) -> scrunchie 8 x 3, 4-sided bow knot, 8-point eyes (later back to 12), 3 skirt rows,
  no cup bottom, simpler glyphs. Final max 1,396.
- Scale 76 / 77 px after the rounder puff -> H 1.10 m.
- Brown wedges in the skirt apron -> straight bottom edge (the lift alone did not fix it; the cause was the curved
  edge, which a row grid cannot fill at the corners).
- The free arm in the hand over stood out like a handle -> hangs at her side.
- The scrunchie was inside the puff (not seen) -> on the puff's own section where it leaves the cap.
- Strap notches on the shoulder shelf -> straps lifted.
- Cup camera aimed while the root was still turned -> the root reset before the aim; a thin ink line for the card cup.
- Lineup spots touched Ricky, Dot and Brett -> moved.
