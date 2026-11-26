# SK2 sketch gate v2: Viet Tran (3D Design Lead), Ghostie sketch v2 + body map v2, 2026-11-25

**Verdict: SK2 FAIL on one point. The 3/4 view does not agree with the front view or the 3D: the far arm is missing.
The budget passes, with the fix below. The body-map landmarks match the blockout. The fix is one redrawn outline.**

Rega's ruling holds: the centred tie may read as a tongue at the game camera (`design/bible.md` lines 38-46). I do
not score it as a fault.

## Offer (own tools)
- 3dviz-pro-max `SKILL.md` step 2 (object reasoning: find the silhouette and the parts that carry it) and step 4
  (construction and joins): used to judge the arms across the views and the headset budget.
- `references/object-reasoning.md` and `references/object-craft.md`: give the projection check that I used on the
  3/4 arm (where a side part must land in the silhouette at a given yaw).
- `scripts/search.py`, `design-context.py` and `host-probe.py` are build tools. Scoring a sketch does not need them,
  so I did not run them. Nothing in the brief blocked a tool.
- The crops that I zoomed (2x to 5x) are in the session scratchpad. They are not saved as assets.

## 1. Built within 600 per variant: PASS (with a stated path for the headset)
- **Fact** `assets/ghostie/blockout/build_report.json`: body+arms 508, eyes 24, base 532. tie 556, glasses 568,
  headset **656**. The headset part is 124 tris: cup + ink ring + band (`acc_headset_note`).
- **Fact** 600 - 532 = 68. So the headset must be 68 tris or fewer.
- **Fact** `build_ghostie.py` lines 266-287: each cup is a 10-sided flat disc (`CUP_N = 10`): about 8 top + 20 wall
  triangles, plus a separate 10-quad ink annulus (20 tris) on its top edge. 2 cups = about 96. The band is about 28.
- **Opinion** how it gets to 68 or fewer, in order:
  1. Drop the ink annulus geometry (-40). Draw the cup's ink ring with the shader instead: a 2-ring cap
     with vertex colour, or the same inverted hull the body uses. That gives 616.
  2. Cut the cups from 10 to 8 sides, with no back face (6 top + 16 wall = 22 each, so 44). That gives about 594.
  3. Keep the band at 6 stations or fewer, as a one-sided strip of about 12-24 tris. Final about 588-600.
  - Fallback if still over: thin the hidden cavity fan inside the body, which the game camera never sees
    (`build_ghostie.py` line 90). Do not take triangles from the dome profile. Its smoothness is the silhouette.
- **Fact** the tie is 24 (cap 68) and the glasses are 36. Both fit now.

## 2. Do the views agree: FAIL (3/4 arms only)
- **Fact** `ghostie-sheet.png`, 3/4 panel: the viewer-right arm shows at full front-view length. The viewer-left side
  is one straight wall from the shoulder to the hem, with **no arm**.
- **Opinion (measured on the sheet)** in the 3/4 panel the eye midpoint sits about 0.27 of the half-width left of
  the dome centre. That is a yaw of about 15-20 deg. At that yaw each arm tip lands about 135 units from the axis,
  and the body edge is about 104 units from the axis (`body-map.md` B: arms 280 tip to tip, arm-root width 208). So
  **both** arms must stick out past the body edge, by about 30 units each. The far arm cannot hide.
- **Fact** `assets/ghostie/blockout/turn-34.png`: the 3D shows a nub on the viewer-left (far arm) past the outline.
  The near arm lies mostly inside the silhouette, as a crease. The sketch shows the opposite.
- **Opinion** the other views agree:
  - The crown, eye, neck, arm-tip and hem guide lines hold across front, 3/4, side and back.
  - The back has a centred notch, as the 5-lobe front requires.
  - The side shows one eye and the tie at the front edge, with the end-on arm as an oval (my v1 ruling §5 stands).
  - The light is fixed in the world: the shade is on the left in the front and 3/4, and on the right in the side and
    back. This is consistent.
- **Narrowest fix:** redraw the 3/4 outline with a short far-arm nub past the viewer-left edge, at the arm-tip line.
  Make the near arm a little shorter (foreshortened), so that it matches `blockout/turn-34.png`. Nothing else
  changes.

## 3. Body-map landmarks vs the blockout: PASS (the sketch side)
The scale is `build_ghostie.py` line 186: z = 0.47 - (y - 36) x 0.001774.
- **Fact** eye line y 118 is `EYE_Z = 0.3245` (line 120). The ear points and cups are on the eye line
  (`EAR_Z = EYE_Z`, line 255). Match.
- **Fact** collar top 0.2398 (y 166 is 0.2394), knot top 0.2328 (y 170 is 0.2323), V point 0.0752 (y 258 is
  0.0762) (`build_report.json` `tie_landmarks_z_m`). Match within 1 unit.
- **Fact** the glasses are on the eye line (`build_ghostie.py` lines 234-242). Match. The tie is centred on the body
  axis (`front-variants.png`). Match.
