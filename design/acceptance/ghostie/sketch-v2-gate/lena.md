Lena Park (UI/UX Lead (UI/UX Pro Max)):

# Ghostie sketch v2 gate: SK3 and the whole-picture check

## Offer

- `seats/lena-park.md` rows 10, 16, 22 and 27 (lines 31, 37, 43, 48), and the neutral shade rule (line 50): this is the list I check each hex against.
- `seats/lena-park.md` section 3 (lines 82-84): ghost on grass is 1.49:1 and on path 1.33:1, so the ink outline and the contact shadow must carry the value. This turns "does the value read" into "is the ink edge closed all round".
- UI/UX Pro Max `references/quick-reference.md` `color-not-only` and `color-contrast` (3:1 for non-text parts): a variant that only a 1.4-1.6:1 tint marks does not read. This is the rule behind the glasses and headset finding.
- A local WCAG 2.x luminance script, and pixel samples of the real blockout crops. I ran no search.py query, because the rules above already cover the question. The brief blocked none of my tools.

## SK3: **FAIL**

| Check | Result | Mark |
|---|---|---|
| Colours in the palette | PASS. The character fills are `#F8F4EA` (16), `#C8C0D8` (27), `#C9A6D6` (10) and `#2B1E16` (22). The shade is `#E9E5DC`, which equals `#F8F4EA` x 0.94 per channel, so it is neutral (`src/ghost.py` line 13). Ground shadows are ink at 16-18% opacity. The other hexes are not on the character: `#1D63C8` is the annotation blue, `#FDE6C8` is the page and `#BDD662` is the tile grass. `#BDD662` matches the sampled render ground (189,214,98). | Fact (hex grep of `src/*.svg`) |
| Value against grass and path, in the real render | PASS, but only because of the outline. The body in the render is (242,224,192). That is 1.25:1 against the grass (189,214,98) and 1.20:1 against the path (239,202,140). The ink edge is about 10:1 (grass 9.9, path 11.1). With the contact shadow it reads clearly in `lineup-grass-crop-x3.png` and `lineup-path-crop-x3.png`. | Fact (computed from pixel samples) |
| Headset reads | WEAK. In the real render, the band is a faint lilac arc and only one cup shows. It has no ink edge. | Fact (render crop); "weak" is Opinion |
| Glasses read | FAIL. In the real render, the rims are a 1-2 px grey-lilac halo round each eye dot. They read as smudged or tired eyes, not as glasses. The sheet's own game-camera tile 2 shows the same. Rims are `#C8C0D8` at 1.59:1 on the body, with no ink edge (`src/ghost.py` lines 182-188). | Fact (render crop, ratio); read is Opinion |
| Headset band breaks the body outline | FAIL. See the sheet "variant headset" line below. | Fact |

Why FAIL: the brief makes "glasses and headset read" part of SK3. Row 27 (line 48) says "the variant is told by shape". At the game camera, the shape of the glasses does not survive, because a 1.59:1 tint with no edge is under 3:1. The tie reads because it has an ink edge (row 10, line 31).

Fix (Opinion, my pick): keep row 27 and add a thin ink line (`#2B1E16`, about 1.5-2 units) on both sides of the glasses rims and the headset band, as the cups and the tie already have. Ink on the body is 15:1. Then run Viet's render again and check it at 1x.

Caveat (Fact): the blockout render is the v5 build (`assets/ghostie/blockout/`), not a v2 model. It uses the same colour rows, so the value read carries over. The body proportions are different.

## Whole-picture check (each panel zoomed at 2x)

**ghostie-sheet.png**
- Front: none seen. Fact (2x crop).
- 3/4: collar wings are drawn full width and symmetric, while the body turns. They are not foreshortened. Opinion.
- Side: none seen as a drawing flaw. The end-on arm oval is already ruled (`sketch-viet.md` §5). Fact.
- Back: none seen. Fact.
- Palette and shape rules: none seen. Fact.
- Variant tie: none seen. Fact.
- Variant glasses: the rims have no ink edge (1.59:1). They read on the card, but not at the game camera. Fact.
- Variant headset: **the band replaces the dome's ink outline on both upper sides.** Pixel rows at sheet y 760-790 (display units) run peach, then lilac band, then body, with no ink between them. At the crown the ink thins from 5 px to 2 px under the band. On those sides the silhouette edge is lilac on peach (1.45:1), which leaves a gap in the outline. The cups have ink, but the band has none, which is not consistent. Fact (pixel scan, `ghost.py` lines 191-198).
- Wave: the label says "faint blue = rest", but the rest-arm line (`#1D63C8` at 0.3) renders grey. The line also ends open as a hook into the body side. Fact for the colour; Opinion that the open end reads as a stray mark.
- Rest pose: none seen. Fact.
- 64 px silhouette: none seen. Fact.
- Game camera row: tile 1 shows the tie as a tongue (Rega accepted, `chair-read-sketch-v2.md`). Tile 2 shows the glasses as smudged eyes. In tile 3, the band and the cups are faint. Fact for what shows; Opinion for the read.
- Tie build spec: none seen. Fact.

**body-map.png**
- A explore: none seen as a drawing flaw. The tongue read shows in all 8 tiles, and Rega accepted it. Fact.
- B front landmarks: a stray blue tick floats below the end of the dimension bar, just above the "C. ATTACHMENT POINTS" heading. The bar stops above the hem line, and the tick sits apart from it. A guide line runs behind the "2nd head" label. Fact (2x crop).
- B notes: none seen. Fact.
- C attachment: the same headset band outline gap as on the sheet. The crown ink shows above the band only in a thin crescent. Fact.
- D game camera: tile 5 (glasses) shows smudged eyes, and tile 4 (headset) is faint. Fact for what shows; Opinion for the read.

**tie-options.png**
- Ghostie card: none seen. Fact.
- Game cam x3 and 1x: the tongue read (accepted). The "game cam x3" label is cut off at the top edge of the crop, but the full sheet shows it whole. Fact.
- Kit card and Kit crops: none seen. Fact.
- Close-ups and notes: none seen. Fact.

**Real render (blockout lineup crops)**
- Glasses ghost: rims are not legible (see SK3). Fact.
- Headset ghost: the near cup does not show, and the band is faint. Fact.
- Tie ghost: the tie is off-centre, as in the v5 build, not the v2 centred tie. The render is older than the sketch. Fact.

Open flaws that block the card: (1) the headset band breaks the outline (sheet and body map C), (2) the glasses do not read at the game camera, (3) the stray tick on body map B.
