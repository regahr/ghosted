# ATS-9000 3D build brief (chair, 2026-11-26)

Rega picked direction B with a neck (ts 1795628417.229379). The chair chained the 3D straight after the B sheet
(thread ts 1795628461.631429). Rega is the gate: no seat rounds. The chair checks at 2x, then the sheet and the 3D go
to Rega on one card.

## References (match these)
- Sketch v2: `assets/ats9000/sketch/ats-sheet.png`, `body-map.png`, `body-map.md` and `notes.md`. The profiles are in
  `sketch/src/ats.py`.
- Chair calls: `acceptance/ats9000/chair-calls.md`:
  - it faces the camera;
  - the stamp rests at 45°;
  - red ink appears only as text on the CV prop;
  - bevel the box edges about 0.02 m.
- The working pipeline to reuse: `assets/ricky/v1/` (`build_ricky.py`, `render_ricky.py`, `ingame.html`,
  `shoot_ingame.mjs`, `make_sheets.py`). Also the locked Kit, Ghostie and Ricky for the lineups.

## Before you model
- Write `assets/ats9000/v1/ready.md`, `direction.md` and the skill tool outputs.
- Build a blockout first, at the real game camera next to Kit. Set the scale so the robot is 1.21 times Kit on screen,
  facing the camera, measured the same way as Ricky.

## Requirements
- **Budget:** 900 visible triangles or fewer, at most 3 non-swap meshes: the static body, the stamp arm, and the
  screen. If it is tight, use 12-sided neck rings.
- **Shape:** the B turnaround, with a monitor head on a bellows neck (3 ink rings on a grey core), a mailbox-arch body,
  a front CV slot with a lip tray, ink treads, the stamp arm on the robot's left (one hinge), and the antenna on the
  right top corner.
- **The neck must show at the game camera,** so measure it in px in `measure.md`.
- **Screen:** one decal or UV on the head front, with 5 states: idle, reading, found, not fit, loading. The scan line
  scrolls. Never angry.
- **Colours:** palette rows 18, 22, 12, 13 and 23, plus 21 only on the CV prop text, with a neutral shade.
- **Motion:**
  - the stamp rests at 45°, winds up to 140°, and slams to 0°;
  - a CV slides into the slot;
  - the tread hubs spin and the belts scroll;
  - the antenna ball blinks;
  - optional: a small idle bob of the bellows.
- **Open risk (sketch note 1):** at the game camera, the dark neck band may read as a second smiling mouth above the
  slot. Show it honestly in a x3 crop. If it reads as a mouth, say so. Do not try a new design on your own.

## Deliverables (in `assets/ats9000/v1/`)
- the turnaround and `hero.png`;
- `stamp.png`, `slot.png` and `screens.png`;
- the silhouettes and the grey render;
- the in-game render and the compare;
- the lineups on grass and path, in colour and grey, with x3 and 1x crops, next to Kit, Ricky and the Ghosties;
- `compare-sketch.png`;
- `crops/`;
- `measure.md` and `selfcheck.md`. A visible fault is never a PASS.

## Rules
- No blind iterations.
- Run a tiny Blender test first.
- Work only in `assets/ats9000/v1/`.
