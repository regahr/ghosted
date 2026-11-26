# Card 1: Kit, the Applicant (v4)

Pictures:
- `card-1-kit.png`: the design.
- `k-options.png`: one panel for each option.

All files are local and unpushed. The folder is not a git repo, so there is no commit sha. The base folder is
`design/`.

## Your rule for this card

Slack C0CHA2A1DM1, ts 1795594400.024269, (private Slack thread)
> "A1c A2b let's go"

That reply chose two things:
- A1c: the seats score each design first, then you accept it or ask for a redo.
- A2b: the final art is modelled in Blender and exported to the game.

## How Kit got here

| Version | Gate result | Why |
|---|---|---|
| v2 | FAIL. 3 seats passed, 2 failed. | Viet: the handle tore through the hand, the trouser hems cut into the shoes, the shirt showed angular shading, and Kit was over the 2,500-triangle limit. Lena: the tie red was not the palette red. |
| v3 | FAIL. 4 seats passed, 1 failed. | Viet: a handle leg poked through the fist, and the sleeve lost its shoulder line. |
| v4 | **PASS. 5 of 5 seats.** | The scores are in `acceptance/kit/*.md`. |

## The scores (verbatim)

- **Viet, `acceptance/kit/viet-tran.md` L39:** "**Overall: PASS.** All six must items pass. Both v3 faults are gone in every
  view, and the 3/4 case gap now shows in the silhouette."
- **Illustrator, `acceptance/kit/illustrator.md` L18:** "**Overall: PASS** (I1, I2, I3 must: pass. I4 should: pass.)"
- **Emil, `acceptance/kit/emil-kowalski.md` L28:** "Kit v4 **PASSES** E1 (must) and E2 (should)."
- **Lena, `acceptance/kit/lena-park.md`:** PASS on v3, and it carries over. v4 changed no colour.
- **BMGD, `acceptance/kit/bmgd.md`:** PASS on v3, and it carries over. v4 changed no role or tone.

## What is in the model

- The visible model is at most 2,480 triangles, with the active face included. The limit is 2,500.
- It has 3 meshes.
- The same `kit.glb` file looks the same in Blender and in the game engine. The mean difference is 2.0 to 2.2
  out of 255 (`assets/kit/compare_report.json`).

## Known weak points

1. **The case arm looks stiff.** Two seats flagged it:
   - Illustrator, L28: "the case arm now hangs about 30-35 degrees out from the body (v3: about 20 degrees ...).
     Opinion: the arm reads as stiff and held out."
   - Emil, L17: "this is a pass with less margin than v3."
2. **At the real game camera, the faces cannot be read.** BMGD, `acceptance/kit/bmgd.md` L24: "The faces do not
   read at 1x at all." So at that size the sprout carries the mood.
3. **The head outline shows flat facets in close-ups.** The triangle budget is used up: 2,480 of 2,500.
4. **The builder's notes were not fully reliable.** In v2 and v3, its notes claimed 3 fixes that the renders did
   not show. From v4, each claimed fix must come with a crop image, and the seats judged from the images only.

## Options (picture: k-options.png)

1. Accept as is.
2. **Accept, with a small fix to the arm.** My pick.
3. Redo: you say what is wrong.

**My pick: 2.**
- The arm fix is small and two seats named it.
- Only the arm and the case move, so Viet, the Illustrator and Emil check them again.
- Then Kit is locked, and the before and after go on the next card.
