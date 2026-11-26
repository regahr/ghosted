# Emil Kowalski (Principal Designer): sketch gate, card 2 (Ghostie), item SK5

## Offer
- `~/.claude/skills/emil-design-eng/SKILL.md`, "Spring Animations" (bounce 0.1-0.3) and "Debugging Animations" (slow motion, frame by frame). With these I judge the wave as a moving beat, not as a still frame.
- `~/.claude/skills/improve-animations/AUDIT.md`: the 0.25x audit is for the game build, not for this sketch.
- The brief blocks none of my tools. No drawing in this task, so no `ready.md`.

## Verdict: SK5 PASS

## Evidence
1. **Rest pose reads alive and kind.**
   - **Fact** `assets/ghostie/sketch/ghostie-sheet.png`, FRONT and 3/4: rest tilt 4 deg, arms not the same height (arm_L higher), tie B askew, soft hem lobes. Two eye ovals, no mouth.
   - **Opinion:** the pose has a lean and an asymmetry, so it does not read as a stiff icon. The face is open and has no mouth, so it reads kind, not spooky. It holds at the game camera x3 thumbs.
2. **Wave at +40 deg: the arm_L tip reaches the bottom of the eye dots.**
   - **Fact** `acceptance/ghostie/fix-brief-v4.md` L42: "swing `arm_L` from 0 to +40° up from rest, 2 times, on a soft spring with bounce about 0.2".
   - **Fact** `assets/ghostie/sketch/notes.md`, "What does not work yet" item 4: the tip top is at about y 163, and the eye bottom is at 163.
   - **Opinion: acceptable.** The peak lasts only a few frames of a 320 ms beat (`seats/emil-kowalski.md` L72, 240-560 ms), twice, on a spring. The tip is out at the side of the body, past the outline, not centred under the eyes, so it cannot read as a mouth. The rest-pose rule protects the still read (cards, idle), and the wave is never shown on a card (fix-brief-v4 L43).
   - **Opinion:** do not go past +40 deg. Above the eye line, the arm starts to read as a horn or an ear in the silhouette.
3. **Tie B is clear of the wave path.**
   - **Fact** `ghostie-sheet.png` WAVE panel (crop x 1380-1800, y 880-1220 at 2x): the right collar wing of the tie ends about 10 px (sheet scale) inside the arm root. The arm pivots at its root (`src/ghost.py` L40, root about 249,213) and swings out and up, away from the tie.
   - **Opinion:** they do not collide. The gap is small, so Viet must keep the collar wing inside the body hull in 3D.
4. **Parts allow the float bob.**
   - **Fact** `seats/emil-kowalski.md` L92-93: y +/- 0.06 m, 2.4 s, with x and yaw sines. The WAVE panel shows the bob arrow.
   - **Opinion:** the body is one closed hull with no loose part, so the bob needs no extra joint. The tie moves with the body.

## Notes (not a fail)
- **Fact** `src/build.py` L210 (sheet SHAPE RULES text): "tips below the eye line at all times". This conflicts with the wave. Narrow fix in the next sheet pass: change it to "tips below the eye line at rest; the wave may reach the eye bottom, never above it".
- **Fact** `seats/emil-kowalski.md` L72 says "arm yaw +/- 20 deg", and fix-brief-v4 L42 says "+40° up". **Opinion:** the later fix-brief note is the current one. I will align L72 to it at the build phase. This is my file, and it does not change the sketch.
- For the game build: check the wave at 0.25x (fix-brief-v4 L42).
