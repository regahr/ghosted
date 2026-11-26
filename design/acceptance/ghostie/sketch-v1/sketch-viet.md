# SK2 sketch gate: Viet Tran (3D Design Lead), Ghostie sketch v1, 2026-11-25

**Verdict: FAIL on one point (back-view hem). Everything else in SK2 passes. The fix is one curve.**

## Offer (own tools)
- 3dviz-pro-max SKILL.md step 2 (object reasoning: solve the hardest part first) and step 4 (join decision): used to
  judge the tie and the arm root. `scripts/search.py`, `design-context.py` and `host-probe.py` are build tools. They
  were not needed to score a sketch, so I did not run them.

## 1. Tie B with collar wings within budget: PASS
- **Fact** `assets/ghostie/v5/build_report.json`: body+arms 508, eyes 24, base 532, the v5 tie 39 tris (knot, blade,
  V, ink backing).
- **Fact** the budget is 600 per variant (`sketch-brief.md`, "Budget for Viet"). 600 - 532 = **68**. The tie cap is 68,
  not 90: the brief's 508 + 90 leaves out the 24 eye triangles.
- **Opinion** tie B is the v5 tie (about 39) plus two collar wings (fill + ink plate, about 6-8 each), so about 51-55.
  That fits under 68. The sheet's "est. 60-80" (`ghostie-sheet.png`, TIE B BUILD SPEC) is too high at its top end.
  If it goes over, drop the collar wings first, as notes.md line 47 says.

## 2. Do the views agree: FAIL (back hem only)
- **Fact** `v5/build_ghostie.py` lines 65-71: 5 scallops, with a lobe at the front. With an odd count, the back
  (180 deg) falls on a notch. `v5/turn-back.png` shows this.
- **Fact** `ghostie-sheet.png`, BACK: the hem is a mirror of the FRONT, with a lobe centred and notches on each side.
  This does not agree with the 5-lobe front, and it does not agree with the locked v5 hem.
- **Opinion** the other views agree: the crown, eye, arm-tip and hem guide lines hold. arm_L is higher in the front
  and on the viewer-left in the back. In the 3/4 view the tie moves toward the centre, as it should. In the side view
  only one eye shows and the tie sits at the front edge. I did not measure the 3/4 hem phase.

## 3. Smooth dome and closed arm root on the v5 one-mesh method: PASS (reachable)
- **Fact** `v5/build_ghostie.py` line 54: `SEG = 12`. Line 381 smooth-shades the body. The facets in paint-over mark 5
  are the 12-sided crown outline, not the shading.
- **Fact** the headset variant is at 596 of 600 (`build_report.json`). Any dome smoothing must add about 0 triangles.
- **Opinion** SEG 16 costs about +64. Pay for it by taking the dome from 8 profile rings to 6 (lines 61-62), about -64,
  or by thinning the hidden 60-triangle cavity fan (line 95). The game camera never sees the cavity.
- **Opinion** the closed arm root is already the v5 method: an exact-boolean union, one skinned mesh and one hull
  (`v5/changes.md` line 31). The sketch asks for nothing new at the join.

## 4. Paint-over marks 1-3 fixable: PASS
- **Fact** `v5/ingame.html` lines 51-57: one inverted hull over the whole skinned body, with smooth normals.
- **Opinion** all three marks have one cause at the concave root:
  - Mark 1 (crease): the hull shows through the join. Fix: scale the hull offset down near the root with a vertex
    attribute.
  - Mark 2 (pale wedge): a normal break at the boolean seam crosses the toon band. Fix: transfer the body normals
    across the root.
  - Mark 3 (hem hook): the arm's underside hull starts inside the outline. Fix: the same hull-offset fix as mark 1.
  - Cost for all three: 0 triangles.

## 5. The side-view arm reads as an oval: not a fault
- **Opinion** seen end-on, the inverted hull draws a closed loop around the arm, because the arm stands out in front
  of the body (Fact: the hull is on the whole mesh, `ingame.html` line 51). The sketch shows what the 3D will render
  (see also `v5/crops/arm-end-on-side.png`). The oval is a little taller than the front-view arm thickness. That is
  minor, and the blockout settles it.

## Watch at the blockout (not a sketch fault)
- **Opinion** `ghostie-sheet.png`, WAVE: at +40 deg the inner edge of arm_L passes close to tie B's right collar wing.
  Render the wave once with the tie on and check the clearance in screen pixels.

## Narrowest fix
Redraw the BACK hem only, with a notch centred (two full lobes either side of the centre). It must match the 5-lobe
front and `v5/turn-back.png`. Nothing else changes. Also correct the tie note on the sheet to "cap 68". That is a text
fix, not a must.

## Re-check (2026-11-25, after BACK_BODY change): SK2 PASS
- **Fact** `sketch/src/ghost.py` lines 286-289: `BACK_BODY` puts hem notches at x 206, 150 and 94. The crown centre is
  x 150 (line 23, `M150,36`), so a notch sits at the back centre with two lobes on each side. The FRONT (lines 30-32)
  keeps its notches at 192 and 112, with a lobe centred near 150.
- **Opinion** on `ghostie-sheet.png`, BACK, the centre notch shows on the body centre line, and the four lobes read
  as the far side of the 5-lobe front. That agrees with the centre dip in `v5/turn-back.png`. The arms, side shade and
  outline did not change. The tie note now says "Est. 51-55 tris (Viet). Cap 68" (`build.py` line 270).
