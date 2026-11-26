# Ready check: ATS-9000 body map + sketch (Illustrator, 2026-11-26)

Rule: `~/.claude/skills/council/SKILL.md` "Rega is the gate", "Ready check before any drawing", "Whole-picture check"
("Judge a sketch as a sketch"), "Game art pipeline" 0, 1a, 1b, 1. Brief: `design/acceptance/ats9000/sketch-brief.md`.
Paths are relative to `runs/jobless-roguelike/design/` unless they start with `concept/`.

| # | Need | State | Source |
|---|---|---|---|
| 1 | Goal: body map, then a 2D sketch sheet for Viet's 3D build. No seat rounds; the chair checks at 2x, then Rega | decided | `sketch-brief.md` header; council `SKILL.md` "Rega is the gate" |
| 2 | Role and tone: the gate of ATS Catch; reads CVs for keywords; literal, NOT evil; comic and kind. Voice: "KEYWORD 'SYNERGY' NOT FOUND. PLEASE BE MORE SYNERGY." | decided | `seats/bmgd.md` L40, L71; `sketch-brief.md` "Role" |
| 3 | Shape parts: box head + screen + scan line (Viet, BMGD visor slit), box body, cone hopper (BMGD), 2 treads, stamp arm "NOT A FIT", antenna (Viet). Combine in 2-3 directions, pick one | decided (the combining is my job) | `seats/bmgd.md` L40; `seats/viet-tran.md` L65; `sketch-brief.md` "Shape parts" |
| 4 | Size: about 1.2 x Kit's on-screen height; Kit = 75 px at the game camera -> target 90 px | decided | `sketch-brief.md` "Size"; `assets/ricky/v1/measure.md` (Kit 75 px) |
| 5 | Game camera: 26 m, pitch 42, yaw 20, fov 26, 900 px tall -> 74.97 px per metre at the target; 1.6 px outline | decided | `sketch-brief.md` "Game camera"; `assets/ricky/sketch/src/build.py` L36-41 (same constants) |
| 6 | Camera estimate method: project the sketch model at pitch 42 / yaw 20, metric px = height x 75 px/m + outline. Proven: Ricky 1.00 m estimate 67 px, real blockout 66 px | decided | `assets/ricky/sketch/src/build.py` `cam_scale`; `assets/ricky/v1/measure.md` table row 1 |
| 7 | Budget: 900 triangles or fewer, at most 3 non-swap meshes | decided | `sketch-brief.md` "Budget"; `seats/viet-tran.md` L65 |
| 8 | Palette: body row 18 `#8E9BA8`; screen and visor ink row 22; eyes + scan line cream row 12 `#FFE8A6` (NOT teal); antenna ball gold row 13; stamp rubber ink row 22; shade = neutral grey multiplier. Not BMGD's or Viet's hexes | decided | `sketch-brief.md` "Colours"; `seats/lena-park.md` L18-47, L82 |
| 9 | Colours the brief does not name: treads, hopper, CV prop, name plate | decided (my pick, rows already in the brief's list): treads ink 22, hopper 18, CV paper + name plate panel 23. No new row | `sketch-brief.md` "Colours" |
| 10 | Red-ink row 21: text-only. I use it ONLY for the printed words "NOT A FIT" on the CV prop (that is text). The stamp rubber stays ink 22. Flagged in `notes.md` | decided, flagged | `seats/lena-park.md` row 21 "warning text"; `sketch-brief.md` "stamp ink row 22, or red-ink row 21 ... flag it" |
| 11 | Value: mid grey; on grass 1.74:1, so the ink outline carries it. Show a greyscale lineup with Kit, Ricky, a Ghostie | decided | `sketch-brief.md` "Value"; `seats/lena-park.md` L82 |
| 12 | Motion parts and joins: scan line, stamp arm down, treads roll, antenna blink, hopper takes a CV | decided | `sketch-brief.md` "Motion parts" |
| 13 | Body map landmarks: screen/face zone, hopper mouth, stamp pivot, antenna base, tread line; no human mouth (the hopper is the "mouth") | decided | `sketch-brief.md` "Body map" |
| 14 | Expressions / variants on the sheet: the brief lists none; the pipeline asks for them | decided (my call): screen states idle, reading, keyword found, not a fit, loading. Screen only; the body never changes | council `SKILL.md` "Game art pipeline" step 1 |
| 15 | References: mock ATS Tower `concept/out/shots/02-hub.png`, ATS Catch `concept/out/shots/05-ats-catch.png`; Kit (`assets/kit/turn-*.png`), Ricky (`assets/ricky/v1/turn-front.png`, `lineup-grass.png`), Ghostie (`assets/ghostie/v7/turn-front.png`); no web, no image generation | decided | `sketch-brief.md` "What to make" 2 and last paragraph |
| 16 | Hardest part: a mid-grey box robot must read at about 90 px from above (pitch 42) as "a machine that reads your CV", and stay kind | named; solved first in the explore sheet: every thumbnail and direction gets a game-camera tile before the pick | own call |
| 17 | Second hard part: draw order of box parts (treads under the body, the arm beside it) in every view | named; the sketch model splits each tread into back end / middle / front end | own call |
| 18 | My skill steps: illustrator "Workflow" Phase 1-2 (references, 8-12 thumbnails, 2-3 directions, pick with reason); 9.2 thumbnail + squint check (greyscale lineup, 64 px silhouette); 10 #1 fewest marks; 10 #2 no cliche | decided | `~/.claude/skills/illustrator/SKILL.md` "Workflow", 9.2, 10 |
| 19 | Tools: hand-written SVG Bezier profiles, python to extrude and project them, `magick` to render; reuse the Ricky / Ghostie SVG and camera approach | decided | `sketch-brief.md` item 5; `assets/ricky/sketch/src/`, `assets/ghostie/sketch/src/camera.py` |
| 20 | Checklist: sketch gate (shape and silhouette; build in budget; views agree; palette and value; role at game camera; motion parts); 2x check of every panel; `notes.md` with Fact / Opinion | decided | council `SKILL.md` step 2, "Whole-picture check"; `sketch-brief.md` last paragraph |
| 21 | Boundary: write only in `assets/ats9000/sketch/` | decided | `sketch-brief.md` last line |

Missing or unclear: none. Start.

Calls I make myself (shape language is mine) and flag in `notes.md`:
- One stamp arm only, on the robot's LEFT side (viewer-right in the front view), so it faces the camera at yaw 20
  and in the 3/4 view. The antenna sits on the other top corner to balance it.
- The treads are ink, like Kit's dark trousers: a dark base anchors the mid-grey body on grass.
