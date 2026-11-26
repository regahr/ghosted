Illustrator (Illustrator): Kit v5, GHOSTED acceptance gate, items I1-I4

Scope: v5 changes only the case arm, the wrist and how the case hangs (`assets/kit/changes.md` L1-L18). Re-score of I1-I4. The v4 score is in `v4/illustrator.md`.

## Offer

- `~/.claude/skills/illustrator/SKILL.md` § 9.2 (Composition Critique): the "view at thumbnail size" and "squint" checks. I used them for I1: I read `silhouette-64.png` and `silhouette-64-34.png` pixel by pixel (luma, 50% threshold = 128), and I looked at the x4 copies at real size. I also used them for I3, on `expr-card-strip.png` at its real size.
- `~/.claude/skills/illustrator/references/standards.md` (§ 7.10 checklist): general illustration QA. The gate has its own checklist, so I did not apply it item by item.
- The brief did not block any of my tools. I did not use `changes.md` or `crops/sil34-rows.json` as evidence. I checked their claims against the PNGs.

## Scores

| Item | Verdict | Evidence |
|---|---|---|
| I1 [must] 64 px silhouette: round head, sprout, case | **PASS** | Fact: `silhouette-64-34.png`, column x 29: rows 50-53 have one grey gap pixel (luma 148, 173, 181, 223), and rows 54-58 have a clean 3 px white gap (x 27-29, luma 241-255). Every row 50-58 has background above 50% between the leg and the case. Front `silhouette-64.png`: rows 50-53 have 1 clean px (x 31, luma 254-255) plus a grey px, and rows 54-58 have 3-4 px. Head disc and sprout curl are not changed. |
| I2 [must] Hand-made shapes | **PASS** | Fact: `crops/arm-front-v4-v5.png` and `crops/arm-back-v4-v5.png` show the v5 sleeve as a tapered tube with a visible break at the elbow and a closed outline. `crops/grip-*-v5.png` show a closed fist outline, and the handle legs come out from under the fist. |
| I3 [must] Expressions told apart at card size | **PASS** | Fact: `expr-card-strip.png` is the same as v4. Each face has its own eyes and mouth, and the sprout gives a second cue. v5 did not touch the face sets (`changes.md` L17). |
| I4 [should] Its own design | **PASS** | Opinion: no change since v2. The round head, sprout, blue sweater, tie, lanyard and case are generic parts. They do not add up to a known character. |

**Overall: PASS** (I1, I2, I3 must: pass. I4 should: pass.)

## Did my v4 arm fix land? (`v4/illustrator.md`, fix notes 1 and 3)

- **Arm relaxed: landed.** Fact: in `crops/arm-front-v4-v5.png` the v4 arm is a straight bar held out from the body. The v5 arm hangs close to the torso, and the forearm turns in a little at the elbow. `turn-front.png` and `hero.png` show the same. Opinion: the arm now reads as relaxed. The case looks carried, not held away.
- **Case plumb under the fist: landed.** Fact: in `crops/grip-front-v5.png` and `grip-back-v5.png` the handle legs rise almost vertically from the fist's underside, and the case sits straight below the fist. In v4 the case hung to the right of the hand.
- **Handle loop counter open: landed.** Fact: `crops/grip-hero-v5.png`, `grip-34-v5.png` and `grip-side-v5.png` show a clear triangle of background between the fist, the two legs and the case top. In `grip-front-v5.png` and `grip-back-v5.png` the counter is only a narrow slit, because the loop is seen almost edge-on in those views.
- **3/4 top corner (v4 fix note 2): not changed.** Fact: rows 50-53 of `silhouette-64-34.png` still close with 1 grey px (luma 148-223), as in v4 (`v4/silhouette-64-34.png`, rows 50-53: 139-215). It is not worse. Rows 54-58 are clean.

## Notes (none blocks the gate)

1. **The 3/4 gap is now thin at the top.** Opinion: it holds at 64 px, but it has no margin left. If a later change moves the case or the hip, look at rows 50-53 of `silhouette-64-34.png` again. Lowering the case by about 1 cm would give a clean pixel there.
2. **The front-view loop counter is only a slit.** Opinion: this is correct for a loop seen edge-on, and the hero and 3/4 views carry the read. Do not widen the handle to fix it.
3. **The case face is tilted in the front view.** Fact: in `turn-front.png` the bottom edge of the case slopes down to the right (about x 615-720, y 985-995), because the face is turned 18 degrees off side-on. Opinion: this reads as a case seen in perspective, not as a hang problem. It is acceptable.
