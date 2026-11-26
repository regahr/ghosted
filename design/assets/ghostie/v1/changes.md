# Ghostie v1: build notes and changes (builder: Viet Tran seat)

- Date: 2026-11-25. Card 2 of the design acceptance flow (Rega "go", Slack C0CHA2A1DM1, ts 1795599417.458319).
- Rule (a lesson from Kit): every claim below names the file that shows it. The seats judge from the renders, not from this file.

## How to rebuild (all local)

1. `Blender -b --factory-startup -P build_ghostie.py` writes `ghostie.blend`, `ghostie.glb`, `build_report.json` and `ghost_toon.json`.
2. `Blender -b ghostie.blend -P render_ghostie.py` writes the turnaround, hero, `_var-*`, `_close-*`, the silhouettes, `grey.png` and `crop_points.json`.
3. `node shoot_ingame.mjs` (three.js r170 with swiftshader) writes `ingame*.png`, `lineup-*.png` and `ingame_report.json`.
4. `python3 make_sheets.py` writes `variants.png`, `compare-ingame*.png`, `compare_report.json`, the `lineup-*-grey*.png` images and `crops/*.png`.

None of the runs crashed Blender. The newest `Blender-*.ips` file is still the Kit one from 16:01.

## What was built

| Part | Build | Triangles | Shown in |
|---|---|---|---|
| body | A lathe teardrop with 16 columns. It has an elliptic dome (crown 0.47 m, shoulder 0.31 m), a near-vertical side and a flared hem. The first ring has 8 vertices, which saves triangles for one more dome ring. | 192 | `turn-front.png`, `turn-side.png` |
| hem | 4 scallops. Each lobe is a wide tab with 3 low vertices, and each notch is a 40 mm V that tucks in. A rim 20 mm thick turns under into a closed, hollow cavity, and the rim edges are hard. | (in body) | `crops/hem-thickness-under.png`, `crops/hem-notch-34.png` |
| eyes | 2 ink dots, ovals with 8 sides. Each vertex is ray-cast onto the faceted body and lifted 1.1-2.2 mm. There is no mouth. | 16 | `crops/eye-on-surface-front.png` |
| arms | 2 tapered flaps with 5 sides. The pivot is on the body surface and the base ring is 32-54 mm inside the body. | 2 x 15 | `crops/arm-root-front.png`, `crops/arm-root-back.png` |
| acc_tie | A knot and a blade, both open shells, with the front face 3.0-5.8 mm off the surface. | 28 | `crops/tie-on-surface.png`, `crops/tie-side-profile.png` |
| acc_glasses | 2 hex frames around the eye dots, plus a bridge with a vertex on the centre ridge. | 52 | `crops/glasses-on-surface-front.png` |
| acc_headset | A mono headset. The band lies on the body's own vertex columns (so no chord cuts into the dome) and runs from one ring above the shoulder, over the crown, to a hex ear cup on the left (+X). | 60 | `crops/headset-cup-on-surface.png`, `crops/headset-band-over-crown.png` |

The node tree is root > float > body, eyes, arm_L, arm_R, acc_tie, acc_glasses, acc_headset. The glTF is Y-up and in metres. The accessory nodes carry `variant` and `default_visible` extras. The float node carries `float_rest_m` = 0.22, and the arms carry `pivot_axis_blender`.

## Decisions I made, with reasons (Opinion unless marked Fact)

1. **Size: 0.47 m body, floating 0.22 m, so the crown is at 0.69 m (70% of Kit's 0.977 m).** The Illustrator asked for about 1.0 Kit head-height (0.36 m) (`design/seats/illustrator.md`, section 4). At 0.36 m the ghost would be about 20 px at the 26 m camera, and the accessory about 2 px. At 0.47 m it is 27 px against Kit's 55 px (Fact: `ingame_report.json`, `lineup-grass`). It stays clearly smaller than Kit. If the gate wants 1.0 H, it is one constant (`HB`) in `build_ghostie.py`.
2. **Eyes on the vertex columns (±22.5°), below the shoulder ring.** In v0 the eyes sat at ±16.5°. The glasses frame then spanned a crease of the faceted body, and the body cut through the frame front by 3.16 mm (an earlier `build_report.json` run). Now the eye dot and the frame each lie on 2 faces that share the column ridge, inside one face row. Their visible faces are 2.25-3.0 mm off the surface (Fact: `build_report.json`). The cost: the eyes are set wide. I find that cute, but it is a style call for the Illustrator.
3. **Toon bands: Kit's 2-band thresholds, with the shadow band tinted lavender (184, 170, 255).** v0 used Kit's 3-band face ramp. The N.L = 0.5 boundary ran across a large, flat-lit side, so a small difference in normals flipped big wedges between Blender and three.js (`ingame.png` against `turn-34.png` in that run). The 2-band ramp is stable (Fact: `compare_report.json` mean 0.71/255). The lavender tint keeps the value of the shadow band level with Kit's grey shadow (relative luminance about 0.66-0.68). A stronger lavender dropped the ghost to grass value in the backlit world shot. Under the warm Applyside light the "lavender" reads pink-mauve (`lineup-grass-crop-x3.png`).
4. **No ink outline on the accessories.** They are open shells, and an inverted hull on an open shell drew detached lines beside the tie (v0 `turn-front.png`). Faded and without ink also fits the idea that the recruiter has faded. The body and the arms do have ink.
5. **The "Seen ✓" tag is a game-side billboard. It is not in the mesh, and I did not build it here.** It costs no triangles, and the UI can size it for legibility (Lena's rules for world text).
6. **Hull normals in three.js are angle-weighted.** This matches Blender's Solidify. With the area-weighted `computeVertexNormals` (Kit's path), the narrow hem rim lost its ink under the lip, and the compare showed it (mean 1.36 → 0.71, `compare-ingame.png`). The Kit path is unchanged.
7. **Variant renders:** tie and glasses at -30°, headset at -60°, so that the ear cup faces the camera (`variants.png`).
