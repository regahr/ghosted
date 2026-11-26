# The Panel v1: screen measures at the game camera (Viet Tran, 2026-11-26)

Set-up (= Juno v1): three.js r170, 26 m, pitch 42, yaw 20, fov 26, 1600x900, 1.6 px ink hull. The set is turned
15 deg like the cast (net yaw 5). The camera follows Kit (target = Kit, 0.5 m up, 0.5 m back). Kit stands 0.7 m in
front of the table front edge, x -40 u (`sketch/body-map.md`). Spots (mine, cheap to change): grass set (3.05, 5.15),
Kit (3.18, 6.15); path Kit at his own spot (1.30, 0.10), set (1.17, -0.90).
Sources: `ingame_report.json` (from `shoot.mjs`), `measure.json` (from `make_sheets.py`), `panel_build_report.json`.
Masks (`_mask-*.png`): hair + hairline ink red, brows orange, eye ink blue, mouth ink green, teeth cyan, skin white,
the rest grey, hull black.

## Scale
| Item | Value | Source |
|---|---|---|
| Table top | 0.733 m (220 u) = 0.75 x Kit 0.977 m | `build_panel.py` (TT = sketch `panel.py` TABLE_TOP) |
| Table front edge on screen, top to floor | 40.8 px; Kit 0.977 m upright = 54.9 px; ratio 0.743 (0.75 less 3 % depth) | `ingame_report.json` `_mask-grass` `panel.set`, `kitTop/kitBot` |
| Kit bbox | 75 px tall, grass and path (= Juno v1) | `measure.json` `kit_*` |
| Seated head, cap top to chin | CF 23.2 px, WB 23.3 px (both grounds) | `measure.json` `idle_*` |
| Kit head, the same vertical measure | about 20.2 px (0.36 m x 54.9 / 0.977) | Kit report numbers |

- **Fact:** the heads are 23.2 px; the sketch estimate was 21.1 px (`sketch/notes.md` Size). They are Kit-sized
  heads (chair call 1) and about 15 % bigger than Kit's head on screen, because they sit 0.7 m behind Kit and higher,
  with the chin-up 8 set. **Opinion:** they read as Kit-sized at 1x (`lineup-grass-crop-1x.png`).

## Forehead band (rule: 4 px or more) and side hair
Band = skin rows from the lowest hair pixel (hairline ink counted as hair) to the brow top, per brow column:
min / median / max (columns).

| Render | CF | WB |
|---|---|---|
| grass idle (talk) | 5 / 6 / 6 (4) | 6 / 7 / 7 (5) |
| path idle | 5 / 6 / 7 (5) | 6 / 7 / 7 (5) |
| grass CF nod (+6, lowest frame) | 6 / 6 / 6 (2) | 6 / 7 / 7 (5) |
| grass CF tilt | 4 / 5 / 5 (4) | 6 / 7 / 7 (5) |
| grass all lean in | 6 / 6 / 6 (4) | 6 / 7 / 7 (7) |

- **Fact:** 4 px or more in every column of every render. Lowest: CF tilt, 4 px (at the rule).
- **Fact, side hair:** the lowest hair pixel beside each eye is 8-11 px above the eye top (all renders); the hair in the
  eye columns is 8-11 px above the eye top. Nothing hangs on the forehead or at the temples.
- **Fact:** the WB flat-top front edge is on the skull above the hairline; the band under it is 6-7 px (red block,
  then skin, in `crops/face-mask-grass-wb.png`).
- Proof: `gamecam-face-x3.png` (x3: colour, grey, mask), `crops/face-mask-*.png` and `crops/face-*.png` (x6).

## The mouth at 1x (no beard read; chair call 3: idle in game = TALK)
| Render | Mouth | Dark px | Teeth px | Gap under the eyes | Light rows under the mouth (min, median) | Luma mouth / skin |
|---|---|---|---|---|---|---|
| grass idle, CF talk | 3 x 1 | 2 | 0 | 2 | 2, 2 | 19 / 186 |
| grass idle, WB talk | 3 x 1 | 3 | 0 | 2 | 2, 2 | 19 / 186 |
| path idle, CF talk | 3 x 1 | 3 | 0 | 2 | 2, 2 | 19 / 186 |
| path idle, WB talk | 2 x 1 | 2 | 0 | 2 | 2, 2 | 19 / 185 |
| grass CF grin, rest head | 5 x 1 | 5 | 0 | 1 | 2, 2 | - |
| path CF grin, rest head | 5 x 1 | 5 | 0 | 1 | 2, 2 | - |
| **grass CF grin at the nod's lowest frame (+6)** | 1 x 1 | 1 | 0 | 1 | **0, 0** | 19 / 182 |
| **path CF grin at the nod's lowest frame** | 5 x 1 | 2 | 0 | 0 | **0, 0** | - |
| grass lean, CF / WB talk | 1 x 1 / 3 x 1 | 1 / 3 | 0 | 2 | 2 / 1-2 | 19 / 185 |
| grass rest lines (card faces) | 0 x 0 | 0 | - | - | - | - |
| grass CF tilt (smirk line) | 0 x 0 | 0 | - | - | - | - |

- **Fact:** idle, lean and the grin at the rest head keep 1-2 light rows between the mouth and the chin line.
- **Fact, FAIL:** at the lowest frame of the CF nod (chin down +6) the grin meets the chin line (0 rows). See
  `selfcheck.md` item 7 for the options.
- **Fact:** the teeth band does not resolve at 1x (0 cyan px), as on Juno v1. The rest lines and the CF smirk are
  sub-pixel at 1x (0 px).
- How I got there (Fact): the blockout mouths (sketch position) sat ON the chin line at 1x, 0 rows under
  (`blockout/blockout-sheet.png`, faces). Chin-up 12 and 16 deg and a fuller jaw gave 0 rows too (tested, not kept).
  What worked: the mouths 4 u higher than the sketch, the chin ink at 0.35 weight, the grin 0.8 as tall.
