# ATS-9000 body map v1 (Illustrator, 2026-11-26)

Picture: `body-map.png`. Source: `src/ats.py` (profiles and landmarks), `src/build.py` `body_map()`.
Front-view units: x axis 150, ground y 340, y down. 1 u = 3.85 mm (camera calibration, see `notes.md`).
Z + = the robot's front. "Left" and "right" are the ROBOT's sides.

## A. Proportions (1 head-height = the head box, 88 u = 0.34 m)
| Part | Units | Heads | Metres |
|---|---|---|---|
| Total, ground to antenna ball top | 310 | 3.52 | 1.19 |
| Hopper (head top to mouth) | 44 | 0.50 | 0.17 |
| Head box | 88 | 1.00 | 0.34 |
| Neck | 14 | 0.16 | 0.05 |
| Body | 106 | 1.20 | 0.41 |
| Treads | 36 | 0.41 | 0.14 |
| Head width | 168 | 1.91 | 0.65 |
| Body hem width | 148 | 1.68 | 0.57 |

Big head on a short flared body, on a dark base: the same toy logic as Kit (big head, dark legs) and Ricky (bell
jacket). Kit is 0.98 m; the ATS is 1.19 m, the gatekeeper a bit bigger than the hero (brief "Size").

## B. Landmarks (front view y; `src/ats.py` `LM`, L35)
| Landmark | y | Note |
|---|---|---|
| antenna ball top | 30 | gold ball r 10 |
| HOPPER MOUTH | 52 | the CV "mouth": rim r 58, rim 5 u, inside ink |
| head top = hopper base = antenna base | 96 | |
| screen (face zone) | 110-172 | x 84-216, inset ink panel on the head front |
| eye line | 136 | 2 cream pills, x 122 and 178, 16 x 26 u |
| scan line rest | 162 | cream, 3 u, x 92-208; sweeps y 116-166 |
| chin = neck top | 184 | |
| body top (shoulders) | 198 | |
| STAMP PIVOT | 224 | hub axis, on the X axis |
| TREAD LINE | 304 | body bottom = tread top |
| axle line | 322 | hub centres on the outer tread faces |
| ground | 340 | |

Face zones: the screen is the whole face. There is NO mouth on the face or on the body front. The hopper on the head
top is the mouth (brief "Body map"). The body front is plain on purpose: a light name plate under the screen read as a
grin at 90 px, so it was dropped (Opinion, my read of the first build; the option stays in
`model({"plate": True})`).

## C. Attachment points and joins
| Part | Where | Join (for the 3D) |
|---|---|---|
| Screen | head front, Z 56, x 84-216, y 110-172 | flat inset panel; eyes + scan line are a texture with a V scroll / state swap |
| Hopper | turned funnel centred on the head top: base r 36 at y 96 (a 6 u straight collar), mouth r 58 at y 52 | fixed, same mesh as the head |
| Antenna | socket on the head top, robot's RIGHT corner: x 82, Z -24; stalk tilts out to x 68, y 46; ball r 10 | fixed socket; the stalk may wobble (spring, optional) |
| Stamp arm | hub: cylinder on the X axis, r 15, robot's LEFT side, y 224, x 216-244; bar x 244-258, y 220-302; block x 240-264, Z -27..27, y 296-326; rubber ink 8 u | ONE hinge at the hub axis. Rest 22 deg forward, wind-up 150, slam 0 |
| Neck | ink block, x 124-176, y 182-200, Z -30..30 | fixed; the head does not turn |
| Treads | 2 ink belts, x 66-106 and 194-234, y 304-340, Z -58..74 (tank nose 74 u ahead) | fixed to the body; belt texture scrolls, hub decals on the OUTER faces spin |
| Back | 3 vent lines on the head back; a hatch outline on the body back | decals, so front and back never get mixed up |

The stamp arm and the antenna are on opposite sides by design (a diagonal balance). The arm is on the robot's LEFT so
it faces the camera at yaw 20 and in the 3/4 view. Clearances: the block is 6 u clear of the tread (x 234 vs 240); the
antenna ball is 14 u clear of the hopper rim in the front view (ball edge x 78 vs rim x 92), more in 3D because it sits at Z -24.

## D. Camera check (game camera 26 m, pitch 42)
`body-map.png` E: the same landmarks projected at yaw 20 and yaw 5 (x5). At both yaws:
- the hopper mouth reads as a dark oval on top: the "mouth" is the first dark shape you see;
- the screen and both eyes stay visible under the hopper; the eyes sit about a third down the figure;
- the stamp pivot is on the camera side;
- the antenna base and ball stay clear of the hopper;
- the tread line and both tread noses show; the base is the darkest mass.
