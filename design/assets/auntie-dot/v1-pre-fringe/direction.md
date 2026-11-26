# Direction: Auntie Dot 3D v1 (Viet Tran, 2026-11-26)

3dviz-pro-max `SKILL.md` steps 1 (intent), 2 (hardest parts first), 4 (construction and joins), 5 (quality targets).
Tool outputs are in `skill/`.

## 1. Intent and visual direction
- What the player sees: the kindest character in the game. A short, round "cottage loaf": a big round head with a
  white swept-up hair dome and a top-back bun, on a soft purple pear with folded hands, and a faded lilac headset
  ring round the neck. At the game camera she must read as **a white dome and bun on a peach face, on a dark purple
  pear, with a lilac ring at the neck**, about 0.9 x Kit's height.
- References: only the accepted sheet (`../sketch/dot-sheet.png`), the body map (`../sketch/body-map.png`) and their
  Bezier source (`../sketch/src/dot.py`). Kit (`../../kit/`) sets the toon, the ink hull and the light. Ricky v1
  (`../../ricky/v1/`) sets the pipeline. The ATS v1 `ingame.html` sets the full lineup.
- Viewing distances:
  - game camera: 26 m, pitch 42, yaw 20; Dot about 67-68 px tall at 1x;
  - card: 900x1200 front, 3/4, side and back; hero 1200x1200; face and headset close views.
- Look: Kit's 2-band toon (neutral grey 178 shade band), Kit's light, a 7 mm inverted-hull ink outline; flat ink
  decals for the face, the hairline, the strands, the placket and the pockets.

## 2. The hardest parts (solved first on the blockout, `blockout/`)
1. **Scale and the face read at the game camera.** Dot is short and the camera looks down 42 deg, so the hair dome
   can cover the eyes and the smile can merge into a dark mark. Measured in screen pixels on the blockout, next to
   the real Kit, before the final model.
2. **The hairline.** White hair on peach skin is 1.48:1, so the edge needs ink. It must run on the forehead, drop
   behind the ear and meet the nape, in every view, with no gap or zig-zag. Solution: the hairline is a per-column
   curve on ONE head surface (continuous skin), with an ink lip and a thin ink band on the skin side, built into
   the body mesh (no decal can follow it round the back).
3. **The arms on a pear.** The folded arms lie on the belly; the talk arm goes up beside the face; the card arm goes
   forward. Sleeves must leave the body with no shoulder ball, no hook and no float, in all three poses.
4. **The neck ring.** The band rests round the neck line, the cups sit on the collarbones and face forward; the
   band must not sink into the shoulder slope nor float visibly.
5. **The budget:** a round head, a bun, a pear, two arms, a headset and the face inside 1,400 triangles, with the
   card beat inside the same budget. Shading normals come from the analytic surfaces (Ricky / Ghostie v7 method).

## 3. Construction (step 4) and join decisions
Units: sketch front-view units, y down, axis x 150, sole y 340, bun top y 40. 1 unit = H / 300 m; H is set by the
blockout measure. Blender Z-up, Dot faces -Y; glTF Y-up.

Nodes: `root > float > bounce > rig` (bones `body_root` at the feet, `torso` (pivot at the feet: the sway), `head`
(pivot 6 units under the chin, y 178), `arm_L_up`, `arm_L_lo`, `arm_R_up`, `arm_R_lo`). Skinned meshes: `body`,
`decals` (non-swap: 2), swap parts `eyes_open`, `eyes_happy`, `mouth_smile`, `mouth_talk`, prop `card`.

