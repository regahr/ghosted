# Ghostie v2: changes (builder: Viet Tran seat)

- Date: 2026-11-25. Source: `acceptance/ghostie/fix-brief-v2.md` (gate v1 failed, 5 of 5 seats).
- v1 (renders, scripts, glb, notes) is archived in `v1/`.
- Rule: every claim names the file that shows it. The seats judge from the renders.

## How to rebuild (all local)

1. `Blender -b --factory-startup -P build_ghostie.py` writes `ghostie.blend`, `ghostie.glb`, `build_report.json` and `ghost_toon.json`.
2. `Blender -b ghostie.blend -P render_ghostie.py` writes the turnaround, hero, `_var-*`, `_close-*`, the 2 silhouettes, `grey.png` and `crop_points.json`.
3. `node shoot_ingame.mjs` (three.js r170 with swiftshader) writes `ingame*.png`, `lineup-*.png` and `ingame_report.json`.
4. `python3 make_sheets.py` writes `variants.png`, `compare-ingame*.png`, `lineup-*-grey*.png`, the `-crop-x3` images and `crops/*.png`.

There was no Blender crash in v2. The newest `Blender-*.ips` is still the Kit one from 16:01.

## Triangles (budget 450, checklist amendment 2)

Measured in three.js (Fact: `ingame_report.json` `visibleTris`):
- tie: 430
- glasses: 426
- headset: 442

Blender gives the same split (`build_report.json`):

| Part | Triangles |
|---|---|
| body | 294 |
| eyes | 24 |
| arm collars | 32 |
| arm_L | 24 |
| arm_R | 24 |
| tie | 32 |
| glasses | 28 |
| headset | 44 |

## The 8 fixes

| # | What changed | Proof |
|---|---|---|
| 1 Round outline | A lathe's side outline is its profile, so the triangles went into profile rings:<br>- crown: a 14-gon fan (v1: 8)<br>- dome: 5 rings plus the shoulder, turning 15° each (v1: 22-34°)<br>- skirt: 2 rings that bow into the flare (v1: 1)<br>Columns went from 16 to 14 (cos 12.9° gives a 2.5% outline wobble). Eyes now have 12 sides. | `hero.png`, `variants.png`, `silhouette-64-x4.png`, `crops/eye-far-34.png` |
| 2 Arms | Round mittens that leave the body square-on and point 20° back, so no default view sees them end-on. They are 8-sided, widest 44 mm out, with the tip at 68 mm.<br>A hull cannot draw the root line (there the hull is inside the body), so the root ink is geometry: a 6 mm ink collar on the body around the rest-pose join, 1.2 mm off the surface (`build_report.json`: collar 0.34-1.2 mm off the surface, base ring inside the body at rest and at ±20°). | `silhouette-64-34-x4.png`, `turn-side.png`, `crops/arm-end-on-side.png`, `crops/arm-root-front.png`, `crops/arm-root-back.png` |
| 3 Hem | 28 hem vertices (7 per scallop). The height is ((1 - cos 4θ) / 2)^1.4 x 34 mm, which is flat at the lobe and round, with zero slope, at the notch. The front shows 2 notches. | `crops/hem-notch-34.png`, `silhouette-64-x4.png`, `turn-front.png` |
| 4 Headset | The band lies 0.6 mm above the surface (v1: 3.4 mm) on the 90° face midlines. A lathe quad is flat, so no chord cuts in. The band covers only the inner 0.6 mm of the 7 mm crown ink. The ear cup is 8-sided, r 46 mm (v1: 6-sided, r 34 mm), and carries the ink hull. | `variants.png`, `crops/headset-band-over-crown.png`, `crops/headset-cup-on-surface.png`, `lineup-grass-crop-x3.png` |
| 5 Tie | Moved down to the chest: knot top at z 0.141 m, below the arm root at 0.160 (`build_report.json`). It is longer (0.12 m) so that it reads vertical.<br>Colour: Lena #10 hq-wall `#C9A6D6`, one step darker than #27, which echoes Recruiter HQ.<br>Ink edge: a mitred ink plate 2.5 mm wider than the tie, at 1.6 mm. A hull cannot outline a part this thin. | `crops/tie-on-surface.png`, `crops/tie-side-profile.png`, `variants.png`, `lineup-grass-crop-x3.png`, `lineup-path-crop-x3.png` |
| 6 Neutral shade | The ghost band is now (178, 178, 178) in `build_ghostie.py` and `ghost_toon.json`.<br>Pixel samples in `lineup-grass.png`: lit `#F3E2C3`, hue 38.8; shade `#E7D4B4`, hue 37.6, a 1.2° difference.<br>Samples in `hero.png`: `#F4E5C9` / `#F3E2C5`, hue 38-39.<br>Outline 1.6 px (`ingame_report.json` `outlineW_m` 0.0213 at the 26 m camera). | `lineup-grass.png`, `hero.png` |
| 7 Rest pose | Node rotations only:<br>- `float`: lean 3° toward the viewer (x), roll 5° (y in Blender, z in three.js)<br>- `arm_L`: up 13°<br>- `arm_R`: down 9° and forward 8° (`build_report.json` `rest_pose`)<br>In `ingame.html`, `pose()` now composes the yaw on top of the rest quaternion, so the tilt survives the float. | `hero.png`, `turn-front.png` |
| 8 Eyes turned in | **Not done.** The eyes sit on vertex column ±1 (now 25.7°) so that the glasses stay clean. Turning them in by 4-5° puts the frames across a column ridge (the v1 cut-through). | `crops/eye-far-34.png` |

## Other v2 changes

- The glasses are flat print 1.5 mm off the surface, with no walls. This saved 24 triangles for the arm collars. Their visible faces are 1.1-1.5 mm off the surface (`build_report.json`).
- The headset variant is rendered at -60° so that the ear cup faces the camera (`variants.png`).
- The compare test still matches: mean 0.75/255, with 0.29% of pixels over 40 (`compare_report.json`, `compare-ingame.png`).
