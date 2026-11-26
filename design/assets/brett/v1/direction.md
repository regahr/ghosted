# Direction: Brett Bullet-Points 3D v1 (Viet Tran, 2026-11-26)

3dviz-pro-max `SKILL.md` steps 1 (intent), 2 (hardest parts first), 4 (construction and joins), 5 (quality targets).
Tool outputs are in `skill/`.

## 1. Intent and visual direction
- What the player sees: the rival, one week ahead. A smug but likeable LinkedIn networker. At the game camera he must
  read as **a green ring floating over a blond swoop, a peach face with two eyes and a white grin, a red wedge with a
  white V and white sleeves, navy legs**, about 1.05 x Kit's height without the ring.
- Shape: "the wedge" (sketch direction A): wide square chest, narrow waist, long legs; wide at the top, the opposite
  of Ricky's bell and Dot's pear.
- References: only the accepted sheet (`../sketch/brett-sheet.png`), the body map (`../sketch/body-map.png`,
  `body-map.md`) and their Bezier source (`../sketch/src/brett.py`). Kit sets the toon, ink hull and light; Auntie Dot
  v1 (`../../auntie-dot/v1/`) sets the pipeline and the full lineup.
- Viewing distances:
  - game camera: 26 m, pitch 42, yaw 20; Brett about 79 px tall at 1x (without the ring);
  - card: 900x1200 front, 3/4, side and back; hero 1200x1200; face, halo, swoop and hand close views.
- Look: Kit's 2-band toon (neutral grey 178 shade band), Kit's light, the inverted-hull ink outline (it also runs
  round the halo, chair call 3); flat ink decals for the face, the part, the vest V, collar and ribs.

## 2. The hardest parts (solved first on the blockout, `blockout/`)
1. **The grin at 1x.** It sits close under the eyes and the camera looks down 42 deg. A dark mouth or an edged white
   shape merges into a moustache or goatee (sketch test, `../sketch/notes.md` "The grin"). Solution from the sketch:
   white teeth crescent with no edge, over an ink smile line with the corners up, plus the 10 deg chin-up carriage.
   Measured on the blockout in screen pixels next to the real Kit: grin box, luma profile (light over dark), gap to
   the eyes.
2. **The halo.** It must read on green grass (1.71:1) through its ink edge only, float level above the swoop, follow
   the head, and stay level under the chin-up nod. Solution: a low torus inside the body mesh, skinned to its own
   `halo` bone, a child of `head`; every head nod adds the opposite turn on `halo` about the same axis, so the ring
   follows the head's position and stays level. It is in the body mesh, so the merged ink hull draws round it.
   Checked numerically (ring normal vs world up after the carriage) and on screen.
3. **Hair against the eyes.** The swoop rolls forward over the forehead. Its lowest point (y 57) must stay above the
   hairline (62) and both above the eyes (85) in the game view, with the carriage.
4. **Scale without the halo.** The halo is hidden for the scale measure (its bone scaled to 0), so the box is
   sole to swoop top only.
5. **The arms.** Three poses from one bind pose with fixed bone lengths: hands on hips (both), the Like (his right fist
   out at the side, thumb up), bullets (his right hand up beside the chest). Sleeves leave the vest with no shoulder
   ball, no float, no hook.
6. **The budget:** head, hair cap, swoop, ears, halo, wedge, hips, two arms, legs, shoes and the face in 1,400
   triangles in every beat (the thumb and fingers are swap parts that add to the beat that shows them).

## 3. Construction (step 4) and join decisions
Units: sketch front-view units, y down, axis x 150, sole y 340, swoop top y 16. 1 unit = H / 324 m; H (sole to swoop
top) is set by the blockout measure. Blender Z-up, Brett faces -Y; glTF Y-up.

Nodes: `root > float > bounce > rig` (bones `body_root` at the feet, `torso` (pivot at the feet: the lean),
`head` (pivot on the chin, y 148), `halo` (child of `head`, pivot at the ring centre, y 0), `arm_L_up`, `arm_L_lo`,
`arm_R_up`, `arm_R_lo`). Skinned meshes: `body`, `decals` (non-swap: 2). Swap parts: `eyes_open`, `eyes_wink`,
`brows_rest`, `brows_smug`, `brows_lost`, `mouth_grin`, `mouth_talk`, `mouth_lost`, `thumb`, `fingers_1`,
`fingers_2`, `fingers_3`.

