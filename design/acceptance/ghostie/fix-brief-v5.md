# Ghostie v5 fix brief (chair, 2026-11-25)

v4 was not gated in full. The builder reported, and the chair confirmed in `assets/ghostie/v4/variants.png`, that the
arm join stays open. The cause is in the method: an inverted-hull outline cannot close the join of a separate flap that
lies in front of the body.

## Fix (Viet owns the method)
1. **One mesh for the body and the arms.** Grow each arm out of the body surface. It shares vertices with the body,
   and it is not a separate part.
   - Skin the mesh to 2 bones, `arm_L` and `arm_R`, with the pivot on the body surface, so the wave still works.
   - The outline hull must use the same skin. In three.js, the outline is a skinned mesh on the same skeleton.
   - Keep the v4 arm shape and position: round tips, below the eye dots at the game camera, and the eye-vs-arm pixel
     table.
2. **Proof:**
   - no "C" hook and no open root ink in `variants.png`, `hero.png` and `turn-side.png`;
   - no pale sliver in `crops/arm-root-front.png`;
   - the wave renders (`_close-wave.png`, `_ingame-wave.png`) match between Blender and three.js. The ink at the
     raised arm's root should now be better than the v3 known limit.
3. **Mesh count:** body+arms is now 1 non-swap mesh. Report it.
4. **Tie:** keep the v4 tie, unless the tie-only read by BMGD and the Illustrator asks for a change. The chair sends
   any change.
5. **If cheap:** remove the dotted hairline on the lower body in three.js (`ingame.png`, x 230-365, y 620-760). It was
   not checked in v4.

Keep everything else from v4. The budget stays at 600. v4 is archived in `assets/ghostie/v4/`. Test Blender on a tiny
skinned case first, because skinning plus attributes crashed Blender before (the `outline_w` name clash, 16:01). Every
claim names a crop.

## Tie change for v5 (chair, from `v4-tie-bmgd.md` and `v4-tie-illustrator.md`; both FAIL the v4 tie)
Keep the over-the-shoulder path and the lift. Change the shape:
1. **Ink:** one closed ink stroke round the whole tie (knot, both long sides, V), at the body-outline weight.
2. **Knot:** a small trapezoid about 1.5x the blade root width, with a clear step to the blade. Position (chair
   reconciliation): on the front, just below the eye line. That is higher than in v4, but never at eye level next to
   an eye, and never centred below the eyes.
3. **Blade:** about 1/4 as wide as it is long, along the full length, like Kit's. That is about 2x the v4 width.
   Shorten it if the budget needs it. Never make it thinner. Give it one soft S-bend, so it reads as wind.
4. **Tip:** a symmetric V point like Kit's, not a one-sided flag. It leaves the outline at the SIDE of the shoulder,
   blown sideways, with the V clear of the outline by about one blade width. It must not sit at the crown corner,
   where it reads as a hair bow or a horn.
5. **Proof:** `variants.png`, `hero.png`, `turn-front.png`, `turn-side.png` (no loose ink stub), `crops/tie-vs-kit.png`.
   At 26 m: two eye dots and nothing centred below them.
Open for Rega later, only if this still reads as a horn: a tie that hangs down on the front like Kit's (the
Illustrator's pick), or the blown-back tie.
