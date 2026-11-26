# Ready check: Brett Bullet-Points body map + sketch (Illustrator, 2026-11-26)

Rule: `~/.claude/skills/council/SKILL.md` "Ready check before any drawing", "Whole-picture check" (and "Judge a sketch
as a sketch"), "Game art pipeline" 1a, 1b, 1. Brief: `design/acceptance/brett/brief.md` (step 1 only).
Rega, ts 1795653224.813279: "ok go, all ur pick" (brief L3). Paths are relative to `runs/jobless-roguelike/design/`.

| # | Need | State | Source |
|---|---|---|---|
| 1 | Goal: body map + 2D sketch sheet that gives Viet's 3D build what it needs. Rega sees sketch and 3D on one card; chair does a 2x check | decided | `brief.md` L3-4, L35-37; council "Rega is the gate" |
| 2 | Role: the rival, one week ahead in the funnel, talks in bullets, first to like your post in week 12; met at meetup nodes (green door) | decided | `brief.md` L8-9; `seats/bmgd.md` L43, L63 |
| 3 | Voice and tone: smug, toxic-positive LinkedIn guy; harmless, secretly as lost as you; comic, never mean; likeable underneath | decided | `brief.md` L10-12; `seats/bmgd.md` L75 |
| 4 | Shape: BMGD hint "capsule 1.15 m, torus halo"; the shape language is mine | decided | `brief.md` L13 |
| 5 | Halo: the "#OpenToWork" ring, round or above the head; the ONE green thing on him; row 2 `#7FA65A` with an ink edge | decided (chair call) | `brief.md` L14-17 |
| 6 | Body colours: existing rows only; no grass greens on the body; read apart from Kit 14, Ricky 17, Dot 11, ATS 18, Ghostie 16; teal 20 and gold 13 not as big areas; I pick the rows and give reasons | decided (mine to pick, brief allows) | `brief.md` L18-23; `seats/lena-park.md` L20-48 |
| 7 | Size: about 1.05 x Kit on screen = 1.05 x 75 = 78.75 px, measured as Ricky (facing the camera, net yaw 5). My reading: the figure (hair top to sole) is 79 px; the floating halo is extra and reported apart (flagged in `notes.md`) | decided, reading flagged | `brief.md` L24; `assets/ricky/v1/measure.md` L6, L17 |
| 8 | Game camera: 26 m, pitch 42, yaw 20, fov 26, 1600x900, 1.6 px outline = 74.97 px per m | decided | `assets/auntie-dot/sketch/ready.md` row 11; `assets/kit/ingame.html` L146, L156-157 |
| 9 | Budget for the 3D: 1,400 visible triangles or fewer, at most 3 non-swap meshes. The design must allow a 3-mesh build | decided | `brief.md` L25 |
| 10 | Motion: confident idle; "thumbs up / like" (week 12); "talking in bullets" (counting on fingers). Draw the joins, the thumb and the fingers | decided | `brief.md` L26-29 |
| 11 | Face: a mouth with a big confident grin that must NOT read as a beard at 1x (Ricky's lesson); hair must not cross the eyes | decided | `brief.md` L30-31; `assets/ricky/v1/measure.md` L45 |
| 12 | Lineup: colour and grey, with Kit, Ricky, Dot, the ATS and a Ghostie at the game camera. Base: the real render `assets/auntie-dot/v1/lineup-grass.png` (it holds all five) | decided | `brief.md` L32 |
| 13 | References: local only, the locked family (Kit, Ghostie v7, Ricky v1, ATS v1, Dot v1 under `assets/`) | decided | chair brief to me |
| 14 | Body map: proportions, landmarks (eyes, ears, neck, chest, hands), attachment points (halo, collar, thumb, fingers) | decided by me (step 1a is my job) | council `SKILL.md` 1a; `body-map.md` |
| 15 | Hardest parts: (a) a green halo that reads on green grass at 1x and sits where a halo sits (above the crown, not stuck to a body part); (b) a big grin that reads as a grin, not a beard, at 1x. Both solved first in the body map with a game-camera check | named | `brief.md` L14-17, L30-31 |
| 16 | My skill steps: illustrator Phase 1-2 (references, 8-12 thumbnails, 2-3 directions, a pick with a reason); § 9.2 thumbnail and squint check (grey lineup); § 10 #1 fewest marks | decided | `~/.claude/skills/illustrator/SKILL.md` "Workflow", § 9.2, § 10 |
| 17 | Tools: hand-written cubic Bezier half outlines lifted to round bodies with the Ricky sketch library (`assets/ricky/sketch/src/ricky.py`); Dot's pose render and transforms (`assets/auntie-dot/sketch/src/dot.py`); Dot / ATS camera calibration and lineup helpers (`assets/auntie-dot/sketch/src/build.py`); `magick` to render | decided | chair brief; `brief.md` L36 |
| 18 | Checklist: sketch gate (shape and silhouette; buildable in budget and views agree; palette and value; role at the game camera; motion parts); 2x self-check of every panel; `notes.md` with Fact / Opinion | decided | council `SKILL.md` step 2, "Whole-picture check", "Judge a sketch as a sketch" |

Missing or unclear: none that blocks. Calls I make and flag in `notes.md`:
- Size with or without the halo (row 7). I size the figure; the halo is reported apart.
- Body colour rows (row 6): my pick with reasons and ratios in `notes.md`.
