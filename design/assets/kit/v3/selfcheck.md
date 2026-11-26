# Kit v3: self-check against the acceptance checklist

- Date: 2026-11-25. Builder: Viet Tran seat.
- This is the builder's check. The 5 seats score again, each on its own.
- Rule for this file: each claim names a render or a measured number. Where I only saw a thing at zoom, I say so.
- `v2/` holds the previous build. `changes.md` lists each fix.

Result: **all 15 must items PASS**, by my own check. The weak points are listed at the end.

## Viet Tran: shape and build

| Item | Result | Evidence |
|---|---|---|
| V1 reads correctly | PASS | `turn-front.png` and `turn-34.png`: a round head on a pear-shaped body, with a gap between the legs and a gap between the free arm and the body. In `silhouette-64-34-x4.png` the case is separated from the leg by background (this was not so in v2). Height to the hair top is 0.977 m, 2.71 head-heights (`build_report.json`). |
| V2 no cut-through, no floating parts, no gaps | PASS | The 3 joins that failed in v2 now have automated checks in `build_report.json` `checks`. **Hem on shoe:** `leg_verts_below_collar_outside_shoe` 0 and `leg_verts_above_collar_inside_shoe` 0; `turn-back.png` shows flat round hem rings on the shoes. **Crotch:** `leg_verts_in_seat_outside_trousers` 0 and `leg_verts_between_inside_trousers` 0; `turn-back.png` shows no outline whiskers. **Grip:** 4 bar sections are inside the fist; the deepest is 20.7 mm and the 2 exit sections are 4.6 mm, one per side; 2 sections show on each side. `turn-34.png` and `hero.png` show a handle loop under the fist. **Hair:** the edge is 2.3 to 3.9 mm above the skin and the tuck ring is 4.6 mm inside the head. `turn-side.png` at 4x zoom shows one ink line at the sideburn and no skin sliver. **Others:** case against torso, legs, shoes and sleeve = 0; both hands against torso = 0. Contacts that are there on purpose: the head rests in the collar, and the tie tucks under the collar points. |
| V3 detail at the real view size | PASS | `ingame-world-crop-x3.png` and `ingame-world-grass-crop-x3.png`: at the 26 m camera Kit is 56 px tall (`ingame_report.json`). The hair, sprout, shirt, tie and case all read. `expr-gamecam-strip.png` shows the 5 expressions at that camera; there the sprout is what changes (up, flat, bent, up, tall). `expr-card-strip.png` shows the faces at 160 px. |
| V4 toon bands, clean shadows | PASS | `toon.json`: props use 2 bands with the terminator at N.L = 0, and skin uses 3 bands. `turn-34.png`: the shirt front and flank are one lit area, with no angular wedges across the flank. `turn-front.png`: the case is flat-shaded with a chamfer, and its front is one colour with no diagonal. No shadow maps, so no acne. A small shadow sliver remains on the back of the sleeve in `turn-34.png` (see the weak points). |
| V5 visible hero ≤ 2,500 triangles, measured in three.js | PASS | `ingame_report.json` `visibleTris` counts every visible hero mesh, the active `face_<expr>` and `eyes_<expr>` included, and leaves out the outline hulls and the blob. Results: hopeful 2,466, ghosted 2,462, rejected 2,452, focused 2,466, offer_joy **2,481 (max)**. `build_report.json` `visible_hero_max` is also 2,481. Meshes: body 1,292, head and hair 762, case 182, plus the sprout (84) and the active face set (chair ruling). |
| V6 in-game matches Blender | PASS | `compare-ingame.png`, `compare-ingame-front.png` and `compare-ingame-expr-ghosted.png`. Mean absolute difference on figure pixels (`compare_report.json`): 2.2, 2.1 and 2.1 out of 255. 1.1% to 1.3% of pixels differ by more than 40, all at anti-aliased outline edges. |

## Illustrator

