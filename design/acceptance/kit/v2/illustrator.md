Illustrator (Illustrator): Kit v2 acceptance, items I1-I4

## Offer

- `~/.claude/skills/illustrator/SKILL.md` § 9.2 "View at thumbnail size (2") — if it doesn't read, comp is too busy": used for I1 and I3. I judged the silhouette at its real 64 px file, not only the x4 preview, and the faces at the 160 px strip.
- `~/.claude/skills/illustrator/references/philosophy.md` line 26 ("Readability is King"): used for I3. A face must read without the sprout and the sweat drop doing all the work.
- `~/.claude/skills/illustrator/references/risks.md` lines 5 and 12 (no copying of existing characters): used for I4.
- `~/.claude/skills/illustrator/SKILL.md` § 10 pitfall 1 (over-detailing): used for I2, to check that the added parts are designed shapes and not noise.
- The SKILL.md reference links (for example `references/7-standards-reference.md`) point to files that do not exist. The real files have short names (`standards.md`, `philosophy.md`, `risks.md`). The brief blocks none of my tools.

I opened every render myself. I did not copy `assets/kit/selfcheck.md`. Where my eyes and selfcheck differ, I say so.

## Scores

| Item | Verdict | Evidence (file: what I see) |
|---|---|---|
| I1 [must] 64 px silhouette: round head, sprout, briefcase | **PASS** | `silhouette-64.png` (47x64, native) and `silhouette-64-x4.png`: a clean round head that is wider than the shoulders, a hooked sprout on top (about 1 px thick at native size), and a case with a handle notch clear of the right leg. All 3 cues read. In `silhouette-64-34.png`, the case merges into the leg line and reads as a lump, not a case. Fact: the item asks for the 64 px silhouette, and the front one passes. |
| I2 [must] hand-made shapes with designed profiles | **PASS** | `turn-front.png`, `turn-34.png`, `hero.png`: the collar has 2 points, the tie has a knot and a pointed blade, the fringe has 4 zigzag locks, the sprout curls, the sleeves end in a cuff lip, the shirt hem has a lip over the trousers, the shoes have a sole and a toe, and the case has a bevel and gold clasps. Weak spots: the hands are mitten blobs (I cannot see the "thumb bump" that selfcheck claims), the back of the head in `turn-back.png` is a plain bowl with a jagged lower edge, and the torso is still a pear capsule. Each part has a designed profile, so this is a pass, but only just. |
| I3 [must] expressions can be told apart at card size | **PASS** | `expr-card-strip.png` (5 faces, 160 px tall): hopeful (oval eyes, smile, cheeks), ghosted (dot eyes, dash mouth, sweat drop, sprout drooped), rejected-but-fine (closed ^ ^ eyes, wide smile, drop), focused (brows angled in, dash mouth), offer-joy (open mouth with tongue, tall sprout). All 5 differ. Risk: focused and ghosted have the same dot eyes and almost the same dash mouth (`expr-focused.png` against `expr-ghosted.png`). Only the brows, the sprout and the drop separate them. |
| I4 [should] own design, copies no known character | **PASS** | `hero.png`: a round-headed office kid with a curled cowlick, a blue shirt, a red tie, a lanyard badge and a case. The single curled hair strand is a common cartoon trope (the "ahoge"), not one owner's mark. I found no one-to-one match with a known character (Opinion). The tie, lanyard and case combination is generic office dress. |

**Overall: PASS.** All must items (I1, I2, I3) pass. The should item (I4) passes.

## Fix notes (do these even though it passes)

1. **Focused face (I3).** Fact: my spec says focused eyes are "ovals scaled y 0.5" (`design/seats/illustrator.md`, section 2 table, Focused row), and selfcheck says "half eyes" (`assets/kit/selfcheck.md` line 30). But `expr-focused.png` shows full round eyes with highlights. Fix: squash the eyes to half height (a lid line on top), so focused no longer shares ghosted's dot eyes.
2. **Grip and hair seams (I2).** `turn-front.png`, `turn-back.png` and `turn-side.png` show brown spikes where the hand closes on the case handle, and `turn-side.png` shows a skin wedge between the fringe and the hair cap at the temple. It looks like a hole in the hair. Fix: hide the handle inside the closed mitten, and close the temple gap with one side lock. Also give the back of the head 2 or 3 nape locks, as selfcheck claims are already there. In `turn-back.png` I see a bowl cut.
3. **Thicken the sprout and push the case out (I1).** At native 64 px the sprout is about 1 px thick and can drop out under downscaling or anti-aliasing. In the 3/4 silhouette the case merges with the leg. Fix: make the sprout about 1.5x thicker at its base, and move the case about 0.05 m out from the leg, so the 3/4 view keeps a gap of background between case and leg.
