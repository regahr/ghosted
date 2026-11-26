Viet Tran (3D Design Lead (3DViz Pro Max)): GHOSTED acceptance gate, Kit v2, items V1-V6

## Offer

- `3dviz-pro-max/templates/checklists/visual-anti-slop.md` items 1-7. **Fact**: these are the source of V1-V6 (checklist.md, line "Source: ... items 1-7"). I used items 1 (read), 2 (construction), 3 (detail at real scale), 4-6 (material, surface, light) as my lens.
- `3dviz-pro-max/references/object-craft.md#choose-continuity-at-the-join` and `#diagnose-deformation-at-the-region-that-fails`. They change the fix notes for V2: the faults sit at joins (hand/handle, pants/shoes, hair/skin), so the fix is per join, not a global cleanup.
- Tools run: I opened every render myself, made 3-4x nearest-neighbour crops in the scratchpad (not saved in the project), and parsed `kit.glb` for node, mesh and triangle counts. I did not use the selfcheck as evidence.

## Scores

| Item | Verdict | Evidence |
| --- | --- | --- |
| V1 read: silhouette, proportions, negative space | **PASS** | **Fact** (seen): `silhouette-64-x4.png` shows round head, hooked sprout and a separate briefcase with a gap to the leg; `turn-front.png` reads as a chunky office kid at 2.71 heads (`build_report.json` "head_heights": 2.71), with clear leg gap and arm-to-body gap on the briefcase side. |
| V2 construction: no cut-through, no floating parts, no gaps | **FAIL** | **Fact** (seen): `turn-back.png` crop of the pant hems at the shoes shows a ragged saw-tooth where the pants cut into the shoes, plus black outline "whiskers" sticking out sideways at the crotch; `turn-front.png` and `turn-back.png` show a ragged brown/skin tear where the handle cuts through the hand (no handle shape is visible); `turn-side.png` shows the hair shell ending in a hard vertical slab at the temple with a light sliver gap between hair and skin. |
| V3 detail at real view size (26 m game camera, card close-up) | **PASS** (weak) | **Fact** (seen): `ingame-world-crop-x3.png` still reads sprout, blue shirt, red tie and briefcase at game size; `expr-card-strip.png` reads all 5 faces at card size. **Opinion**: the lanyard and badge are sub-pixel noise at 26 m, and the head outline shows its 22 facets in `hero.png` / `turn-front.png`. |
| V4 toon style: 2 bands props, 3 bands face, clean shadows | **FAIL** | **Fact** (seen): the face carries 3 clean curved bands (`turn-front.png`), but `turn-34.png` shirt shows angular dark wedges down the lower-left and right flank that follow the low-poly facets, not the form; `turn-front.png` briefcase front is a flat panel split by a diagonal light/dark triangle in its lower-left corner (a normal-interpolation streak on a flat face). These are the "streaks or blotches" the item bans. |
| V5 triangles at most 2.5k for the hero; at most 3 meshes (swap parts excluded, chair amendment) | **FAIL** (triangles; mesh count passes) | **Fact** (parsed `kit.glb`): mesh nodes body 1,431, head 730, briefcase 236 (= 3 meshes, PASS under the amendment), sprout 84, face sets 160-312. The hero on screen is body + head + briefcase + sprout + 1 face set = 2,641 to 2,793 triangles, above 2,500. The 2,481 in `build_report.json` "hero_total" leaves out the face set, which is always drawn. The amendment changes only the mesh count, not the triangle budget. |
| V6 in-game matches Blender in shape and colour | **PASS** | **Fact** (seen): `compare-ingame.png`, `compare-ingame-front.png` and `compare-ingame-expr-ghosted.png` show the two sides matching in silhouette, sprout curl, tie, briefcase, hues and band placement; I find no visible difference beyond outline anti-aliasing. |

**Overall: FAIL.** Must items V2, V4 and V5 fail. V1, V3 and V6 pass.

## Fix notes (up to 3)

1. **V2, joins** (Opinion): model a real handle arc that the mitten closes over (mitten fingers wrap the bar, no through-cut), give the pant hems a cuff that ends just above the shoe collar instead of a tube sunk into the shoe, and close the hair shell at the temples with a tapered sideburn lock that is shrinkwrapped to the skull. Add pairwise checks for pants vs shoes, hand vs handle and hair vs head to `build_report.json` "checks"; the current checks do not cover the three joins that fail.
2. **V4, shading** (Opinion): mark the briefcase panels flat (split normals / auto-smooth by angle so each flat face has one normal) and give the shirt a smoothed custom normal set (data-transfer from a subdivided copy, or weighted normals) so the 2-band terminator follows the barrel of the torso as one clean curve. Kill the outline whiskers by capping open edges or welding the hull at the crotch.
3. **V5, budget** (Opinion): free about 300 triangles from the body (1,431 over 7 primitives): cut back-of-shoe, inner-leg and under-shirt loops nobody sees from a top-down 26 m camera, then spend a part of the saving on 26-28 head segments so the round head stops showing corners in the card close-up. Report "hero_total" with the heaviest face set (offer_joy, 312) included.

Decision note: if the chair or Rega wants face sets left out of the triangle budget the same way they are left out of the mesh count, that is a checklist amendment, not my call. My pick is to keep them in, because they are drawn every frame.
