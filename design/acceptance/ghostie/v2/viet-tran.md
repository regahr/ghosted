# Ghostie v2: Viet Tran (3D design lead), items V1-V6

- Date: 2026-11-25. Judge seat. I did not build v2. I judged from the PNGs. `selfcheck.md` and `changes.md` are claims only.
- All paths are under `design/assets/ghostie/` unless shown otherwise.

## Offer (my own tools)

- `3dviz-pro-max/templates/checklists/visual-anti-slop.md`, items 1-7: V1-V4 are scored against these (silhouette, joins, detail at view size, material identity).
- `3dviz-pro-max/references/object-craft.md`, "choose continuity at the join": I used it to judge the arm-to-body join. The arm is a separate part on a collar. The join must read as one flap, not a part stuck on.
- `3dviz-pro-max/references/subject-clarity-and-motion.md`: I used it for the 26 m read. A landmark that reads as the wrong part (tie as mouth, arms as ears) is a clarity fault.
- The brief blocks no tool of mine. I ran local Python (PIL) pixel samples and a read of the glTF node list. I changed no asset.

## v1 faults: fixed or not

1. Faceted outline (v1 fix 1): **partly fixed.** Fact: `hero.png` crown has about 14 straight segments with visible corners (for example x 400-440, y 340-410 and x 780-840, y 330-410). Fact: `crops/hem-notch-34.png` shows 3 straight segments with 2 sharp corners, not a round scallop. Fact: `crops/eye-far-34.png` eye is a 12+ sided oval and reads round. The builder agrees (`selfcheck.md`, still weak 1).
2. Arms (v1 fix 2): **not fixed.** Fact: `silhouette-64-34-x4.png`: the far arm is gone and the near arm is a small nick on the right edge (about y 150). Fact: `crops/arm-end-on-side.png` and `turn-side.png` (x 405-515, y 630-715): the arm seen end-on is still an octagon patch on the body, with 2 light slivers in the ink. Fact: `crops/arm-root-front.png`: a pale vertical strip (the collar end) shows between the body and the arm, so the join reads as a peg in a socket. Fact: `hero.png`, `turn-34.png`: the near arm is a hexagon with a pointed tip, not a round mitten.
3. Headset band (v1 fix 3): **fixed, with a small mark.** Fact: `crops/headset-band-over-crown.png`: the band now ends under the ink and the crown line is unbroken. A thin light line shows above the ink (about x 190-270, y 100). Fact: `variants.png` headset panel: the ear cup is a hexagon, and its ink is open at the lower left (about x 1550-1580, y 340-360).
4. Off-white in game (v1 fix 4): **fixed.** Fact: pixel sample `lineup-grass.png` (717,435) and (764,462) = RGB 231,211,179, hue 37. The v1 sample at (764,462) was 233,208,203 (pink). Fact: `lineup-grass-crop-x3.png`, `lineup-path-crop-x3.png`: the ghosts read cream, not pink.

## Scores

