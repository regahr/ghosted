Viet Tran (3D Design Lead (3DViz Pro Max)): GHOSTED acceptance gate, Kit v3, items V1-V6

## Offer

- `3dviz-pro-max/templates/checklists/visual-anti-slop.md` items 1-7. **Fact**: V1-V6 come from this source (`design/acceptance/checklist.md`, the "Source:" line under "Viet Tran"). I used item 1 (read), item 2 (construction), item 3 (detail at real scale) and items 4-6 (material, surface, light) to judge.
- `3dviz-pro-max/references/object-craft.md#choose-continuity-at-the-join` and `#diagnose-deformation-at-the-region-that-fails`. These shape fix notes 1 and 2: both faults that remain are at one join each (fist/handle, sleeve/torso). The fix is local to that join, not a global pass.
- Tools I ran: I opened every render myself. I made 2-4x nearest-neighbour crops with `magick` in the scratchpad (not saved in the project). I parsed `kit.glb` for its node tree, mesh count and triangle counts. I printed the 64 px silhouettes as ASCII to check the negative space. I did not use `selfcheck.md` or `changes.md` as evidence.
- Conflict note. **Fact**: `assets/kit/changes.md` line 3 says "Builder: Viet Tran seat". So this seat is scoring a build that was made under its own name. I scored from the PNGs only. The chair may want a second 3D read for this reason.

## Check of my v2 faults

| v2 fault | v3 status | Evidence |
| --- | --- | --- |
| V2: the pant hems cut into the shoes; outline whiskers at the crotch | **Gone** | **Fact** (seen): a 3x crop of `turn-back.png` (hems) shows one clean, round, outlined hem ring on each shoe collar. There are no whiskers at the seat in `turn-front.png` or `turn-back.png`. |
| V2: the handle tore through the hand; no handle shape showed | **Reduced, not gone** | **Fact** (seen): `turn-34.png` (3x crop) is now clean: a real handle loop, with both legs going into the fist. But 4x crops of `turn-front.png`, `turn-back.png` and `turn-side.png` all show the top of one handle leg breaking out through the front of the fist. It shows as a ragged brown spike on the skin, with no ink line at the cut. `hero.png` (4x) shows a smaller notch at the left of the fist. |
| V2: the hair ended in a vertical slab at the temple, with a light sliver | **Gone** | **Fact** (seen): a 3x crop of `turn-side.png` shows a pointed sideburn lock with one ink line on its front edge. There is no skin-coloured sliver between the hair and the head. |
| V4: angular dark wedges on the shirt flank (3/4 view) | **Gone** | **Fact** (seen): a 2x crop of `turn-34.png` shows the shirt front and flank as one lit band. The dark band is only at the hem and under the sleeve. |
| V4: a diagonal streak on the flat case front | **Gone** | **Fact** (seen): a 3x crop of `turn-front.png` shows the case front as one flat colour, with a thin chamfer band at the bottom edge only. |
| V5: visible triangles 2,641-2,793, over 2,500 | **Gone** | **Fact** (my parse of `kit.glb`): body 1,292 + head 762 + briefcase 182 + sprout 84 = 2,320. The heaviest face set is offer_joy: face 69 + eyes 92 = 161. 2,320 + 161 = **2,481**, which is not more than 2,500. This agrees with `ingame_report.json` "visibleTris" "offer_joy": 2481. |

## Scores

