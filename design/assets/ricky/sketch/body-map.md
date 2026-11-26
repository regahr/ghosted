# Recruiter Ricky body map v1 (Illustrator, 2026-11-25)

Picture: `body-map.png`. Source: `src/ricky.py` (`LM`, the half outlines), `src/build.py` (`body_map`).
Brief: `design/acceptance/ricky/sketch-brief.md`. Front-view units: top of the quiff y 36, sole y 340;
304 units = 1.00 m. Axis x 150.

## A. Proportions (front, upright, symmetric)
- Head = top of the quiff to the chin = 114 units. Whole figure = 304 units = 2.67 heads. Kit is 2.71
  (`assets/kit/build_report.json` L141), so Ricky stays in Kit's toy-pawn family.
- Height 1.00 m = 1.05 x Kit's 0.95 m (`assets/kit/LOCKED.md`; `seats/viet-tran.md` L63).
- Head 112 wide (x 94-206). Jacket 136 wide at the shoulders, 148 at the hem: a soft bell.
- Legs: jacket hem y 268 to ankle y 318. Shoes y 320-340, toes forward.

## B. Landmarks
- Eye line y 98. Eyes: ink ovals at x 132 and 168, each with a row 16 glint.
- Ears: on the eye line at the head sides (x 94 and 206). They are small, and the headset cups cover them.
- Mouth zone: x 125-175, y 110-134. It holds a wide grin (row 22 with row 16 teeth). In drain step 1 it shrinks
  to a small "o". In step 2 it is gone, because a ghost never replies (`bible.md` L30).
- Neck: hidden. Chin y 150 = the neck line. A row 16 shirt collar rings the neck, and the collar wings sit at
  y 150-167.
- Shoulder joint (arm root): x 84 and 216, y 176. Here a suit-coloured shoulder ball is the join. The sleeve runs
  to the wrist (y 234), then a row 16 cuff, then the hand.
- Hands: skin balls centred at y 246, beside the jacket hem.
- Shirt V: from the collar to the V point at y 238. Jacket button at y 250.

## C. Attachment points
- **Headset band:** centred over the crown, top y 32. It sits in the ear plane, 6 units behind the head centre,
  and passes behind the quiff.
- **Headset cups:** one on EACH ear point. The cup centres are x 89 and 211 (X +-61), y 100. In the front view
  each cup sits on the head's side edge.
- **Mic boom:** from the right cup (viewer-left in the front view) along the cheek. The mic ball ends at the
  mouth corner (x 106, y 126, forward 36).
- **Tie:** centred on x 150. The knot top is at y 160, under the shirt collar at the neck line (y 152). The V point
  is at y 232, inside the shirt V (y 238).
- All accessories are on the real object's place. No accessory moves to dodge the camera.

## D. Game-camera check (26 m, pitch 42, yaw 20, 1.6 px outline)
- Method (Fact, `src/ricky.py` `render`, `src/build.py` `cam_png`): every front outline is lifted onto a round
  body, and the same projection draws the views, the dots and the tiles. 75 px per metre comes from
  `assets/kit/ingame.html` L156 (900 / (2 x 26 x tan 13 deg)). It matches `kitPx` 55 for a 1 m pole
  (`ghostie/v7/ingame_report.json` L41), because 75 x cos 42 = 55.7.
- Scale (Fact): this metric estimate gives Ricky 67 px tall. The real Kit is 72 px in the same lineup
  (ink bbox y 424-496 in `ghostie/v7/lineup-grass.png`). Its top is 13 px above its own 1 m pole top
  (`kitTop` y 437, L25-27). So the tiles are drawn at the screen target, 1.05 x 72 = 76 px (`cam_scale`,
  factor 1.134). See notes.md, open item 1.
- Landmarks at 1x, at the target scale, in px from the feet point (Fact, `gamecam_marks`):
  - eyes y -42.4 / -40.1;
  - mouth -36.3, about 5 px under the eyes;
  - knot top -29.6, about 12 px under the eyes;
  - tie V -12.3;
  - cups -54.1 / -46.3. From above, the cups sit behind the face, so they read at the top of the head;
  - band top -65.1;
  - hands -23.2 / -13.1;
  - hem -5.9.
- **Opinion:** at the game camera Ricky reads as a near-black bell with a lilac ring on top, and a white V with a
  lilac stripe. The grin is small but visible. The eyes and grin sit lower in the head than on Kit, because the
  camera looks down on the quiff.

## E. Drain mapping (Ricky -> Ghostie, same metres)
| Ricky | Ghostie (`assets/ghostie/sketch/body-map.md`) |
|---|---|
| eye line y 98 | eye line y 118 |
| cups on the ear points | cups on the ear points (x 56 / 244) |
| band centred over the crown | band centred over the crown |
| shirt collar at the neck line y 152 | small collar at the neck line y 166 |
| tie centred, knot top y 160 | tie centred, knot top y 170 |
| tie V y 232 | tie V y 258 |
| jacket hem y 268 | 5 soft hem lobes y 301 |
| grin | mouth zone empty (gone in step 2) |
| legs, shoes, mic, hair | fade in step 1, gone in step 2 (the quiff melts into the dome) |

The Ghostie in the strip uses the locked Ghostie parts (`ghostie/sketch/src/ghost.py`). It is scaled to
0.57 m crown to hem and floats 0.22 m (`ghost_toon.json` `float_rest_m`). The 0.57 m is my estimate
from its 37 px width at 75 px per m.
