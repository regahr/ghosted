# Ghostie v3: changes (builder: Viet Tran seat)

- Date: 2026-11-25.
- Source: `acceptance/ghostie/fix-brief-v3.md` (budget 600; at most 3 non-swap meshes).
- Archives: v1 in `v1/`, v2 in `v2/`.
- Every top-level PNG and every file in `crops/` was re-shot from the final v3 build. The half-done files from before the 18:01 stop were deleted first.
- Rule: every claim names the file that shows it.

## Rebuild (all local)

1. `Blender -b --factory-startup -P build_ghostie.py`
2. `Blender -b ghostie.blend -P render_ghostie.py`
3. `node shoot_ingame.mjs`
4. `python3 make_sheets.py`

Blender: the tiny test ran first (build plus a single `turn-front` render), then the full runs. There was no crash; the newest `Blender-*.ips` is still the Kit one from 16:01.

## Triangles and meshes per variant

Triangles are measured in three.js (`ingame_report.json` `visibleTris`). The budget is 600.

| Variant | Triangles | Non-swap meshes | Swap meshes |
|---|---|---|---|
| tie | 580 | 3: body, arm_L, arm_R | eyes, acc_tie |
| glasses | 528 | 3 | eyes, acc_glasses |
| headset | 580 | 3 | eyes, acc_headset + its child acc_headset_band |

- Split (`build_report.json`): body 384, eyes 24, arm_L 42, arm_R 42, tie 88, glasses 36, headset 88 (cup 34 + ink ring 24 + band 30).
- glTF meshes: acc_glasses, acc_headset_band, acc_headset, acc_tie, arm_L, arm_R, body, eyes.
- `arm_collars` is gone: the arm needs no collar now.

## The fixes

| # | Change | Proof |
|---|---|---|
| 1 Arms | Flat flaps, 6-sided: 18 mm thin front-to-back, 52-60 mm wide, tapering to a round tip.<br>- Root at z 0.100 (v2: 0.160); highest point z 0.143 / 0.150, below the eye dots (bottom at 0.231).<br>- 30° droop in the geometry. Rest pose: arm_L +6° (net 24°), arm_R -3° and forward 8° (net 33°).<br>- arm_L, the near arm in 3/4, points 35° back, so it lies square to the 3/4 camera and breaks that silhouette. arm_R points 15° back.<br>- No collar. The flap's faces meet the body directly.<br>- Root ring inside the body at rest and at ±20° (`build_report.json`). | `silhouette-64-34-x4.png`, `crops/arm-root-front.png`, `crops/arm-end-on-side.png`, `turn-back.png`, `hero.png`, `lineup-grass-crop-x3.png` |
| 2 Tie | Flipped over the **left** shoulder (+X), the side that both the 3/4 card and the 26 m camera see.<br>- The knot sits off-centre at +36°, outside the left eye at +15°.<br>- The blade climbs to z 0.337 at 90°, where it crosses the side outline (`turn-front.png`), and ends on the back (`turn-back.png`, `turn-side.png`).<br>- Ink plate on the long sides and the tip only; no ink at the top of the knot.<br>- Palette #10 `#C9A6D6`. Stations sit on the column ridges, so no chord cuts in (visible faces 0.05-9.8 mm off the surface). | `lineup-grass-crop-x3.png`, `lineup-path-crop-x3.png`, `variants.png`, `crops/tie-on-surface.png` |
| 3 Crown and shoulders | 12 columns (a lathe's side outline is always a vertex column, so columns add no outline corners). The dome has 8 rings: 10° steps, with the flattest step (80°) dropped. | `hero.png`, `variants.png`, `silhouette-64-x4.png` |
| 4 Hem | - 5 scallops x 12 vertices. Each notch top is a 5-vertex curve: 63/89/100/89/63% of its depth (`build_report.json`).<br>- 2 front notches at ±36°.<br>- The lower skirt ring bows out (r 0.213) and the hem tucks back to 0.199/0.193, so the bottom corners curl in.<br>- The v2 doubled sliver at the left hem is gone in `hero.png`. | `crops/hem-notch-34.png`, `hero.png`, `silhouette-64-x4.png`, `turn-front.png` |
| 5 Frames | - Glasses: 8-sided frames on the flat eye faces (`crops/glasses-on-surface-front.png`).<br>- Ear cup: 12-sided, with a flat top. In the first v3 run, a fan over the curved patch sagged 11 mm into the body.<br>- An ink ring at the cup base closes the ink where the cup's hull hides inside the body.<br>- The band is its own child node with no hull. Its hull had drawn a second crown line with a light gap (`crops/headset-band-over-crown.png`). | `variants.png`, `crops/headset-cup-on-surface.png` |
| 6 Eyes turned in | **Done.** The eyes moved from 25.7° to 15°, the centre of the flat face between columns. The dot and its 8-sided frame lie on one flat face, and the glasses stay clean (eye-to-frame gap 3.9 mm). | `crops/eye-far-34.png`, `crops/glasses-on-surface-front.png` |

## Kept from v2 (Lena and Emil passed)

- **Shade band:** neutral 178. `lineup-grass.png` samples: lit `#F3E2C3`, hue 38.8; shade `#E7D3B3`, hue 36.9.
- **Outline:** 1.6 px (`outlineW_m` 0.0213).
- **Palette colours:** unchanged.
- **Lean:** 3°.
- **Uneven arms:** kept.
- **Float roll:** flipped. The `float` quaternion z is now +0.0436, which is +5° on three.js z (v2: -5°). The arm_L side goes up.
- **Blender vs three.js compare:** mean 0.76/255, 0.29% of pixels over 40 (`compare-ingame.png`, `compare_report.json`).
