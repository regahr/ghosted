# Juno the barista sketch v1: notes (Illustrator, 2026-11-26)

Files: `ready.md`, `explore.png`, `body-map.png`, `body-map.md`, `juno-sheet.png`, `silhouette-64.png`, and
`crops/` (2x crops of every panel, made by `src/crops.sh`). Sources: `src/juno.py`, `src/build.py`, and the SVGs in
`src/`. Rebuild: `cd src && python3 build.py && cd .. && sh src/crops.sh` (about 80 s).
Brief: `design/acceptance/juno/brief.md`. Paths are relative to `runs/jobless-roguelike/design/`.

## Method
- **Fact:** every shape starts as a hand-written cubic Bezier front half outline or front mark (`src/juno.py`
  `HEAD_HALF`, `CAP_HALF`, `BODY_HG`, `HAIRLINE`, `STRANDS`, `BIB`, `STRAPS`, `SKIRT`, `POCKET`, `SMILE`, `LAUGH`,
  `CUP_HALF`, `LID_HALF`). The Ricky sketch library (`assets/ricky/sketch/src/ricky.py`) lifts them onto round
  bodies, so the views, the camera tiles and the poses come from one design and agree.
- **Fact:** reused code: Dot's posed render (`assets/auntie-dot/sketch/src/dot.py`), Brett's hair cap
  (`assets/brett/sketch/src/brett.py` `hair_cap`, imported) and back-hair helper (copied, nape moved to y 142),
  and Brett's `build.py` helpers (calibration, grey formula, `ratio`, tiles, lineup, silhouette, the face numbers).
- **Fact:** the lineups sit on the real renders `assets/brett/v1/lineup-grass.png` and `lineup-path.png` (Dot v1's
  scene with Brett added: Kit, Ricky, Dot, Brett, 3 Ghosties, the ATS). Juno is scaled for her feet row with Dot's
  two measures (`auntie-dot/v1/measure.md`).
- **Fact:** one fix made during the build: at pitch 42 the face fill (on the skull surface) and the hairline ink (on
  the hair-cap surface) projected to different heights, and a dark wedge of hair showed on the forehead. The face
  fill now lies on the cap surface too (`juno.py` `cap.face_host`), and the front view did not change.
- **Opinion:** a working drawing for Viet, not final art.

## Direction: A, "the hourglass" (`explore.png`, `crops/ex-directions.png`)
- **Opinion, why:** round shoulders, a pinch at the apron tie, a flared hem. It is wide at the top AND the bottom,
  which no one in the family is (Kit capsule, Ricky bell, Dot pear, Brett wedge, ATS box, Ghostie dome). The apron
  tie makes the pinch real, not a costume trick. The high round puff gives her a dark round top that no one else
  has. It also keeps the forehead clear, because all the hair is pulled back. Holding the cup in both hands is a
  warm, calm, "for you" stance. The coffee-brown top says barista before anything else.
