# Ghostie v6 self-check (Viet Tran, builder, 2026-11-25)

Rules: every claim names an image. A visible fault is never a PASS. Paths are in `assets/ghostie/v6/`.
"Fact" = measured or seen in the named image. "Opinion" = my read.

## Counts (Fact: `build_report.json`, `ingame_report.json` `visibleTris`)
| Variant | Body + arms | Eyes | Accessory | Total (three.js) | Cap |
|---|---|---|---|---|---|
| tie | 476 | 24 | 40 | **540** | 600; tie 68 |
| glasses | 476 | 24 | 98 | **598** | 600 |
| headset | 476 | 24 | 84 | **584** | 600 |
Non-swap meshes: 1 (`body`, skinned to body_root, arm_L, arm_R). Swap parts: eyes, acc_tie, acc_glasses, acc_headset.
Skin: 0 unweighted vertices. Mesh: 0 non-manifold edges, closed (the hem has a hidden cavity fan).

## Brief requirements
| # | Item | Verdict | Evidence |
|---|---|---|---|
| 1a | Body upright and symmetric in the mesh; 4° lean on the float node | PASS | Fact: the mesh is built mirror-symmetric (`build_ghostie.py`); the tilt is `float.rotation` (`build_report.json` `rest_pose`). `turn-front.png` is upright; `rest-front.png` shows the tilt. |
| 1b | Smooth dome, no visible corners at card size | **WEAK (not PASS)** | Fact: `crops/dome-front-x2.png`, `crops/dome-34-x2.png`: 8 rows, so each outline vertex turns about 11°. At 2x the polygon steps are visible on the ink line. Fact: `crops/overlay-sketch-front.png`: the dome lies on the sketch curve. Opinion: smoother needs about 6 more rows (+190 triangles), which 600 cannot hold. |
| 1c | 5 hem lobes, 3 from the front, notch centred at the back | PASS on count, **WEAK on shape** | Fact: `crops/hem-front-x2.png` (3 lobes), `crops/hem-back-x2.png` (centre notch). The lobes are 40-segment polylines with visible straight runs, and the back corners are square. Fact: `crops/overlay-sketch-front.png`: the 3D hem sits about 7 units lower than the sketch hem. This is the card camera looking down on the front of the hem ring. |
| 2a | Arms one skinned mesh with the body | PASS | Fact: one `body` mesh; the arm tubes start on the body's own edge loop (no boolean). |
| 2b | Soft shoulders: no corner, crease, pale wedge or hem hook | **FAIL** | Rest, front: clean (`crops/arm-root-front.png`), but the outline shows polygon steps. Fact, visible faults: a small ink hook under the near arm in 3/4 (`crops/near-arm-34.png`); a thin crease line at the far-arm root in 3/4 (`crops/far-arm-nub-34.png`); a darker shade wedge under each arm (`crops/arm-rest-droop.png`, `crops/arm-root-front-R.png`); in the side view the end-on arm draws a small "v" line that can read as a smile (`crops/arm-end-on-side.png`). |
| 2c | Arm shape and height as in the sketch | PASS (front) | Fact: `crops/overlay-sketch-front.png`: the arm outline sits on the sketch line; tip at front-view (284.9, 241.4) vs sketch about (290, 237). |
| 2d | Tips below the eye dots at the game camera, rest and wave 0..+40° | **FAIL (1 of 3 ghosts)** | Fact: `measure.md`: arm_L passes in every row (margin ≥0.4 px). arm_R misses on the headset ghost by 1.8-1.9 px (tip at the eye centre). See open item 2. |
| 2e | 3/4 shows the far-arm nub | PASS, with the crease above | Fact: `turn-34.png`, `crops/far-arm-nub-34.png`. |
| 2f | Wave reads clean | **FAIL** | Fact: `crops/arm-wave-blender.png`, `wave-40-front.png`: a short ink spur and a hard corner where the raised arm meets the shoulder; a thin shade streak under the raised arm. I tried 3 pivot and weight set-ups (`tests/body4`, `tests/body5`, `tests/waveA`, `tests/waveB`), so I stopped. See open item 1. |
| 3 | Eyes on the body-map eye line y 118 | PASS | Fact: `crops/overlay-sketch-front.png`: the blue sketch eye centres fall in the 3D eye dots. |
| 4a | Collar wings flat, inside the silhouette, joined to the knot | PASS | Fact: `crops/tie-on-surface.png`, `front-tie.png`. |
| 4b | Tie centred, hangs from the collar, ink all round | PASS | Fact: `crops/tie-on-surface.png`, `crops/tie-side-profile.png` (it lies on the surface). |
| 4c | Tie ≤ 68 triangles | PASS | Fact: 40 (`build_report.json`). |
| 5 | Glasses: round rims on the eye line, ink edge readable at 1x | PASS, minor | Fact: `crops/glasses-on-surface-front.png` (12-sided rims: a lilac inner band and an ink outer band); `crops/gamecam-glasses-x9.png` and `lineup-grass-crop-1x.png`: the rims read as two dark rings. Opinion: the 12 sides show as facets at close range. |
| 6a | Headset band over the crown, on the dome outline, with ink, never a forehead stripe | PASS at card, **WEAK at the game camera** | Fact: `crops/headset-band-front.png` (on the outline, ink outside it), `crops/headset-band-over-crown.png`. Fact: `crops/gamecam-headset-x9.png`: the band is a faint lilac arc, with ink only on its far edge. |
| 6b | One cup on each ear point, level, same size, with ink | PASS on place, **WEAK on look** | Fact: the cups are mirror copies (`acc_headset['cups_level_z_m']`). Face-on, the cup shows an ink pad (`crops/headset-cup-on-surface.png`), because a hull cannot draw ink round a part that sits on the body. Opinion: the 8-sided pad reads as a dark octagon close up. |
| 6c | Headset ≤ 600 total, 8-sided cups, no back, thin band, no ink-ring geometry | PASS | Fact: 584; the band and cup ink come from the headset hull and the ink pad (0 extra triangles). |
| 7 | Palette rows 16, 27, 10, 22 only; neutral shade | PASS | Fact: `PAL` in `build_ghostie.py`; shade band grey 178 (`ghost_toon.json`); `grey.png`, `lineup-grass-grey-crop-x3.png`. |
| S1 | Matches the accepted sketch | **Partly** | Fact: `compare-sketch.png`, `crops/overlay-sketch-front.png`, `crops/overlay-sketch-wave.png`. The front outline, eyes, tie and accessories match. The differences: the hem looks lower and flatter; the wave arm is squarer, with a corner at the shoulder; the side view shows no closed arm oval; the sketch's lilac glasses are now ink rims (B item 5); the headset cups are thin edge-on blocks, not ovals. |
| V6 | In-game matches Blender | PASS | Fact: `compare-ingame.png`, `compare-ingame-front.png`: mean diff 0.73/255, 0.28-0.29 % of pixels over 40. |