| Join | Decision | Reason |
|---|---|---|
| Hair cap to head skin | **Continuous skin**: one revolved surface; rows above the per-column hairline lie on the sketch `CAP_HALF` surface (radial projection from the skull centre), the last row thins to the skin AT the hairline; an ink band on the skin carries the edge | Dot's proven method (no overhang: an overhang drew a second hull line). Hair vs skin is 1.29:1, so the edge needs ink (sketch note) |
| Hairline at the ear | The hairline stays ABOVE the ear top (y 80 at the ear column), then drops behind the ear to the nape (y 132) | Sketch builder note: the far-ear notch. A layered ear that pokes through the cap makes that notch |
| Swoop to cap | **Layered**: a tube through the 5 hand-placed `WAVE` points (Catmull-Rom smoothed), round ends, half sunk into the cap | It must stand off the cap as a roll in the silhouette, front and side |
| Ears | **Layered**: small ellipsoids half sunk at the eye line, X +-55, axis pointing out | Body map B; the side view shows a round ear |
| Halo | **Separate part in the body mesh** on the `halo` bone (counter-turned under a nod) | Chair call 3: level, ink edge, follows the head |
| Head to neck to vest | **Separate parts, sunk**: head closed at the chin; a skin neck tube from inside the head to inside the vest top | The head nods 10 deg about the chin; a sunk neck cannot tear |
| Sleeve to vest | **Sunk tube (reads as continuous skin)**: the white upper sleeve starts inside the vest at the arm root (X +-56, y 176), no shoulder ball outside | Sketch: "shirt sleeve out of the vest armhole, no shoulder ball". Dot's method: welded skin would pinch when the arm lifts to the Like |
| Elbow | **Rigid ball joint**: both sleeve parts end in a sphere of the sleeve radius, each on one bone | Cannot pinch at the hips bend (about 90 deg) or the Like bend |
| Hand | **Separate ball**, the sleeve end sunk into it, on the forearm bone | Sheet: sleeve then ball hand |
| Thumb, fingers | **Swap parts** (capsules) on `arm_R_lo`, built in the pose frame of their beat and moved back to the rest frame | Body map C; brief budget: swap meshes |
| Vest to hips | **Layered**: the chinos hips band sits under the vest hem (vest hem y 252, hips y 246-268) | The sheet shows a navy band under the hem |
| Legs to hips, shoes | **Separate**: leg tubes sunk into the hips, shoes as ellipsoids, all on `body_root` (planted in the idle lean) | Feet planted |
| Face, part, vest V, collar, ribs | **Decals**, projected onto the analytic surface (head, cap, vest), lifted along the normal; face on `head`, vest marks on `torso` | Flat marks need no volume |

Poses: bone rotations stored as axis + angle in float space (Dot / Ricky method), solved in the build with a two-bone
reach to the sketch's hand targets (`brett.py` `model()`): hips (+-50, 246, 10), Like (-96, 172, 20), bullets
(-82, 176, 28). The carriage is the head nod -10 deg plus +10 deg on `halo`; it is part of every in-game state and
off for the model-sheet turnaround. The idle puff is torso -3 deg about the feet plus a 3-unit rise of the torso.

## 4. Triangle plan (cap 1,400 visible)
| Part | Plan |
|---|---|
| Head + hair cap + hairline ink (16 columns) | about 300 |
| Swoop tube | about 110 |
| Ears, neck | about 50 |
| Halo torus (12 x 5) | 120 |
| Vest wedge (16 columns) | about 180 |
| Hips | about 50 |
| Arms: 2 x (upper sleeve, forearm, hand) | about 250 |
| Legs and shoes | about 120 |
| Decals: part, vest V, skin V, collar, ribs | about 90 |
| Eyes, brows, mouth (swap) | about 80 |
| Thumb or fingers (swap, in their beat) | about 20-50 |
| Total | about 1,370 in the heaviest beat |

## 5. Quality targets (step 5)
- Card: clean wedge, swoop and ring outline at 2x; no hook, crease or ring at the arm root, elbow or hand; every
  decal seated with ink; the hairline continuous round the head and above / behind the ears; no grin sliver or brow
  tip on the side profile; the ring level and centred; upright and symmetric apart from the part and the swoop.
- Game camera: 1.05 x Kit in pixels without the ring (78-79 px); the lowest hair pixel in the eye columns above the
  eye top; the grin reads as light teeth over a dark line, not a dark bar or a beard; the ring reads on the grass.
- Engine: the three.js render of the exported glb matches the Blender render.

## 6. Skill records used (step 4)
- `knowledge.style-low-poly` (`skill/resolve-style-low-poly.txt`): spend detail on the contour. Adapted: 16 columns on
  the head and the wedge, 8 sides on the sleeves and the swoop, 6 on the legs.
- `knowledge.shared-skinned-articulated-rig` (`skill/resolve-skinned-rig.txt`): the joint hierarchy owns the pose,
  rigid subparts need no skinning blend. Adapted: every vertex on one bone (rigid parts), poses stored on bones, the
  bind pose kept as the neutral turnaround.
- `knowledge.layered-decal-surface-handoff` (`skill/resolve-decal.txt`): projection stretches at grazing angles.
  Adapted: the face marks stay inside +-32 deg of the front; marks are runtime meshes, swapped by expression.
- `knowledge.reasoning-texture-screen-footprint` (`skill/resolve-screen-footprint.txt`): judge detail by its screen
  footprint. Adapted: the grin and the ring are measured in screen pixels at the real camera.
- Coverage gap: no catalog record for a floating halo that stays level, or a vest armhole join
  (`skill/search-halo.txt`, `skill/search-joins.txt`). The join decisions above are my own, from
  `references/object-craft.md` "Choose continuity at the join".
