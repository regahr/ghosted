# Emil Kowalski (Principal Designer): Ghostie sketch v2 gate, item SK5 and the whole-picture check

## Offer
- `~/.claude/skills/emil-design-eng/SKILL.md`, "Spring Animations" (bounce 0.1-0.3) and "Debugging Animations" (frame by frame). I use these to judge the wave as a moving beat and its peak frame, and not only as a still.
- `~/.claude/skills/improve-animations/AUDIT.md` (0.25x audit): this is for the game build, not for this sketch.
- The brief blocks none of my tools. This task does not draw, so I wrote no `ready.md`.
- I made my own 2x and 4x crops from the PNGs, in the scratchpad only, and did not use the Illustrator's `crops/`. I edited no asset.

## SK5: FAIL (one narrow fix: the rest-pose arm)

1. **Rest pose: it reads alive, but one arm has a hook.**
   - **Fact** `assets/ghostie/sketch/src/ghost.py` L74-80 (FRONT_REST): the drooped arm_R path goes `46,260 -> C44,250 38,256 30,262`. The outline goes up, then turns back down in a tight U. At 2x and 4x (sheet x 1830-1960, y 1040-1180) this shows as a pinched V notch under the drooped tip. The tip curls into a small claw.
   - **Fact** `acceptance/ghostie/sketch-fix-v2.md`, fix 2: "no step or kink. Check both arms in every view."
   - **Opinion:** the 4 deg tilt, the uneven arms and the open face with no mouth read alive and kind. The hooked tip under a limp straight arm top (`14,244 -> 48,190`, one long straight run) makes the arm read limp and a little claw-like, and less shy-and-kind. This is the "crooked flaw" kind that Rega rejected. Fix: round the underside the same way as the upright arm (`C264,247 256,250 254,260`, L44), only lower. Do not change the tilt.
2. **Wave clears the centred tie and collar: PASS.**
   - **Fact** sheet TIE BUILD SPEC text: "Centred on the body axis (x 150). Collar: 2 flat wings, span 46", so the collar spans x 127-173.
   - **Fact** `ghost.py` L61-71: the raised arm's inner root is at x 252-256, so the gap from the collar is about 80 units. At 2x (sheet x 1300-1760, y 840-1240) the right wing ends far inside the arm root.
   - **Opinion:** no collision is possible. The arm swings out and away from the axis.
3. **Wave tip with the eyes at y 118: it lands at collar height, out at the side.**
   - **Fact** `ghost.py` L21-22: eye 118, eye_bottom 131. L66-67: the raised tip peaks at about y 175 (`282,174` with control `296,170`).
   - **Fact** at 2x: the tip top is at about sheet y 1017, and the eye bottom is at about sheet y 974.
   - **Result:** the tip sits about 44 units below the eye bottom. It is level with the neck line (166) and the knot top (170), at x 282-302, outside the body edge. The spec "never above the bottom of the eyes" holds with margin.
   - **Fact** `src/build.py` L196-197 and L299: the sheet rule now reads "arm tips below the eye bottom (y 131) at rest and in the wave". This closes my v1 note.
   - **Opinion:** the swing is about 43 deg (rest about 20 deg down, wave about 23 deg up), so it matches +40. The headroom now allows a bigger wave, but the spec stays +40. Do not change it at the sketch stage. At the game camera the wave is a small "hi" flap. Check it frame by frame in the build.
4. **Parts allow the motion (bob, wave): PASS.**
   - **Opinion:** the body is one closed hull, and the tie is a flat print that moves with it. No loose part needs a joint.

## Whole-picture check (2x, every panel)

### ghostie-sheet.png
- **FRONT:** **Opinion:** the shade band ends in a hard curved cut across the left hem lobe and does not follow the lobe. It is minor. No other flaw seen. The dome is symmetric, and the shoulders are soft.
- **3/4:** **Opinion:** the collar wings are the same width on both sides. In a 3/4 turn the far wing should be a bit narrower. It is minor. No shape flaw seen.
- **SIDE:**
  - **Fact:** the eye ellipse (`ghost.py` L233, x 77 ± 4.5) sits on the front outline, so ink merges with ink and the edge bulges at 2x.
  - **Opinion:** the end-on arm oval still reads as a hole or a pocket. This is known, and Viet ruled on it (`sketch-viet.md` §5).
- **BACK:** none seen. The notch is centred, and the shade is mirrored correctly.
- **VARIANT tie:** none seen apart from the front shade cut.
- **VARIANT glasses:** none seen.
- **VARIANT headset:**
  - **Fact** `ghost.py` L191: the band top is y 46 with stroke 9, so its top edge is at about 41.5. That is inside the crown outline at y 36. At 3x the crown ink shows ABOVE the band, so the band reads as a stripe painted on the forehead, not as a band over the head. Fix 3 of `sketch-fix-v2.md` says "goes over the crown".
  - **Opinion:** the band has no ink edge, and the cups have one. This is inconsistent.
- **WAVE:**
  - **Opinion:** the faint blue rest arm is a loop that is open on the body side and has low contrast. It reads as a handle on the hip.
  - **Opinion:** the flank under the raised arm (`256,226 -> 262,292`) is flatter than the mirrored side.
  - **Opinion:** add a small swing arc from rest to +40 so that the panel shows motion, as the bob arrow does.
  - Labels are clear of the body.
- **REST POSE:** **Fact:** the hooked, pinched notch under the drooped arm_R (see SK5.1). The shade band starts at that notch with a hard vertical edge.
- **64 px silhouette:** none seen.
- **Game camera x3:** **Opinion:** the centred tie reads as a tongue under the eyes. This is a known risk, and Rega accepts it (`chair-read-sketch-v2.md`, ts 1795615890.262169).
- **Tie build spec:** none seen.
- **Palette and rules:** none seen.

### body-map.png
- **A explore:** none seen. The blue mouth boxes are notes.
- **B front landmarks:**
  - **Fact:** the "2nd head" label sits on the arm-root-top guide line, and the line strikes through the text. This breaks fix 6, "no text touches or overlaps any drawing".
  - **Fact:** the head ruler stops above the hem line. Its end tick floats about 50 px lower, alone, just above the "C. ATTACHMENT POINTS" heading.
  - **Opinion:** the guides at 258 and 260 make a double line, which looks like a mistake.
  - **Opinion:** the header says "body 265 crown-to-hem", and PROPORTIONS says "280 units". These are two measures with no label to tell them apart.
- **B notes:** none seen beyond the 265/280 wording.
- **C attachment:** **Fact:** the headset band is again inside the crown ink, the same as the sheet headset variant. The other 3 figures: none seen.
- **D game camera:** **Opinion:** tongue risk (tile 3), as known. No drawing flaw seen.

## Verdict
SK5 FAIL on one narrow fix: round the underside of the drooped arm in the rest pose. The wave clears the tie and the collar, and its tip lands at collar height, about 44 units below the eye bottom.

Open visible flaws that block the card under the whole-picture rule:
1. The rest-pose arm hook.
2. The headset band sits inside the crown, on the sheet and on body map C.
3. The "2nd head" label is struck through by a guide line, and the ruler end tick floats (body map B).
4. The eye merges into the outline in the side view.

The other items are Opinion polish.