## Open items for the chair (no 3rd method tried, by the rule)
1. **The wave shoulder** (2f). LBS on a 70-unit-tall arm root at 40° leaves a corner and a spur. The next method would be a
   wave morph target (a sculpted pose shape, 0 triangles). That is a 3rd method, so the chair decides.
2. **arm_R tip on the headset ghost** (2d). It misses because that ghost turns 34° to the camera. Options: a stronger
   rest pose (arm_R swung forward, Emil's call); accept it for turned ghosts; or a lower arm on the sketch.
3. **Outline smoothness at 600** (1b, 1c, 2b). The dome, hem and arm outlines show polygon steps at 2x. This is a
   budget limit, not a modelling fault I can remove inside 600.

## Whole-picture check (every panel at 2x)
- `turn-front.png`: dome and hem polygon steps; shade wedge under each arm.
- `turn-34.png`: crease at the far-arm root; ink hook under the near arm; a small spike at the lower-left hem corner.
- `turn-side.png`: the end-on arm draws a small "v" (can read as a smile); the eye shows as a thin sliver at the front edge (as the sketch).
- `turn-back.png`: square bottom corners; small back lobes.
- `front-variants.png`, `variants.png`: no extra fault beyond the above.
- `hero.png`: reads clean at that size.
- `_close-headset.png`: a dark octagon pad; the end-on arm pocket line.
- `wave-40-front.png`, `_close-wave.png`: shoulder corner and spur.
- `lineup-*-crop-x3.png`, `lineup-*-crop-1x.png`: the tie reads as a tongue (accepted); the glasses read; the headset band is faint.
