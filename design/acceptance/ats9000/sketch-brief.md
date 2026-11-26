# ATS-9000: body map and sketch brief (chair, 2026-11-26)

Rega, ts 1795626758.472359: "go". Pipeline: council skill, "Rega is the gate", "Ready check before any drawing",
"Judge a sketch as a sketch", and "Game art pipeline" steps 0, 1a, 1b and 1. No seat rounds: the chair checks at 2x,
then the sketch goes to Rega.

## Decided needs (sources, plus chair calls where the seats conflict)
- **Role:** the gate of the ATS Catch mini game. The ATS reads CVs for keywords. It is literal, NOT evil
  (`seats/bmgd.md` L40). Its voice line: "KEYWORD 'SYNERGY' NOT FOUND. PLEASE BE MORE SYNERGY." (L71). The tone is
  comic and kind.
- **Shape parts to explore** (the Illustrator owns the shape language):
  - BMGD: a box head 0.5, a visor slit, a box body 0.6, and a cone HOPPER that it feeds CVs into.
  - Viet (`seats/viet-tran.md` L65): a box body, a head with a screen and a moving scan line, 2 treads, a stamp arm
    "NOT A FIT", and an antenna.
  - Combine these in 2-3 directions and pick one. It must read as "a machine that reads your CV".
- **Colours (chair, by palette ownership: Lena):**
  - body row 18 `#8E9BA8`;
  - visor and screen ink row 22;
  - eyes or scan line in cream, row 12 `#FFE8A6` or row 23 `#FFF8EE` (Lena: cream on ink is 13.3:1; NOT teal, which
    is 1.1:1 for deuteranopes);
  - antenna ball gold row 13 `#F0B43C`;
  - stamp ink row 22, or red-ink row 21 `#B23A26` (red-ink is text-only in the palette, so if you use it on the stamp,
    flag it);
  - BMGD's `#8FA3B8` and `#E0533D`, and Viet's `#2b3a4a`, are NOT palette rows. Do not use them.
  - The shade is a neutral grey multiplier.
- **Size (chair):** about 1.2 times Kit's on-screen height at the game camera. Kit is 75 px in the Ricky lineup
  (`assets/ricky/v1/measure.md`). It is a gatekeeper, a bit bigger than Kit, still a toy.
- **Budget for the 3D:** 900 triangles or fewer (Viet L65), at most 3 non-swap meshes.
- **Value:** mid grey. The robot on grass is only 1.74:1, so the ink outline carries it (`seats/lena-park.md` L82).
  Show a greyscale lineup with Kit, Ricky and a Ghostie.
- **Motion parts:**
  - the scan line moving on the screen;
  - the stamp arm coming down ("NOT A FIT");
  - the treads rolling;
  - the antenna blinking;
  - the hopper taking a CV.
  Draw the joins clearly.
- **Body map (step 1a):** the landmarks for a machine:
  - the screen or face zone;
  - the hopper mouth;
  - the stamp pivot;
  - the antenna base;
  - the tread line.
  It has no human mouth. The hopper is its "mouth" for CVs.
- **Game camera:** 26 m, pitch 42°, yaw 20°. Reuse the Ghostie and Ricky camera estimate method
  (`assets/ricky/sketch/src/`, `assets/ghostie/sketch/src/camera.py`).

## What to make (in `design/assets/ats9000/sketch/`)
1. **`ready.md` first.** Stop if any need is missing.
2. **`explore.png`.** Local references (the mock ATS Tower in `concept/out/shots/02-hub.png`, Kit, Ricky and the
   Ghostie), then 8-12 thumbnails, then 2-3 directions and a pick with a reason.
3. **`body-map.png` and `body-map.md`.**
4. **`ats-sheet.png`.** An upright turnaround (front, 3/4, side, back), plus:
   - the motion panels: scan, stamp, hopper;
   - a 64 px silhouette;
   - the greyscale lineup;
   - game-camera thumbnails next to Kit;
   - the palette rows used.
5. **SVG sources** in `src/`, plus `notes.md`, with each claim tied to a file and marked Fact or Opinion.

It is a sketch for the 3D builder: line polish is not judged. Check at 2x that the shape, the proportions, the
placements, the views agreeing and the game-camera read are right. No web, no image generation, no other service. Work
only in `assets/ats9000/sketch/`.
