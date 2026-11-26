# Brett Bullet-Points sketch v1: notes (Illustrator, 2026-11-26)

Files: `ready.md`, `explore.png`, `body-map.png`, `body-map.md`, `brett-sheet.png`, `silhouette-64.png`, and
`crops/` (2x crops of every panel, made by `src/crops.sh`). Sources: `src/brett.py`, `src/build.py`, and the SVGs in
`src/`. Rebuild: `cd src && python3 build.py && cd .. && sh src/crops.sh` (about 50 s).
Brief: `design/acceptance/brett/brief.md` step 1. Paths are relative to `runs/jobless-roguelike/design/`.

## Method
- **Fact:** every shape starts as a hand-written cubic Bezier front half outline or front mark (`src/brett.py`
  `HEAD_HALF`, `CAP_HALF`, `VEST_WEDGE`, `HIPS`, `HAIRLINE`, `PART`, `GRIN`, `GRIN_LINE`, `SHIRT_V`, `COLLAR`), plus
  5 hand-placed points for the swoop (`WAVE`, smoothed). The Ricky sketch library
  (`assets/ricky/sketch/src/ricky.py`) lifts them onto round bodies, so the views, the camera tiles and the poses
  come from one design and agree.
- **Fact:** the render with per-part poses is Dot's (`assets/auntie-dot/sketch/src/dot.py`, imported). The camera
  calibration, grey formula, `ratio`, tiles, lineup and silhouette are Dot's `build.py` helpers, adapted. The lineup
  base is the real render `assets/auntie-dot/v1/lineup-grass.png` (Kit, Ricky, Dot, 3 Ghosties, the ATS).
- **Opinion:** a working drawing for Viet, not final art.

## Direction: A, "the wedge" (`explore.png`, `crops/ex-directions.png`)
- **Opinion, why:** chest out, square shoulders, narrow waist. He is wide at the TOP, the opposite of Ricky's bell
  and Dot's pear, so his silhouette is new in the family (Kit capsule, Ricky bell, Dot pear, ATS box, Ghostie
  dome). Chest out is the smug, confident posture; hands on hips is his idle. The blond swoop, red sweater vest
  over a white open-collar shirt and the floating green ring say "LinkedIn networker". The worried "secretly lost"
  face and the wink keep him likeable (brief L11-12).
