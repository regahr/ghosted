# Customer interview: 5 decisions for Rega

Run: `runs/jobless-roguelike`. Full report: `council-report.md`.

Sources:
- **Your ask:** Slack C0CHA2A1DM1, message ts 1795588687.579819,
  (private Slack thread)
- **Seat files:** local, unpushed. The folder is not a git repo, so there is no commit sha. They are at
  `seats/`.
- **Council rules:** `~/.claude/skills/council/SKILL.md`, also local and not in git.

Each option has a picture, `q1-linkedin.png` to `q5-device.png`.

## Q1. LinkedIn finale (picture: q1-linkedin.png)

- Your ask: "final goal is to be able post on linkedin" (Slack link above).
- Paweł, `seats/pawel-huryn.md` L36: "**Share link** (`linkedin.com/sharing/share-offsite/?url=`)... No LinkedIn
  app, no review, no tokens. Cost: about 1 day."
- Theo, `seats/theo-forge.md` L70: "(c) (a) in M1, then (b) in M3. **Pick: c.**"
- Theo, `seats/theo-forge.md` L65: "A real post needs Rega's direct ask."
- BMGD, `seats/bmgd.md` L50: "Use a parody name (for example "LinkedUp"), not the real brand."
- Not proved: the brief blocked web search, so the LinkedIn limits come from the seats' memory.

Options:
- (a) The share link plus copy text.
- (b) An image card only.
- (c) (a) now, plus a real API post in M3.

**My pick: a.** It meets the goal in about 1 day. Nothing posts to your real profile unless you press Post
in LinkedIn yourself.

## Q2. Sign-in (picture: q2-signin.png)

- Your ask: "authenticated using google".
- Lena, `seats/lena-park.md` L60: "Must play without Google sign-in? (a) Yes, guest mode (b) No, sign-in first.
  **My pick: a.**"
- Lena, `seats/lena-park.md` L32: "Add "Play as guest" with a later account link, so the first run starts in
  less than 10 s."

Options:
- (a) Google first.
- (b) Guest first, then link Google.

**My pick: a.** It is what you asked for, and you are the only player. (b) adds a save merge that we must
build and test.

## Q3. Run length (picture: q3-runlength.png)

- BMGD, `seats/bmgd.md` L23: "One run is one "Season" of 12 in-game weeks, 20-30 min."
- BMGD, `seats/bmgd.md` L32: "Targets: first offer on run 2-3."
- Paweł, `seats/pawel-huryn.md` L76: "**Session length.** (a) 5 min, (b) 15 min, (c) 30 min plus. **Pick: b.**"
- Council rule, `~/.claude/skills/council/SKILL.md` (Report shape, part 7): "In a game council, BMGD always owns
  the loop feel, the player-facing text and the scope."

Options:
- (a) 10-15 min.
- (b) 20-30 min.
- (c) 45+ min.

**My pick: b.** BMGD owns this decision. If you only have short breaks in the day, pick a.

## Q4. Look (picture: q4-look.png)

- Viet, `seats/viet-tran.md` L64: "(a) toy diorama with toon shading... **Pick: a.**"
- Lena, `seats/lena-park.md` L59: "(a) dark neon (Gaming palette)... **My pick: a.**"
- Council rulings, `~/.claude/skills/council/SKILL.md` (Rulings, 2026-11-15): "for gaming, leisure, websites
  and retail, 3DViz Pro Max leads the design."

Options:
- (a) A warm toy diorama.
- (b) Dark neon.
- (c) A grey office that turns bright as you get closer to an offer.

**My pick: a.** Viet leads design for games. Lena still checks the contrast.

## Q5. Device (picture: q5-device.png)

- Theo, `seats/theo-forge.md` L72: "(a) desktop only... **Pick: a.** Phone halves the 3D budget."
- Viet, `seats/viet-tran.md` L63: "(b) desktop first, phone works... **Pick: b.**"
- Lena, `seats/lena-park.md` L57: "(b) Desktop first, mobile landscape later... **My pick: b.**"

Options:
- (a) Desktop only.
- (b) Desktop first, with the phone in the complete version.

**My pick: b.** The phone work comes only at the end.

## Defaults the council set. Say so if you want to change one

- Tone is comic and kind. The jokes target the system, never you.
- The game uses no real job data or CV.
- The hero is a preset toy figure.
- Timers are on, with a "Relaxed" toggle.
- The music is lo-fi keys.
- Sound is on after the Play tap.
- Your save is on the device first, then synced.

These defaults are in `council-report.md`, section 5.
