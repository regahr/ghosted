# Ghostie v1: Viet Tran (3D design lead), items V1-V6

- Date: 2026-11-25. Judge seat. I did not build this. I judged from the PNGs. The builder notes are claims only.
- All paths are under `design/assets/ghostie/` unless shown otherwise.

## Offer (my own tools)

- `3dviz-pro-max/templates/checklists/visual-anti-slop.md`, items 1-4: V1-V4 are scored against these. Item 4 ("do
  materials have the intended identity?") is why V4 checks the off-white, not only the band count.
- `3dviz-pro-max/references/object-craft.md` ("choose continuity at the join"): the arm-to-body joins are judged with it.
- The brief blocks no tool of mine. I ran one local pixel sample (Python PIL) on the PNGs. I changed no asset.

## Scores

- **V1 read: FAIL.**
  - Fact: `silhouette-64-34-x4.png`: in 3/4 the arms are gone. The shape reads as a bell or a helmet, not a ghost.
  - Fact: `hero.png`: the left arm is a thin sliver beside the body. The right arm is a hard triangle with a jagged inner cut.
  - Fact: `turn-34.png`: the near arm nearly vanishes into the body edge.
  - Fact: `silhouette-64-x4.png`: the front reads as a ghost (dome, arms, 4-lobe hem).
  - Opinion: the arms are the only landmark besides the dome and the hem. Only the front view carries them, so V1 fails.
  - Opinion: the front silhouette (dome, small side arms, scalloped hem) is close to a well-known app-logo ghost. I4 is the Illustrator's call. I flag it.
- **V2 construction: FAIL.**
  - Fact: `variants.png`, headset panel, at the crown (about x 1480-1530, y 175-185): the lavender band breaks the black crown outline.
    `crops/headset-band-over-crown.png` confirms it: the band lies over the ink line. Card size shows this.
  - Fact: `turn-side.png`, centre (about x 390-480, y 600-690): the arm seen end-on is a pentagon pasted on the body,
    with ink on only 2 edges. It reads as a patch, not a flap that grows from the body. `crops/arm-end-on-side.png` confirms it.
  - Fact: `crops/arm-root-front.png`: there is no ink at the top edge of the arm root. The arm fill runs into the body fill.
  - Fact: `compare-ingame.png`, three.js panel (about x 1440-1480, y 545-560): the outline at the top of the far arm is dotted and broken.
  - Fact: `crops/eye-on-surface-front.png`, `crops/glasses-on-surface-front.png` and `crops/tie-on-surface.png`: no cut-through is seen. The builder's claim here holds.
  - Fact: the builder's own report (`build_report.json` `acc_headset_wall_faces_offset` -0.57 mm) shows the ear cup sinks into the body. It is hidden, so I do not count it.
- **V3 detail at real size: FAIL (card size). Game camera: borderline.**
  - Fact: `hero.png`: the crown is 8 straight segments, and each skirt side is 2 straight lines. The eyes are 8-sided polygons (`crops/eye-far-34.png`).
    Opinion: at card size this is the faceted "code model" look that Rega called slopped. It does not look hand-made.
  - Fact: `lineup-grass-crop-x3.png`: at 26 m the ghosts read as ghosts with 2 eye dots. The tie is a faint smudge, the
    glasses are just seen, and the headset band is nearly lost.
  - Opinion: at 26 m this passes for a background NPC. The card-size fail decides the item.
- **V4 toon and material: FAIL.**
  - Fact: `turn-front.png`, `hero.png`: 2 bands, hard edges, no acne, streaks or blotches. This part passes.
  - Fact: pixel sample, lit body in `hero.png` and `turn-front.png` = RGB (244, 228, 199), about `#F4E4C7`. The bible asks for `#F8F4EA` (`design/bible.md` line 30). It reads beige.
  - Fact: `lineup-grass-crop-x3.png` and `lineup-path-crop-x3.png`: the lower half of each ghost is pink-mauve (sample in `lineup-grass.png` at 764,462 = RGB 233,208,203).
  - Opinion: the intended identity is an off-white, opaque ghost. In game it reads as a pink blob. The builder admits this (`selfcheck.md` weak point 3).
- **V5 budget and meshes: PASS.**
  - Fact: `ingame_report.json` `visibleTris`: tie 266, glasses 290, headset 298. All are at most 300.
  - Fact: `build_report.json`: body, arm_L and arm_R are 3 meshes. The eyes and 1 accessory are swap parts (chair amendment, `acceptance/checklist.md` V5).
  - Fact: the headset has 2 triangles spare. Opinion: any V1-V3 fix that adds body columns cannot fit at 300. See decision below.
- **V6 in-game = Blender: PASS.**
  - Fact: `compare-ingame.png` and `compare-ingame-front.png`: shape and colour match. The difference shows only on outline edges. `compare_report.json` mean 0.71/255.
  - Fact: the only shape difference is the broken outline at the far arm top in three.js (see V2).

## Fix list (narrowest)

1. **Round the outline at card size (V3, V1).** Give the body more columns or smoother dome rings so the crown and
   skirt read as curves, not 8 straight segments. Proof: a new `hero.png` and `variants.png`, plus `silhouette-64-x4.png`.
   This needs more triangles (see decision).
2. **Make the arms real flaps (V1, V2).** Give each arm a rounded mitten profile that grows out of the body, with a
   closed outline at the root, and set it so it still breaks the silhouette in 3/4. Proof: `silhouette-64-34-x4.png`
   (arms seen), `turn-side.png` and `crops/arm-end-on-side.png` (no pasted pentagon), `crops/arm-root-front.png` (ink at the root).
3. **Keep the headset band inside the crown outline (V2).** Lower the band, or draw the body ink over it. Proof:
   `variants.png` headset panel and `crops/headset-band-over-crown.png` with an unbroken crown line.
4. **Make it off-white in game (V4).** Lit body near `#F8F4EA`. A neutral cool grey shadow band, not lavender, that
   stays off pink under the Applyside light. Proof: `lineup-grass-crop-x3.png` and `lineup-path-crop-x3.png` read white,
   plus a pixel sample of the lit body in `hero.png`.

## Decision for Rega (budget)

The fixes 1 and 2 do not fit in 300 triangles (headset is at 298).

1. Raise the ghost budget to 450 triangles per variant. 24 ghosts x 450 = 10.8k triangles. **My pick.**
   Opinion: this is small next to one Kit (2.5k), and it buys the round shape that the card needs.
2. Keep 300. Cut the hem rim cavity and the dome ring count to pay for more columns. Opinion: the shape gets rounder
   from the front but flatter on top. It is a risk.
3. Keep 300 and accept the faceted look. Opinion: this repeats what Rega called slopped.

**Overall: FAIL** (V1, V2, V3, V4 fail; V5, V6 pass)
