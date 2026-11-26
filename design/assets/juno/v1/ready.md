# Ready check: Juno the barista 3D v1 (Viet Tran, builder, 2026-11-26)

Rule: `~/.claude/skills/council/SKILL.md`, "Ready check before any drawing". Paths are under
`runs/jobless-roguelike/design/`.

| # | Need | State | Source |
|---|---|---|---|
| 1 | Goal: blockout at the game camera (scale set), then the final 3D Juno that matches the sketch. Rega sees sketch and 3D on one card; the chair checks at 2x first | decided | `acceptance/juno/brief.md` "Chair calls after the sketch"; council "Rega is the gate" |
| 2 | Accepted sketch: direction A "the hourglass", `assets/juno/sketch/juno-sheet.png` | decided (chair 2x check passed) | `brief.md` "Chair calls after the sketch", first line |
| 3 | Body map: puff top y 10 (centre y 40, z -18, 72 x 60 x 64), cap top 52, hairline 64 centre / 84-88 at the head sides, brows 84-89, eye line 104 (= ears), mouth zone 122-140, chin 154, neckline 162, shoulder root (+-54..96, 186), bib top 198, waist / apron tie 238 (pinch, 82 wide), hem 294 (134 wide), legs 288-326, sole 340; body depth 0.8 | decided | `sketch/body-map.md` A-C; curves `sketch/src/juno.py` `LM`, `HEAD_HALF`, `CAP_HALF`, `BODY_HG`, marks |
| 4 | Size: 1.0 x Kit on screen = 75 px, COUNTING the puff; measured alone on magenta at Kit's spot, ink included, net yaw 5 (= Brett, Ricky) | decided | `brief.md` chair call 1 |
| 5 | Palette: top + skirt + shoes row 5 `#7A4A2E`, apron + cheeks row 6 `#F4A672`, tie / bow / pocket / scrunchie / marker row 7 `#D4503A`, hair row 25 `#4A3226`, skin row 15, leggings row 26, cup + lid + teeth + glint row 23 `#FFF8EE`, ink row 22; shade = Kit's neutral grey band | decided | `brief.md` chair call 3; `sketch/notes.md` "Colours" |
| 6 | Cup: white cup with a lid; text "You are not a PDF." as a hand-drawn stroke decal in ink, polylines, not a font; readable at card size; just a cup at the game camera | decided | `brief.md` chair call 4 |
| 7 | Builder notes: no skin sliver at the forehead edge in 3/4; side-profile ticks allowed as a known limit | decided | `brief.md` chair call 5 |
| 8 | Face rules: no fringe (forehead band >= 4 px at 1x, nothing down the temples beside the eyes); rest mouth = closed smile line; laugh and talk = Ricky style; prove no beard read at 1x | decided | `brief.md` chair call 6; `bible.md` "Art rule: no fringe", "Art rule: mouths" |
| 9 | Game camera: 26 m, pitch 42, yaw 20, fov 26, 1600x900, 1.6 px outline; root turned 15 deg (net yaw 5) | decided | `assets/brett/v1/ready.md` row 10; `assets/brett/v1/ingame.html` `renderLineup` |
| 10 | Budget: 1,400 visible triangles or fewer in every beat; the split is mine to cut | decided | `brief.md` chair call 2; `sketch/notes.md` "Notes for the 3D builder" |
| 11 | Motion: rest (cup in both hands at the apron); hand over (her right arm forward, cup on the palm, other hand at her side, smile); small wave (her right hand by the shoulder, 3 frames, cup in the left hand); writing (cup up at the chest in the left hand leaning back 10 deg, marker in the right hand, head down 14 deg, eyes down; then the hand over) | decided | `sketch/notes.md` builder notes; `juno.py` `model()` arms `cup`, `hand`, `wave0-2`, `write`/`holdhigh`/`pen` |
| 12 | Expressions: rest smile, laugh (Ricky mouth), talk (Ricky mouth), dry (one brow, smirk), writing (eyes down) | decided | `sketch/juno-sheet.png` EXPRESSIONS; `juno.py` `SMILE`, `LAUGH`, `TALK`, `SMIRK`, `BROWS_DRY`, `HAPPY_EYES`, `DOWN_EYES` |
| 13 | Joins | mine; decided in `direction.md` section 3 | skill `SKILL.md` step 4 |
| 14 | Hardest parts | named in `direction.md` section 2, solved first on the blockout | skill step 2 |
| 15 | My skill steps and tools: `direction.md`, hardest parts first, join decisions, `search.py`, `resolve.py`, `design-context.py`, `host-probe.py`; outputs in `skill/` | decided, run | skill `SKILL.md`; council "Offer is not use" |
| 16 | Pipeline: reuse Brett v1 (`build_brett.py`, `render_brett.py`, `make_sheets.py`, `shoot_ingame.mjs`, `ingame.html`); Blender 4.3, three.js r170, Playwright | decided | chair task; `assets/brett/v1/` |
| 17 | Lineup: Kit, Ricky, Dot, Brett (locked v1 glb), the ATS and Ghosties; grass and path; colour and grey; x3 and 1x crops | decided | chair task; `brief.md` "Chair call, colours" |
| 18 | Deliverables: turnaround, hero; hand-over, wave, writing; expressions; cup close-up at card size; silhouettes, grey, in-game + compare; lineups; compare-sketch, crops; measure.md; selfcheck.md | decided | chair task message |
| 19 | Where Juno stands in the lineups | mine (cheap to change); set after a first look, written in `measure.md` | this file |
| 20 | Stop rule: an item that fails twice stops the build and is reported | decided | council "No blind iterations" |

Result: no need is missing. I start.
