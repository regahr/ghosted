# The Panel: body map v1 (Illustrator, 2026-11-26)

Picture: `body-map.png`. Code: `src/panel.py` (model, all numbers below), `src/build.py` (renders, face check).
Units: 1 u = 1/300 m (3.33 mm, as Juno v1). H = height above the floor. z = toward the player (front view).
Each person is drawn in Juno's front frame (sole y 340) and lifted DH = 90 u onto a chair behind the table.

## The set (world)
| Item | Size / place | Source |
|---|---|---|
| Table | 600 x 30 x 180 u = 2.0 x 0.1 x 0.6 m; top at H 220 = 0.733 m = 0.75 x Kit 0.977 m | BMGD hint `seats/bmgd.md` L45; chair call `brief.md` L30 |
| Table body | a front panel (hides the legs) and two side panels: a "panel" desk | mine |
| Seats, left to right | Culture Fit x -200, Whiteboard x 0, the box x +200 | mine |
| Torso axis | z -140; the torso front sits at the table back edge (z -90) | mine |
| Chairs | seat H 146, back z -192 (part of the table mesh; hidden at the game camera) | mine |
| The box | 100 x 90 x 80 u = 0.33 x 0.30 x 0.27 m, on the table top, z -40 | mine |
| Kit in the lineups | 0.7 m in front of the table front edge (z +300), x -40 | mine |

## The people (Juno front frame, y down)
- **Proportions:** the Juno head (skull y 58-154 = 96 u = 0.32 m, 108 wide), the size of Kit's head (0.977 / 2.71 =
  0.36 m). At the game camera: 21.1 px from cap top to chin vs about 20 px for Kit by the same measure (`body-map.png` E).
- **Seated height:** shoulders H 244 (24 u = 8 cm above the table), chin H 276, cap top H 378 = 1.26 m.
- **Head set (rest):** chin up 8 deg (attentive). At pitch 42 this keeps a skin gap between the mouth and the chin
  line (see `notes.md`, "Face check"). Nod: -8 (rest) to +6.
- **Eyes:** eye line y 104 (H 326), eyes x 132 / 168. **Ears:** on the eye line at the head sides (x 96 / 204).
- **Hairline:** high and clean: y 64 at the centre, y 86 at the sides in front of the ears. Nothing on the forehead,
  nothing beside the eyes.
- **Mouth zone:** x 138-162, y 117-135 (5 u higher than Juno's). Rest: a closed line. Grin / talk: Ricky style.
- **Neck:** chin y 154, neck opening y 158-162.
- **Shoulder joints:** x +-56 (Culture Fit: soft, round), x +-60 (Whiteboard: square).
- **Arms at rest:** the elbow rests on the table (H 230, z -78), the forearm lies on the top, the hands meet at
  z -26 in front of the torso.
- **Below the table:** lower torso, thighs, shins and shoes (hidden at the front and at the game camera).

## Attachment points
| Accessory | Where it sits | Who |
|---|---|---|
| Headband (row 12) | over the crown from ear to ear, behind the hairline (z -16) | Culture Fit |
| Bow (row 12) | centred on the crown, y 46 (two lobes + a knot) | Culture Fit |
| Bun (row 25) | low, at the nape (y 128, z -54); hidden at the front | Culture Fit |
| Blouse V (row 12) | the neck opening down to y 190 (fill, no ink edge) | Culture Fit |
| Flat-top (row 25) | a flat block on the skull, y 38-60, z -46..+34; its front edge is 4 u above the hairline, ON the skull | Whiteboard |
| Glasses (ink) | two rims on the eye line, the bridge, arms back to the ear points | Whiteboard |
| Shirt V + collar (row 8) | the neck opening (fill, no ink edge) | Whiteboard |
| Pocket (row 23) + 2 pens (rows 21, 9) | his left chest (viewer's right), y 190-206 | Whiteboard |
| Marker (row 23, cap row 21) | his RIGHT hand (viewer's left): lies on the table at rest, upright for the click, forward for the point | Whiteboard |
| Icon decal (row 12) | centred on the box front, 0.82 of the face; swaps: camera-off / dark / muted | the box |

## Pivots (motion)
- Head nod and tilt: at the chin (y 154), tilt pivot 6 u higher.
- Lean in: about the elbow line (local H 140, z -10); the box leans about its bottom front edge.
- Whiteboard's arm: shoulder, elbow, wrist; the marker is held in the ball hand.

## Game camera check (`body-map.png` E: 26 m, pitch 42, net yaw 5, 1x = 0.25 px per u)
- Every landmark dot lands on its feature in the game-camera view (eyes, ears, shoulders, bow, flat-top, icon).
- Forehead band at 1x: 6.2 / 6.6 / 6.2 px (both people; rule: 4 px or more). Side hair is 6.2 px above the eye top.
- The flat-top front edge is 1.05 px above the hairline: it reads as hair on top, not as a fringe.
