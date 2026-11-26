# Ready check: Ghostie 3D v6, the final model (Viet Tran, 2026-11-25)

Rule: `~/.claude/skills/council/SKILL.md`, "Ready check before any drawing", "Game art pipeline", "Offer is not use".
Brief: `design/acceptance/ghostie/build-brief-v6.md` (called B below). Paths are under `runs/jobless-roguelike/design/`.

| # | Need | State | Source |
|---|---|---|---|
| 1 | Goal: the final Ghostie 3D model, built to match the sketch. Seen by the 5 design seats at the 3D gate, then Rega. | decided | B lines 1-4 |
| 2 | Accepted sketch | **decided by the chair, with one note.** B line 3 quotes Rega (ts 1795617228.257839): "the final result should be the 3D, the sketch should support the 3D drawing requirement", so sketch v2 is the 3D reference. The sketch-v2 gate had seat fails (`acceptance/ghostie/sketch-v2-gate/*.md`: glasses read, headset band, 3/4 far arm, rest-arm hook). B turns each of them into a 3D requirement (B items 2, 5, 6). There is no file that records each seat's acceptance. I go ahead on the chair's brief, and I say so in the report. | B lines 3-4; `sketch-v2-gate/` |
| 3 | View sizes: game camera 26 m, pitch 42°, yaw 20°, 1.6 px outline, 1600x900 lineup; card renders 900x1200 (22° lens) | decided | `blockout/ingame.html` `renderLineup`; `blockout/render_ghostie.py` `TURN_CAM` |
| 4 | Budget: 600 visible triangles per variant (three.js count); at most 3 non-swap meshes; tie at most 68 | decided | `acceptance/checklist.md` V5 amendment 3; B items 4, 6 |
| 5 | Palette: rows 16 `#F8F4EA` body, 27 `#C8C0D8` glasses and headset, 10 `#C9A6D6` tie, 22 `#2B1E16` ink; neutral shade band (Kit's grey 178 band) | decided | B item 7; `sketch/src/ghost.py` lines 9-13; `kit/toon.json` |
| 6 | References and direction: the sheet, the body map and the Bezier source | decided | `sketch/ghostie-sheet.png`, `sketch/body-map.png`, `sketch/src/ghost.py`; my `direction.md` |
| 7 | Body map: eye line y 118 (eyes x 124/176), ear points x 56/244 on y 118, mouth zone empty, neck y 166, knot top y 170, V y 258, arm roots y 190-260, hem cusps y 301, crown y 36 | decided | `sketch/body-map.md` B, C |
| 8 | Scale: front unit = 0.47 m / 265 = 1.774 mm (v5 size kept) | decided | `sketch/body-map.md` B ("v5 size kept"); `blockout/build_ghostie.py` line 187 |
| 9 | Moving parts: float bob and yaw (Emil); arm_L wave 0 to +40°; rest pose = 4° tilt on the float node, arm_R droops lower (in game only) | decided | B item 1; sheet "WAVE" and "REST POSE" panels; `sketch/src/build.py` line 336 (`rot -4`) |
| 10 | Joins: body + arms as one continuous skin (B item 2). The method is my call, in `direction.md` | decided | B item 2; my `direction.md` |
| 11 | Hardest parts: the arm join and the wave on one skin; the headset band over the crown within budget; tips below the eyes at the game camera | decided | my `direction.md` |
| 12 | Hem phase: the sheet views do not agree with each other (front notches at x 112/188, back at 94/150/206, side at 106/194). B asks for "3 seen from the front and a notch centred at the back". I match the front view and the back centre notch, and I report the other views. | decided (my call, within B) | `sketch/src/ghost.py` lines 30-32, 49-50, 101-108 |
| 13 | My skill steps and tools: SKILL.md steps 1, 2, 4, 5, 8, 9; `search.py`, `resolve.py`, `design-context.py`, `host-probe.py` (outputs in `skill/`) | decided | SK `SKILL.md` |
| 14 | Checklist: `acceptance/checklist.md` V1-V6, I1-I3, L1-L3, B1-B2, E1-E2, S1; B items 1-7; B deliverables list | decided | files named |
| 15 | Tools handed over: Blender 4.3, the local three.js and Playwright in `concept/node_modules`, Python with PIL. No web services. | decided | B "pipeline scripts to reuse"; `skill/host.json` |

Result: no need is missing. Item 2 has a note for the chair. I start.
