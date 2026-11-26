# Council report: jobless roguelike (working title)

- Date: 2026-11-25
- Subject: `runs/jobless-roguelike/brief.md`
- Thread: Slack C0CHA2A1DM1, ts 1795588687.579819 ((private Slack thread))
- Format: game council, 7 game seats plus Theo Forge (the subject includes how it is built). 8 seats. Each seat
  ran alone and saw no other answer. Each claim in `seats/*.md` is marked Fact (with a source) or Opinion.
- Limit: the brief blocked web search. All LinkedIn, Supabase and Vercel limits come from memory and are **not
  proved**. Theo Forge must check them before M1 starts.

## 1. Verdict

**Go with changes. 8 of 8 seats agree.** All 8 seats give the same main change: a rejection is a short
joke that gives the player a reward. It never copies the real pain. "Minimum acceptance rate" is the joke on
the HUD. It is not the real odds.

| Seat | Verdict | Main point |
|---|---|---|
| BMGD | go with changes | One run is a "Season" of 12 in-game weeks (20-30 min) on a node map. A pity counter makes an offer sure after 3 full funnels with no offer. 12 mini games. |
| Paweł Huryn | go with changes | Measure "enjoy": Rega starts 3 or more runs a week on their own, for 2 weeks. One throwaway prototype first. |
| Lena Park | go with changes | Put the HUD in the DOM over the canvas. One shared frame for all mini games. Reduced motion from M1. |
| Viet Tran (design lead, games) | go with changes | Small toy diorama rooms on a fixed camera. No open 3D city. React Three Fiber on a client-only route. |
| Emil Kowalski | go with changes | A rejection lasts 600-900 ms and can be skipped. A success is rare, so it is big. The LinkedIn card is the trophy. |
| Kael Resonance | go with changes | Comic office-toy sound: bad news goes "boing", good news goes "ding". All sound in M1 is made in code. |
| Mira Sol | go with changes | Warm lo-fi in a major key. Ghosting gets a comic stinger. There is no sad home state. |
| Theo Forge | go with changes | One seeded TypeScript sim on the client. One edge function, for LinkedIn only. The share link ships first. |

## 2. Blockers and high risks

1. **The game hurts like real life** (all 8 seats). Mitigation: each rejection is under 1 s, can be skipped,
   gives Copium or Grit, uses a pool of 40+ gags with no repeat inside 10, and the jokes target the system,
   never the player.
2. **Scope** (BMGD, Viet, Theo). 12 mini games, 3D and a meta loop is a large build. Mitigation: one shared
   mini game frame (`start(seed, difficulty) -> result`), one modular 3D kit, and one full-flow run for each
   milestone.
3. **LinkedIn limits not proved** (Paweł, Theo). Mitigation: the share-offsite link plus a copy-text button
   needs no LinkedIn app. The API post is optional, and only in M3.
4. **3D performance in a browser** (Viet, Lena, Emil). Mitigation: 150 draw calls is the hard cap. The first
   room loads in 3 MB or less. The 3D loop pauses under a mini game.
5. **Supabase Free pauses after about 7 days with no use** (Theo, not proved). Mitigation: the game saves on
   the device first, then syncs to Supabase.

## 3. Ranked plan

| # | Action | First step | Number | Seats |
|---|---|---|---|---|
| 1 | Customer interview with Rega | 5 questions in the thread, with diagrams | 5 decisions | Paweł (script), all |
| 2 | M0 throwaway prototype | Grey-box, runs on this machine, no auth | 3 mini games; shows that ghosting is funny | Paweł, BMGD, Emil |
| 3 | M0 skeleton | Next.js + local `supabase start`, Google OAuth, RLS | 4 tables, RLS on each | Theo |
| 4 | M1 first playable | 1 district, 5 rooms, pity counter, finale | 5 mini games; Rega starts 3 runs in week 1 | BMGD, Viet, Theo, Lena |
| 5 | M2 depth | Meta unlocks, balance test in CI | 8 mini games; 40% "one more run" | BMGD, Paweł, Theo |
| 6 | M3 finale and polish | Share card, offer sequence, delete my data | OG card + share-offsite link | Emil, Lena, Theo, Mira |
| 7 | Complete version | 3 districts and a final floor, daily seed | 12 mini games; North Star met 2 weeks in a row | all |

The 12 mini games (BMGD, `seats/bmgd.md`): CV Tetris, Cover Letter Rhythm, ATS Catch, Recruiter Call,
Take-home Debug, Panel Plates, Salary Tug, Ghost Hunt, Coffee Chat Memory, Feed Dodge, Reference Relay,
Onboarding Form. Each lasts 30-60 s.

**Offered by seats** (all used in this report, unless a reason is given):
- BMGD: `gds-gdd` roguelike and party-game types, the genre-complexity CSV, the GDD checklist, `gds-create-narrative`
  and `gds-playtest-plan`. The two workflows run in the build, not here.
- Paweł: `interview-script` (Mom Test), `metrics-dashboard`, `test-scenarios` and `prioritization-frameworks`.
  `privacy-policy` waits for M3. `pre-mortem` is not run yet; it is recommended before M2.
- Lena: `ui-ux-pro-max` design-system search, the palette and font CSVs, and the pre-delivery checklist.
  `MASTER.md` is not saved, because a council changes no files.
- Viet: the toy-miniature and tilt-shift style profiles, `kit-core.js`, `kit-lod.js`, `village-layout.js`, the
  orbit camera and `capture.py`. `capture.py` and `host-probe.py` wait for M1, because no build exists yet.
