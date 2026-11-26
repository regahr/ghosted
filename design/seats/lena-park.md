Lena Park (UI/UX Lead (UI/UX Pro Max)):

# GHOSTED: world palette, contrast, colour-blind safety, signs

SK = `~/.claude/plugins/cache/ui-ux-pro-max-skill/ui-ux-pro-max/2.15.0/.claude/skills/ui-ux-pro-max/`

## Offer

- `SK/references/quick-reference.md` lines 9, 18, 125 (`color-contrast`, `color-not-only`, `color-accessible-pairs`): the pass lines below (4.5:1 text, 3:1 large text, no meaning by colour only).
- `SK/data/ux-guidelines.csv` lines 37-38: same rules, severity High.
- `SK/data/colors.csv` (`search.py "game warm playful toy" --domain color`): "Casual Puzzle Game" reward gold and "Pet Tech" warm orange plus blue. Start point; I tuned each hex to the mock.
- `SK/references/pro-rules.md` line 64, Pre-Delivery Checklist: use at gate 6.5 on the HUD.
- `search.py --stack threejs "palette atlas toon"`: 0 results (Fact, run 2026-11-25). Atlas and toon notes are my fallback.
- All ratios: local script, WCAG 2.x formula, Vienot deuteranopia and protanopia matrices. The brief blocked none of my tools.

## 1. Master palette: 24 swatches

Atlas: 256 px, 8 x 8 cells of 32 px; UVs point at cell centres (Opinion). Shade comes from `MeshToonMaterial` with a 2-step `gradientMap` (Fact: 2 bands for props, `runs/jobless-roguelike/seats/viet-tran.md` line 28). Do not paint shade into the atlas.

