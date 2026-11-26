# Ready check: Recruiter Ricky body map + sketch (Illustrator, 2026-11-25)

Rule: `~/.claude/skills/council/SKILL.md` "Ready check before any drawing", "Whole-picture check", "Game art
pipeline" 0, 1a, 1b, 1. Brief: `design/acceptance/ricky/sketch-brief.md`. Paths are relative to
`runs/jobless-roguelike/design/`.

| # | Need | State | Source |
|---|---|---|---|
| 1 | Goal: body map, then a 2D sketch sheet for Viet's 3D build. Rega is the gate; the chair checks at 2x | decided | `sketch-brief.md` header; council `SKILL.md` "Rega is the gate" |
| 2 | Role and tone: runs the Recruiter Call; "Super excited to connect!", then forgets; cheerful and busy, not evil | decided | `seats/bmgd.md` L41; `sketch-brief.md` "Tone" |
| 3 | Size: Kit 0.95 m (built 0.977 m, 2.71 heads); Ricky 1.05 x Kit = 1.00 m; same toy-pawn family | decided | `assets/kit/LOCKED.md`; `assets/kit/build_report.json` L140-141; `seats/viet-tran.md` L63 |
| 4 | Game camera: 26 m, pitch 42, yaw 20, fov 26, 1600x900, 1.6 px outline -> 75 px per metre at the target | decided | `assets/kit/ingame.html` L146, L156-157 (900 / (2 x 26 x tan 13 deg) = 74.97) |
| 5 | Budget: 1,400 triangles or fewer | decided | `acceptance/checklist.md` L52 (V5) |
| 6 | Palette: suit row 17, skin row 15, ink row 22; shade = neutral grey multiplier; only existing rows | decided | `sketch-brief.md` "Look", "Skin", "Palette"; `seats/lena-park.md` L20-47 |
| 7 | Accent (headset + tie): pick an existing row; not like `#F2994A`; apart from Kit's `#D4503A` | decided (my pick, the brief hands it to me): row 10 `#C9A6D6` | `sketch-brief.md` "Look"; reason in `body-map.md` |
| 8 | Value break vs Kit's trousers (1.27:1) | decided: shirt V in row 16, plus the row 10 accent | `acceptance/kit/lena-park.md` L51; `sketch-brief.md` "Legibility risk" |
| 9 | Other colours (hair, shoes): existing rows only | decided (my pick): hair row 25, shoes row 5 (wood, like Kit's brown shoes) | `seats/lena-park.md` L26, L46 |
| 10 | Drain colours, steps 1 and 2: existing rows only, no lerp colours on the sheet | decided (my pick): suit 17 -> 11 -> 27 -> 16; skin 15 -> 15 -> 16 -> 16; tie stays row 10; headset 10 -> 10 -> 27 -> 27 | `sketch-brief.md` "Palette"; `assets/ghostie/LOCKED.md` (row 27 headset, row 10 tie) |
| 11 | Drain end: the locked Ghostie; headset and tie on its body-map points | decided | `assets/ghostie/LOCKED.md`; `assets/ghostie/sketch/body-map.md` C; `v7/front-variants.png` |
| 12 | Body map: proportions, eyes, mouth, ears, neck, shoulders, hands, feet; headset and tie attachment | decided by me (step 1a is my job) | council `SKILL.md` 1a; `body-map.md` |
| 13 | Ears for the cups: Kit shows no ears; Ricky gets small ears on the eye line at the head sides, under the cups | decided by me (shape language) | same as Ghostie rule "ears on the eye line" (`ghostie/sketch/body-map.md` B) |
| 14 | Mouth: Ricky has a wide smile (he talks); it fades in drain step 2 (a ghost never replies) | decided | `bible.md` L30; `seats/viet-tran.md` L63 "wide smile" |
| 15 | Motion parts: a hop like Kit's; "on the phone" hand to the headset; the drain. Draw the arm joins | decided | `sketch-brief.md` "Motion parts" |
| 16 | Props: none named in the brief (Viet's old clipboard is not in it) | decided: no prop; the phone gesture uses the headset | `sketch-brief.md` "Look" lists suit, headset, tie only |
| 17 | References: Kit (`kit/turn-*.png`), Ghostie (`ghostie/sketch/`, `v7/front-variants.png`, `v7/lineup-grass-crop-*.png`); no web | decided | `sketch-brief.md` last line |
| 18 | Hardest part: the drain must keep the headset and tie on the same landmarks while the body turns into the Ghostie | named; solved first in the body map (landmark table maps Ricky -> Ghostie) | `body-map.md` E |
| 19 | My skill steps: illustrator Phase 1-2 (references, 8-12 thumbnails, 2-3 directions, pick with reason); § 9.2 thumbnail and squint check (greyscale lineup); § 10 #1 fewest marks | decided | `~/.claude/skills/illustrator/SKILL.md` "Workflow", § 9.2, § 10 |
| 20 | Tools: hand-written SVG Bezier paths, python to place them, `magick` to render; reuse Ghostie SVG approach and its camera estimate idea | decided | `sketch-brief.md` item 5; `ghostie/sketch/src/` |
| 21 | Checklist: council sketch gate (shape, build in budget, views agree, palette and value, role at game camera, motion parts); 2x self-check of every panel; `notes.md` with Fact/Opinion | decided | council `SKILL.md` step 2, "Whole-picture check"; `sketch-brief.md` last paragraph |

Conflicts found: none that block. Two calls I make and flag in `notes.md` for the chair:
- The locked Ghostie has one swap part per Ghostie (tie OR headset). The drain strip ends on a Ghostie that shows both,
  only to prove the mapping. Which part the game keeps is the chair's or Rega's call.
- The drain steps use existing rows (11, 27) instead of in-between colours. In 3D the drain may lerp; that is Viet's
  and Lena's call.
