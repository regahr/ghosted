Viet Tran (3D Design Lead (3DViz Pro Max)): GHOSTED acceptance gate, Kit v5, items V1-V6

## Offer

- `3dviz-pro-max/templates/checklists/visual-anti-slop.md` items 1-7. **Fact**: V1-V6 come from this source (`design/acceptance/checklist.md`, the "Source:" line under "Viet Tran"). Items 1-3 (read, construction, real-scale detail) carry most of this re-score, because v5 changes only the case arm.
- `3dviz-pro-max/references/object-craft.md#choose-continuity-at-the-join` and `#diagnose-deformation-at-the-region-that-fails`. These set the method: check the changed region (shoulder, elbow, cuff, fist, handle, case) from all 4 turns and the hero, then the joins next to it that the change could move (cuff/hand, fist/handle, case/leg, arm/torso negative space).
- Tools I ran: I opened all 4 turns, `hero.png`, `compare-ingame.png`, `expr-gamecam-strip.png` and the builder's `crops/arm-*-v4-v5.png`. I made my own 2-4x nearest-neighbour crops with `magick` in the scratchpad (not saved in the project): the arm in each turn, the grip in each turn and the hero, and the 3/4 arm in v4 against v5. I printed both 64 px silhouettes (v4 and v5) as ASCII and sampled grey values at the gaps. I parsed `kit.glb` for nodes and triangle counts. I did not use `changes.md` or `selfcheck.md` as evidence.
- Conflict note: an earlier instance of this seat built Kit. I scored as an outside judge, from pixels and the glb only.

## The changed area

| Check | Result | Evidence |
| --- | --- | --- |
| Sleeve along the bent path: joins | Clean | **Fact** (seen): 3x crops of `turn-front.png` (520,520), `turn-34.png` (520,520), `turn-back.png` (130,520) and a 2.5x crop of `turn-side.png` (300,520). The sleeve is one closed shape from shoulder to cuff. The shoulder cap in the side view is closed. The hand sits inside the cuff with a closed ink line in all views. No crease, pinch or gap at the elbow. |
| Sleeve: outline | Same as v4 | **Fact** (seen): the outer edge has a continuous outline in all 4 turns. Where the sleeve lies over the torso (front, 3/4, side) the inner edge has no ink and reads only by a shade band. My v4/v5 3/4 crop pair shows the same in v4, so it is not a regression. The elbow bend shows as a small kink in the back and front outer contour; in 3/4 the arm reads nearly straight. |
| Sleeve: shading bands | Clean | **Fact** (seen): 2 bands on the sleeve (lit, and a darker band on the underside of the forearm) in all 4 turns and the hero. No acne, streaks or blotches in my 3-4x crops. |
| Grip: handle exits below the fist equator | Yes | **Fact** (seen): 4x crops of the grip in `turn-front.png` (614,735), `turn-34.png` (642,748), `turn-side.png` (503,766), `turn-back.png` (161,753) and `hero.png` (787,766). In each, both handle legs leave from the bottom of the fist. In 3/4 and the hero a short sliver of the handle bar shows at the lower right of the fist, under the fist outline, with ink between. Nothing brown shows on the upper half of the fist. |
| Case plumb, face turned | Yes | **Fact** (seen): `hero.png` and `compare-ingame.png`: the case hangs straight under the fist, its face turned so a narrow side bevel shows. Both handle legs read in the hero. |

## Regression check

