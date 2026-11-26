# Auntie Dot is locked (v1, after no-fringe pass 2)

Rega's acceptance: ts 1795659821.728169, "autie dot 3, lock auntie dot" (option 3: it is fine now).

The locked state is `assets/auntie-dot/v1/`. It has the strand lines back and the side hair raised behind the ears.
- An earlier state is in `v1-pre-fringe/`: the original v1.
- Another earlier state is in `v1-fringe-a/`: pass 1, with no strands.

The game uses these files:
- `dot.glb`, with 2 non-swap meshes, `body` and `decals`, both skinned;
- the swap parts: eyes open and happy, mouth smile and talk;
- the `card` prop;
- `dot_toon.json`, and the toon and outline set-up in `ingame.html`.

## The numbers (`v1/dot_build_report.json`, `measure.md`)
- **Triangles:** 1,340 at rest and 1,362 in the card beat, of 1,400.
- **Height:** 0.98 m. That is 68 px against Kit's 75 px (0.907 times) at the game camera.
- **Hair:** the side hair sits 8-11 px above the eye top. No hair in the eye rows.
- **Blender vs three.js:** mean difference 1.19-1.21/255.

## Design source
- The sketch: `assets/auntie-dot/sketch/`, direction A, the "cottage loaf".
- The chair calls are in `acceptance/auntie-dot/brief.md`:
  - a row 11 cardigan and a row 23 white bun;
  - her old headset in row 27, worn round her neck;
  - 0.9 times Kit.

## Known limits accepted
- The jaw, hands and bun show facets at 2x.
- The talk arm reads as a straight tube.
- There are small ink marks at the sleeve joins and the ear in 3/4.
- The hair renders warm under the light.
- The smile is faint at 1x.
- The band ends show a small tab on the cups.

## What the game build must do
- **Sway:** ±4°, with the head lagging 2°.
- **Talk:** the head tilts 8° and a hand comes up.
- **Card:** she hands over a Skill card with a 2° lean.
- Emil should check the timing of the talk arm half-way, where it passes in front of the chest.

## Asset files (the real 3D assets, local on this machine)
- **Blender source:** `design/assets/auntie-dot/v1/dot.blend`
- **Game file (glTF binary):** `design/assets/auntie-dot/v1/dot.glb`
- **Build script** (it rebuilds the model from nothing in Blender 4.3): `design/assets/auntie-dot/v1/build_dot.py`
- These files live only on this machine. The folder is not a git repo and is not pushed or backed up anywhere yet.
