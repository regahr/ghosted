# Ghostie sketch and paint-over brief (chair, 2026-11-25)

Rega's call, ts 1795607965.756479: "ok i follow ur pick". The picks are: sketch the Ghostie now, and add a blockout
and a paint-over before the final model. Rules: the ready check, no blind iterations, sketch first (council skill).

## Goal
One sheet that decides the Ghostie's final shape before any more Blender work. The tie is the hardest part: it failed
5 times. v5 serves as the blockout. Its body, colours, pose and arm position already pass, so this sheet is both the
sketch and the paint-over on v5.

## Decided needs (sources)
- **Role and tone:** a recruiter who never replied. It is comic and kind, and it has NO MOUTH (`design/bible.md`,
  Ghost row).
- **View sizes:**
  - card size: `assets/ghostie/v5/hero.png` and `variants.png`;
  - the game camera, top-down, 26 m, ghost body about 27 px at 1x: `assets/ghostie/v5/lineup-grass-crop-x3.png`.
- **What already passes and stays:** the dome, the crown, the 5-scallop hem and the size.
  - Off-white `#F8F4EA` (row 16), lit cream under the warm light, which is accepted.
  - A neutral grey shade.
  - A tilted rest pose, with the arm tips below the eye dots at the game camera.
  - Proof: `acceptance/ghostie/v3/lena-park.md`, `v3/emil-kowalski.md`, `v4-tie-*.md`.
- **Palette (only these):**
  - `#F8F4EA` body (16);
  - `#C8C0D8` faded accessory (27);
  - `#C9A6D6` tie lilac (10);
  - `#2B1E16` ink (22).
  The rows are in `design/seats/lena-park.md`.
- **The 3 variants:** tie, glasses and headset. The glasses and headset read already. Keep their shape. Clean up only
  what you see.
- **Budget for Viet:**
  - 600 visible triangles per variant;
  - the body with arms is about 508;
  - the tie must be buildable in about 90 triangles or fewer.
- **Motion parts (Emil):** float bob; `arm_L` waves from 0 to +40° up from rest. The arms are part of the body mesh,
  skinned. Draw the arm as a soft flap that grows out of the body, with no seam.
- **Tie tests (from BMGD and you, v1-v4):**
  - At the game camera, the two eye dots show with NOTHING centred below them.
  - At card size, it reads as a TIE, with a knot, a blade and a V point. It must not read as a quill, a horn, a hair
    bow, a strap, a party horn or a tongue.
  - Compare it with Kit's tie (`assets/kit/hero.png`).
- **Known 3D faults to mark on the paint-over** (Viet fixes these in the model):
  - the ink crease line from the near arm root;
  - the pale root wedge;
  - the hem hook under the near arm (`assets/ghostie/v5/variants.png`).

## What to make (folder `design/assets/ghostie/sketch/`)
1. **`ready.md` first.** Use the council skill's "Ready check before any drawing". If any need is missing or unclear,
   STOP and report back. Do not draw.
2. **`tie-options.png`.** 3 tie ideas, each drawn at card size AND at the game-camera thumbnail, with Kit's tie beside
   them. Mark your pick.
   - One must be a tie that hangs down the front, like Kit's (your earlier pick). Show honestly whether it lands in the
     mouth zone at the top-down camera.
   - Others can be off-centre or blown aside.
3. **`ghostie-sheet.png`.** The model sheet with your picked tie:
   - front, 3/4, side and back;
   - the 3 variants;
   - a 64 px silhouette;
   - a game-camera thumbnail next to Kit;
   - a wave pose.
   Use designed curves, not code primitives.
4. **`paintover-v5.png`.** Paint over `v5/hero.png`, `v5/variants.png` and `v5/lineup-grass-crop-x3.png`, so that Viet
   sees exactly what to change.
5. **Sources:** the SVG source of each PNG, rendered with `magick`.

## Tools
- Your own illustrator skill (offer, then use it).
- Hand-written SVG with Bezier curves.
- `magick` to render and to composite paint-overs.
- No web, no image generation, no other service.
