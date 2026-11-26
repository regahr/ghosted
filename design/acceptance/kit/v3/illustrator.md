Illustrator (Illustrator): Kit v3, GHOSTED acceptance gate, items I1-I4

## Offer

- `~/.claude/skills/illustrator/SKILL.md` § 9.2 (Composition Critique): the "view at thumbnail size" and "squint / value structure" checks. I used them as the method for I1 (64 px silhouettes, read pixel by pixel) and I3 (card strip at its real size).
- `~/.claude/skills/illustrator/references/standards.md` (§ 7.10 checklist): this is general illustration QA. It does not add to a 3D-kit gate that has its own checklist, so I did not apply it item by item.
- No tool of mine was blocked by the brief.

## Scores

| Item | Verdict | Evidence |
|---|---|---|
| I1 [must] 64 px silhouette: round head, sprout, case | **PASS** | Fact: in `assets/kit/silhouette-64.png` the sprout is 2-3 px wide at its base (rows 4-6; v2 was about 1 px) and curls at the tip. The head is a clean disc. The case is a separate block with 3-4 px of background between it and the leg (rows 47-58). In `silhouette-64-34.png` the head and sprout read, and the case reads as a block with a handle notch (row 49). But it still joins the leg (see fix note 1). |
| I2 [must] Hand-made shapes | **PASS** | Fact: `turn-front.png`, `turn-34.png` and `hero.png` show a clean fist on a rounded handle loop, with both handle legs visible and no brown spikes. `turn-back.png` shows a jagged nape hairline with 2-3 points instead of the v2 bowl cut. The other parts are still shaped: a tie with a knot, a pointed collar, tapered sleeves, shoe lobes, a chamfered case. |
| I3 [must] Expressions told apart at card size | **PASS** | Fact: `expr-focused.png` now has half-height eyes with a flat upper lid, tilted-in brows and a short off-centre mouth. It no longer shares the dot eyes of `expr-ghosted.png`. In `expr-card-strip.png` each face has its own mark: hopeful (open ovals, smile), ghosted (dots, flat line, drooped sprout, sweat drop), rejected (closed arcs, smile, bent sprout, sweat drop), focused (lidded eyes), offer-joy (open "D" mouth, tall sprout). |
| I4 [should] Its own design | **PASS** | Opinion: no change from v2. The round head, sprout, blue sweater, tie, lanyard and case are generic parts and do not add up to a known character. |

**Overall: PASS** (I1, I2, I3 must: pass. I4 should: pass.)

## v2 fix notes: status

1. Focused half-height eyes: **done** (`expr-focused.png`).
2. Nape locks: **done** (`turn-back.png`). No spikes at the grip: **done** (`turn-front.png`, `turn-34.png`, `hero.png`).
3. Thicker sprout base: **done** (`silhouette-64.png` rows 4-6). Case out from the leg in the 3/4 silhouette: **not done**. Fact: `changes.md` line 28 says "`silhouette-64-34-x4.png`: the case is separated from the leg by background". The pixels say otherwise. In `silhouette-64-34.png`, rows 50-60 are one solid run from the leg into the case, and no background column lies between them. The 1.2 cm move (same line) is less than the 5 cm I asked for in v2.

## Fix notes (none blocks the gate)

1. **3/4 case gap (I1).** Move the case about 4-5 cm further out, or turn it about 15-20 degrees, so that `silhouette-64-34.png` shows at least 1 px of background between the leg and the case. Then fix the claim in `changes.md` line 28 so it matches the pixels.
2. **Rejected vs hopeful at game camera (I3, outside the card gate).** In `expr-gamecam-strip.png` at 1x, rejected and hopeful both read as "smile". Spec `seats/illustrator.md` line 41 (Rejected-but-fine row) gives rejected a right-arm thumbs-up. Add that pose swap, so the state reads from the body when the face is only a few pixels high.
3. **Side-view temple (I2, polish).** In `turn-side.png` a skin wedge still shows between the fringe lock and the side hair. Lengthen the sideburn lock by about 1 cm to close it.
