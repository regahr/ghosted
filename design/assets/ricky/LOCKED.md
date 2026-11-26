# Recruiter Ricky is locked (v1)

Rega's acceptance: card 3, option 1 (Slack C0CHA2A1DM1, ts 1795624795.450479). v1 is accepted as it is.

The game uses these files from `assets/ricky/v1/`:
- `ricky.glb`, with 2 meshes:
  - `body`, skinned, with the bones for the hop and the phone pose;
  - `decals`.
- The swap parts are `mouth_grin` and `mouth_o`.
- `ricky_toon.json`, and the toon and outline set-up in `ingame.html`.

## The numbers (`v1/ricky_build_report.json`, `ingame_report.json`, `measure.md`)
- **Triangles:** 1,392 of 1,400.
- **Height:** 1.18 m world. That gives 79 px against Kit's 75 px at the game camera, a ratio of 1.053.
- **Hair:** the lowest hair sits 10-11 px above the eye top at the game camera, with no fringe (Rega, ts
  1795622664.391049).
- **Blender vs three.js:** mean difference 1.25-1.36/255.

## Design source
- The sketch: `assets/ricky/sketch/`, direction A, the bell jacket.
- The chair calls: `acceptance/ricky/chair-calls.md`. The accent is row 10 lilac, and a drained Ricky becomes the
  headset Ghostie.

## Known limits accepted with v1 (`v1/selfcheck.md`, and the card)
- The headset band stands off the head, and reads like an antenna in the side view.
- At the game camera, the dark grin can read as a beard.
- The jaw and hands show facets at 2x.
- There are small ink ticks at the shirt V and the sleeve.
- In the -60° close view, the grin pokes past the cheek.
- There are two in-between frames to check in the game build: the drain swap (arms are still present at step 3), and
  the arm swinging out half-way into the phone pose.

## What the game build must do
- **Hop:** squash only on the bounce, as Kit does.
- **Phone pose:** bone animation from rest to the hand on the right cup.
- **Drain:** the suit colour lerps through rows 17, 11, 27 and 16. The legs, shoes, mic and tie fade with their ink.
  He scales to 0.62 and floats, then the headset Ghostie (`assets/ghostie/LOCKED.md`) swaps in.
- Set `transparent = true` for the fades.

## Asset files (the real 3D assets, local on this machine)
- **Blender source:** `design/assets/ricky/v1/ricky.blend`
- **Game file (glTF binary):** `design/assets/ricky/v1/ricky.glb`
- **Build script** (it rebuilds the model from nothing in Blender 4.3): `design/assets/ricky/v1/build_ricky.py`
- These files live only on this machine. The folder is not a git repo and is not pushed or backed up anywhere yet.
