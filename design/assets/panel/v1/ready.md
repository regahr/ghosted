# The Panel 3D v1: ready check (Viet Tran, 2026-11-26)

Paths are relative to `runs/jobless-roguelike/design/`. Each need is **decided** (with its source) or **missing**.

| Need | State | Source |
|---|---|---|
| Goal and viewer: the panel interview set (weeks 9-11), seen by the player at the game camera | decided | `acceptance/panel/brief.md` "Decided needs", Role |
| Accepted sketch: direction A, "bow, flat-top, black cube" | decided | `brief.md` "Chair calls after the sketch"; `assets/panel/sketch/panel-sheet.png` |
| Body map: landmarks, attachment points, pivots | decided | `assets/panel/sketch/body-map.md`, `body-map.png`; numbers in `sketch/src/panel.py` |
| Real view size: 26 m, pitch 42, yaw 20, fov 26, 1600x900 | decided | `brief.md` Game camera; `assets/juno/v1/measure.md` set-up |
| Budget: whole set 2,000 visible tris or fewer, at most 4 non-swap meshes (table+chairs, CF, WB+marker, box) | decided | `brief.md` chair call 4 |
| Size: Kit-sized heads; table top 0.733 m | decided | `brief.md` chair call 1 |
| Palette: rows 24, 22, 12, 10, 26, 8, 25, 15, 23, 21, 9, 6 | decided | `sketch/notes.md` Colours; table row 24 kept (`brief.md` chair call 2) |
| Faces: Ricky-style open mouths or closed line; no fringe, nothing at the temples; idle in game = TALK mouth; card views keep rest lines; CF grin keeps 1 px skin above the chin at 1x | decided | `bible.md` "Art rule: no fringe", "Art rule: mouths"; `brief.md` chair calls 3, 5 |
| Motion: CF nod + tilt; WB marker up, click, point; box blink + muted; all lean in | decided | `brief.md` Motion; `sketch/body-map.md` Pivots; `sketch/notes.md` Motion |
| Joins | decided (mine) | `direction.md` "Join decisions" |
| Hardest parts | decided (mine) | `direction.md` "Hardest parts" |
| Lineup: Kit in front of the table, grass and path, colour and grey, x3 and 1x | decided | `brief.md` Game camera; set spot is my call, cheap to change (`measure.md`) |
| Pipeline: Juno v1 (Blender build -> glb -> three.js ingame.html + Playwright -> PIL sheets) | decided | the task brief; `assets/juno/v1/` |
| My skill steps and tools | decided | `direction.md`; `skill/search.txt`, `skill/design-context.txt`, `skill/host-probe.txt` |
| Checklist | decided | the task deliverables list; selfcheck in `selfcheck.md` |

Nothing is missing. Start.
