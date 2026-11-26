# Did the Illustrator give a draft before the 3D model?

Pictures:
- `d-why.png`: v1 and v2, the two 3D versions that were modelled from a written spec.
- `d-draft-options.png`: one panel for each option.

All files are local and unpushed. The folder is not a git repo, so there is no commit sha. The base folder is
`design/`.

## Your question

Slack C0CHA2A1DM1, ts 1795604525.148009,
(private Slack thread)
> "wait, does illustrator already provide his draft before handovered to 3d artist?"

## Answer: no, there was no drawn draft. Not for the Ghostie, and not for Kit.

The Illustrator gave a written spec made of code primitives, with no drawing. The 3D builder modelled straight from
that text.

- `seats/illustrator.md` L66 (local, unpushed):
  > "Dome: half Sphere(0.4, 16, 8) + open Cylinder(0.4, 0.45, 0.35, 16). Hem: 5 Spheres(0.09) on the bottom ring (wavy edge)."
- The same file, L7:
  > "all shapes are generic primitives."
- The same file, L86, the character sheet:
  > "1920x1080, `#fde7c8`, orthographic three.js render."
  So even the sheet was a code render, not a drawing.

## Why this matters: both fails came from shape, not from detail

- v1, `acceptance/ghostie/v1/illustrator.md` L15:
  > "at card size the ghost reads as a low-poly code model, a clear step below Kit. This is the "slopped" look Rega rejected."
- v2, `acceptance/ghostie/v2/illustrator.md` L35:
  > "at card size it still reads as a low-poly code model next to Kit. The arm, the one new shape, reads as a machined peg."
- v2, `acceptance/ghostie/v2/viet-tran.md` L24:
  > "at card size this is still the "code model" look Rega called slopped."

The seats find the faults only after a full Blender build and render, and each pass takes about 15-25 minutes. A
drawing would let them judge the shape, the arms and the tie before anyone models.

## Options (picture: d-draft-options.png)

1. **Draw first, then model.** My pick.
   - The Illustrator draws a 2D model sheet: front, 3/4, side and back, the 3 variants, and a thumbnail at the 26 m
     game size.
   - The Illustrator, BMGD, Lena and Emil score the drawing, then you accept it or ask for a redo.
   - Viet models to match it. The gate gets a new must item: "the 3D model matches the accepted drawing".
   - Ricky, ATS-9000 and every later design follow the same order.
   - Kit stays locked.
2. **Finish 3D v3 first.** A 2D sheet is drawn only if v3 fails again. This is faster if v3 passes, but v1 and v2
   both failed this way.
3. **Draw first, and draw Kit too.** This is option 1, plus Kit is drawn and re-modelled if the drawing differs.
   It re-opens Kit, which you accepted on card 1 ("i follow ur pick", ts 1795598749.600789).

## What is not proved

- The Illustrator is an AI seat. Its "drawing" is a clean vector drawing (SVG to PNG) made on this machine. It is not
  a hand painting by a person.
- I have not yet seen how good its drawings are. The first sheet will show that, and you judge it.

## Status

The v3 3D build is paused. It stopped at 18:01 with some v3 renders half done. Those renders are not scored
(`assets/ghostie/PAUSED.md`). v1 and v2 are archived in `assets/ghostie/v1/` and `v2/`.
