# Direction: Juno the barista 3D v1 (Viet Tran, 2026-11-26)

3dviz-pro-max `SKILL.md` steps 1 (intent), 2 (hardest parts first), 4 (construction and joins), 5 (quality targets).
Tool outputs are in `skill/`.

## 1. Intent and visual direction
- What the player sees: the barista at the Job Board Cafe, the Morale heal node. Warm, calm, a little dry. At the game
  camera she must read as **a dark round puff on top, a peach face with two eyes and a small smile, a dark-brown
  hourglass with an apricot apron front, a thin red line at the waist, a white cup in front, navy legs**, about
  1.0 x Kit (75 px) with the puff.
- Shape: "the hourglass" (sketch direction A): round shoulders, pinch at the apron tie, flared hem. New in the family.
- References: only the accepted sheet (`../sketch/juno-sheet.png`), the body map (`../sketch/body-map.png`,
  `body-map.md`) and their Bezier source (`../sketch/src/juno.py`). Kit sets the toon, ink hull and light; Brett v1
  (`../../brett/v1/`) sets the pipeline, the Ricky-style mouths and the no-fringe measures.
- Viewing distances:
  - game camera: 26 m, pitch 42, yaw 20; Juno about 75 px tall at 1x with the puff;
  - card: 900x1200 front, 3/4, side and back; hero 1200x1200; face, puff, cup, hand and join close views; the cup
    alone at card size, where the line must be readable.
- Look: Kit's 2-band toon (neutral grey 178 shade band), Kit's light, the inverted-hull ink outline; flat ink decals
  for the face, the strand lines, the apron edges and the cup text.

## 2. The hardest parts (solved first on the blockout, `blockout/`)
1. **The forehead band at 1x (no fringe).** The hair cap is slicked flat, and the camera looks down 42 deg, so the
   hairline ink can creep toward the brows on screen. Brett needed the hairline raised from 62 to 56 to clear 4 px.
   Juno's sketch gap is hairline 64 to brow top 84 (20 units at about 3.4 mm a unit: less than Brett's 22 units at
   3.8 mm). Measured on the blockout with Brett's mask method (hair + hairline ink red, brows orange), per brow column.
2. **The mouth at 1x.** The rest smile is a thin ink line; at 1x it can drop out or merge into a dark bar. The laugh
   is a filled dark mouth (Ricky style), which can read as a goatee. Measured on the mask: box, luma, gap to the eyes.
3. **The cup changes hands.** Rest: in both hands at the apron. Hand over: on her right palm. Wave: in her left hand.
   Write: up at the chest in her left hand, leaning back 10 deg. One cup cannot follow different bones, so each beat
   has its own cup swap part, built in that beat's pose frame and skinned to the bone that holds it (Brett's thumb
   method). Only one cup is visible at a time.
4. **The cup line at card size inside the budget.** "You are not a PDF." as hand-drawn ink polylines on the cup
   front: strokes as thin strips on the cup surface. About 50 segments, about 100 triangles.
5. **The waist pinch and tie.** The tie must read as a red line at the narrowest point, all the way round, with the
   bow at the back. The tie is a colour band in the body mesh (0 extra triangles) with the bow and tails as small
   layered parts at the back.
6. **The budget:** head, cap, puff, scrunchie, ears, body, bow, arms, legs, shoes, apron decals, face, cup and the
   cup line in 1,400 triangles in every beat.

## 3. Construction (step 4) and join decisions
Units: sketch front-view units, y down, axis x 150 (centred X = x - 150), sole y 340, puff top y 10. 1 unit =
H / 330 m; H (sole to puff top) is set by the blockout measure. Blender Z-up, Juno faces -Y; glTF Y-up.

Nodes: `root > float > bounce > rig` (bones `body_root` at the feet, `torso`, `head` (pivot on the chin, y 154),
`arm_L_up`, `arm_L_lo`, `arm_R_up`, `arm_R_lo`). Skinned meshes `body`, `decals` (non-swap: 2). Swap parts: eyes,
brows, mouths, the four cups (`cup_rest`, `cup_hand`, `cup_wave`, `cup_write`) and the `marker`.

