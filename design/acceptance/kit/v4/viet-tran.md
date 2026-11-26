Viet Tran (3D Design Lead (3DViz Pro Max)): GHOSTED acceptance gate, Kit v4, items V1-V6

## Offer

- `3dviz-pro-max/templates/checklists/visual-anti-slop.md` items 1-7. **Fact**: V1-V6 come from this source (`design/acceptance/checklist.md`, the "Source:" line under "Viet Tran"). I used item 1 (read), item 2 (construction), item 3 (detail at real scale) and items 4-6 (material, surface, light).
- `3dviz-pro-max/references/object-craft.md#choose-continuity-at-the-join` and `#diagnose-deformation-at-the-region-that-fails`. These set how I checked: each v3 fault is at one join (fist/handle, sleeve/torso), so I checked that join from all 4 turn angles, and then the joins next to it that the fix could move (case/leg, handle/case, sleeve/hand).
- Tools I ran: I opened every turn, hero, expression, in-game and compare render myself. I made 2.5-8x nearest-neighbour crops with `magick` in the scratchpad (not saved in the project). I sampled pixel values at the temple lock. I printed both 64 px silhouettes as ASCII. I parsed `kit.glb` for nodes and triangle counts. I did not use `changes.md` or `selfcheck.md` as evidence. I used the builder's `crops/*-v3-v4.png` only to compare against my own crops.
- Conflict note: an earlier instance of this seat built Kit. I scored as an outside judge, from pixels and the glb only.

## Check of my v3 faults, and of the other v4 fixes

