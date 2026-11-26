# Ready check: Gary the pigeon postman, body map + sketch (Illustrator, 2026-11-26)

Rule: `~/.claude/skills/council/SKILL.md` "Ready check before any drawing", "Whole-picture check" ("Judge a sketch as a
sketch"), "Game art pipeline" 1a, 1b, 1. Brief: `design/acceptance/gary/brief.md` (chair, 2026-11-26). Rega: "all ur
pick" (ts 1795653224.813279), "proceed" (ts 1795664774.871229). Paths are relative to `runs/jobless-roguelike/design/`.

| # | Need | State | Source |
|---|---|---|---|
| 1 | Goal: body map + 2D sketch sheet that gives Viet's 3D build what it needs; Rega sees it on one card after the chair's 2x check | decided | `brief.md` L3-6; council "Rega is the gate" |
| 2 | Role: brings every result (yes, no, "under review"); the kindest delivery in the game; a little bumbling, sincere, never smug | decided | `brief.md` L9-11; `seats/bmgd.md` L46, L63 |
| 3 | Shape: BMGD hint (sphere body, cone beak, 2 box wings); shape language is mine; a toy pigeon in the round-toy family, postman cap + mail bag; reads "bird plus post" at the game camera | decided (shape mine) | `brief.md` L12-14 |
| 4 | Colours (existing rows only): body row 8 `#A8C4DC`; a darker row for wings or head if value needs it; beak + feet row 13 `#F0B43C` (small); cap row 26 or 22; bag row 5 or 24; envelope row 23 with a row 7 or row 10 stamp; outline + one darker element to separate from grass and path | decided (chair call; row picks mine) | `brief.md` L15-23; `seats/lena-park.md` L19-46 |
| 5 | Lineups: colour and grey, with Kit and 2-3 of the locked cast. Base = the newest real family render, `assets/panel/v1/lineup-grass.png` and `lineup-path.png` (Kit, Ricky, Ghosties, ATS, Dot, Brett, Juno, the Panel) | decided | `brief.md` L23; `assets/panel/LOCKED.md` |
| 6 | Size: about 0.5 x Kit standing (Kit 0.977 m -> about 0.49 m, about 37 px of Kit's 75 px); wingspan in flight about 1.0 x Kit (about 0.98 m) | decided | `brief.md` L24-25; `assets/kit/build_report.json`; `assets/panel/v1/measure.md` (Kit 75 px) |
| 7 | Budget for 3D: <= 900 visible triangles, <= 3 non-swap meshes; envelopes and the bag flap are swap parts | decided | `brief.md` L26-27 |
| 8 | Face: eyes + a beak that is clearly a beak; no human mouth; nothing (tuft, cap) covers the eyes | decided | `brief.md` L28-29; `bible.md` "Art rule: no fringe" |
| 9 | Motion: fly in (0.6 s flap loop), land with a little hop, hold out an envelope (beak or wing), soft "sorry" head tilt for a no, happy hop for a yes, fly off | decided | `brief.md` L30-36 |
| 10 | Game camera: 26 m, pitch 42, yaw 20 (net yaw 5 for a lineup-facing character), fov 26, 1600x900, 1.6 px outline = 74.97 px per m | decided | `brief.md` L37; `assets/kit/ingame.html` L156-157 (as in the Panel and Juno sketches) |
| 11 | References: local only, the locked cast (Kit, Ghostie v7, Ricky v1, ATS v1, Dot v1, Brett v1, Juno v1, Panel v1). No web (not handed over) | decided | coordinator message; workspace `CLAUDE.md` |
| 12 | Body map: proportions, landmarks (eyes, beak, ear points, neck, chest, wing roots = shoulders, wing tips = hands, tail, legs, feet) and attachment points (cap, bag strap, bag, envelope in the beak, envelope in the wing tip) | decided by me (step 1a) | council `SKILL.md` 1a |
| 13 | Moving parts and joins: 2 rigid wings that pivot at the wing root (flap); head pivot at the neck (tilt, nod); whole-body hop; envelope swap at the beak socket or the wing-tip socket; bag flap swap | decided by me | `brief.md` L26-36 |
| 14 | Hardest parts: (a) a cap on a small head seen from 42 deg above must not hide the eyes; (b) "bird plus post" at about 37 px; (c) a light blue-grey body must still separate from light grass and path; (d) the wing holding an envelope reads as a hand | named | `brief.md` L12-23 |
| 15 | My skill steps: Phase 1-2 (references, 8-12 thumbnails, 2-3 directions, pick with reason); § 9.2 thumbnail and squint (grey) check; § 10 #1 fewest marks | decided | `~/.claude/skills/illustrator/SKILL.md` "Workflow", § 9.2, § 10 |
| 16 | Tools: Juno sketch code (`assets/juno/sketch/src/juno.py`, `build.py`), the Panel `build.py` lineup helpers, the Ricky library, the Dot render; `magick`; nothing leaves this machine | decided | coordinator message; `brief.md` L44 |
| 17 | Checklist: sketch gate items (shape and silhouette; buildable and views agree; palette and value; role at the game camera; motion parts); 2x self-check; `notes.md` with Fact / Opinion | decided | council `SKILL.md` step 2, "Whole-picture check" |

Missing: none. Unclear: none. "Body 0.5 x Kit" I read as the standing height to the cap top (the cap counts, as
Juno's puff counted). I start.
