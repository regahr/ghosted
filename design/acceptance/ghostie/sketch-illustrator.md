# Ghostie sketch gate, SK1: Illustrator judge (2026-11-25)

Judge: an Illustrator seat that did not draw the sketch. I scored from the images. `sketch/notes.md` is treated as claims.
Item: SK1 (`acceptance/checklist.md` line 23). Extra check: the tie reads as a tie at card size.

## Verdict: PASS

## Evidence
1. **Fact.** `assets/ghostie/sketch/src/ghost.py` lines 22-39: the front body is one closed path of 18 cubic Bezier
   segments (dome, crown, 3 hem lobes, both arm flaps). There are no sphere, cylinder or box primitives. `ellipse()` is
   used only for the eyes, glasses rims, the headset cup and the ground shadow (lines 195-340). These are small
   designed ovals, not the body form.
2. **Fact.** `ghostie-sheet.png`, turnaround row: the dome is wider at the shoulder than at the crown. The arm_L flap is
   higher than the arm_R flap and grows out of the side with one outline and no seam. The hem has soft unequal lobes.
   **Opinion:** this is a designed shape with asymmetry and a tilt. It does not read as an assembled code model.
3. **Fact.** `silhouette-64.png` (64x64, I looked at x8 nearest): it shows a tall dome, two side flaps at different
   heights and a lobed hem. **Opinion:** it reads as a ghost at 64 px. Nothing else in the cast has this outline.
   The hem lobes are shallow at this size, which is a minor point and not a fail.
4. **Fact.** `tie-options.png`, column B, card and x2.4 close-up: it has a trapezoid knot, two collar wings, a blade
   that gets wider, a symmetric V point, and ink all round. This is the same read order as Kit's tie in the Kit column.
   **Opinion:** it reads as a TIE. It does not read as a quill, horn, bow, strap or tongue.
5. **Fact.** `ghostie-sheet.png`, VARIANTS "tie (B, slipped)" panel at card scale: the knot, blade and V still separate
   from each other. **Opinion:** the tie read holds at card size.
6. **Fact.** `paintover-v5.png`, hero and tie variant panel: tie B is painted on the v5 render at card scale with the
   knot below the eye line. **Opinion:** it reads as a tie on the real render too.

## Watch items (not SK1 fails; other seats own them)
- **Opinion.** `ghostie-sheet.png`, SIDE: the closed arm oval can read as a hole or a pocket. The 3D hull will settle
  this. Viet should check it in the blockout.
- **Opinion.** `tie-options.png`, column B, game camera x3: the diagonal lilac mark near the right eye column could read as
  a tear streak. BMGD (SK4) scores this at the game camera. The sheet's thumb is an approximation (`notes.md` item 2),
  so it must be proved on the real `lineup-grass-crop-x3.png` render.

## Fix
None needed for SK1.
