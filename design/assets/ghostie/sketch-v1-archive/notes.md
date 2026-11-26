# Ghostie sketch v1: my own read (Illustrator, 2026-11-25)

These are builder claims. The seats score from the images. Paths are in `design/assets/ghostie/`.
I looked at every PNG at full size and shrunk to about game-camera size (whole sheets at 8-10 %).

## Tie pick: B, "slipped"
- A tie that hangs down like Kit's (knot, widening blade, symmetric V, two small collar points), but it sits
  off-centre on the arm_L (+x) side, a little askew. Story: the recruiter stopped caring.
- **Fact** `sketch/tie-options.png`, column B, card and close-up: knot at the top, blade widens, V point at the
  bottom, ink all round. Same read order as Kit's tie in the Kit column.
- **Fact** `sketch/tie-options.png`, column B, game camera x3 with the dashed mouth zone: the zone under the two
  eye dots is empty. The tie is a small lilac mark next to the arm root.
- **Opinion** B passes both tie tests. It is the only option that does.

## Why not A or C
- **A (centre, like Kit). Fact** `tie-options.png` column A, game camera x3: a lilac and ink bar sits centred
  under the eye dots, inside the dashed mouth zone. **Opinion:** it reads as an open mouth or a tongue. It fails
  the no-mouth rule (`design/bible.md` line 30). My earlier pick (A) was wrong for this camera.
- **C (blown aside). Fact** `tie-options.png` column C: the blade lies flat in the air at eye height, beside the
  face. **Opinion:** at card size it is still close to the flag / horn read that failed v1-v5. At the game camera
  it reads as a cigarette. It also sits where arm_L waves up (+40 deg), so they would collide.

## What works
- **Opinion** `sketch/ghostie-sheet.png`, turnaround: one smooth dome, 3 soft hem lobes seen from the front, arms
  grow out of the side with one closed outline. The views share the crown, eye, arm-tip and hem guide lines.
- **Fact** `ghostie-sheet.png`: only 4 character colours (rows 16, 27, 10, 22) plus a flat neutral shade tint.
- **Fact** `sketch/silhouette-64.png`: reads as a ghost at 64 px (dome, two flaps, wavy hem).
- **Opinion** `ghostie-sheet.png`, game camera row: tie, glasses and headset are told apart by shape, and all
  three keep the area under the eyes empty. They sit at the same size as the v5 ghost next to Kit.
- **Opinion** `sketch/paintover-v5.png`: the hero and the tie panel read as a tie once the v5 tie is erased and B
  is painted at card scale. The crease and the pale wedge are painted out, so Viet sees the target.

## What does not work yet (honest)
1. **Side view arm. Opinion** `ghostie-sheet.png`, SIDE: the arm seen end-on is a closed oval with a shade. At
   small size it can read as a hole or a pocket. This is the weakest drawing on the sheet. In 3D the hull will
   draw this loop anyway, so I kept it closed rather than draw an open hook.
2. **Game camera thumb is an approximation. Fact** `src/ghost.py` `thumb()`: it is my front view, squashed to
   86 % for the 42 deg pitch. It does not model the 20 deg yaw. **Opinion:** the real yaw turns the +x side
   (tie side) further from the centre, so the real read should be safer than my thumb. Viet's first render must
   prove it in `lineup-grass-crop-x3.png`.
3. **B at the game camera. Opinion** `tie-options.png` column B x3: the mark is diagonal and close to the right eye
   column. A strict judge could call it a tear streak. It is not centred and not a mouth.
4. **Wave pose. Fact** `src/ghost.py` `FRONT_BODY_WAVE`: at +40 deg the arm_L tip reaches about the bottom of the
   eye dots (tip top y about 163, eye bottom 163). The rest-pose rule (tips below the eyes) holds only at rest.
   Emil to confirm this is fine for a 750 ms beat.
5. **Tie budget is an estimate. Opinion** `ghostie-sheet.png`, TIE B BUILD SPEC: 60-80 tris with the ink plate
   and the collar. Viet must confirm against the 90 limit. The collar points are optional; drop them first if the
   budget is tight (knot + blade + V still read).
6. **Paint-over is on raster. Fact** `paintover-v5.png`: the old tie was erased by a colour mask and refilled
   with the sampled lit tone (`#F3E3C6` from `v5/hero.png`); the outline where the old tip crossed it is
   redrawn by hand. Small seams can show at 400 % zoom.
7. **Facets. Opinion** `paintover-v5.png`, mark 5: the v5 dome and hem show flat polygon corners at card size.
   My sketch is smooth. Viet decides if the budget allows smoothing.

## Marks for Viet (`paintover-v5.png`)
1. Remove the ink crease from the near arm root (hero; all three variant panels).
2. Fill the pale root wedge with one flat body tone.
3. Close the hem hook / underside ink under the near arm on the outline.
4. Replace the tie with B (spec on `ghostie-sheet.png`).
5. Clean-up only: round glasses rims, oval headset cup. Shapes kept.

## Sources and rebuild
- `src/ghost.py`: every shape as a hand-written cubic Bezier path. `src/build.py`: tie options and sheet.
  `src/paint.py`: paint-over. Run `python3 build.py tie sheet` then `python3 paint.py` in `src/`.
- `src/*.svg`: the SVG source of each PNG and each pasted tile. Rendered with `magick` (MSVG). MSVG drops group
  transforms after a text or rect, so `svg_doc()` writes those last; the drawing is unchanged.
