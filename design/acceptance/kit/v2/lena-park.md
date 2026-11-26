Lena Park (UI/UX Lead (UI/UX Pro Max)):

# GHOSTED acceptance gate: Kit v2, items L1-L3

SK = `~/.claude/plugins/cache/ui-ux-pro-max-skill/ui-ux-pro-max/2.15.0/.claude/skills/ui-ux-pro-max/`

## Offer

- `SK/references/quick-reference.md` `color-contrast` and `color-not-only` (cited from my seat file, `design/seats/lena-park.md` lines 9, 68). They set the 3:1 non-text line for L1 and the rule that value, not hue, separates the cast for L2.
- `SK/references/quick-reference.md` `color-accessible-pairs`. I used it for the L3 swap test: does a new colour add a value step or a hue that the palette does not have yet?
- My contrast script: the WCAG 2.x relative luminance formula, plus CIE Lab dE76 for "is this a near-duplicate". It runs locally. The numbers below come from it (run 2026-11-25).
- The brief blocked none of my tools. I did not run `search.py`: the rules I need are in the references above, and a search adds nothing to a scoring job.

## Verdict: L1 PASS, L2 PASS (partly unproved), L3 FAIL (one-line fix)

| Item | Result | Evidence (one line) |
|---|---|---|
| L1 | **PASS** | Shirt, the main mass, is 2.91:1 on grass and 3.26:1 on path, so the grass case needs the outline. The ink outline `#2B1E16` is 9.90:1 on grass and 11.08:1 on path, and `ingame-world-crop-x3.png` shows it closed around the whole figure on the path. |
| L2 | **PASS, partly unproved** | In `grey.png` Kit reads mid grey: shirt pixel 105, legs 41, hair 47, skin 182. The planned ghost (L 0.906) and recruiter (L 0.027) sit above and below the shirt (L 0.171): ghost vs shirt 4.33:1, shirt vs recruiter 2.86:1. |
| L3 | **FAIL** | Hair and legs: I add them (reasons below). Tie `#E0533D` is a near-duplicate of cafe-roof `#D4503A` (dE76 4.3, 1.09:1). I require a swap to `#D4503A`. |

## L1: values against the ground (Fact, computed)

| Part | Hex | L | vs grass `#B5D67A` | vs path `#EBD3A6` |
|---|---|---|---|---|
| shirt | `#2F6FDB` | 0.171 | 2.91 | 3.26 |
| legs | `#2F3E5C` | 0.048 | 6.55 | 7.33 |
| hair | `#4A3226` | 0.039 | 7.25 | 8.11 |
| wood (shoes, case) | `#7A4A2E` | 0.092 | 4.52 | 5.06 |
| tie | `#E0533D` | 0.224 | 2.35 | 2.63 |
| skin | `#F2C79E` | 0.622 | 1.04 | 1.07 |
| outline ink | `#2B1E16` | 0.015 | 9.90 | 11.08 |

- **Fact:** the outline is in the engine render. `toon.json` `outline` is `#2B1E16`, 0.007 m. The figure in `ingame-world-crop-x3.png` has a dark edge all the way round, the skin head included.
- **Fact:** the shaded toon band is 178/255 (`toon.json` `bands2`/`bands3`). This makes the shirt darker on its shaded side, so the shaded side has more contrast with the ground, not less.
- **Limit (Fact):** `ingame-world.png` puts Kit on the path only. No render shows Kit on grass, and grass is the case where the shirt is below 3:1. The PASS on grass rests on the outline numbers, not on a picture.
- **Opinion, not a gate item:** `toon.json` sets the outline at 0.007 m. My seat file asked for 0.02 m (`design/seats/lena-park.md` line 78). At the 26 m camera, the crop shows the edge as 1 to 2 px. That is enough today. Check it again when the ghost (1.33:1 on path) gets the same width. The ghost has no dark mass inside its outline, so the outline is all the separation it has.

## L2: greyscale separation (Fact where computed; the rest unproved)

