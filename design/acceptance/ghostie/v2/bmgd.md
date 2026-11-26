BMGD (Game Designer): Ghostie v2, card 2, items B1-B2

## Offer

- `bmad-game-dev-studio/0.7.2/src/workflows/2-design/gds-create-narrative/checklist.md` line 54 ("Each has distinct role in story") and line 111 ("Tone matches GDD art/audio direction"). Same test as v1: B1 = role, B2 = tone.
- `design/seats/bmgd.md` Cast table, Ghosties row: the Ghostie is a collectible result ("Brenda from Talent"). This sets what the accessory must say: "this was a recruiter".
- No tool of mine is blocked by this brief.

## Items

- **B1. FAIL.** Name, role, size and most of the tone match. The tie variant still breaks "no mouth" at the 26 m camera.
  - Fact: bible: "It has no mouth, because 'a ghost never replies'" (`design/bible.md` line 30); "The ghost with no mouth" (line 51).
  - Fact: `variants.png`, `hero.png`: at card size the tie sits low on the chest, below the arm, with an ink edge. It reads as a tie. Fix 5 is done as written (knot top z 0.141 below arm root 0.160, `changes.md` line 44).
  - Fact: `lineup-grass-crop-x3.png`, `lineup-path-crop-x3.png`, left ghost: the top-down camera shortens the body, so the "chest" lands just under the eyes. The lilac shape now has a dark ink top edge, sits between and below the two eye dots, and runs to the hem.
  - Opinion: it reads as a mouth with a tongue out (a "blep"), or a drip from a nose. The read is stronger than v1: v1 was a faint smudge (`v1/lineup-grass-crop-x3.png`); v2 is a framed, darker mark in the exact mouth spot. The ink edge that was meant to help makes it look like lips.
  - Fact: glasses (middle) and headset (right) read in the same crops. The headset band is a visible arc on the crown now. No mouth on either.
  - Fact: role. Ghost body 27 px against Kit 55 px (`ingame_report.json`, `lineup-grass`). It reads as a small collectible, not a threat.
- **B2. PASS.** Comic and kind. Nothing mocks the player.
  - Fact: `variants.png`, `hero.png`, both lineup crops: round dome, small dot eyes, stub arms, no teeth, no brows, no sneer.
  - Opinion: one flag. The tongue-out read of the tie variant is close to a raspberry, which is a taunt. With the vacant eyes it reads cheeky, not cruel, so I do not fail B2. The B1 fix removes this risk too.

## Why moving it down did not work (Opinion)

At 26 m we look down on the dome. Any centred mark on the front, below the eyes, lands in the mouth zone, however low it sits on the body. Moving it lower cannot fix it; the mark must change its shape or leave the centre of the face.

## Narrowest fixes (tie variant only; the other two variants are done for me)

1. Give the tie a shape no mouth has. Pick one (Illustrator and Viet own the shape):
   a. My pick: the tie flips sideways over one shoulder, as if blown by a fast exit. It runs diagonal and crosses the side outline, so it changes the silhouette. A mouth never leaves the face.
   b. Add a white shirt-collar V with ink above the knot, so the tie has the same context that makes Kit's tie read in the same crop.
2. Remove the dark ink line on the top of the knot. Keep the ink only on the long sides.
3. Re-shoot `lineup-grass-crop-x3.png` and `lineup-path-crop-x3.png`. The test: at x3, the left ghost has two eye dots and nothing in the centre below them.

**Overall: FAIL** (B1 only: tie variant reads as a mouth with a tongue out at the 26 m camera. Fix 1 clears my items.)
