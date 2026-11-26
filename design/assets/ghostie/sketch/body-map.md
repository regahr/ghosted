# Ghostie body map v2 (Illustrator, 2026-11-25)

Picture: `body-map.png`. Source: `src/ghost.py` (`LM`), `src/camera.py`, `src/build.py`.
Brief: `design/acceptance/ghostie/bodymap-brief.md`. Front-view units: crown y 36, hem cusps y 301.

## A. Explore (council 1b; illustrator `references/workflow.md` Phase 2)
8 thumbnails at the game camera: eye line 150 (v5), 134, 118, 104 x neck line 48 or 64 under it.
**Pick: eye 118, neck +48.** Reason (Opinion): the face sits high (eyes 47 % down the ghost at the camera,
v5 56 %), the collar stays above the arm roots, and the crown keeps room for the headset band. 104 crowds the
crown; +64 pushes the tie into the arm and hem zone.

## B. Proportions and landmarks (front, upright, symmetric)
- Head = crown to neck line = 130 units. Whole body = crown to lowest hem lobe = 280 = 2.15 heads. Width at the
  arm roots 208 (1.6 heads); arms reach 280 tip to tip. v5 size and dome kept.
- Eye line y 118 (v5 150). Two tall ink ovals at x 124 and 176.
- Ear points: on the eye line at the side edges, x 56 and 244. No ear shapes.
- Mouth zone: x 132-168, y 136-160. Always empty.
- Neck line y 166: a small centred collar (2 flat wings, span 46, inside the outline). Collar and knot sit below
  the mouth zone.
- Chest y 186-258 (the tie lies here). Arm roots y 190-260, soft curve on top and below. Hem: 5 soft lobes; 3 seen
  from the front, a notch centred at the back.

## C. Attachment points
- Headset: band centred over the crown (top at x 150, y 46), one cup on each ear point.
- Tie: centred on x 150, hangs from the collar at the neck line; knot top y 170, V point y 258.
- Glasses: on the eye line, one round rim on each eye.

## D. Game-camera estimate (26 m, pitch 42, yaw 20, 1.6 px outline)
- Method (Fact, `src/camera.py`): a round body built from the front outline; marks projected on its surface;
  outline and arms on the widest slice. Scale 0.142 px per unit (ghost 41.6 px tall at 1x, as v5).
- Model check (Fact): v5 eyes measure 56 % down the ghost in `v5/lineup-grass-crop-x3.png` (ink bbox y 33-158,
  eye pixels y 99-107). The model on the v5 eye line gives 55 %.
- v2 at 1x, below the eye centre: eye bottom 1.5 px, mouth zone 3.2-5.9 px, collar top 6.5 px, knot top 7.0 px,
  V point 17.0 px.
- **Opinion (risk):** at the game camera the collar and knot sit only about 1 px below the mouth zone. In my
  estimate the centred tie reads like a tongue under the eyes (`crops/bm-D-gamecam.png` tile 3,
  `crops/sheet-gamecam.png`). This is the conflict the brief foresaw (tie centred vs no mouth). Viet's real render
  decides it; the brief says the chair then stops and shows Rega.
- **Opinion (risk):** with yaw 20 the arm_R tip lands about 1 px under the eye centre (arm_L about 8 px under).
  The rest pose droops arm_R more in game; Viet's render must confirm "tips below the eyes".