- Kit in `grey.png` (pixels sampled at fixed points): skin 182, tie 129, shirt 105, case 81, hair 47, legs 41, background 233. Kit reads as one mid-grey mass, with a dark band at the bottom and a light head.
- Planned ghost `#F8F4EA`: L 0.906. It is one light mass with no dark band. Against Kit's shirt it is 4.33:1, and against Kit's legs 9.73:1. It cannot be confused with Kit in greyscale.
- Planned recruiter `#2E2C3D`: L 0.027. It is one dark mass from shoulder to feet. Against Kit's shirt it is 2.86:1. **The risk:** against Kit's legs it is only 1.27:1, and against the hair 1.15:1. The two figures are told apart by the mass above the waist: mid grey on Kit, near black on the recruiter. They are not told apart by the legs.
- **Unproved:**
  1. No render shows the ghost, the recruiter and Kit together. The numbers above use hexes. They do not come from lit, toon-shaded, tone-mapped pixels. For example, the Kit shirt renders `#0D5AAC` on the path in the crop, not `#2F6FDB`.
  2. I do not know if the recruiter's skin head and cream phone break up its dark mass enough at 26 m.
  3. I do not know the shade band: a recruiter in shadow may fall to the same value as the shadow under a building (`ingame-world.png`, olive-brown shadow by the cafe).
  4. The ATS robot (L 0.32) sits between Kit's shirt and skin in value. It is outside L2's wording, but it needs the same check.
- **Required for the next gate (Opinion):** one `grey.png`-style render with Kit, the ghost and the recruiter side by side, and one with them on grass, both from the three.js path. Until then, L2 stays a PASS on the numbers only.

## L3: palette ruling (my decision as palette owner)

From the 24 already (Fact, `assets/kit/build_kit.py` lines 14-22): shirt #14, skin #15, wood #5, panel #23, gold #13, ink #22, cafe-wall #6 (cheeks), cafe-roof #7 (tongue), ats-wall #8 (sweat).

| Brief colour | Ruling | Reason (Opinion) and number (Fact, computed) |
|---|---|---|
| hair `#4A3226` | **Add as #25 `hair`** | No palette colour can take this role. Wood `#7A4A2E` is dE76 20.4 away and only 1.60:1 lighter, so it would read as a hat. Ink `#2B1E16` would merge with the outline (1.37:1, dE76 12.1), and the hair locks would vanish. With `#4A3226`, hair against skin is 7.57:1, so the face frame reads at 26 m. |
| legs `#2F3E5C` | **Add as #26 `trousers`** | It gives the hero a dark base under a mid-blue shirt (shirt vs legs 2.25:1), and that split is what makes Kit two-tone in grey. Recruiter `#2E2C3D` is the nearest palette colour, but it would put Kit's legs in the villain's suit colour (1.27:1), which is the L2 risk above. ats-roof `#3D6B99` is too light (dE76 20.8), and the legs would merge into the shirt. |
| tie `#E0533D` | **Swap to cafe-roof `#D4503A`. Do not add.** | It is a near-duplicate: dE76 4.3, contrast 1.09:1. At game size the tie is a few pixels, so the difference cannot be seen. A third warm red would only use up an atlas cell. The change costs very little: the tie against the shirt goes from 1.24:1 to 1.13:1, and in both cases the tie reads by hue (red vs blue, which deuteranopes still see). It also ties Kit to the warm red family of the cafe and the Morale bar. |

- Once hair and legs are added, the palette has 26 swatches in an 8 x 8 atlas, so 38 cells stay free. My seat file's atlas plan is unchanged (`design/seats/lena-park.md` line 18).
- I did not edit `design/seats/lena-park.md`, as the brief said. Whoever owns the next write to that file needs to add rows #25 and #26 as above.
- **Fix to pass L3:** in `assets/kit/build_kit.py` line 14, change `'tie': '#E0533D'` to `'tie': '#D4503A'`, then build again and render again. No geometry changes.
- If Rega wants the brief's tie red kept, that is Rega's call. Options:
  1. Swap the tie to `#D4503A`. **My pick.**
  2. Keep `#E0533D` and add it as #27, accepting a near-duplicate red.
