# Card 2: the Ghostie sketch

Pictures:
- `card-2-ghostie-sketch.png`: the model sheet.
- `tie-options.png`: the 3 tie ideas at card size and at the game camera.
- `g-card2-options.png`: one panel for each option.

All files are local and unpushed. The folder is not a git repo, so there is no commit sha. The base folder is
`design/`.

## Your rules for this card
- Slack ts 1795607965.756479, (private Slack thread)
  > "ok i follow ur pick"
  That reply picked two things: sketch the Ghostie now, and add a blockout and a paint-over to the pipeline.
- Slack ts 1795604691.829739, (private Slack thread)
  > "illustrator always provide draft sketch first, then 3d artist build based on it (after sketch approved by all)"

## What it is
- The Illustrator drew a 2D sheet with hand-made curves (`assets/ghostie/sketch/`):
  - front, 3/4, side and back views;
  - the 3 variants: tie, glasses and headset;
  - the wave;
  - a 64 px silhouette;
  - game-camera thumbnails next to Kit;
  - a paint-over on the v5 3D render, which marks what Viet must fix.
- The tie is option B, "slipped": it hangs askew and off-centre. The joke is that the recruiter stopped caring.
  - Option A, centred like Kit's tie, read as a mouth at the game camera.
  - Option C, blown sideways, read as a cigarette.

## The sketch gate: 5 of 5 seats pass (verbatim)
- Illustrator (a second seat that did not draw it), `acceptance/ghostie/sketch-illustrator.md` L6: "## Verdict: PASS"
- Viet, `acceptance/ghostie/sketch-viet.md` L62: "## Re-check (2026-11-25, after BACK_BODY change): SK2 PASS". The first
  score failed only the back hem, and I redrew that one curve.
- Lena, `acceptance/ghostie/sketch-lena.md` L42: "## Re-check (Lena Park, 2026-11-25): SK3 PASS". The first score
  failed only one white stroke, and I deleted it.
- BMGD, `acceptance/ghostie/sketch-bmgd.md` L31: "## Verdict: SK4 PASS"
- Emil, `acceptance/ghostie/sketch-emil.md` L8: "## Verdict: SK5 PASS"

## Checks carried into the 3D build
- **BMGD, `sketch-bmgd.md` L33:**
  > "in the first game-camera render (`lineup-grass-crop-x3.png`), the knot top must sit at least one eye-dot height
  > below the bottom of the eye dots, and outside the right eye column."
- **Viet, `sketch-viet.md`:** the tie fits about 51-55 triangles, under a cap of 68. At the +40° wave, the arm must
  clear the tie's collar wing. Measure that in pixels.
- **Not proved:** the game-camera thumbnails are 2D estimates. The first 3D render proves them.

## Chair calls you can overrule here
1. **The ghost budget is 600 triangles, not 300** (`acceptance/checklist.md`, chair amendments 2 and 3). 24 ghosts come
   to 14.4k triangles, about 6 Kits.
2. **The off-white `#F8F4EA` reads slightly cream under the warm light.** This is accepted, because Kit and the panels
   shift the same way (Lena's pick, `acceptance/ghostie/v1/lena-park.md`).

## Options (picture: g-card2-options.png)
1. **Accept the sketch.** My pick.
   - Viet builds v6 on the v5 one-mesh body: a smooth dome, tie B and the paint-over fixes 1-3.
   - It runs the game-camera checks above.
   - Then the 5-seat 3D gate, including "matches the sketch", and the 3D card comes to you.
   - Under the no-blind-iterations rule, if any item fails twice I stop and ask you.
2. **Accept with a change.** You name it, and the Illustrator changes the sketch only (2D, no Blender pass).
3. **Redo the sketch.** You say what is wrong.
