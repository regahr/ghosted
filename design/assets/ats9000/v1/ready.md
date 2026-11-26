# Ready check: ATS-9000 3D v1 (Viet Tran, builder, 2026-11-26)

Rule: `~/.claude/skills/council/SKILL.md`, "Ready check before any drawing". Paths are under
`runs/jobless-roguelike/design/`.

| # | Need | State | Source |
|---|---|---|---|
| 1 | Goal: blockout, then the final 3D ATS-9000 that matches sketch v2 (direction B with a neck). Rega is the gate; the chair checks at 2x first | decided | `acceptance/ats9000/build-brief-3d.md` L1-5; council `SKILL.md` "Rega is the gate" |
| 2 | Accepted sketch | decided | Rega ts 1795628417.229379 ("B looks cool to me, just need to give it a neck"); chair chained the 3D, thread ts 1795628461.631429 (brief L3-4); `assets/ats9000/sketch/ats-sheet.png` |
| 3 | Body map: head 176 x 90 u, neck y 150-200 (core r 17, 3 ink rings r 26, 8 u tall), body arch y 200-304, Z +-50, slot y 240-254, lip y 254-262 Z 44-62, treads x 66-106 / 194-234, y 304-340, Z -58..74, stamp hub y 224 x 212-246, antenna base x 80 Z -16 | decided | `assets/ats9000/sketch/body-map.md` B-C; profiles `sketch/src/ats.py` L35-94 |
| 4 | Facing: faces the camera (root turned 15 deg, net yaw 5, like Ricky in the lineup) | decided | `chair-calls.md` 1; `ricky/v1/ingame.html` L308 |
| 5 | Screen size: 1.21 x Kit on screen (Kit 75 px by the Ricky method, target 90.75 -> 91 px); set by measuring the blockout | decided | `chair-calls.md` 1; brief "Before you model"; `ricky/v1/measure.md` |
| 6 | Game camera: 26 m, pitch 42, yaw 20, fov 26, 1600x900, 1.6 px outline | decided | `ricky/v1/ingame.html` L283, L291 |
| 7 | Budget: 900 visible triangles or fewer; at most 3 non-swap meshes: static body, stamp arm, screen; 12-sided neck rings if tight | decided | brief "Requirements" |
| 8 | Palette: 18 `#8E9BA8`, 22 `#2B1E16`, 12 `#FFE8A6`, 13 `#F0B43C`, 23 `#FFF8EE`; 21 `#B23A26` only as text on the CV; neutral shade (Kit's grey 178 band; sketch shade x0.85) | decided | brief "Colours"; `sketch/src/ats.py` L15-22; `chair-calls.md` 2 |
| 9 | Toon, light, ink hull, contact shadow: Kit's locked set-up (`kit/toon.json`), reused through the Ricky pipeline | decided | brief "References"; `kit/toon.json` |
| 10 | Bevel the box edges about 0.02 m | decided | `chair-calls.md` 5 |
| 11 | Screen: one mesh on the head front, 5 states (idle, reading, found, not fit, loading) by UV, scan line scrolls; never angry | decided | brief "Screen"; sheet SCREEN STATES; `ats.py` `screen_marks` L303 |
| 12 | Motion: stamp rest 45 / wind-up 140 / slam 0 (one hinge, + = lower end forward); CV slides into the slot; hubs spin, belts scroll; antenna ball blinks (gold / gold x0.62); bellows bob optional | decided | brief "Motion"; `ats.py` `rot_x` L265, `REST_DEG` L84 |
| 12a | **Belt scroll needs a visible mark.** The sketch belt is plain ink, so a scrolling plain ink belt shows nothing. My reading: thin cleat lines in robot grey x0.85 (the neutral shade of row 18) across the belt, in a texture that scrolls along the loop. Cheap to change (one texture) | decided by me; flagged to the chair | sheet side view (plain belt); brief "Motion" |
| 12b | Bellows idle bob: optional; I leave it out of v1 (it would need a bone or a morph on the static mesh) | decided by me; flagged | brief "Motion" (optional); sketch `notes.md` 5 "Emil's call" |
| 13 | Open risk: the dark neck band may read as a second smiling mouth above the slot; show it honestly in an x3 crop; no redesign | decided | brief "Open risk"; sketch `notes.md` 4 risk 1 |
| 14 | Joins (head-neck, neck-body, hub-body, stamp-hub, antenna-head, lip-body, slot, screen, treads-body, hubs-treads) | mine to decide; decided in `direction.md` 3 | skill `SKILL.md` step 4 |
| 15 | Hardest parts | named in `direction.md` 2, each tested first in `tests/` | skill step 2 |
| 16 | My skill steps and tools: `direction.md` (step 1), hardest parts first (step 2), join decisions (step 4), `search.py`, `resolve.py`, `design-context.py`, `host-probe.py` (steps 4-5), outputs in `skill/` | decided | skill `SKILL.md`; council "Offer is not use" |
| 17 | Pipeline: reuse `assets/ricky/v1/` (`build_ricky.py`, `render_ricky.py`, `ingame.html`, `shoot_ingame.mjs`, `make_sheets.py`); Blender 4.3, three.js r170, Playwright; locked Kit, Ghostie v7, Ricky v1 in the lineups | decided | brief "References"; `skill/host.json` |
| 18 | Deliverables and checklist: turnaround, hero, stamp, slot, screens, silhouettes, grey, in-game + compare, lineups grass/path colour/grey x3 and 1x, compare-sketch, crops, measure.md (neck in px), selfcheck.md; a visible fault is never PASS | decided | brief "Deliverables" |
| 19 | Stop rule: an item that fails twice stops the build and is reported | decided | brief "Rules"; council "No blind iterations" |
| 20 | Scope: work only in `assets/ats9000/v1/`; no web, no other service | decided | brief "Rules" |

Result: no need is missing. Items 12a and 12b are my readings of the brief; both are cheap to change if the chair
reads them the other way. I start.
