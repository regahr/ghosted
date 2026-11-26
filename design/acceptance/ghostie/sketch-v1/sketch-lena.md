# Ghostie sketch v1: SK3 (Lena Park, 2026-11-25)

Item: SK3, `acceptance/checklist.md` line 25. I judged it with the ui-ux-pro-max colour and contrast rules. The palette is in `seats/lena-park.md`, lines 21-48.

## Verdict: FAIL (one stray colour; the fix is one line)

## Colours in the SVG sources (Fact: every hex counted with grep)

| Hex | Where | Row | Verdict |
|---|---|---|---|
| `#F8F4EA` | body | 16 (line 37) | ok |
| `#C8C0D8` | glasses, headset | 27 (line 48) | ok |
| `#C9A6D6` | tie | 10 (line 31) | ok |
| `#2B1E16` | ink, eyes, outline, contact shadow at 16-18 % | 22 (line 43) | ok |
| `#EAE6DC` | shade band | body x 0.944 / 0.943 / 0.940 per channel | ok: neutral, see below |
| **`#FFFFFF`** | **side-view arm highlight, stroke 3: `src/ghost.py` line 280, in `ghostie-sheet.svg`** | **none** | **FAIL** |
| `#FDE6C8`, `#1D63C8`, `#BDD662`, `#FFFFFF` (PICK label, `build.py` line 107) | card ground, note marks, thumb grass, UI label | n/a | ok: not character colours |

- The shade is neutral. **Fact:** each channel is the body x 0.94 (spread 0.003), so it has no hue shift. This meets the rule at `seats/lena-park.md` line 50.
- **Fact:** the sheet label says "x178/255", but the tint drawn is x 0.944 (about 241/255). **Opinion:** this is not an SK3 fail, because the 3D toon ramp sets the band. Fix the label so that Viet does not copy the wrong value.
- **Fact:** the white stroke is 1.10:1 against the body. **Opinion:** it adds nothing at game size. But it is a fifth character colour, and the sheet itself says "palette rows 16, 27, 10, 22 only".

## Value (Fact: computed, WCAG relative luminance)

| Pair | Ratio |
|---|---|
| tie on body / on shade | 1.93 / 1.70 |
| tie on ink edge | 7.62 |
| accessory (27) on body | 1.59 |
| body on grass `#B5D67A` / path `#EBD3A6` | 1.49 / 1.33 |
| body on thumb grass `#BDD662` | 1.48 |
| ink outline on grass / path / grass-deep | 9.90 / 11.08 / 5.77 |

- **Opinion:** the tie reads against the body through its closed ink edge (7.6:1) and its lilac hue step. This is as intended in row 10 (line 31). In the x3 thumbnails, the tie B mark is visible next to the arm.
- **Opinion:** in the game-camera thumbnails (`ghostie-sheet.png`, GAME CAMERA x3), all three ghosts separate from the grass. The separation comes from the ink outline and the contact shadow, not from the body value (1.48:1). This matches the v3 3D result (`acceptance/ghostie/v3/lena-park.md` lines 24-25).
- **Fact:** the thumbnails use the sampled render grass `#BDD662`, not row 1 `#B5D67A`. No thumbnail shows the path. The computed path values (ink 11.08:1) cover the path case. These are 2D estimates, not renders, so Viet's lineup must prove the path case in 3D.

## Narrowest fix

Delete `src/ghost.py` line 280 (the `#FFFFFF` stroke on the side-view arm). Then run `python3 build.py sheet` again. Nothing else changes. (Optional: change the sheet's shade label to match the tint drawn.)

## Re-check (Lena Park, 2026-11-25): SK3 PASS

- **Fact:** `src/ghostie-sheet.svg` has 7 hex values only: `#F8F4EA` 25, `#2B1E16` 115, `#C9A6D6` 16, `#C8C0D8` 8, `#EAE6DC` 10, `#1D63C8` 23 (notes), `#FDE6C8` 1 (card). No `#FFFFFF` (grep count). The arm stroke is gone (`diff src/ghost.py.bak src/ghost.py`: old line 280 removed). In `ghostie-sheet.png`, the side-view arm box (1120,413)-(1189,496) holds only `#F8F4EA`, `#2B1E16`, `#EAE6DC` and blue guide-line anti-aliasing. Pure-white pixels in the PNG: 33,337, all inside (40,1340)-(386,1596), the 64 px silhouette test tile backdrop (`src/build.py` line 281). That is a test ground, not a character colour.
- **Fact:** the label now reads "drawn here as a light x0.94 tint" (`src/build.py` line 206, and in the SVG). The drawn tint is `#EAE6DC` / `#F8F4EA` = 0.944 / 0.943 / 0.940 per channel. The label matches.
- **Fact:** the back hem change (`BACK_BODY`, `src/ghost.py` lines 284-294) changes the path only. Its fill and stroke are still `BODY` and `INK`.
- **Opinion (no fail):** the PNG renders sheet text as pure `#000000` rather than the ink `#2B1E16`. This is UI text, not a character colour. The comment at `src/ghost.py` line 14 says "x 0.945". The measured value is 0.940-0.944. That is cosmetic and needs no change.
