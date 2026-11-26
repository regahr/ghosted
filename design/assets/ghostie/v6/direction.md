# Direction: Ghostie 3D v6 (Viet Tran, 2026-11-25)

3dviz-pro-max SKILL.md steps 1 (intent and direction), 2 (hardest objects first), 4 (construction and joins) and 5
(quality targets). Tool outputs are in `skill/`.

## 1. Intent and visual direction
- What the viewer sees: a shy office ghost, a soft sheet dome with two tall ink eyes, no mouth, small flipper arms and
  a 5-lobe hem. One recruiter prop per variant: a centred tie under a collar, round glasses, or a headset.
- References: only the accepted sheet (`sketch/ghostie-sheet.png`), the body map (`sketch/body-map.png`) and their
  Bezier source (`sketch/src/ghost.py`). Kit (`assets/kit/`) sets the toon shading, the ink hull and the light.
- Viewing distances:
  - game camera: 26 m, pitch 42°, yaw 20°; the ghost is about 41 px tall at 1x;
  - card: 900x1200 front, 3/4, side and back; hero 1200x1200; close views at 2.2x.
- Look: Kit's 2-band toon (grey 178 shade band, neutral), Kit's light, a 7 mm inverted-hull ink outline.

## 2. The hardest parts, solved first on a small test (`tests/`)
1. **Arm join and wave on one skin.** Test: the body and both arms only, rendered front, 3/4 and with the wave at
   +40°, at card size, before any accessory. Pass: no corner, crease, pale wedge or hook at the shoulder.
2. **Smooth dome within the budget.** Same test: the front and 3/4 outline at card size.
3. **Arm tips below the eye dots at the game camera.** Measured in screen pixels on the same test glb, in the real
   lineup, at rest and at wave 0, 20 and 40°.
4. **Headset band over the crown, with ink, inside 600.** Test after the body passes.

## 3. Construction (step 4) and join decisions
- **Body:** a ring lattice built from the sketch curves. Each row is a superellipse. Its half-width comes from the
  FRONT outline and its half-depth from the SIDE outline at the same y. So the front and side outlines are the sketch
  curves at every row. The body is upright and mirror-symmetric in the mesh.
- **Join 1, arm to body: continuous skin (one mesh, shared vertices).** No boolean. On each side, a 2x2 patch of body
  faces is opened. The arm is a tube that starts on that opening's edge loop and runs out to a round tip. The tube's
  top and bottom edges follow the sketch arm outline, point for point. The first arm ring flares, so the shoulder is
  a fillet and not a step. Reason: v1-v4 used separate flaps and v5 a boolean union; both left a hook, a crease or a
  wedge at the join (`acceptance/ghostie/retro-viet.md` §2).
- **Join 2, accessories to body: separate swap parts that lie on the surface** (layered covering). Each part is
  projected onto the body and offset along the normal. The parts are fixed to the float node, so they do not move
  with the arms. The tie, collar, glasses and headset never cross an arm.
- **Join 3, wave:** a linear-blend skin. Bones: body_root, arm_L and arm_R. Weights are written by ring: 1 on the outer
  rings, a blend on the flare ring, 0 on the body.
- **Ink:** one inverted hull on the body (as Kit). The headset gets its own hull, so it needs no extra ink geometry.
  The tie, the collar and the glasses carry their ink as a slightly larger ink card under each coloured card.
- **Hem:** an open hem with no inner cavity. The game camera never sees under it.

## 4. Triangle plan (cap 600 per variant)
| Part | Plan |
|---|---|
| Dome: 8 rows, 8 columns at the crown and then 16 | about 208 |
| Shoulder and arm rows (y 180, 190, 225, 260) | about 128 |
| Hem band, 16 to 30 vertices, 5 lobes | 46 |
| 2 arms (3 rings and a pole each, minus the opening) | about 96 |
| Eyes, 2 x 12-gon | 24 |
| Base | about 502 |
| Tie + collar + ink cards | about 40 (cap 68) |
| Glasses: 2 rims, each a lilac band and an ink band, plus the bridge | 82-98 |
| Headset: 2 cups (8 sides, no back) + a ridge band | about 84-90 |

## 5. Quality targets (step 5)
- Card: no outline corner on the dome, the shoulders or the arm tips at 2x zoom. No shade streaks. Every accessory
  seated on the surface, with ink all round.
- Game camera: eyes, tie, rims and headset tell the variants apart at 1x. The arm tips sit below the eye dots.
- Engine: the three.js render of the exported glb matches the Blender render.

## 6. Skill records used (step 4)
- `knowledge.style-low-poly` (resolved, `skill/resolve-style-low-poly.txt`): "spend geometric detail on the contour".
  Adapted: most of the budget goes to the dome rows and the arm outline, and little goes to the flat sides.
- `knowledge.style-cel-shaded` (resolved): limited bands. Kit's 2-band toon is kept.
- `recipe.mesh-orientability-check` (in `skill/design-context.txt`): the open hem is checked for consistent winding.
- Coverage gap: the catalog has no record for a character arm join or a sheet ghost (`skill/search-ghost.txt`).
