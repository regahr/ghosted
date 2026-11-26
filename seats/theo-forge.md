# Theo Forge (Head of Engineering): jobless roguelike

Skill read (not invoked): `foreman/.claude/skills/master-foreman/SKILL.md`. "MF" = `foreman/.claude/skills/master-foreman/`.

## Offer

- **MF `SKILL.md` L91-103 (modes, gates 2.5 and 6.5).** Build each milestone as one `full-flow` run in `runs/`. Rega clears a gate before any take is recorded.
- **MF `SKILL.md` L63-89 (hard boundary).** The build world is local: `supabase start` plus `next dev`. A deploy to Vercel or hosted Supabase happens only on Rega's ask (L137-140).
- **MF `references/test-cases.md` L7-16.** Count the cases from the sim branches (ghost, interview, offer), then add an empty case and a completed case.
- **MF `references/implementation.md` L55-69.** One real-database test per case means RLS and save tests run on local Supabase. The concurrency audit covers a save from two tabs.
- **MF `references/verify-and-record.md` L9, L22, and `proof-gate.md` L37-46.** Each case gets a Playwright video. The "money shot" of the last case is the LinkedIn confirm screen.
- **Blocked by the brief:** no web search. The LinkedIn, Supabase and Vercel limits below are **not proved**.

## 1. Verdict

**Go with changes.** Keep all game rules in one client-side seeded sim. Use an edge function only for LinkedIn. Ship the share URL first. (Opinion)

## 2. Recommendations

**Architecture (Opinion)**
- `packages/sim`: pure TypeScript, no DOM, no three.js. It takes `(seed, actions[])` and returns the state. The 3D layer only renders the state.
- Seeded RNG (sfc32). Each room gets its own stream from `hash(runSeed, roomIndex)`, so a new mini game does not change older rooms.
- A save is `{seed, actions, snapshot, version}`, written at each room exit. Write it to IndexedDB first, then sync it to Supabase. A crash loses one room at most.
- No anti-cheat. RLS only keeps Rega's rows private.

**Schema (Opinion)**
- `runs(id, user_id, seed bigint, status, floor, outcome, snapshot jsonb, version int, started_at, ended_at)`
- `run_actions(run_id, seq, type, payload jsonb)`, append-only.
- `unlocks(user_id, key, unlocked_at)`
- `share_cards(slug, run_id, title, stats jsonb, is_public)`
- RLS: `user_id = auth.uid()` on every table. Anon may `select` a `share_cards` row when `is_public` is true, because LinkedIn reads OG tags from a public URL.
- The save uses `update ... where version = $n`.

**Auth.** Google through Supabase Auth with `@supabase/ssr`. Playwright logs in as a seeded email user on local Supabase and never drives Google. (Opinion)

**LinkedIn (not proved)**
- `linkedin.com/sharing/share-offsite/?url=<card URL>` needs no app, no scope and no review. It takes only a URL. Rega types the post text.
- The API path is the "Share on LinkedIn" product (`w_member_social`) plus OpenID (`openid profile`). It needs a developer app and a company page. The token lives about 60 days. The secret stays in an edge function.
- Next `ImageResponse` at `/api/og/[slug]` makes the card image.

**3D load budget (Opinion)**
- Initial JS 350 KB gzip or less. Load each mini-game scene with dynamic `import()`.
- First scene: 3 MB of assets or less. Whole game: 40 MB or less. Use glTF with meshopt and KTX2, served from `public/` by the CDN.
- 60 fps target on Rega's laptop, 30 fps floor, 150 draw calls per scene.

**Tests (Opinion)**
- Vitest golden seeds: a fixed seed and action list give one exact event-log hash.
- A balance test runs 10,000 seeded runs. It asserts that the offer rate stays in Rega's band and that every run gives a fun reward.
- RLS tests on local Supabase: user A cannot read user B's rows.
- Playwright: `?seed=` plus a `window.__sim` hook (test builds only). WebGL runs with `--use-angle=swiftshader`.

**Cost (not proved).** Vercel Hobby, Supabase Free and the share URL cost $0. Supabase Pro costs $25/month.

## 3. Risks

1. **Supabase Free pauses after about 7 days with no use (not proved).** *Mitigation:* IndexedDB is the primary save. A pause blocks only sync and the post.
2. **A non-deterministic sim breaks replay and tests.** *Mitigation:* lint bans `Math.random` and `Date` in `packages/sim`. CI runs the golden-seed replay.
3. **The LinkedIn API changes or refuses the app.** *Mitigation:* the share URL is the default. The API is an add-on behind one interface.

## 4. Milestones (each one is a `full-flow` run with gates)

- **M0:** Next.js, local Supabase, Google auth, schema, green RLS tests, one 3D room.
- **M1 first playable:** one floor of 5 rooms, 3 mini games, seeded sim, resume after a tab kill, ghost and offer outcomes, share URL with OG card.
- **M2:** unlocks, 6 mini games, 2 biomes, balance test, size check in CI.
- **M3:** API post with a confirm screen (if Rega picks it). A real post needs Rega's direct ask.
- **Complete:** 10-12 mini games, 3 biomes, audio, a video proof for each P0 case, deploy on Rega's ask.

## 5. Questions for Rega (the chair adds a diagram for each option, per Rega's CLAUDE.md)

1. **LinkedIn method:** (a) share URL only; (b) API one-click post; (c) (a) in M1, then (b) in M3. **Pick: c.**
2. **Real post on your real profile:** (a) yes, after a confirm screen with the full text; (b) never, copy text and image only. **Pick: a.**
3. **Devices:** (a) desktop only; (b) desktop and phone. **Pick: a.** Phone halves the 3D budget.
4. **Save:** (a) cloud only; (b) local first, cloud sync. **Pick: b.**
5. **Free-tier pause:** (a) accept it, local save covers it; (b) pay $25/month for Pro. **Pick: a.**
