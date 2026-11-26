# ATS-9000 is locked (v1, direction B with a neck)

Rega's acceptance: card 4, option 1, "accept as is" (Slack C0CHA2A1DM1, ts 1795631210.838989, "i meant 1").

The game uses these files from `assets/ats9000/v1/`:
- `ats.glb`, with 3 non-swap meshes: body, stamp and screen;
- the `tex/` screen states and the scan, hub and belt textures;
- the toon and outline set-up in `ingame.html`.

## The numbers (`v1/ats_build_report.json`, `ingame_report.json`, `measure.md`)
- **Triangles:** 875 of 900.
- **Height:** 1.22 m. That is 91 px against Kit's 75 px (1.21 times) at the game camera, facing the camera.
- **Blender vs three.js:** mean difference 1.29/255.

## Design source
- Sketch v2: `assets/ats9000/sketch/`, direction B, the Mailbox Bot, with a neck (Rega, ts 1795628417.229379).
- Chair calls: `acceptance/ats9000/chair-calls.md`.

## Known limits accepted with v1
- At the game camera, the dark neck band reads as a round mouth under the eyes, and the slot reads as a second mouth.
  This is accepted as part of the look.
- **Fixed (2026-11-26, Rega ts 1795653224.813279, "ok go, all ur pick"):** at 1x the scan line broke into 2 short
  dashes. The cause: the line was 3 u on a 62 u screen, under 1 px at the game camera, so the 0.5 alpha cut-off
  dropped its faint, shrunk parts. The fix is texture-only: the line is now 7.5 u (about 2 px), still cream row 12,
  still under the eyes (`v1/make_textures.py` `SCAN_H`). The alpha cut-off stays. The model is unchanged (875
  triangles, the same meshes). At 1x it is now one continuous line, 1-2 px thick, with no gap from x 12 to 48 in the
  crop. Proof: `v1/crops/scanfix/before-after-x3.png`, and `before-` / `after-` x3 and 1x crops for grass and path.
  The card still reads well: `v1/screens.png`.
- Other limits:
  - the grey reads neutral under Kit's warm light;
  - the antenna ball has 8 facets;
  - the stamp block is rounded, not bevelled;
  - there is a light facet at the head's bottom corners at 2x.

## What the game build must do
- **Stamp:** rest 45°, wind-up 140°, slam 0°.
- **CV slot:** a CV slides into the slot.
- **Treads:** the hubs spin and the belts scroll.
- **Antenna:** the ball blinks.
- **Screen:** 5 states by UV, with the scan line scrolling in V. Never angry.
- **Antialiasing:** turn on edge smoothing (MSAA or FXAA) in the renderer. Without it, the thin scan line on the
  slightly turned screen shows pixel steps. They are visible when zoomed (Rega, ts 1795653511.869429) and read as one
  line at 1x.

## Asset files (the real 3D assets, local on this machine)
- **Blender source:** `design/assets/ats9000/v1/ats.blend`
- **Game file (glTF binary):** `design/assets/ats9000/v1/ats.glb`
- **Build script** (it rebuilds the model from nothing in Blender 4.3): `design/assets/ats9000/v1/build_ats.py`
- These files live only on this machine. The folder is not a git repo and is not pushed or backed up anywhere yet.
