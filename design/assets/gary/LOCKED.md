# Gary the pigeon postman is locked (v1, after pass 2)

Rega's acceptance: card 9, "1" (ts 1795672279.229029), after pass 2 (option 2 plus a satchel fix, ts
1795672044.582919).

The game uses these files from `assets/gary/v1/`:
- `gary.glb`, with 3 non-swap meshes: body 572, wing_R 100 and wing_L 100;
- the swap parts: eyes (4 sets), brows (3 sets), the envelope (beak and wing sockets), and the bag flap (closed or open).

## The numbers (`v1/gary_build_report.json`, `measure.md`)
- **Triangles:** 842 at rest, at most 896 (the sorry beat), of 900.
- **Height:** 0.479 m. That is 35-36 px against Kit's 75 px (0.47-0.48 times).
- **Wingspan:** 1.032 m (1.056 times Kit).
- **Eyes:** 3.0-3.2 px at 1x. The cap clears the eyes by 3-4 px.

## Design source
- The sketch: `assets/gary/sketch/`, direction A, "round postie".
- The chair calls are in `acceptance/gary/brief.md`.

## What the game build must do
- **Fly in:** a 0.6 s flap loop (up 50°, level 5°, down -35°), legs tucked, the body pitched 10°, the letter in his beak.
- **Land:** a little hop.
- **Hold out the letter:** in his wing fingers.
- **Result:** a NO gets a soft "sorry" head-tilt; a YES gets a happy hop.
- **Fly off.**

## Known limits accepted
- In the side view, the strap end tucks under the folded wing.
- On grass his eyes are small dots at 1x.
- There are small ink ticks at the back of the neck.
- The folded wing looks smaller than in the sketch from the side.
- Slight facets at card size.

## Asset files (local on this machine)
- **Blender source:** `design/assets/gary/v1/gary.blend`
- **Game file:** `design/assets/gary/v1/gary.glb`
- **Build script:** `design/assets/gary/v1/build_gary.py`
