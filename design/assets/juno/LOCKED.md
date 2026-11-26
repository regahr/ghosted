# Juno the barista is locked (v1)

Rega: "ok proceed then" (ts 1795664774.871229), after "all ur pick" (ts 1795653224.813279). The chair took option 2
on card 7 (Viet's pick).

The game uses these files from `assets/juno/v1/`:
- `juno.glb`, with 2 non-swap meshes, `body` and `decals`;
- 4 cup swap parts, one per hold, plus the marker;
- the eye and mouth swap parts;
- `juno_toon.json`, and the toon and outline set-up in `ingame.html`.

## The numbers (`v1/juno_build_report.json`, `measure.md`)
- **Triangles:** 1,386-1,396 per beat, of 1,400.
- **Height:** 1.10 m. That is 75 px against Kit's 75 px (1.000) at the game camera, counting the puff.
- **Face:** the forehead band is 5-7 px, and the side hair sits 9-10 px above the eye top. No fringe.
- **Blender vs three.js:** mean difference 1.03/255.

## Design source
- The sketch: `assets/juno/sketch/`, direction A, "the hourglass".
- The chair calls are in `acceptance/juno/brief.md`.

## What the game build must do
- **Card-7 option 2:** at the game camera, her idle face uses the TALK mouth (2-3 px at 1x), so she does not read as
  mouthless. Card and close-up views keep the calm closed smile.
- **Hand-over:** she hands the cup forward.
- **Wave:** 3 frames.
- **Writing:** her head goes down 14°, she writes, then she turns the cup to the player.

## Known limits accepted
- A short broken ink line at the shoulder seam (as on Brett and Dot).
- The puff has 8 sides and is a little flatter than in the sketch.
- The scrunchie is a full ring, so a red line shows across the front.
- The apron hem is straight.
- The wave forearm is straighter than in the sketch.
- There are small ink ticks at the skirt hem, and a hair notch at the far ear in 3/4.
- Side-profile ticks.

## Asset files (local on this machine)
- **Blender source:** `design/assets/juno/v1/juno.blend`
- **Game file:** `design/assets/juno/v1/juno.glb`
- **Build script:** `design/assets/juno/v1/build_juno.py`