| Join | Decision | Reason |
|---|---|---|
| Hair cap to head skin | **Continuous skin**: one revolved surface; rows above the per-column hairline lie on the sketch `CAP_HALF` surface; the last row thins to the skin AT the hairline; an ink band on the skin carries the edge | Brett and Dot's proven method; no lip over the forehead, so no fringe and no 3/4 skin sliver (chair call 5) |
| Hairline at the ear | Above the ear top at the ear column, then down behind the ear to the nape (y 140) | Body map B; sketch `hair_back` |
| Puff to cap | **Layered**: an ellipsoid half sunk into the crown, top-back | It must stand off as a ball in every view |
| Scrunchie | **Layered**: a low torus where the puff meets the cap | Body map C |
| Ears | **Layered**: small ellipsoids half sunk at the eye line | Body map B |
| Head to neck to body | **Separate parts, sunk**: head closed at the chin; a skin neck tube from inside the head to inside the body top | The head nods 14 deg in the write beat; a sunk neck cannot tear |
| Sleeve to body | **Sunk tube (reads as continuous skin)**: the brown sleeve starts inside the body at the arm root, no shoulder ball outside | Sketch notes: "the sleeve comes out of the body as continuous skin". Welded skin would pinch in the wave |
| Cuff at the elbow | **Rigid ball joint**: a brown cuff ball on the upper-arm bone; the skin forearm starts inside it | Sketch: brown cuff ball at the elbow; cannot pinch at any bend |
| Hand | **Separate ball**, the forearm end sunk into it | Sketch: ball hands |
| Tie | **Colour band in the body mesh** (rows y 234-241), red | 0 extra triangles; it runs all the way round |
| Bow and tails | **Layered**: two flat ellipsoids, a knot and two short tails at the back, on the torso | Body map C: the bow is at the back |
| Apron (bib, straps, skirt, pocket) and the strand lines, neckline, cheeks | **Decals**, projected onto the analytic surface and lifted; the large skirt is a grid strip so it follows the flare | Flat marks need no volume; Brett's lesson: a big fan sinks between rings |
| Legs to body, shoes | **Separate**: leg tubes sunk into the skirt, shoes as ellipsoids, on `body_root` | Feet planted |
| Cup | **Swap part per beat**, skinned to the holding bone | Hardest part 3 |
| Marker | **Swap part** on `arm_R_lo`, write beat only | Body map C |

Poses: bone rotations stored as axis + angle in float space (Brett / Dot / Ricky method), solved in the build with a
two-bone reach to the sketch's hand targets (`juno.py` `model()`). The bind pose has the arms down at the sides; the
turnaround uses the rest beat (cup in both hands), upright and symmetric, as the sketch sheet.

## 4. Triangle plan (cap 1,400 visible)
| Part | Plan |
|---|---|
| Head + hair cap + hairline ink | about 260 |
| Puff (8 x 5) + scrunchie (8 x 4) | about 140 |
| Ears, neck | about 50 |
| Body hourglass (14 columns) with the tie band | about 300 |
| Bow + tails | about 50 |
| Arms: 2 x (sleeve, cuff, forearm, hand) | about 180 |
| Legs and shoes | about 90 |
| Decals: apron, straps, pocket, strands, neckline, cheeks | about 150 |
| Eyes, brows, mouth (swap) | about 70 |
| Cup + lid + line (swap, one visible) | about 150 |
| Total | about 1,390 |

## 5. Quality targets (step 5)
- Card: clean hourglass and puff outline at 2x; no hook, crease or ring at the arm root, cuff or hand; every decal
  seated with ink; the hairline continuous round the head, above the ears and behind them; no skin sliver at the
  forehead edge in 3/4; the bow centred at the back; upright and symmetric at rest; the cup line readable.
- Game camera: 1.0 x Kit in pixels with the puff (75 px); forehead band >= 4 px in every brow column; the side hair
  above the eye top, outside the eye columns; the smile reads as a smile, the laugh as an open mouth, no beard.
- Engine: the three.js render of the exported glb matches the Blender render.

## 6. Skill records used (step 4)
- `knowledge.style-low-poly` (`skill/resolve-style-low-poly.txt`): spend detail on the contour. Adapted: 14 columns on
  the hourglass, 6 sides on the arms and legs, 8 on the puff and the cup.
- `knowledge.layered-decal-surface-handoff` (`skill/resolve-decal.txt`): projection stretches at grazing angles.
  Adapted: the face and apron marks stay near the front; marks are runtime meshes; the big skirt mark is a grid.
- `knowledge.hero-prop-detail-hierarchy` (`skill/resolve-hero-prop.txt`): allocate prop detail by what resolves at
  the nearest approved camera. Adapted: the cup line exists for the card view only; at the game camera the cup is a
  white shape with a lid, so the cup body itself stays 8-sided.
- `knowledge.style-toy-miniature` (`skill/resolve-toy-miniature.txt`): tactile, simplified parts. Adapted: ball hands,
  ball cuff, ball puff, as the family.
- Coverage gap: no catalog record for a prop that changes hands between beats (`skill/search-prop-hold.txt`) or for
  a hair puff join (`skill/search-hair.txt`). The decisions above are my own, from `references/object-craft.md`
  "Choose continuity at the join".
