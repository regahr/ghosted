# Brett v1: screen measures at the game camera (Viet Tran, 2026-11-26)

Set-up (= Dot v1, Ricky v1, ATS v1): three.js r170, 26 m, pitch 42, yaw 20, fov 26, 1600x900, 1.6 px outline, y down.
Brett's root is turned 15 deg (net yaw 5), as Kit, Ricky, Dot and the ATS. In-game state: rest arms, chin up 10 deg.
Source: `ingame_report.json` (`lineup-grass`, `lineup-path`), made by `shoot_ingame.mjs`; blockout:
`blockout/ingame_report.json`. Grin and side-hair numbers: `grin_report.json`, made by `make_sheets.py`.
Method (= Ricky, ATS, Dot): each character alone on a flat magenta background, no contact shadow, same camera; the box
counts every non-background pixel, so the ink outline is included. The scale is set at Kit's own spot.
Lineup spots (mine, cheap to change): grass (-3.45, 4.4), path (-3.2, 0.1). Two earlier grass spots touched the ATS
and then a Ghostie; this one is clear (`lineup-grass-crop-x3.png`).

## Scale (chair call 1: 1.05 x Kit WITHOUT the halo; Kit = 75 px, target 78.75 px)
| Step | H (m, sole to swoop top) | At Kit's spot, no halo (grass / path) | Ratio | With halo | No chin-up |
|---|---|---|---|---|---|
| blockout | 1.23 | 77 / 78 px | 1.027 / 1.040 | 92 / 93 px | 77 / 77 px |
| final | 1.25 | 80 / 80 px | 1.067 | 94 / 95 px | 79 / 79 px |
| **final** | **1.235** | **79 / 79 px** | **1.053 / 1.053** | 93 / 93 px | 78 / 78 px |

- **Fact:** 79 px is the nearest whole pixel to 78.75. Width 53 px. 1 unit = 3.812 mm (`brett_build_report.json`).
- **Fact:** the halo is hidden for the measure by scaling its bone to 0 (`ingame.html` `pose({ noHalo })`). It adds
  14 px on top.
- **Fact:** at his own spots he is 81 px (grass, nearer the camera) and 76 px (path, 4.5 m to the left).

## Hair against the eyes, the forehead band, the side hair (Rega's no-fringe rule, ts 1795658703.410809)
Mask render `_lineup-*-hairmask.png`: hair AND the hairline ink and the part red, brows orange, open-eye ink blue,
grin line green, teeth cyan, halo yellow, hull black, the rest white.

| Lineup | Eye top | Lowest hair in the eye columns | Gap | Forehead band (skin rows from hair edge to brow top, per brow column) | Lowest side hair (outside the eye columns) | Side hair above the eye top |
|---|---|---|---|---|---|---|
| grass | 520 | 511 | **+9 px** | **min 5, median 6, max 8 px** (7 columns) | 512 | **+8 px** |
| path | 365 | 357 | **+8 px** | **min 4, median 5, max 5 px** (5 columns) | 358 | **+7 px** |

- **Fact:** with the sketch hairline (y 62) the band was 4 px while the hairline ink counted as skin. I raised the
  front hairline to y 56 (temples 74-81, still above the ear top 83) and set the swoop root up 6 and back 4
  (`build_brett.py` `HAIRLINE`, `WAVE3`). Then the band, ink counted as hair, is 5-8 px (grass) and 4-5 px (path).
  The path value sits on the 4 px floor.
- **Fact:** the side hair stays above the eye line at the temples and drops only BEHIND the ear (hairline 79 at the
  ear column, 81 just behind it, then 106-132 to the nape). Its lowest pixel is 7-8 px above the eye top, outside the
  eye columns.
- **Fact:** no ink strand lines on the front of the hair; the only marks are the hairline ink edge, the part (above
  y 53, partly under the swoop) and the swoop's own outline.
