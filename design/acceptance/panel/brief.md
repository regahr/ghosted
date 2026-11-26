# The Panel: sketch (chair, 2026-11-26)

Rega: "all ur pick" (ts 1795653224.813279) and "ok proceed then" (ts 1795664774.871229). The chair makes the open calls.
This brief is the SKETCH stage; the 3D follows after the chair's 2x check. Pipeline: council skill "Rega is the gate",
"Ready check", "Judge a sketch as a sketch", "No blind iterations", "Game art pipeline". Art rules: `bible.md`
"Art rule: no fringe" and "Art rule: mouths". Keep `runs/jobless-roguelike/handoff.md` in mind: the quota is low, so
work efficiently.

## Decided needs (sources, plus chair calls)
- **Role:** "Panel Plates", the panel interview set in Panel Heights (weeks 9-11). Three interviewers sit at one table
  (`seats/bmgd.md` L45):
  1. **Ms. Culture Fit**: the vibe check; asks "where do you see yourself";
  2. **Mr. Whiteboard**: the technical one with a marker;
  3. **The Camera-Off One**: a black box on the table, like a video call with the camera off.
- **Tone:** comic and kind. Interviews feel absurd, but no one is cruel to the player.
- **Shape hints:** BMGD gives a table box 2.0 x 0.1 x 0.6, 2 sphere heads and 1 box. The Illustrator owns the shape
  language. Each of the three must read apart at the game camera by silhouette, not by colour alone. The two humans are
  seated, so only their upper bodies show above the table. Keep them in the toy-pawn family (Kit, Ricky, Dot, Brett,
  Juno).
- **Chair call, colours** (existing rows only; BMGD's `#C9A27A` and `#2E2A33` are not rows):
  - the table: wood, row 5 `#7A4A2E`, or panel-edge, row 24 `#E9D3B4`. Pick one and give the reason;
  - the Camera-Off box: ink row 22 or dark suit row 17, with a cream row 12 "camera off" icon or initials;
  - the people: rows that keep them apart from the locked cast (Kit blue 14, Ricky dark 17, Dot purple 11, Brett red 7,
    Juno brown 5 and apricot 6, the ATS grey 18, the Ghostie white 16). No big teal (row 20) or gold (row 13) areas.
- **Chair call, budget for the 3D:** the WHOLE set (table, 2 people, box, props) is 2,000 visible triangles or fewer, at
  most 4 non-swap meshes.
- **Chair call, size:** a seated person's head is at about Kit's head height at the game camera. The table top is about
  0.75 times Kit's height.
- **Faces:** each human has a mouth in the Ricky style or a closed line. There is no fringe, and nothing down the temples.
  Prove at 1x that no mouth reads as a beard.
- **Motion:**
  - Ms. Culture Fit nods and tilts her head;
  - Mr. Whiteboard clicks his marker and points;
  - the Camera-Off box blinks a "muted" or "camera off" icon;
  - all three lean in for "any questions for us?".
- **Game camera:** 26 m, pitch 42°, yaw 20°. Show a colour and grey lineup with Kit in front of the table.

## Make (in `assets/panel/sketch/`)
- `ready.md` first;
- `explore.png`: local references, 8-12 thumbnails, 2-3 directions, and a pick;
- `body-map.png` and `.md`;
- `panel-sheet.png`: the turnaround of the set and of each person, the motion panels, expressions, a 64 px silhouette,
  colour and grey lineups, game-camera tiles with Kit, a face check x3, and the palette;
- the SVG sources;
- `notes.md`.
Reuse the code in `assets/juno/sketch/src/` and `brett/sketch/src/`.

## Chair calls after the sketch (2026-11-26)
The sketch passes the chair's 2x check: direction A, "bow, flat-top, black cube" (`assets/panel/sketch/panel-sheet.png`).
1. **Heads:** Kit-sized heads (the Illustrator's reading). The table top is 0.733 m.
2. **Table:** row 24 is kept. The box's read (11.1:1) matters most, and the table reads by its ink outline and the shaded
   front panel.
3. **Idle face in game:** both humans use the TALK mouth at the game camera, by Juno's card-7 rule. Card views keep the
   rest lines.
4. **Budget:** 2,000 or fewer for the whole set, at most 4 non-swap meshes: the table with chairs, Culture Fit,
   Whiteboard with his marker, and the box. The sketch estimates about 1,320.
5. **3D notes:** see `sketch/notes.md`. Culture Fit's open grin must not touch the chin line at 1x.
