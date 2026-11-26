# Ghostie 3D v6 build brief (chair, 2026-11-25): the final model, built to the sketch

Rega, ts 1795617228.257839: "the final result should be the 3D, the sketch should support the 3D drawing requirement".
So the sketch v2 is the 3D reference, and this build is the final result.

## References (match these)
- Sketch: `assets/ghostie/sketch/ghostie-sheet.png`, `body-map.png` and `body-map.md`. Shapes are in
  `sketch/src/ghost.py`.
- Blockout, already rendered at the real camera: `assets/ghostie/blockout/` (eyes, collar, centred tie, 2-cup
  headset).
- The pipeline scripts to reuse: `assets/ghostie/blockout/build_ghostie.py`, `render_ghostie.py`, `ingame.html`,
  `shoot_ingame.mjs` and `make_sheets.py`.
- Rulings:
  - `design/bible.md`, "Ghostie ruling": no mouth, and the centred tie may read as a tongue (Rega).
  - `acceptance/checklist.md`: budget 600 per variant, at most 3 non-swap meshes, and S1 "matches the accepted sketch".

## Before you model (council skill: "Ready check before any drawing", and "Offer is not use")
- Write `assets/ghostie/v6/ready.md`. If anything is missing, stop and report.
- Write `assets/ghostie/v6/direction.md`. Name the hardest parts and the join decisions.
- Run and save the output of your skill's `scripts/search.py`, `design-context.py` and `host-probe.py`.

## Requirements from the sketch and the seat notes
1. **Body:**
   - upright and symmetric in the mesh; the 4° rest lean lives on the `float` node, not in the mesh;
   - a smooth dome with no visible corners at card size;
   - 5 hem lobes, with 3 seen from the front and a notch centred at the back.
2. **Arms:**
   - one skinned mesh with the body (the v5 method);
   - soft shoulders with no corner, crease, pale wedge or hem hook (v5 paint-over marks 1-3);
   - the arm shape and height as in the sketch;
   - the tips below the eye dots at the game camera, at rest and in the wave (0 to +40°);
   - the 3/4 view shows the far-arm nub.
3. **Eyes:** on the body-map eye line, y 118.
4. **Tie variant:**
   - the collar wings lie flat on the body, inside the silhouette, joined to the knot;
   - the tie is centred and hangs from the collar, with ink all round;
   - at most 68 triangles.
5. **Glasses variant:** round rims, on the eye line, with an ink edge thick enough to read at 1x at the game camera
   (Lena and BMGD).
6. **Headset variant:**
   - the band goes OVER the crown, on or just outside the dome outline, with an ink edge, and never as a stripe on the
     forehead;
   - one cup on each ear point, level and the same size, with ink;
   - total at most 600 triangles: use 8-sided cups with no back face, a thin band, and no extra ink-ring geometry.
7. **Colours:** palette rows 16, 27, 10 and 22 only, and a neutral shade band (Lena).

## Deliverables
These are the same set as v5, in `assets/ghostie/v6/`:
- the turnaround and variants;
- `hero.png`;
- the silhouettes;
- the grey render;
- the in-game render and the compare;
- the lineups on grass and path, in colour and in grey, with x3 and 1x crops;
- the wave renders;
- the crops;
- `measure.md`: screen-pixel eye, arm-tip and knot positions at the game camera;
- `selfcheck.md`: every claim names a crop, and a visible fault is never a PASS;
- `compare-sketch.png`: each sheet view side by side with the matching 3D view (for S1).

## Rules
- No blind iterations: if an item fails twice, stop and report. Do not try a 3rd method on your own.
- Test Blender on a tiny case first. After any crash, read the newest .ips file.
- Work only in `assets/ghostie/v6/`.
