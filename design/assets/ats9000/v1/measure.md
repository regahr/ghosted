# ATS-9000 v1: screen measures at the game camera (Viet Tran, 2026-11-26)

Set-up (= Ricky v1): three.js r170, 26 m, pitch 42, yaw 20, fov 26, 1600x900, 1.6 px outline, y down. The ATS root
is turned 15 deg (net yaw 5 to the camera: it faces the camera, chair call 1).
Source: `ingame_report.json` (`lineup-grass`, `lineup-path`), made by `shoot_ingame.mjs`; blockout:
`blockout/ingame_report.json`.
Method (= Ricky): each character rendered alone on a flat magenta background, no contact shadow, same camera and
position as the lineup; the box counts every non-background pixel, so the ink outline is included.

## Scale (brief: 1.21 x Kit, target 1.21 x 75 = 90.75 px)
| Step | H (m) | Where | Kit px | ATS px | Ratio |
|---|---|---|---|---|---|
| blockout | 1.25 | path lineup spot / grass spot | 75 | 93 / 93 | 1.24 / 1.24 |
| **final** | **1.22** | **path lineup spot** (Kit's depth) | **75** | **91** | **1.213** |
| final | 1.22 | Kit's own spot (grass and path) | 75 | 90 | 1.200 |
| final | 1.22 | grass lineup spot (2.7 m nearer the camera than Kit) | 75 | 93 | 1.240 (perspective) |

- **Fact:** 1.25 m (the sketch estimate) gave 93 px, 2 px over. 1.22 m gives 90-91 px at Kit's depth, the nearest
  whole pixel to 90.75. The width is 63-66 px.
- **Fact:** on the grass lineup the ATS stands at (-3.9, 5.3), 2.7 m nearer the camera than Kit, so it shows 93 px
  there. The scale is set at Kit's depth, as for Ricky.
- **Fact:** turned to yaw 20 (not facing), the box is 101 px tall, because the stamp block then hangs toward the
  camera (`lineup-grass-turned` in `ingame_report.json`).

## The neck (brief: "the neck must show at the game camera")
Mask render `_lineup-*-neckmask.png`: rings red, core green, screen blue, slot yellow, hull black, rest white.
Centre column, top to bottom (grass, from y 561; K = ink hull, R = ring, W = grey, . = edge blend):
`KKKKKKKKKKKKK W . K . K RR K RR K . WWWW...`

| Lineup | Screen bottom (px) | Head grey under the screen (px) | Dark neck band (px) | Neck width (px) | Grey body between neck and slot (px) | Slot (px) |
|---|---|---|---|---|---|---|
| grass | 575 | 1-2 (y 574) | **9** (y 576-584) | 12 | 14 (y 585-598) | 3 (y 599-601) |
| path | 504 | 1-2 (y 503) | **8-9** (y 504-512) | 13 | 14 (y 513-526) | 3 (y 527-530) |

- **Fact:** the neck shows as a dark band 8-9 px tall and 12-13 px wide, with 4 px of red ring pixels in the centre
  column; the green core never shows at 1x (the hull and the rings cover it).
- **Fact:** only 1-2 px of grey head separate the dark screen from the dark neck band at 1x.
- **Fact:** the eyes are about 6 px tall (eye top 563 to bottom 569 on grass); the screen is about 42 x 16 px.

## The neck read (open risk, sketch note 1) - honest
Proof: `crops/gamecam-neck-x3-grass.png`, `crops/gamecam-neck-x3-path.png`, `crops/gamecam-neck-x6-grass.png`,
`crops/gamecam-neck-x6-path.png` (colour, grey and the mask), 1x: `crops/gamecam-neck-1x-*.png`.
- **Opinion: yes, it reads as a mouth.** The body crown cuts the lower edge of the dark neck band into a round
  curve, so under the screen it is a dark half-disc, flat on top and round below. With the two cream eyes right above
  it, at x3 and x6 it reads as a wide open smiling mouth (a "D" turned on its side), and the slot lower down reads as
  a second, closed mouth. At 1x it is a dark blob just under the eyes, and the face read is "eyes + open mouth".
- **Opinion:** the ring structure does not show at the game camera; it shows on the cards only.
- I did not try a new design (brief "Open risk"). Options for Rega are in `selfcheck.md`.
