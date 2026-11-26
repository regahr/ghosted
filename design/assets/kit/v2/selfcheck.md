# Kit v2: self-check against the acceptance checklist

- Date: 2026-11-25. Builder: Viet Tran seat (3D design lead).
- Gate: `design/acceptance/checklist.md` (Rega, Slack C0CHA2A1DM1, ts 1795594400.024269, "A1c A2b let's go").
- This is the builder's own check. The 5 seats still score the design, each on its own.
- How to rebuild everything, in this folder:
  1. `/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup -P build_kit.py` (writes kit.blend, kit.glb, toon.json, build_report.json)
  2. `/Applications/Blender.app/Contents/MacOS/Blender -b kit.blend -P render_kit.py` (writes every Blender PNG and kit_render.blend)
  3. `node shoot_ingame.mjs` (writes ingame*.png from ingame.html)

Result: **13 of 15 must items PASS, 2 FAIL** (V5 mesh count, L3 palette). Both fails come from what the brief itself asks for. The options are at the end.

## Viet Tran: shape and build

| Item | Result | Evidence |
|---|---|---|
| V1 reads correctly | PASS | `turn-front.png`, `turn-34.png`, `turn-side.png`, `turn-back.png`: a round head on a pear-shaped pawn body, 2.69 head-heights (0.977 m to the top of the hair, `build_report.json`). The legs have clear gaps between them, the free arm has space from the body, and the briefcase hangs clear of the leg. |
| V2 no cut-through, no floating parts, no gaps | PASS | Measured in `build_report.json` `checks`: briefcase against torso, legs, shoes and sleeve = 0 overlapping triangles. Free hand against torso = 0. Every face set sits 6.5 to 15 degrees below the hair edge. The sprout clears the hair by at least 4.2 mm in all 5 poses. The sweat drop floats 1.5 mm clear of the hair. The tie, collar points, lanyard and badge are projected onto the shirt (shrinkwrap). Contacts that are there on purpose: the head rests in the collar ring, the tie tucks under the collar points, and the handle passes through the mitten (the grip). Seen: no part pokes through the head in any render (the v1 fault). |
| V3 detail right at the real view size | PASS | `ingame-world.png` and `ingame-world-crop-x3.png`: Kit is 51 px tall at the 26 m follow camera (FOV 26, 1600x900). The hair, sprout, blue shirt, red tie and briefcase all read. The face and badge are card-size detail only. `expr-card-strip.png` shows the face at 160 px card size. |
| V4 toon style, clean shadows | PASS | Props use 2 bands and skin uses 3 (`toon.json` bands2 and bands3; Shader-to-RGB plus a CONSTANT ColorRamp in `render_kit.py`). Kit has no shadow map, so there is no acne, no streaks and no blotches. Seen in every turnaround and close-up: the band edges follow the form cleanly. The ground contact is an ink blob at 25% (the game's own contact shadow, Lena section 3). |
| V5 triangle budget and mesh count | **FAIL (mesh count only)** | Triangles PASS: the hero is **2,481** (body 1,431 + head 738 + sprout 84 + briefcase 236), and body + head = 2,169. The face sets add 160 to 312 each, and only 1 shows at a time. In three.js the count is also 2,481 (`shoot_ingame.mjs` log). Mesh count: 4 meshes (body, head, briefcase, sprout) plus 1 visible face set. The brief asks for `sprout` and `briefcase` as their own named nodes, so the strict "at most 3 meshes" is not met. Draw calls in the character scene = 20 (12 toon primitives because the base colours are separate materials, 4 outline hulls, 3 face primitives, 1 blob). |
| V6 in-game matches Blender | PASS | `compare-ingame.png` (3/4), `compare-ingame-front.png` and `compare-ingame-expr-ghosted.png`: Blender on the left, three.js r170 loading `kit.glb` on the right. Mean absolute difference on figure pixels is 1.8/255 (3/4), 1.8/255 (front) and 2.0/255 (ghosted close-up). About 1% of pixels differ by more than 40, all at anti-aliased outline edges. The match is by construction: both renderers read `toon.json`, and the Blender shader evaluates the same formula as MeshToonMaterial (band times sun, plus hemisphere and ambient, divided by pi, then Neutral tone mapping). |

## Illustrator: character art

| Item | Result | Evidence |
|---|---|---|
| I1 64 px silhouette: round head, sprout, briefcase | PASS | `silhouette-64.png` (front) and its 4x preview `silhouette-64-x4.png`: a round head, a curled sprout, and the case as a box with a handle below the right hand. The 3/4 version (`silhouette-64-34.png`) loses the case into the leg, so use the front silhouette. |
| I2 hand-made shapes | PASS | `hero.png` and the turnarounds show: a shirt hem lip over the trousers, sleeves that taper with a cuff lip, a collar band with 2 points, a tie with a knot and a pointed blade, hair as 4 side-swept fringe locks plus a temple line and nape locks, a curled sprout, mitten hands with a thumb bump, shoes with a flat sole and a toe, and a bevelled case with a handle, mounts and gold clasps. |
| I3 expressions differ at card size | PASS | `expr-card-strip.png` (160 px each): hopeful (oval eyes, smile, cheeks, sprout up), ghosted (dot eyes, flat line, sweat drop, sprout drooped 80 degrees), rejected-but-fine (closed ^ ^ eyes, wide smile, sweat drop, sprout bent 34 degrees), focused (half eyes, brows angled in, small offset mouth), offer-joy (big eyes with 2 highlights, open D mouth with tongue, sprout stretched to 1.32). |
| I4 [should] its own design | PASS (Opinion) | A generic pawn toy with an office kit. I know no character it copies. |

## Lena Park: legibility and access

| Item | Result | Evidence |
|---|---|---|
| L1 3:1 against grass and path, or an outline | PASS | Computed (WCAG): shirt against grass is 2.91 and against path 3.26. Legs 6.55 / 7.33, hair 7.25 / 8.11, skin 1.04 / 1.07. The ink outline is 9.9 / 11.1, and `ingame-world-crop-x3.png` shows the outline around the whole figure on the path. |
| L2 hero, ghost and recruiter differ in greyscale | PASS (computed only) | `grey.png`: Kit's main mass (the shirt) is mid grey, luminance 0.171. Lena's computed values are ghost 0.91 and recruiter 0.03, so these are 3 separate value steps. Limit: the ghost and the recruiter are not built in this pass, so no render shows all 3 together. |
| L3 colours from the 24 palette | **FAIL** | From the palette: shirt, skin, wood (shoes and case), panel (collar and badge), gold (lanyard and clasps), ink (face and outline), cafe-wall (cheeks), cafe-roof (tongue), ats-wall (sweat). Not in the palette, but fixed by the brief: hair `#4A3226`, tie `#E0533D` and legs `#2F3E5C`. They pass once Lena adds them to `seats/lena-park.md` with a reason, or once Rega swaps them for palette colours (tie to cafe-roof `#D4503A`, for example). |

## BMGD: loop and register

| Item | Result | Evidence |
|---|---|---|
| B1 matches the bible | PASS | `hero.png`: Kit, a wooden pawn toy of about 0.95 m, with a blue shirt, red tie, briefcase, lanyard badge, a sprout that carries the mood, and the 5 bible expressions (`expr-*.png`). |
| B2 comic and kind | PASS | The expressions are soft and recover: "rejected" smiles with a sweat drop, and "ghosted" is deflated, not sad-crying. Nothing mocks the player. |

## Emil Kowalski: feel

| Item | Result | Evidence |
|---|---|---|
| E1 rest pose alive and kind | PASS (Opinion) | `hero.png` and `turn-34.png`: the head tilts 5 degrees toward the case and lifts 3, the arms are not mirrored (the free hand sits a little forward), and the sprout curls. |
| E2 [should] rig allows the motion | PASS | `kit.glb` nodes: root > bounce (origin at the feet) > body > head (pivot at the neck, 0.60 m) > face_<expr>, sprout (pivot at its root). body > briefcase (pivot at the grip). Squash on `bounce` keeps the feet on the floor. Each face_<expr> carries `sprout_quat_three_xyzw` and `sprout_scale_three_y` in its extras, and `ingame.html` `setExpr()` applies them. |

## What is still weak (honest)

- The head outline shows facets in the 600 px close-ups: 22 segments, held down by the 2.5k budget. At game size it does not show.
- The mittens are plain. The thumb bump is hard to see.
- From the side, the hair still reads a little like a cap.
- `hero.png` is the rest pose, not an action pose. No animation is made (Emil's motion is still a spec).
- On the 3/4 silhouette the case merges with the leg (the front silhouette is fine).
- Kit is about 51 px tall at the real follow camera, so the face cannot be read there; the sprout and the colours carry the read. The v1 world mock had Kit at 2.2x scale. Kit here is 1.0x.
- The outline is a world-space hull: 7 mm for the sheet renders and about 1.6 px (21 mm) at the 26 m camera. The game needs to set this per camera distance, the way `renderWorld()` does.

## Open decisions (to the chair, then Rega)

V5 mesh count:
1. Count the sprout as an expression part (like the face sets), so the hero = 3 meshes. No work. **My pick.** It keeps the named nodes the brief asked for, and the sprout is the mood part.
2. Make the sprout a skinned bone inside the head mesh: 3 meshes exactly, but the glTF gets a skin and the outline hull must be skinned too.
3. Merge everything into 1 mesh with an atlas in M1 (the bible plan), and keep `sprout` and `briefcase` as bones or sockets.

L3 colours:
1. Lena adds hair `#4A3226`, tie `#E0533D` and legs `#2F3E5C` to the palette with a reason (hero identity). **My pick.**
2. Swap them for the nearest palette colours (tie to `#D4503A`, hair to wood `#7A4A2E`, legs to recruiter `#2E2C3D`). The hair would get lighter, and the legs would then share the recruiter's colour.
