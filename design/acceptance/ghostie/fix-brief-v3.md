# Ghostie v3 fix brief (chair, 2026-11-25)

Gate v2 result: FAIL. Viet (V1, V2, V3, V5), Illustrator (I2 must, I4 should) and BMGD (B1) fail it. Lena and Emil pass it.
The scores are in `acceptance/ghostie/v2/`. Keep everything that Lena and Emil passed: the neutral shade, the palette
colours, the outline width, the float lean and the uneven arms.

## Chair rulings
- **Budget: 600 visible triangles per variant** (checklist, chair amendment 3). Spend the new triangles on the profile:
  the crown, the shoulder turn and the hem curves. You may also move triangles from the hidden hem cavity.
- **Tie: BMGD's option (a)** over the Illustrator's "shorter, darker chest stripe". The reason: the top-down camera puts
  any centred mark below the eyes in the mouth zone (`v2/bmgd.md`). The tie flips sideways over one shoulder, as if blown
  by a fast exit. It runs on a slant and crosses the side outline. It has no ink on top of the knot, only on the long
  sides. It keeps palette row 10, `#C9A6D6`.
- **Arms: one merged spec** from Viet, the Illustrator and Emil:
  - Each arm is a flat, tapered flap with a round tip. It grows out of the body with no visible joint, no pale collar
    strip, no octagon end and no hexagon tip.
  - Move the root 10-15% lower, below the eye line at the 26 m camera, so the arms do not read as ears.
  - The arms droop down and out by 25-35°. Turn the near arm out toward the camera, so it breaks the 3/4 silhouette.
  - Keep Emil's uneven pose: `arm_L` sits higher than `arm_R`. Flip the `float` roll to +5° in three.js z, so the tilt
    and `arm_L` add up and the "ready to wave" lean shows on the card.
  - Merge `arm_collars` into `body`. The result is at most 3 non-swap meshes: body, arm_L and arm_R (V5).
- **I4 (the app-logo look):** avoid the round mid-height nubs and the pointed, flared hem corners. The lower, drooping arms
  and the rounded hem corners below cover this.

## Fixes and their proof files
1. **Arms**, as specified above. Proof: `silhouette-64-34-x4.png` (both arms must show, or the near arm clearly),
   `crops/arm-root-front.png`, `crops/arm-end-on-side.png`, `turn-back.png`, `hero.png`, `lineup-grass-crop-x3.png`
   (the arms must not read as ears).
2. **Tie over the shoulder.** Proof: `lineup-grass-crop-x3.png` and `lineup-path-crop-x3.png`. The test: the left ghost
   shows two eye dots and nothing centred below them. Also `variants.png`, which must still read as a tie.
3. **Round crown and shoulders**, with no visible corners at 1200 px. Proof: `hero.png`, `variants.png`,
   `silhouette-64-x4.png`.
4. **Hem:**
   - Give each notch 2 more vertices, so that its top is a curve.
   - The outer corners must not flare to points.
   - Fix the doubled outline sliver at the left hem (`hero.png`, x 340-360, y 730-770).
   Proof: `crops/hem-notch-34.png`, `hero.png`, `silhouette-64-x4.png`.
5. **Glasses and ear-cup frames** at 8 sides or round. Close the ear-cup ink at its lower left. Proof: `variants.png`.
6. **Optional:** turn the eyes in 4-5°, but only if the glasses stay clean.

## Rules
- Archive the v2 renders and files to `assets/ghostie/v2/` first.
- Test Blender on a tiny case first. After any crash, read the newest .ips and fix the cause.
- Each claim in `selfcheck.md` names a crop. A visible fault means that the item is not PASS. Also check V5 mesh
  count, not only triangles.
- Re-shoot every deliverable.
