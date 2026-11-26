Kael Resonance (Audio Director (SFX)):

# Seat answer: jobless roguelike, audio (SFX, cues, mix)

Paths: `GAD` = `~/.claude/skills/game-audio-director`, `GA` = `~/.claude/skills/game-audio`, `BGAF` = `~/.claude/skills/build-game-audio-feedback`.

## Offer

- `GAD/references/middleware-and-platforms.md` L43-60, L83-105: unlock, formats, budgets, loudness. Sets my numbers.
- `GAD/references/adaptive-audio-patterns.md` L102-152 (unlock sketch), L158-165 (pause, tab hidden, death). Base of the audio manager.
- `GAD/references/generative-audio-and-voice-rights.md` L15-30: which tools can ship.
- `GA/sfx-engine.md`, `GA/mixing-guide.md` L7-16, `GA/mute-button.md` L3-15: procedural SFX, gain table, mute. M1 needs zero audio files.
- `BGAF/SKILL.md` L12, L16, L20: cue map and verify list.
- Blocked by the brief: the ElevenLabs MCP, WebSearch and WebFetch in `GAD` (rule 3 of the council). Not used. Local `ffmpeg` loudness checks stay allowed (`GAD` middleware L107).

## 1. Verdict

**Go with changes.** Opinion: rejection is the most common event, so its sound decides if the game is cathartic or painful. It must sound comic, never cold.

## 2. Recommendations (complete version)

**Sonic thesis.** Opinion: "a cheerful office-toy world: mechanical stamps, rubber, paper, desk bells. Bad news goes 'boing', good news goes 'ding'."

**Core SFX list** (Opinion, design; layer method is Fact, `GAD/SKILL.md` L83):
| Cue | Sound | Variants |
|---|---|---|
| `apply_send` | paper whoosh + mail slot clack | 4 |
| `rejection` | rubber stamp thud + cartoon "boing" down, then a soft coin tick (the player gets "Grit" points) | 6, pitch +/-80 cents |
| `ghosting` | a phone ring that fades out, then a cricket chirp and wind. Max 1.5 s of near-silence. | 4 |
| `ghost_streak_5` | a comic choir "ohhh" stinger | 2 |
| `interview_invite` | rising 3-note chime + paper rustle | 2 |
| `offer` | big stinger: desk bell, confetti burst, crowd cheer, music ducked 8 dB for 2 s | 1 + 2 sweeteners |
| `linkedin_post` | a "publish" click, then like-pop counters that speed up (a reward cascade) | pool of 8 pops |

**Rules.**
- Fact (`GAD/SKILL.md` L85, L103): every cue that plays more than a few times a minute gets a round-robin pool and pitch/volume randomization. Rejection and ghosting play the most, so they get the most variants.
- Fact (`GAD/SKILL.md` L124): error sounds stay gentle. Opinion: no buzzers, no minor-key falls, no sigh voices on rejection.
- Opinion: ghosting is the one designed silence (Fact rule: `GAD/SKILL.md` L98). Keep it short. Long silence feels real.

**Mini-game feedback cues.** Fact (`BGAF/SKILL.md` L12): give every mini game the same cue grammar: input OK, hit, miss, combo, warning, timer low, win, lose. Opinion: one shared set, re-pitched per mini game. Lose cue max 0.6 s. Win cue 1.0-1.5 s. Timer-low ticks speed up from 2/s to 4/s in the last 5 s.

**Web Audio unlock and mute.** Fact (`GAD/references/middleware-and-platforms.md` L45-52): resume the `AudioContext` on `pointerup`, `click`, `keydown` or `touchend`. Touch `pointerdown` does not count. Test `state !== 'running'` for iOS. Opinion: the first sound plays on the Google sign-in "Play" tap. Fact (`GAD/references/adaptive-audio-patterns.md` L115-117): suspend on tab hidden, resume on return. Mute button on every screen, saved in localStorage (Fact, `GA/mute-button.md` L9). Fact (`GAD/SKILL.md` L130): separate sliders for master, music, SFX, UI. Fact (`GAD/SKILL.md` L128): each critical cue has a visual twin (the stamp, the fading phone icon).

**Mix and loudness.** Fact (`GAD/SKILL.md` L99): feedback over music over ambience. Fact (`GA/mixing-guide.md` L14-16): SFX gain 0.2-0.3, UI 0.15-0.25. Opinion: target -16 LUFS integrated on the full mix, true peak max -1 dBTP (Fact basis: `GAD/references/middleware-and-platforms.md` L101-103). Max 32 voices (Fact range 24-48, same file L87). Never steal the offer stinger.

**Sources and rights.** Fact (`GA/SKILL.md` L42): procedural Web Audio needs no files and no license. Opinion: M1 is 100% procedural. Later: home foley (stamps, paper, phones) and CC0 packs, each logged in `ai-asset-log.md` (Fact rule, `GAD/SKILL.md` L106). Fact (`GAD/SKILL.md` L167): no Suno or Udio. Opinion: no remote generation service. If Rega wants AI SFX, Stable Audio 3 Small SFX runs local (Fact, `GAD/references/generative-audio-and-voice-rights.md` L30). No synthetic voice.

**Formats.** Fact (same file L57): Opus mono 48 kHz, MP3 fallback. Opinion: max 3 MB of SFX at first load.

## 3. Risks

1. **Rejection sound feels like real pain.** Mitigation: comic register, Grit tick, Rega playtests it first.
2. **Repetition fatigue** (hundreds of rejections per run). Mitigation: 6+ variants, pitch spread, and a 20% chance of a rare "gag" variant.
3. **No sound on iPhone or after tab return.** Mitigation: unlock on the Play tap; test a real iPhone and Firefox (Fact, `BGAF/SKILL.md` L20).

## 4. Milestones

- **M1 (first playable):** audio manager (unlock, mute, tab suspend), procedural cues: apply, rejection, ghosting, offer, 8 shared mini-game cues. Zero files.
- **M2:** variation pools, the event-to-caption table, separate sliders, visual twins, loudness check with `ffmpeg loudnorm`.
- **M3:** in-house foley pass, stingers quantized to Mira Sol's beat, 3D point sources in the office world (Viet Tran's scenes).
- **Complete:** SFX bible, `ai-asset-log.md` at 100%, cue skins per mini game, real-device test pass.

## 5. Questions for Rega

1. **How should rejection sound?** a) comic "boing" b) dry office stamp c) Rega chooses in settings. **Pick: a**, with c as a setting.
2. **Ghosting silence length?** a) 0.5 s b) 1.5 s c) 3 s. **Pick: b.**
3. **Sound on at first launch?** a) on after the Play tap b) off until Rega turns it on. **Pick: a.**
4. **Asset source?** a) procedural only b) procedural + home foley + CC0 c) also local AI SFX (Stable Audio 3 Small SFX). **Pick: b.**
5. **Voice in the game?** a) none, text only b) gibberish "Animal Crossing" voice from synth c) recorded human voice. **Pick: b** (procedural, no rights risk).
