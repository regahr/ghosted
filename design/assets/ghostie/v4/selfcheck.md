# Ghostie v4: self-check (builder, Viet Tran seat)

- These are builder claims; the seats score on their own.
- Rule: a fault I can see in a render means the item is not PASS. Every claim names a file.

## Measured: eye dots vs arm tips on screen, 26 m camera

Source: `ingame_report.json` `eyeVsArm`, computed in three.js.
- Eye y is the centre of the eye-dot box.
- Each arm tip is the arm vertex farthest from its pivot.
- The gap is the higher of the 2 tips minus the eye y, in 1x pixels of the 1600x900 frame (×3 in the crops).
- y grows downward.

| Ghost | Eye y | arm_L tip y | arm_R tip y | Gap 1x (x3 crop) |
|---|---|---|---|---|
| grass, tie | 431.3 | 439.1 | 437.9 | 6.6 px (≈20) |
| grass, glasses | 459.6 | 468.5 | 465.1 | 5.5 px (≈17) |
| grass, headset | 460.9 | 473.4 | 464.7 | 3.8 px (≈11) |
| path, tie | 430.2 | 438.0 | 436.8 | 6.6 px |
| path, glasses | 458.4 | 467.4 | 464.0 | 5.6 px |
| path, headset | 459.8 | 472.3 | 463.6 | 3.8 px |

v3 for comparison: the arms were level with the eyes. My read: every tip is now below the eye dots. The headset ghost's arm_R gap is the smallest, 3.8 px at 1x, and I would not call it a wide gap. The Illustrator and Viet judge "clear".

## Viet Tran (V1-V6)

| Item | My read | Evidence |
|---|---|---|
| V1 read | PASS (my read) | `silhouette-64-x4.png`: dome, drooping flaps, 5-scallop hem. The table above puts the arm tips below the eyes at 26 m (`lineup-grass-crop-x3.png`). |
| V2 construction | **PARTIAL** | **Clean:**<br>- cup: one closed stroke (`crops/headset-cup-on-surface.png`)<br>- tie on the surface, visible faces ≥ 1.3 mm off it (`build_report.json`)<br>- eyes and glasses (`crops/eye-on-surface-front.png`, `crops/glasses-on-surface-front.png`)<br>**Still visible:**<br>1. `variants.png`, all panels: the near arm hangs in front of the body as a curved flap. Its ink is open at the root, so it reads as a "C" hook.<br>2. `crops/arm-root-front.png`: a thin pale sliver under the root, between the body ink and the flap's lower ink.<br>3. `turn-side.png`: the near arm crosses the body side with its ink open at the root. |
| V3 detail | **PARTIAL** | `hero.png`: the crown is unchanged and round, and the arm tip is round. The arm-root faults in V2 show at card size. |
| V4 toon | PASS | Neutral band, unchanged (`ghost_toon.json`). |
| V5 | PASS | 578 / 528 / 580 triangles (`ingame_report.json`); 3 non-swap meshes. |
| V6 | PASS | `compare-ingame.png`: mean 0.75/255, 0.28% of pixels over 40. |

## Illustrator (I2)

**PARTIAL.**
- Better: the hem notch apex is round (`crops/hem-notch-34.png`), the arm tips are round (`hero.png`), and the cup stroke is clean.
- Still faulty: the arm root and hook faults listed under V2.

## BMGD (B1)

My read: the tie reads as a tie, upside down: a knot low on the chest and a wide point flying off the shoulder (`hero.png`, `variants.png`, `crops/tie-vs-kit.png`).

In both lineup x3 crops, the left ghost shows 2 eye dots, nothing centred below them, and a lilac point past the shoulder outline.

Weak points:
- In `crops/tie-vs-kit.png` the knot is smaller and less clear than Kit's.
- The blade's widening is foreshortened at 3/4.
- The ink on the long sides is thin: the walls are 2.7 mm tall plus a 1.6 mm plate.

Lena and BMGD should re-check the ink pixels and the read.

## Lena Park and Emil

No change to the colours, the band, the outline or the pose. Lena's tie-ink note is addressed with ink side walls and the plate, but they are thin (see above).

## Still weak

1. The near-arm "C" hook with open root ink in `variants.png`, and the pale sliver in `crops/arm-root-front.png`. The inverted-hull outline cannot draw a join where a separate flap lies in front of the body. A clean fix needs either a skinned arm in the body mesh or a screen-space outline. Both are bigger than this brief.
2. The headset ghost's arm gap is 3.8 px at 1x.
3. The tie's knot read and its long-side ink are thin (`crops/tie-vs-kit.png`).
4. The dotted hairline in three.js (`ingame.png`, brief item 6) was not checked separately.
