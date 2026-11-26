# Mira Sol (Composer (Music)): jobless roguelike

Date: 2026-11-25. Skill loaded: `music-composition`. Pulled: `game-audio`.

## Offer

- `~/.claude/skills/music-composition/references/genres/game-music.md` (loop length table L85-96, vertical layering L98-121, stingers L154-162, pitfalls L233-244). It sets my loop lengths and the state system below.
- `~/.claude/skills/music-composition/references/harmony/chromatic-harmony.md` L180-182 (IV-iv-I) and `assets/progressions-catalog.md` L104-117 (Mixolydian, Lydian loops). They give the "tired but uplifted" harmony.
- `~/.claude/skills/game-audio/bgm-patterns.md` L5-14 (background gains, rests) and L16-51 (anti-repetition, 30 s minimum before exact repeat). It sets the M1 browser-synth rules.
- `~/.claude/skills/game-audio/SKILL.md` L159-166 (look-ahead scheduler, AudioContext on first click). It makes M1 music possible with zero audio files.
- The brief blocks no tool of mine.

## 1. Verdict

**Go with changes.** Fact: the brief says the game must "never [be] a second source of pain" (`runs/jobless-roguelike/brief.md` L21-22). Opinion: music is the cheapest way to keep a failed run kind. The music must never punish a ghosting.

## 2. Recommendations (music only)

**Style.** Opinion: warm lo-fi / chillhop keys (Rhodes, soft bass, brushed kit, vinyl air). Major keys only in the hub. The world says "no", the music says "you are fine".

**One theme.** Opinion: write one 4-bar "hope motif" (rising ^1-^2-^3-^5). Every state quotes it. Fact: long games use a recurring theme as the player's anchor (`game-music.md` L244).

**Harmony for a tired player.** Opinion:
- Hub: Lydian or Mixolydian vamps, no strong V-I. Example in F: `Fmaj7 - G/F - Em7 - Am7` (Lydian #4 is bright with no push). Fact: Lydian I-II colour (`progressions-catalog.md` L113).
- Small sadness, never despair: `IV - iv - I` (`Bb - Bbm - F`). Fact: "smiling-through-tears" (`chromatic-harmony.md` L80, L182).
- No minor-key home state. Minor only as a 2-bar colour.

**Music states** (one key family, F major / D minor, so all crossfades are clean):

| State | Tempo | Loop | Form |
|---|---|---|---|
| Hub (home, cafe) | 84 BPM | 3:00 effective | 4 rotating 8-bar phrases, layers phase |
| Job board | 92 BPM | 2:00 | hub harmony + plucked arp layer |
| Interview / mini game | 92-120 BPM | 1:30 per tier | vertical layers on a `tension` 0-1 value |
| Ghosted | none | 4-6 s stinger | music thins to pad, comic "unread" figure, back to hub |
| Rejection with reply | none | 6-8 s | `IV - iv - I`, then hub |
| Offer | none | 10-12 s | motif full, `bVI - bVII - I` lift |
| LinkedIn finale | 100 BPM | 60 s, no loop | full theme, key lift F to G at the post button |

Fact: hub 2:00-6:00, failure 5-15 s stinger, victory 10-60 s (`game-music.md` L87-96).

**Interview layers.** Fact: each layer must work alone and share one harmonic frame (`game-music.md` L113-119). Opinion: tier 0 pad + keys; tier 1 + soft kick at 92; tier 2 + hats and bass; tier 3 + tempo step to 120 at a phrase edge only. Tension falls back in 2 bars on a mistake. It never adds alarm sounds.

**Ghosted is a joke, not a wound.** Opinion: no sad cue. The music drops out for 1 beat, a small "seen" 2-note figure plays, then the hub returns on the next downbeat. Ghosting is the normal result (brief L16), so it repeats many times. A sad stinger heard 50 times becomes real pain.

**Run variety.** Opinion: each new run picks one of 3 hub intros (8 bars). Fact: "start-of-day variations" (`game-music.md` L83).

**Mix.** Fact: Kael Resonance sets the music level (`council/SKILL.md` L131). My ask: music under SFX, lead gain 0.10-0.18 (`bgm-patterns.md` L10).

## 3. Risks

1. **Loop fatigue in the hub.** Rega stays there between runs. Mitigation: 3:00 effective loop, 4 rotating phrases, probabilistic notes; never repeat exactly inside 30 s (`bgm-patterns.md` L51).
2. **Music adds pain on failure.** Mitigation: no minor stinger for ghosting; play-test 20 ghostings in a row; if it hurts, cut the stinger to silence + hub.
3. **Synth music sounds cheap.** Mitigation: M1 uses Web Audio synth (fast). Complete version uses recorded or composed stems with the same form, keys and state map, so code does not change.

## 4. Milestones

- **M1 (first playable):** Web Audio synth. Hub loop, interview with 2 layers, ghosted stinger, offer stinger. One key. Crossfade at bar edge.
- **M2:** all 7 states, 4 interview tiers on `tension`, 3 hub intros, rejection cue, the hope motif in every state.
- **M3:** LinkedIn finale cue with key lift. Per-mini-game colour layer (one instrument each).
- **Complete:** stems (OGG, 48 kHz) replace synth; seamless loop points at a pickup (`game-music.md` L71); quiet mode (pad only) for long sessions.

## 5. Questions for Rega

1. **Music style?** a) lo-fi chillhop keys b) cozy acoustic (guitar, glockenspiel) c) synthwave office d) chiptune. **Pick: a.**
2. **Ghosted moment tone?** a) comic "seen" figure b) bittersweet IV-iv-I c) silence only. **Pick: a.**
3. **Music source for the complete version?** a) browser synth only b) composed stem files c) AI-generated music (rights: Kael decides). **Pick: b**, with a for M1.
4. **While you play, do you use your own playlist?** a) no, game music b) yes, often c) both. **Pick: c**: separate music slider and quiet mode.
5. **LinkedIn finale feel?** a) big win with key lift b) quiet proud moment c) ironic, over the top. **Pick: a.**