- Emil: the `emil-design-eng` frequency table, `choreograph`, `gestures`, `improve-animations/AUDIT.md` and
  `break-ui/CATALOG.md`.
- Kael: the `game-audio-director` references (with its remote tools left out, rule 3), `game-audio` sfx-engine,
  mixing guide and mute button, and `build-game-audio-feedback`.
- Mira: the `music-composition` game-music reference, the chromatic-harmony reference and progression catalog,
  and `game-audio` bgm-patterns.
- Theo: the master-foreman modes and gates 2.5 and 6.5, `test-cases.md`, `implementation.md` and the proof gate.

## 4. Disagreements and the chair's view

| Topic | Seats | Chair's view |
|---|---|---|
| Look | Viet: warm toy diorama. Lena: dark neon (Gaming palette). | Viet leads design for games (council rulings, 2026-11-15). Lena keeps the contrast veto. **Question 4 for Rega.** |
| Device | Theo: desktop only. Viet, Lena, Emil: desktop first, phone later. | Desktop first. The phone comes in the complete version, with a low preset. **Question 5.** |
| Run length | BMGD: 20-30 min. Paweł: 15 min. | BMGD owns the scope and the loop feel. **Question 3.** |
| Sign-in | Lena: guest mode. Rega's ask: "authenticated using google". | Rega's words come first. **Question 2.** |
| LinkedIn | All seats: share link plus copy text first. Theo: API post in M3, after a confirm screen. | Share link in M1 to M3. The API post goes in only if Rega asks for it. **Question 1.** |
| Mini games in M1 | Viet 1, Lena 2, Theo 3, BMGD 5, Paweł 5. | M0 prototype: 3. M1: 5 (BMGD owns the scope). |
| Tone | BMGD: dark but kind. Paweł: recruiter satire. Emil: mostly slapstick. Kael, Mira: comic. | Default: comic and kind, and the jokes target the system. Rega can change it. Not asked, so the interview stays at 5 questions. |
| Real data | Paweł: none. Emil: an optional box for your own rejection lines. | Default: no real data. The optional box comes in M2, and the text stays on the device. |

## 5. Defaults the council set (Rega can change any of them)

- Hero: a preset toy figure that you dress up (Viet). Movement: click-to-move on a fixed camera (Viet).
- Mini game view: 2D overlays, with 3D for 3-5 key games (Viet).
- Timers: on, with a "Relaxed" toggle that gives 1.5x time (Lena).
- Music: lo-fi keys. Your own playlist can play while the game music is quiet (Mira).
- Sound: on after the Play tap. Voices are made-up words (gibberish) from a synth (Kael).
- Save: on the device first, then synced to Supabase. Accept the Free-tier pause (Theo).
- Finale brand: a parody name (for example "LinkedUp") inside the game, because LinkedIn is a trademark (BMGD).

## 6. Decisions for Rega

They are in `interview/context.md`, with one diagram for each option:
1. LinkedIn finale
2. Sign-in
3. Run length and first win
4. Look
5. Device

## 7. Build owners

Product type: game. So Viet Tran is the design lead.

| Seat | Skill to invoke | Decisions it owns | Phases |
|---|---|---|---|
| BMGD | `bmad-game-dev-studio:gds-gdd`, `bmad-game-dev-studio:gds-create-narrative`, `bmad-game-dev-studio:gds-playtest-plan` | Core loop, loop feel, run tuning (pity counter, win rate), the mini game list and their rules, player-facing text, scope | Spec, each milestone review, playtest |
| Paweł Huryn | `pm-product-discovery:interview-script`, `pm-product-discovery:metrics-dashboard`, `pm-execution:test-scenarios` | What to build, priority, the prototype decision, how the "done when" of each milestone is measured (North Star, "one more run" rate) | Interview, spec, gate 2.5, milestone sign-off |
| Lena Park | `ui-ux-pro-max:ui-ux-pro-max` | Accessibility, HUD and menu layout, the mini game frame, sign-in and composer screens, palette and type, CLS, the pre-delivery checklist | Spec, each UI build, gate 6.5 checklist |
| Viet Tran | `3dviz-pro-max:3dviz-pro-max` | Design lead: 3D world, look, camera, the 3D asset budget, room generation, motion that carries 3D content. Models each asset only from an accepted sketch | Spec, each 3D build, capture proof |
| Illustrator (added 2026-11-25, Rega's sketch-first ruling, ts 1795604691.829739) | `illustrator` | The 2D draft sketch of every character, NPC, prop and district, before any 3D. Checks that the 3D matches the sketch | Each art asset, sketch gate and 3D gate |
| Emil Kowalski | `emil-design-eng` | UI motion, the rejection and success sequences, press feedback, gesture physics, the 3D to 2D handoff timing | Each UI build, animation audit |
| Kael Resonance | `game-audio-director` (judgement only), `build-game-audio-feedback` | SFX, feedback cues, the mix and loudness, audio unlock and mute, rights of each audio asset | Each milestone with audio |
| Mira Sol | `music-composition`, `game-audio` | Background music, music states, loops. Kael sets the mix level | M1 synth, M2 states, M3 finale |
| Theo Forge | `master-foreman` (reads the file, does not invoke it) | Architecture, Supabase schema and RLS, edge functions, LinkedIn integration, tests (seeded replay, Playwright), gates 2.5 and 6.5, build cost | Each milestone as one `full-flow` run |
