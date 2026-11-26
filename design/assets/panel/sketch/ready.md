# Ready check: The Panel (Ms. Culture Fit, Mr. Whiteboard, the Camera-Off One) body map + sketch (Illustrator, 2026-11-26)

Rule: `~/.claude/skills/council/SKILL.md` "Ready check before any drawing", "Whole-picture check" ("Judge a sketch as a
sketch"), "Game art pipeline" 1a, 1b, 1. Brief: `design/acceptance/panel/brief.md` (chair, 2026-11-26). Rega: "all ur
pick" (ts 1795653224.813279), "ok proceed then" (ts 1795664774.871229). Paths are relative to `runs/jobless-roguelike/design/`.

| # | Need | State | Source |
|---|---|---|---|
| 1 | Goal: body map + 2D sketch sheet that gives Viet's 3D build what it needs; Rega sees it on one card after the chair's 2x check | decided | `brief.md` L3-6; council "Rega is the gate" |
| 2 | Role: "Panel Plates" set, Panel Heights (weeks 9-11): 3 interviewers at one table: Ms. Culture Fit (vibe check), Mr. Whiteboard (technical, marker), the Camera-Off One (black box on the table) | decided | `brief.md` L10-15; `seats/bmgd.md` L45 |
| 3 | Tone: comic and kind; absurd, never cruel | decided | `brief.md` L16 |
| 4 | Shape: BMGD hint table 2.0 x 0.1 x 0.6, 2 sphere heads, 1 box; shape language is mine; the three read apart by silhouette, not colour alone; humans seated, upper body above the table; toy-pawn family | decided (mine) | `brief.md` L17-19 |
| 5 | Colours: existing rows only. Table row 5 or row 24 (pick one, with reason). Box row 22 or 17 with a row 12 icon. People: rows apart from Kit 14, Ricky 17, Dot 11, Brett 7, Juno 5/6, ATS 18, Ghostie 16; no big row 20 or 13 areas | decided (chair call; row picks mine) | `brief.md` L20-26; `seats/lena-park.md` palette table |
| 6 | Budget for 3D: whole set <= 2,000 visible triangles, <= 4 non-swap meshes | decided | `brief.md` L27-28 |
| 7 | Size: table top about 0.75 x Kit height; a seated head "at about Kit's head height at the game camera" | **unclear, resolved by the brief itself (flagged)**: read as head SIZE = Kit's head size. The other reading (head top at Kit's head top, 0.98 m) cannot be built: with the table top at 0.73 m the chin would sit below the table top. Numbers and the choice are in `notes.md` "Open 1" | `brief.md` L29-30; Kit 0.977 m `assets/kit/build_report.json` |
| 8 | Game camera: 26 m, pitch 42, yaw 20 (net yaw 5 for the lineup), fov 26, 1600x900, 1.6 px outline = 74.97 px per m | decided | `brief.md` L37; `assets/kit/ingame.html` L156-157; Juno `build.py` L50 |
| 9 | Faces: mouth Ricky style or a closed line; no fringe (band >= 4 px at 1x), nothing down the temples; prove at 1x no mouth reads as a beard | decided | `brief.md` L31-32; `bible.md` "Art rule: no fringe", "Art rule: mouths" |
| 10 | Motion: Culture Fit nods + tilts; Whiteboard clicks marker + points; box blinks a muted / camera-off icon; all three lean in ("any questions for us?") | decided | `brief.md` L33-36 |
| 11 | Lineups: colour and grey, Kit in front of the table; base = Juno v1 lineup renders (`assets/juno/v1/lineup-grass.png`, `lineup-path.png`) | decided | `brief.md` L37; coordinator message |
| 12 | References: local only, the locked cast (Kit, Ghostie v7, Ricky v1, ATS v1, Dot v1, Brett v1, Juno v1) | decided | coordinator message |
| 13 | Body map: proportions, landmarks (eyes, ears, neck, shoulders, chest, hands, table top, seat), attachment points (bow + headband, flat-top, glasses, pocket pens, marker, box icon) | decided by me (step 1a) | council `SKILL.md` 1a |
| 14 | Moving parts and joins: head (nod/tilt pivot at the chin), right arm + marker, box icon swap, lean pivot at the elbow line | decided by me | `brief.md` L33-36 |
| 15 | Hardest parts: (a) a seated pawn whose head sits well above a 0.73 m table; (b) the black box must read as a "person" on the table; (c) three silhouettes apart in a 150 px wide set | named | `brief.md` L17-30 |
| 16 | My skill steps: Phase 1-2 (references, 8-12 thumbnails, 2-3 directions, pick with reason); § 9.2 thumbnail and squint (grey) check; § 10 #1 fewest marks | decided | `~/.claude/skills/illustrator/SKILL.md` "Workflow", § 9.2, § 10 |
| 17 | Tools: Juno sketch code (`assets/juno/sketch/src/juno.py`, `build.py`), Ricky library, Dot render, Brett hair cap; `magick`; nothing outside this machine | decided | coordinator message; `brief.md` L47 |
| 18 | Checklist: sketch gate items (shape and silhouette; buildable and views agree; palette and value; role at the game camera; motion parts); 2x self-check; `notes.md` with Fact / Opinion | decided | council `SKILL.md` step 2, "Whole-picture check" |

Missing: none. Unclear: row 7 only, and the brief's own table call settles it (only one reading can be built). I
start, and flag it as Open 1 in `notes.md` so the chair can overrule it.
