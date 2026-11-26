# Ghostie v6: screen measures at the game camera (Viet Tran, 2026-11-25)

- Camera: three.js r170, 26 m follow camera, pitch 42°, yaw 20°, 1.6 px outline, 1600x900 frame (`ingame.html`
  `renderLineup`). y grows downward. Source: `ingame_report.json` `eyeVsArm`.
- Pose: the in-game rest pose. The float node carries the 4° tilt, arm_R droops 14°, and arm_L waves 0, 20 or 40°.
  The 3 ghosts keep the blockout lineup yaws (+10°, -2°, -14°), so their effective yaws to the camera are 10°, 22°
  and 34°.
- Eye bottom: the lowest eye-dot vertex on screen.
- Tip: the arm vertex farthest from the arm root centre (front units x 250, y 225). This is the same rule that the
  build uses for the sketch tip.
- Collar, knot and V point: the body-map landmarks (y 166, 170, 262), stored in the `acc_tie` extras. The tie, glasses
  and headset ghosts share the body, so the landmarks are given for all 3 rows; only the tie ghost shows the tie.
- d: pixels below the eye bottom.

| Lineup | Ghost | Wave | Eye centre y | Eye bottom y | Collar top (d) | Knot top (d) | V point (d) | Tip L y | Tip R y | Tip margin below eye bottom |
|---|---|---|---|---|---|---|---|---|---|---|
| grass | tie | 0 | 425.4 | 427.0 | 430.9 (+3.9) | 431.4 (+4.4) | 440.5 (+13.5) | 430.9 | 428.7 | 1.7 |
| grass | glasses | 0 | 453.5 | 455.4 | 459.1 (+3.7) | 459.7 (+4.3) | 468.8 (+13.4) | 460.1 | 455.8 | 0.4 |
| grass | headset | 0 | 455.2 | 457.6 | 460.7 (+3.1) | 461.3 (+3.7) | 470.5 (+12.9) | 465.0 | 455.7 | **-1.9 (FAIL)** |
| path | tie | 0 | 424.2 | 425.9 | 429.8 (+3.9) | 430.3 (+4.4) | 439.4 (+13.5) | 429.8 | 427.6 | 1.7 |
| path | glasses | 0 | 452.4 | 454.3 | 458.0 (+3.7) | 458.6 (+4.3) | 467.7 (+13.4) | 459.0 | 454.7 | 0.4 |
| path | headset | 0 | 454.1 | 456.4 | 459.6 (+3.2) | 460.2 (+3.8) | 469.4 (+13.0) | 463.9 | 454.6 | **-1.8 (FAIL)** |
| grass | tie | 20 | 425.4 | 427.0 | 430.9 (+3.9) | 431.4 (+4.4) | 440.5 (+13.5) | 430.5 | 428.7 | 1.7 |
| grass | glasses | 20 | 453.5 | 455.4 | 459.1 (+3.7) | 459.7 (+4.3) | 468.8 (+13.4) | 459.8 | 455.8 | 0.4 |
| grass | headset | 20 | 455.2 | 457.6 | 460.7 (+3.1) | 461.3 (+3.7) | 470.5 (+12.9) | 464.7 | 455.7 | **-1.9 (FAIL)** |
| grass | tie | 40 | 425.4 | 427.0 | 430.9 (+3.9) | 431.4 (+4.4) | 440.5 (+13.5) | 427.5 | 428.7 | 0.5 |
| grass | glasses | 40 | 453.5 | 455.4 | 459.1 (+3.7) | 459.7 (+4.3) | 468.8 (+13.4) | 456.9 | 455.8 | 0.4 |
| grass | headset | 40 | 455.2 | 457.6 | 460.7 (+3.1) | 461.3 (+3.7) | 470.5 (+12.9) | 461.8 | 455.7 | **-1.9 (FAIL)** |
| path | tie | 40 | 424.2 | 425.9 | 429.8 (+3.9) | 430.3 (+4.4) | 439.4 (+13.5) | 426.4 | 427.6 | 0.5 |
| path | glasses | 40 | 452.4 | 454.3 | 458.0 (+3.7) | 458.6 (+4.3) | 467.7 (+13.4) | 455.8 | 454.7 | 0.4 |
| path | headset | 40 | 454.1 | 456.4 | 459.6 (+3.2) | 460.2 (+3.8) | 469.4 (+13.0) | 460.7 | 454.6 | **-1.8 (FAIL)** |

Other numbers (same report): ghost body 27 px tall (float to crown), Kit 55 px.

## Read
- **Fact:** arm_L (the wave arm) stays below the eye bottom in every row, at 0, 20 and 40°. The thinnest margin is
  0.4-0.5 px.
- **Fact:** arm_R (the rest arm) fails on the headset ghost by 1.8-1.9 px. Its tip sits at the eye centre height
  (455.7 vs 455.2). It passes on the tie ghost (+1.7 px) and only just on the glasses ghost (+0.4 px).
- **Fact (cause):** the headset ghost turns 34° from the camera, so arm_R swings back, and the camera reads "back" as
  "up". The arm geometry follows the sketch (tip at front-view y 241, `build_report.json` `arm_tip_front_units`).
- **Opinion:** I tried one method, a 14° rest droop of arm_R (in the sketch REST POSE). A further droop does not close
  it: about 50° would be needed. The fix is a rest-pose or a sketch decision, so it goes to the chair (see
  `selfcheck.md`, open item 2). I did not try a second method on my own.
- **Fact:** the knot top is 3.7-4.4 px under the eye bottom and the V point 12.9-13.5 px under it. The blockout had
  4.5 and 13.7 px (`../blockout/measure.md`). The tie still reads as a tongue, as Rega accepted (`design/bible.md`
  lines 41-43).
