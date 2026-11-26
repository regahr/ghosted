# Juno v1: screen measures at the game camera (Viet Tran, 2026-11-26)

Set-up (= Brett v1, Dot v1, Ricky v1, ATS v1): three.js r170, 26 m, pitch 42, yaw 20, fov 26, 1600x900, 1.6 px outline,
y down. Juno's root is turned 15 deg (net yaw 5), as Kit and the rest. Source: `ingame_report.json` (made by
`shoot_ingame.mjs`); blockout: `blockout/ingame_report.json`. Face numbers: `face_report.json` (made by
`make_sheets.py`). Method (= Brett): each character alone on flat magenta, no contact shadow, same camera; the box
counts every non-background pixel, so the ink outline is in it. The scale is set at Kit's own spot.
Lineup spots (mine, cheap to change): grass (-1.95, 4.85), path (-1.75, 1.6). Two earlier grass spots touched Ricky,
then Dot; one earlier path spot touched Brett. These are clear (`lineup-grass-crop-x3.png`, `lineup-path-crop-x3.png`).

## Scale (chair call 1: 1.0 x Kit, COUNTING the puff; Kit = 75 px)
| Step | H (m, sole to puff top) | At Kit's spot (grass / path) | Ratio | Width |
|---|---|---|---|---|
| blockout | 1.12 (sketch estimate) | 75 / 75 px | 1.000 | 43 px |
| final, first | 1.12 | 76 / 77 px | 1.013 / 1.027 | 43 px |
| test | 1.095 | 75 / 75 px | 1.000 | - |
| **final** | **1.10** | **75 / 75 px** | **1.000 / 1.000** | 41 / 42 px |

- **Fact:** the final puff is rounder than the blockout's (8 x 4 rings, not 6 x 2), so it added 1-2 px at H 1.12.
  H 1.10 gives 75 px on both grounds. 1 unit = 3.333 mm (`juno_build_report.json`).
- **Fact:** at her own spots she is 77 px (grass, nearer the camera) and 76 px (path).
- **Fact:** landmarks on screen, grass, rest (y px): puff top about 557, chin 588, tie 611, hem 622, feet 623
  (`ingame_report.json` `lineup-grass.juno`).

## Forehead band and hair against the eyes (bible "Art rule: no fringe"; chair call 6)
Mask renders `_lineup-*-hairmask*.png`: hair AND the hairline ink AND the strand lines red, brows orange, eye ink
blue, mouth ink green, teeth cyan, hull black, the rest white. Band = skin rows from the lowest red pixel to the top
brow pixel, per brow column (ink counted as hair).

| Lineup | Expression | Forehead band (min / median / max, columns) | Hair in the eye columns above the eye top | Lowest side hair above the eye top |
|---|---|---|---|---|
| grass | rest, laugh, talk | **6 / 6 / 7 px** (8 columns) | +10 px | **+10 px** |
| grass | dry (one brow up) | 5 / 7 / 7 px (4) | +10 px | +10 px |
| grass | writing (head down 14) | 5 / 6 / 6 px (5) | (eyes are lids) | - |
| path | rest, laugh, talk | **5 / 5 / 6 px** (3 columns) | +9 px | **+9 px** |
| path | dry | 5 / 5 / 7 px (7) | +9 px | +9 px |
| path | writing | 5 / 5 / 6 px (5) | - | - |

- **Fact:** the band is 5 px or more in every column, every expression, both grounds (rule: 4 px). The sketch
  hairline (y 64 at the centre) is kept; no raise was needed (Brett needed one).
- **Fact:** the side hair stays above the eye line and drops only behind the ear; its lowest pixel beside the face is
  9-10 px above the eye top. Only strand lines are ON the hair; nothing hangs on the forehead or the temples.
- Proof: `crops/gamecam-face-mask-*-grass.png`, `crops/gamecam-face-mask-*-path.png` (x6, colour and mask, with the
  hair-low and eye-top lines); `gamecam-face-x3.png` (x3, colour and grey, all expressions, both grounds).

## The mouth at 1x (chair call 6: no beard, moustache or goatee read)
| Lineup | Mouth | Dark px (box) | Luma: mouth / skin round it | Gap below the eye bottom |
|---|---|---|---|---|
| grass | rest smile (closed line) | 1 px (1 x 1) | 60 / 164 | 4 px |
| grass | laugh (Ricky style) | 6 px (6 x 2) | 45 / 154 | 4 px |
| grass | talk (Ricky style) | 3 px (3 x 1) | 38 / 162 | 4 px |
| grass | dry (smirk line) | 0 px | - | - |
| path | rest smile | 1 px (1 x 1) | 59 / 152 | 3 px |
| path | laugh | 5 px (6 x 1) | 52 / 151 | 5 px |
| path | talk | 2 px (4 x 1) | 40 / 154 | 3 px |
| path | dry | 0 px | - | - |

- **Fact:** no mouth makes a dark band wider than 6 px or taller than 2 px, and every mouth sits 3-5 px under the eyes,
  in the face centre. The teeth band does not resolve at 1x (0 cyan pixels): at 1x the laugh is a small dark mark.
- **Opinion:** no beard, moustache or goatee read in any expression (`gamecam-face-x3.png`). The laugh reads as a
  small open mouth, the same Ricky style Rega accepted on Brett.
- **Fact, weak:** the rest smile and the dry smirk do NOT resolve at 1x (0-1 px). At the game camera her face is
  brows and two eyes. I tried a thicker smile line (4.8 units): still 2 px at 1x and too heavy at card size, so it is
  back at 3.6 (selfcheck weak point 1). The sketch's own 1x estimate was 5.1 x 0.8 px, so it was sub-pixel there too.

## Read (Opinion)
- Colour: a dark round puff with a thin red ring, a peach face with brows and eyes, a dark-brown hourglass with an
  apricot apron front, a red pocket, a white cup in front, navy legs. New in the family; apart from Brett (red wedge,
  white sleeves, blond, green ring) at a glance (`lineup-grass-crop-x3.png`, `lineup-path-crop-x3.png`).
- Grey: a dark puff and a dark hourglass round a mid-light apron and a white cup (`lineup-*-grey-crop-x3.png`).
- At rest the tie line at the waist is hidden by the hands and the cup; it shows in the hand-over and wave beats
  (`gamecam-beats-x3.png`).
