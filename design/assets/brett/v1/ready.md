# Ready check: Brett Bullet-Points 3D v1 (Viet Tran, builder, 2026-11-26)

Rule: `~/.claude/skills/council/SKILL.md`, "Ready check before any drawing". Paths are under
`runs/jobless-roguelike/design/`.

| # | Need | State | Source |
|---|---|---|---|
| 1 | Goal: blockout at the game camera (scale set), then the final 3D Brett that matches the sketch. Rega sees sketch and 3D on one card; the chair checks at 2x first | decided | `acceptance/brett/brief.md` L3-4, L38-39; council "Rega is the gate" |
| 2 | Accepted sketch: direction A "the wedge", `assets/brett/sketch/brett-sheet.png` | decided (chair 2x check passed) | `brief.md` L41-42 |
| 3 | Body map: 2.53 heads; halo centre y 0, swoop top 16, cap top 32, hairline 62 (temples 84-88), eye line 94 (= ears), chin 144, neck line 152, shoulder root (+-56, 176), chest y 188 (widest, 148), V point 198, hem 252, hips 246-268, knee 298, sole 340; vest depth 0.64 | decided | `sketch/body-map.md` A-C; curves `sketch/src/brett.py` `LM`, `HEAD_HALF`, `CAP_HALF`, `VEST_WEDGE`, `HIPS`, `WAVE` |
| 4 | Size: 1.05 x Kit = 78.75 px, measured WITHOUT the halo, as Ricky (alone on magenta, ink included, at Kit's spot, net yaw 5) | decided | `brief.md` L43 (chair call 1) |
| 5 | Palette: vest row 7 `#D4503A`, shirt / teeth / glint row 23 `#FFF8EE`, hair row 12 `#FFE8A6`, skin row 15, chinos row 26, shoes row 5, halo row 2 `#7FA65A` (the ONE green thing), ink row 22; shade = Kit's neutral grey band | decided | `brief.md` L44-46 (chair calls 2-3); `sketch/notes.md` "Colours" |
| 6 | Halo: level ring above the crown, centre y 0, ring 76 x 60 (centre line), tube r 6; ink edge (the outline pass draws round it); follows the head, stays LEVEL when the head nods; no glow | decided | `brief.md` L46 (chair call 3); `body-map.md` C |
| 7 | Carriage: chin up 10 deg at rest in game (turnaround stays neutral) | decided | `brief.md` L47 (chair call 4); `body-map.md` D |
| 8 | Grin: white teeth crescent with no edge, over an ink smile line with the corners up; prove at 1x it reads as a grin, not a moustache or goatee | decided | `brief.md` L48-49 (chair call 5) |
| 9 | Builder notes: no grin sliver or brow tip on the side profile; no hair notch at the far ear in 3/4; hairline and part need ink | decided | `brief.md` L50 (chair call 6); `sketch/notes.md` "Notes for the 3D builder" |
| 10 | Game camera: 26 m, pitch 42, yaw 20, fov 26, 1600x900, 1.6 px outline; root turned 15 deg (net yaw 5) as Kit, Ricky, Dot, ATS | decided | `assets/auntie-dot/v1/ready.md` row 9; `assets/auntie-dot/v1/ingame.html` L344-395 |
| 11 | Budget: 1,400 visible triangles or fewer, at most 3 non-swap meshes (every beat counted) | decided | `brief.md` L25 |
| 12 | Motion: confident idle (hands on hips; puff = lean back 3 deg about the feet + rise 3 u, about 2 s; feet planted); the Like (his right fist out at the side, thumb up, wink); bullets (his right hand up beside the chest, 1-2-3 fingers, mouth open, other hand on the hip) | decided | `brief.md` L26-29; `sketch/notes.md` builder notes; `brett.py` `model()` arms `hips`, `thumb`, `count1-3` |
| 13 | Expressions: grin (rest), talk, wink (the Like), secretly lost | decided | `sketch/brett-sheet.png` EXPRESSIONS; `brett.py` `GRIN`, `TALK`, `WINK`, `BROWS_*`, `LOST_MOUTH` |
| 14 | Joins (hair-skin, swoop-hair, ears, halo, head-neck, neck-vest, sleeve-vest, elbow, hand, hips-vest, legs-hips, shoes, thumb and fingers to the hand) | mine to decide; decided in `direction.md` §3 | skill `SKILL.md` step 4 |
| 15 | Hardest parts | named in `direction.md` §2, solved first on the blockout | skill step 2 |
| 16 | My skill steps and tools: `direction.md` (step 1), hardest parts first (step 2), join decisions (step 4), `search.py`, `resolve.py`, `design-context.py`, `host-probe.py` (steps 4-5); outputs in `skill/` | decided, run | skill `SKILL.md`; council "Offer is not use" |
| 17 | Pipeline: reuse Auntie Dot v1 (`build_dot.py`, `render_dot.py`, `make_sheets.py`, `shoot_ingame.mjs`, `ingame.html`, which loads Kit, 3 Ghosties, Ricky, the ATS and Dot); Blender 4.3, three.js r170, Playwright | decided | chair task; `assets/auntie-dot/v1/` |
| 18 | Deliverables: turnaround, hero; idle, like, bullets; expressions; silhouettes, grey, in-game + compare; lineups (Kit, Ricky, Dot, ATS, Ghostie) grass/path colour/grey with x3 and 1x crops; compare-sketch, crops; measure.md (scale, hair vs eyes, grin at 1x); selfcheck.md | decided | chair task message |
| 19 | Where Brett stands in the lineups | mine to decide (cheap to change); set after a first look, written in `measure.md` | this file |
| 20 | Lineup arms: the sketch's game-camera tiles and lineup show the rest arms with the chin-up carriage; I use that for the main lineups and add the idle (hands on hips), Like and bullets at the game camera as separate crops | mine (cheap to change) | `sketch/crops/sheet-gamecam.png`, `sheet-lineup.png` |
| 21 | Stop rule: an item that fails twice stops the build and is reported | decided | council "No blind iterations" |

Note: `skill/host-probe.txt` says Blender was not found (the probe runs without the app path in this sandbox). Fact:
`/Applications/Blender.app/Contents/MacOS/Blender --version` prints 4.3.0, the same as Dot's `skill/host.json`.

Result: no need is missing. I start.
