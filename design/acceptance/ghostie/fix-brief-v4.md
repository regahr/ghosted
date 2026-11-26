# Ghostie v4 fix brief (chair, 2026-11-25)

Gate v3 result: FAIL. Viet (V1, V2, V3), Illustrator (I2) and BMGD (B1) fail it. Lena (L1-L3) and Emil (E1, E2) pass it.
The scores are in `acceptance/ghostie/v3/`. The body, the crown, the colours, the shade band, the outline, the pose and
the mesh count all pass. **Change only the arms, the eyes, the tie and the headset cup ink.** The budget stays at 600.
Take any triangles you need from the hidden hem cavity.

## Fixes and their proof files
1. **Arms below the eyes at the game camera** (Viet V1 and V3, Illustrator).
   - Judge the arm height on screen, from the 26 m game camera, not in world z. The top-down camera moved the eyes down
     the screen by the same amount as the v3 arms moved down.
   - Raise the eye dots about 8-10% of the body height on the dome. The glasses must stay clean.
   - Droop the arm tips further down and out, so they sit clearly below the eye dots on screen on all 3 ghosts.
   - Proof: `lineup-grass-crop-x3.png`, `lineup-path-crop-x3.png`. Each ghost must show the eye dots above the arm tips,
     with a clear gap. Add a measured line to `selfcheck.md`: eye y against arm-tip y, in pixels, for each ghost.
2. **Round arm tip** with a curved top edge, not a 6-sided wedge (Viet, Illustrator). Proof: `hero.png`, `variants.png`.
3. **Arm join seams** (Viet V2, Illustrator I2):
   - remove the ink spur and the hook under the near arm (all panels of `variants.png`, about x 420-450, y 425-520);
   - remove the pale wedge at the root (`crops/arm-root-front.png`);
   - remove the end-on "slot" (`turn-side.png`, x 420-495, y 650-750);
   - check `turn-back.png` (x 650-690, y 780-820).
   The body outline must flow into the flap with no step and no sliver.
4. **Tie** (BMGD B1; the Illustrator agrees):
   - Keep it over the shoulder, but turn it the right way round. A small knot goes low on the front, off-centre on the
     same side (+40° to +50°), below the eye line.
   - The blade widens as it goes up over the shoulder.
   - It ends in a wide pointed tip that lifts off the body past the shoulder outline, into the air. This is the "blown by
     a fast exit" joke.
   - No part of the tie sits at eye level next to an eye.
   - Ink on the long sides. Lena found none in v3, although `changes.md` claimed it.
   - Proof:
     - `variants.png` and `hero.png` show the knot and the pointed tip in the air.
     - Both lineup x3 crops show two eye dots, nothing centred below them, and a small lilac point past the shoulder outline.
     - A side-by-side crop with Kit's tie: `crops/tie-vs-kit.png`.
5. **Headset cup ink:** one closed stroke round the cup, with no doubled edge and no pale sliver. Proof:
   `crops/headset-cup-on-surface.png`, `variants.png`.
6. **If cheap:**
   - Round the apex of each hem notch into a curve (`crops/hem-notch-34.png`).
   - Remove the dotted hairline on the lower body in three.js (`ingame.png`, x 230-365, y 620-760).

## Notes for the game build (not for v4)
- Wave (Emil): swing `arm_L` from 0 to +40° up from rest, 2 times, on a soft spring with bounce about 0.2. Check it at 0.25x.
- Never show the wave pose on a card.

## Rules
- Archive the v3 renders and files to `assets/ghostie/v3/` first.
- Test Blender on a tiny case first.
- Every claim names a crop. A visible fault means that the item is not PASS.
- Re-shoot every deliverable.
