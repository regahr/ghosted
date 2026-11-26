Lena Park (UI/UX Lead (UI/UX Pro Max)):

# GHOSTED acceptance gate, card 2: Ghostie v1, items L1-L3

Base: `runs/jobless-roguelike/design/`. A = `assets/ghostie/`.
SK = `~/.claude/plugins/cache/ui-ux-pro-max-skill/ui-ux-pro-max/2.15.0/.claude/skills/ui-ux-pro-max/`

## Offer

- `SK/references/quick-reference.md` `color-contrast` (3:1 non-text), `color-not-only` (value, not hue, separates the cast), `color-accessible-pairs` (near-duplicate test): the pass lines for L1, L2 and L3.
- My local WCAG 2.x script (sRGB to linear, relative luminance) on pixels read with PIL from the PNGs, and the glTF material colours read from `A/ghostie.glb`. Run 2026-11-25.
- The brief blocked none of my tools. I did not run `search.py`: scoring needs the rules above, not a new search.
- `A/selfcheck.md` and `A/changes.md` were read as claims only.

## Verdict

| Item | Result | Evidence (one line) |
|---|---|---|
| L1 | **PASS** | Fact: `A/lineup-grass.png` / `A/lineup-path.png`. Ghost lit `#F3E2C3` is 1.27:1 on grass `#BDD662` and 1.22:1 on path `#EFCA8C`; the shade band `#E9D0CB` is 1.11 / 1.06. Value alone fails. The ink outline `#231001` is 11.31:1 on grass and 11.78:1 on path, and it is closed around all 3 ghosts at 6x zoom. Outline is screen-constant 1.6 px (`A/ingame_report.json` `outlineW_m` 0.0213). Contact shadow is present. |
| L2 | **PASS (hero vs ghost only)** | Fact: `A/lineup-grass-grey-crop-x3.png` and `A/lineup-path-grey-crop-x3.png`: ghost lit 228, ghost shade 213, Kit shirt 90-103, Kit hair 47, grass 203, path 207. Ghost and Kit are about 125 levels apart. The recruiter is not built, so this proves hero vs ghost only. The grey formula is true luminance (`A/make_sheets.py` lines 34-39). |
| L3 accessory `#C8C0D8` | **PASS, added as palette row 27** | Fact: `A/ghostie.glb` has 3 materials, 0 textures: ghost `#F8F4EA` (#16), ink `#2B1E16` (#22), acc `#C8C0D8`. I added `#C8C0D8` as row 27 `ghost-faded` in `design/seats/lena-park.md`, with the reason. |
| L3 shadow tint (184, 170, 255) | **FAIL** | Fact: `A/build_ghostie.py` line 25 and `A/ghost_toon.json` set the ghost shadow band to (184, 170, 255). It renders pink, hue 10: `#E9D0CB` in `A/lineup-grass-crop-x3.png`, and `#D1BEC3` on the lower body in `A/turn-front.png`. Pink is in no palette row, it is not the Illustrator's lavender (`seats/illustrator.md` line 80, `#d9cff5`), and it is not off-white (bible line 30). |

## Does the ghost read off-white? (Fact, sampled; Opinion where marked)

Spec `#F8F4EA`: saturation 0.056, luminance 0.906.

| File | Lit body (median of 9x9 patches) | Reads as |
|---|---|---|
| `A/hero.png` (4 points) | `#F3E4C8` / `#F3E3C7` / `#F3E3C6`, sat 0.18, hue 38-39, L 0.78 | cream / beige |
| `A/variants.png` (6 points) | `#F3E3C5` to `#F3E4C8`, sat 0.18-0.19 | cream / beige |
| `A/lineup-grass.png` (3 ghosts, ~3000 px each) | median `#F2E0C2`, sat 0.20, hue 37-38 | beige; lower half `#E9D0CB`, hue 10: **pink** |

- **Fact:** it does not read off-white. The lit band is beige (3x the spec saturation), and the shade band is pink.
- **Fact:** the accessories render `#D1BEC3` to `#D2BFC6` in `A/variants.png`, 1.38-1.41:1 against the body: pinkish too.
- **Opinion:** the pink comes from the tinted band (fixed below). The beige comes from the warm key light that lights Kit as well, so every white in the world shifts the same way. On the path the beige ghost has the same hue as the sand (39 vs 38). The outline carries it, so L1 holds.
- **Fact (computed):** a neutral band of (178, 178, 178) lands at the same value as the lavender one (predicted L 0.543 vs 0.546), so the builder's value concern (ghost dropping to grass value when backlit) does not come back.

## Fix list (narrowest)

1. `A/build_ghostie.py` line 25: ghost shadow band (184, 170, 255) → (178, 178, 178), Kit's neutral band. Rebuild and re-render steps 1-4 of `A/changes.md`. Then re-sample: the shade band must have hue within ±15° of the lit band (no pink), and the outline stays ≥ 1.6 px.

Nothing else is needed for L1-L3.

## For Rega (via the chair): the lit ghost reads cream, not off-white

1. Accept the warm-lit cream as how `#F8F4EA` looks in this world (the same shift as Kit and the panels). No change. **My pick.**
2. Cool the ghost base so it lands near off-white under the warm light: a new palette row and a rebuild.
3. Add a small emissive lift to the ghost body: it reads whiter, but it flattens the toon bands.

## Notes (Opinion, not gate items)

- The neutral band goes against the Illustrator's lavender shade (`seats/illustrator.md` line 80). A real lavender under this warm light needs a strong blue band, and that drops the value (`A/changes.md` decision 3). Value wins for me.
- The accessories are faint in game (1.4:1 on the body). That is for V3 / I3. A darker faded colour would help, but row 27 is a valid choice as it stands.
- L2 must be re-proved at the recruiter gate with all three together (Kit, ghost, recruiter) on grass in three.js. Predicted: recruiter L 0.027 against Kit's shirt is 2.86:1, against the legs only 1.27:1.

**Overall: FAIL** (L3: the pink shadow tint). Fix: item 1 above, one value.
