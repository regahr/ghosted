# Ready check: Auntie Dot body map + sketch (Illustrator, 2026-11-26)

Rule: `~/.claude/skills/council/SKILL.md` "Ready check before any drawing", "Whole-picture check" (and "Judge a sketch
as a sketch"), "Game art pipeline" 1a, 1b, 1. Brief: `design/acceptance/auntie-dot/brief.md` (step 1 only).
Paths are relative to `runs/jobless-roguelike/design/`.

| # | Need | State | Source |
|---|---|---|---|
| 1 | Goal: body map + 2D sketch sheet that gives Viet's 3D build what it needs. Rega sees sketch and 3D together; chair does a 2x check | decided | `brief.md` L3-5, L36-46; council "Rega is the gate" |
| 2 | Role: mentor at the meta hub (Copium buys Skills); ex-recruiter who once ghosted someone, now answers everyone | decided | `brief.md` L8-9; `seats/bmgd.md` L42 |
| 3 | Voice and tone: warm, wise, a bit cheeky; the kindest character | decided | `brief.md` L10-13; `seats/bmgd.md` L72-73 |
| 4 | Shape: BMGD hint "short capsule, bun sphere"; the shape language is mine to explore | decided | `brief.md` L14 |
| 5 | Palette: cardigan/dress row 11 `#7A5596`; hair (bun) row 23 `#FFF8EE`; skin row 15 `#F2C79E`; ink row 22 `#2B1E16`; glasses frame or shoes from existing rows; shade = neutral grey multiplier | decided | `brief.md` L15-21; `seats/lena-park.md` rows 11, 15, 22, 23 |
| 6 | Shoes: existing row. My pick: row 5 wood `#7A4A2E` (same as Kit and Ricky, the family) | decided (my pick, brief allows) | `brief.md` L20; `seats/lena-park.md` row 5 |
| 7 | Glasses: optional. Explored in the thumbnails; the pick is in `notes.md` | decided (my call, brief allows) | `brief.md` L20 |
| 8 | Story prop: her old recruiter headset, faded row 27 `#C8C0D8`, worn round the NECK (band behind the neck, a cup on each side of the chin at the collarbones), not on the ears. At the game camera a lilac ring at the neck is enough | decided | `brief.md` L22-24 |
| 9 | Skill card prop (for the "hand over a Skill card" gesture): HUD card look, row 23 panel, row 24 edge, row 13 gold mark (Copium) | decided (from the palette "Use" column) | `seats/lena-park.md` rows 13, 23, 24 |
| 10 | Size: 0.9 x Kit on screen = 0.9 x 75 = 67.5 px, measured facing the camera (net yaw 5) as Kit and Ricky were | decided | `brief.md` L25-26; `assets/ricky/v1/measure.md` (Kit 75 px); `assets/ats9000/v1/measure.md` (method) |
| 11 | Game camera: 26 m, pitch 42, yaw 20, fov 26, 1600x900, 1.6 px outline = 74.97 px per m at the target | decided | `assets/kit/ingame.html` L146, L156-157; `assets/ricky/sketch/ready.md` row 4 |
| 12 | Budget for the 3D: 1,400 visible triangles or fewer, at most 3 non-swap meshes. The design must allow a 3-mesh build | decided | `brief.md` L27 |
| 13 | Motion: idle sway; talk beat (head tilt + a hand up); "hand over a Skill card". Draw the joins | decided | `brief.md` L28-31 |
| 14 | Face: open and kind, a mouth (she replies). Bun and hair must not cross the eyes (Ricky fringe lesson) | decided | `brief.md` L32-33; `assets/ricky/v1/measure.md` "Hair line" |
| 15 | Lineup: greyscale with Kit, Ricky, a Ghostie and the ATS. Base: the real render `assets/ats9000/v1/lineup-grass.png` (it holds all four) | decided | `brief.md` L34 |
| 16 | References: local only. Kit (`assets/kit/turn-*.png`), Ricky (`assets/ricky/v1/turn-front.png`, sketch), Ghostie v7, ATS v1, the v1 lineup | decided | `brief.md` L5 ("Reuse..."); chair brief to me |
| 17 | Body map: proportions, landmarks (eyes, ears, neck, chest, hands), attachment points (headset band and cups, bun, card in hand) | decided by me (step 1a is my job) | council `SKILL.md` 1a; `body-map.md` |
| 18 | Hardest part: the neck headset must sit where a real headset sits round a neck (band behind the neck, cups at the front) AND show at pitch 42 under a big round head. Solved first in the body map with a top view and a game-camera dot check | named | `brief.md` L22-24; council 1a "never move an accessory to dodge the camera" |
| 19 | My skill steps: illustrator Phase 1-2 (references, 8-12 thumbnails, 2-3 directions, a pick with a reason); § 9.2 thumbnail and squint check (grey lineup); § 10 #1 fewest marks | decided | `~/.claude/skills/illustrator/SKILL.md` "Workflow", § 9.2, § 10; `references/workflow.md` § 8.1 |
| 20 | Tools: hand-written cubic Bezier half outlines, lifted to round bodies with the Ricky sketch library (`assets/ricky/sketch/src/ricky.py`: profiles, `revolved`, `ellipsoid`, `tube`, `render`, `cam`); ATS camera calibration (`assets/ats9000/sketch/src/build.py` L47-50); `magick` to render | decided | chair brief; `brief.md` L45 |
| 21 | Checklist: sketch gate (shape and silhouette; buildable in budget and views agree; palette and value; role at the game camera; motion parts); 2x self-check of every panel; `notes.md` with Fact / Opinion | decided | council `SKILL.md` step 2, "Whole-picture check", "Judge a sketch as a sketch" |

Missing or unclear: none that blocks. Calls I make and flag in `notes.md`:
- Hair row 23 `#FFF8EE` is almost the Ghostie body row 16 `#F8F4EA`. The bun is small, so I keep the brief's row.
- The Skill card prop look (row 23 + 24 + 13) is my reading of the palette, not a decided card design.
