# Auntie Dot body map v1 (Illustrator, 2026-11-26)

Picture: `body-map.png`. Source: `src/dot.py` (`LM`, the half outlines, `model`), `src/build.py` (`body_map`,
`lm3d`, `hair_gap`). Numbers at the game camera: `src/_tmp/bodymap.json`. Brief: `design/acceptance/auntie-dot/brief.md`.
Front-view units: top of the bun y 40, sole y 340 (300 units). Axis x 150.

## A. Proportions (front, upright, symmetric)
- Head = top of the bun to the chin = 132 units. Whole figure = 300 units = 2.27 heads. Kit is 2.71 and Ricky 2.67,
  so Dot is shorter and rounder, in the same toy-pawn family.
- Without the bun: hair top y 70 to chin y 172 = 102 units (the skull is 98 tall, 112 wide).
- Body: a pear ("cottage loaf"). 32 wide at the neck (y 176), 120 at the arm root (y 206), 164 at the belly
  (y 280), hem y 316. Depth 0.85 of the width.
- Legs: hem to ankle y 326, then shoes y 324-340, toes forward.
- Size (Fact, `build.py` calibration, ATS method): 0.9 x Kit 75 px = 67.5 px on screen, facing the camera.
  That gives 1 u = 3.34 mm, so about 1.00 m from the top of the bun to the sole. The tile measures 68 x 50 px
  (`measure_px`). Viet's blockout sets the real scale (Ricky: estimate 67 px, real 66 px).

## B. Landmarks
- Hairline: soft waves, y 88-89 at the centre, y 112-116 at the temples. Strands sweep up and back into the bun.
  Nothing lies on the forehead.
- Eye line y 126. Eyes: ink ovals (6.5 x 8.5) at x 132 and 168, each with a row 23 glint. Brows: thin ink arcs at
  y 109-113.
- Ears: on the eye line at the head sides (x 93 and 207), in the open. The headset is NOT on them.
- Mouth zone: x 134-166, y 140-160. Rest: a closed warm smile (ink line). Talk: an open "D" mouth (ink fill).
  Happy: the smile with closed "^ ^" eyes.
- Chin y 172. Neck: short, a skin cylinder (half-width 17) from the chin into the body top at y 180-190.
- Neck line y 180: the headset band rests here, on the shoulder slope.
- Collarbones: the cup centres, x 117 and 183, y 194.
- Shoulder joint (arm root): x 90 and 210, y 206 (X +-52 inside the body). The sleeve comes out of the body here.
- Chest: two row 23 buttons at y 214 and 238 on the placket (x 150).
- Hands (rest): folded on the belly, hand balls at X +-18, y 262, 9 units in front of the surface.
- Belly (widest) y 280. Pockets y 272-298, at x 108-134 and 166-192.

## C. Attachment points
- **Bun:** centre (X 0, y 60, Z -18): on the crown, a little behind. Radii 25 x 21 x 23. Top y 40.
- **Headset band (row 27):** round the NECK. An open ring at the neck line (y 180), 38 wide and 33 deep (half
  sizes), behind the neck. The back point sits 3 units lower (y 183), on the nape. It spans 224 deg round the back,
  then each end runs forward and a little down over the collarbone into the top of its cup.
- **Headset cups (row 27):** ONE ON EACH COLLARBONE, at the band ends. Centre X +-33, y 194, 5 units in front of
  the body surface. Discs 25 across, 13 thick. The flat face looks forward and 22 deg up.
- **No mic boom.** It is an old headset that she no longer uses for calls.
- **Skill card:** in her right hand (viewer-left in the front view), card centre 22 units above the hand, a little
  in front. 30 x 42 x 3 units, row 23, with a row 13 Copium disc on the face. The card edge is row 24 in 3D.
- Every accessory is where the real object sits. Nothing moved to dodge the camera.

## D. Game-camera check (26 m, pitch 42, net yaw 5 as in the lineups, 1.6 px outline)
- Method (Fact): the same projection draws the views, the tiles and the dots (`src/build.py` `cam_png`,
  `gamecam_marks`). 74.97 px per metre comes from `assets/kit/ingame.html` L156.
- Landmarks at 1x, in px from the feet point (Fact, `bodymap.json`), y up is negative:
  - bun centre -55.1; ears -40.9 / -39.3; hairline centre -39.9;
  - eyes -31.9 / -31.4; mouth -27.5 (about 4 px under the eyes);
  - band back point -34.7. It is above the eye line on screen, so the head hides it, as it hides a real neck band.
    The band sides show beside the chin;
  - cups -20.9 / -19.9 (11 px under the eyes, 7 px under the mouth: under the chin, not hidden by it);
  - top button -14.4; folded hands -1.6; hem +2.9.
- **Hair vs eyes (Fact, `hair_gap`):** the hairline in each eye column is 6.8 px ABOVE the eye top at 1x. The hair
  never crosses the eyes. The bun is 23 px above the eyes.
- **Opinion:** at the game camera Dot reads as a white bun on a white swept dome, a peach face with two dots and a
  smile, two lilac discs under the chin, and a purple pear with two hand dots. The lilac reads as a ring at the neck
  (brief L24).

## E. Notes for the 3D build (3 non-swap meshes, brief L27)
- One possible split (Opinion): (1) body + neck + sleeves + hands + legs + shoes as one skin with vertex colours or
  atlas cells; (2) head + hair + bun + ears; (3) the headset. The card is a swap or prop mesh, shown only in the card
  beat.
- Joins: continuous skin from the body into each sleeve at the arm root (no shoulder ball, unlike Ricky).
