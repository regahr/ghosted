# Ghostie v3: Viet Tran (3D design lead), items V1-V6

- Date: 2026-11-25. Judge seat. I did not build v3, and I judged from the PNGs only. `selfcheck.md` and `changes.md` are claims.
- Paths are under `design/assets/ghostie/` unless shown otherwise. Zoom crops I made to look closer are in my scratchpad only. I changed no asset.
- SK and S1 are not scored (Rega's ruling: the Ghostie is exempt from the sketch stage).

## Offer (my own tools)

- `3dviz-pro-max/templates/checklists/visual-anti-slop.md`, items 1-7: I score V1-V4 against them.
- `3dviz-pro-max/references/object-craft.md`, "choose continuity at the join": I use it for the arm-to-body join.
- `3dviz-pro-max/references/subject-clarity-and-motion.md`: I use it for the 26 m read. A part that reads as a different part (arms as ears) is a clarity fault.
- The brief blocks none of my tools. I used PIL zoom crops and a read of the `ghostie.glb` JSON.

## v2 faults: fixed or not

1. Arms (v2 fix 1): **partly fixed.**
   - Fact: `turn-front.png` (both arms) and `turn-back.png`: the flaps droop about 30-40° and have no collar. The pale collar strip of v2 is gone.
   - Fact: `crops/arm-root-front.png`: a pale wedge and a hairline still show between the flap's lower ink and the body ink.
   - Fact: `variants.png`, all 3 panels, under the near arm (about x 435-450, y 485-520): a dark ink hook. It shows at card size.
   - Fact: `turn-side.png` (x 420-495, y 650-750) and `crops/arm-end-on-side.png`: seen end-on, the arm is a hook shape with ink on one side and hairlines on the other. It reads as a slot cut into the body.
   - Fact: `lineup-grass-crop-x3.png`, all 3 ghosts: the arms are small pointed nubs, level with the eye dots and nearly horizontal. The builder agrees (`selfcheck.md`, still weak 4).
2. Merge `arm_collars` (v2 fix 2): **fixed.** Fact: `ghostie.glb` meshes: acc_glasses, acc_headset_band, acc_headset, acc_tie, arm_L, arm_R, body, eyes. With the eyes and accessories as swap parts, 3 meshes remain: body, arm_L, arm_R.
3. Round crown and hem (v2 fix 3): **mostly fixed.** Fact: `hero.png`: the crown is a run of short segments with soft corners. `variants.png` at card size: the crown and shoulders read as curves. Fact: `crops/hem-notch-34.png`: the notch top is still a peak with 2 short bevels, not a curve. Opinion: at card size the hem reads wavy, so the notch peak is minor.
4. Tie as mouth (v2 fix 4): **fixed.** Fact: `lineup-grass-crop-x3.png` and `lineup-path-crop-x3.png`, left ghost: 2 eye dots, and a lilac diagonal on the upper right. Nothing is centred below the eyes.
5. Small seams (v2 fix 5): **partly fixed.** Fact: `hero.png` (x 340-360, y 730-770): the v2 doubled sliver is gone. Fact: `crops/headset-cup-on-surface.png`: the cup ink is doubled on the right edge, with a pale sliver between the two strokes and a hairline at the lower right. Fact: `turn-back.png` (x 650-690, y 780-820): a doubled ink step at the hem under the right arm.

## Scores

- **V1 read: FAIL.** Fact: `silhouette-64-x4.png`: the front reads as a ghost (dome, 2 drooping flaps, wavy hem). Fact: `silhouette-64-34-x4.png`: the near arm is a small bump at the lower right, and the far arm does not show. Fact: `lineup-grass-crop-x3.png` (left ghost): two pointed nubs stick out level with the eye dots from an egg-shaped dome. Opinion: at the 26 m camera this still reads as a bald head with ears. That is the main v2 fault, and the fix brief says "the arms must not read as ears".
- **V2 construction: FAIL.** Fact: `variants.png` ink hook under the near arm in all 3 panels (seen at card size). Fact: `turn-side.png` end-on arm reads as a slot. Fact: `crops/arm-root-front.png` pale wedge at the root. Fact: `crops/headset-cup-on-surface.png` doubled cup ink. Fact: `hero.png`, `turn-front.png`: eyes, glasses and tie lie on the surface, with no cut-through. Opinion: the hook and the end-on slot are far bigger than the ~1 px limits that Kit carries, so they cannot pass as known limits.
- **V3 detail at real size: FAIL.** Fact: `lineup-grass-crop-x3.png`: the arms read as ears (see V1). Fact: `hero.png` (x 790-890, y 660-745): the near arm tip is a 6-sided wedge with visible corners, not a round mitten. Fact: `variants.png`: the crown, the 8-sided glasses and the 12-sided cup read clean at card size. Fact: `lineup-grass-crop-x3.png`: the tie reads as a diagonal stripe, the glasses as grey rings, and the headset as an arc plus a side bump. Opinion: the body now looks hand-made at card size; the arms do not.
- **V4 toon and material: PASS.** Fact: `hero.png`, `turn-front.png`, `turn-back.png`: 2 bands, hard edges, no acne, streaks or blotches. The cream cast is accepted by chair ruling. Fact: `turn-front.png` (x 230-350, y 750-830): the shade band follows a few facets at the lower left. Opinion: it reads as cloth folds, so it passes.
- **V5 budget and meshes: PASS.** Fact: `ingame_report.json` `visibleTris`: tie 580, glasses 528, headset 580, all at most 600. Fact: my read of `ghostie.glb` gives body 384 + arm_L 42 + arm_R 42 + eyes 24 + tie 88 = 580, which matches. Fact: 3 non-swap meshes (body, arm_L, arm_R).
- **V6 in-game = Blender: PASS, with a known limit.** Fact: `compare-ingame.png`: the shape and colour match; the label reads mean 0.76/255, 0.29% px over 40, mostly on outline edges. Fact: `ingame.png` (about x 230-365, y 620-760) and the difference panel of `compare-ingame.png`: a thin dotted diagonal line on the lower body shows in three.js only. Opinion: it is faint and about 1 px wide, so it is a known limit, not a fail. It is cheap to fix while the arms are reworked.

## Known limits to carry into the build

1. The far arm does not show in the 3/4 silhouette (`silhouette-64-34-x4.png`). Accept: the near arm carries the 3/4 read.
2. The hem notch top is a bevelled peak, not a curve (`crops/hem-notch-34.png`). It reads wavy at card size.
3. A dotted hairline on the lower body in three.js only (`ingame.png`). Fix it if it is cheap; it is not visible at 26 m.
4. Triangle headroom is 20 for the tie and headset variants (580 of 600). Any arm rework must take triangles from the hidden hem cavity, not from the profile.

**Overall: FAIL** (V1, V2, V3 fail; V4, V5, V6 pass)

## Fix list (narrowest, the arms only plus one seam)

1. **Arms must not read as ears at 26 m (V1, V3).** Judge the arm height in screen space from the game camera, not in world z: the flap root and tip must sit clearly below the eye dots in `lineup-grass-crop-x3.png`. Droop the flaps so that from the top-down camera they point down and out, not sideways. Proof: `lineup-grass-crop-x3.png`, `lineup-path-crop-x3.png` (arms below the eyes, not level), `silhouette-64-x4.png` (still reads as a ghost with arms).
2. **Round arm tip (V3).** Give the tip a rounded profile with no visible corner at 1200 px. Take the triangles from the hem cavity. Proof: `hero.png` near arm, `variants.png`.
3. **Arm join seams (V2).** Remove the ink hook under the near arm, the pale wedge at the root, and the end-on slot look (ink both edges of the flap when seen end-on, or hide the inner stroke). Proof: `variants.png` (x 435-450, y 485-520 in all panels), `crops/arm-root-front.png`, `turn-side.png` (x 420-495, y 650-750), `turn-back.png` (x 650-690, y 780-820).
4. **Cup ink (V2).** One ink stroke on the cup's right edge, no pale sliver. Proof: `crops/headset-cup-on-surface.png`, `variants.png` headset panel.

Keep everything else as it is: the body, the crown, the hem, the tie over the shoulder, the frames, the shade band, the float roll and the mesh split.