| Fault | v4 status | Evidence |
| --- | --- | --- |
| V2: the handle leg broke out through the fist face (front, back, side, hero) | **Gone** | **Fact** (seen): 4x crops of `turn-front.png` (660,720), `turn-34.png` (600,740), `turn-side.png` (340,740) and `turn-back.png` (100,720). In each, both handle legs go into the bottom of the fist. No brown shows on the fist face. `crops/grip-side-v3-v4.png` agrees. |
| V2: the sleeve lost its shoulder cap in `turn-side.png` | **Gone** | **Fact** (seen): a 2.5x crop of `turn-side.png` (300,500) shows a closed, outlined cap, the same shape as v2 (`crops/sleeve-side-v2-v3-v4.png`). `build_report.json` "sleeves_in_torso": 0 (v3 was 8). |
| Case touched the leg in the 3/4 silhouette | **Gone** | **Fact** (my ASCII of `silhouette-64-34.png`): rows 50-61 have a 2-4 px background gap between the leg and the case. |
| Temple slab | **Gone, small new seam** | **Fact** (seen, and pixel sample): the lock in `turn-side.png` now ends in a slanted point, not a vertical slab. But a 1 px mid-tone line (#7D5A39, #A37B53, #835F3E) runs between the ink (#231102) and the hair (#402003) along about 35 px of the lower lock edge (x 377-383, y 340-375). v3 did not have it. |
| Sprout per expression | **Works** | **Fact** (seen): `expr-card-strip.png` shows 5 sprout poses (curl, flop, droop, straight, tall). One `sprout` mesh is posed from face-node extras (`ingame.html` lines 74-75). `compare-ingame-expr-ghosted.png` shows the same flop in Blender and three.js. The ghosted flop lies on the hair with an ink line along it and does not cut into it. |

## Regression check (what the fix could break)

- Case arm now angles out: **Fact** (seen) `turn-front.png` and `hero.png`: the sleeve meets the torso with no gap at the armpit, and the case hangs clear of the leg. **Opinion**: the arm reads as holding a weight away from the body. That is acceptable.
- Handle mounts removed: **Fact** (seen) `turn-34.png` 4x: both legs go into the case top with a closed ink line. In `turn-back.png` 4x the two legs overlap end-on and read as one slanted strap, with a small ink wedge where it meets the case top. **Opinion**: this is a read limit of the angle, not a cut-through.
- Collar columns removed: **Fact** (seen) a 3.5x crop of `turn-back.png` (320,490), against the same crop of `v3/turn-back.png`: the collar band is the same, with a slightly more faceted lower edge. No gap or show-through.
- Hair: **Fact** (seen) the nape in `turn-back.png` and the fringe in `turn-front.png` are closed shapes with outlines. The only new hair fault is the 1 px temple seam above.
- Sleeve inner edges in `turn-side.png` have no ink for about 80 px where the sleeve lies on the torso. **Fact**: v2 shows the same (`crops/sleeve-side-v2-v3-v4.png`, left panel). It is not a regression.

## Scores

| Item | Verdict | Evidence |
| --- | --- | --- |
| V1 read: silhouette, proportions, negative space | **PASS** | **Fact** (ASCII): `silhouette-64.png` rows 44-59 have a 4-8 px gap between the body and the case, plus a round head and a hooked sprout (rows 0-6). `silhouette-64-34.png` rows 50-61 now have a 2-4 px gap between the leg and the case. |
| V2 construction: no cut-through, no floating parts, no gaps | **PASS** | **Fact** (seen): the grip is clean in all 4 turns and the hero; the sleeve cap is closed in the side view. Nothing floats; the sweat drop and the card sit on their surfaces. **Opinion**: the 1 px temple seam is a polish item. It is not visible at 56 px in-game or at card size, so it does not fail the item. |
| V3 detail at real view size (26 m camera, card close-up) | **PASS** | **Fact** (seen): `expr-gamecam-strip.png` and `ingame-world-grass-crop-x3.png` at 56 px (`ingame_report.json` "kitPx": 56): the sprout, blue shirt, red tie and case read in all 5 expressions. `expr-card-strip.png` shows 5 faces and 5 sprout poses that differ at card size. |
| V4 toon: 2 bands on props, 3 on faces, clean shadows | **PASS** | **Fact** (seen): `turn-front.png` and `compare-ingame-expr-ghosted.png` show 3 curved bands on the face. The shirt, case and shoes have 2 bands. My 2.5-4x crops show no acne, streaks or blotches. `build_report.json` "bands2"/"bands3" agree. |
| V5 at most 2,500 visible triangles in three.js; at most 3 meshes (swap parts excluded) | **PASS** | **Fact** (my parse of `kit.glb`): meshes body 1,321, head 736, briefcase 178 (3 meshes); swap parts: sprout 84 plus `face_*`/`eyes_*`. Max active set offer_joy: 2,319 + 69 + 92 = **2,480**. Min: rejected 2,451. `ingame_report.json` "visibleTris" agrees (2,451-2,480). |
| V6 in-game matches Blender in shape and colour | **PASS** | **Fact** (seen): `compare-ingame.png` and `compare-ingame-expr-ghosted.png` match in silhouette, sprout pose, tie, case, hues and band placement. `compare_report.json` "mean" 2.0-2.2. |

**Overall: PASS.** All six must items pass. Both v3 faults are gone in every view, and the 3/4 case gap now shows in the silhouette. I found one small new fault (the temple seam) and no regression that fails an item.

## Fix notes (up to 3, none blocking)

1. **Temple seam** (Opinion): close the 1 px mid-tone line on the lower lock edge in `turn-side.png` (x 377-383, y 340-375). Move the lock's front edge verts about 1 mm into the hair shell, or let the lock's inner face meet the head skin, so the outline has no light line inside it.
2. **Triangle margin** (Opinion): offer_joy is 20 triangles under the cap. Any later change (rig loops for the hop, a new expression) must take triangles from somewhere else first. Keep `visible_hero_max` as a build check that fails at more than 2,500.
3. **Back-view handle** (Opinion): in `turn-back.png` the handle reads as one strap. If Rega's card uses a back or rear-3/4 view, turn the case about 10 degrees about its vertical axis so both legs show. Otherwise leave it.
