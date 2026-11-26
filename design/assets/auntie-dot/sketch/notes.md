# Auntie Dot sketch v1: notes (Illustrator, 2026-11-26)

Files: `ready.md`, `explore.png`, `body-map.png`, `body-map.md`, `dot-sheet.png`, `silhouette-64.png`, and
`crops/` (2x crops of every panel, made by `src/crops.sh`). Sources: `src/dot.py`, `src/build.py`, and the SVGs in
`src/`. Rebuild: `cd src && python3 build.py && cd .. && sh src/crops.sh` (about 45 s).
Brief: `design/acceptance/auntie-dot/brief.md` step 1. Paths are relative to `runs/jobless-roguelike/design/`.

## Method
- **Fact:** every shape starts as a hand-written cubic Bezier front half outline or front mark (`src/dot.py`
  `HEAD_HALF`, `CAP_HALF`, `BODY_PEAR`, `HAIRLINE`, `COMB`, `SMILE`, `TALK`, `POCKETS`). The Ricky sketch library
  (`assets/ricky/sketch/src/ricky.py`) lifts them onto round bodies, so all views, the camera tiles and the poses
  come from one design and agree by construction.
- **Fact:** the render is Ricky's, copied into `dot.py` with two additions: a pose transform per part (head tilt,
  sway), and per-piece culling (the band behind the neck; the back hair). The camera calibration is the ATS one
  (`assets/ats9000/sketch/src/build.py` L47-50). The grey formula, `ratio`, the lineup and the silhouette are
  Ricky's `build.py` helpers.
- **Opinion:** a working drawing for Viet, not final art.

## Direction: A, "cottage loaf" (`explore.png`, `crops/ex-directions.png`)
- **Opinion, why:** a big round head on a soft pear. The widest point is the belly, so she reads short, older and
  round, and still a toy pawn like Kit and Ricky. Her silhouette is new in the family: Kit is a capsule, Ricky a
  bell, the ATS a box, the Ghosties a dome. Folded hands on the belly say calm, kind and listening. The top-back bun
  clears the eyes and gives a clear bump on the 64 px silhouette (`crops/sheet-silhouette.png`).
