# Direction: Recruiter Ricky 3D v1 (Viet Tran, 2026-11-25)

3dviz-pro-max `SKILL.md` steps 1 (intent), 2 (hardest parts first), 4 (construction and joins), 5 (quality targets).
Tool outputs are in `skill/`.

## 1. Intent and visual direction
- What the player sees: a cheerful, busy recruiter. A near-black bell jacket with a white shirt V, a lilac tie, a
  lilac headset ring over a brown quiff, and a wide grin. At the game camera he must read as **a dark bell with a
  white V and a light ring on top**, next to the mid-grey Kit.
- References: only the accepted sheet (`../sketch/ricky-sheet.png`), the body map (`../sketch/body-map.png`) and
  their Bezier source (`../sketch/src/ricky.py`). Kit (`../../kit/`) sets the toon, the ink hull and the light. The
  Ghostie v7 (`../../ghostie/v7/`) sets the pipeline and the drain end.
- Hair change (Rega, ts 1795622664.391049): no fringe. The hair is a cap on top. The front hairline sits on the
  forehead, well above the brows (front-view y 62-68; the brows are y 77-83), and the temples stay above the brows
  until they pass behind the ear plane. Then the hair curves down the back to the nape, as in the sheet BACK view.
- Viewing distances:
  - game camera: 26 m, pitch 42°, yaw 20°; Ricky is about 76 px tall at 1x (1.05 x Kit's 72 px);
  - card: 900x1200 front, 3/4, side and back; hero 1200x1200; close views.
- Look: Kit's 2-band toon (neutral grey 178 shade band), Kit's light, a 7 mm inverted-hull ink outline.

## 2. The hardest parts (solved first on the cheap blockout in `blockout/`: `blockout-sheet.png`, `ingame_report.json`)
1. **The phone arm.** The right hand must reach the right cup with a clear elbow, and with no pinch, crack or
   floating part, at rest, mid-way and at the end. Test: the arm alone plus the head and cup, rest and phone, in
   front and 3/4.
2. **The arm-to-jacket join and the shoulder ball.** No hook, crease or hard ring where the sleeve meets the
   jacket, at card size; the inner ink line between arm and jacket must show where the arm lies in front.
3. **The screen scale and the hair line at the game camera.** Measured in screen pixels on the blockout, next to the
   real Kit and a Ghostie, before the final model.
4. **The budget:** a round head, a round bell and two arms inside 1,400 triangles. The toon terminator must not show
   the facets, so the shading normals come from the analytic surface (Ghostie v7 method), at 0 triangles.

## 3. Construction (step 4) and join decisions
Units: sketch front-view units, y down, axis x 150, sole y 340. 1 unit = H / 304 m; H is set by the blockout
measure (§5). Blender Z-up, Ricky faces -Y; glTF Y-up.

Nodes: `root > float > bounce > rig > body` (skinned) and `bounce > decals`; swap parts `mouth_grin`, `mouth_o`
on `bounce`.
- `float`: the drain lift. `bounce`: pivot at the soles, the hop squash (scale), as Kit's `bounce` node.
- `rig` bones: `body_root`, `arm_L_up`, `arm_L_lo`, `arm_R_up`, `arm_R_lo`.

| Join | Decision | Reason |
|---|---|---|
| Head to hair | **Continuous skin**: one revolved surface; the rows above the hairline ring are hair, with a 3-unit lip at the hairline (the cap is skull + 3, as `capd`) | No second shell, so no hidden faces and no z-fight; the lip gives Kit's hair edge (`kit/build_report.json` "hair_edge_height_above_skin_mm") |
| Quiff to hair cap | **Layered**: an ellipsoid sunk into the crown (the sheet's `pomp`) | It must stand off the cap silhouette, as in the sheet side view |
| Head to jacket | **Separate parts**: the head sits on the collar ring; the neck is hidden | The sheet draws the head as its own ball on the collar (Kit does the same) |
| Collar ring | **Layered**: a short white ring tube round the neck, under the chin | Value break in every view (sheet: "collar rings the neck") |
| Arm to jacket | **Separate articulated parts, sunk**: the shoulder ball is the round top of the upper-sleeve capsule, half inside the jacket at the shoulder joint (x 84/216, y 176). The ball merges into the jacket (same colour, no ink at the buried part); the inner ink line shows only where the sleeve lies in front of the jacket | The Ghostie lesson is about flat flaps; Ricky's sleeves are round tubes like Kit's, and Kit uses sunk tubes. A continuous skin would tear when the arm lifts to the cup. Brief: "merge the shoulder balls into the jacket first" |
| Elbow | **Separate rigid parts with a shared joint ball**: the upper-sleeve capsule and the forearm capsule both end in a sphere of the sleeve radius at the elbow; each is weighted 1.0 to one bone | A rigid ball joint cannot pinch at 120°. In the straight rest pose the two capsules meet tangent, so no ring shows |
| Cuff, hand | **Layered on the forearm bone**: a white ring at the sleeve end, then a skin ball | Sheet: sleeve, cuff, hand |
| Legs to jacket | **Separate**: two short tubes sunk under the hem, their own material `leg` | The drain fades the legs: own material = own fade |
| Shoes | **Separate** ellipsoids, own material `shoe` | Fade with the legs |
| Headset | **Layered, in the body mesh** (`body_root` bone): band over the crown in the ear plane, a cup on each ear point, mic boom and ball from the right cup (viewer-left in front) | Inside the body hull, so it gets ink with no extra mesh |
| Face, shirt V, collar wings, tie, button | **Decals** in one `decals` mesh, projected onto the surface and lifted along the normal; ink cards under the tie and the collar (Ghostie v7 method) | Flat marks need no volume |
| Mouth | swap parts `mouth_grin` (rest) and `mouth_o` (drain step 1); none in step 2 | Body map E |

Phone gesture: a **bone pose**, not a morph. `arm_R_up` turns at the shoulder and `arm_R_lo` at the elbow. The angles
are solved in the build (a two-bone reach to a point on the outer face of the right cup), and stored on `float` as
axis + angle in float space, as Ghostie's `wave_axis_float_blender`. A morph would collapse the forearm rings
mid-way (the forearm turns about 150°).

Hop: `bounce` scale only (squash 1.08/0.88 on the bounce, stretch 0.96/1.07 in the air) plus arms out by bone.
Drain: material colour lerps and opacity fades, driven by the game. The materials are split for it: `suit`, `leg`,
`shoe`, `skin`, `hair`, `shirt`, `acc` (headset), `mic`, `tie`, `ink`, `brow`, `white`.

## 4. Triangle plan (cap 1,400 visible; non-swap meshes: `body`, `decals` = 2)
| Part | Plan |
|---|---|
| Head + hair cap (16 columns, rows to the hairline lip) | about 300 |
| Quiff ellipsoid | about 60 |
| Jacket bell (16 columns, 8 rows, hem and neck fans) | about 290 |
| Collar ring | 32 |
| Arms: 2 x (upper capsule, forearm capsule + cuff, hand) at 6-8 sides | about 290 |
| Legs (2 x 8-side tube) and shoes (2 x ellipsoid) | about 130 |
| Headset: band, 2 cups, mic | about 130 |
| Decals: eyes, glints, brows, shirt V, collar wings, tie with ink, button | about 120 |
| Mouth (grin) | about 20 |
| Total | about 1,370 |

## 5. Quality targets (step 5)
- Card: a smooth head and bell outline at 2x; no hook, crease or ring at the shoulder, elbow or cuff; every decal
  seated, with ink; the headset centred, a cup on each ear, the mic from the right cup; the tie centred under the
  collar; upright and symmetric mesh.
- Game camera: a dark bell with a white V and a light ring; 1.05 x Kit's height in pixels; the hair's lowest point
  above the eye top in px.
- Engine: the three.js render of the exported glb matches the Blender render.

## 6. Skill records used (step 4)
- `knowledge.style-low-poly` (resolved, `skill/resolve-style-low-poly.txt`): spend detail on the contour. Adapted:
  16 columns on the head and the bell; 6-8 sides on the thin arms and legs.
- `knowledge.morph-target-topology-compatibility` (resolved, `skill/resolve-morph-topology.txt`): I checked it and
  chose bones for the phone, because the forearm turn is too large for a linear morph. No morph targets ship.
- `knowledge.style-stylized` (in `skill/search-character.txt`): one exaggeration (the bell and the big head) and keep
  the identifying parts (headset, V, tie).
- Coverage gap: the catalog has no record for a character sleeve join or a headset (`skill/search-character.txt`,
  `skill/search-accessories.txt`).
