# Ghostie body map and sketch v2 brief (chair, 2026-11-25)

Rega, ts 1795614083.836699: "ok ur pick". The pick is to decide a ghost body map first, with the headset centred
with 2 cups and the tie centred under a collar, proved at the real game camera. Pipeline: council skill "Game art
pipeline", steps 1a and 1b, the ready check, the whole-picture check, and no blind iterations.

## Steps for the Illustrator
1. **`sketch/ready.md`:** rewrite it for this task. If any need is missing, stop and report.
2. **`sketch/body-map.png` and `body-map.md`:**
   - **Proportions:** keep the v5 size and the dome.
   - **Landmarks:**
     - Move the eye line UP on the dome, so the face sits high and leaves a clear neck zone.
     - The ear points are on the eye line, at the side edges.
     - Draw the neck line with a small collar, centred, clearly below the eyes.
     - Mark the chest, the arm roots and the hem.
   - **Attachment points:**
     - headset: the band is centred over the crown, with a cup on each ear point;
     - tie: centred, hanging from the collar;
     - glasses: on the eye line.
   - **Face zone:** mark the mouth zone that must stay empty. The collar and the tie knot must sit BELOW it.
   - **Game-camera check:** show your 2D estimate of the landmarks at the top-down camera (26 m, pitch 42°). Mark
     where the knot lands against the eye dots. This is an estimate. Viet's real render proves it later.
3. **Upright sketch v2** (`ghostie-sheet.png`, plus a short `tie-options.png` showing only the centred tie with a
   collar, next to Kit). Apply `acceptance/ghostie/sketch-fix-v2.md` in full:
   - an upright, symmetric turnaround, with the tilt in its own panel;
   - soft shoulders;
   - the headset centred with 2 cups;
   - the collar wings inside the outline;
   - clean labels.
4. **Self-check:** zoom every panel at 2x. Save the crops in `sketch/crops/`. Write `sketch/flaws.md` with one line per
   panel. Do not report while you can still see a flaw.

## Decided needs (sources)
- Palette: rows 16, 27, 10 and 22 only (`seats/lena-park.md`). The shade is neutral, x0.94 in 2D.
- Budget for Viet: body and arms about 508 triangles, eyes 24, tie 68 or fewer (`sketch-viet.md`).
- Motion: arm_L waves 0° to +40°, the tip never above the eye bottom (`sketch-emil.md`).
- Bible: no mouth, ever (`design/bible.md` L30).
- v1 sketch: `assets/ghostie/sketch-v1-archive/`. Reuse `src/` freely.

## What happens next (not your task)
- Viet makes a blockout from the v5 model: raised eyes, a collar, the centred tie and a symmetric headset.
- Viet renders the REAL game-camera lineup.
- If the centred tie reads as a mouth there, the chair stops and shows Rega the evidence.