- B (BMGD's capsule + bun): at the game camera it reads as "a purple Kit with a bun". Only colour tells them apart.
- C (tea cosy): very "granny", but it has no feet (breaks the pawn family). The nape bun hides behind the head at
  pitch 42, and the glasses ring the eyes at 1x (Ricky's fringe lesson).
- **Glasses: none** (my call, brief L20 allows). They crowd the eyes at 1x, and a Ghostie variant already wears
  glasses (`assets/ghostie/v7/front-glasses.png`).

## Colours (all existing rows, `seats/lena-park.md`)
| Row | Hex | Use | Source |
|---|---|---|---|
| 11 hq-roof | `#7A5596` | cardigan dress, sleeves | chair call, `brief.md` L16 |
| 23 panel | `#FFF8EE` | hair, bun, 2 buttons, eye glint; the Skill card | chair call L17 (hair); my pick for the rest |
| 15 skin | `#F2C79E` | head, ears, neck, hands, legs | chair call L18 |
| 22 ink | `#2B1E16` | outline, eyes, brows, mouth, hairline, strands, placket | chair call L19 |
| 27 ghost-faded | `#C8C0D8` | the old headset round the neck (band + 2 cups) | chair call L22 |
| 5 wood | `#7A4A2E` | shoes (as Kit and Ricky) | my pick, L20 allows |
| 13 gold | `#F0B43C` | Copium disc on the Skill card (prop) | my pick: palette "Use" says Copium |
| 24 panel-edge | `#E9D3B4` | Skill card edge (3D only) | my pick: palette "Use" says borders |
- **Fact:** shade = base x 0.85, a neutral grey multiplier (`ricky.py` `SHADE_K`).
- **Fact (computed, printed on `dot-sheet.png`):** cardigan vs grass 3.61:1; cardigan vs Ricky's suit 2.31:1;
  cardigan vs Kit's shirt 1.24:1 (hue purple vs blue); headset vs cardigan 3.36:1; hair vs skin 1.48:1;
  hair vs the Ghostie body 1.04:1; skin vs cardigan 3.77:1; headset vs hair 1.66:1.

## Self-check at 2x (one line per panel; crops in `crops/`)
- sheet-front: symmetric; cups on the collarbones, band behind the neck; buttons and placket centred. No flaw.
- sheet-34: the far cup sits behind the band end; the back hair shows as a white rim at the back edge. No flaw.
- sheet-side: the hairline runs from the temple down behind the ear to the nape as a straight diagonal; the eye is
  on the front edge (as Kit). Builder note below.
- sheet-back: the band shows across the nape with its two ends turning forward; back hair ends in a soft nape
  curve. No flaw.
- sheet-sway: three frames, feet planted, head lags. No flaw.
- sheet-talk: the hand comes up beside the shoulder; joint dots on shoulder, elbow, wrist. The upper arm is half
  behind the near cup in the front view (that is where a real arm would be).
- sheet-card: the card is in the hand, face to the player, in the front and 3/4 views. No flaw.
- sheet-expressions: rest, talk, happy. No flaw.
- sheet-silhouette: bun bump on a dome on a pear, two feet. Reads at 64 px. The arms merge with the body (folded).
- sheet-lineup: Dot on real grass with Kit, Ricky, 3 Ghosties and the ATS; colour and grey. She is shorter than Kit
  and Ricky and reads apart from them in grey (light head on a dark pear).
- sheet-gamecam and bm-gamecam: hair 6.8 px above the eyes; the cups show under the chin.
- explore: thumbnails are rough on purpose.

## Open (for the chair or Rega)
1. **Size.** Fact: my estimate is 68 px (target 67.5) at about 1.00 m. Viet's blockout must measure Dot next to the
   real Kit and set the scale, as for Ricky and the ATS.
2. **White hair near the Ghostie white.** Fact: hair row 23 vs Ghostie row 16 is 1.04:1. Opinion: at the game
   camera her white dome sits on a peach face and a purple body, so she does not read as a Ghostie
   (`crops/sheet-lineup.png`). The brief chose row 23; I kept it. Lena may want to check.
3. **Low hair-to-skin value (1.48:1).** The hairline carries an ink line and the strands are ink, so the edge reads.
   In 3D the hairline needs an ink edge (decal or outline).
4. **The mouth at 1x.** The smile is about 4 px under the eyes and only 1 px thick. Opinion: it reads as a smile
   at x3; at 1x it is a small dark mark under the eyes, like Ricky's grin. Fine for the kindest character, but Viet
   should check it does not read as a moustache.
5. **Skill card look.** Row 23 + row 24 edge + row 13 disc is my reading of the palette, not a decided card design.
   If the game's Skill card UI is designed later, the prop follows it.

## Notes for the 3D builder (not sketch fails)
- **Budget:** 1,400 visible triangles, at most 3 non-swap meshes (`brief.md` L27). Opinion: body + sleeves + hands
  + legs + shoes about 600; head + hair + bun + ears about 500; headset (band + 2 cups) about 200. The card is a prop
  shown only in the card beat. A split is in `body-map.md` E.
- **Joins:** continuous skin from the body into each sleeve at the arm root (x 90 / 210, y 206). No shoulder ball.
- **Hair:** in 3D, curve the side hairline down behind the ear to the nape (my 2D cut is a straight diagonal in the
  side view, `crops/sheet-side.png`). Keep the swept strands as an ink decal or a few modelled ridges toward the bun.
- **Headset:** the band floats just clear of the shoulder slope at the neck line; the back of it is hidden by the
  head at the game camera, which is fine (brief L24). The cups face forward and a little up. No mic.
- **Talk beat:** head roll 8 deg about the neck; her right arm only. **Card beat:** right arm forward, 2 deg lean.
  **Idle sway:** +-4 deg about the feet, head lags 2 deg.
- **Draw order:** the 2D painter sorts by part; any tiny overlap glitch in a crop is the sketch tool.