| Item | Verdict | Evidence |
| --- | --- | --- |
| V1 read: silhouette, proportions, negative space | **PASS** | **Fact** (seen): `silhouette-64.png` (ASCII, rows 47-60) has a 3-5 px background gap between the leg and the case, plus a round head and a hooked sprout. **Fact**: in `silhouette-64-34.png` rows 51-61, the case joins the leg with no gap. This was the same in v2. So the `changes.md` row 6 claim, "the case is separated from the leg by background", is not true for the 3/4 silhouette. **Opinion**: the front read is enough for V1. The 3/4 merge is the Illustrator's I1 call. |
| V2 construction: no cut-through, no floating parts, no gaps | **FAIL** | **Fact** (seen): (a) the handle leg breaks through the fist face with a ragged edge that has no outline, in `turn-front.png`, `turn-back.png`, `turn-side.png` and `hero.png` (crops above). (b) New since v2: in `turn-side.png` (2.5x crop, about x 400-500, y 570-760) the sleeve has lost its shoulder cap. Its top outline is now two loose ink wedges, and the sleeve blue merges into the torso with no ink line for about 250 px. `v2/turn-side.png`, same crop, shows a closed, outlined shoulder cap. **Opinion**: the probable cause is the new culling, `build_report.json` "sleeves_in_torso": 8, which removed the sleeve's top faces and so its hull outline. |
| V3 detail at real view size (26 m game camera, card close-up) | **PASS** | **Fact** (seen): `expr-gamecam-strip.png` shows Kit at 56 px (`ingame_report.json` "kitPx": 56). The sprout, blue shirt, red tie and case read in all 5 expressions. `ingame-world-grass-crop-x3.png` reads on grass. `expr-card-strip.png` shows 5 faces that differ at card size. |
| V4 toon style: 2 bands on props, 3 on faces, clean shadows | **PASS** | **Fact** (seen): `expr-ghosted.png` and `turn-front.png` show 3 clean curved bands on the face (lit, mid, chin). The shirt, case and shoes show 2 bands. I found no acne, streaks or blotches in the 2-3x crops. `toon.json` / `build_report.json` "bands2" and "bands3" agree. |
| V5 at most 2,500 visible triangles; at most 3 meshes (swap parts excluded) | **PASS** | **Fact** (my parse of `kit.glb`): the mesh nodes are body, head and briefcase (3 meshes). The swap parts are sprout, `face_*` and `eyes_*`. The visible maximum is 2,481 (offer_joy) and the minimum is 2,452 (rejected). **Opinion**: the margin is only 19 triangles. Any fix for V2 must stay inside it. |
| V6 in-game matches Blender in shape and colour | **PASS** | **Fact** (seen): `compare-ingame.png`, `compare-ingame-front.png` and `compare-ingame-expr-ghosted.png` match in silhouette, sprout, tie, case, hues and band placement. The grip notch shows on both sides. `compare_report.json` "mean" is 2.1-2.2. |

**Overall: FAIL.** One must item fails: V2. Three v2 faults are gone, and V4 and V5 now pass. V2 fails for two reasons: the handle still breaks through the fist in 3 of 4 turn views, and a new fault (the open sleeve top in the side view) came from the culling pass.

## Fix notes (up to 3)

1. **V2, grip** (Opinion): keep both handle legs inside the fist until they leave through its lower face. Lower the bar top by about 5 mm, or widen the fist along the bar by about 5 mm, so that the 4.6 mm "exit sections" in `build_report.json` do not reach the front and back faces. Add a check that counts handle vertices outside the fist hull above the fist's equator (target 0). Then look at the result in `turn-front.png`, `turn-back.png` and `turn-side.png`, not only `turn-34.png`.
2. **V2, sleeve cap** (Opinion): put back the top ring of the sleeve (cull only faces that are fully inside the torso from every turn angle), or cap the sleeve top so that the inverted-hull outline is closed. Check this in `turn-side.png` against `v2/turn-side.png`. Fix 1 makes the fist bigger or the bar shorter, and fix 2 puts faces back, so take the triangles from the far side of the legs or from the under-seat disc, which a top-down camera never sees.
3. **Evidence hygiene** (Opinion): change the `changes.md` row 6 claim about the 3/4 silhouette, or move the case out until `silhouette-64-34.png` rows 51-61 show a gap. Add `turn-side` and `turn-back` crops of each join to the self-check, because both faults that remain are visible only from those angles.
