# Ready check: Recruiter Ricky 3D v1 (Viet Tran, builder, 2026-11-25)

Rule: `~/.claude/skills/council/SKILL.md`, "Ready check before any drawing". Paths are under
`runs/jobless-roguelike/design/`.

| # | Need | State | Source |
|---|---|---|---|
| 1 | Goal: blockout, then the final 3D Ricky that matches the accepted sketch. Rega is the gate; the chair checks at 2x first | decided | `acceptance/ricky/build-brief-3d.md` L1-5; council `SKILL.md` "Rega is the gate" |
| 2 | Accepted sketch | decided | Rega "only 1" (ts 1795622448.197729), "that's hair fringe, mic looks fine" (ts 1795622623.559849); `assets/ricky/sketch/ricky-sheet.png` |
| 3 | Body map: proportions 2.67 heads, eye line y 98, cups on the ear points, band over the crown, mic from the right cup, tie knot y 160, V y 232, shoulder joint y 176, hands y 246, hem y 268 | decided | `assets/ricky/sketch/body-map.md` A-C; curves `sketch/src/ricky.py` L36-82 |
| 4 | **Hair change:** no fringe. The hair is a cap on top; the hairline is clearly above both eyes and both brows; nothing of the hair crosses the eyes in any view; keep row 25 and the quiff; the mic stays | decided | Rega ts 1795622664.391049 "can erase the hair fringe?", relayed by the chair (message to me) |
| 4a | My reading of 4: "crosses the eye line" = covers or touches the eyes or brows. The back of the head keeps the sheet's nape hair (BACK view), which is below eye height but never in front of the face | decided by me; flagged to the chair | sheet BACK view; this file |
| 5 | Game camera: 26 m, pitch 42°, yaw 20°, fov 26°, 1600x900, 1.6 px outline | decided | `assets/ghostie/v7/ingame.html` L230, L238 |
| 6 | Screen size: Ricky = 1.05 x the real Kit's on-screen height; Kit is 72 px in the v7 lineup. Set by measuring the blockout, not by metres | decided | `acceptance/ricky/chair-calls.md` item 1; brief "Before you model" 4 |
| 7 | Budget: 1,400 visible triangles or fewer; at most 3 non-swap meshes; shoulder balls merge into the jacket first if tight | decided | brief "Requirements" |
| 8 | Palette: suit 17 `#2E2C3D`, skin 15 `#F2C79E`, hair 25 `#4A3226`, shirt/collar/cuffs 16 `#F8F4EA`, accent 10 `#C9A6D6` (headset + tie), shoes 5 `#7A4A2E`, ink 22 `#2B1E16`; drain rows 11 `#7A5596`, 27 `#C8C0D8`; neutral shade band (Kit's grey 178) | decided | brief "Colours"; `sketch/src/ricky.py` L13-23; `kit/toon.json` bands2 |
| 9 | Toon, light, ink hull, contact shadow: Kit's locked set-up | decided | `assets/kit/LOCKED.md`, `kit/toon.json`; Ghostie v7 pipeline |
| 10 | Motion: hop (squash only on the bounce), phone (right hand to the right cup; bone or morph), drain (suit 17 -> 11 -> 27 -> 16, legs fade, float up, headset Ghostie swaps in at the end) | decided | brief "Motion"; `chair-calls.md` item 2 |
| 11 | Drain end: the locked HEADSET Ghostie; the tie fades with the suit | decided | `chair-calls.md` item 2; `assets/ghostie/LOCKED.md` |
| 12 | Joins (arm-jacket, elbow, head-collar, hair-skin, legs-jacket, headset-head, tie-shirt) | mine to decide; decided in `direction.md` §3 | brief "Joins"; skill `SKILL.md` step 4 |
| 13 | Hardest parts | named in `direction.md` §2 and tested first in `tests/` | skill step 2 |
| 14 | My skill steps and tools: `direction.md` (step 1), hardest parts first (step 2), join decisions (step 4), `search.py`, `resolve.py`, `design-context.py`, `host-probe.py` (steps 4-5), outputs in `skill/` | decided | skill `SKILL.md`; council "Offer is not use" |
| 15 | Pipeline: reuse Ghostie v7 `build_ghostie.py`, `render_ghostie.py`, `ingame.html`, `shoot_ingame.mjs`, `make_sheets.py`; Blender 4.3, three.js r170, Playwright | decided | brief "References"; `skill/host.json` |
| 16 | Deliverables and checklist: turnaround, hero, phone, hop, drain strip, silhouettes, grey, in-game + compare, lineups grass/path colour/grey x3 and 1x, compare-sketch, crops, measure.md, selfcheck.md; a visible fault is never PASS | decided | brief "Deliverables" |
| 17 | Hair proof: game-camera x3 crop of the face; measure line "hair lowest point vs eye top" in screen px | decided | chair's message (hair change) |
| 18 | Stop rule: an item that fails twice stops the build and is reported | decided | brief "Rules"; council "No blind iterations" |

Result: no need is missing. Item 4a is my reading of Rega's hair line; it is cheap to change (one parameter) if the
chair reads it the other way. I start.
