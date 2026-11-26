Lena Park (UI/UX Lead (UI/UX Pro Max)):

# GHOSTED acceptance gate: Kit v3, items L1-L3

SK = `~/.claude/plugins/cache/ui-ux-pro-max-skill/ui-ux-pro-max/2.15.0/.claude/skills/ui-ux-pro-max/`

## Offer

- `SK/references/quick-reference.md` `color-contrast`, `color-not-only` and `color-accessible-pairs`: the 3:1 non-text line for L1, the rule that value (not hue) separates the cast for L2, and the near-duplicate test for L3. My seat file cites them (`design/seats/lena-park.md`, Offer section).
- My local contrast script: WCAG 2.x relative luminance on the spec hexes and on pixels sampled from the v3 renders (run 2026-11-25). I also read the material colours from `kit.glb` itself, not only from `build_kit.py`.
- The brief blocked none of my tools. I did not run `search.py`, because a scoring job needs the rules above and nothing new from a search.
- `selfcheck.md` was read as a claim only. Every verdict below rests on my own reads and numbers.

## Verdict: L1 PASS, L2 PASS (on numbers; joint render still missing), L3 PASS

| Item | Result | Evidence (one line) |
|---|---|---|
| L1 | **PASS** | `ingame-world-grass-crop-x3.png`: the rendered shirt `#1467C2` is 3.46:1 on the rendered grass `#BDD662`, and the ink outline `#231001` is 11.31:1 on grass and 11.78:1 on path. At 6x zoom the outline is closed around the shirt, hand, case and shoes on grass. |
| L2 | **PASS (computed; not proved by a joint render)** | `grey.png`: skin 183, tie 124, shirt 105, case 81, hair 47, legs 42, background 234. Same value plan as v2. The ghost (L 0.906) and the recruiter (L 0.027) are still not modelled, so no render puts the three side by side. |
| L3 | **PASS** | `kit.glb` materials (read from the glTF JSON, sRGB): tie `#D4503A`, the same as `build_kit.py` line 17. All 13 materials map to palette rows #5, #6, #7, #8, #13, #14, #15, #22, #23, #25, #26. `turn-front.png` tie pixel is `#E14417` (v2: `#EB471E`), so the render moved with the source. |

## L1: hero against the ground (Fact, computed)

Spec hexes on the spec ground (same as v2; the tie row is new):

| Part | Hex | vs grass `#B5D67A` | vs path `#EBD3A6` |
|---|---|---|---|
| shirt | `#2F6FDB` | 2.91 | 3.26 |
| tie (new) | `#D4503A` | 2.57 | 2.88 |
| outline ink | `#2B1E16` | 9.90 | 11.08 |

Rendered pixels in `ingame-world-grass-crop-x3.png` (three.js, toon shading, Neutral tone mapping):

| Sample | Pixel | vs grass `#BDD662` | vs path `#EFCA8C` |
|---|---|---|---|
| outline | `#231001` | 11.31 | 11.78 |
| shirt, lit | `#1467C2` | 3.46 | 3.60 |
| shirt, shade | `#183556` | 7.70 | 8.02 |
| hair | `#492605` | 8.29 | 8.64 |
| case | `#6F3706` | 5.82 | 6.07 |
| skin | `#E3AB73` | 1.25 | 1.31 |

- **Fact:** the v2 gap is closed. `ingame-world-grass.png` places Kit with his body on grass at the grass and path edge, and `ingame_report.json` (`ingame-world-grass`) gives `kitPx` 56 and `outlineW_m` 0.0213.
- **Fact:** in the render the lit shirt passes 3:1 on grass by itself (3.46). The spec hex alone does not (2.91). The outline carries every part either way.
- **Fact:** the in-game outline is screen-constant: `ingame.html` line 156 sets it from `outlinePx = 1.6` (line 145), so at 26 m it is 0.0213 m. `toon.json` `width_m` 0.007 is the close-up value only. This answers my v2 note about the 0.007 m line being thin at game distance.
- **Opinion, not a gate item:** skin is 1.25:1 on grass, so the face and free hand read only through the outline. At 6x zoom the line along the left cheek is thinner and broken in 1 or 2 pixels where the hair edge meets the face. It reads today. Re-check it if the outline ever drops below 1.6 px.

## L2: greyscale separation

- **Fact:** `grey.png` values are within 5 levels of v2 for every part (v2: skin 182, tie 129, shirt 105, case 81, hair 47, legs 41). The tie is 5 levels darker, as the swap predicts.
- **Fact (computed in v2, unchanged):** ghost vs shirt 4.33:1; shirt vs recruiter 2.86:1; recruiter vs Kit legs only 1.27:1. Kit and the recruiter differ above the waist (mid grey vs near black), not at the legs.
- **Still unproved (Fact: no such file in `assets/kit/`):** a greyscale render of Kit, the ghost and the recruiter together, on grass, from the three.js path. Kit is the only model that exists, so this item cannot be proved by Kit alone.
- **Condition (Opinion):** L2 is a PASS for Kit. The joint greyscale render must be a must item at the ghost gate and the recruiter gate. If it fails there, the fix goes on the NPC, not on Kit.

## L3: palette

- **Fact:** `build_kit.py` lines 13-26 PAL: every value is a palette row. Tie `#D4503A` (#7), hair `#4A3226` (#25), legs `#2F3E5C` (#26).
- **Fact:** rows #25 `hair` and #26 `trousers` are in `design/seats/lena-park.md` lines 46-47, with their reasons.
- **Fact:** `kit.glb` has 13 materials and 0 textures. Their base colours (converted from linear to sRGB) are: wood `#7A4A2E`, gold `#F0B43C`, ink `#2B1E16`, white `#FFF8EE`, sweat `#A8C4DC`, cheek `#F4A672`, tongue `#D4503A`, hair `#4A3226`, skin `#F2C79E`, legs `#2F3E5C`, shirt `#2F6FDB`, panel `#FFF8EE`, tie `#D4503A`. No colour is outside the 26 rows.
- **Fact:** the badge "C" uses shirt blue (`changes.md` row 8), so no new colour.
- **Fact:** tie vs shirt is now 1.13:1 in value. The tie reads by hue (red vs blue), which deuteranopes still separate. This is the cost I accepted in v2.

## Open items for later gates (not Kit blockers)

1. Joint greyscale render (Kit, ghost, recruiter, on grass), three.js path. Owner: whoever builds the ghost.
2. Keep the in-game outline at 1.6 px or more for the ghost, which has no dark mass inside its outline (1.33:1 on path).
