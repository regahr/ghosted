# Ghostie v2 fix brief (chair, 2026-11-25)

Gate v1 result: FAIL, 5 of 5 seats (scores in `acceptance/ghostie/v1/`).

## Chair rulings
- Budget: 450 visible triangles per variant (checklist, chair amendment 2). Shown to Rega on card 2.
- Body colour: Lena owns the palette. Her pick 1 stands: `#F8F4EA` lit by the warm world key reads cream, the same shift Kit
  and the panels get. Viet's V4 colour fail is resolved by the shadow fix below, not by a new base colour. Shown to Rega
  on card 2 as an open default.
- Shade band: neutral grey multiplier (178,178,178), like Kit (Lena fix 1, Viet fix 4 agree). No lavender.

## Fixes (each with its proof file)
1. Round outline at card size: more columns and dome rings, no visible corners on crown or sides. Eyes 12-sided.
   Proof: `hero.png`, `variants.png`, `silhouette-64-x4.png`. (Viet 1, Illustrator 1)
2. Arms: rounded flaps that grow out of the body, ink closed at the root and tip, still visible in the 3/4 silhouette.
   Proof: `silhouette-64-34-x4.png`, `turn-side.png`, `crops/arm-end-on-side.png`, `crops/arm-root-front.png`. (Viet 2, Illustrator 3)
3. Hem: rounded scallops, not sharp V notches; keep the 2 notches that read in the front silhouette.
   Proof: `crops/hem-notch-34.png`, `silhouette-64-x4.png`. (Illustrator 2)
4. Headset: band stays inside the crown outline; ear cup larger. Proof: `variants.png`, `crops/headset-band-over-crown.png`,
   `lineup-grass-crop-x3.png`. (Viet 3, BMGD advisory)
5. Tie: moved down to the chest, below the arm line, with a thin ink edge or a darker palette colour (palette rows only,
   `seats/lena-park.md`). It must not read as a mouth or nose at the 26 m camera.
   Proof: `lineup-grass-crop-x3.png`, `lineup-path-crop-x3.png`, `variants.png`. (BMGD required, Illustrator 4)
6. Shade band neutral (178,178,178) in `build_ghostie.py` and `ghost_toon.json`; shade hue within ±15° of lit hue; outline
   still ≥1.6 px. Proof: pixel samples in `lineup-grass.png`, `hero.png`. (Lena)
7. Rest pose (node rotations only): `float` roll 4-6° and lean 3° toward viewer on x/z (pose() sets only y);
   `arm_L` up 10-15°, `arm_R` down 8-10° and slightly forward. Proof: `hero.png`, `turn-front.png`. (Emil)
8. Optional: eyes turned in 4-5° so the far eye is not a sliver in 3/4, only if the glasses stay clean. (Illustrator 5)

## Rules
- Archive v1 renders and files to `assets/ghostie/v1/` first.
- Test Blender on a tiny case first; after any crash read the newest .ips in ~/Library/Logs/DiagnosticReports and fix the cause.
- Every claim in `selfcheck.md` names a crop or file. Do not score an item PASS while listing it as a weak point.
- Re-shoot every deliverable from v1, plus compare and lineup files.
