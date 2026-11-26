# Ghostie blockout: measurements and read (Viet Tran, 2026-11-25)

- Question: does a centred tie under a collar read as a mouth at the real game camera?
- Setup: a copy of v5 with only the body-map changes (`ready.md`).
- Camera: three.js r170, 26 m follow camera, pitch 42°, yaw 20°, 1.6 px outline, the same lineup as v5 (`ingame.html` `renderLineup`).

## Measured on screen, 1x (1600x900 frame; y grows downward)

Source: `ingame_report.json` `eyeVsArm`.
- Eye bottom: the lowest eye-dot vertex on screen.
- Collar top, knot top and V point: the body-map landmarks (y 166, 170, 258) on the tie mesh. They are stored in `acc_tie` extras and projected through each ghost's float node.
- The tie, glasses and headset ghosts share the same body positions, so all 3 rows are measured. Only the tie ghost shows the tie.

| Ghost | Eye bottom y | Collar top y (Δ) | Knot top y (Δ) | V point y (Δ) | Arm-tip gap below eye centre |
|---|---|---|---|---|---|
| grass, tie | 432.0 | 436.1 (+4.1) | 436.5 (+4.5) | 445.7 (+13.7) | 7.8 |
| grass, glasses | 460.5 | 464.4 (+3.9) | 464.8 (+4.3) | 474.1 (+13.6) | 6.7 |
| grass, headset | 462.3 | 465.7 (+3.4) | 466.1 (+3.8) | 475.5 (+13.2) | 5.0 |
| path, tie | 430.9 | 434.9 (+4.0) | 435.4 (+4.5) | 444.6 (+13.7) | 7.8 |
| path, glasses | 459.3 | 463.2 (+3.9) | 463.7 (+4.4) | 473.0 (+13.7) | 6.8 |
| path, headset | 461.2 | 464.6 (+3.4) | 465.0 (+3.8) | 474.3 (+13.1) | 5.0 |

Δ is pixels below the eye bottom.

**Fact:** below the eye *centre* (grass tie ghost, centre y 430.1): collar 6.0 px, knot 6.4 px, V point 15.6 px. The Illustrator's estimate was 6.5 / 7.0 / 17.0 px (`../sketch/body-map.md` D). The real render is close to the estimate, slightly tighter.

**Fact:** the whole tie is about 9.6 px tall at 1x and sits 4 px under the eye dots, centred between them.

## Triangles

Measured in three.js (`ingame_report.json` `visibleTris`); this is a blockout, so there is no gate:

| Variant | Triangles |
|---|---|
| tie | 556 |
| glasses | 568 |
| headset | **656, over the 600 cap** |

The headset is over because it now has 2 cups and a full band (`build_report.json`). The final model would need a cheaper cup or band.

## My read (Opinion)

**Yes. The centred tie reads as a mouth with a tongue out at the game camera.**
- **`crops/tie-ghost-gamecam-x9.png`** (left ghost, grass and path, ×9):
  - The collar's dark ink edge makes a short horizontal line under the eyes, which reads as a lip line.
  - The lilac tie hangs below it as a rounded tongue shape.
  - The collar wings themselves are white on white and vanish.
- **`lineup-grass-crop-x3.png`, `lineup-path-crop-x3.png`:** the same read, "surprised face, tongue out".
- **`lineup-grass-crop-x1.png`:** at the size the player sees, a lilac dot centred under the eyes, like an "o" mouth.
- **`front-variants.png`** (card size): the tie reads as a tie under a collar. So the problem only shows at the game camera. The top-down view folds the 4 px gap between eyes and collar into the face zone.

Root reason (Opinion): any mark centred within about 5-15 px under the eye dots at 26 m lands in the mouth zone (BMGD's v2 finding, `../../../acceptance/ghostie/v2/bmgd.md`). The collar's ink line makes it worse, because it draws the mouth line itself.

## Other observations

- **Headset:** at card size (`front-variants.png`) the band over the crown is seen edge-on and is hard to see. The 2 cups read on the eye line. At 26 m (`lineup-grass-crop-x3.png`, right ghost) the band shows as an arc with a cup on each side.
- **Glasses:** they sit on the new eye line and read as rims at both sizes (`front-variants.png`, middle ghost in the lineups).
