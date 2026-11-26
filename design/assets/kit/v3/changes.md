# Kit v2 to v3: what changed and which render proves it

- Date: 2026-11-25. Builder: Viet Tran seat.
- Input: the gate scores in `design/acceptance/kit/*.md` (all 5 read) and the coordinator's fix list.
- The v2 files are kept in `v2/`. The v2 renders were moved there before this build.
- Rebuild in this folder, in order:
  1. `Blender -b --factory-startup -P build_kit.py`
  2. `Blender -b kit.blend -P render_kit.py`
  3. `node shoot_ingame.mjs`
  4. `python3 make_strips.py`

## Must fixes

| # | Fix | How | Proof |
|---|---|---|---|
| 1 | L3 tie colour | The tie is now `#D4503A` (palette #7). Hair `#4A3226` (#25) and legs `#2F3E5C` (#26) are now in `seats/lena-park.md` lines 46-47. | `turn-front.png`: the tie is cafe-roof red. `toon.json` and `build_kit.py` PAL. |
| 2a | Pant hems cut into the shoes; whiskers at the crotch | The shoe now has a flat collar at 0.062 m. The trouser tube ends in a closed hem lip that stands on that collar, so the join is one flat round ring. The trousers have a flat seat disc, so the legs leave it through a flat plane, and the leg tops are closed. | `turn-back.png`, `turn-front.png`: clean round hem rings on the shoes and no whiskers. In `build_report.json`: `leg_verts_below_collar_outside_shoe` 0, `leg_verts_above_collar_inside_shoe` 0, `leg_verts_in_seat_outside_trousers` 0, `leg_verts_between_inside_trousers` 0. |
| 2b | The handle tore through the hand, and no handle shape showed | The handle is now a rounded-rectangle bar that rises 6.8 cm above the case. The fist stands upright with its long axis along the bar. The bar runs 2 cm deep inside the fist and leaves through the two narrow sides, so both handle legs show below the fist. | `turn-34.png`, `hero.png` and `turn-side.png` show a readable handle loop under the fist. In `build_report.json`: `grip_sections_inside_fist` 4, deepest 20.7 mm, 2 exit sections (4.6 mm, one per side), 2 visible sections on each side. |
| 2c | The hair ended in a vertical slab at the temple, with a light gap | The hair edge now lies 2.3 to 3.9 mm above the skin (it was 9 mm or more). The tuck ring sits 4.6 mm inside the head. The temple ends in a pointed sideburn lock, and the edge rises over the ear. The hair edge and tuck rings get a 20% outline width. The width is stored once, as the colour attribute `outline_wc` (glTF `COLOR_0`). `render_kit.py` turns it into a Solidify vertex group, and `ingame.html` reads `COLOR_0.r`. So the ink line sits on the edge, not beside it. | `turn-side.png` shows a pointed sideburn with one clean ink line and no skin sliver (checked at 4x zoom). In `build_report.json`: `hair_edge_height_above_skin_mm` 2.3 to 3.9, `hair_tuck_ring_inside_head` -4.6 mm. |
| 3 | Angular dark wedges on the shirt; a diagonal streak on the case front | The torso now has 22 columns, up from 16. The prop terminator moved to N.L = 0, so the 2-band shadow falls only where the sun does not reach, and the band no longer crosses the low-poly flank. The case is flat-shaded with a 1-segment chamfer, so each panel has one normal. | `turn-34.png`: the shirt front and flank are one clean lit area. `turn-front.png`: the case front is one flat colour with no diagonal. `toon.json` bands2 = `[[-1,178],[0.0001,255]]`. |
| 4 | V5: the visible hero must be 2,500 or fewer, face set included, measured in three.js | Faces nobody can see were culled (inside the torso, sleeves and shoes). The face parts are lighter (fans of 1 to 2 rings), the case uses a chamfer, and there are fewer rings where the profile is straight. The hero is 3 meshes plus the sprout and the active face set. | `ingame_report.json` `visibleTris`: hopeful 2,466, ghosted 2,462, rejected 2,452, focused 2,466, **offer_joy 2,481 (max)**. Blender `build_report.json` `visible_hero_max` gives the same 2,481. |

## Should fixes

| # | Fix | Proof |
|---|---|---|
| 5 | Focused eyes are now half-height ovals with a flat upper lid line. Nape locks are real: 3 points at the back hairline. | `expr-focused.png` (lidded eyes), `turn-back.png` (3 nape points). |
| 6 | The sprout base is 1.5x thicker (radius 21 mm to 31 mm). The case moved out from the leg (hand x 0.236 to 0.256 m, case 1.2 cm further out). The grip spikes are gone (see 2b). | `silhouette-64-34-x4.png`: the case is separated from the leg by background. `silhouette-64-x4.png`: thicker sprout. `turn-front.png`: no spikes at the fist. |
| 7 | Uneven stance: the case shoulder is 1 cm (about 2.5 degrees) lower, the free hand is forward with the palm open and a thumb lobe, and Kit's right foot toes out 9 degrees. The eyes are split into their own nodes `eyes_<expr>`, with the pivot on the eye line, so the game blinks with `scale.y` (`ingame.html` `kit.userData.blink(t)`). Squash stays on `bounce`. | `turn-front.png`, `hero.png`. `kit.glb` nodes: root > bounce > body > head > face_*, eyes_*, sprout. |
| 8 | `expr-gamecam-strip.png`: the 5 expressions at the 26 m follow camera, at 3x and at 1x. The badge carries a bitten "C" mark for Crunchr in shirt blue. | `expr-gamecam-strip.png`, `hero.png` (the C on the badge). |
| 9 | Kit on grass: `ingame-world-grass.png` and `ingame-world-grass-crop-x3.png`. | Those 2 files. |

## Other changes

- The outline width is now per vertex in both renderers, from one source: the `outline_wc` colour attribute.
- **Crash fix (chair note, 16:01).** Two headless runs crashed in `layerCopy_mdeformvert` (inside `Mesh.validate()`, which the glTF exporter calls) and in `layerFree_mdeformvert` at exit. The cause was my own code: a vertex group and a colour attribute were both named `outline_w` on the same mesh. The attribute call returned None and the script stopped, which left the deform-vert layer broken. The fix:
  - `build_kit.py` now writes only the colour attribute `outline_wc`, so the exported mesh has no vertex groups.
  - `render_kit.py` builds the `outline_width` vertex group from that attribute with `vertex_groups.new()` and `vg.add()`, after the mesh is final, and never exports.
  - I tested this first on a small sphere (attribute, validate, glTF export, vertex group, Solidify, clean exit). Then I ran the full build and render. There is no new crash log after 16:01.
- Both hand meshes had inward-facing normals from a left-handed frame. three.js showed them as ink-black hands; Blender hid this. Fixed by forcing a right-handed frame in `ellipsoid_frame`.
- `make_strips.py` (new) builds the game-camera strip, the card strip and the world crops.
