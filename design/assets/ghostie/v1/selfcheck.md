# Ghostie v1: self-check (builder, Viet Tran seat)

These are builder claims. The 5 seats score the design on their own. Every claim names a file, and every join claim names a crop in `crops/`. Where a render shows a fault, I say so.

**Result by my check: V1, V2 (one hidden exception), V3, V5 and V6 pass. V4 passes with a note. L3 is open (Lena must add a colour). E2 is partial (the wave outline).**

## Viet Tran (V1-V6)

| Item | Result | Evidence |
|---|---|---|
| V1 read | PASS | `turn-front.png`, `turn-34.png` and `silhouette-64-x4.png` show a dome, a flared skirt, a 4-scallop hem and 2 flaps. The 64 px silhouette reads as a ghost with arms. |
| V2 construction | PASS, 1 hidden exception | **Eyes:** `crops/eye-on-surface-front.png`, offset 1.1-2.2 mm. **Glasses:** `crops/glasses-on-surface-front.png`, front 2.25-3.0 mm, with no body showing through the frame. **Tie:** `crops/tie-on-surface.png`, `crops/tie-side-profile.png`, front 3.0-5.8 mm. **Headset:** `crops/headset-cup-on-surface.png`, `crops/headset-band-over-crown.png`, front faces 3.3-8.5 mm. **Hem:** `crops/hem-thickness-under.png` shows the lavender rim, 20 mm. **Arms:** base ring 32-54 mm inside the body, and still inside at a ±20° swing (`build_report.json`). **Exception:** the bottom edge of the ear-cup walls sinks up to 0.57 mm into the body where it crosses the shoulder crease. It is hidden under the cup, and no crop can show it. Numbers: `build_report.json` `acc_headset_wall_faces_offset`. |
| V3 detail at real size | PASS | `lineup-grass-crop-x3.png` and `lineup-path-crop-x3.png` (ghost body 27 px, Kit 55 px). The eyes read, and the tie, glasses and headset band can just be seen. At card size: `variants.png`. |
| V4 toon | PASS, with a note | Kit's 2-band thresholds, no shadow map, so no acne. The lavender shadow shows on the hem rim and the arm undersides (`crops/hem-thickness-under.png`). Note: the 16-column body shows its corners in the outline at close-up (`hero.png`, crown), the same known limit as Kit's head. |
| V5 budget ≤ 300 | PASS | Measured in three.js (Fact: `ingame_report.json` `visibleTris`): tie 266, glasses 290, headset 298. Blender gives the same (`build_report.json`). 1 body mesh plus the parts that swap or move (eyes, 2 arms, 1 accessory). |
| V6 in-game = Blender | PASS | `compare-ingame.png` and `compare-ingame-front.png`. Mean difference 0.71/255, with 0.25% of pixels over 40 (outline edges only), from `compare_report.json`. |

## Illustrator (I1-I4)

- I1 (written for Kit; for the ghost: dome, skirt, hem): PASS. `silhouette-64-x4.png`.
- I2 designed profile: PASS. Elliptic dome, flared skirt, tab-and-V hem with a rim, tapered flaps (`turn-side.png`, `crops/hem-notch-34.png`).
- I3 variants told apart at card size: PASS for all 3 in `variants.png`. At the 26 m camera only the shape of the accessory reads (`lineup-grass-crop-x3.png`).
- I4 own design: PASS (Opinion).

## Lena Park (L1-L3)

- L1: an outline and a contact shadow separate the ghost from grass and path. `lineup-grass.png`, `lineup-path.png`.
- L2: in `lineup-grass-grey.png` and `lineup-grass-grey-crop-x3.png`, the ghosts are light grey with an ink line, and Kit is dark. The recruiter is not in this shot.
- L3: **OPEN.** The accessory colour `#C8C0D8` and the lavender shadow tint are not in Lena's 24-colour palette. Lena must add them with a reason, or name a palette colour. I did not edit `design/seats/lena-park.md`, because it is outside this card's boundary.

## BMGD (B1-B2)

There is no mouth ("a ghost never replies"), and it is opaque off-white `#F8F4EA` (bible, Ghost row). The size and the round shapes keep it a joke, not a threat (`hero.png`).

## Emil (E1-E2)

- E1 rest pose alive: partial (Opinion). The arms are slightly forward and down, and the float sines are coded in `ingame.html` `pose()`. Still frames do not show the motion.
- E2 parts for the motion: PASS for float (float node) and wave (arm pivot). **Weak:** when the arm is raised, its ink outline breaks where the arm lies against the body (`crops/arm-wave-blender.png`, `crops/arm-wave-threejs.png`). Seen end-on, the arm is a pentagon with a partial outline (`crops/arm-end-on-side.png`). At 26 m this cannot be seen. At card size it can.

## Weak points (honest)

1. The crown outline shows corners at close-up: 16 columns and 5 dome rings inside a 300-triangle budget (`hero.png`).
2. The arm outline breaks when the arm overlaps the body: wave pose and side view (crops above).
3. Under the warm world light, the lavender shadow reads pink-mauve. When the sun is behind it (`lineup-grass-crop-x3.png`), the ghost looks pinker than "off-white".
4. Its expression is neutral rather than clearly sheepish. Only 2 dots and the pose carry it.
5. The size breaks the Illustrator's 1.0 H on purpose (see `changes.md`, decision 1).
6. The headset variant has 2 triangles of headroom (298 of 300).
