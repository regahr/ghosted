# Direction: ATS-9000 3D v1 (Viet Tran, 2026-11-26)

3dviz-pro-max `SKILL.md` steps 1 (intent), 2 (hardest parts first), 4 (construction and joins), 5 (quality targets).
Tool outputs are in `skill/`.

## 1. Intent and visual direction
- What the player sees: a friendly office machine that screens CVs. A mid-grey monitor head with a black screen and
  two cream pill eyes, on a dark bellows neck, on a grey mailbox body with a black slot "mouth" and a lip tray, on
  two black tank treads. A stamp arm on its left, an antenna with a gold ball on its right top corner.
- At the game camera it must read as **grey head, dark neck band, grey body, dark treads**, with the cream eyes on
  the dark screen, next to the mid-grey Kit, 1.21 x Kit's height.
- References: only the accepted sheet v2 (`../sketch/ats-sheet.png`), the body map (`../sketch/body-map.png`,
  `body-map.md`) and their Bezier source (`../sketch/src/ats.py`). Kit sets the toon, the ink hull and the light;
  Ricky v1 sets the pipeline.
- Viewing distances: game camera 26 m (about 91 px tall); cards 900x1200 (front, 3/4, side, back), hero 1200x1200,
  motion cards (stamp, slot, screens).
- Look: Kit's 2-band toon (neutral grey 178 shade band), Kit's light, the 7 mm inverted-hull ink outline. Ink parts
  (screen, slot, neck rings, treads, rubber, stalk) are unlit ink, as Kit's ink. Box edges bevelled 0.02 m so the
  toon light catches a thin edge band (`skill/resolve-bevel-normal.txt`).

## 2. The hardest parts (solved first on tiny tests in `tests/` and on the blockout in `blockout/`)
1. **The neck at the game camera.** The head (68 u deep) hides part of the neck from pitch 42. The neck must show as
   a band in px, and we must see honestly whether it reads as a second mouth. Test: the blockout at the game camera
   with a mask render (rings red, core green), counting visible neck px in the centre column.
2. **The screen and the moving textures in the game engine.** One screen mesh with 5 states by UV, a scrolling scan
   line, hub spokes that turn and belt cleats that scroll, all from the exported glb, in both Blender and three.js.
   Test: `tests/test_textures.py` (Blender, a tiny glb) + `tests/test_textures.mjs` (three.js reads it, sets the UV
   offsets, renders).
3. **Bevels inside 900 triangles.** Bevelled head, body and stamp block with flat faces and a hard toon edge, and
   12-sided rings. Test: the triangle count of the bevelled head in `tests/test_textures.py`.
4. **The scale:** 1.21 x Kit measured in px on the blockout, the Ricky way.

## 3. Construction (step 4) and join decisions
Units: sketch front-view units, y down, axis x 150, ground y 340; X = x - 150 (+X = viewer-right = the robot's LEFT),
Z forward. 1 unit = H / 334 m; H is set by the blockout measure. Blender Z-up, robot faces -Y; glTF Y-up (faces +Z).

Nodes: `root > float > bounce > body` (static), `bounce > screen`, `bounce > stamp_pivot > stamp`, and a prop `cv`
(not part of the robot; parked under root, hidden by default).

| Join | Decision | Reason |
|---|---|---|
| Head to neck, neck to body | **Separate parts, sunk**: the grey core runs 4 u into the head and 6 u into the body (body map C) | Rigid robot parts; the head does not turn; the sunk core hides the seam |
| Bellows rings | **Layered**: 3 short ink cylinders (12 sides) around the core | They are the bellows folds; ink = the dark band that separates head and body |
| Shoulder hub to body | **Separate part, sunk**: hub cylinder on the X axis from inside the body side to x 246 | A mechanical shoulder; its inner end is hidden inside the body |
| Stamp arm to hub | **Separate articulated part**, ONE hinge at the hub axis (`stamp_pivot` node); bar, block and rubber are one rigid mesh | Brief: one hinge; a rigid mesh cannot pinch |
| Antenna to head | **Separate parts, sunk**: socket cylinder into the head top, stalk tube, ball | Static in v1 |
| Lip tray to body | **Continuous with the body mesh, separate shell**: a trapezoid prism pushed into the front face | Body map C: "the lip is part of the body mesh" |
| Slot | **Decal**: one ink quad 0.5 u in front of the body front | Body map C allows a decal; a CV can pass "into" it |
| Screen | **Decal mesh**: 2 quads 0.6 u in front of the head front: the eyes atlas quad and the scan-line quad | Its own non-swap mesh (brief); UV state swap and V scroll |
| Treads to body | **Separate, touching**: the belt top meets the body hem (y 304) | Body map C |
| Hub discs | **Decals on the outer tread faces**, each disc mapped to the full hub texture, so one UV rotation turns all 6 | Hubs spin with one texture transform |
| Back vents and hatch | **Decals** (ink line quads) | Front and back never get mixed up |

## 4. Triangle plan (cap 900 visible; non-swap meshes: `body`, `stamp`, `screen` = 3)
| Part | Plan |
|---|---|
| Head (bevelled rounded box) | about 140 |
| Body arch + lip + slot | about 150 |
| Neck core (12, open) + 3 rings (12, capped) | about 160 |
| Treads (2 stadium prisms) + 6 hub discs | about 140 |
| Shoulder hub + pivot dot | about 40 |
| Antenna (socket, stalk, ball) | about 80 |
| Back decals | about 20 |
| Stamp arm (bar, bevelled block, rubber) | about 90 |
| Screen (2 quads) | 4 |
| Total | about 825 |

## 5. Quality targets (step 5)
- Card: crisp box edges with a thin bevel band; neck rings separate with grey gaps; every decal seated; the stamp arm
  on the robot's left at 45 deg; the antenna on the right top corner; symmetric upright turnaround.
- Game camera: 1.21 x Kit in px; the neck band visible in px under the head; the eyes visible on the screen.
- Engine: the three.js render of the exported glb matches the Blender render; the texture motions work from the glb.

## 6. Skill records used (step 4)
- `knowledge.style-low-poly` (`skill/resolve-style-low-poly.txt`): spend detail on the contour; 12 segments around
  turning parts (rings, hub), few faces on flat panels. Adapted.
- `knowledge.hard-surface-bevel-normal-contract` (`skill/resolve-bevel-normal.txt`): one normal owner; export split
  normals from Blender and keep them in three.js (no recompute on the toon mesh). Adapted.
- `knowledge.reasoning-texture-screen-footprint` (`skill/resolve-screen-footprint.txt`): the screen is about 12 px
  wide at the game camera and about 300 px on the hero card, so a 256 px cell per state is enough; nearest-free
  linear filtering with mipmaps.
- `recipe.robot-arm-forward-frames` (`skill/resolve-robot-arm.txt`): one joint frame at the hub axis; the arm angle
  is the only state.
- Coverage gap: no catalog record for a bellows neck or tank treads (`skill/search-character.txt`).