- **V1 read: FAIL.** Fact: `silhouette-64-x4.png`: the front reads as a ghost (dome, 2 arm bumps, wavy hem). Fact: `silhouette-64-34-x4.png`: in 3/4 the shape is a bell with a nick, the same fault as v1. The fix brief asked for arms "still visible in the 3/4 silhouette" (`fix-brief-v2.md`, fix 2). Fact: `lineup-grass-crop-x3.png`: from the 26 m camera the hem is hidden, and the high side arms sit where ears sit. Opinion: the ghosts read as bald heads with ears more than as ghosts.
- **V2 construction: FAIL.** Fact: `crops/arm-end-on-side.png`: octagon patch, 2 light slivers in the ink. Fact: `crops/arm-root-front.png`: pale collar strip at the root. Fact: `turn-front.png` (x 230-245, y 575-640) and `turn-back.png` (x 205-215, y 615-670): the same pale strip on both arms. Fact: `hero.png` (x 340-360, y 730-770): a doubled outline sliver at the left hem. Fact: `crops/eye-on-surface-front.png`, `crops/glasses-on-surface-front.png`, `crops/tie-on-surface.png`: no cut-through. That part holds.
- **V3 detail at real size: FAIL.** Fact: `hero.png`: crown corners, a hexagonal arm tip, hexagonal glasses frames in `variants.png`. Opinion: at card size this is still the "code model" look Rega called slopped. It is better than v1, but it does not look hand-made. Fact: `lineup-grass-crop-x3.png`, `lineup-path-crop-x3.png`, first ghost: the tie is a lilac mark just under the eyes at the chin. Opinion: at 26 m it reads as an open mouth or a tongue, not a tie. The glasses read only as a thin line, and the headset as a faint arc. These match the builder's own notes (`selfcheck.md`, I3 and still weak 5).
- **V4 toon and material: PASS.** Fact: `hero.png` lit body (600,400) = RGB 244,229,201, hue 39. The cream cast is accepted by the chair ruling. Fact: `lineup-grass.png` shade sample = RGB 231,211,179, hue 37: neutral band, within ±15° of lit hue, no pink. Fact: `turn-front.png`, `hero.png`, `turn-back.png`: 2 bands, hard edges, no acne, streaks or blotches.
- **V5 budget and meshes: FAIL (mesh count only).** Fact: `ingame_report.json` `visibleTris`: tie 430, glasses 426, headset 442, all at most 450. Fact: `ghostie.glb` has 8 meshes: `body`, `arm_collars`, `arm_L`, `arm_R`, `eyes`, `acc_tie`, `acc_glasses`, `acc_headset`. With the eyes and the accessories exempt as swap parts (chair amendment, `acceptance/checklist.md` V5), 4 meshes stay: body, arm_collars, arm_L, arm_R. The rule is at most 3. Opinion: this is cheap to fix. Merge `arm_collars` into `body`, because the collar is fixed to the body (`selfcheck.md`, E2).
- **V6 in-game = Blender: PASS.** Fact: `compare-ingame.png`: shape and colour match. The difference shows only on outline edges. The label says mean 0.75/255, 0.29% px over 40. Fact: the v1 broken outline at the far arm top is not seen in the three.js panel.

## Fix list (narrowest)

1. **Arms (V1, V2, V3).** Make each arm a round mitten (no hexagon tip), with no pale collar strip at the root. Turn the near arm out about 20-30° toward the camera in the rest pose and lower both a little, so they break the 3/4 silhouette and do not sit at ear height from the 26 m camera. Proof: `silhouette-64-34-x4.png` (near arm reads as an arm), `crops/arm-root-front.png` and `turn-back.png` (no pale strip), `crops/arm-end-on-side.png` (no octagon patch, no slivers), `lineup-grass-crop-x3.png` (not ears).
2. **Merge `arm_collars` into `body` (V5).** Proof: the `ghostie.glb` node list shows at most 3 non-swap meshes. The triangle count is unchanged.
3. **Round the crown and the hem (V3).** Use the 8 spare triangles, or move triangles from the hidden hem cavity to the profile rings, so `hero.png` shows no crown corners and `crops/hem-notch-34.png` shows a curve. Use 8-sided or round frames on the glasses and the ear cup. Proof: `hero.png`, `variants.png`, `crops/hem-notch-34.png`.
4. **Tie must not read as a mouth (V3).** Move it lower and make it read as a tie at 26 m (for example a darker ink knot), or accept a different chest mark. BMGD owns the call. Proof: `lineup-grass-crop-x3.png`, `lineup-path-crop-x3.png`.
5. **Small seams (V2).** Close the ear cup ink (`variants.png`) and the left hem sliver (`hero.png`, x 340-360, y 730-770). Proof: the same files.

**Overall: FAIL** (V1, V2, V3, V5 fail; V4, V6 pass)