- **Fact** at the game camera the arm tips are 5.0-7.8 px below the eye centre (`ingame_report.json` `gapPx`). So
  "arm tips below the eye bottom" holds in the real render. The sheet's estimate tile drew arm_R at the eye line.
  The real render settles it.
- Blockout-side differences. These are not sketch faults, and the final model must fix them:
  - **Fact** the blockout arms are v5's, unchanged: the highest arm point is z 0.134-0.141 (about y 221-225), and the
    tips are at z 0.045 (about y 276). The body map puts the arm roots at y 190-260, and the sheet's arm-tip line is
    at about y 237 (Opinion: measured on the sheet). So the blockout arms hang about 15 % of the body lower than the
    sketch.
  - **Fact** body map C: the headset band top is at y 46, inside the crown outline. The blockout band runs on the
    crown outline, edge-on (`front-variants.png`, and `measure.md` "hard to see").
  - **Fact** `build_report.json` `rest_pose`: the 3 deg lean and 5 deg roll are baked into the mesh. So the blockout
    front is lopsided (in `front-variants.png` the left wall is straight and the right side slants, with a crease).
    The sheet is upright and symmetric. Move the lean to the float node, so that the turnaround renders upright.
  - **Fact** the stale label `below eye line 0.258-0.0275` (`build_ghostie.py` line 339) still names v5's eye line.
    The value passes. Only the label is wrong.

## Whole-picture check (every panel, 2x; 4-5x where marked)

| Panel | Read |
|---|---|
| Sheet: title and guide lines | none seen (Fact) |
| Sheet: FRONT | Hairline jog on the inner edge of the ink outline at the lower-left lobe, where the shade band ends; visible at 4-5x, faint at 2x (Fact). The shade band ends in a flat cut across the lobe and reads as a patch (Opinion). |
| Sheet: 3/4 | **Far arm missing** on the viewer-left; the near arm is at full front length (Fact; SK2 fail, see §2). The same shade-band end as the front (Opinion, minor). |
| Sheet: SIDE | No drawing flaw. The tie is drawn as a full narrow V inset from the front edge, and its collar wing pokes back as a small flag. In 3D it is a sliver on the front edge (`blockout/turn-side.png`) (Opinion, minor). The end-on arm oval is at the arm-tip line (Fact). |
| Sheet: BACK | Centre notch is correct (Fact). Same hairline ink jog where the shade band ends at the lower-right lobe (Fact, minor). |
| Sheet: palette and shape rules | none seen (Fact) |
| Sheet: variant tie | none seen (Fact). The tongue read is ruled OK (`bible.md` line 41). |
| Sheet: variant glasses | none seen (Fact) |
| Sheet: variant headset | The band is a wide face-on lilac stripe inside the dome, with no ink, while the cups have ink (Fact). Mixed ink weight (Opinion). It matches body map C (band top y 46), but not the blockout (see §3). |
| Sheet: WAVE | Soft shoulder on both sides; arm tip below the eyes (Fact). The faint rest-arm ghost line meets the raised arm with no gap and reads as a loop (Opinion, minor). Labels are clear of the body (Fact). |
| Sheet: REST POSE | The arm_R tip (viewer-left) narrows to a sharper point than arm_L (Opinion, minor). Tilt only in this panel, as ruled (Fact). |
| Sheet: 64 px silhouette | none seen (Fact) |
| Sheet: game-camera estimate | Tile 1: arm_R sits at the eye line, as a horizontal nub (Fact). The real render puts it 7.8 px lower (`ingame_report.json`), so the tile disagrees with the 3D (Fact). Replace the tiles with `blockout/lineup-grass-crop-x3.png` before Rega sees the card (Opinion). |
| Sheet: tie build spec | none seen (Fact). The note "cap 68" is correct. |
| Body map A: explore | none seen as a drawing flaw (Fact). The blue mouth-zone box is intended. |
| Body map B: front landmarks | The head-height bar's bottom tick floats about 40 px below the bar end and below the hem, next to the "C." header (Fact). The header says "body 265 crown-to-hem", and the notes say "whole body = 280" (cusps vs lowest lobe, both true but unlabelled) (Fact, minor). Hairline ink jog at the lower-left lobe, where the shade ends (Fact, minor). |
| Body map B: notes | "arm tips below the eye bottom (y 131)" agrees with the render (Fact). |
| Body map C: attachment | Side tile: the same inset tie as the sheet side (Opinion, minor). Otherwise none seen. |
| Body map D: game camera | Tile 2 and tile 3: arm_R at the eye line, which the real render disproves (Fact, see above). Tile 1 (v5 crop) is a warm wall background, unlike the others (Opinion, cosmetic). |
| Blockout (reference, not judged for SK2) | Baked lean makes the front lopsided; the arms hang low; the collar wings are ink lines only, which vanish at 26 m (`measure.md`); the headset band is edge-on (Fact; see §3). |

## What blocks the card
1. 3/4 far arm (SK2 must). One outline redraw.
2. The game-camera estimate tiles disagree with the real render. Swap them for the blockout crops.
Minor, but visible, so fix in the same pass: the ink jog at the end of the shade band (front, back, body map B), the
floating tick in body map B, and the 265/280 label.