- B (BMGD's capsule + halo, here in a cream vest): at the game camera it reads as "Kit in a cream jumper": the same
  capsule as Kit. Cream also sinks into the lawn and the path in value (1.35:1 and 1.20:1).
- C (the ring stands up behind the head, like the #OpenToWork photo frame): it reads at pitch 42, but as a ring
  round the head, and that is what Ricky's lilac headset band already looks like in the lineup. From the back it
  hides the whole head.
- **Halo place: above the crown, level** (brief L14 allows "round or above"). A halo sits above the head; it reads
  as an open green ellipse at pitch 42.

## Colours (all existing rows, `seats/lena-park.md` L20-48)
| Row | Hex | Use | Reason |
|---|---|---|---|
| 7 cafe-roof | `#D4503A` | sweater vest (the big area) | My pick. A cafe tone (chair's example, brief L22). Loud go-getter red. Complementary to the lawn: 2.57:1 on grass, 2.88:1 on path. Apart from Kit by hue (blue), from Ricky (3.24:1), Dot (purple), the ATS (grey) and the Ghosties (3.82:1). Apricot row 6 (1.22:1 on grass) and cream row 12 (1.35:1 on grass, 1.20:1 on path) would sink |
| 23 panel | `#FFF8EE` | shirt: sleeves, collar, V; teeth; eye glint | My pick. The crisp networker shirt. The light V and sleeves separate him from Kit in grey |
| 12 cream | `#FFE8A6` | hair: the blond swoop | My pick. Blond is the "Brett" type. Row 12 is the LinkedUp Tower wall colour, a quiet link to his LinkedIn life. A light top in grey |
| 15 skin | `#F2C79E` | head, ears, neck, hands | the family |
| 26 trousers | `#2F3E5C` | chinos | the family (Kit's trouser row): he is the player one week ahead |
| 5 wood | `#7A4A2E` | shoes | the family (Kit, Ricky, Dot) |
| 2 grass-deep | `#7FA65A` | the #OpenToWork halo, the ONE green thing, ink edge | chair call, brief L14-17 |
| 22 ink | `#2B1E16` | outline, eyes, brows, smile line, part, hairline | the family |
- **Fact:** shade = base x 0.85, a neutral grey multiplier (`ricky.py` `SHADE_K`).
- **Fact (computed, printed on `brett-sheet.png`):** vest vs grass 2.57:1, vs path 2.88:1; vest vs Kit shirt
  1.13:1, vs Ricky 3.24:1, vs Dot 1.40:1, vs ATS 1.48:1, vs Ghostie 3.82:1; halo vs grass 1.71:1, vs path 1.92:1,
  vs hair 2.31:1; shirt vs vest 3.98:1; hair vs skin 1.29:1; teeth vs skin 1.48:1.
- No grass green on the body; teal 20 and gold 13 not used.

## The grin (brief L30: "check at 1x that it does not read as a beard")
- **Fact:** three mouths were tested at the game camera (1x, nearest x4-x8):
  1. Ricky-style dark open grin with a white strip: a dark bar under the eyes = a beard (as Ricky).
  2. A white "D" grin with a 2 u ink edge: at 1x the edge and the chin line merge into a moustache-and-goatee; with
     a thin edge it reads as a WHITE beard.
  3. White teeth crescent with no edge, over an ink smile line with the corners up, plus a chin-up carriage of
     10 deg: reads as a toothy grin (`crops/bm-gamecam.png` face x6, `crops/sheet-lineup.png`). **Picked.**
- **Fact:** without the carriage, version 3 still compresses at pitch 42; the carriage turns the face 10 deg to the
  camera. So the chin-up is part of the design, not only a pose. The turnaround stays neutral.

## Self-check at 2x (one line per panel; crops in `crops/`)
- sheet-front: symmetric body; the side part and the swoop are the designed asymmetry. Collar and V centred.
  The halo is a flat bar (seen edge-on at pitch 0, as it should be). No flaw.
- sheet-34: the far ear shows a small notch where the hair cap edge meets it. Builder note.
- sheet-side: a small white sliver of the grin and the brow tip sit on the face profile (2D marks slide to the
  edge). Not in 3D: builder note. The swoop flicks up and forward; the vest is flatter (depth 0.64).
- sheet-back: back hair is a short back-and-sides cut to the nape; the swoop shows over the top. No flaw.
- sheet-idle: three frames, feet planted, frames apart. No flaw.
- sheet-like: thumb up out to the side, clear of the body in front and 3/4; joint dots on shoulder, elbow, wrist.
- sheet-bullets: 1, 2, 3 fingers; the other hand on the hip; frames apart. No flaw.
- sheet-expressions: grin, talk, wink, lost. No flaw.
- sheet-silhouette: wedge on two legs, the halo a separate bar above. Reads at 64 px. Arms close to the body.
- sheet-lineup: on real grass next to Dot, below Ricky; colour and grey. He reads apart: a green ring, a blond top,
  a red wedge. In grey: light top and V on a mid-grey wedge (Kit is mid-grey too; the ring, hair and white V tell
  them apart).
- sheet-gamecam / bm-gamecam: hair 5.7-6.2 px above the eyes; grin reads; ring open over the hair.
- bm-hands: crops of the raised hand; the arm runs off to the right of each crop (on purpose).
- explore: thumbnails are rough on purpose.

## Open (for the chair or Rega)
1. **Size with or without the halo.** I read "1.05 x Kit, measured as Ricky" as the figure: 80 px without the halo
   (target 78.75), 92 px with it. If the halo must count, the body shrinks to about 68 px, shorter than Kit.
   Fact: the estimate is 1.23 m to the swoop top (Kit 0.977 m, but Kit's model is not on the same unit; on screen
   it is 1.05 x Kit). Viet's blockout sets the scale, as for Ricky, the ATS and Dot.
2. **Row 7 has a UI meaning:** "roof, Morale bar fill" (`seats/lena-park.md` L28). The brief bans only teal and
   gold as big areas. Opinion: the vest is a costume, not a signal, and Kit's tie already uses a red. Lena may check.
3. **Vest vs Kit in grey is 1.13:1.** They differ by hue (red vs blue) and by the halo, blond hair and white
   sleeves, not by value. Dot vs Kit was 1.24:1 and passed.
4. **Halo vs grass 1.71:1.** It reads only with the ink edge. In 3D the outline pass must draw round the halo.
5. **The chin-up carriage (10 deg)** is my call to make the grin read. Emil may want to check it in the idle.
6. **The grin sits close under the eyes at 1x** (0.1 px gap). It still reads as eyes + grin at x3 and x6.

## Notes for the 3D builder (not sketch fails)
- **Budget:** 1,400 visible triangles, at most 3 non-swap meshes (brief L25). Opinion: body (vest, sleeves, hands,
  hips, legs, shoes) about 650; head (skull, hair cap, swoop, ears) about 550; halo torus about 100-150. The thumb
  and finger hands are swap meshes. Split in `body-map.md` F.
- **Rest pose:** neck 10 deg chin up. The halo stays level (counter-rotate it under a nod), follows roll.
- **Halo:** row 2, the ink outline must draw round it. No glow, no emissive.
- **Hair:** the swoop is a thick rolled tube from the part (his right) up and over to his left; keep its lowest edge
  above the hairline. The hairline and part need ink (decal or outline): hair vs skin is only 1.29:1. Fix the small
  notch where the cap meets the far ear.
- **Grin:** the teeth are a white crescent with no edge; the ink smile line under it carries the shape, corners up.
  In 3D it wraps the front of the face only (it should not show on the side profile).
- **Joins:** shirt sleeve out of the vest armhole as continuous skin (as Dot). No shoulder ball.
- **Idle:** hands on hips; puff = lean back 3 deg about the feet and rise 3 u, about 2 s a cycle; feet planted.
  **Like:** his right arm out to the side, fist at head height, thumb up, wink. **Bullets:** his right hand up
  beside the chest, a finger pops up on each bullet; the other hand stays on the hip; mouth open.
- **Draw order:** the 2D painter sorts by part; any tiny overlap glitch in a crop is the sketch tool.
