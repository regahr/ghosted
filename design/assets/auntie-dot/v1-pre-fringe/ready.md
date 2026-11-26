# Ready check: Auntie Dot 3D v1 (Viet Tran, builder, 2026-11-26)

Rule: `~/.claude/skills/council/SKILL.md`, "Ready check before any drawing". Paths are under
`runs/jobless-roguelike/design/`.

| # | Need | State | Source |
|---|---|---|---|
| 1 | Goal: blockout at the game camera (scale set), then the final 3D Dot that matches the sketch. Rega sees the sketch and the 3D together on one card; the chair checks at 2x first | decided | `acceptance/auntie-dot/brief.md` L3-5, Steps 3; council "Rega is the gate" |
| 2 | Accepted sketch: direction A "cottage loaf", `assets/auntie-dot/sketch/dot-sheet.png` | decided (chair 2x check passed; Rega "ok go, all ur pick", ts 1795653224.813279, chains the sketch into the 3D, Rega judges both on one card) | `brief.md` L3-5, "Chair calls after the sketch" |
| 3 | Body map: 2.27 heads, bun top y 40, hairline y 88 (temples 112), eye line y 126 (= ears), chin 172, neck line 180, cups y 194 at x 117/183, shoulder root y 206 at X +-52, hands y 262, belly y 280, hem 316, sole 340 | decided | `sketch/body-map.md` A-C; curves `sketch/src/dot.py` L44-104 |
| 4 | Hairline: an ink edge in 3D; the side hairline curves down BEHIND the ear | decided | `brief.md` "Chair calls" 2; `sketch/notes.md` "Notes for the 3D builder" |
| 5 | Smile: small and curved; prove at 1x it does not read as a moustache or beard; thinner line if it reads dark | decided | `brief.md` "Chair calls" 3 |
| 6 | Skill card: row 23 face, row 13 Copium disc, row 24 edge, in her right hand | decided | `brief.md` "Chair calls" 4; `body-map.md` C |
| 7 | Headset: a band round the neck, one cup on each collarbone, no mic, all row 27 | decided | `brief.md` "Chair calls" 5; `body-map.md` C |
| 8 | Size: 0.9 x Kit on screen; Kit = 75 px by the Ricky method, so target 67.5 px; set by the blockout, measured as Ricky and the ATS (alone on magenta, ink included, at Kit's depth) | decided | `brief.md` L23-24, "Chair calls" 6; `assets/ricky/v1/measure.md` |
| 9 | Game camera: 26 m, pitch 42, yaw 20, fov 26, 1600x900, 1.6 px outline; Dot root turned 15 deg (net yaw 5) as Kit, Ricky, ATS | decided | `assets/ricky/v1/ingame.html` L283; `assets/ats9000/v1/ingame.html` L306 |
| 10 | Budget: 1,400 visible triangles or fewer, at most 3 non-swap meshes | decided | `brief.md` L27 |
| 11 | Palette: dress row 11 `#7A5596`, hair + bun row 23 `#FFF8EE`, skin row 15 `#F2C79E` (head, hands, legs), ink row 22 `#2B1E16`, headset row 27 `#C8C0D8`, shoes row 5 `#7A4A2E`, buttons and glints row 23, card 23 / 24 `#E9D3B4` / 13 `#F0B43C`; shade = neutral grey band (Kit's bands2, grey 178) | decided | `brief.md` L15-21; `sketch/notes.md` "Colours"; `assets/kit/toon.json` |
| 12 | Motion: idle sway +-4 deg about the feet, head lags 2 deg; talk = head roll 8 deg + her right hand up + open mouth; card = her right arm forward with the card, 2 deg lean | decided | `brief.md` L28-31; `sketch/notes.md` builder notes; `sketch/src/build.py` L430, L473-546 |
| 13 | Expressions: rest smile, talk (open D), happy (closed eyes) | decided | `sketch/dot-sheet.png` EXPRESSIONS; `dot.py` SMILE, TALK, HAPPY_EYES |
| 14 | Joins (body-sleeve, elbow, hand, head-neck, neck-body, hair-skin, bun-hair, ears, headset-body, legs-hem, card-hand) | mine to decide; decided in `direction.md` §3 | skill `SKILL.md` step 4 |
| 15 | Hardest parts | named in `direction.md` §2, solved first on the blockout | skill step 2 |
| 16 | My skill steps and tools: `direction.md` (step 1), hardest parts first (step 2), join decisions (step 4), `search.py`, `resolve.py`, `design-context.py`, `host-probe.py` (steps 4-5); outputs in `skill/` | decided, run | skill `SKILL.md`; council "Offer is not use" |
| 17 | Pipeline: reuse Ricky v1 (`build_ricky.py`, `render_ricky.py`, `make_sheets.py`, `shoot_ingame.mjs`) and the ATS v1 `ingame.html` (it already loads Kit, 3 Ghosties, Ricky and the ATS); Blender 4.3, three.js r170, Playwright | decided | brief "Reuse the working Ricky pipeline"; `skill/host.json` |
| 18 | Deliverables: turnaround, hero, sway, talk, card, silhouettes, grey, in-game + compare, lineups grass/path colour/grey with x3 and 1x crops (Kit, Ricky, Ghosties, ATS), compare-sketch, crops, measure.md (scale, hair vs eyes, smile), selfcheck.md | decided | chair's task message |
| 19 | Where Dot stands in the lineups | mine to decide (cheap to change): grass at (-2.5, 5.6) (the first pick, (-5.0, 4.0), was under the tree), path at (-2.0, 0.1), root yaw 15 | this file |
| 20 | Stop rule: an item that fails twice stops the build and is reported | decided | council "No blind iterations" |

Result: no need is missing. I start.
