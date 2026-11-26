# Gary v1: measures (Viet Tran, 2026-11-26)

Set-up (= Panel v1): three.js, 26 m, pitch 42, yaw 20, fov 26, 1600x900, 1.6 px ink hull. Gary is turned 15 deg like
the cast. Spots (cheap to change): grass, 0.62 m right of Kit; path, 0.95 m in front of Kit; the flyer 0.9 m up.
Sources: `ingame_report.json` (from `shoot.mjs`), `measure.json` (from `make_sheets.py`), `gary_build_report.json`.
Masks (`_mask-*.png`): cap and brim red, eye ink blue, brows orange, gold green, body white, hull black.

## Scale
| Item | Value | Source |
|---|---|---|
| Unit | 1 u = 2.2929 mm (= sketch `build.py` M_PER_U) | `build_gary.py` U |
| Standing height to the cap top | 209 u = 0.479 m (0.49 x Kit 0.977 m); the sketch 0.488 m includes the ink line | `measure.json` world |
| On screen, standing | 35 x 25 px on grass, 36 x 26 px on the path; Kit 75 px. Ratio 0.47 / 0.48 | `measure.json` grass, path |
| Sketch on screen | 35 x 26 px (`sketch/body-map.md` Camera check) | |

- **Fact:** Gary is 35-36 px tall next to Kit's 75 px, the same as the sketch.

## Wingspan
| Item | Value | Source |
|---|---|---|
| World, wings level | 1.032 m = 1.056 x Kit (chair call 2: keep 1.06) | `measure.json` world.span_bind_m |
| On screen, flap level, flying 0.9 m up | 80 px wide (sketch: 81 px) | `measure.json` fly_level |

## Cap against the eyes (rule: the cap never covers the eyes)
Lowest red (cap or brim) pixel above the top blue (eye) pixel, in the eye columns, at 1x. Left eye / right eye.

| Render | Clear (px) |
|---|---|
| grass rest | 4 / 4 |
| path rest | 3 / 4 |
| grass hold | 4 / 4 |
| grass sorry (head tilt) | 4 / 5 |
| grass land hop | 3 / 4 |

- **Fact:** 3 px or more in every render (the sketch: 2.4-2.9 px). Proof: `crops/face-mask-mask-*.png`,
  `gamecam-face-x6.png` (mask row).

## Eye size at 1x
| Item | Value | Source |
|---|---|---|
| Model | eye ovals 7.5 x 9.8 u (sketch 6.5 x 8.5 u, + 15 %, chair call 3) | `build_gary.py` ER |
| Geometric height on screen (eye centre to eye top, x2) | 2.6 px grass, 2.8 px path (sketch 2.35 px) | `ingame_report.json` eye_l, eye_top |
| Pure eye-ink pixels in the mask | each eye 1-2 px tall, 2 px wide, 2-4 px | `measure.json` face.eyes |
| Beak | 1-3 x 4 px, gold, under the eyes | `measure.json` face.beak_wxh_px |

- **Fact:** the eyes grew 15 % and are 2.6-2.8 px tall by geometry. Anti-aliasing with the face and the brows leaves
  1-2 px of pure eye ink.
- **Opinion:** at 1x the eyes read as two dark dots beside the beak, but only just. See `selfcheck.md` weak point 1.

## Triangles (visible, per beat; budget 900)
rest 832, flap up / level / down 850, land hop 850, hold 860, sorry 886 (max), happy hop 808, fly off 832.
Non-swap meshes: body 572, wing_R 100, wing_L 100 (3 meshes). Swaps: eyes 12-62, brows 12, envelope 18, flap 12-22.
Source: `gary_build_report.json`; three.js count at rest = 832 (`ingame_report.json` lineup-grass.garyTris).
