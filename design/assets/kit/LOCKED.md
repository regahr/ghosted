# Kit is locked (v5)

Rega's acceptance:
- Card 1, option 2: "i follow ur pick" (Slack C0CHA2A1DM1, ts 1795598749.600789). This accepted Kit v4 plus the small
  arm fix.
- v5 makes only that arm fix.

Gate results:

| Version | Seats | Result |
|---|---|---|
| v4 | All 5 | PASS (`acceptance/kit/v4/`, plus `bmgd.md` and `lena-park.md`, which carry over from v3) |
| v5 | Viet, Illustrator, Emil re-checked the arm change | PASS (`acceptance/kit/viet-tran.md`, `illustrator.md`, `emil-kowalski.md`) |

The game uses these files: `kit.glb`, `toon.json`, and the toon and outline set-up in `ingame.html`.

Frozen (Emil, `acceptance/kit/emil-kowalski.md`): the arm and the case position (WL, EL, `CASE_OUT`). Do not change them
without a new E1 check.

Chair ruling, 2026-11-25: Viet suggested turning the arm 3-4 degrees further out, to open the front silhouette gap. It is
not done. The reasons:
- Emil owns the pose feel and asked for the arm to be frozen.
- Rega accepted this fix.
- Viet's verdict is that the fist and case still read apart from the body at the 56 px game camera.

## Known limits, carried into the build

- **Silhouette gaps:** the front gap between arm and body is about 1 px, and the 3/4 gap between leg and case is under
  1 px in rows 50-53 (Viet, v5).
- **Head:** the outline shows its facets in close-ups. The budget is spent: 2,480 of 2,500 triangles.
- **Faces:** they cannot be read at the real game camera. The sprout carries the mood there.
- **What the game build must do (Emil):**
  - The sprout must spring toward its target, not snap.
  - The case swings as a pendulum on its handle-top pivot, up to 12 degrees.
  - Squash goes only on `bounce`.
- **Builder notes:** they claimed things the renders did not show, in v2, v3 and v5. v5's claimed gap of "about
  1 px in rows 50-58" is really under 1 px in rows 50-53. Treat builder notes as claims. The seats judge from the
  renders.

## Asset files (the real 3D assets, local on this machine)
- **Blender source:** `design/assets/kit/kit.blend`
- **Game file (glTF binary):** `design/assets/kit/kit.glb`
- **Build script** (it rebuilds the model from nothing in Blender 4.3): `design/assets/kit/build_kit.py`
- These files live only on this machine. The folder is not a git repo and is not pushed or backed up anywhere yet.
