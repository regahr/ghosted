# Brett Bullet-Points is locked (v1, after the mouth pass)

Rega's acceptance: ts 1795659740.072339, "1", after the mouth pass (ts 1795659302.700869).

The game uses these files from `assets/brett/v1/`:
- `brett.glb`, with 2 non-swap meshes:
  - `body`, skinned, which includes the halo on its own bone;
  - `decals`.
- 12 swap parts: eyes, brows, mouths, thumb and fingers.
- `brett_toon.json`, and the toon and outline set-up in `ingame.html`.

## The numbers (`v1/brett_build_report.json`, `measure.md`)
- **Triangles:** 1,338-1,386 per beat, of 1,400.
- **Height:** 1.235 m. That is 79 px against Kit's 75 px (1.053 times) without the halo, and 93 px with it.
- **Face:** the forehead band is 4-8 px, and the side hair sits 7-8 px above the eye top. No fringe.
- **Blender vs three.js:** mean difference 1.07-1.11/255.

## Design source
- The sketch: `assets/brett/sketch/`, direction A, "the wedge".
- The chair calls are in `acceptance/brett/brief.md`:
  - a row 7 vest;
  - a row 2 #OpenToWork halo with an ink edge, kept level;
  - the chin up 10° in game.
- The mouths are in Ricky's style (`bible.md`, "Art rule: mouths"). The collar wing ink is removed.

## Known limits accepted
- In the side card view, the brow and grin tips poke past the face outline. This does not show in game.
- The bullets mouth is a small dark shape at 1x, as Ricky's is.
- Facets show at 2x, and the V-neck rib lines have small gaps.
- The vest renders more orange under the warm light.

## What the game build must do
- **Idle:** hands on hips, with a chest puff.
- **The Like:** thumb up and a wink.
- **Bullets:** fingers pop up 1, 2, 3.
- **Halo:** it stays level while the head nods.

## Asset files (the real 3D assets, local on this machine)
- **Blender source:** `design/assets/brett/v1/brett.blend`
- **Game file (glTF binary):** `design/assets/brett/v1/brett.glb`
- **Build script** (it rebuilds the model from nothing in Blender 4.3): `design/assets/brett/v1/build_brett.py`
- These files live only on this machine. The folder is not a git repo and is not pushed or backed up anywhere yet.
