# Ready check: Juno the barista body map + sketch (Illustrator, 2026-11-26)

Rule: `~/.claude/skills/council/SKILL.md` "Ready check before any drawing", "Whole-picture check" (and "Judge a sketch
as a sketch"), "Game art pipeline" 1a, 1b, 1. Brief: `design/acceptance/juno/brief.md`. Rega, ts 1795653224.813279:
"ok go, all ur pick" (brief L3). Paths are relative to `runs/jobless-roguelike/design/`.

| # | Need | State | Source |
|---|---|---|---|
| 1 | Goal: body map + 2D sketch sheet that gives Viet's 3D build what it needs. Rega sees it on one card after the chair's 2x check | decided | `brief.md` L3-5; council "Rega is the gate" |
| 2 | Role: barista at the Job Board Cafe, the heal node (+Morale); writes a kind line on each cup ("You are not a PDF.") | decided | `brief.md` L8-9; `seats/bmgd.md` L44, L74 |
| 3 | Tone: warm, calm, a little dry humour; the one place the game is simply kind | decided | `brief.md` L10 |
| 4 | Shape: BMGD hint capsule + apron box + cup; the shape language is mine; the silhouette must be NEW (not capsule, bell, pear, wedge, box, dome) | decided (mine) | `brief.md` L11-13 |
| 5 | Colours: existing rows only; apron or outfit from row 6 `#F4A672` and/or row 7 `#D4503A`; read apart from Brett (row 7 vest) by shape and colour split; cup row 12 or 23 with ink text; a darker or ink element carries the read on grass and path (row 6 alone is about 1.2-1.35:1) | decided (chair call; row choice mine) | `brief.md` L14-19; `seats/lena-park.md` L20-48 |
| 6 | Lineups: colour and grey with Kit, Ricky, Dot, Brett, the ATS and a Ghostie. Base: the real Brett v1 renders `assets/brett/v1/lineup-grass.png` and `lineup-path.png` (they hold all of them, Dot's v1 scene plus Brett) | decided | `brief.md` L20; chair brief |
| 7 | Size: about 1.0 x Kit on screen = 75 px, measured as Ricky / Brett (facing the camera, net yaw 5). The hair puff is part of her figure and counts | decided (puff reading mine, flagged) | `brief.md` L21; `assets/brett/v1/measure.md` L13-20 |
| 8 | Game camera: 26 m, pitch 42, yaw 20, fov 26, 1600x900, 1.6 px outline = 74.97 px per m | decided | `assets/kit/ingame.html` L156-157; `assets/brett/sketch/ready.md` row 8 |
| 9 | Budget for the 3D: 1,400 triangles or fewer. The design keeps few parts (body, head + hair + puff, cup) | decided | `brief.md` L22 |
| 10 | Face rules: no fringe (forehead band >= 4 px at 1x, nothing down the temples beside the eyes); strand lines on hair are fine; the mouth must not read as a beard at 1x | decided | `brief.md` L23-27; `bible.md` "Art rule: no fringe" |
| 11 | Mouths: open or grinning mouths in Ricky's style (dark fill, white teeth band along the top); a calm look may use a simple closed smile line; check x3 at the game camera | decided | `bible.md` "Art rule: mouths" (ts 1795659302.700869); coordinator message |
| 12 | Prop: the cup with a line on it; readable text at card size, just a cup at the game camera | decided | `brief.md` L28 |
| 13 | Motion: handing over a cup; a small wave; writing on the cup. Draw the joins, the hands and the cup hold | decided | `brief.md` L29-32 |
| 14 | References: local only, the locked family (Kit, Ghostie v7, Ricky v1, ATS v1, Dot v1, Brett v1) | decided | chair brief |
| 15 | Body map: proportions, landmarks (eyes, ears, neck, chest, hands), attachment points (hair puff + tie, apron bib, straps, waist tie and bow, cup, marker) | decided by me (step 1a) | council `SKILL.md` 1a |
| 16 | Hardest parts: (a) the forehead band >= 4 px with hair pulled back, at pitch 42; (b) a row 6 apron that does not sink on grass or path; (c) a new silhouette that is not Brett's red | named | `brief.md` L13-19, L24 |
| 17 | My skill steps: Phase 1-2 (references, 8-12 thumbnails, 2-3 directions, a pick with a reason); § 9.2 thumbnail and squint check (grey lineup); § 10 #1 fewest marks | decided | `~/.claude/skills/illustrator/SKILL.md` "Workflow", § 9.2, § 10 |
| 18 | Tools: hand-written cubic Bezier half outlines lifted to round bodies (Ricky library `assets/ricky/sketch/src/ricky.py`); Dot's posed render (`assets/auntie-dot/sketch/src/dot.py`); Brett's build helpers (`assets/brett/sketch/src/build.py`: calibration, grey, ratio, tiles, lineup, silhouette); `magick` | decided | chair brief; `brief.md` L42 |
| 19 | Checklist: sketch gate items (shape and silhouette; buildable and views agree; palette and value; role at the game camera; motion parts); 2x self-check of every panel; `notes.md` with Fact / Opinion | decided | council `SKILL.md` step 2, "Whole-picture check" |

Missing or unclear: none that blocks. Calls I make and flag in `notes.md`:
- The hair puff counts in her 75 px height (row 7).
- The rows for hair, top and legs (row 5): my pick, with reasons and ratios in `notes.md`.
