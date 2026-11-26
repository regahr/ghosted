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

## No fringe, pass 2 (Rega ts 1795658703.410809: the strands are fine; the SIDE hair beside the left eye is not)
Before: `../v1-pre-fringe/` (the version Rega judged) and `../v1-fringe-a/` (pass 1, now superseded).
Changes in this pass:
- Front as in v1-pre-fringe: strand lines back, front hairline y 89 at the centre, ink hairline band.
- Sides pulled up and back (front-view y): 72 deg 98 (was 107), 90 deg 100 (was 113), 104 deg 103 (was 115),
  120 deg 117 (was 143), 145 deg 150 (was 162). The hair drops only behind the ear, from the 120-deg column on.
Mask: hair red, hairline ink band orange, brows yellow, eyes blue. v1-pre-fringe was re-measured with the SAME mask
(`_pre-fringe-remeasure/`, its glb unchanged).
| Lineup | Version | Lowest side hair, viewer-left / viewer-right (above the eye top) | Hair or ink in the eye rows beside the eyes | Forehead (hair edge to brow top) |
|---|---|---|---|---|
| grass | v1-pre-fringe | 613 / 614 (10 / 9 px above) | none | not measured (no brow mask then) |
| grass | **now** | 612 / 614 (**11 / 9 px above**) | **none** (no gap to measure: no hair pixel in rows eye top-6 .. eye bottom) | 4 px |
| path | v1-pre-fringe | 393 / 395 (9 / 7 px above) | none | - |
| path | **now** | 392 / 394 (**10 / 8 px above**) | **none** | 5 px |

- **Fact:** in both versions no hair pixel and no hairline-ink pixel lies beside the eyes at 1x; the side hair's lowest
  point is 8-11 px above the eye top. The side hairline moved up 13-26 units in the model, but at the game camera
  this shows as only 1 px, because those columns lie on the foreshortened sides of the head.
- **Fact:** what still runs down beside the viewer-left eye at 1x is the head's ink OUTLINE (the hull), from the hair
  edge down the cheek, and the small ear bump on the eye line. The mask shows it as black, not hair.
- Proof: `crops/fringe-side-compare-x6.png` (pre colour, pre mask, now colour, now mask; grass and path),
  `crops/fringe-side-compare-x3-grass.png`, `crops/fringe-side-compare-x3-path.png`, `crops/gamecam-face-hair-*.png`,
  front card `turn-front.png`.
- **Opinion: I cannot prove this pass fixes what Rega saw.** By the pixels there was no side hair beside the eyes
  before either, so the "fringe" Rega reads is most likely the dark head outline plus the ear at the temple. Stopped
  after one pass, as asked.

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
