# Ghostie v5: changes (builder: Viet Tran seat)

- Date: 2026-11-25.
- Source: `acceptance/ghostie/fix-brief-v5.md`, including the section "Tie change for v5".
- v4 is archived in `v4/` and was not touched. Every deliverable is re-shot from the final v5 build.

## Rebuild (local)

1. `Blender -b --factory-startup -P build_ghostie.py`
2. `Blender -b ghostie.blend -P render_ghostie.py`
3. `node shoot_ingame.mjs`
4. `python3 make_sheets.py`

**Tiny skinned test first:** the script is `scratchpad/skintest/t.py`. It ran a sphere plus a cylinder through an exact boolean union, an armature with envelope weights, a Solidify and a glTF export with skins. It produced 196 triangles and the groups body_root and arm_L, with no crash. No Blender run crashed in v5; the newest `Blender-*.ips` is still the Kit one from 16:01.

## Triangles and meshes (three.js `ingame_report.json` `visibleTris`; budget 600)

| Variant | Triangles | Non-swap meshes | Swap meshes |
|---|---|---|---|
| tie | 571 | **1**: body (body + both arms, skinned to body_root / arm_L / arm_R) | eyes, acc_tie |
| glasses | 568 | 1 | eyes, acc_glasses |
| headset | 596 | 1 | eyes, acc_headset (with child band) |

- Split (`build_report.json`): body+arms 508, eyes 24, tie 39, glasses 36, headset 64.
- The union adds about 40 triangles at the join. To fit the headset, its band now uses every 2nd ring as a station (2.4-3.2 mm off the surface) and its cup has 10 sides.

## Changes

| # | Change | Proof |
|---|---|---|
| 1 One mesh + skin | - The v4 arm flaps (shape, tips, rest pose baked in) are unioned into the body with Blender's exact boolean, so body and arms share vertices along the join and one ink hull wraps both.<br>- Skinned with Blender's envelope parenting (an operator; no weights written by hand): body_root (head z 0, tail at the crown, r 0.16 + 0.08), arm_L and arm_R (pivot on the body surface → rest tip, r 0.04 + 0.04).<br>- `build_report.json`: 0 unweighted vertices; the arm tips have arm-bone weight 1.0.<br>- three.js: the outline hull is a `SkinnedMesh` bound to the same skeleton (`ingame.html` `hullFor`).<br>- The wave rotates the arm_L bone in both Blender (`render_ghostie.py` `wave`) and three.js (`pose()`), about the same signed float-space axis stored in `float.extras.wave_axis_float_blender`. | `variants.png`, `hero.png`, `turn-side.png`, `crops/arm-root-front.png`, `crops/arm-end-on-side.png`, `_close-wave.png` / `crops/arm-wave-blender.png`, `_ingame-wave.png` / `crops/arm-wave-threejs.png` |
| 1b Arm shape and gap | Unchanged from v4. The eye-vs-arm-tip table re-measured the same values (`selfcheck.md`). | `lineup-grass-crop-x3.png`, `lineup-path-crop-x3.png` |
| Tie (chair's v5 section) | - **Knot:** a raised trapezoid 36 → 26 mm, about 1.5x the 24 mm blade root, standing 10 mm proud against the blade's 6 mm (the step). It sits at +40°, z 0.228, below the eye line (eye bottom 0.278), off-centre.<br>- **Blade:** 24 → 34 mm wide over about 0.12 m (about 1/4 width/length) with one S-bend. It runs round the side of the left shoulder at z 0.23-0.25 and leaves the body at the SIDE, not the crown.<br>- **Tip:** a symmetric V in the air, 56 mm off the body (`build_report.json`). Its face turns to the front.<br>- **Ink:** a backing 4.5 mm wider than the tie on every side (knot, long sides, V) gives one closed stroke. It lies under the tie on the body and behind it in the air.<br>- Tie edges are now built in the tangent plane with a radial normal. The first v5 run showed zigzag edges at the column ridges. | `variants.png`, `hero.png`, `turn-front.png`, `turn-side.png`, `crops/tie-vs-kit.png` |
| Headset | Band thinned to every 2nd ring (budget); one ink ring on the cup top edge (v4). | `variants.png`, `crops/headset-cup-on-surface.png` |

Unchanged: body profile, crown, colours, neutral shade band, 1.6 px outline, float lean and roll.
