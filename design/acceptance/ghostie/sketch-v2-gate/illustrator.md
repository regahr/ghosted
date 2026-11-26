# Sketch v2 gate: Illustrator (judge; I did not draw it), 2026-11-25

Rules: `acceptance/checklist.md` line 23 (SK1); council skill "Whole-picture check" and "Game art pipeline" 1a.
Ruling applied: the centred tie may read as a tongue at the game camera (`bible.md` lines 41-43). It is not scored as a flaw.
Crops at 2x (4x for the headset band) are in my scratchpad:
`<scratchpad>`.

## Verdict

- **SK1 by its own text: met.**
  - **Fact:** the body is one Bezier path (`src/ghost.py` line 137 `path`, line 143 `oval_path`). Ellipses are used only for the eyes, cups, rims and shadows (`src/ghostie-sheet.svg`).
  - **Fact:** `silhouette-64.png` is symmetric about x 32 on every 4th row (bbox 7-59 x 6-61) and shows the dome, 2 arm stubs and the lobed hem.
  - **Opinion:** it reads as a ghost at 64 px.
- **Seat verdict: FAIL**, because of the whole-picture check below (brief: "a visible flaw that a viewer would notice is a FAIL"). Flaw 1, the headset band, is the one that blocks. Flaws 2 and 3 also block unless the chair rules otherwise.

## Body map: proportions and landmarks

- **Proportions: PASS.**
  - **Fact:** 2.15 head-heights, width 1.6 hh (`body-map.md` B).
  - **Fact:** the eyes are symmetric about x 150 (124 / 176).
- **Landmarks: PASS.**
  - **Fact:** the following are decided and drawn: eye line, ear points on the eye line, the empty mouth zone, neck line, arm roots, chest and hem.
  - **Fact:** the camera estimate agrees with the real render. Estimate: knot 7.0 px under the eye centre (`body-map.md` D). Render: knot 6.4 px (`blockout/measure.md`).
- **Attachment points: PASS on paper. The drawn headset does not follow them** (see flaw 1).

## Whole-picture check, one line per panel

| # | Panel | Read | Mark |
|---|---|---|---|
| 1 | Sheet: variant headset; Body map C: headset | **FLAW.** The band has no ink line and a smaller radius than the dome. Above the band, the crown ink line still shows as a black crescent. At the sides, the band hides the body outline. The band reads as lying on the forehead, not over the crown, so the accessory is not where the real object sits. The real render puts the band on the crown edge (`blockout/front-variants.png`, right), so the sketch and the render disagree. | Fact (visible, crop `s-hs-band-x4.png`); the reading is Opinion |
| 2 | Sheet: side; Body map C: side | **FLAW.** The arm, seen end-on, is a closed oval that floats in the middle of the body. It reads as a hole or a mouth. Viet's earlier ruling (`sketch-viet.md` §5) says this is what the hull draws, but a viewer sees a floating part. | Fact (visible); Opinion that it blocks |
| 3 | Sheet: side; Body map C: side | **FLAW.** The tie is drawn face-on, about 30 units inside the front contour, with a collar wing that sticks up like a flag. Seen from the side, a tie on the chest sits on the front contour, edge-on. The side view and the front view disagree. | Opinion |
| 4 | Sheet: front | none seen | Opinion |
| 5 | Sheet: 3/4 | Minor: both eyes and both collar wings have the same width, with no foreshortening on a turned round head. The far arm is hidden; this is plausible at this turn. | Opinion |
| 6 | Sheet: back | none seen (notch centred; the shade band is mirrored correctly) | Opinion |
| 7 | Sheet: palette and shape rules | none seen | Opinion |
| 8 | Sheet: variant tie | none seen (tongue read ruled OK) | Opinion |
| 9 | Sheet: variant glasses | none seen | Opinion |
| 10 | Sheet: wave | Minor: the rest-arm ghost line is grey (RGB 186,191,200), but its label says "faint blue". | Fact |
| 11 | Sheet: rest pose | none seen | Opinion |
| 12 | Sheet: 64 px silhouette | none seen | Fact (symmetry measured) |
| 13 | Sheet: game camera estimate | Minor: in the headset tile, the near cup rides at crown height while the far cup is at the eyes, so the pair looks lopsided. The real lineup (`lineup-grass-crop-x3.png`) does not show it this way. | Opinion |
| 14 | Sheet: tie build spec | Minor: the tie fills only the top half of a tall empty box. | Opinion |
| 15 | Body map A: explore | none seen (tongue read ruled OK) | Opinion |
| 16 | Body map B: front landmarks | **FLAW (labels):** (a) The heading says "body 265 crown-to-hem", but the notes say "Whole body = 280 units"; these are two numbers for one measure. (b) A stray, unlabelled tick floats under the head-height bar, just above the "C." heading. (c) The tie V point (y 258) and arm root bottom (y 260) guide lines merge into one double line. | Fact |
| 17 | Body map B: notes | none seen | Opinion |
| 18 | Body map C: tie, glasses | none seen | Opinion |
| 19 | Body map D: game camera | none seen beyond the ruled tongue read | Opinion |
| 20 | Tie options: Ghostie card and close-up | none seen | Opinion |
| 21 | Tie options: Kit card and close-up | none seen | Opinion |

## Real-render evidence (blockout; this is S1 ground, listed so the chair sees it)

`blockout/front-variants.png`:
- **Fact:** the glasses rims are octagons; the sketch draws them round.
- **Fact:** the headset cups are tilted and uneven. The left cup is about y 270-330 and the right cup about y 250-305.
- **Fact:** the collar wings are thin open lines that float apart from the knot.
- **Fact:** the shoulders are a hard corner where the stub arms meet a straight side; the sketch has a soft shoulder.
- **Fact:** the front hem shows 2 lobes; the sketch shows 3.
- **Opinion:** the sketch and the blockout do not yet match. That is for the paint-over, not this gate.

## To pass

1. Redraw the headset band so that it sits ON the crown: an inked band whose outer edge meets or sits outside the dome outline.
2. Side view: show the arm as a stub that joins the contour, or have the chair rule that the floating oval stands.
3. Side view: put the tie and collar on the front contour, edge-on.
4. Fix the body-map label items (16a-c) and the "faint blue" label (10).
