# Kit v4: self-check (builder)

- Date: 2026-11-25. Builder: Viet Tran seat.
- The seats score again, each on its own.
- Rule: a claim names a file. Join claims name a 2x crop in `crops/`. Where I could not see the thing, I write "not shown". v3 is in `v3/`, and `changes.md` lists the v4 edits.

Result: by my check, **all 15 must items pass**. The weak points are listed at the end.

## Viet Tran (V1-V6)

| Item | Result | Evidence |
|---|---|---|
| V1 read | PASS | `turn-front.png`, `turn-34.png`, `silhouette-64-x4.png`: round head, sprout, a gap between the legs, and the case clear of the body. |
| V2 construction | PASS | **Grip:** `crops/grip-front-v3-v4.png`, `grip-back-v3-v4.png`, `grip-side-v3-v4.png`, `grip-hero-v3-v4.png`. In v4 the fist outline is closed and the handle legs leave from under the fist. `build_report.json`: handle vertices outside the fist above its equator = 0. **Sleeve cap:** `crops/sleeve-side-v2-v3-v4.png`, v4 shows a closed, outlined cap like v2. **Hems:** `crops/hems-back.png`, a round hem ring on each shoe, with leg/shoe checks all 0. **Temple:** `crops/temple-side-v3-v4.png`, no skin wedge and no skin sliver along the edge. **Other contacts:** case against torso, legs, shoes and sleeve = 0. |
| V3 detail at real size | PASS | `ingame-world-crop-x3.png`, `ingame-world-grass-crop-x3.png` (Kit 56 px at the 26 m camera), `expr-gamecam-strip.png`, `expr-card-strip.png`. |
| V4 toon bands | PASS | Not edited in v4. `turn-34.png` and `turn-front.png`: 2 bands on props and 3 on skin, no acne. A thin shadow strip on the back of the case-side sleeve in `turn-34.png` is still there (see the weak points). |
| V5 visible ≤ 2,500 in three.js | PASS | `ingame_report.json` `visibleTris`: max 2,480 (offer_joy), min 2,451 (rejected). Hero meshes: body, head, briefcase, plus the sprout and 1 face set and 1 eye set. |
| V6 in-game matches Blender | PASS | `compare-ingame.png`, `compare-ingame-front.png`, `compare-ingame-expr-ghosted.png`. `compare_report.json` mean is 2.0-2.2 out of 255, with 1.1-1.4% of pixels over 40 (outline edges). |

## Illustrator (I1-I4)

| Item | Result | Evidence |
|---|---|---|
| I1 64 px silhouette | PASS | `silhouette-64-x4.png`: round head, sprout and case box. `crops/sil34-rows40-63.png` and `sil34-rows.json`: in the 3/4 silhouette, rows 48-61 have background between the leg and the case. |
| I2 hand-made shapes | PASS | `hero.png`: hem lip, cuffs, collar points, knotted tie, fringe locks, curled sprout, handle loop, chamfered case. `turn-back.png`: 3 nape points. |
| I3 expressions at card size | PASS | `expr-card-strip.png`. Not edited in v4, except the sprout poses. |
| I4 [should] own design | PASS (Opinion) | No change. |

## Lena Park (L1-L3)

| Item | Result | Evidence |
|---|---|---|
| L1 | PASS | `ingame-world-grass-crop-x3.png` and `ingame-world-crop-x3.png`: the ink outline is closed around Kit on grass and on path. |
| L2 | PASS (computed only) | `grey.png`. The ghost and the recruiter are not modelled, so no joint render exists. |
| L3 | PASS | No colour changes in v4. All colours are palette #5-#26 (see `build_kit.py` PAL). |

## BMGD and Emil

| Item | Result | Evidence |
|---|---|---|
| B1 | PASS | `hero.png`. |
| B2 | PASS | `expr-card-strip.png`. |
| E1 | PASS (Opinion) | `turn-front.png`, `hero.png`: uneven stance as in v3, with the case hand 3 cm further out. |
| E2 [should] | PASS | `kit.glb`: root > bounce > body > head > face_*, eyes_*, sprout. The sprout extras now include `sprout_scale_three_xyz`. |

## Sprouts at game size (BMGD note)

`expr-gamecam-strip.png`: hopeful has the curl, ghosted lies flat, rejected leans to the other side, focused is a thin straight spike, and offer-joy is the tallest curl. At 1x, the focused spike is thin (1-2 px). It reads as "no curl", not as a strong shape.

## Weak points

- Grip, side view (`crops/grip-side-v3-v4.png`): the 2 handle legs leave 2 short outline ticks at the fist's lower edge. That is their own outline, not a cut, but it is busier than the other views.
- `turn-34.png`: a thin shadow strip on the back of the case-side sleeve follows its 8 sides (not changed in v4).
- The head outline shows facets in the close-ups. The budget is used: 2,480 of 2,500.
- The case hand now sits further from the body, and the arm angles out more than in v3 (`turn-front.png`). This was done for the 3/4 gap.
- Nothing is animated.
