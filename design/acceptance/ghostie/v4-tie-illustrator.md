Illustrator (Illustrator): Ghostie v4, tie only (card 2, I2 and I3). Arms not scored.

Read from the frozen archive `assets/ghostie/v4/` only, plus `assets/kit/hero.png`. No asset edited.

## Offer
- `~/.claude/skills/illustrator/SKILL.md` § 9.2: the "view at thumbnail size" and "squint" checks. Used for Q1 on the x3 lineup crops.
- `~/.claude/skills/illustrator/SKILL.md` § 1.3 "Story First": a prop must say its one word at a glance. Used for Q1 and Q2.
- `~/.claude/skills/illustrator/SKILL.md` § 10 #1 "Over-detailing": keep the fix to the fewest marks. Used for the fix.

## Answers
1. **Tie at card size: NO.**
   - Fact: `lineup-grass-crop-x3.png` and `lineup-path-crop-x3.png`, left ghost (about x 180-205, y 65-125): a thin lilac line with a small hook at the top. Kit's tie in the same crop (about x 665-680, y 200-245) is red, wide, with a knot on top against a white collar.
   - Fact: `crops/tie-vs-kit.png`: Kit's tie has a knot at the top, a blade that widens down, a V point, and ink on both sides. The Ghostie tie has a tiny knot at the bottom, a thin blade, a slanted wedge at the top, and no ink.
   - Opinion: in the lineup it reads as a hair streak or a strap, the same as v3. Next to Kit it does not read as the same object.
2. **Tip in the air: reads as a horn or a hair ribbon, not as a tie blown back.**
   - Fact: `turn-front.png` (x 610-680, y 322-400) and `variants.png` panel 1 (x 370-425, y 215-270): the tip is a slanted wedge at crown height that sits just past the outline.
   - Opinion: people read a tie by "knot on top, point at the bottom". Here the knot is at the bottom and the wide end is at the top. So the eye reads a dagger or a quill on the body, with a horn or a bow at the crown. The tip is cut flat on one side, not a V. It is also stiff and straight, so nothing says "wind".
3. **Hand-made shape: NO.**
   - Fact: `hero.png` knot (x 625-665, y 650-690): a 5-sided nub that is about as wide as the blade, with no step to the blade. Fact: blade (x 650-760, y 380-650): straight sides, so it widens in a line with no curve. Fact: no ink on the long sides in `hero.png`, `variants.png` or `crops/tie-vs-kit.png`. Fix 4 of `fix-brief-v4.md` (line 30) asked for that ink.
   - Fact: `turn-side.png`: ink on one side only (x 270-410, y 400-640), and a loose ink stub at x 395-405, y 322-405 that does not close round the tip.
   - Opinion: it looks like a machined part, not a drawn tie. Kit's tie (`assets/kit/hero.png`, x 505-565, y 585-740) has the knot, the step, the V and the ink that this one does not have.
4. **Verdict: FAIL for the tie part of I2** (no ink, a knot with no step, a cut wedge tip, a loose ink stub). **I3 tie part: PASS for "told apart"** (Fact: `variants.png`, the tie panel is clearly different from glasses and headset). **FAIL for meaning**, because it does not say "tie" (Q1).

## Narrowest fix (keep the over-the-shoulder joke, change only these)
1. Ink: one closed ink stroke round the whole tie, at the same weight as the body outline, as on Kit. This is the largest single gain.
2. Knot: a clear trapezoid about 1.5x the blade root width, with a step (notch) where the blade starts. It sits at the neck point, which is the top of the front-facing part. Same place as Kit's knot: just under the "collar", not halfway down the body.
3. Tip: a symmetric V point like Kit's, not a slanted cut.
4. Wind: one soft S-bend in the blade, and lift the V clear of the outline by about one blade width, so it reads as cloth that flaps, not a horn.
5. Width at the game camera: make the blade about 2x wider in the lineup crops. At present it is one pixel line at x3 (Opinion).
- Check: `crops/tie-vs-kit.png` again, then both lineup x3 crops. If it still reads as a horn after 1-4, return the choice to Rega: a down-hanging tie on the front (option A, my pick for the read) or the blown-back tie (option B, the joke).
