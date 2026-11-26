# Ghostie v2: self-check (builder, Viet Tran seat)

These are builder claims. The seats score on their own.
- Rule (fix brief): an item with a fault I can see in a render is **not** PASS. It is marked PARTIAL or FAIL, with the file.
- Every claim names a file. v1 is in `v1/`.

## Viet Tran (V1-V6)

| Item | My read | Evidence |
|---|---|---|
| V1 read | PASS | `silhouette-64-x4.png` shows a dome, 2 round arm bumps and a hem with 2 round notches. `silhouette-64-34-x4.png` shows the near arm as a bump on the right edge. The far arm does not show in the 3/4 silhouette; it shows only as a small inked nub in `turn-34.png`. |
| V2 construction | **PARTIAL** | **Clean:**<br>- eyes: `crops/eye-on-surface-front.png`, 1.1-2.2 mm off the surface<br>- glasses: `crops/glasses-on-surface-front.png`, 1.1-1.5 mm<br>- tie: `crops/tie-on-surface.png`, front 1.5-7.7 mm, ink edge on both sides<br>- arm root ink closed: `crops/arm-root-front.png`<br>- ear cup: `crops/headset-cup-on-surface.png`<br>**Faults I can see:**<br>- `crops/headset-band-over-crown.png`: where the band crosses the crown outline, a light notch about 3 px wide breaks the inner edge of the ink line at 2x.<br>- `crops/arm-end-on-side.png`: the ink ring around the mitten is closed, but 2 thin light slivers show inside the ring, where the collar meets the arm's hull.<br>- `crops/arm-root-back.png`: a thin light sliver runs along the body outline next to the root. |
| V3 detail at real size | **PARTIAL** | At card size, `variants.png` reads as curves.<br>In the 900x1200 turns and the 1200 px hero (`turn-34.png`, `hero.png`, `compare-ingame.png`), I can still see soft corners on the crown and the shoulder, at the profile rings. They are fewer and softer than v1 (`v1/hero.png`), but they are visible.<br>At 26 m, the ghosts read as ghosts (`lineup-grass-crop-x3.png`). |
| V4 toon | PASS | Neutral 178 band, 2 bands, no acne. Lit and shade hue 38.8 / 37.6 (`lineup-grass.png` samples in `changes.md`). |
| V5 budget ≤ 450 | PASS | three.js `visibleTris`: tie 430, glasses 426, headset 442 (`ingame_report.json`). |
| V6 in-game = Blender | PASS | `compare-ingame.png`, `compare-ingame-front.png`: mean 0.75/255, 0.29% of pixels over 40, on outline edges (`compare_report.json`). |

## Illustrator (I1-I4)

- **I1: PASS.** `silhouette-64-x4.png`: dome, flared skirt, 2 round notches, 2 arms.
- **I2: PARTIAL.**
  - Better: the scallops are round (`crops/hem-notch-34.png`), the mittens are round (`turn-front.png`), the eyes have 12 sides (`crops/eye-far-34.png`), and the tie has an ink edge.
  - Still visible: soft profile corners at 1200 px (`hero.png`). The far eye is still a sliver in 3/4 (`hero.png`; fix 8 not done, see `changes.md`).
- **I3 variants: PASS at card size** (`variants.png`).
  - At 26 m: the glasses are faint and the headset reads only as a band arc and a side bump (`lineup-grass-crop-x3.png`).
- **I4:** no change from v1.

## Lena Park (L1-L3)

- **L1: PASS.** An outline and a contact shadow separate the ghost on grass and path (`lineup-grass.png`, `lineup-path.png`). The outline is 1.6 px (`ingame_report.json`).
- **L2:** the ghosts are light and Kit is dark (`lineup-grass-grey-crop-x3.png`, `lineup-path-grey-crop-x3.png`). The recruiter is not in the shot.
- **L3: PASS.** These colours are all palette rows:
  - `#F8F4EA` (#16)
  - `#C8C0D8` (#27, glasses and headset)
  - `#C9A6D6` (#10, tie)
  - `#2B1E16` (#22)

  The shade band is neutral 178.

## BMGD (B1-B2)

- **B1: OPEN. I cannot prove it.**
  - At 26 m the tie is now a vertical lilac stripe, 2-3 px wide, from the chest to the hem, below the arm line (`lineup-grass-crop-x3.png`, `lineup-path-crop-x3.png`).
  - From the elevated camera it still starts about one eye-gap below the eyes. It may still read as a long nose. That is BMGD's call.
- **B2:** comic and kind (`hero.png`).

## Emil (E1-E2)

- **E1:** the float leans 3° and rolls 5°, and the arms are asymmetric (left up, right down and forward). See `hero.png` and `turn-front.png`. Whether it reads as alive is Emil's call.
- **E2:** the float and wave nodes are kept.
  - `pose()` now keeps the rest tilt.
  - The wave crops are re-shot: `crops/arm-wave-blender.png`, `crops/arm-wave-threejs.png`.
  - The collar is fixed to the body, so in the wave pose the root line no longer follows the arm. Use the wave only in play, not on a card (Emil's v1 ruling).

## Still weak

1. Soft profile corners at 1200 px on the crown and shoulder (`hero.png`).
2. The light notch where the headset band crosses the crown ink (`crops/headset-band-over-crown.png`).
3. The slivers at the collar and hull join (`crops/arm-end-on-side.png`, `crops/arm-root-back.png`).
4. The far eye is a sliver in 3/4. Fix 8 is not done.
5. The tie may still read as a nose at 26 m (BMGD to judge).
6. The far arm is missing from the 3/4 silhouette.
7. The headset variant has 8 triangles of headroom (442 of 450).