| Item | Result | Evidence |
|---|---|---|
| I1 64 px silhouette: head, sprout, case | PASS | `silhouette-64.png` / `-x4.png`: a round head, a thicker curled sprout, and the case as a box with its handle loop. The 3/4 version `silhouette-64-34.png` now also keeps the case apart from the leg. |
| I2 hand-made shapes | PASS | `hero.png` and the turnarounds show: hem lip, tapered sleeves with a cuff, collar band with 2 points, knotted and pointed tie, 4 fringe locks, pointed sideburns, 3 nape points (`turn-back.png`), curled sprout, an upright fist and an open hand with a thumb lobe, shoes with a sole and collar, trouser hems, a chamfered case with a handle loop, mounts and clasps, and a "C" mark on the badge. |
| I3 expressions differ at card size | PASS | `expr-card-strip.png`: hopeful (oval eyes, smile, cheeks), ghosted (dot eyes, flat mouth, sweat drop, flat sprout), rejected (^ ^ eyes, wide smile, sweat drop), focused (half-height eyes with a lid line, angled brows, small offset mouth), offer-joy (big eyes with 2 highlights, open mouth with tongue, tall sprout). Focused and ghosted no longer share dot eyes (`expr-focused.png`). |
| I4 [should] own design | PASS (Opinion) | Generic office pawn. I know no character it copies. |

## Lena Park

| Item | Result | Evidence |
|---|---|---|
| L1 3:1 or an outline | PASS | The shirt is 2.91:1 on grass and 3.26:1 on path; the ink outline is 9.90:1 and 11.08:1 (computed, WCAG). `ingame-world-grass-crop-x3.png` shows the outline closed around Kit on grass, and `ingame-world-crop-x3.png` on the path. |
| L2 hero, ghost and recruiter in greyscale | PASS (computed only) | `grey.png`: the shirt is mid grey (L 0.171). The ghost (0.91) and the recruiter (0.03) are Lena's numbers. The ghost and recruiter are still not modelled, so no joint render exists. |
| L3 palette colours | PASS | Every Kit colour is in the palette: shirt #14, skin #15, hair #25, legs #26 (`seats/lena-park.md` lines 46-47), tie #7 `#D4503A`, wood #5, panel #23, gold #13, ink #22, cheeks #6, tongue #7, sweat #8. |

## BMGD

| Item | Result | Evidence |
|---|---|---|
| B1 matches the bible | PASS | `hero.png`: pawn toy, blue shirt, red tie, case, lanyard badge (now with the Crunchr "C"), sprout, and the 5 expressions (`expr-*.png`). |
| B2 comic and kind | PASS | `expr-card-strip.png`: the low states are deflated, not crying; "rejected" smiles. |

## Emil Kowalski

| Item | Result | Evidence |
|---|---|---|
| E1 rest pose alive | PASS (Opinion) | `turn-front.png` and `hero.png`: the case shoulder sits 1 cm lower, the free hand comes forward with an open palm, Kit's right foot toes out 9 degrees, and the head tilts toward the case. |
| E2 [should] rig | PASS | `kit.glb` nodes: root > bounce > body > head > face_<expr>, eyes_<expr> (pivot on the eye line, so `scale.y` blinks; `ingame.html` `blink()`), sprout (pivot at its root). The briefcase pivots at the grip. |

## Weak points (honest)

- `turn-34.png`: a thin shadow sliver on the back of the case-side sleeve still follows the 8-sided sleeve facets. It is small, but a strict V4 reader may flag it.
- The head outline shows facets in the 600 px close-ups (22 segments). The triangle budget is used up: 2,481 of 2,500.
- At the 26 m camera, hopeful and focused look the same (`expr-gamecam-strip.png`), because only the face differs and it is too small there. Ghosted reads as a flat sprout, not a hanging one: the hair stops a larger droop (3.7 mm clearance at 80 degrees).
- The legs below the trouser seat are short (about 9 cm show).
- There is still no animation; the rig is only ready for it.
