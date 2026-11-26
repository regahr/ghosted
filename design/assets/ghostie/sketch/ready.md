# Ready check: Ghostie body map + sketch v2 (Illustrator, 2026-11-25)

Rule: `~/.claude/skills/council/SKILL.md` "Ready check before any drawing", "Whole-picture check", "Game art
pipeline" 1a and 1b. Brief: `design/acceptance/ghostie/bodymap-brief.md`; fixes: `acceptance/ghostie/sketch-fix-v2.md`.
Paths are relative to `runs/jobless-roguelike/design/`.

| # | Need | State | Source |
|---|---|---|---|
| 1 | Goal: decide the body map first, then an upright sketch v2 with the headset centred (2 cups) and the tie centred under a collar | decided | `bodymap-brief.md` lines 3-5; Rega ts 1795614083.836699 "ok ur pick" |
| 2 | Who sees it: BMGD (role rules), Viet (buildable), Lena (values), then Rega with the sketch | decided | council `SKILL.md` step 1a "Owners" |
| 3 | Proportions: keep v5 size and dome; give them in head-heights | decided | `bodymap-brief.md` step 2; council 1a |
| 4 | Landmarks: eye line UP, ears on the eye line at the side edges, neck line with a small centred collar below the eyes, chest, arm roots, hem | decided | `bodymap-brief.md` step 2 |
| 5 | Attachment: headset band centred over the crown + a cup on each ear point; tie centred, hanging from the collar; glasses on the eye line | decided | `bodymap-brief.md` step 2 |
| 6 | Face zone: empty mouth zone; collar and knot BELOW it; no mouth ever | decided | `bodymap-brief.md` step 2; `bible.md` L30 |
| 7 | Game camera: 26 m, pitch 42 deg, yaw 20 deg, 1.6 px outline; v5 ghost size in `v5/lineup-grass-crop-x3.png` | decided | `bodymap-brief.md`; `assets/ghostie/v5/ingame.html` line 196 |
| 8 | Palette: rows 16, 27, 10, 22 only; shade neutral x0.94 in 2D | decided | `bodymap-brief.md` "Decided needs"; `seats/lena-park.md` |
| 9 | Budget: body+arms about 508, eyes 24, tie 68 or fewer | decided | `bodymap-brief.md`; `acceptance/ghostie/sketch-viet.md` §1 |
| 10 | Motion: arm_L 0 to +40 deg; the tip never above the eye bottom; float bob | decided | `acceptance/ghostie/sketch-emil.md` item 2 |
| 11 | Sheet fixes: upright symmetric turnaround, tilt in its own panel, soft shoulders, headset 2 cups, collar inside the outline, upright wave, no label on a drawing; back hem has a centre notch | decided | `sketch-fix-v2.md` 1-7; `sketch-viet.md` §2 |
| 12 | Tie sheet: only the centred tie with a collar, next to Kit | decided | `bodymap-brief.md` step 3 |
| 13 | My skill steps: illustrator `references/workflow.md` Phase 2 (8-12 thumbnails, 2-3 directions, pick with a reason), SKILL.md § 9.2 thumbnail/squint check, § 10 #1 fewest marks | decided | `~/.claude/skills/illustrator/` |
| 14 | Self-check: 2x crop of every panel in `crops/`, `flaws.md` one line per panel; no report while a flaw shows | decided | `bodymap-brief.md` step 4; council "Whole-picture check" |
| 15 | Tools: hand-written SVG Bezier paths, `magick`; no web, no image generation | decided | `sketch-brief.md` "Tools" |

Conflicts found: none. Calls I make inside my rights (shape language, `SKILL.md` "Who decides what"):
- "Head" of a ghost = crown to the neck line. The exact eye height is chosen from the thumbnails (body-map.md).
- The game-camera estimate projects my front view onto a round body (v5 front and side widths are about equal,
  `v5/turn-front.png`, `v5/turn-side.png`). I check the method on the v5 eye line against the real v5 crop first.
- v1 outputs that no longer match (paint-over, notes) are removed from `sketch/`; they stay in `sketch-v1-archive/`.