| Join | Decision | Reason |
|---|---|---|
| Hair to head skin | **Continuous skin**: one revolved surface; rows above the per-column hairline are hair (skull + 4, as the sketch `CAP_HALF`), thinning to the skin AT the hairline; a 2.6-unit ink band on the skin carries the edge | Chair call 2 (ink edge). One shell: no z-fight; the hairline goes round the back to the nape. Build note: a 4-unit overhang (Ricky's lip) drew a second thin hull line above the hairline in both renderers, and a 1.2-unit lip flipped its triangles, so the final has no overhang |
| Bun to hair | **Layered**: an ellipsoid sunk into the crown (centre y 60, Z -18, radii 25/21/23) | It must stand off the dome as a bump in the silhouette (sheet, 64 px silhouette) |
| Ears | **Layered**: small ellipsoids half sunk at the eye line, X +-56, Z -4 | Body map B; the hairline passes behind them |
| Head to neck to body | **Separate parts, sunk**: the head is closed at the chin; a short skin neck tube runs from inside the head to inside the body top | The sketch draws a short neck between chin and body; the head rolls 8 deg in the talk beat about a pivot under the chin, so a rigid ball-on-neck cannot tear |
| Sleeve to body | **Sunk tube (reads as a continuous sleeve)**: the upper sleeve starts inside the body at the arm root (X +-52, y 206) with a round end that never shows; no shoulder ball outside the body | Sketch note "continuous skin, no shoulder ball". A welded skin would stretch and pinch when the arm lifts to the face; a sunk tube keeps the same silhouette and cannot tear. Same colour, and the merged ink hull shows no ring at the buried part |
| Elbow | **Rigid ball joint**: the upper sleeve and the forearm both end in a sphere of the sleeve radius, each weighted 1.0 to one bone | Cannot pinch at the folded-arm bend (about 100 deg) |
| Hand | **Separate ball**, sunk 2-3 units into the sleeve end, on the forearm bone | Sheet: sleeve then hand ball, no cuff |
| Legs to hem | **Separate**: two short skin tubes sunk under the hem, on `body_root` (they do not sway) | Feet stay planted in the sway |
| Shoes | **Separate** ellipsoids on `body_root` | As Kit and Ricky |
| Headset | **Separate parts in the body mesh** on `torso`: a 4-sided tube band round the neck line (back point y 183), ends running forward and down into two discs on the collarbones, faces 22 deg up | Body map C; inside the body hull, so it gets ink with no extra mesh |
| Face, strands, placket, buttons, pockets | **Decals**, projected onto the analytic surface and lifted along the normal; face parts on `head`, body parts on `torso` | Flat marks need no volume |
| Card | **Prop mesh skinned to `arm_R_lo`**, built in the hand's rest frame so it lands in the hand in the card pose | Brief: shown only in the card beat |

Poses: bone rotations stored as axis + angle in float space (Ricky method), solved in the build with a two-bone reach
to the sketch's hand targets (talk: hand at (-94, 180, 24); card: hand at (-42, 234, 104)); head roll and torso lean
are added to the same pose tables. The sway is a parameter (torso +-4 deg about the feet, head -half of it).

## 4. Triangle plan (cap 1,400 visible)
| Part | Plan |
|---|---|
| Head + hair + hairline ink (16 columns) | about 340 (built: 288) |
| Bun, ears, neck | about 100 |
| Body pear (16 columns, 7 bands, hem fan) | about 240 |
| Arms: 2 x (upper capsule, forearm, hand) | about 290 |
| Legs and shoes | about 90 |
| Headset band and 2 cups | about 140 |
| Decals: brows, strands, placket, buttons, pockets | about 120 |
| Eyes (swap) and smile (swap) | about 60 |
| Total at rest | about 1,380; the card (about 20) is shown instead of nothing, so the card beat must also stay <= 1,400 |

## 5. Quality targets (step 5)
- Card: a smooth dome, bun and pear outline at 2x; no hook, crease or ring at the arm root, elbow or hand; every
  decal seated with ink; the hairline continuous round the head and behind the ears; the band centred with a cup on
  each collarbone; upright and symmetric mesh.
- Game camera: 0.9 x Kit in pixels (67-68 px); the hair's lowest pixel in the eye columns above the eye top; the
  smile reads as a smile (small curved line), not a dark bar or a moustache.
- Engine: the three.js render of the exported glb matches the Blender render.

## 6. Skill records used (step 4)
- `knowledge.style-low-poly` (resolved, `skill/resolve-style-low-poly.txt`): spend detail on the contour. Adapted:
  16 columns on the head and the pear; 8 sides on the sleeves; 6 on the legs.
- `knowledge.style-stylized` (resolved, `skill/resolve-style-stylized.txt`): one exaggeration (big head, round
  pear) and keep the identifying parts (bun, neck ring, folded hands).
- `recipe.expression-attention-rig` (resolved, `skill/resolve-expression-rig.txt`): a small set of honest
  expressions; adapted as three swap sets (rest, talk, happy), no gaze.
- Coverage gap: no catalog record for a sleeve join on a pear body or a neck-worn headset (`skill/search-joins.txt`,
  `skill/search-accessories.txt`). The join decisions above are my own, from `references/object-craft.md`
  "Choose continuity at the join".
