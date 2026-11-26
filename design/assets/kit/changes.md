# Kit v4 to v5: the case arm only

- Date: 2026-11-25. Builder: Viet Tran seat. Rega accepted v4 with option 2 (Slack ts 1795598749.600789): one small arm fix, then Kit is locked.
- The v4 renders, scripts and crops are in `v4/`. Only the case arm, its wrist, and how the case hangs were changed.
- Rebuild order is the same as v4 (see below).

| Fix | Change | Proof |
|---|---|---|
| Relax the case arm | The upper arm now hangs about 22 degrees out (shoulder to elbow), with a slight elbow bend. The wrist moved from (0.286, -0.012, 0.326) to (0.230, 0.100, 0.322), a little behind the hip. The sleeve is the same profile laid along a bent path: `bent_sleeve()`, with one extra ring at the elbow. | `crops/arm-front-v4-v5.png`, `crops/arm-back-v4-v5.png`: v4 angles out; v5 hangs close to the body and bends at the elbow. |
| Case plumb under the fist | `CASE_OUT` goes from 0.056 to 0 (Emil's cap: at most 0.056). The case face turns from 26 to 18 degrees off side-on. | `crops/grip-front-v5.png`, `grip-back-v5.png`, `grip-side-v5.png`, `grip-34-v5.png`, `grip-hero-v5.png`: the handle legs rise steeply out of the fist's underside, and the loop shows its open counter between the fist and the case. |
| Grip stays clean | Unchanged rule, re-checked. | `build_report.json`: handle vertices outside the fist above its equator = 0; the highest one outside is 35.1 mm below the equator. |
| 3/4 gap kept | The gap now comes from the hand sitting behind the hip and from the narrower case face. | `crops/sil34-rows-v5.png` and `crops/sil34-rows.json`: rows 48-59 each have 2 or more dark runs (background between the leg and the case). Rows 60-62 lie below the case. **The gap is thinner than in v4: 1 px in rows 50-58, where v4 had 2-4 px.** |

**Budget:** visible in three.js (`ingame_report.json`) is at most 2,480 (offer_joy), unchanged.

**Side effects to note (seen, not hidden):**
- In `turn-side.png` the case now hangs a little behind the leg.
- Because the face is turned less, the case is narrower in the front view (`silhouette-64-x4.png` still shows it as a box, with a 2-4 px gap to the leg).

**Not changed:** face, hair, sleeve cap, hems, colours, toon, outline and in-game code.

---

# (previous) Kit v3 to v4: narrow fixes

- Date: 2026-11-25. Builder: Viet Tran seat.
- Input: the v3 gate (`design/acceptance/kit/*.md`) and the coordinator's v4 list.
- The v3 files and renders are in `v3/`. Items that passed in v3 were left alone.
- Evidence rule: each fix below names a crop in `crops/`. All crops are 2x nearest-neighbour, cut around a projected 3D point (`crop_points.json`, written by `render_kit.py`). The `*-v3-v4` and `*-v2-v3-v4` files show the same window in each version.
- Rebuild in this folder, in order:
  1. `Blender -b --factory-startup -P build_kit.py`
  2. `Blender -b kit.blend -P render_kit.py`
  3. `node shoot_ingame.mjs`
  4. `python3 make_strips.py`

## Must

| # | Fix | Change | Proof |
|---|---|---|---|
| 1 | Grip: a handle leg broke through the fist face | The bar top now sits 4 mm below the fist centre. Inside the fist the bar is only ±6 to ±11 mm wide, and its legs run straight down out of the fist's underside, then splay to the case. New check: handle vertices outside the fist above its equator = **0**. The highest handle vertex outside the fist is 32.4 mm below the equator, and the fist's half-height is 35 mm (`build_report.json`). | `crops/grip-front-v3-v4.png`, `grip-back-v3-v4.png`, `grip-side-v3-v4.png`, `grip-hero-v3-v4.png`, `grip-34.png`. In v4 the fist outline stays closed, and the legs come out from under it. In the side crop, the 2 legs show their own outline ticks at the fist's lower edge. |
| 2 | Sleeve cap lost its outline | Cause: the v3 sleeve profile had dropped the shoulder-cap ring (-0.02 m, r 0.040) and culled hidden sleeve faces. v4 puts the ring back and does not cull the sleeves (`culled_hidden_faces.sleeves_in_torso` = 0). | `crops/sleeve-side-v2-v3-v4.png`: v2 closed cap, v3 two loose wedges, v4 closed outlined cap. |

## Should

| # | Fix | Change | Proof |
|---|---|---|---|
| 3 | Case out from the leg in the 3/4 silhouette | The hand is 3 cm further out (x 0.286 m). The case hangs 5.6 cm out along its face normal (v3: 1.2 cm), and its face is turned 26 degrees from side-on (v3: 35). | `crops/sil34-rows40-63.png` and `crops/sil34-rows.json`: rows 48-61 each have 2 or more dark runs, so background separates the leg from the case in every row. Row 62 is below the case. The front silhouette `silhouette-64-x4.png` still shows the case as a box. |
| 4 | Skin wedge at the temple | The hair edge now fills from the last fringe lock (azimuth 40 degrees) down to the sideburn tip, so the side hairline runs as one diagonal. The hair-edge outline width was reduced to 8%, which removed a 1-2 px skin sliver along the new edge. | `crops/temple-side-v3-v4.png`: v3 has the wedge between the fringe and the vertical sideburn; v4 has one diagonal edge with no wedge. |
| 5 | Sprout per expression at game size | Rejected now bends hard to Kit's right (-56 degrees about Y), the other way from ghosted. Focused is straight and stiff: the curl is squeezed to 40% sideways and the sprout stretched to 112%, via the new extras `sprout_sxy` and `sprout_scale_three_xyz`. Hopeful keeps its curl. | `expr-gamecam-strip.png` (top row 3x, left 1x): hopeful has the curl, ghosted lies flat, rejected leans to the other side, focused is a thin straight spike, and offer-joy is the tallest curl. |

## Budget

- Visible hero, measured in three.js (`ingame_report.json` `visibleTris`): hopeful 2,465, ghosted 2,461, rejected 2,451, focused 2,465, offer_joy **2,480 (max)**.
- The sleeve cap rings (+32) and the longer handle (+20) were paid for by removing the 2 handle mount blocks (-24), 2 side hair columns (-22) and 2 collar columns (-16).

## Not changed

- Everything that passed in v3: hems, crotch, face sets, palette, toon bands, the in-game material and outline code, and the stance (except the case-side hand, moved 3 cm out for fix 3).
- `crops/hems-back.png` is included only as a regression check. The hems were not edited.
