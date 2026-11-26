# Gary 3D v1: ready check (Viet Tran, 2026-11-26)

Paths are relative to `runs/jobless-roguelike/design/`. Each need is **decided** (with its source) or **missing**.

| Need | State | Source |
|---|---|---|
| Goal and viewer: Gary brings every result (yes, no, under review); the kindest delivery; the player sees him at the game camera | decided | `acceptance/gary/brief.md` "Decided needs", Role |
| Accepted sketch: direction A, "round postie" | decided | `brief.md` "Chair calls after the sketch"; `assets/gary/sketch/gary-sheet.png` |
| Body map: proportions, landmarks, attachment points (cap, brim, badge, bag, strap, 2 envelope sockets), pivots | decided | `assets/gary/sketch/body-map.md`, `body-map.png`; numbers in `sketch/src/gary.py` |
| Real view size: 26 m, pitch 42, yaw 20 (fov 26, 1600x900, as Juno and Panel v1) | decided | `brief.md` Game camera; `assets/panel/v1/measure.md` set-up |
| Budget: 900 visible tris or fewer; 3 non-swap meshes (body, wing L, wing R); envelopes and bag flap are swaps; thin the strap and feathers first, keep eyes, beak, cap | decided | `brief.md` chair call 1 |
| Size: 0.5 x Kit standing (0.488 m to the cap top); wingspan 1.06 x Kit (1.03 m) | decided | `brief.md` Size + chair call 2; `body-map.md` |
| Eyes: 15 % bigger than the sketch; the cap never covers the eyes | decided | `brief.md` chair call 3 |
| 3D fixes: folded wings tucked back and in (no "hanging arms" from the front); strap not a low loop in the side view | decided | `brief.md` chair call 4 |
| Palette: rows 8, 9, 26, 22, 13, 5, 23, 7 | decided | `sketch/notes.md` Colours |
| Face: eyes + brows only, beak, no mouth; nothing over the eyes | decided | `brief.md` Face; `body-map.md` Mouth zone |
| Motion: key poses only; flap 3 keys (up 50, level 5, down -35); land hop, hold letter, sorry tilt (head roll -14), happy hop, fly off; flight pitch 10 nose down, legs tucked | decided | `brief.md` Motion + chair call 5; `body-map.md` Moving parts |
| Joins | decided (mine) | `direction.md` "Join decisions" |
| Hardest parts | decided (mine) | `direction.md` "Hardest parts" |
| Lineups: Kit + cast, grass and path, colour and grey, x3 and 1x; Gary right of Kit on grass, in front on the path, a flying copy | decided | `brief.md`; spots from `sketch/notes.md` Open 4 (cheap to change) |
| Pipeline: Panel v1 (Blender build -> glb -> three.js ingame.html + Playwright -> PIL sheets) | decided | the task brief; `assets/panel/v1/` |
| My skill steps and tools | decided | `direction.md`; `skill/search.txt`, `skill/design-context.txt`, `skill/host-probe.txt`, `skill/resolve-*.txt` |
| Checklist | decided | the task deliverables list; `selfcheck.md` |

Nothing is missing. Start.
