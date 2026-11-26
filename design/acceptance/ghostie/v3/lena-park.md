Lena Park (UI/UX Lead (UI/UX Pro Max)):

# GHOSTED acceptance gate, card 2: Ghostie v3, items L1-L3

Base: `runs/jobless-roguelike/design/`. A = `assets/ghostie/`. v2 files: `A/v2/`.
SK = `~/.claude/plugins/cache/ui-ux-pro-max-skill/ui-ux-pro-max/2.15.0/.claude/skills/ui-ux-pro-max/`

## Offer

- `SK/references/quick-reference.md` `color-contrast` (3:1 non-text), `color-not-only` (value, not hue, tells the cast apart), `color-accessible-pairs`: the pass lines for L1, L2 and L3.
- My local WCAG 2.x script (sRGB to linear, relative luminance, HSV hue), a 4-connected flood fill for outline closure, and a coverage-weighted outline width scan. Run with PIL and numpy on the PNGs on 2026-11-25. I read the glTF material colours from `A/ghostie.glb` and `A/v2/ghostie.glb`.
- The brief blocked none of my tools. I did not run `search.py`: the gate needs the rules above, not a new search.
- `A/changes.md` and `fix-brief-v3.md` were read as claims only. I re-measured each one.

## Verdict

| Item | Result | Evidence |
|---|---|---|
| Shade band neutral | **PASS** | Fact: `A/ghost_toon.json` is byte-identical to `A/v2/ghost_toon.json` (diff empty). Ghost, acc and tie bands are (178, 178, 178) and (255, 255, 255): neutral, as `seats/lena-park.md` line 50 requires. |
| Shade hue within ±15° of lit | **PASS** | Fact (`A/lineup-grass.png`, ghost body mask, 2835 px): lit median `#F3E1C2` hue 38.0 (p2-p98 37.2-39.2); shade median `#E7D3B3` hue 36.9. Difference 1.1°. Same in `A/lineup-path.png` (38.0 / 36.9). `A/hero.png`: lit `#F3E3C7` hue 38.2, shade `#E8D7BA` hue 37.8 (0.4°). The builder's claim (`A/changes.md`: lit `#F3E2C3`, shade `#E7D3B3`) matches within 1 level. |
| No pink on the body | **PASS** | Fact: every pixel with hue <20° or >290° and sat >0.12 is on an accessory, an ink edge or Kit. `A/hero.png`: one cluster, x 572-793, y 406-641, 7506 px, median `#D2A1C0`: the tie strap only. `A/variants.png`: tie (x 276-426), glasses frames (x 752-863, `#DECBC3`), headset edges (x 1453-1608). `A/lineup-grass.png`: left ghost tie (x 719-727, `#D5A7BB`), glasses (x 753-764, `#C4AFA9`), ink-mixed edge px (x 815-840, `#7A6660`), Kit's red tie (x 883-886). `A/lineup-path.png`: the same clusters. No body pixel is pink. |
| Outline ≥ 1.6 px | **PASS** | Fact: `A/ingame.html` lines 187 and 195 set `outlinePx = 1.6` and `outW = outlinePx * vh / h`; `A/ingame_report.json` `outlineW_m` 0.02134 (same as v2). Measured coverage-weighted ink width, 3 ghosts: sides median 2.00 px grass, 1.96 px path; crown median 1.91 / 1.75; hem median 1.78 / 1.78. Lowest hem columns are about 1.45 px (one solid ink pixel plus a 45% blend, e.g. `A/lineup-grass.png` x 712, y 447-449), the same as v2 (min 1.43, `A/v2/lineup-*.png`). |
| Outline closed | **PASS** | Fact: flood fill of non-ink pixels from the crop border (x 680-862, y 396-500) reaches 0 body pixels of all 3 ghosts at a 50% ink threshold, on grass and on path, and on grass at 35%. On path at the strict 35% threshold it leaks at the hem bottom (x 749-843, y 469-477), where the outline meets the darker contact shadow: those pixels are 62% ink against the fixed reference. Opinion: that is anti-aliasing against the shadow, not a gap. At 8x zoom the ink is visibly closed round every ghost, arm and arm tip. |
| L1 grass | **PASS** | Fact (`A/lineup-grass.png`, ground `#BDD662`): lit body 1.26:1, shade 1.11:1, so value alone fails; the ink outline `#231001` is 11.31:1 on grass and separates them. Contact shadow present. |
| L1 path | **PASS** | Fact (`A/lineup-path.png`, ground `#EFCA8C`): lit 1.21:1, shade 1.06:1; ink outline 11.78:1. |
| L2 hero vs ghost | **PASS (hero vs ghost only)** | Fact (`A/lineup-grass-grey.png`, `A/lineup-path-grey.png`, true luminance per `A/make_sheets.py` lines 33-39): ghost lit 227, ghost shade 213, tie 185-186; Kit shirt 103, Kit hair 46; grass 203, path 207; ink 21. Ghost and Kit are 110+ levels apart. Opinion (`A/lineup-path-grey-crop-x3.png`): the three ghosts and Kit read apart at a glance. The recruiter is not built, so L2 is not proved for all three. |
| L3 GLB colours | **PASS** | Fact (`A/ghostie.glb`: 4 materials, 0 textures, 0 images; same 4 base colours as `A/v2/ghostie.glb`): ghost `#F8F4EA` = row 16 (`seats/lena-park.md` line 37); acc `#C8C0D8` = row 27 (line 48); tie `#C9A6D6` = row 10 (line 31); ink `#2B1E16` = row 22 (line 43). New meshes use only these: `acc_headset_band` acc, `acc_headset` acc + ink ring, `acc_tie` tie + ink. Outline colour `#2B1E16` (row 22) from `assets/kit/toon.json` line 53. |
| L3 toon json | **PASS** | Fact: `A/ghost_toon.json` holds band multipliers only (178 grey, 255 white), no colour. |

## Notes (Opinion, not gate items)

- The tie moved off the face centre: in `A/lineup-grass-crop-x3.png` the left ghost shows two eye dots and nothing centred below them. My v2 note (tie reads as a mouth) is closed. BMGD owns the final call.
- In `A/hero.png` and `A/variants.png` I see no ink along the tie's long sides, though `A/changes.md` claims an ink plate there. It does not change L1-L3 (tie is 185 grey against body 227). Viet and the Illustrator should check the claim.
- The headset cup in `A/variants.png` (x 1555-1610) has ink on its right side only. That is the Illustrator's item 5, not mine.
- L2 must be proved again at the recruiter gate, with Kit, ghost and recruiter together on grass.

**Overall: PASS** (L1-L3; L2 for hero vs ghost only until the recruiter is built).
