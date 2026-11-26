# Ghostie v7 self-check (Viet Tran, builder, 2026-11-25)

Rules: every claim names an image. A visible fault is never a PASS. Rega is the only gate, so this check is strict.
Paths are in `assets/ghostie/v7/`. v6 is unchanged in `../v6/`.

## Counts (Fact: `build_report.json`; three.js `ingame_report.json` `visibleTris`)
| Variant | Body + arms | Eyes | Accessory | Total | Cap |
|---|---|---|---|---|---|
| tie | 652 | 24 | 40 | **716** | 800 |
| glasses | 652 | 24 | 98 | **774** | 800 |
| headset | 652 | 24 | 112 | **788** | 800 |

- Non-swap meshes: 1 (`body`, skinned to body_root, arm_L, arm_R, plus 1 morph target `wave` that moves 45 vertices).
- Skin: 0 unweighted vertices. Mesh: 0 non-manifold edges.
- Blender vs three.js: mean difference 0.73/255; 0.28-0.29 % of pixels differ by more than 40 (`compare-ingame.png`, `compare-ingame-front.png`).

## The 4 changes
| # | Change | Verdict | Evidence |
|---|---|---|---|
| 1a | Dome: 11 rows (v6: 8), so each outline vertex turns about 8° (v6: 11°) | **Better, still WEAK** | Fact: `crops/v6-v7-dome-front-x2.png`, `crops/v6-v7-dome-34-x2.png`. The steps are smaller but still visible at 2x, mostly where the dome meets the side (rows y 106 and 134). |
| 1b | Hem: 5 scallops, round tops and round notches, no zigzag (52 vertices; v6: 40) | **Front PASS; back WEAK** | Fact: `crops/v6-v7-hem-front-x2.png`: round notches and round lobes, faint segment steps at 2x. Fact: `crops/v6-v7-hem-back-x2.png`, `compare-sketch.png` (back): the 2 narrow back lobes are shallow, so the back hem reads almost flat. The sketch shows 4 deep back scallops. |
| 1c | Shoulder and arm contour: + shoulder row y 165, 4 arm rings (v6: 3) | PASS front, WEAK 3/4 | Fact: `crops/arm-root-front.png`, `crops/overlay-sketch-front.png`. 3/4: see item 4. |
| 2 | Wave = morph target to the sheet WAVE outline (0 triangles) | **Front PASS; close 3/4 WEAK** | Fact: `wave-40-front.png`, `wave-20-front.png`, `crops/overlay-sketch-wave.png`: the outline follows FRONT_WAVE, and the front view has no shoulder corner and no spur. Fact: `_ingame-wave.png` (three.js) matches `_close-wave.png` (Blender); the hull follows the morph. Fact, still visible: in the -40° close view (`_close-wave.png`, `crops/arm-wave-blender.png`) the arm reaches toward the camera and leaves a small notch at the top of the shoulder. Second attempt on this item, so I stop here. |
| 3 | arm_R rest: 14° droop + 45° forward swing | **PASS on the measure; a look note** | Fact: `measure.md`: arm_R on the headset ghost went from -1.9 px (v6) to +4.5 px, and every tip on every ghost and wave angle is now 2.9 px or more below the eye bottom. Opinion: in `rest-front.png` and `rest-34.png` the swung arm reads short. In 3/4 it makes a small "handle" loop in front of the body. The sheet REST POSE shows a longer arm that hangs out to the side. Emil should look at it. |
| 4a | 3/4 near-arm hook, far-arm crease | **Not fixed** | Fact: `crops/near-arm-34.png`, `crops/far-arm-nub-34.png`: both are still there, but smaller. |
| 4b | Side-view "v" | **Not fixed** | Fact: `crops/arm-end-on-side.png`, `turn-side.png`. |
| 4c | Rounder cups, no octagon pad | PASS | Fact: `crops/headset-cup-on-surface.png`, `_close-headset.png`: a 10-sided lilac pad with a round ink disc under it. There is no dark pad any more. Opinion: the ink ring is broken into arcs at the top-left and bottom-right of the cup. |

## Kept from v6 (re-checked)
- Eyes on y 118: PASS (`crops/overlay-sketch-front.png`).
- Tie, collar and 40 triangles: PASS (`crops/tie-on-surface.png`).
- Glasses with an ink edge at 1x: PASS (`crops/gamecam-glasses-x9.png`).
- Headset band on the crown outline with ink: PASS at card (`crops/headset-band-front.png`). Still faint at the game camera (`crops/gamecam-headset-x9.png`).
- Palette and neutral shade: PASS (`grey.png`).
- Upright symmetric mesh, with the tilt on the float node: PASS (`turn-front.png`, `rest-front.png`).

## S1 (matches the accepted sketch): `compare-sketch.png`
- **Matches:** front, 3/4, tie, glasses placement, and the wave (now close to the sheet).
- **Differs:**
  - The back hem is near flat.
  - The headset cups are thin blocks when seen edge-on (the sheet draws ovals).
  - The rest-pose arm_R is short, because of the forward swing (change 3).
  - The side view has no closed arm oval, and has the small "v" instead.

## Whole-picture check (2x, panel by panel)
- `turn-front.png`: small dome and side steps; shade wedge under each arm.
- `turn-34.png`: crease at the far-arm root; small hook under the near arm; a spike at the lower-left hem corner.
- `turn-side.png`: the "v"; a thin eye sliver at the front edge (as in the sketch).
- `turn-back.png`: flat back hem; square bottom corners.
- `rest-front.png`, `rest-34.png`: short swung arm_R; a handle loop in 3/4.
- `wave-40-front.png`: clean. `_close-wave.png`: small shoulder notch.
- `_close-headset.png`: broken ink ring round the cup; the end-on arm pocket line.
- `lineup-*-crop-x3.png`: tongue-tie (accepted), glasses read, headset band faint.
