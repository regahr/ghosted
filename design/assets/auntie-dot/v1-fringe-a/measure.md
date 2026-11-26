# Auntie Dot v1: screen measures at the game camera (Viet Tran, 2026-11-26)

Set-up (= Ricky v1 and ATS v1): three.js r170, 26 m, pitch 42, yaw 20, fov 26, 1600x900, 1.6 px outline, y down.
Dot's root is turned 15 deg (net yaw 5: she faces the camera), as Kit, Ricky and the ATS.
Source: `ingame_report.json` (`lineup-grass`, `lineup-path`), made by `shoot_ingame.mjs`; blockout:
`blockout/ingame_report.json`. Smile numbers: `smile_report.json`, made by `make_sheets.py`.
Method (= Ricky, ATS): each character rendered alone on a flat magenta background, no contact shadow, same camera;
the box counts every non-background pixel, so the ink outline is included. The scale is set at Kit's own spot.

## Scale (brief: 0.9 x Kit; Kit = 75 px, so the target is 67.5 px)
| Step | H (m, bun top to sole) | At Kit's spot (grass / path) | Ratio | At Dot's own spot (grass / path) |
|---|---|---|---|---|
| blockout | 1.00 | 68 / 68 px | 0.907 / 0.907 | 71 / 67 px |
| final | 1.00 | 69 / 69 px (the 10-column bun added 1 px) | 0.920 | 73 / 68 px |
| **final** | **0.98** | **68 / 68 px** | **0.907 / 0.907** | 72 / 66 px |

- **Fact:** 0.9 x 75 = 67.5 px. 67 and 68 px are equally near; 68 px (0.907) is what 0.98 m gives at Kit's spot on
  both lineups. Width 49 px. 1 unit = 3.267 mm (`dot_build_report.json` `unit_mm`).
- **Fact:** the sketch estimate was 1.00 m and 68 px (`../sketch/body-map.md` A). The final bun is rounder (10
  columns), so 0.98 m keeps 68 px.
- **Fact:** Dot's own lineup spots differ by perspective only: grass (-2.5, 5.6) is 3 m nearer the camera than Kit
  (72 px); path (-2.0, 0.1) is 3.3 m to the left of Kit (66 px).

## No fringe (Rega ts 1795658373.096399: "hair fringe detected"; fix pass 2026-11-26)
Before this pass: `../v1-pre-fringe/`. Changes: the 4 ink strand lines on the front hair are gone; the front hairline
is raised and arched back (front-view y 80 at the centre, was 89; 90 at 50 deg, was 96; 102 at 72 deg, was 107); in
front of the 100-deg columns the hairline band is the skin's own shade tone (skin row 15 x the neutral grey band
178/255 = `#A98B6E`), not ink; ink stays behind the ears and at the nape.
Mask render `_lineup-*-hairmask.png`: hair red, hairline band orange, brows yellow, open-eye ink blue, smile green.
| Lineup | Lowest hair or hairline pixel, eye columns | Brow top | **Forehead skin** | Eye top | Hair-to-eye gap |
|---|---|---|---|---|---|
| grass | 613 | 620 | **6 px** | 623 | 11 px (was 9) |
| path | 393 | 400 | **6 px** | 402 | 10 px (was 8) |

- **Fact:** 6 px of plain forehead skin show between the hair edge and the brows at 1x on both lineups (target: 4 px
  or more). No hair pixel lies below the brows' top anywhere.
- **Fact:** the front hair has no ink line at the game camera now: no strands, and the edge is a soft shade tone.
- Proof: `crops/gamecam-face-x3-grass.png`, `crops/gamecam-face-x3-path.png` (before: `../v1-pre-fringe/crops/` same
  names), `crops/gamecam-face-hair-grass.png`, `crops/gamecam-face-hair-path.png` (x6 with the mask), front card
  `turn-front.png`, `crops/face-front-x2.png`.
- **Opinion:** at x3 the hair reads as a plain white dome pulled back into the bun, over a clear forehead; it does not
  read as bangs. The edge between hair and face is still a fairly straight line across the top of the face at the game
  camera (the camera looks down 42 deg, so the arch flattens); if Rega still reads that edge as a fringe, the next
  step is a higher hairline, which changes the sketch's proportions (a call for Rega, not this pass).

## The smile read (chair call 3)
| Lineup | Smile pixels | Box (w x h) | Below the eye bottom | Smile luma (min / mean) | Skin round it | Eye ink |
|---|---|---|---|---|---|---|
| grass | 5 | 8 x 2 px | 2 px | 21 / 52 | 135 | 39 |
| path | 7 | 7 x 2 px | 2 px | 21 / 76 | 137 | 50 |

- **Fact:** the smile line is 2.6 units wide (8.5 mm), thinner than the sketch stroke (3.2), so at 1x it is under
  1 px thick and blends with the skin: its mean luma (52-76) is far lighter than the eye ink (39-50).
- **Opinion: it does not read as a moustache or a beard.** At x3 and x6 it is a short, light, curved mark between
  the eyes and the chin line, the width of the gap between the eyes (`crops/gamecam-face-x3-grass.png`,
  `crops/gamecam-face-hair-grass.png`). There is no dark bar under the eyes (Ricky's grin was a filled shape; this is
  a line). The honest limit: at 1x it is faint, so the 1x face reads mainly as "two eyes under a white dome"; the
  smile reads at x3 and at card size (`expressions.png`, `crops/face-front-x2.png`).

## Landmarks on screen (grass lineup, y in px, rest pose)
| Bun top | Hairline (front) | Eye top | Eye bottom | Smile | Cups | Top button | Hands | Feet |
|---|---|---|---|---|---|---|---|---|
| 590 (bbox top) | 614 (mask) | 623 | 625 | 627-628 | 638.6 | 643 | 655 | 661 (bbox bottom) |

## Read (Opinion)
- In colour Dot reads as a white dome with a bun, a peach face, two lilac discs under the chin and a purple pear; she
  is the shortest figure next to Kit, Ricky and the ATS (`lineup-grass-crop-x3.png`, `lineup-path-crop-x3.png`).
- In grey she reads as a light dome on a dark pear; Ricky is darker and taller, Kit mid-grey, the Ghosties white,
  the ATS mid-grey and boxy (`lineup-grass-grey-crop-x3.png`, `lineup-path-grey-crop-x3.png`).
- The talk hand and the card read at the game camera (`crops/gamecam-talk-x3.png`, `crops/gamecam-card-x3.png`).
