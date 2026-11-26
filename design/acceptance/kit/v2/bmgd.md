BMGD (Game Designer): Kit v2 acceptance, items B1-B2

- Date: 2026-11-25. Judge: BMGD seat, alone. Gate: `design/acceptance/checklist.md` lines 52-55.
- I opened the PNGs myself. I did not use the builder's self-check as evidence.

## Offer

- `bmad-game-dev-studio/0.7.2/src/workflows/2-design/gds-create-narrative/checklist.md` line 25 ("Tone and atmosphere established") and line 111 ("Tone matches GDD art/audio direction"). I use them as the test for B2: the art's tone has to match the text register in my spec.
- `.../gds-create-narrative/steps/step-04-characters.md`. A character must carry its loop role and its arc. I use it for B1: Kit's look must show "ex-designer, wants a reply".
- No other tool of mine fits a still-art gate. The brief does not block any of my tools.

## Scores

| Item | Result | Evidence |
|---|---|---|
| B1 matches the bible: name, role, tone | **PASS** | `hero.png`: a round-head pawn toy with a blue shirt, red knotted tie, lanyard badge, brown case and a curled sprout. These match the bible "Hero build" row (`design/bible.md` line 25). `expr-card-strip.png` shows the 5 bible expressions in order (line 26). Height is 0.977 m (`build_report.json` notes in `selfcheck.md` line 19), close to the 0.95 m in the bible. |
| B2 comic and kind, nothing mocks the player | **PASS** | `expr-rejected.png`: closed ^ ^ eyes, a wide smile and one sweat drop. This is "rejected but fine". `expr-ghosted.png`: dot eyes, flat mouth, sprout drooped. Kit is deflated but not crying, and no tear, no dark tint, no laughing face. `ingame-world.png`: Kit stands upright and small in a warm, bright block, and nothing points at him. |

**Verdict: PASS on both must items.**

## Claims

- **Fact**: the bible asks for "a hair sprout that carries the mood at game size" (`design/bible.md` line 25).
- **Fact**: the 5 expressions are hopeful, ghosted, rejected but fine, focused, offer joy (`design/bible.md` line 26). `expr-card-strip.png` shows 5 faces in that order.
- **Fact**: my spec sets the register "comic and kind" (`design/seats/bmgd.md` line 65). It also says that each "no" gets "one short, soft beat" (line 63).
- **Opinion**: the "rejected" face is the best piece of the set for tone. It says "this hurts, I am fine" without a joke at Kit's cost.
- **Opinion**: the name "Kit" does not show in any render. That is correct, because the player names the hero (bible line 24). The badge stays blank, so a typed name can go there later.

## Fix notes (not blocking)

1. **Prove the sprout at game size.** `ingame-world.png` and `ingame-world-crop-x3.png` show only the hopeful sprout, about 4 px at 51 px tall. The bible makes the sprout the mood signal at game size (line 25), but no render shows the ghosted droop or the offer-joy stretch at the 26 m camera. Add a 5-pose strip at 51 px. If the droop does not read, make it bigger before the build.
2. **The "wooden" cue is weak (Opinion).** The bible says "a wooden pawn toy" (line 25). The render reads as a soft chibi office worker. There is no grain, no peg base and no lacquer shine. This is Viet's call as look lead, so it is a note, not a FAIL.
3. **Use the badge for lore (Opinion).** The blank badge is a free place for a small "Crunchr" mark, or the player's typed name at card size. A laid-off designer who still wears the old lanyard is comic and kind. It tells the backstory with no text box.
