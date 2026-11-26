# The Panel: sketch notes (Illustrator, 2026-11-26)

Brief: `design/acceptance/panel/brief.md`. Ready check: `ready.md`. Body map: `body-map.png`, `body-map.md`.
Sheet: `panel-sheet.png`. Explore: `explore.png`. 64 px silhouette: `silhouette-64.png`. Sources: `src/` (`panel.py`
model, `build.py` renders; run `python3 build.py` in `src/`; the SVGs are its output). Paths are relative to
`runs/jobless-roguelike/design/`. Every claim is Fact (with its source) or Opinion.

## Direction: A, "bow, flat-top, black cube" (pick)
- **Fact:** 10 thumbnails and 3 directions are on `explore.png` (front, 3/4 and the game camera with Kit in front).
- **Opinion, the reason:** the three read apart by silhouette alone (`panel-sheet.png`, 64 px silhouettes): a round
  head with two bow lobes on top (Culture Fit), a square flat-top block (Whiteboard), a plain cube lower than both
  heads (the Camera-Off One). The light table makes the black cube the strongest value in the set, so the joke ("a
  black box is on your panel") reads first.
- **Opinion, B (BMGD literal, 2 sphere heads + box) is out:** the two bare balls read apart by colour only, which the
  brief rules out (`brief.md` L18), and the box melts into a wood table (2.19:1).
- **Opinion, C (cloud hair, spikes, monitor) is out:** a monitor reads as a prop, not a person; cloud hair spreads
  beside the face (temple-rule risk); spikes break the calm toy-pawn family.
- **Tone (Opinion):** comic and kind. Culture Fit smiles and nods; Whiteboard is flat and focused, not mean; the box
  is a joke, not a threat.

## Colours (existing rows only, `seats/lena-park.md` palette table)
| Row | Hex | Use |
|---|---|---|
| 24 | `#E9D3B4` | table and chairs (one mesh): the chair call "panel-edge" |
| 22 | `#2B1E16` | the Camera-Off box; ink: outlines, eyes, brows, mouths, glasses |
| 12 | `#FFE8A6` | box icon; Culture Fit bow, headband, blouse V |
| 10 | `#C9A6D6` | Culture Fit cardigan and sleeves |
| 26 | `#2F3E5C` | Whiteboard vest; legs (hidden) |
| 8 | `#A8C4DC` | Whiteboard shirt: sleeves, collar, V |
| 25 | `#4A3226` | hair, both |
| 15 | `#F2C79E` | skin |
| 23 | `#FFF8EE` | marker body, pocket, teeth, eye glints |
| 21 | `#B23A26` | marker cap, red pen (small) |
| 9 | `#3D6B99` | blue pen (tiny) |
| 6 | `#F4A672` | Culture Fit cheeks (tiny) |

- **Chair call, the table: row 24, not row 5.** Reason (Fact, ratios from the `build.py` `ratio()` formula): the box
  is 11.11:1 against row 24 but only 2.19:1 against row 5. The box is a character whose whole read is "black", so it
  needs the light ground. Cost (Fact): row 24 is 1.12:1 against grass and 1.00:1 against path, so the table reads by
  its ink edge and the shaded front panel only (`panel-sheet.png`, lineups). See Open 2.
- **Box:** row 22 with a row 12 icon (13.34:1). Row 17 was the other choice; row 22 is the darker one.
- **Apart from the locked cast (Fact, ratios):** no big area uses rows 14, 17, 11, 7, 5, 6, 18 or 16; no row 20 or 13
  at all. Lilac 10 vs Dot's purple 11: 2.78:1 (also a different hue: light lilac vs dark plum). Navy vest 26 vs
  Ricky's suit 17: 1.27:1, so Whiteboard parts from Ricky by shape (flat-top, glasses, light-blue sleeves, no jacket
  or tie), not by value (Opinion). Shirt 8 vs Kit 14: 2.62:1.
- **Values inside the set (Fact):** lilac 10 vs hair 25: 5.58:1; bow 12 vs hair 25: 9.77:1; vest 26 vs table 24:
  7.35:1; shirt 8 vs vest 26: 5.90:1; lilac 10 vs table 24: 1.46:1 (her edge on the table is the ink line).

## Size (chair call `brief.md` L29-30)
- **Fact:** table top H 220 u = 0.733 m = 0.75 x Kit (0.977 m, `assets/kit/build_report.json`).
- **Fact:** the seated head is the Juno head, 0.32 m; Kit's head is 0.36 m (0.977 / 2.71). At the game camera: 21.1 px
  (cap top to chin) vs about 20 px for Kit by the same measure (`body-map.png` E; `src/_tmp/bodymap.json`).
- **Fact:** cap top 1.26 m, shoulders 8 cm above the table top. Kit (0.98 m) stands in front: the panel sits a head
  higher than the player (`panel-sheet.png`, game camera row).

