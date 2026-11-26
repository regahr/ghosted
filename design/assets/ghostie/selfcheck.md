# Ghostie v5: self-check (builder, Viet Tran seat)

- These are builder claims; the seats score on their own.
- Rule: a fault I can see in a render means the item is not PASS. Every claim names a file.

## Eye dots vs arm tips on screen, 26 m camera

Source: `ingame_report.json` `eyeVsArm`.
- three.js skinned positions: an arm tip is the farthest vertex weighted ≥ 0.9 to that arm bone.
- 1x pixels of the 1600x900 frame; y grows downward.
- The gap is the higher tip minus the eye y.

| Ghost | Eye y | arm_L tip y | arm_R tip y | Gap 1x (≈ x3 crop) |
|---|---|---|---|---|
| grass, tie | 431.3 | 439.1 | 437.9 | 6.6 (≈20) |
| grass, glasses | 459.6 | 468.5 | 465.1 | 5.5 (≈17) |
| grass, headset | 460.9 | 473.4 | 464.7 | 3.8 (≈11) |
| path, tie | 430.2 | 438.0 | 436.8 | 6.6 |
| path, glasses | 458.4 | 467.4 | 464.0 | 5.6 |
| path, headset | 459.8 | 472.3 | 463.6 | 3.8 |

These are the same as v4, so the skin did not move the arms.

## Arm join (the v5 method fix)

| Proof file | My read |
|---|---|
| `variants.png`, `hero.png` | The near arm is now one closed ink shape that grows out of the body; the v4 "C" hook with open root ink is gone. **Still visible:** a thin tapering crease line runs from the arm root up and inward across the body, about 60 px long in the 600 px panels. At the concave join of the merged mesh, the hull shows through. It reads as a fold line, but it is a visible mark. |
| `turn-side.png`, `crops/arm-end-on-side.png` | The arm seen end-on is a closed ink loop (no v4 slot), with a thin crease line above it. |
| `crops/arm-root-front.png` | The body outline flows into the top of the arm with no step. **Still visible:** a small pale wedge at the lower root, between the body line and the arm's lower ink. |
| `crops/arm-wave-blender.png` vs `crops/arm-wave-threejs.png` | Both raise the arm on the arm_L bone. In three.js the raised arm keeps a closed outline. In Blender the stroke along the raised arm's top still breaks near the root. Better than v3 in three.js, not in Blender. The two crops are framed differently (Blender close-up vs three.js 1200 px), so this is not a pixel match. |
| hem under the near arm (`variants.png`) | The small hook at the hem under the near arm is reduced but still visible at x≈335, y≈380 of the tie panel. |

**V2: PARTIAL.** The method fix removed the hook and slot, but the crease line and the lower-root wedge remain.

## Tie (chair's v5 tie section)

| Point | My read | File |
|---|---|---|
| Closed ink stroke | A dark rim on every side, at a thinner weight than the body outline. | `crops/tie-vs-kit.png`, `variants.png` |
| Knot | A raised trapezoid with a step at the blade. It reads, but small. It sits right of the right eye and just below it. | `variants.png`, `hero.png` |
| Blade | It is wider than v4 and has the S-bend. It still reads more like a short horizontal flag than Kit's hanging tie. The edges show small steps at the column ridges. | `crops/tie-vs-kit.png` |
| Tip | A symmetric V in the air at the side of the shoulder (`turn-front.png`), not at the crown. | `turn-front.png`, `hero.png` |
| 26 m | 2 eye dots, nothing centred below them; the tie is a small lilac mark at the ghost's upper side. | `lineup-grass-crop-x3.png`, `lineup-path-crop-x3.png` |

**B1 and I2 on the tie:** for BMGD and the Illustrator to judge. My opinion: it is a tie in a side wind, but it is close to the "horn or flag" risk. Per the brief, the hanging tie stays open for Rega.

## Other

- **V5: PASS.** Triangles 571 / 568 / 596 ≤ 600 (`ingame_report.json`); 1 non-swap mesh.
- **V6:** `compare-ingame.png` mean 0.82/255, 0.34% of pixels over 40. The difference is in the arm crease region (three.js draws the crease shorter than Blender) and on outline edges.
- **Three.js hairline (brief item 5):** I compared v4 and v5 `ingame.png` at x 200-420, y 580-800 and saw no dotted hairline in either. It was either fixed by an earlier change or sits elsewhere. Not proved further.

## Still weak

1. The crease line from the arm root across the body, in `variants.png` and `hero.png`.
2. The pale wedge at the lower arm root (`crops/arm-root-front.png`).
3. The small hem hook under the near arm (`variants.png`).
4. The Blender wave pose still breaks the top stroke near the root (`crops/arm-wave-blender.png`). Rule from Emil: never use the wave pose on a card.
5. The tie's read (flag vs tie) and its small stepped edges (`crops/tie-vs-kit.png`).
6. Headset headroom is 4 triangles (596 of 600); the headset arm gap is 3.8 px.
