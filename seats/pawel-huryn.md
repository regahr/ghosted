Paweł Huryn (Principal Product Manager):

# Seat answer: jobless roguelike

Date: 2026-11-25. Subject: `runs/jobless-roguelike/brief.md`. Skill loaded first: `pm-execution:test-scenarios`.

## Offer (my own tools)

- `~/phuryn-pm-skills/pm-execution/skills/test-scenarios/SKILL.md`: I use its shape (happy path, edge, error, security) to write each milestone "done when" as a test Rega or Playwright can run. The "done when" rows in section 4 use it.
- `~/phuryn-pm-skills/pm-product-discovery/skills/interview-script/SKILL.md` (Mom Test, past behaviour, lines 69-75): it sets the customer interview in section 6. It changes the questions: ask about real past job-hunt moments, not "would you like X".
- `~/phuryn-pm-skills/pm-product-discovery/skills/metrics-dashboard/SKILL.md` (North Star, input, health; lines 18-20, 30-38): it sets the "enjoy" metrics in section 2.
- `~/phuryn-pm-skills/pm-execution/skills/prioritization-frameworks/SKILL.md` (line 12, "prioritize problems, not features"): it sets the priority order.
- `~/phuryn-pm-skills/pm-toolkit/skills/privacy-policy/SKILL.md`: use it in M3 to write a short privacy note for Google sign-in.
- `pm-execution:pre-mortem`: I recommend it before M2. I did not run it.
- The brief blocks web search (brief.md line 27-28). So my LinkedIn API facts come from my knowledge, not a fresh check. Theo Forge must check them before M3.

## 1. Verdict

**Go with changes.** The problem is real and the user is one person, so the product can fit him well (Opinion). Change: make the game a release of pain, not a copy of it. Ghosting must be funny and give loot, never a dead end (Opinion).

## 2. Recommendations

**Problem statement.** Fact (brief.md line 6, 21-22): Rega is "so exhausted of applying and getting ghosted". The job: "When I feel drained by the job hunt, I want a short run where rejection is absurd and I still win something, so I end the session lighter." (Opinion, JTBD form.)

**What "enjoy" means, and how we measure it.** Only one user, so no statistics. Use a self-report plus behaviour (Opinion, from metrics-dashboard lines 20-22: use a rate, need qualitative and quantitative).
- North Star: **voluntary runs per week** that Rega starts without a prompt. Target: 3 or more in a week, for 2 weeks in a row.
- Input 1: **mood delta**. One tap after each run: "How do you feel now vs before?" (-2 to +2). Target: median +1 or more. Guardrail: no run with -2 twice in a row.
- Input 2: **"one more run" rate**: share of runs where the next run starts within 2 minutes. Target: 40% or more.
- Input 3: **mini game skip rate**. Any mini game skipped in more than 50% of meets gets cut or fixed.
- Health: load to first input under 5 s on Rega's laptop; zero crashes per 10 runs.
- Store events in one Supabase table `run_events` (run_id, type, value, ts). No third-party analytics (workspace CLAUDE.md: nothing leaves the machine without a direct ask).

**Priority** (problems first, prioritization-frameworks line 12): (1) catharsis loop, (2) run variety via mini games, (3) the win and the LinkedIn post, (4) 3D polish, (5) meta progress.

**LinkedIn post feature.** Two options:
- A. **Share link** (`linkedin.com/sharing/share-offsite/?url=`). Fact (my knowledge of LinkedIn share docs, not checked today): it takes only a URL; LinkedIn reads the page Open Graph title and image; the user writes the text. No LinkedIn app, no review, no tokens. Cost: about 1 day.
- B. **Real API post** (OAuth with `w_member_social`, UGC/Posts API). Fact (same source): the user signs in to LinkedIn a second time, tokens expire (about 60 days), and the wider post APIs need LinkedIn product approval. Risk: the game posts on Rega's real profile. One bug is a public post to his recruiters.
- My pick: **A**, with a generated "I got the job" card image (OG image from a Vercel route) and a copy button for the post text. Opinion.

**Google sign-in privacy.** Ask for `openid email profile` only. Fact (Supabase Auth docs, my knowledge): Supabase stores email, name and avatar in `auth.users`. Keep game data apart from identity; set Row Level Security on every table (Opinion). Never ask for Gmail, Drive or Calendar scopes. Never take real job data or a CV into the game. Add a "delete my data" button in M3.

**Prototype or not** (my decision right, council SKILL.md line 134): **Yes, one throwaway prototype**, 2D or grey-box 3D, 3 mini games, no auth, local only. Goal: prove that ghosting can feel funny. One version only. Then build the real game.

## 3. Risks

1. **The game hurts.** Low acceptance plus real fatigue can feel like work. Mitigation: every rejection gives a reward (coins, a "ghost" card), and the mood delta guardrail stops a build that scores -2.
2. **Scope.** "Complete version" plus 3D plus "lots of mini games" is large for one builder. Mitigation: cap M1 at 3 mini games, complete at 12.
3. **LinkedIn public post.** Mitigation: share link only; the player always edits and sends the post.

## 4. Milestones and "done when" (measured by me; built and proved by Theo Forge)

| Milestone | Scope | Done when (measure) |
|---|---|---|
| M0 Prototype | 1 room, 3 mini games, ghost reward | Rega plays 3 runs; mood delta median +1 or more |
| M1 First playable | Google sign-in, 3D hub, 5 mini games, run ends at offer or burnout | Playwright: sign in, finish 1 run, event rows saved. Rega: 3 voluntary runs in week 1 |
| M2 Loop depth | 8 mini games, perks, meta coins | One-more-run rate 40%+; no mini game above 50% skip |
| M3 Win and share | "I got the job" ending, share card, delete data | Share link opens LinkedIn with the card; OG image check passes; delete removes all rows |
| Complete | 12 mini games, 3 biomes, sound, music | North Star 3+ runs a week for 2 weeks |

## 5. Questions for Rega

See section 6 (interview script). Max 5, each with options and my pick.

## 6. Customer interview script (Rega, 20 min)

Opening: "This is about your job hunt, not about the game. No right answers."

Warm-up (past behaviour):
- "Tell me about the last application that ghosted you. What happened, step by step?"
- "What did you do right after? What helped?"
- "What made you laugh during this search, if anything?"

Decision questions:
1. **Win rate.** How often does a run end in a job offer? (a) 1 in 10 runs, (b) 1 in 4, (c) never until a meta goal is met. **Pick: b.**
2. **Tone.** (a) Satire of recruiters, (b) Cozy and kind, (c) Dark humour. **Pick: a.**
3. **Session length.** (a) 5 min, (b) 15 min, (c) 30 min plus. **Pick: b.**
4. **LinkedIn.** (a) Share link, you write the post, (b) The game posts for you through the API, (c) Image download only. **Pick: a.**
5. **Real data.** (a) No real data, (b) Type your real job title for flavour, (c) Import CV. **Pick: a.**

Wrap-up: "What did I not ask that matters to you?"
