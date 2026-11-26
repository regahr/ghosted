# Gary the pigeon postman: sketch (chair, 2026-11-26)

Rega: "all ur pick" (ts 1795653224.813279), and "proceed" with the handoff kept current (ts 1795664774.871229). The chair
makes the open calls. This brief is the SKETCH stage; the 3D follows after the chair's 2x check. Pipeline: council skill
"Rega is the gate", "Ready check", "Judge a sketch as a sketch", "No blind iterations", "Game art pipeline". Art rules:
`bible.md`. The quota is low, so work efficiently.

## Decided needs (sources, plus chair calls)
- **Role:** Gary brings every result: each yes, each no, and each "under review" (`seats/bmgd.md` L46, L63). His job is
  to make every "no" a short, soft beat, so he must be the kindest delivery in the game. He is a little bumbling,
  always sincere and never smug.
- **Shape hints:** BMGD gives a sphere body, a cone beak, 2 box wings, and a 0.6 s flap. The Illustrator owns the shape
  language. He is a toy pigeon in the family's round-toy style, with a postman look, such as a small cap and a mail bag.
  He must read as "bird plus post" at the game camera.
- **Chair call, colours** (existing rows only; BMGD's `#9AA6B8` and `#F2B84B` are not rows):
  - body: row 8 `#A8C4DC` light blue-grey. Not robot row 18, which would look like the ATS. Pick a darker row for the
    wings or head if the value needs it;
  - beak and feet: gold row 13 `#F0B43C` (small areas only);
  - cap: navy row 26 or ink row 22;
  - mail bag: wood row 5 or panel-edge row 24;
  - envelope: panel row 23, with a small stamp (row 7 or row 10);
  - he must separate from the grass and path at the game camera, with an outline and a darker element;
  - show colour and grey lineups with Kit and 2-3 of the locked cast.
- **Chair call, size:** a small bird, about 0.5 times Kit's height standing. In flight his wingspan is about 1.0 times
  Kit's height.
- **Budget for the 3D:** 900 visible triangles or fewer, at most 3 non-swap meshes. Envelopes and the bag flap are swap
  parts.
- **Face:** eyes, and a beak that is clearly a beak (no human mouth). If he has a head tuft or cap, nothing may cover his
  eyes (the no-fringe rule, applied to a bird).
- **Motion:**
  - fly in with a 0.6 s flap loop;
  - land with a little hop;
  - hold out an envelope in his beak or wing;
  - a soft "sorry" head-tilt for a no, and a happy hop for a yes;
  - fly off.
- **Game camera:** 26 m, pitch 42°, yaw 20°.

## Make (in `assets/gary/sketch/`)
- `ready.md` first;
- `explore.png`: 8-12 thumbnails, 2-3 directions, and a pick;
- `body-map.png` and `.md`;
- `gary-sheet.png`: the turnaround, the flight poses, the motion panels, expressions, a 64 px silhouette, colour and grey
  lineups, game-camera tiles next to Kit, and the palette;
- the SVG sources;
- `notes.md`.
Reuse the sketch code in `assets/panel/sketch/src/` or `juno/sketch/src/`.

## Chair calls after the sketch (2026-11-26)
The sketch passes the chair's 2x check: direction A, "round postie" (`assets/gary/sketch/gary-sheet.png`).
1. **Budget:** 900 triangles or fewer. The sketch plan is about 1,010. Thin the strap and the finger feathers first, and
   keep the eyes, beak and cap. Use 3 non-swap meshes: the body, the left wing and the right wing.
2. **Wingspan:** keep 1.06 times Kit, for the read in flight.
3. **Eyes:** grow them by 15%, for the read at 1x. The cap must still never cover the eyes.
4. **3D fixes:**
   - Tuck the folded wings back and in, so that from the front they do not read as hanging arms.
   - Route the strap so that it does not show as a low loop in the side view.
5. **Motion:** key poses only. The 0.6 s flap loop is fixed, and the other timings are for the game build.