- Proof crops: `crops/gamecam-face-hair-grass.png`, `crops/gamecam-face-hair-path.png` (x6, colour and mask with the
  hair-low and eye-top lines), `crops/gamecam-face-x3-grass.png`, `crops/gamecam-face-x3-path.png` (x3 face),
  `crops/gamecam-face-x3-grey-*.png`, `crops/gamecam-face-1x-*.png`.

## The grin at 1x (chair call 5)
| Lineup | Box (w x h) | Teeth px / luma | Line px / luma | Skin round it | Eye ink | Gap to the eye bottom |
|---|---|---|---|---|---|---|
| grass | 17 x 4 px | 18 / 210 | 4 / 70 | 176 | 38 | 0 px |
| path | 13 x 4 px | 13 / 211 | 1 / 60 | 175 | 40 | 1 px |

- **Fact:** the teeth are LIGHTER than the skin (210 vs 176); the smile line under them is dark but only 1-4 px wide
  at 1x. There is no dark bar under the eyes.
- **Opinion:** it reads as a white toothy grin with the corners up, not a moustache or goatee
  (`crops/gamecam-face-hair-grass.png` x6, `crops/gamecam-face-x3-grass.png`, `gamecam-beats-x3.png` "rest").
  The honest limit: at 1x the grin touches the eyes (0-1 px gap), and the ink line mostly drops out, so the grin is a
  light crescent rather than "teeth over a line". The line reads at x3 and at card size (`expressions.png`).
- **Fact:** the no-chin-up test (`crops/gamecam-nocarry-x3.png`, `ingame_report.json` `hair_no_carry`): grin gap
  1 px (0 with the chin-up), forehead band 7-8 px (5-8 with the chin-up: the tilt brings the swoop down on screen).
  So in this 3D build the chin-up does not open the grin more; it is kept because chair call 4 asks for it (smug
  carriage). Opinion: it costs 2 px of forehead on grass and still passes the 4 px floor.

## The halo
- **Fact:** grass 26 x 16 px, path 24 x 14 px; an open ellipse with the ink hull round it (`crops/gamecam-rest-x3.png`).
- **Fact:** after the chin-up carriage the ring's up axis is 0.000 deg from world up; the head's is 10.0 deg
  (`brett_build_report.json` `carry_halo_up_vs_world_up_deg`). The ring centre moves 97 mm back with the head.

## Landmarks on screen (grass lineup, y in px, rest)
| Halo | Swoop / hair top | Lowest hair (eye cols) | Brow top | Eye top | Eye bottom | Grin | Feet |
|---|---|---|---|---|---|---|---|
| 482-497 | about 498 | 511 | 516 | 520 | 524 | 524-527 | 575 (box bottom, with ink) |

## Read (Opinion)
- Colour: a green ring over a blond roll, a peach face with two eyes and a white grin, a red wedge with a white V
  and white sleeves, navy legs. He is the tallest human in the row (`lineup-grass-crop-x3.png`, `lineup-path-crop-x3.png`).
- Grey: light hair, light V and sleeves on a mid-grey wedge, dark legs; Kit is mid-grey too, but the ring, hair and
  white sleeves tell them apart (`lineup-grass-grey-crop-x3.png`).

## Mouth pass (2026-11-26): the grin at 1x after the Ricky-style mouths
| Lineup | Box (w x h) | Dark mouth px / luma | Teeth px / luma | Skin round it | Gap to the eye bottom |
|---|---|---|---|---|---|
| grass | 13 x 4 px | 25 / 33 | 2 / 207 | 181 | 1 px |
| path | 12 x 4 px | 26 / 40 | 2 / 180 | 180 | 1 px |
- **Fact:** at 1x the mouth reads as a dark shape; the teeth band is about 2 px. Proof: `gamecam-mouths-x3.png`.
  The hair, forehead and side-hair numbers above are unchanged by this pass (`grin_report.json`).
