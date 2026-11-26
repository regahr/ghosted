# Ghostie v7: screen measures at the game camera (Viet Tran, 2026-11-25)

Setup as in `../v6/measure.md`: three.js r170, 26 m, pitch 42°, yaw 20°, 1.6 px outline, 1600x900, y down. Source:
`ingame_report.json` `eyeVsArm`.
- v7 rest pose: 4° float tilt; arm_R droops 14° and swings 45° forward.
- v7 wave: the `wave` morph target. Wave 20 = weight 0.5; wave 40 = weight 1.
- Tip: the arm vertex farthest from the arm root centre.
- Arm high point: the highest arm vertex (skin weight 0.9 or more) on screen.
- Margin: tip y minus eye bottom y. A positive margin means the tip is below the eyes.

| Lineup | Ghost | Wave | Eye centre y | Eye bottom y | Collar top (d) | Knot top (d) | V point (d) | Tip L y | Tip R y | Arm high point L / R | Tip margin (px) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| grass | tie | 0 | 425.4 | 427.1 | 430.9 (+3.8) | 431.4 (+4.3) | 440.5 (+13.4) | 433.5 | 434.9 | 427.9 / 429.6 | 6.4 |
| grass | glasses | 0 | 453.6 | 455.5 | 459.1 (+3.6) | 459.7 (+4.2) | 468.8 (+13.3) | 462.8 | 462.2 | 457.0 / 456.8 | 6.7 |
| grass | headset | 0 | 455.2 | 457.6 | 460.7 (+3.1) | 461.3 (+3.7) | 470.5 (+12.9) | 467.5 | 462.1 | 461.7 / 456.6 | 4.5 |
| path | tie | 0 | 424.3 | 425.9 | 429.8 (+3.9) | 430.3 (+4.4) | 439.4 (+13.5) | 432.4 | 433.8 | 426.8 / 428.5 | 6.5 |
| path | glasses | 0 | 452.5 | 454.3 | 458.0 (+3.7) | 458.6 (+4.3) | 467.7 (+13.4) | 461.7 | 461.1 | 455.9 / 455.7 | 6.8 |
| path | headset | 0 | 454.1 | 456.5 | 459.6 (+3.1) | 460.2 (+3.7) | 469.4 (+12.9) | 466.4 | 461.0 | 460.6 / 455.5 | 4.5 |
| grass | tie | 20 | 425.4 | 427.1 | 430.9 (+3.8) | 431.4 (+4.3) | 440.5 (+13.4) | 431.5 | 434.9 | 426.8 / 429.6 | 4.4 |
| grass | glasses | 20 | 453.6 | 455.5 | 459.1 (+3.6) | 459.7 (+4.2) | 468.8 (+13.3) | 460.8 | 462.2 | 455.9 / 456.8 | 5.3 |
| grass | headset | 20 | 455.2 | 457.6 | 460.7 (+3.1) | 461.3 (+3.7) | 470.5 (+12.9) | 465.5 | 462.1 | 460.5 / 456.6 | 4.5 |
| grass | tie | 40 | 425.4 | 427.1 | 430.9 (+3.8) | 431.4 (+4.3) | 440.5 (+13.4) | 430.0 | 434.9 | 425.6 / 429.6 | 2.9 |
| grass | glasses | 40 | 453.6 | 455.5 | 459.1 (+3.6) | 459.7 (+4.2) | 468.8 (+13.3) | 459.3 | 462.2 | 454.7 / 456.8 | 3.8 |
| grass | headset | 40 | 455.2 | 457.6 | 460.7 (+3.1) | 461.3 (+3.7) | 470.5 (+12.9) | 463.9 | 462.1 | 459.3 / 456.6 | 4.5 |
| path | tie | 40 | 424.3 | 425.9 | 429.8 (+3.9) | 430.3 (+4.4) | 439.4 (+13.5) | 428.9 | 433.8 | 424.5 / 428.5 | 3.0 |
| path | glasses | 40 | 452.5 | 454.3 | 458.0 (+3.7) | 458.6 (+4.3) | 467.7 (+13.4) | 458.2 | 461.1 | 453.6 / 455.7 | 3.9 |
| path | headset | 40 | 454.1 | 456.5 | 459.6 (+3.1) | 460.2 (+3.7) | 469.4 (+12.9) | 462.8 | 461.0 | 458.2 / 455.5 | 4.5 |

## Read
- **Fact:** every tip is below the eye bottom, on all 3 ghosts, at rest and at wave 20 and 40. The smallest margin is
  +2.9 px (tie ghost, wave 40). In v6 the smallest was -1.9 px (arm_R on the headset ghost).
- **Fact:** arm_R on the headset ghost: v6 -1.9 px, v7 +4.5 px. This is the 45° forward swing.
- **Fact:** arm_L at wave 40: the tip is +2.9 to +4.5 px. The arm's top edge (high point) reaches 425.6 on the tie ghost,
  1.5 px above the eye bottom (427.1), and 454.7 on the glasses ghost, 0.8 px above (455.5). The brief measures tips,
  so this passes, but the raised arm top does reach the eye line.
- **Fact:** knot +3.7 to +4.4 px under the eye bottom, V point +12.9 to +13.5 px. Unchanged from v6.
