Illustrator (Illustrator): Ghostie v1, GHOSTED acceptance gate card 2, items I1-I4

## Offer

- `~/.claude/skills/illustrator/SKILL.md` § 9.2 (Composition Critique): the "view at thumbnail size" and "squint" checks. I used them for I1 (I read the 64 px silhouettes pixel by pixel at a 50% threshold) and I3 (card strip and game-camera crops).
- `~/.claude/skills/illustrator/references/philosophy.md` line 26 ("Readability is King"): used for I3 and for the tie-as-nose read.
- `~/.claude/skills/illustrator/references/risks.md` line 12 (do not copy existing characters): used for I4.
- The brief blocked none of my tools. I read `selfcheck.md` and `changes.md` only as claims and checked them against the PNGs.

## Scores

| Item | Verdict | Evidence |
|---|---|---|
| I1 [must] 64 px silhouette: dome, flared skirt with hem, arms | **PASS** | Fact: `assets/ghostie/silhouette-64.png` (79x64). Dome rows 0-19. Arms are a ledge at rows 34-42 (width 51 to 73 px, then back to 56 at row 43). The skirt widens from 53 px (row 44) to 59 px (row 56). The hem has 2 notches at rows 57-59 (2-3 px deep) and a centre lobe to row 63. Fact: in `silhouette-64-34.png` the arms are nearly gone (1 px at rows 43-44) and the hem has 1 notch (rows 59-62). Opinion: the front view carries all 4 cues; the 3/4 view is weak on the arms. |
| I2 [must] Hand-made shapes, designed profiles | **FAIL** | Fact: `hero.png`, `turn-front.png` and `variants.png` at card size show the outline as straight segments: about 6 per side on the crown and side, with clear corners. The eyes are 8-sided polygons with no highlight. The hem is a zigzag of straight lines with sharp V notches (`crops/hem-notch-34.png`), not soft scallops. In `hero.png` the left arm is a thin wedge whose ink does not close, and in `variants.png` (headset) the near arm is a loose outline fragment. The tie has no ink edge and is a flat lavender shape (`crops/tie-on-surface.png`). Fact: locked Kit (`assets/kit/hero.png`) has smooth curves, value modelling and eye highlights. Opinion: the parts do have designed profiles (flare, hem tabs, tapered flaps), so the letter of I2 is close. But at card size the ghost reads as a low-poly code model, a clear step below Kit. This is the "slopped" look Rega rejected. It fails the bar of "hand-made and charming at card size". |
| I3 [must] Variants told apart at card size (and at game camera if possible) | **PASS** (card) / weak (game) | Fact: in `variants.png` the tie, the hex glasses and the headset band with ear cup are each clear. Fact: in `lineup-grass.png` at 1x the 3 ghosts are about 40 px tall and I cannot tell them apart. In `lineup-grass-crop-x3.png` and `lineup-path-crop-x3.png` the glasses read as a bar between the eyes and the headset as a faint arc. The tie reads as a small mark under the eyes. Opinion: at game camera the tie looks like a nose or a mouth. That breaks the "no mouth, a ghost never replies" idea (`bible.md` line 30). |
| I4 [should] Its own design | **PASS**, with a watch note | Opinion: a dome ghost with no mouth, wide dots and a faded office accessory is generic and its own. Watch: the black front silhouette (`silhouette-64-x4.png`) is a dome with side nubs and a wavy hem. That is close to a well-known app-logo ghost. The eyes, tie and pose separate it in colour, so this is not a fail. |

## Size change (changes.md decision 1)

**Accepted.** Fact: in `lineup-grass-crop-x3.png` the ghost is about half Kit's height, and Kit's head and sprout stay on top. Opinion: at 1.0 H (about 20 px in game) the accessories would be lost, and they are already faint at 27 px. The ghost still reads as small, a joke and not a threat. My 1.0 H ask was a starting size, not a story rule.

## Other notes (not gate items)

- Opinion: in `turn-front.png` the tie sits directly under the eyes, where a beak would be. The front face reads as a bird or a penguin.
- Opinion: in `hero.png` (3/4) the far eye is a thin sliver at the edge of the face, because the eyes are set wide (decision 2). It is fine from the front. In 3/4 it looks a little fish-like.
- Fact: the lit body is cream/beige in `hero.png`, and the ghosts read pink in `lineup-grass-crop-x3.png`. The colour is Lena's call, so I do not score it.

**Overall: FAIL** (I2 must fails. I1 and I3 pass. I4 passes.)

## Narrowest fix list

1. **Rounder outline at card size.** Put the triangles into the profile, not the columns. Add dome and side rings so that the front and 3/4 outline has no visible corners at 1200 px. Use 12-sided eye dots. If 300 triangles cannot hold this, Viet must choose: raise the ghost budget, or drop a column count (V5 is Viet's call).
2. **Soft hem.** Change the hem tabs and sharp V notches to round scallops: curved lobes and a rounded notch. Keep the 2 notches that read in the front 64 px silhouette.
3. **Arms.** Close the ink on both flaps in `hero.png` and the headset view, and round the flap tip so it reads as a little mitten and not a cut triangle.
4. **Tie.** Move it down to the chest, below the arm line, and give it one darker value or a thin ink edge. Then it does not read as a nose or a mouth at either size.
5. Optional (should): turn the eyes in a little, about 4-5 degrees, so the far eye does not become a sliver in 3/4. Only if Viet can keep the glasses clean.

Re-render `hero.png`, `turn-front.png`, `turn-34.png`, `variants.png`, `silhouette-64*.png` and `lineup-grass-crop-x3.png`, and I will score again.
