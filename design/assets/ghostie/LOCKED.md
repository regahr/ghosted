# Ghostie is locked (v7)

Rega's acceptance: card 2, option 1 (Slack C0CHA2A1DM1, ts 1795620475.864169). v7 is accepted as it is.

The game uses these files from `assets/ghostie/v7/`:
- `ghostie.glb`: 1 skinned body mesh with 3 bones and a `wave` morph target. The swap parts are the eyes,
  `acc_tie`, `acc_glasses` and `acc_headset`.
- `ghost_toon.json`;
- the toon and outline set-up in `ingame.html`.

## The numbers (from `v7/ingame_report.json` and `build_report.json`)
- **Triangles:** tie 716, glasses 774, headset 788. The cap is 800 (checklist amendment 4).
- **Blender vs three.js:** mean difference 0.73/255.
- **Rest arm tips at the game camera:** 4.5 to 6.7 px below the eye bottom (`v7/measure.md`).

## The design source
- Sketch v2 and the body map: `assets/ghostie/sketch/`.
- Rulings: `design/bible.md`, "Ghostie ruling". There is no mouth. The centred tie may read as a tongue in game:
  Rega likes it, ts 1795615890.262169.

## Known limits, accepted with v7 (`v7/selfcheck.md`)
- The dome-to-side join shows small outline steps at 2x.
- The back hem is flatter than in the sketch.
- In the 3/4 view, there is a small near-arm hook and a far-arm crease.
- The side view shows a "v" mark.
- The headset band is faint at the game camera.
- The edge-on headset cups are thin.

## What the game build must do
- **Wave:** drive the `wave` morph target from 0 to 1 (+40°), 2 times, on a soft spring with bounce about 0.2. Check it
  at 0.25x. Never show the wave pose on a card.
- **Float:** the bob runs on the `float` node; the 4° rest lean lives there too.
- **Drain from a recruiter:** set `transparent = true` at run time for any fade.

## History
- 5 Blender passes from a written spec failed, and so did 3 sketch rounds. v6 was built to the sketch, and v7 is v6
  smoothed to 800.
- The retro is in `acceptance/ghostie/retro-viet.md`.
- The lessons became council rules: sketch first, body map, ready check, no blind iterations, and Rega is the gate.

## Asset files (the real 3D assets, local on this machine)
- **Blender source:** `design/assets/ghostie/v7/ghostie.blend`
- **Game file (glTF binary):** `design/assets/ghostie/v7/ghostie.glb`
- **Build script** (it rebuilds the model from nothing in Blender 4.3): `design/assets/ghostie/v7/build_ghostie.py`
- These files live only on this machine. The folder is not a git repo and is not pushed or backed up anywhere yet.
