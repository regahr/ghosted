Lena Park (UI/UX Lead (UI/UX Pro Max)):

# GHOSTED acceptance gate, card 2: Ghostie v2, items L1-L3

Base: `runs/jobless-roguelike/design/`. A = `assets/ghostie/`.
SK = `~/.claude/plugins/cache/ui-ux-pro-max-skill/ui-ux-pro-max/2.15.0/.claude/skills/ui-ux-pro-max/`

## Offer

- `SK/references/quick-reference.md` `color-contrast` (3:1 non-text), `color-not-only` (value, not hue, tells the cast apart), `color-accessible-pairs`: the pass lines for L1, L2 and L3.
- My local WCAG 2.x script (sRGB to linear, relative luminance, HSV hue) run with PIL on the PNGs, and the glTF material colours read from `A/ghostie.glb`. Run 2026-11-25.
- The brief blocked none of my tools. I did not run `search.py`: the gate needs the rules above, not a new search.
- `A/changes.md` and `A/selfcheck.md` were read as claims only. I re-measured each one.

## Verdict

| Item | Result | Evidence |
|---|---|---|
| Shade band neutral | **PASS** | Fact: `A/build_ghostie.py` lines 23-25 and `A/ghost_toon.json` `band_colors` set ghost, acc and tie bands to (178, 178, 178). Fact (measured, `A/lineup-grass.png`, ghost body mask, 1820 px): lit median `#F3E1C2` hue 38.4 (p2-p98 37.2-39.2); shade median `#E7D4B4` hue 36.9 (33.3-37.6). Difference 1.5°, limit ±15°. Same in `A/lineup-path.png` (hue 38.4 / 36.9). `A/hero.png`: lit median `#F3E3C6` hue 38.2; shade `#E7D4B5` hue 37.5. |
| No pink on the body | **PASS** | Fact: in `A/hero.png` every pixel with hue <20° or >290° (5468 px) sits in x 446-512, y 712-867: the tie only. In the lineups the 23-24 pink-hue pixels are the tie (`#BA8BA4`). The v1 pink band `#E9D0CB` is gone. |
| Outline ≥ 1.6 px | **PASS** | Fact: `A/ingame.html` line 193 sets `outW = outlinePx * vh / h` with `outlinePx = 1.6` (line 185): 0.02134 m at the 26 m camera, as `A/ingame_report.json` `outlineW_m`. Measured ink coverage across the side edges of the 3 ghosts: median 1.91 px on grass, 1.92 px on path. Ink `#231001` is closed around all 3 ghosts in `A/lineup-grass-crop-x3.png`. |
| L1 grass | **PASS** | Fact (`A/lineup-grass.png`): lit body 1.26:1 and shade 1.12:1 on grass `#BDD662`, so value alone fails; the ink outline is 11.31:1 on grass and separates them. A contact shadow is present. |
| L1 path | **PASS** | Fact (`A/lineup-path.png`): lit 1.21:1, shade 1.07:1 on path `#EFCA8C`; ink outline 11.78:1 on path. |
| L2 hero vs ghost | **PASS (hero vs ghost only)** | Fact (`A/lineup-grass-grey.png`, `A/lineup-path-grey.png`, true luminance per `A/make_sheets.py` lines 38-43): ghost lit 227, ghost shade 214, tie 152; Kit shirt 90-104, Kit hair 46-47; grass 203, path 207; ink 21. Ghost and Kit are 110+ levels apart. The recruiter is not built, so L2 is not proved for all three. |
| L3 GLB colours | **PASS** | Fact (`A/ghostie.glb`, 4 materials, 0 textures, 0 images): ghost `#F8F4EA` = row 16; acc `#C8C0D8` = row 27; tie `#C9A6D6` = row 10; ink `#2B1E16` = row 22. Outline colour `#2B1E16` (row 22) from `assets/kit/toon.json` line 53. |
| L3 toon json | **PASS** | Fact: `A/ghost_toon.json` holds only band multipliers (178 grey, 255 white). They are neutral, as `seats/lena-park.md` line 50 requires. |
| L3 tie row #10 | **PASS, allowed** | Fact: `seats/lena-park.md` line 31: row 10 `hq-wall` `#C9A6D6`, use "Recruiter HQ". It is a palette row, so L3 holds. 1.93:1 below the ghost body (row 27 is 1.59:1), and it has an ink edge. Opinion: allowed. The echo of Recruiter HQ on a ghost's tie fits the story, and the variant is told by shape. I annotated row 10 with this use. |

## Notes (Opinion, not gate items)

- The tie renders pink-mauve, not lilac: `#D3A2C1` (hue 322) in `A/hero.png`, `#BA8BA4` (hue 328) in the lineups. Fact: the base is hue 284. This is the same warm-light shift the chair accepted for the body, and it is in the tie, not the shade. Not a fail.
- In `A/lineup-grass-crop-x3.png` the left ghost's tie sits just below the eyes and can read as a mouth or a tongue at 26 m. That is BMGD's call (fix-brief item 5).
- The cream look of `#F8F4EA` stays with Rega as an open default (chair ruling).
- L2 must be proved again at the recruiter gate, with Kit, ghost and recruiter together on grass.

**Overall: PASS** (L1-L3; L2 for hero vs ghost only until the recruiter is built).
