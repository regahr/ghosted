# Recruiter Ricky 3D build brief (chair, 2026-11-25)

Rega accepted the sketch: "only 1" (ts 1795622448.197729), then "that's hair fringe, mic looks fine"
(ts 1795622623.559849). The fringe over the left eye at the game camera is accepted as his hair style. Rega is the
gate: no seat rounds. The chair checks at 2x, then the result goes to Rega.

## References (match these)
- Sketch: `assets/ricky/sketch/ricky-sheet.png`, `body-map.png` and `body-map.md`. The curves are in
  `sketch/src/ricky.py`.
- Chair calls: `acceptance/ricky/chair-calls.md`.
- Locked Kit: `assets/kit/LOCKED.md` and `kit.glb`, the toon and outline set-up.
- Locked Ghostie: `assets/ghostie/LOCKED.md` and `v7/`. Reuse its working pipeline scripts: `build_ghostie.py`,
  `render_ghostie.py`, `ingame.html`, `shoot_ingame.mjs`, `make_sheets.py`.

## Before you model (council skill: "Ready check", "Offer is not use", "Game art pipeline" step 4 blockout)
1. Write `assets/ricky/v1/ready.md`, and stop if a need is missing.
2. Write `direction.md`, with the hardest parts, the join decisions and the triangle plan.
3. Save the output of your skill's `search.py`, `design-context.py` and `host-probe.py`.
4. Build a quick BLOCKOUT first. Render it at the real game camera next to the real Kit and a Ghostie, and set the
   screen scale so that Ricky is 1.05 times Kit's real on-screen height (Kit is 72 px in the v7 lineup). Then build the
   final model.

## Requirements
- **Budget:** 1,400 visible triangles or fewer, and at most 3 non-swap meshes. If it is tight, merge the shoulder balls
  into the jacket first.
- **Shape:** direction A, the "bell jacket" pawn, 2.67 heads. The turnaround must match the sheet in the front, 3/4,
  side and back views. Keep the mesh upright and symmetric.
- **Colours** (palette rows only):
  - suit 17 `#2E2C3D`;
  - skin 15;
  - hair 25;
  - shirt V, collar ring and cuffs 16;
  - accent 10 `#C9A6D6` on the headset and the tie;
  - shoes 5;
  - ink 22;
  - a neutral shade band.
- **Headset:** centred over the crown, one cup on each ear point, and the mic from the right cup, all with ink. The tie
  is centred under the collar, with ink.
- **Joins:** decide each one in `direction.md`, so that no visible seam, crease or hook shows at card size. The Ghostie
  lesson: arms that grow out of one skinned mesh close their outline.
- **Motion:**
  - the hop (squash only on the bounce, as Kit does);
  - the phone gesture, with the right hand to the right cup (a bone or a morph);
  - the drain. The suit colour lerps from row 17 to 11, then 27, then 16. The legs fade, he floats up, and at the end
    the headset Ghostie swaps in. Plan the parts so that this works: legs as their own part or a vertex group, and the
    float node.
- **Game camera:** a greyscale lineup with Kit and the Ghosties. Ricky must read as a dark bell with a white V.

## Deliverables (in `assets/ricky/v1/`)
- the turnaround and `hero.png`;
- `phone.png`, `hop.png` and `drain-strip.png`;
- the silhouettes and the grey render;
- the in-game render and `compare-ingame.png`;
- the lineups on grass and path, in colour and grey, with x3 and 1x crops;
- `compare-sketch.png`;
- `crops/`;
- `measure.md` and `selfcheck.md`. A visible fault is never a PASS.

## Rules
- No blind iterations: if an item fails twice, stop and report.
- Run a tiny Blender test first, and read the newest .ips after any crash.
- Work only in `assets/ricky/v1/`.

## Change from Rega (ts 1795622664.391049): "can erase the hair fringe?"
- No fringe. The hair is a cap on top, with the hairline above both eyes and brows, so the forehead shows.
- No hair crosses the eye line in any view, especially at the game camera.
- Keep the quiff and hair colour row 25.
- The mic stays as it is.
- Proof: a game-camera x3 face crop, and the hair's lowest point against the eye top, in px, in measure.md.
