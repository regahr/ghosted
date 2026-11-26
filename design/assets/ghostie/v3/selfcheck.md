# Ghostie v3: self-check (builder, Viet Tran seat)

- These are builder claims; the seats score on their own.
- Rule: a fault I can see in a render means the item is not PASS. Every claim names a file.
- The V5 mesh count is checked, as well as the triangles.

## Viet Tran (V1-V6)

| Item | My read | Evidence |
|---|---|---|
| V1 read | PASS | `silhouette-64-x4.png`: dome, 2 drooping arm flaps below mid-height, 5-scallop hem with 2 front notches. `silhouette-64-34-x4.png`: the near arm breaks the right edge. The far arm does not show in 3/4. |
| V2 construction | **PARTIAL** | **Clean:**<br>- eyes (`crops/eye-on-surface-front.png`)<br>- glasses (`crops/glasses-on-surface-front.png`)<br>- tie (`crops/tie-on-surface.png`)<br>- band under the crown ink with no second line (`crops/headset-band-over-crown.png`)<br>- hem left side in `hero.png`<br>**Faults I can see:**<br>1. `crops/arm-root-front.png`: where the flap leaves the body, the body's ink line steps out around the flap root. A pale sliver shows between the body ink and the flap's lower ink stroke.<br>2. `crops/arm-end-on-side.png`: the flap has ink on its outer edge only, and a thin ink stroke starts inside the body face at the root.<br>3. `variants.png`, every panel, under the near arm at the hem (about x 335 / 785 / 1235, y 380): a small ink hook. In the headset panel it is a thin-lined point.<br>4. `crops/headset-cup-on-surface.png`: a thin pale sliver inside the ink on the right edge of the cup. |
| V3 detail at real size | **PARTIAL** | At card size (`variants.png`) the crown and shoulders read as curves.<br>In `hero.png` at 1200 px the crown is smooth, and I see no corners on the crown arc. The 3 hem faults in V2 above are visible at card size.<br>At 26 m (`lineup-grass-crop-x3.png`), see B1 and the arm note under I2. |
| V4 toon | PASS | Neutral 178 band; lit/shade hue 38.8 / 36.9 (`lineup-grass.png` samples in `changes.md`). |
| V5 budget and meshes | PASS | **Triangles** in three.js (`ingame_report.json`): tie 580, glasses 528, headset 580, all ≤ 600.<br>**Meshes:** 3 non-swap (body, arm_L, arm_R); the glTF mesh list is in `changes.md`. |
| V6 in-game = Blender | PASS | `compare-ingame.png`, `compare-ingame-front.png`: mean 0.76/255, 0.29% of pixels over 40, on outline edges. |

## Illustrator (I1-I4)

- **I1: PASS.** `silhouette-64-x4.png`.
- **I2: PARTIAL.**
  - Better: the crown and shoulders are round (`hero.png`), the notch tops are curves (`crops/hem-notch-34.png`), the arms are tapered flaps with round tips (`turn-front.png`), and the frames are 8- and 12-sided (`variants.png`).
  - Still faulty: the hook at the hem under the near arm (`variants.png`) and the arm-root sliver (`crops/arm-root-front.png`).
  - At 26 m the arm flaps sit about level with the eye dots (`lineup-grass-crop-x3.png`, left ghost: flaps at y≈1005, eyes y≈1008 in my composite). The top-down camera drops the eyes as far as I lowered the arms. Whether they still read as ears is the Illustrator's call; I cannot prove they do not.
- **I3: PASS at card size** (`variants.png`). At 26 m: the tie is a diagonal stripe over the shoulder, the glasses are faint, and the headset is a band arc plus a side bump (`lineup-grass-crop-x3.png`).
- **I4:** the arms droop below mid-height, there are 5 scallops (not 3 points), and the hem corners curl in (`silhouette-64-x4.png`). This is the Illustrator's call.

## Lena Park (L1-L3)

Unchanged rules, all kept:
- **L1:** outline plus contact shadow (`lineup-grass.png`, `lineup-path.png`).
- **L2:** greyscale lineups re-shot (`lineup-grass-grey-crop-x3.png`).
- **L3:** palette rows #16, #27, #10, #22 only, and a neutral band.

## BMGD (B1-B2)

- **B1 test, by my read: met.** In `lineup-grass-crop-x3.png` and `lineup-path-crop-x3.png`, the left ghost shows 2 eye dots. The tie is a diagonal lilac stripe on the upper right of the body, going over the shoulder; nothing sits centred below the eyes. BMGD judges.
- **B2:** comic and kind (`hero.png`).

## Emil (E1-E2)

- The roll is flipped to +5° on three.js z (`ghostie.glb` float quaternion z +0.0436), so the arm_L side and the raised arm add up (`turn-front.png`, `hero.png`).
- `pose()` still composes the yaw on top of the rest tilt.
- The wave crops were re-shot: `crops/arm-wave-blender.png`, `crops/arm-wave-threejs.png`.

## Still weak

1. The hook or point at the hem under the near arm (`variants.png`).
2. The arm-root sliver (`crops/arm-root-front.png`) and the root stroke seen end-on (`crops/arm-end-on-side.png`).
3. The pale sliver on the cup's right edge (`crops/headset-cup-on-surface.png`).
4. At 26 m the arm flaps sit about level with the eyes (`lineup-grass-crop-x3.png`). The ear read is open.
5. The far arm does not show in the 3/4 silhouette (`silhouette-64-34-x4.png`).
6. Headroom: 20 triangles for the tie and headset variants (580 of 600).
