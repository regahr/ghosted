Illustrator (Illustrator): Ghostie v3, GHOSTED acceptance gate card 2, items I1-I4

All paths are under `runs/jobless-roguelike/design/`. I judged from the PNGs only. I read `selfcheck.md` and `changes.md` as claims. SK and S1 are not scored (Rega's exemption).

## Offer

- `~/.claude/skills/illustrator/SKILL.md` § 9.2 (Composition Critique): the "view at thumbnail size" and "squint" checks. I used them for I1 (row-by-row width of `silhouette-64.png` at a 50% threshold), for the ear read and for the tie read at the game camera (`lineup-grass-crop-x3.png`, enlarged 2x).
- `~/.claude/skills/illustrator/SKILL.md` § 1.3 ("Story First", "Hierarchy of Read"): I used it for the tie question. A prop must say its one word at a glance.
- `~/.claude/skills/illustrator/SKILL.md` § 10 #2 (cliché imagery): I used it for I4.
- The brief did not block any of my tools.

## My v2 fixes: did they land?

| v2 fix | Landed? | Evidence |
|---|---|---|
| 1. Arms: flat tapered flap, no joint, root 10-15% lower, droop 25-35°, round tip | **Partly** | Fact: `turn-front.png` arms now sit at y≈640-770, under the eyes (y≈500-575); the left arm droops down and out. Fact: `hero.png` and `turn-34.png` near arm is still horizontal, with a flat top edge and a 5-segment polygon tip: it reads as a thumb. Fact: `crops/arm-root-front.png` the body ink steps out at the root and a pale sliver shows; `variants.png` x≈420-445, y≈425-520 (enlarged): an ink spur runs into the body above the arm and a small hook hangs under it, in all 3 panels. |
| 1b. Arms must not read as ears at the game camera | **No** | Fact: `lineup-grass-crop-x3.png`, all 3 ghosts: the arm nubs sit level with the eye dots (left ghost nubs y≈105, eyes y≈108; middle ghost nubs y≈190-195, eyes y≈195). Opinion: the middle ghost reads as a round head with 2 ears. The builder also says so (`selfcheck.md`, "Still weak" 4). |
| 2. Hem outer corners not flared, notch top a curve | **Corners yes, notch no** | Fact: `silhouette-64-x4.png` the outer hem corners curl in. Fact: `crops/hem-notch-34.png` the notch top is still one sharp apex between 2 straight segments, not a curve. |
| 3. Hem notch +2 vertices | **No (see 2)** | Same file. |
| 4. Round crown and shoulders, no corners at 1200 px | **Mostly** | Fact: `hero.png` the crown reads as a curve at card size, but straight segments still show at 1200 px, and the right shoulder has a hard corner (x≈770, y≈370; `turn-front.png` x≈620, y≈370). Opinion: a big step up from `v2/hero.png`; acceptable in proportion to Kit's known limits. |
| 5. Tie (chair took BMGD's over-the-shoulder option) | **Does not read as a tie** | See "Tie read" below. |
| 6. Optional: eyes turned in | **Done** | Fact: `hero.png` far eye is a full oval (x≈410), not a sliver. |

## Tie read (asked by the chair)

**No, it does not read as a tie.** Opinion, on these files:
- `hero.png`, `turn-front.png`, `variants.png` panel 1: a thin lilac strap of even width from the shoulder, ending in a small flared tab just right of and level with the right eye. There is no knot and no wide blade. Next to Kit (`assets/kit/hero.png`: red tie with a knot and a wide blade) it reads as a bag strap, a sash or a ribbon.
- `turn-side.png`: the tie is an arch over the top of the head. It reads as a headband or hair clip.
- `lineup-grass-crop-x3.png` and `lineup-path-crop-x3.png`, left ghost: a thin lilac diagonal line beside the right eye. It reads as a scratch, a scar or a tear streak. The B1 test (nothing centred below the eyes) is met, but the mark is now at the eye.
- Opinion: BMGD owns B1. My call is on shape: the over-the-shoulder idea can work, but the drawn shape lost the two cues that say "tie": the knot and the blade.

## Scores

| Item | Verdict | Evidence |
|---|---|---|
| I1 [must] 64 px silhouette: dome, skirt with hem, arms | **PASS** | Fact: `silhouette-64.png` (78x64): dome rows 0-19; arms rows 40-54 (width 52 to 62 px, then back to 53 at row 54); skirt and 5-scallop hem rows 54-63 (`silhouette-64-x4.png`). Fact: `silhouette-64-34-x4.png` the near arm is a small bump on the right edge and the far arm does not show. Opinion: the front view carries all 3 cues; the 3/4 arm read stays weak. |
| I2 [must] Hand-made shapes, designed profiles | **FAIL** (narrow) | Fact: ink spur and hook at the near arm in all 3 panels of `variants.png` (x≈420-445, y≈425-520) and the root sliver in `crops/arm-root-front.png`. Fact: the hem notch is a sharp apex (`crops/hem-notch-34.png`). Fact: the near arm is a thumb with a flat top and a polygon tip (`hero.png`, `turn-34.png`). Opinion: the body is now close; the crown passes in proportion. But the arm, the one part that gives the ghost its gesture, is still a machined stub with broken ink at card size. These are the "slopped" marks Rega rejected. |
| I3 [must] Variants told apart at card size | **PASS** | Fact: `variants.png` tie (lilac strap), 8-sided glasses with bridge, 12-sided ear cup with band: each is clear and different. Fact: `crops/headset-cup-on-surface.png` a pale sliver on the cup's right edge (small). Opinion: told apart, yes. The tie variant does not say "tie" (see above); that is a meaning fault, not a "told apart" fault. |
| I4 [should] Its own design, not the app-logo ghost | **PASS** | Fact: `silhouette-64.png` arms now at 63-84% of the height (v2: 50-67%), hem has 5 scallops and curled-in corners (`silhouette-64-x4.png`). Opinion: the mid-height nubs and the flared points are gone; the front silhouette no longer matches the app-logo ghost. |

**Overall: FAIL** (I2 must fails narrowly. The tie does not read as a tie and the arms still read as ears at the game camera; both are brief fixes that did not land.)

## Known limits (accept if the rest passes)

- Small straight segments on the crown at 1200 px and one shoulder corner (`hero.png`).
- Far arm hidden in the 3/4 silhouette (`silhouette-64-34-x4.png`).
- Pale sliver on the ear cup edge (`crops/headset-cup-on-surface.png`).

## Narrowest fixes

1. **Arm ink and joint (I2).** Remove the ink spur above the near arm and the hook under it (`variants.png`, all panels). Close the root so the body outline flows into the flap with no step and no sliver (`crops/arm-root-front.png`).
2. **Arm shape (I2).** Round the top edge and the tip of the near arm; droop it 25-35° like the left arm, so it is not a horizontal thumb (`hero.png`, `turn-34.png`).
3. **Ear read (game camera).** The top-down camera puts the arms on the eye line. Lowering the arms alone did not fix it. The narrowest fix: raise the eyes about 8-10% of body height on the dome (keep them on the front face), and drop the arm tips further so the tips sit clearly below the eye line in `lineup-grass-crop-x3.png`.
4. **Hem notch (I2).** Round the apex in `crops/hem-notch-34.png` into a curve (2 more vertices at the top).
5. **Tie (meaning; BMGD's B1 decides).** Keep the over-the-shoulder path, but add a knot at the neck point (front, between the eyes and the arm line, offset to the tie side) and widen the blade end into a clear tie point, and move the blade end away from the right eye so it does not read as a tear or a scar at 26 m. Check it next to Kit's tie in a side-by-side.

Re-render `hero.png`, `turn-front.png`, `turn-34.png`, `variants.png`, `crops/arm-root-front.png`, `crops/hem-notch-34.png` and `lineup-*-crop-x3.png`, and I will score again.
