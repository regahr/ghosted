# Ricky v1: screen measures at the game camera (Viet Tran, 2026-11-25)

Set-up (= Ghostie v7): three.js r170, 26 m, pitch 42°, yaw 20°, fov 26°, 1600x900, 1.6 px outline, y down.
Source: `ingame_report.json` (`lineup-grass`, `lineup-path`), made by `shoot_ingame.mjs`.
Method: each character rendered alone on a flat magenta background, no contact shadow, same camera and position as
the lineup; the box counts every non-background pixel, so the ink outline is included. Kit and Ricky are measured the
same way.

## Scale (brief: Ricky = 1.05 x Kit's on-screen height)
| Step | H (m) | Lineup | Kit px | Ricky px | Ratio |
|---|---|---|---|---|---|
| blockout | 1.00 | grass / path | 75 / 75 | 66 / 66 | 0.88 / 0.88 |
| blockout | 1.19 | grass / path | 75 / 75 | 79 / 79 | 1.053 / 1.053 |
| final | 1.19 | grass / path | 75 / 75 | 80 / 80 | 1.067 / 1.067 (the flat-top band added 1 px) |
| **final** | **1.18** | grass / path | **75 / 75** | **79 / 79** | **1.053 / 1.053** |

- **Fact:** by this method Kit is 75 px (y 424-498). The brief's 72 px is the v7 ink box measured another way
  (`ghostie/v7` notes, y 424-496). Ricky is set by the ratio with one method, so 1.053 is the number that counts.
- **Fact:** 1.05 x 75 = 78.75 px; 79 px is the nearest whole pixel. Ricky is 1.18 m in world units (Kit 0.977 m).
  1.00 m gave only 66 px, so metres alone would have made him smaller than Kit (chair call 1 was right).
- **Fact:** Ricky stands at Kit's depth on the path lineup and 1.3 m nearer the camera on the grass lineup; both
  give 79 px.

## Hair line (Rega ts 1795622664.391049: no fringe)
Mask render (`_lineup-*-hairmask.png`): hair red, eye decals blue, the rest white, the hull black.
| Lineup | Eye top (px) | Eye bottom (px) | Hair lowest, in the eye columns (px) | Hair lowest, anywhere (px) | Gap (px) |
|---|---|---|---|---|---|
| grass | 511 | 516 (geometry) | 501 | 501 | **+10** |
| path | 468 | 472.6 (geometry) | 457 | 457 | **+11** |

- **Fact:** the hair's lowest visible pixel is 10-11 px ABOVE the eye top at 1x, on both lineups. No hair pixel lies
  below that line anywhere on Ricky. Proof: `crops/gamecam-face-hair-grass.png`, `crops/gamecam-face-hair-path.png`
  (x6, with the mask and both lines); the x3 crops `crops/gamecam-face-x3-grass.png`, `crops/gamecam-face-x3-path.png`.
- Front-view hairline in the build: y 63 at the front, 70 at 67.5°, 75 at the ear plane; the brows are y 77-83 and
  the eye top y 88.5 (`build_ricky.py` `HAIRLINE`).

## Landmarks on screen (grass lineup, y in px)
| Eye top | Eye bottom | Collar top | Knot top | Tie V point | Feet (pivot) |
|---|---|---|---|---|---|
| 510.6 | 516.0 | 521.7 (+5.7 under the eyes) | 525.9 (+9.9) | 545.4 (+29.4) | bbox bottom 562 |

## Read (Opinion)
- Ricky reads as a dark bell with a white V and a lilac tie, under a lilac ring with a brown cap; Kit reads mid-grey
  beside him (`lineup-grass-grey-crop-x3.png`, `lineup-path-grey-crop-x3.png`).
- The grin is the darkest mark under the eyes at 1x. At 1x it can read as a beard or moustache
  (`crops/gamecam-face-x3-grass.png`). See `selfcheck.md`.