| # | Group | Name | Hex | Use |
|---|---|---|---|---|
| 1 | Ground | grass | `#B5D67A` | lawn |
| 2 | Ground | grass-deep | `#7FA65A` | alternate lawn, tree crowns |
| 3 | Ground | path | `#EBD3A6` | roads, plaza |
| 4 | Ground | plinth | `#E59F64` | board edge |
| 5 | Ground | wood | `#7A4A2E` | trunks, doors |
| 6 | Cafe | cafe-wall | `#F4A672` | Job Board Cafe |
| 7 | Cafe | cafe-roof | `#D4503A` | roof, Morale bar fill |
| 8 | ATS | ats-wall | `#A8C4DC` | ATS Tower (cold) |
| 9 | ATS | ats-roof | `#3D6B99` | roof, glass bands |
| 10 | HQ | hq-wall | `#C9A6D6` | Recruiter HQ; Ghostie tie (annotated 2026-11-25 at the Ghostie v2 gate: 1.93:1 below the ghost body, one step darker than #27 so the tie reads with its ink edge; the echo of Recruiter HQ fits the story. Never use this colour alone to mean "recruiter" in the HUD.) |
| 11 | HQ | hq-roof | `#7A5596` | roof, awnings |
| 12 | LinkedUp | cream | `#FFE8A6` | tower walls, windows, sign boards |
| 13 | LinkedUp | gold | `#F0B43C` | tower roof, Copium, offer glow |
| 14 | Chars | hero-shirt | `#2F6FDB` | hero body |
| 15 | Chars | skin | `#F2C79E` | heads, hands |
| 16 | Chars | ghost | `#F8F4EA` | ghost body |
| 17 | Chars | recruiter | `#2E2C3D` | suit |
| 18 | Chars | robot | `#8E9BA8` | ATS robot |
| 19 | Accent | ghost-purple | `#6B3FC9` | "GHOSTED x9", ghost trail |
| 20 | Accent | teal | `#2FB8AE` | reply received (never alone) |
| 21 | Accent | red-ink | `#B23A26` | warning text |
| 22 | UI | ink | `#2B1E16` | text, outlines, eyes, visor |
| 23 | UI | panel | `#FFF8EE` | HUD cards, bubbles |
| 24 | UI | panel-edge | `#E9D3B4` | borders, chip off-state |
| 25 | Chars | hair | `#4A3226` | Kit hair (added 2026-11-25 at the Kit gate: 7.57:1 against skin) |
| 26 | Chars | trousers | `#2F3E5C` | Kit legs (added 2026-11-25 at the Kit gate: 2.25:1 below the shirt) |
| 27 | Chars | ghost-faded | `#C8C0D8` | Ghostie accessories: tie, glasses, headset (added 2026-11-25 at the Ghostie gate: Illustrator's faded accessory, `seats/illustrator.md` line 70; 1.59:1 below the ghost body, so it reads as faint print, not a new colour mass; the variant is told by shape, never by this colour alone) |

Shadow bands are neutral grey multipliers only (as Kit's 178 grey). A tinted band adds a hue that is in no row (Ghostie gate, 2026-11-25).

Clear colour (not in atlas): `#FBE7CC`, as in the mock (Fact: `concept/out/shots/02-hub.png`).

## 2. HUD contrast (Fact: computed; rule quick-reference.md line 9)

| Pair | Ratio | Verdict |
|---|---|---|
| ink on panel / panel on ink | 15.3 | pass |
| ghost-purple on panel | 6.3 | pass |
| red-ink on panel | 5.7 | pass |
| cafe-roof on panel | 3.98 | **fail** small text: bar fill or icon only |
| ink on gold | 8.7 | pass |
| hero-shirt on panel | 4.5 | pass, just |
| teal on panel | 2.3 | **fail**: use ink on a teal chip (6.6) |

Rules (Opinion):
- HUD text sits only on `panel` or `ink` cards, never on the 3D world.
- World-space text ("GHOSTED x9", "+9 Copium") gets a 4 px `ink` stroke or a panel pill.
- HUD text 14 px bold minimum; numbers 16 px.

## 3. Ghost, recruiter, robot: shape first, then value

Luminance (Fact, computed): ghost 0.91, robot 0.32, recruiter 0.03. Three clear value steps that stay white, mid grey, near black under deuteranopia and protanopia, so hue is not needed (meets quick-reference.md line 18).

| NPC | Value | three.js build | Height |
|---|---|---|---|
| Ghost | light | `Capsule(0.28, 0.4)` body, 3 `Cone` drips at the hem, 2 ink sphere eyes, no arms, floats 0.15 m | 0.9 m |
| Recruiter | dark | `Box(0.5, 0.7, 0.3)` square-shoulder suit, skin `Sphere(0.18)` head, cream phone `Box` at ear | 1.4 m |
| ATS robot | mid | `Box(0.55)` head on `Cylinder` body, ink visor, 2 cream emissive eyes, antenna with gold ball | 1.1 m |
| Hero | mid-dark | `Capsule` body, skin `Sphere` head, cafe-roof red tie | 1.2 m |

Problem (Fact, computed): ghost on grass 1.49:1, on path 1.33:1; robot on grass 1.74:1. Fixes (Opinion):
- Ink inverted-hull outline, 0.02 m, on every character.
- Contact shadow under each: `CircleGeometry`, ink at 25% opacity.
- Robot eyes cream on ink (13.3:1), not teal: teal on robot is 1.1:1 for deuteranopes (Fact, computed).
- Hero gets a 0.5 m cream floor ring.

## 4. In-world signs

- Board: `cream` box 0.04 m deep, ink text (13.3:1, Fact, computed), 2 px ink border.
- Font: the HUD rounded bold face. `CanvasTexture` 512 x 128, letters 28 px or taller, so cap height stays above 12 px on a 1280 x 720 screen (Opinion).
- Put the sign on the roof edge, tilted 25 degrees to face the camera. In the mock, the far wall sign skews and its grey text gets lost (Fact: `concept/out/shots/02-hub.png`, "Recruiter HQ").
- Max 3 words. Each district also has one big icon prop (cup, scanner, phone, trophy), so text is never the only cue.

## Questions for Rega

1. **Ghost colour.** (a) Off-white `#F8F4EA` with ink outline; (b) pale lilac `#E6DCF5`; (c) translucent white 70%. **Pick: (a).** Translucency makes value unstable.
2. **Outlines.** (a) Characters only; (b) characters and buildings; (c) none. **Pick: (a).** It fixes the 1.3-1.7:1 values for about 1 extra draw call per character.
3. **Which red for HUD text.** (a) `#D4503A` for bars, `#B23A26` for text; (b) one red `#B23A26` for both. **Pick: (a).** Roofs stay warm and text passes.