- B (BMGD's capsule + apron box, red apron on a light top): at the game camera it is Kit's capsule with Brett's red
  on the front and white sleeves. It reads as a Brett cousin.
- C (a column with a long apron and a red head scarf): barista-true, but at pitch 42 the scarf is a red cap over the
  face. A red top over a brown body is Brett's colour split upside down, and the column is close to the ATS box.
- Thumbnails 4 (a mug: her hand on the hip is the handle) and 5 (space buns) were the strongest runners-up. The mug
  ties up an arm that the motion needs. The buns at the top sides of the head sit close to where Ricky's headset
  cups read.

## Colours (all existing rows, `seats/lena-park.md` L20-48)
| Row | Hex | Use | Reason |
|---|---|---|---|
| 5 wood | `#7A4A2E` | top (rolled sleeves) and skirt; shoes | My pick. Coffee brown is the barista colour. It is the dark element that carries her read: 4.52:1 on grass and 5.06:1 on path (brief L18-19). It is the family's shoe row, so it is in the world already. |
| 6 cafe-wall | `#F4A672` | apron: bib, straps, skirt apron; cheeks | Chair call (brief L15). It ties her to the Job Board Cafe. Alone it sinks (1.22:1 grass, 1.37:1 path), so it sits INSIDE the brown frame: apron vs top 3.70:1. |
| 7 cafe-roof | `#D4503A` | apron tie + back bow, pocket, scrunchie, marker | Chair call (brief L15), small accents only. Brett's whole vest is row 7; on Juno it is a thin line at the waist, a ring on the puff and a pocket. Tie vs apron 2.11:1, scrunchie vs hair 2.82:1. |
| 25 hair | `#4A3226` | the puff and hair | The family hair row (Kit). Dark top: 7.25:1 on grass, 8.11:1 on path; 7.57:1 vs skin, so the hairline reads without help. |
| 15 skin | `#F2C79E` | head, ears, neck, forearms, hands | the family |
| 26 trousers | `#2F3E5C` | leggings | the family legs (Kit, Brett) |
| 23 panel | `#FFF8EE` | the cup and lid; teeth; eye glint | Chair call (brief L17). Cup vs top 7.00:1, so the cup pops against the brown arms; vs apron 1.89:1 (the ink edge carries it). |
| 22 ink | `#2B1E16` | outline, eyes, brows, mouth, strand lines, cup text | the family |
- **Fact:** shade = base x 0.85, a neutral grey multiplier (`ricky.py` `SHADE_K`).
- **Fact (computed, printed on `juno-sheet.png`):** top 5 vs Brett's vest 7: 1.76:1; vs Kit 14: 1.55:1; vs Ricky 17:
  1.84:1; vs Dot 11: 1.25:1; vs ATS 18: 2.60:1; vs Ghostie 16: 6.72:1.
- **Read apart from Brett (brief L16):** Brett is blond / red wedge / white sleeves, light at the top. Juno is a dark
  puff / brown hourglass / apricot front, dark at the top. In hue, Brett's big area is red and hers is brown with an
  apricot centre. The shared row 7 is only her thin tie line (`crops/sheet-lineups.png`).

## Face (brief L23-27; `bible.md` "Art rule: no fringe" and "Art rule: mouths")
- **Fact (`body-map.md` D):** forehead band 6.4 / 6.7 / 6.4 px at 1x (rule 4 px); in the writing beat 6.1-6.3 px.
  The side hair stays 7.1 px above the eye top, outside the eye columns. Only strand lines ON the hair.
- **Fact:** these are geometry numbers (the brow centre line); the 2.6 u brow ink is about 0.7 px wide at 1x, so the
  skin band in pixels is about 0.3-0.4 px less. It still clears 4 px.
- **Mouth:** rest is a closed smile line (calm direction, allowed by the coordinator's note). Laugh and talk use
  Ricky's style: a filled ink mouth with a white teeth band along the top edge. No thin line under a white crescent.
- **Opinion, x3 check (`crops/sheet-facecheck.png`, colour and grey, grass and path):** the rest smile is a short
  thin curve under the eyes; the laugh is a small dark mouth with a white top edge. Neither reads as a beard,
  moustache or goatee. The brows are the darkest marks on the face at 1x, and they sit well below the hairline.

## Self-check at 2x (one line per panel; crops in `crops/`)
- sheet-front: symmetric. Bib, straps, pocket and cup centred. No flaw.
- sheet-34: a thin sliver of skin shows at the far-left forehead edge, where the face fill reaches the limb.
  Builder note, not in 3D.
- sheet-side: the hairline ink and the brow and smile tips sit on the face profile (2D marks slide to the edge, as
  on Brett). The slicked side hair runs from the crown down behind the ear to the nape. Builder note.
- sheet-back: the bow and tails are centred at the back on the tie. The back hair ends at the nape (y 142). No flaw.
- sheet-handover: the red joint dots sit on the arm in the front view; the cup is on the palm, clear of the body in
  3/4 and side.
- sheet-wave: 3 frames, the hand rocks out; the cup stays in the left hand. No flaw.
- sheet-write: the cup is up at the chest and leans back toward her; the marker is in the right hand at the cup
  front; the head is down 14 deg; the eyes are down. Frame 3 shows the hand-over with the dry face.
- sheet-expressions: rest, laugh (Ricky mouth), dry, writing. The dry face is a small change (one brow, smirk);
  it is meant to be quiet.
- sheet-silhouette: an hourglass with a round ball on top, on two legs. Reads at 64 px and is new in the family.
- sheet-lineups: on real grass between Ricky and Dot, and on the path below Dot and Brett. She reads apart in colour
  and in grey (a dark puff and a dark hourglass round a mid-light apron and a white cup). On grass her puff
  overlaps the lower edge of Ricky's body: she stands in front of him (a spot choice, not a design fault).
- sheet-gamecam: rest, hand over, wave, write, next to Kit, on grass and path, x3 and 1x. The cup reads as a
  white dot; the red tie reads as a line at the waist.
- explore: thumbnails are rough on purpose. Thumb 2 uses row 7 for the cheeks (explore only).

## Open (for the chair or Rega)
1. **Size with the puff.** I counted the puff in her 75 px (brief L21 says 1.0 x Kit, nothing about hair). If only
   the body counted, she would be scaled up and stand about 85 px with the puff, taller than Brett (79 px). Viet's
   blockout sets the real scale.
2. **Budget (Opinion).** The sketch as drawn would cost about 1,600 triangles at the sketch's ring counts. The split below
   brings it to about 1,380. Viet owns the call.
3. **Apron 6 vs Dot's coat 11** in grey: both mid values near her in the grass lineup. They differ in hue and in
   shape (Dot's pear and white bun vs Juno's dark puff and hourglass).
4. **Row 7 has a UI meaning** ("roof, Morale bar fill", `seats/lena-park.md` L28). Juno IS the Morale heal node, so
   the red accent fits her role. Lena may check.
5. **The cup text font.** The card-size cup uses a hand-written font as a stand-in. The 3D decal should be Juno's
   own handwriting, set by Lena or Emil.

## Notes for the 3D builder (not sketch fails)
- **Budget:** 1,400 triangles or fewer (brief L22). Opinion, one split: body (top + skirt as one revolve, apron as
  atlas cells or vertex colour, tie as a colour band on the body) about 420; bow + tails about 60; head + cap + ears
  about 280; puff about 96 (8 x 6) + scrunchie as a colour band at the puff base (0 extra) or a low 8-sided ring
  (about 32); arms (sleeve + cuff merged, forearm, hand) about 150 each = 300; legs + shoes about 140; cup + lid
  about 70. Total about 1,380.
- **Joins:** the sleeve comes out of the body as continuous skin (as Dot and Brett); the cuff is a bulge at the elbow
  in the same mesh; the forearm and the hand are a plain ball join.
- **Hair:** the cap is slicked flat; keep its front edge at the hairline (no lip over the forehead). Two strand lines
  as decal or texture. The puff is a separate ball, top-back. The forehead band must measure 4 px or more in the
  in-game render (as Brett's `measure.md`).
- **Apron:** front only (bib, straps, skirt apron). The tie goes all the way round; the bow sits at the back.
- **Cup:** a separate prop, parented to the hand that holds it per beat. The text is a decal ("You are not a PDF."
  and the other lines); at the game camera it is just a white cup with a lid.
- **Rest:** cup in both hands at the apron. **Hand over:** her right arm forward, cup on the palm, smile. **Wave:**
  her right hand up by the shoulder, 3 frames, about 0.3 s a beat, cup in the left hand. **Write:** cup up at the
  chest in the left hand, leaning back 10 deg, marker in the right hand, head down 14 deg, eyes down; then the hand
  over.
- **Draw order:** the 2D painter sorts by part; any tiny overlap glitch in a crop is the sketch tool.