- **3/4 silhouette gap, thinner than v4.** **Fact** (my ASCII and samples of `silhouette-64-34.png`): the case/leg gap is 2 px in rows 46-48, 3 px in row 49, under 1 px in rows 50-53 (the brightest gap pixel is grey 148-181 of 255, never full white), and 2 px in rows 54-58. v4 was 2-4 px in rows 50-61 (`v4/silhouette-64-34.png`). So the "about 1 px in rows 50-58" claim is a little generous for rows 50-53.
- **Front silhouette lost most of its arm/body negative space (not named in the brief).** **Fact** (ASCII of `silhouette-64.png`, v4 against v5): v4 had a 6-8 px gap in rows 49-58. v5 has about 1 px in rows 46-48, a near-close at row 49 (gap pixels grey 40 and 112, no white), about 1.5 px in rows 50-53 and 3-4 px in rows 54-58. This is the direct cost of the arm Rega asked for (22 degrees out, case plumb under the fist).
- **Real view size.** **Fact** (seen): `expr-gamecam-strip.png` at 56 px (`ingame_report.json` "kitPx": 56): in all 5 expressions the fist and case sit clear of the body with background between, and the case reads as its own block. **Opinion**: the thin 64 px gaps do not hurt the read at the game camera, because the camera looks down at 3/4 and the outline separates the parts.
- Not touched by v5, re-checked briefly: head, hair, sprout, collar, tie, legs and shoes look the same as v4 in the 4 turns (**Fact**, seen). The v4 temple seam note (v4 fix note 1) was not in scope and I did not re-score it.

## Scores

| Item | Verdict | Evidence |
| --- | --- | --- |
| V1 read: silhouette, proportions, negative space | **PASS** | **Fact** (ASCII): `silhouette-64.png` and `silhouette-64-34.png` still show the round head (rows 7-27), the hooked sprout (rows 0-6) and the case as its own block (rows 49-59) with a gap to the leg in every row; the arm/body gap is now 1 px or less in rows 46-53 (see note 1). |
| V2 construction: no cut-through, no floating parts, no gaps | **PASS** | **Fact** (seen): my grip crops in 4 turns and the hero show both handle legs leaving the fist bottom; the cuff/hand and shoulder joins are closed; nothing floats. |
| V3 detail at real view size (26 m camera, card close-up) | **PASS** | **Fact** (seen): `expr-gamecam-strip.png` at 56 px: arm, fist and case read apart from the body in all 5 expressions; `hero.png` shows both handle legs and the turned case face. |
| V4 toon: 2 bands on props, 3 on faces, clean shadows | **PASS** | **Fact** (seen): the sleeve and case have 2 clean bands in my 3-4x crops of all 4 turns and the hero; no acne, streaks or blotches. |
| V5 at most 2,500 visible triangles; at most 3 meshes (swap parts excluded) | **PASS** | **Fact** (my parse of `kit.glb`): body 1,321, head 736, briefcase 178 (3 meshes); swap parts sprout 84 plus `face_*`/`eyes_*`. Max active set offer_joy 2,319 + 69 + 92 = **2,480**, the same as v4. |
| V6 in-game matches Blender in shape and colour | **PASS** | **Fact** (seen): `compare-ingame.png` shows the same arm angle, case plumb under the fist, turned case face, hues and band placement in both halves; `compare_report.json` "mean" 2.0-2.2. |

**Overall: PASS.** All six must items pass. The arm change is clean at every join I checked, the grip rule holds in all 5 views, and the budget is unchanged at 2,480. The one cost is a thinner silhouette gap (note 1). It is a trade-off of the pose Rega asked for, not a construction fault.

## Notes (up to 3, none blocking)

1. **Silhouette gap** (Fact plus Opinion): at 64 px the arm/body gap is under 1 px in rows 50-53 (3/4) and nearly closed at row 49 (front). The read still holds at 56 px in-game. If Rega or the Illustrator seat wants the v4 negative space back, the cheapest move is about 3-4 degrees more arm angle or about 1 cm more case offset outward; do not move the fist above the case.
2. **Inner sleeve edge** (Opinion, not a regression): over the torso in front, 3/4 and side the sleeve's inner edge has no ink and reads only by its shade band, so in 3/4 the upper arm merges with the torso. Fine at game size; only worth fixing if the card uses the 3/4 view at large size.
3. **Triangle margin** (Fact): offer_joy is still 20 triangles under the cap. Any rig loop for the elbow bend or the hop must take triangles from somewhere else first.
