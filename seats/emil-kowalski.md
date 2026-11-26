# Emil Kowalski (Principal Designer): jobless roguelike, how it feels

Seat skill loaded: `~/.claude/skills/emil-design-eng/SKILL.md`. Area: UI motion, juice on rejection and success, menu and mini-game control detail, 3D-to-2D transitions, polish bar.

## Offer

| Tool (path) | How it changes the answer |
|---|---|
| `~/.claude/skills/emil-design-eng/SKILL.md` frequency table (L72-75) | Sorts every screen by how often Rega sees it. Rejection is seen most, so it must be the shortest and funniest beat, never a long animation. |
| `~/.claude/skills/choreograph/SKILL.md` | Plans the 3D-to-2D handoff and the "offer letter" finale as one motion, not a queue. |
| `~/.claude/skills/gestures/SKILL.md` | Rules for drag and swipe mini games (swipe the CV, drag the stamp): 1:1 tracking, release by spring with velocity. |
| `~/.claude/skills/find-animation-opportunities/SKILL.md` | Gate per screen in M2: what earns motion, with a required "rejected candidates" list. |
| `~/.claude/skills/improve-animations/AUDIT.md` | Audit before each milestone ships. |
| `~/.claude/skills/break-ui/CATALOG.md` | Worst cases for the LinkedIn post card: long names, long job titles, empty states. |

Brief blocks none of my tools.

## 1. Verdict

**Go with changes.** Opinion: the idea is strong only if rejection is a gag with a fast payoff. If rejection feels like a real email, the game repeats Rega's pain.

## 2. Recommendations

**Rejection juice (seen most, so keep it short).**
- **Fact:** frequent actions get little or no animation (`emil-design-eng/SKILL.md` L72-75). **Opinion:** a rejection plays in 600-900ms in total. Rega can skip it at once with any key or tap.
- **Opinion:** the rejection is slapstick, not a notification. Example: the CV folds into a paper plane and flies out of a window. Or a tiny "GHOSTED" ghost floats up and waves. Use a spring with bounce 0.3 here (**Fact:** bounce 0.1-0.3 is for playful use, L193).
- **Opinion:** never use a red error colour, a shake, or "Unfortunately...". Each rejection gives a reward: one "Copium" point and a random absurd reason ("They wanted 12 years of experience in a 2-year-old framework").
- **Opinion:** keep 40+ rejection gags in a pool. Do not repeat a gag inside 10 rejections. A repeated joke stops being funny.

**Success juice (rare, so it can be big).**
- **Fact:** rare moments may add delight (L75). **Opinion:** an interview pass gets 1.2-1.8s of confetti and a stamp. The final offer gets a 3-4s sequence: an envelope opens, the letter rises, then the LinkedIn post card builds line by line with a 40-70ms stagger (**Fact:** stagger 30-80ms, non-uniform, L645).
- **Opinion:** the LinkedIn post card is the trophy. Polish it most.

**Menus and controls.**
- **Fact:** every pressable element scales to 0.97 on press, at 100-160ms (L129, L203). **Fact:** keyboard actions in menus get no animation (L77).
- **Fact:** UI uses ease-out `cubic-bezier(0.23, 1, 0.32, 1)` (L112), never ease-in. Menus: 150-250ms.
- **Fact:** a drag mini game tracks the pointer 1:1, then releases with a spring seeded by velocity; a fast flick passes at velocity > 0.11 (`gestures/SKILL.md` L23, L36; `emil-design-eng/SKILL.md` L451).
- **Opinion:** each mini game gives an input response in under 50ms: a squash, a tick, a light. Kael fits sound to the same frame (**Fact:** `council/SKILL.md` L132).
- **Opinion:** "Retry" is the default focused button on a fail screen. Restart in under 1s.

**3D world to 2D mini game.**
- **Fact:** motion that carries 3D content belongs to Viet Tran (`council/SKILL.md` L129). I own the 2D side.
- **Opinion:** the camera pushes into a monitor or a door (Viet). At about 70% of the push, the 2D panel scales in from 0.96 and opacity 0, with a 2px blur that clears, 300ms (**Fact:** blur masks crossfades, `emil-design-eng/SKILL.md` L292). Exit is faster: 200ms (**Fact:** exit faster than enter, L683).
- **Opinion:** pause the 3D render loop under a full mini game to keep 60fps.

**Polish bar.** **Fact:** animate only `transform` and `opacity` (L481). **Fact:** support `prefers-reduced-motion` with fades, not zero motion (L531). **Opinion:** "I enjoy it" test: Rega plays 10 runs and laughs at least once per run, and never skips the success sequence.

## 3. Risks

1. **Rejection fatigue.** The gag becomes a chore. Mitigation: 600-900ms cap, instant skip, gag pool with no repeats, Copium reward.
2. **Janky handoff 3D to 2D.** Frame drops break the feel. Mitigation: pause 3D under overlays; CSS or WAAPI for 2D motion; check with the audit in `improve-animations/AUDIT.md` at real speed and in slow motion.
3. **Over-juice.** Everything bounces, so nothing feels special. Mitigation: run the gate in `find-animation-opportunities/SKILL.md` per screen; big motion only for rare beats.

## 4. Milestones

- **M1 (first playable):** motion tokens (easings, durations), press feedback, 1 rejection gag with skip, 1 drag mini game with correct gesture physics, plain 3D-to-2D fade.
- **M2:** 20 rejection gags, blur handoff with Viet's camera push, interview-pass juice, reduced-motion path, first audit.
- **M3:** offer letter sequence and LinkedIn post card, break-ui pass on the card, 40+ gags.
- **Complete:** all mini games pass the audit, 60fps on Rega's laptop, a slow-motion review the next day of each beat.

## 5. Questions for Rega

1. **Rejection tone?** (a) Slapstick (paper plane, ghost) (b) Dry office satire (c) Absurd surreal (d) Mix. **Pick: (d), mostly slapstick.**
2. **Should real rejection lines from your job hunt go in as gags?** (a) Yes, it is cathartic (b) No, keep it fiction (c) Optional custom input. **Pick: (c).**
3. **Skip rejection animations?** (a) Always skippable (b) A setting to turn them off (c) Never skip. **Pick: (a).**
4. **LinkedIn finale?** (a) A fake in-game feed (b) Real share to LinkedIn (c) A downloadable image card. **Pick: (c), (b) later if you want it.**
5. **Main device?** (a) Laptop with keyboard and mouse (b) Phone with touch (c) Both. **Pick: (a) first, (c) for the complete version.**
