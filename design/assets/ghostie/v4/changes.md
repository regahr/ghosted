# Ghostie v4: changes (builder: Viet Tran seat)

- Date: 2026-11-25.
- Source: `acceptance/ghostie/fix-brief-v4.md`. Only the arms, the eyes, the tie and the cup ink changed.
- Archives: v1, v2 and v3 are in `v1/`, `v2/` and `v3/`.
- Every deliverable is re-shot from the final v4 build.
- Rule: every claim names a file.

## Rebuild (local)

1. `Blender -b --factory-startup -P build_ghostie.py` (this was the tiny test, then the full run)
2. `Blender -b ghostie.blend -P render_ghostie.py`
3. `node shoot_ingame.mjs`
4. `python3 make_sheets.py`

There was no Blender crash; the newest `Blender-*.ips` is still the Kit one from 16:01.

## Triangles and meshes (three.js `ingame_report.json` `visibleTris`; budget 600)

| Variant | Triangles | Non-swap meshes | Swap meshes |
|---|---|---|---|
| tie | 578 | 3: body, arm_L, arm_R | eyes, acc_tie |
| glasses | 528 | 3 | eyes, acc_glasses |
| headset | 580 | 3 | eyes, acc_headset (with child acc_headset_band) |

- Split (`build_report.json`): body 360, eyes 24, arm_L 54, arm_R 54, tie 86, glasses 36, headset 88.
- The body lost 24 triangles: the hidden cavity rim ring is now one fan from the hem to the cavity pole. Those triangles went to the arm tips (+12 each).

## Changes

| # | Change | Proof |
|---|---|---|
| 1 Arms below the eyes at 26 m | - Eyes raised from z 0.258 to 0.305 (+0.047 m = 10% of body height). They stay on the flat face at ±15°, and the glasses stay clean (visible faces 0.49-1.5 mm off the surface, `build_report.json`).<br>- Arms rooted 10° forward of the side (±80°), at z 0.095.<br>- Curved spine: 24° droop at the root, bending to 76° at the tip. Tip z 0.045.<br>- No back sweep.<br>- Measured on screen: see `selfcheck.md`. | `lineup-grass-crop-x3.png`, `lineup-path-crop-x3.png`, `ingame_report.json` `eyeVsArm` |
| 2 Round arm tip | 5 rings closing into a pole, half-widths 26 → 29 → 25 → 15 mm → tip. | `hero.png`, `variants.png` |
| 3 Arm join seams | - The v3 back sweep made the flap run along the body, which drew the spur. The flap now leaves along the surface normal.<br>- **Result: not fully fixed.** See `selfcheck.md`. | `variants.png`, `crops/arm-root-front.png`, `turn-side.png`, `turn-back.png` |
| 4 Tie | The right way round now.<br>- A knot block (34 x 34 mm, 11.5 mm proud) sits low on the front at +44°, z 0.170, below the eye line (eye bottom 0.278).<br>- The blade widens from 12 to 53 mm as it climbs over the left shoulder.<br>- Past the shoulder it lifts off the body: 2 flying stations and a wide pointed tip 71 mm off the body. Its face turns to the front so the point reads.<br>- Ink: the side walls along both long sides are ink, and an ink plate 1.6 mm wider lies under the on-body part. | `variants.png`, `hero.png`, `crops/tie-vs-kit.png`, both lineup x3 crops |
| 5 Cup ink | One stroke: an ink annulus on the cup's flat top edge. The cup has no inverted hull any more, so there is no second stroke and no sliver. | `crops/headset-cup-on-surface.png`, `variants.png` |
| 6 If cheap | Hem notch apex: the scallop is now a plain cosine; the 5 top vertices sit at 75/93/100/93/75% of the depth (v3: 63/89/100/89/63). | `crops/hem-notch-34.png` |

## Unchanged (passed in v3)

- Body profile, crown and the 12 columns. The skirt, the 5 scallops and the colours are unchanged too.
- Neutral 178 shade band.
- 1.6 px outline.
- Pose: lean 3°, roll +5° on three.js z, uneven arms.
- Mesh count.
- Blender vs three.js compare: mean 0.75/255 (`compare-ingame.png`).
