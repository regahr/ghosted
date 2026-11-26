# Gary the pigeon postman: body map v1 (Illustrator, 2026-11-26)

Picture: `body-map.png`. Numbers come from `src/gary.py` (model) and `src/build.py` (camera check). World units: X
right, H up, Z toward the viewer; 1 u = 2.29 mm (standing height 0.488 m = 0.5 x Kit 0.977 m, cap included).

## Proportions
- Standing height to the cap top: 209 u = 0.49 m. Head (cap top to chin) 87 u, so he is 2.40 heads tall.
- Head: a ball, 76 u across, centre H 160, set 14 u forward of the body axis.
- Body: an egg, 116 x 108 x 148 u (W x H x D), centre H 78, tilted 22 deg (chest up, tail end down).
- Tail: a flat fan, 60 x 14 x 68 u, low at the back (centre H 56, Z -82).
- Wings, 2 rigid segments each: the arm is 70 u, the hand is 100 u, and there are 3 finger feathers at the tip.
  Span = 2 x (44 + 70 + 100) = 428 u = 1.03 m = 1.06 x Kit (the brief asks for about 1.0).

## Landmarks
| Landmark | Where (H in u) |
|---|---|
| Cap top | 209 |
| Head top | 198 |
| Cap band, front edge | 188 (cap tilted back 14 deg, so the front edge sits higher) |
| Eye line = ear points | 164. Eyes at x -15 / +15 on the face front, ink ovals with a glint. Ear points at x -37 / +37, under the feathers |
| Beak root | 150 on the face front. A gold cone 34 u long, pointing forward and about 15 deg down, with a cream cere on top |
| Chin / neck | 122. No neck line: a neck blend part with no ink joins the head to the body |
| Wing roots (shoulders) | 106-108, at the body sides (x -47 / +47) |
| Wrist hinge | 70 u along the wing from the root |
| Chest | the front of the egg, about H 100 |
| Belly (bag centre) | 52 |
| Knee / legs | 0-32, gold, x -17 / +17 |
| Feet | gold ovals, H 0-4, forward of the legs |

**Mouth zone:** empty. The beak is the only thing below the eyes. Expressions use the eyes, the lids and the brows
only.

## Attachment points
- **Cap (kepi):** centred on the crown and set back. The band bottom sits 10 u under the head top, and the cap is
  tilted back 14 deg about that point. It has an ink brim at the front and a cream badge on the front of the band.
  It never covers the eyes: at the game camera, the lowest cap pixel is 2.6-2.9 px above the eye top at rest and
  2.4 px above in the sorry tilt.
- **Mail bag:** a 38 x 30 x 15 u satchel on his LEFT belly front, in direction (0.42, -0.42, 0.80) from the body
  centre, 9 u off the surface, turned 24 deg outward. The flap is a swap part (closed, or open with a letter showing).
- **Strap:** one loop that lies on the body surface, in the plane through his RIGHT shoulder and LEFT hip (the plane
  holds the front-back axis). It goes over the shoulder, across the chest to the bag and round the back, like a real
  sash. It is part of the body mesh, and it passes under the folded wing.
- **Envelope socket 1, the beak:** the top edge is held at the beak tip. The letter hangs below the beak, tilted
  35 deg to face up. This is the pose for flying in.
- **Envelope socket 2, the wing fingers:** his RIGHT wing reaches forward and the 3 finger feathers hold the letter in
  front of his chest, below the beak, tilted 38 deg up toward the camera. This is the pose for hold, sorry and yes.
- The envelope is a swap part, and only one socket is used at a time.

## Moving parts and joins (for Viet)
- **Head:** a pivot at the neck (0, 128, 10). It tilts (roll, -14 deg for "sorry") and nods (+6 deg). The cap, beak,
  cere and envelope socket 1 ride on the head.
- **Wings:** a hinge at the root (flap, fold) and a hinge at the wrist (fold, hold). They are rigid, so they need no
  skin across the joint, because the feathers overlap. Folded: the arm runs forward-down and the hand lies back along
  it, with the tips toward the tail.
- **Whole body:** one root for the hop and flight lift, and a pitch of 10 deg nose down in flight.
- **Legs:** stand, or tucked back in flight.

## Camera check (26 m, pitch 42, net yaw 5)
- Standing: 35 x 26 px. Kit is 75 px.
- The eyes are 2.35 px tall, and the cap clears them by 2.6 px or more.
- The beak is 2.9 x 6.4 px and points down. It reads as a beak.
- The landmark dots are in `body-map.png` E, and the px offsets are in `src/_tmp/bodymap.json`.
