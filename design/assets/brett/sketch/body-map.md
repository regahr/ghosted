# Brett Bullet-Points body map v1 (Illustrator, 2026-11-26)

Picture: `body-map.png`. Source: `src/brett.py` (`LM`, the half outlines, `model`), `src/build.py` (`body_map`,
`lm3d`, `hair_gap`, `grin_px`). Numbers at the game camera: `src/_tmp/bodymap.json`. Brief:
`design/acceptance/brett/brief.md`. Front-view units: halo centre y 0, swoop top y 16, sole y 340. Axis x 150.

## A. Proportions (front, upright, symmetric)
- Head = top of the swoop (y 16) to the chin (y 144) = 128 units. Figure = 324 units = 2.53 heads. Kit is 2.71,
  Ricky 2.67, Dot 2.27: Brett has the longest body and legs of the humans, so he reads as the older peer.
- Skull 108 wide, 98 tall (y 46-144). Hair cap 118 wide, top y 32 (volume on top).
- Body: a WEDGE (the red sweater vest). 32 wide at the neck (y 150), 148 at the chest (y 188, the widest point),
  72 at the waist (vest hem y 252). Depth 0.64 of the width (flatter than Kit, Ricky, Dot).
- Hips y 246-268 (chinos). Legs at X +-20, radius 14, knee y 298, ankle y 324. Shoes y 322-340, toes forward.
- Size (Fact, `build.py` calibration, Dot / ATS method): the figure without the halo is 1.05 x Kit 75 px =
  78.75 px facing the camera. The tile measures 80 px without the halo and 92 px with it. That gives 1 u = 3.81 mm:
  about 1.23 m to the swoop top and 1.32 m to the halo top. Viet's blockout sets the real scale.

## B. Landmarks
- Hairline: high and clean. y 62 at the centre, y 84-88 at the temples. A side part on his right (viewer-left),
  x 126-131, y 43-63.
- Swoop: one rolled wave (a tube through 5 hand-placed points, smoothed) from the part, up and over to his left.
  Highest point y 16; lowest point y 57 at x 120, above the hairline. Nothing lies on the forehead.
- Eye line y 94. Eyes: ink ovals (6.5 x 9) at x 132 and 168, each with a row 23 glint. Brows: ink arcs at y 73-79.
- Ears: on the eye line at the head sides (x 95 and 205).
- Mouth zone: x 120-180, y 102-126. Rest: the GRIN = a white teeth crescent (row 23, no edge of its own) over an
  ink smile line with the corners up. Talk: an open ink mouth with a teeth band. Wink: the grin with the left eye
  closed. Lost: a wobbly line and worried brows.
- Chin y 144. Neck: skin cylinder (half-width 16) from the chin into the collar.
- Neck line y 152: the open shirt collar (2 white wings), a small skin V (top button open).
- Vest V: white shirt V from the collar to y 198, with an ink rib line each side. Hem rib at y 244-248.
- Shoulder joint (arm root): x 92 and 208, y 176 (X +-56 inside the vest). The white shirt sleeve comes out of the
  armhole here. No shoulder ball.
- Hands (rest): ball hands at X +-76, y 254, beside the hips.

## C. Attachment points
- **Halo (row 2, ink edge):** a level ring floating above the swoop, centred on the head axis. Centre y 0
  (16 units above the swoop top), ring 76 wide x 60 deep (centre line), tube radius 6. No stalk.
  It follows the head (position and roll, as a child of the head) but stays LEVEL when the head nods, so it is
  level in his chin-up carriage. Reason for this place: a halo sits above the crown; the ring round the head
  (direction C) reads as Ricky's headset band.
- **Collar:** on the neck line, centred. No tie (Kit and Ricky wear ties; Brett is the open-collar networker).
- **Thumb (the Like):** a capsule (radius 6, 26 long) from the top of his right fist, pointing up.
- **Fingers (bullets):** 1, 2 or 3 capsules (radius 3, 15 long, 6.5 apart) from the top of his right hand.
- Every accessory is where the real thing sits. Nothing moved to dodge the camera.

## D. Carriage
- In game he holds his chin up 10 deg (a nod about the chin pivot). It is smug, and it turns the grin to the
  camera: without it, at 1x the grin collapses into a mark that reads as a beard (tested; see `notes.md`).
- The model-sheet turnaround stays neutral (nod 0) for the build. The 3D rest pose sets the neck to 10 deg up.

## E. Game-camera check (26 m, pitch 42, net yaw 5 as in the lineups, 1.6 px outline, with the carriage)
- Method (Fact): the same projection draws the views, the tiles and the dots (`src/build.py` `cam_png`,
  `gamecam_marks`). 74.97 px per metre comes from `assets/kit/ingame.html` L156.
- Landmarks at 1x, in px from the feet point (Fact, `bodymap.json`; y up is negative): halo centre -76.4; ears
  -54.9 / -53.1; hairline centre -54.2; eyes -46.9 / -46.3; mouth -41.7; collar -31.9; V point -19.6; hands
  -18.4 / -15.8; hem -13.5.
- **Hair vs eyes (Fact, `hair_gap`):** the lowest hair in each eye column is 5.7 px (left) and 6.2 px (right)
  ABOVE the eye top at 1x. The swoop alone is 8.1 / 10.9 px above. The hair never crosses the eyes.
- **Grin (Fact, `grin_px`):** 14.9 x 4.3 px at 1x, starting 0.1 px under the eyes.
- **Halo (Fact):** centre 29.5 px above the eyes. Opinion: at pitch 42 it shows as an open green ellipse with an
  ink edge over the blond swoop; it reads on the grass (`crops/bm-gamecam.png`, `crops/sheet-lineup.png`).
- **Opinion, read:** a green ring over a blond swoop, a peach face with two eyes and a white grin, a red wedge with
  a white V and white sleeves, navy legs. Nothing green on the body.

## F. Notes for the 3D build (3 non-swap meshes, brief L25)
- One possible split (Opinion): (1) body = vest + neck + sleeves + hands + hips + legs + shoes, one skin with vertex
  colours or atlas cells; (2) head + hair cap + swoop + ears; (3) the halo (a low torus, 8 x 6 segments is enough).
  The thumb and the finger hands are swap meshes for the Like and the bullets beats.
- Joins: continuous skin from the vest armhole into each sleeve (as Dot). The sleeve-to-hand join is a plain ball.