## Face check (`panel-sheet.png`, "FACE CHECK"; numbers `src/_tmp/facecheck.json`)
- **Fact:** forehead band at 1x: 6.2 / 6.6 / 6.2 px, both people, rest; 6.1-6.4 px at the nod and the lean (rule:
  4 px or more). The lowest side hair is 6.2 px above the eye top. No hair on the forehead or beside the eyes.
- **Fact:** the Whiteboard flat-top's front edge is 1.05 px above the hairline at 1x, on the skull; it does not hang.
- **Fact:** mouths at 1x (w x h px, gap under the eyes): CF smile 5.0 x 1.0, 2.4; CF grin 7.0 x 3.0, 1.5; WB flat line
  4.5 x 0.4, 2.6; WB talk 4.5 x 2.1, 2.1.
- **Opinion:** no mouth reads as a beard at 1x (x3 crops, colour and grey). Each is small and centred under the eyes,
  with skin round it.
- **How I got there (Fact):** the first sheet failed this check. At pitch 42 the CF mouth sat on the chin line, and the
  inked V-neck under it read as a goatee. I fixed it with three changes: the mouths sit 5 u higher than Juno's, the
  V-neck and collar fills have no ink edge, and the rest head is set chin-up 8 deg. The 8 deg set showed a renderer
  fault (the full-ring hair cap drew across the eyes), so the cap is now built from culled arcs (`panel.py`
  `cap_arcs`).
- **Weak point (Fact):** the CF grin's dark lower edge touches the chin line at 1x (`face-cam-1`). It reads as an open
  mouth with a teeth band. 3D note: keep at least 1 px of skin under the grin.
- **Weak point (Fact):** the rest lines (CF smile, WB flat) are about 1 px tall at 1x, as on Juno v1. I suggest the
  Juno card-7 rule: at the game camera the idle face uses the TALK mouth.

## Motion (`panel-sheet.png`, MOTION row)
- Culture Fit nods (-8 to +6 deg at the chin, grin) and tilts (12 deg, a hand under the chin, a smirk).
- Whiteboard: marker up (forearm vertical, cap on top), then *click* (the thumb on the cap, talk mouth), then a point at
  the player (the arm forward, the marker tip toward you).
- The box: a decal swap: camera-off icon, then dark (0.5 s each), and a "muted" mic icon.
- All lean in 14 deg (box 12 deg) for "any questions for us?" (side view panel).

## For the 3D build (Viet; Opinion unless marked)
- **Meshes (4 non-swap):** 1 table + chairs (row 24, chair posts row 22); 2 Culture Fit; 3 Whiteboard (marker in the
  hand bone); 4 the box. Swaps: the icon decals, eyes and mouths, the marker poses.
- **Budget estimate:** CF about 620, WB about 560, table + chairs about 120, box about 20 visible triangles: about
  1,320 of 2,000. Legs and chair posts never show at the game camera (the front panel hides them). Cut them if the
  budget is tight.
- **Joins:** the torso ends below the table top. Only the part above H 220 is seen from the front. The forearms LIE
  on the table top, so put a toon edge on the contact.
- **Flat-top:** a bevelled block, its sides close to the head sides, so it reads as hair, not a hat. The top face is
  lit and the front shaded (`panel-sheet.png` game camera).
- **Head set:** the rest head is pitched chin-up 8 deg. Keep it: it is the face-check fix.
- **Glasses:** ink rims as a decal or thin geometry. They must stay on the eye line in 3/4.
- Sketch-only marks (Fact, not fails): the Kit cut-out is a real-render crop with a drawn shadow; the lineup set is a
  sketch estimate pasted on the real Juno v1 renders, scaled by the Dot perspective rule.

## Open
1. **Size reading (my call, flagged).** The brief says a seated head is "at about Kit's head height at the game
   camera" (`brief.md` L29). I read it as head SIZE (Kit-sized head). The other reading, head top at Kit's head top
   (0.98 m), cannot be built with the table at 0.73 m: the chin would sit below the table top. The chair can
   overrule this.
2. **The table on path (Opinion: risk).** Row 24 table vs path is 1.00:1. Panel Heights' ground is `#CFE3F0`
   (`seats/bmgd.md` L56), which is not a palette row and about 1.1:1 with the table. If the set stands on such a
   ground, the table reads by its outline only. Options for the chair: (a) keep row 24 (my pick: the box read
   matters more); (b) row 5 wood, and give the box a cream 12 edge frame so it still reads.
3. The CF grin edge touches the chin line at 1x (see "Face check"). This is a 3D note, not a sketch fail (Opinion).
4. Names on the table (folded name cards) would help the joke at card size. I left them out (fewest marks).
