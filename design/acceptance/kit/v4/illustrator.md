Illustrator (Illustrator): Kit v4, GHOSTED acceptance gate, items I1-I4

## Offer

- `~/.claude/skills/illustrator/SKILL.md` § 9.2 (Composition Critique): the "view at thumbnail size" and "squint / value structure" checks. I used them for I1 (I read the 64 px silhouettes pixel by pixel, at a 50% grey threshold) and I3 (the card strip at its real size).
- `~/.claude/skills/illustrator/references/standards.md` (§ 7.10 checklist): general illustration QA. It adds nothing to a 3D-kit gate that has its own checklist, so I did not apply it item by item.
- The brief did not block any of my tools. I did not use `changes.md` or `crops/sil34-rows.json` as evidence. I checked their claims against the PNGs.

## Scores

| Item | Verdict | Evidence |
|---|---|---|
| I1 [must] 64 px silhouette: round head, sprout, case | **PASS** | Fact: in `assets/kit/silhouette-64.png` the head is a clean disc, the sprout is 2-3 px wide and curls (rows 0-6), and the case is a separate block (rows 48-60). In `silhouette-64-34.png` the case now has background between it and the leg. The gap is 2-3 px of white in rows 54-61. In rows 49-53 it is only 1 px of light grey (luma 162-215 at x 29-30), so the top corner is a soft join, not a clean cut (see fix note 2). In v3 rows 50-60 were one solid run. |
| I2 [must] Hand-made shapes | **PASS** | Fact: `crops/sleeve-side-v2-v3-v4.png` shows the closed, outlined sleeve cap again (in v3 it was two loose wedges). `crops/temple-side-v3-v4.png` shows one diagonal hairline with no skin wedge. The fist outline is closed with no spikes (`crops/grip-*-v3-v4.png`). Tie, knot, collar, tapered sleeves, nape locks and chamfered case are not changed. The grip has a new drawing problem (fix note 1), but it is a hanging and weight problem. The shapes are still designed shapes. |
| I3 [must] Expressions told apart at card size | **PASS** | Fact: in `expr-card-strip.png` each face has its own eyes and mouth, as in v3. The sprout now adds a second cue. Hopeful has a curl, ghosted is flat with a sweat drop, rejected bends hard to the right with a sweat drop, focused is a thin straight spike, and offer-joy is the tallest curl. `expr-gamecam-strip.png` shows the same sprout shapes at 3x. |
| I4 [should] Its own design | **PASS** | Opinion: no change since v2. The round head, sprout, blue sweater, tie, lanyard and case are generic parts. They do not add up to a known character. |

**Overall: PASS** (I1, I2, I3 must: pass. I4 should: pass.)

## v3 fix notes: status

1. Case out from the leg in the 3/4 silhouette: **mostly done.** The bottom two-thirds of the case is clear. The top corner touches through 1 px of anti-aliased grey (rows 49-53).
2. Rejected vs hopeful at game camera: **done in another way.** The sprout now bends the other way. Opinion: this is enough for the card gate. I did not get the thumbs-up pose, and it stays a nice-to-have.
3. Temple skin wedge: **done.** Fact: in `turn-side.png` at 1x, a skin-coloured sliver about 1 px wide still shows along the outline near the sideburn tip (about x 370-385, y 320-380). You cannot see it at game size.

## Regression check (the case arm now angles out)

- Fact: in `turn-front.png` and `turn-back.png` the case arm now hangs about 30-35 degrees out from the body (v3: about 20 degrees, `v3/turn-front.png`). Opinion: the arm reads as stiff and held out. The gesture says "keep this away from me", and a real heavy case does not hang like that. It does not fail a gate item.
- Fact: `crops/grip-front-v3-v4.png`, `grip-hero-v3-v4.png` and `grip-back-v3-v4.png`. In v4 the hand sits on top of the handle, and the handle legs run out sideways at a low angle. In the back crop they lie nearly flat along the case top. The open counter of the handle loop, which read well in v3, is gone. In `turn-front.png` the case hangs to the right of the hand and is tilted (hand x 731, case centre about x 778), so it does not hang plumb under the grip.

## Fix notes (none blocks the gate)

1. **Make the case hang plumb (I2, grip).** Put the case's centre of mass straight below the fist and keep the arm angle. Then the handle legs go up nearly vertical out of the fist, and the loop shows an open counter again (as in v3). If the 3/4 gap needs more room, turn the case another 10 degrees or so. Do not swing the case sideways.
2. **Clean up the 3/4 top corner (I1).** Chamfer the case's inner top corner a little more, or move the case 1 cm lower, so that rows 49-53 of `silhouette-64-34.png` show at least 1 px of background above 50% luma with no grey bridge.
3. **Relax the case arm (polish).** Bring the upper arm back to about 20-25 degrees and bend it slightly at the elbow, so the case side stays clear without the stiff, held-out look in `turn-front.png` and `turn-back.png`.
