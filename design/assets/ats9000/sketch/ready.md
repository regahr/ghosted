# Ready check: ATS-9000 sketch v2, direction B with a neck (Illustrator, 2026-11-26)

Rule: `~/.claude/skills/council/SKILL.md` "Ready check before any drawing", "Judge a sketch as a sketch", "Game art
pipeline" 1a, 1. Brief: `design/acceptance/ats9000/sketch-brief-B.md`. Chair calls: `acceptance/ats9000/chair-calls.md`.
v1 (direction A) is archived as-is in `assets/ats9000/sketch-v1-A/`. Paths are relative to `runs/jobless-roguelike/design/`.

| # | Need | State | Source |
|---|---|---|---|
| 1 | Goal: develop direction B "Mailbox Bot" into the full v2 sheet, same panels as v1 (turnaround, body map, motion, screen states, 64 px silhouette, colour + grey lineups, game-camera tiles next to Kit, palette) | decided | `sketch-brief-B.md` "Change"; Rega ts 1795628417.229379 "B looks cool to me, just need to give it a neck" |
| 2 | B's shape: tall body with a front CV slot under a small screen head; treads; stamp arm; antenna | decided | `sketch-v1-A/explore.png` direction B; `sketch-v1-A/src/ats.py` `model({"hopper": "slot", "body": "tall", "head_s": 0.8})` |
| 3 | NEW: a neck, clearly visible in every view AND at the game camera, toy family (short cylinder or small accordion) | decided (the design is mine): an accordion of 3 robot-grey rings on an ink core | `sketch-brief-B.md` "ADD A NECK" |
| 4 | Hardest part: at pitch 42 a deep head hides the top of the neck. Rule of thumb: a ray at 42 deg climbs 0.9 u per 1 u forward, so the hidden neck height is about 0.9 x (head front Z - neck front Z) | named; solved first: a shallow "monitor" head (Z +-40), neck r 26 and 40 u tall, so about 27 u of neck shows; plus the body top shows in front of the neck as a light band | own geometry; measured on the game-camera tiles |
| 5 | Head may grow so the eyes read at the game camera | decided: head 176 x 90 u (v1 B was 0.8 x 168), eyes 20 x 30 u | `sketch-brief-B.md`; v1 B note "head too small to carry eyes" |
| 6 | Front CV slot = the mouth; may read as a grin; keep it clearly a slot. Hopper motion becomes "a CV slides into the slot" | decided | `sketch-brief-B.md` "The front CV slot" |
| 7 | Stamp arm: keep, rest about 45 deg so it does not read as a foot | decided | `sketch-brief-B.md` "Keep"; `chair-calls.md` 3 |
| 8 | Antenna, treads, screen states (never angry) | decided: same parts and states as v1 | `sketch-brief-B.md` "Keep" |
| 9 | Palette: v1 rows only (18, 22, 12, 13, 23; 21 as CV text only) | decided | `sketch-brief-B.md` "Keep"; `chair-calls.md` 2; `seats/lena-park.md` |
| 10 | Size: 1.21 x Kit on screen (91 px vs 75), facing the camera (net yaw 5 like the lineup) | decided | `chair-calls.md` 1; `sketch-brief-B.md` "Keep" |
| 11 | Game camera: 26 m, pitch 42, yaw 20, 74.97 px/m; facing = net yaw 5 | decided | `sketch-brief.md` "Game camera"; `chair-calls.md` 1 |
| 12 | Budget: 900 triangles or fewer, at most 3 non-swap meshes | decided | `sketch-brief-B.md` "Keep"; `sketch-brief.md` "Budget" |
| 13 | 3D notes: bevel box edges about 0.02 m; shading bands are lighting, not colour | decided | `chair-calls.md` 5 |
| 14 | Name plate: off | decided | `chair-calls.md` 4 |
| 15 | Body map landmarks: screen (face zone), neck, slot (mouth), stamp pivot, antenna base, tread line | decided (step 1a is mine) | council `SKILL.md` 1a; `sketch-brief.md` "Body map" |
| 16 | Tools: the v1 SVG / extrusion / camera code in `src/`, `magick`; no web, no image generation | decided | `sketch-brief-B.md` "Rules" |
| 17 | My skill steps: illustrator Phase 2 "develop selected direction"; 9.2 thumbnail + squint (grey lineup, silhouette); 10 #1 fewest marks | decided | `~/.claude/skills/illustrator/SKILL.md` |
| 18 | Checklist: 2x check of shape, proportions, placements, views agreeing, game-camera read; `notes.md` with Fact / Opinion | decided | `sketch-brief-B.md` "Rules" |
| 19 | Explore sheet: not asked for in v2 (the pick is Rega's); v1 explore stays in the archive | decided | `sketch-brief-B.md` panel list |

Missing or unclear: none. Start.
