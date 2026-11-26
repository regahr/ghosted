# Ready check: Ghostie 3D v7 (Viet Tran, 2026-11-25)

Rule: `~/.claude/skills/council/SKILL.md`, "Ready check before any drawing". v7 starts from a copy of v6. The v6 ready
check (`../v6/ready.md`) still holds except where this file says otherwise. Paths are under `runs/jobless-roguelike/design/`.

| # | Need | State | Source |
|---|---|---|---|
| 1 | Goal: v7 = v6 plus 4 changes. Rega is the only gate; the chair checks at 2x first. | decided | chair's message to me (v7 brief) |
| 2 | Budget: 800 visible triangles per variant (three.js count), spent on the outline | decided | Rega ts 1795619841.598789, checklist amendment 4 (chair's message). Not yet written into `acceptance/checklist.md`; that is the chair's edit. |
| 3 | Wave: a morph target sculpted at +40° to the sheet WAVE outline (`sketch/src/ghost.py` `FRONT_WAVE`), 0 triangles | decided | chair's message, change 2 |
| 4 | arm_R rest pose: swing about 45° forward, plus the sheet droop; the tip must sit below the eye bottom on all 3 lineup ghosts | decided (chair's call for Emil's area) | chair's message, change 3 |
| 5 | Hem: 5 round scallops, with round tops and round notches, and no zigzag | decided | chair's message, change 1 |
| 6 | If cheap: the 3/4 near-arm hook and far-arm crease, the side-view "v", and rounder cups without the octagon pad | decided (optional) | chair's message, change 4 |
| 7 | Keep everything that passed in v6 | decided | chair's message, change 5; `../v6/selfcheck.md` |
| 8 | Camera, palette, body map, scale and skill outputs: as in v6 | decided | `../v6/ready.md` items 3, 5-8, 13; `../v6/skill/` |
| 9 | Deliverables: the v6 set, plus v7-vs-v6 crops of the dome and the hem at 2x, and `compare-sketch.png` | decided | chair's message |
| 10 | Stop rule: if an item fails twice, stop and report | decided | chair's message; council "No blind iterations" |

## Triangle plan (cap 800)
| Part | v6 | v7 plan |
|---|---|---|
| Dome rows (16 columns below the crown) | 8 | 11 (+96) |
| Shoulder row y 165 | none | +32 |
| Arm rings per arm | 3 | 4 (+24) |
| Hem ring and cavity vertices | 40 | 52 (+24) |
| Body + arms | 476 | about 652 |
| Eyes | 24 | 24 |
| Glasses / tie | 98 / 40 | 98 / 40 |
| Headset | 84 | about 112 (10-sided cups, a round ink decal under each cup, a 10-segment band) |
| Worst variant | 598 | about 774 (glasses) |

Result: no need is missing. I start.
