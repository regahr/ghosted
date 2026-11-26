# ATS-9000 body map v2: direction B "Mailbox Bot" + neck (Illustrator, 2026-11-26)

Picture: `body-map.png`. Source: `src/ats.py` (profiles and landmarks), `src/build.py` `body_map()`.
Front-view units: x axis 150, ground y 340, y down. 1 u = 3.73 mm (camera calibration, see `notes.md`).
Z + = the robot's front. "Left" and "right" are the ROBOT's sides. v1 (direction A): `../sketch-v1-A/body-map.md`.

## A. Proportions (1 head-height = the head box, 90 u = 0.34 m)
| Part | Units | Heads | Metres |
|---|---|---|---|
| Total, ground to antenna ball top | 334 | 3.71 | 1.25 |
| Head box | 90 | 1.00 | 0.34 |
| Neck (bellows) | 50 | 0.56 | 0.19 |
| Body (crown to hem) | 104 | 1.16 | 0.39 |
| Treads | 36 | 0.40 | 0.13 |
| Head width | 176 | 1.96 | 0.66 |
| Body hem width | 150 | 1.67 | 0.56 |
| Head depth | 68 | 0.76 | 0.25 |

## B. Landmarks (front view y; `src/ats.py` `LM`, L35)
| Landmark | y | Note |
|---|---|---|
| antenna ball top | 6 | gold ball r 10 |
| head top = antenna base | 60 | |
| screen (face zone) | 74-136 | x 80-220, inset ink panel on the head front (Z 34) |
| eye line | 102 | 2 cream pills, x 120 and 180, 20 x 30 u (v1 B: 0.8 x 16 x 26) |
| scan line rest | 126 | cream, 3 u, x 88-212; sweeps y 80-130 |
| CHIN = NECK TOP | 150 | |
| NECK BOTTOM = body crown | 200 | |
| STAMP PIVOT | 224 | hub axis, on the X axis |
| CV SLOT (the mouth) | 240-254 | centre 247; lip tray under it, y 254-262 |
| TREAD LINE | 304 | body bottom = tread top |
| axle line | 322 | hub centres on the outer tread faces |
| ground | 340 | |

Face zones: the screen is the face (eyes + scan line). The CV slot on the body front is the mouth. Rega accepts that it
may read as a grin (`sketch-brief-B.md`). There is no other mouth. The name plate stays off (`chair-calls.md` 4).

## C. Attachment points and joins
| Part | Where | Join (for the 3D) |
|---|---|---|
| Screen | head front, Z 34, x 80-220, y 74-136 | flat inset panel; eyes + scan line are a texture with a V scroll / a state swap |
| NECK | bellows centred on the body crown: grey core r 17, y 146-206 (it runs into the head and the body); 3 INK rings r 26, 8 u tall, at y 155-163, 170-178, 185-193 | fixed (the head does not turn); an optional squash bob on the bellows |
| Slot | ink inset on the body front, Z 50, x 102-198, y 240-254; lip tray y 254-262, Z 44-62 | the slot is a decal or a shallow inset; the lip is part of the body mesh |
| Antenna | socket on the head top, robot's RIGHT corner: x 80, Z -16; stalk tilts out to x 66, y 22; ball r 10 | fixed socket; the stalk may wobble (spring, optional) |
| Stamp arm | hub: cylinder on the X axis, r 15, robot's LEFT side, y 224, x 212-246; bar x 246-260; block x 242-266, Z -27..27; rubber ink 8 u | ONE hinge at the hub axis. Rest 45 deg (chair call 3), wind-up 140, slam 0 |
| Treads | 2 ink belts, x 66-106 and 194-234, y 304-340, Z -58..74 (tank nose) | fixed to the body; the belt scrolls, the hub decals spin |
| Body | mailbox arch: crown y 200, sides from y 240, hem x 75-225 at y 304, Z -50..50 | |
| Back | 3 vent lines on the head back; a hatch outline on the body back | decals, so front and back never get mixed up |

Clearances: the stamp block is 8 u clear of the tread (x 234 vs 242). At wind-up (140 deg) the block sits in front of
the head plane (Z of about 58 vs the head front at 34), so it never clips the head. The antenna stays inside the head
depth (Z -16, head Z -34..34).

## D. Why the head is shallow (the hardest part)
At pitch 42, a ray toward the camera climbs about 0.9 u for each 1 u it moves forward. So the head hides about
0.9 x (head front Z - neck front Z) of the neck top. A head 112 u deep (v1) would hide about 27 u. At 68 u deep
(Z +-34) it hides about 7 u, so about 43 u of the 50 u neck shows. The ink rings make it a dark band between the
mid-grey head and body (5.70:1), which is what reads at 1x (`crops/sheet-gamecam.png`, `crops/bm-gamecam.png`).
