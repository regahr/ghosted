# Recruiter Ricky sketch v1: notes (Illustrator, 2026-11-25)

Files: `ready.md`, `explore.png`, `body-map.png`, `body-map.md`, `ricky-sheet.png`, `silhouette-64.png`, and
`crops/` (2x crops of every panel, made by `src/crops.sh`). Sources: `src/ricky.py`, `src/build.py`, and the SVGs
in `src/`. Rebuild: `cd src && python3 build.py && cd .. && sh src/crops.sh`.

## Method
- **Fact:** every shape starts as a hand-written cubic Bezier front half outline or front mark (`src/ricky.py`
  L37-90). Python lifts these onto round bodies, so the four views, the game camera, the drain, the phone pose and
  the hop all come from one design. The views therefore agree by construction.
- **Opinion:** this is a working drawing for Viet, not final art. The turnaround reads like a flat toon render.

## Picks
- **Accent: row 10 `#C9A6D6` (hq-wall, lilac)** on the headset and the tie.
  - **Fact:** it is an existing row (`seats/lena-park.md` L31). It is the locked Ghostie tie colour
    (`assets/ghostie/LOCKED.md`; sketch palette).
  - **Fact (`ricky-sheet.png` value lines, computed in `build.py` `ratio`):** vs the suit 6.42:1; vs Kit's tie
    `#D4503A` 1.98:1 (hue lilac vs red); vs the heal orange `#F2994A` 1.05:1 (hue lilac vs orange).
  - **Opinion:** the tie carries over unchanged into the Ghostie, which tells the story: his lost thread becomes
    a Ghostie. Lilac is the Recruiter HQ family, far from orange and red in hue. Row 19 (ghost-purple) was the
    other candidate, but it is dark: only about 2:1 on the suit, so it gives no value break.
  - **Risk (Opinion):** lilac and heal orange have almost the same grey value (1.05:1). They differ by hue
    only, which breaks Lena's "difference by value" rule if the two ever sit side by side. On Ricky the accent is
    a small part on a near-black body, so his whole read is dark, while the heal door is a large orange mass.
    Lena should confirm.
- **Value break vs Kit's trousers:**
  - **Fact:** suit vs Kit trousers is 1.27:1.
  - **Fact:** the fix is a row 16 shirt V (12.4:1 on the suit), a row 16 collar ring, row 16 cuffs, and the light
    accent. See the greyscale lineup in `crops/sheet-lineup.png`.
  - **Opinion:** in grey, Ricky is a near-black bell with a white V and light cups, while Kit is mid-grey. They
    separate.
- **Direction: A, bell jacket** (`explore.png`, `crops/ex-directions.png`).
  - **Opinion:** it keeps Kit's round toy-pawn family. Its own bell shape and the headset ring still read at the
    game camera. Its round top and hem drain straight into the Ghostie dome and hem.
  - B (power suit) fights the round family. C (capsule) reads as "a dark Kit".
- **Other rows (Fact, `ricky-sheet.png` palette):** hair row 25, shoes row 5, skin row 15, ink row 22. The drain
  uses rows 11 then 27. There are no new colours. Shade is the base colour x 0.85.

## What works (Opinion, each with its crop)
- The turnaround is upright and symmetric. The cups sit on the ears in every view, and the tie is centred under the
  collar (`crops/sheet-front.png`, `sheet-34.png`, `sheet-side.png`, `sheet-back.png`).
- The drain keeps the cups on the ear line and the tie on the centre line all the way to the locked Ghostie
  (`crops/sheet-drain.png`, `crops/bm-drain-map.png`).
- The phone pose shows the shoulder, elbow and wrist joints as red dots. The hand meets the right cup
  (`crops/sheet-phone.png`).
- The hop shows squash, stretch and squash, with squash on the bounce only, like Kit (`assets/kit/LOCKED.md` L35;
  `crops/sheet-hop.png`).
- The 64 px silhouette reads as a round head with headset bumps on a bell, plus two legs
  (`crops/sheet-silhouette.png`).

## Open (for the chair or Rega)
1. **Size at the game camera.**
   - **Fact:** my metric estimate puts Ricky at 67 px.
   - **Fact:** the real Kit is 72 px, and its top is 13 px above its own 1 m pole (`ghostie/v7/ingame_report.json`
     L25-27, L41). So the real Kit reads larger on screen than 0.95 m suggests.
   - I drew the tiles and the lineup at the screen target: 1.05 x Kit = 76 px.
   - Viet's blockout must measure Ricky next to the real Kit and set the scale. If 1.00 m gives about 67 px,
     Ricky will read smaller than Kit.
2. **Drain end with both parts.** The locked Ghostie has one swap part each (tie or headset), and the cap is
   800 triangles (`assets/ghostie/LOCKED.md`). The strip shows both, only to prove the mapping. Which part a drained
   Ricky keeps is the chair's or Rega's call.
3. **Drain colours.** The steps use existing rows (suit 17 -> 11 -> 27 -> 16; skin 15 -> 16). A 3D lerp between
   rows is Viet's and Lena's call.
4. **Accent vs heal orange.** They differ by hue only (1.05:1 in value). Lena should check (see Picks).

## Notes for the 3D builder (not sketch fails)
- **Joins:** a suit-coloured shoulder ball sits at each arm root (x 84/216, y 176), then the sleeve, then a row 16
  cuff ring, then the hand ball. Kit's lesson: decide skin vs separate parts in the blockout.
- **Hair:** the cap ends at the temple line (y 88) and wraps down the back to the nape. In the side view my 2D lift
  draws the temple edge as a straight line (`crops/sheet-side.png`). In 3D, curve it down behind the ear.
- **Shoulder balls:** they show as small round pads in the front and back views. Keep them soft in 3D.
- **Mic boom:** about 1 px thick at the game camera. It may vanish; that is fine.
- **Budget:** 1,400 triangles (`acceptance/checklist.md` L52).
  - **Opinion:** head + cap + quiff about 450, jacket about 250, arms with balls, cuffs and hands about 300, legs
    and shoes about 200, headset with mic about 150, tie and collar about 50. That is about 1,400, so it is tight.
    Merge the shoulder balls into the jacket first if it is over.
- **Side view:** the eye sits on the front edge, as on Kit (`assets/kit/turn-side.png`).
- **Draw order:** the 2D painter sorts parts by depth. Any small overlap glitch in a crop is the sketch tool, not
  the design.

## Self-check at 2x (one line per panel; crops in `crops/`)
- sheet-front: symmetric; cups on the ears; tie centred; the head outline is closed. No flaw.
- sheet-34: the near leg sits under the hem (fixed: draw order); the mic shows at the left cheek. No flaw.
- sheet-side: the straight temple hairline (builder note above); the eye is on the edge. No design flaw.
- sheet-back: the nape hair and the band arc are centred. No flaw.
- sheet-drain: each step is smaller and higher; the cups and tie stay on the landmarks. The step 2 head is a plain
  white dome.
- sheet-phone: the hand meets the cup. The elbow bend is clear in the front view, softer in the 3/4 view.
- sheet-hop: 3 poses, all upright.
- sheet-silhouette: it reads at 64 px.
- sheet-lineup and sheet-gamecam: Ricky on real grass next to Kit and the Ghosties, in colour and grey.
- body-map panels: the labels clear each other after the fix. The wrist row merged into "hand centre (cuff above)".
- explore: the thumbnails are rough on purpose. Direction B's three views touch at the shoulders.
