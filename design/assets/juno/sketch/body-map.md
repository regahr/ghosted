# Juno the barista body map v1 (Illustrator, 2026-11-26)

Picture: `body-map.png`. Source: `src/juno.py` (`LM`, the half outlines, the marks, `model`), `src/build.py`
(`body_map`, `lm3d`, `face_check`). Numbers at the game camera: `src/_tmp/bodymap.json`. Brief:
`design/acceptance/juno/brief.md`. Front-view units: puff top y 10, sole y 340, axis x 150.

## A. Proportions (front, upright, symmetric)
- Head = top of the puff (y 10) to the chin (y 154) = 144 units. Figure = 330 units = 2.29 heads. Without the puff
  (hair cap top y 52): 2.82 heads (Kit 2.71, Ricky 2.67, Brett 2.53, Dot 2.27). The puff makes her the "big top" of
  the humans; her body is Kit's height.
- Skull 108 wide, 96 tall (y 58-154). Hair cap 118 wide, top y 52, slicked flat to the head.
- Puff: 72 wide, 60 tall, 64 deep; centre y 40, 18 units behind the head axis (top-back of the crown).
- Body: an HOURGLASS (one revolved outline, `BODY_HG`). 28 wide at the neck (y 158), 120 at the shoulder (y 186-196),
  82 at the apron tie (y 238, the pinch), 134 at the hem (y 290-294). Depth 0.8 of the width.
- Legs below the hem: X +-20, radius 13, y 288-326. Shoes y 324-340, toes forward.
- Size (Fact, `build.py` calibration, Brett / Dot / ATS method): 1.0 x Kit = 75 px facing the camera (net yaw 5),
  puff included. The tile measures 75 x 43 px. 1 u = 3.41 mm: about 1.12 m to the puff top, 0.98 m to the hair cap
  (Kit 0.977 m). Viet's blockout sets the real scale.

## B. Landmarks
- Hairline: high and clean. y 64 at the centre, curving down to y 88 only at the head sides, in front of the ears
  (x 99 / 201), above the eye top (y 95.5). The hair is pulled straight back: two ink strand lines ON the hair sweep
  up to the puff. Nothing hangs on the forehead or down the temples.
- Brows: ink arcs y 84-89. Forehead band = hairline y 64 to brow top y 84-86.
- Eye line y 104. Eyes: ink ovals (6.5 x 8.5) at x 132 and 168, each with a row 23 glint.
- Ears: on the eye line at the head sides (x 96 and 204).
- Cheeks: row 6 ovals at x 126 / 174, y 121 (card read only; they vanish at 1x).
- Mouth zone x 138-162, y 122-140. Rest: a closed smile line (calm). Laugh and talk: Ricky style, a filled ink mouth
  with a white (row 23) teeth band along the top edge (`bible.md` "Art rule: mouths"). Dry: a one-sided smirk line
  and one brow up. Writing: eyes down (lid arcs).
- Chin y 154. Neck: skin cylinder (half-width 14) from the chin into a round neckline at y 162.
- Shoulder joint (arm root): x 96 and 204, y 186. Sleeves rolled to the elbow: a brown sleeve, a brown cuff ball at
  the elbow, then a skin forearm and a ball hand.
- Waist y 238 (the apron tie). Hem y 294.

## C. Attachment points
- **Puff (row 25):** on the head axis, top-back of the crown (centre y 40, z -18). A child of the head.
- **Scrunchie (row 7):** a ring (radius 22, tube 5) where the puff meets the cap, y 62. Child of the head.
- **Apron bib (row 6):** front only, from the chest (y 198) down to the tie, 44-54 wide; two straps from its top
  corners up to the neckline either side of the neck (x 139-161).
- **Apron skirt (row 6):** front only, from the tie (y 242) to the hem, 78 wide at the top, 116 at the hem.
- **Pocket (row 7):** on the skirt apron, centred, y 254-274.
- **Apron tie (row 7):** a cord round the waist at y 238, over the apron. The **bow and two tails sit at the BACK,
  centred** (where a real apron ties).
- **Cup (row 23, ink text):** held, never fixed to the body. Rest: centred in front of the apron at y 224, both
  hands round it. Hand over: on her right palm. Wave: in her left hand. Write: up at the chest in her left hand,
  leaning 10 deg back toward her.
- **Marker (row 7):** in her right hand, only in the writing beat.
- Every accessory is where the real thing sits. Nothing moved to dodge the camera.

## D. Game-camera check (26 m, pitch 42, net yaw 5 as in the lineups, 1.6 px outline)
- Method (Fact): one projection draws the views, the tiles and the dots (`src/build.py` `cam_png`, `gamecam_marks`,
  `face_check`). 74.97 px per metre is from `assets/kit/ingame.html` L156.
- Landmarks at 1x, px from the feet point (Fact, `bodymap.json`; up is negative): puff centre -60.0; scrunchie -55.2;
  hairline centre -46.3; ears -46.1 / -44.5 (they sit back on the head, so pitch 42 lifts them on screen); eyes
  -36.4 / -35.9; mouth -31.6; neck -29.4; bib -18.6; tie -13.5; cup -12.7; hem +0.4.
- **Forehead band (Fact, `face_check`):** hairline edge to brow top = 6.4 px (left brow column), 6.7 px (centre),
  6.4 px (right brow column). Rule: 4 px or more. In the writing beat (head down 14 deg): 6.1 / 6.3 / 6.1 px.
- **Temples (Fact):** the lowest side hair is 7.1 px above the eye top, outside the eye columns.
- **Mouth (Fact):** the closed smile is 5.1 x 0.8 px, 2.9 px under the eyes. The laugh is 7.2 x 2.2 px, 2.1 px
  under the eyes.
- **Read (Opinion, `crops/bm-gamecam.png`, `crops/sheet-facecheck.png`):** a dark round puff with a thin red ring,
  a clear peach forehead, two eyes, a small smile; a dark-brown hourglass with an apricot apron front, a red line at
  the waist, a white cup in front; navy legs. No beard read: the smile is a short thin line, and the laugh is a
  small dark mouth with a white top edge, lighter than a beard band.

## E. Notes for the 3D build
- See `notes.md` "Notes for the 3D builder" for the triangle split and the joins.
