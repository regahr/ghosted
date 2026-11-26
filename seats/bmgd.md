# BMGD (Game Designer): jobless roguelike

Skill loaded: `bmad-game-dev-studio:gds-agent-game-designer` (Samus Shepard). Root: `~/.claude/plugins/cache/bmad-game-dev-studio/bmad-game-dev-studio/0.7.2/src/`.

## Offer

- `workflows/2-design/gds-gdd/assets/game-types/roguelike.md` (lines 3-69). The roguelike sections: run structure, permadeath, what carries over, difficulty modifiers. I use it as the frame for section 2. **Fact**.
- `workflows/2-design/gds-gdd/assets/game-types/party-game.md` (line 11): mini games are "15-60 seconds typical". I set each mini game to 30-60 s. **Fact**.
- `workflows/2-design/gds-gdd/assets/genre-complexity.csv` (line 4): roguelike is "high" complexity. The risks are "Meta vs in-run progression; Balance bands across runs". These are my top tuning risks. **Fact**.
- `workflows/2-design/gds-gdd/assets/gdd-validation-checklist.md` (lines 11-12): pillars, then loop, then mechanics, and win/loss that you can test. Use it to check the GDD after this council. **Fact**.
- `workflows/2-design/gds-create-narrative/` (step-06-dialogue.md): use it to write the text register guide in M1.
- `workflows/gametest/gds-playtest-plan/`: use it for Rega's playtest of each milestone ("Rega enjoys it" becomes a test you can measure).
- The brief blocks none of my tools.

## 1. Verdict

**Go with changes.** The idea is strong. But "minimum rate of acceptance" must be the joke, not the real odds. Every rejection must pay the player. Rega is tired of real rejection (brief.md line 21-22). **Opinion**.

## 2. Recommendations

**Pillars (Opinion):** (1) The system is absurd. You are competent. (2) Every "no" gives you something. (3) Short, sharp mini games. (4) The win feels earned and loud.

**Core loop (Opinion).** One run is one "Season" of 12 in-game weeks, 20-30 min. Each week: pick 1 node on a district map (like the Slay the Spire node map, **Fact**: Slay the Spire, MegaCrit 2019). A node is an application step, an event, a cafe (heal), or a networking meetup. Play the mini game. Get a result and a reward. The funnel for one job: CV, cover letter, ATS, recruiter call, take-home, panel, negotiation, offer.

**Resources in a run (Opinion):** Morale (HP, 100), Savings (the timer, 12 weeks), Network (contacts), Insight (currency from each rejection and ghost).

**Acceptance tuning (Opinion):**
- Show a big "Acceptance rate: 2%" on the HUD. It is the joke stat.
- The real odds: each funnel step passes on mini game score (60%+ pass for an average player).
- A pity counter: after 3 full funnels with no offer, the next offer is sure.
- Ghosting: 50% of applications ghost at the start, 25% after meta upgrades. Each ghost drops 1 Ghost token and 5 Insight.
- Targets: first offer on run 2-3. Run win rate 30% at start, 70% with full meta. (Hades lets death move the story forward. **Fact**: Hades, Supergiant 2020.)

**What carries over (Opinion):** Insight buys permanent Skills (for example "Keyword Sense": ATS window +2 s). Kept: Skills, Network contacts (a referral skips ATS), the Ghost collection (a pet gallery of the recruiters who ghosted you), mini game variants. Lost: Morale, Savings, open applications.

**Mini games, 12 (30-60 s each, Opinion):**
1. **CV Tetris** (CV): fit skill blocks on one page. A line that goes off the page costs points.
2. **Cover Letter Rhythm** (cover letter): type the buzzwords on the beat. Bonus for the company name spelled right.
3. **ATS Catch** (ATS filter): catch the job ad keywords that fall. Do not catch the red flags.
4. **Recruiter Call** (recruiter call): timed dialogue choices. Dodge "expected salary?" with style.
5. **Take-home Debug** (take-home test): squash bugs in a 60 s pipe puzzle. A scope creep timer adds tasks.
6. **Panel Plates** (panel interview): keep 4 interviewer interest bars up at the same time.
7. **Salary Tug** (salary negotiation): a slider with tells. Push up. Stop before the walk-away line.
8. **Ghost Hunt** (ghosting): use a flashlight in your inbox. Catch the ghost. Get closure (Ghost token).
9. **Coffee Chat Memory** (networking): match names and faces. Success adds a contact.
10. **Feed Dodge** (LinkedIn feed): dodge humblebrag posts. Collect real leads. Protects Morale.
11. **Reference Relay** (reference check): call 3 old managers in order before they forget you.
12. **Onboarding Form** (offer): fill a 10-field form while HR changes the start date. Light, a victory lap.

**Finale (Opinion).** The offer opens the "I'm thrilled to announce" composer. The player picks phrases. A reaction counter goes up. The post shows true run stats: "after 47 applications and 31 ghosts". Use a parody name (for example "LinkedUp"), not the real brand. LinkedIn is a trademark. **Fact** (well known). A real share is a question for Rega (Q1).

**Text register (Opinion).** Jokes go at the system, never at the player. Do: "They chose a candidate with 10 years in a 3-year-old framework." Do not: "You failed." A run that ends is "You go home and sleep. The city will still be here." Never use "loser", "unemployable" or "lazy". Each rejection line ends with what the player gets.

**Scope (Opinion).** The 3D part is the district map you walk on (low-poly, small). The mini games are 2D overlays on one shared template. This keeps 12 mini games possible.

## 3. Risks

1. **The game hurts like real life.** Mitigation: pity counter, Insight on every "no", Rega playtest each milestone with a "did this feel bad?" check.
2. **Scope (12 mini games + 3D + meta).** Mitigation: one mini game template (timer, score, 3 tiers). The 3D is only the map.
3. **Repetition across runs.** Mitigation: each job ad adds modifiers (for example "rockstar ninja": ATS words move faster). 3 difficulty tiers per mini game.

## 4. Milestones

- **M1 (first playable):** 1 district, 5 mini games (CV, ATS, Recruiter Call, Panel, Ghost Hunt), Morale and Savings, pity counter, in-game post finale. No meta.
- **M2:** Insight and Skills, Network, Ghost collection, plus Cover Letter, Take-home, Salary Tug.
- **M3:** 3 districts, events, the remaining 4 mini games, job ad modifiers.
- **Complete:** 12 mini games, 3 districts plus a final "dream company" floor, daily seed, achievements, full text pass.

## 5. Questions for Rega

1. **Finale share:** (a) in-game post only, (b) in-game plus copy text, (c) real LinkedIn share. Pick: **b**.
2. **First win:** (a) run 1, (b) run 2-3, (c) run 5-8. Pick: **b**.
3. **Run length:** (a) 10 min, (b) 20-30 min, (c) 45+ min. Pick: **b**.
4. **Tone:** (a) light satire, (b) dark but kind, (c) raw venting. Pick: **b**.
5. **Input:** (a) mouse only, (b) keyboard and mouse, (c) also phone touch. Pick: **b**, touch later.
