Illustrator (Illustrator): Ghostie v2, GHOSTED acceptance gate card 2, items I1-I4

All paths are under `runs/jobless-roguelike/design/`. I judged from the PNGs only. I read `selfcheck.md` as claims.

## Offer

- `~/.claude/skills/illustrator/SKILL.md` § 9.2 (Composition Critique): the "view at thumbnail size" and "squint" checks. I used them for I1 (I measured the 64 px silhouettes row by row at a 50% threshold) and for I3 (card strip and game-camera crops).
- `~/.claude/skills/illustrator/SKILL.md` § 1.3 ("Hierarchy of Read"): I used it for the arm-shape question and for the read at the game camera.
- `~/.claude/skills/illustrator/SKILL.md` § 10 #2 (cliché imagery): I used it for I4.
- The brief did not block any of my tools.

## v1 fixes: did they land?

| My v1 fix | Landed? | Evidence |
|---|---|---|
| 1. Rounder outline, no corners at 1200 px, 12-sided eyes | **Partly** | Fact: `hero.png` crown and sides still show straight segments with clear corners. I count about 12 on the crown arc, and there are corners at the shoulders (x≈405, y≈410 and x≈835, y≈410). The segments are shorter than in `v1/hero.png`. The eyes are now smooth ovals. The builder also says the corners are still there (`assets/ghostie/selfcheck.md`, V3 and "Still weak" 1). |
| 2. Soft hem, round scallops | **Partly** | Fact: `crops/hem-notch-34.png` shows the notch as 3 straight segments with a flat top and 2 corners. That is a trough, not a round scallop. In `hero.png` the hem is a polyline of about 8 straight segments. Fact: in `silhouette-64-x4.png` the 2 notches now read soft. |
| 3. Arms: closed ink, rounded mitten tip | **Ink yes, shape no** | Fact: the ink is closed at the root (`crops/arm-root-front.png`) and at the end (`crops/arm-end-on-side.png`). But the arm is a horizontal cylinder with a flat 8-sided end cap (`crops/arm-end-on-side.png`, `turn-side.png`). In `hero.png` and `turn-34.png` the near arm ends in a pointed hexagon. In `crops/arm-root-front.png` a light band runs inside the ink at the root, so the arm reads as a part stuck onto the body. It does not grow out of the body. |
| 4. Tie on the chest, ink edge, no nose or mouth read | **Card yes, game no** | Fact: in `turn-front.png` the tie starts at y≈680, under the arm line (y≈600-680), and it has an ink edge. Fact: in `lineup-grass-crop-x3.png` and `lineup-path-crop-x3.png` (left ghost) the tie is a lilac blob directly under the eyes. |
| 5. Optional: eyes turned in | **Not done** | Fact: `hero.png` far eye is still a thin sliver at the face edge (x≈430). The builder confirms this (`selfcheck.md`, "Still weak" 4). |

## The arm shape: soft ghost flap or something else?

**Something else.** Opinion, based on these files:
- `hero.png`, `turn-34.png`: the near arm is a stubby peg with a pointed hexagon tip. It reads as a bolt, a pencil stub or a cork, not a cloth flap.
- `turn-front.png`: both arms are short horizontal tubes at mid height. They do not taper and they do not droop.
- `lineup-grass-crop-x3.png`: at the game camera the 2 nubs sit level with the eyes on a smooth dome, so they read as **ears**. All 3 ghosts read as bald baby heads with ears, not as sheets with arms.
- `silhouette-64-x4.png`: a dome with 2 round side nubs and a wavy hem whose corners flare to points. This is almost the exact shape of a well-known app-logo ghost (see I4).

## Scores

| Item | Verdict | Evidence |
|---|---|---|
| I1 [must] 64 px silhouette: dome, skirt with hem, arms | **PASS** | Fact: `silhouette-64.png` (74x64). The dome is rows 0-19. The arm bumps are rows 32-43 (width 49 to 61 px, then back to 51 at row 44). The skirt widens from 51 px (row 44) to 56 px (row 55). The hem has 2 notches and a centre lobe to row 63 (`silhouette-64-x4.png`). Fact: in `silhouette-64-34-x4.png` the near arm is only a small bump on the right edge, and the far arm does not show. Opinion: the front view carries all the cues. The 3/4 arm read is weak, as in v1. |
| I2 [must] Hand-made shapes, designed profiles | **FAIL** | Fact: corners still show on the crown, shoulders and hem in `hero.png`, `turn-front.png` and `turn-34.png` (see fix 1 and fix 2 above). Fact: the arm is a cylinder with a flat polygon cap (`crops/arm-end-on-side.png`), and it has a pointed hexagon tip in `hero.png`. Fact: locked Kit (`assets/kit/hero.png`) has smooth curves, value modelling and eye highlights. Opinion: v2 is a clear step up from `v1/hero.png`, but at card size it still reads as a low-poly code model next to Kit. The arm, the one new shape, reads as a machined peg. This is still the "slopped" look. It does not meet the "hand-made and charming at card size" bar. |
| I3 [must] Variants told apart at card size (and at game camera if possible) | **PASS** (card) / weak (game) | Fact: in `variants.png` the tie, the 6-sided glasses with bridge, and the headset band with ear cup are each clear. The headset band stays inside the crown. Fact: in `lineup-grass-crop-x3.png` the glasses are a faint grey bar and the headset is a faint arc. The tie is a lilac mark right under the eyes. Opinion: at the game camera the tie ghost looks like it has a mouth or a tongue out. That breaks "no mouth" (`bible.md` line 30, as cited in my v1 card). |
| I4 [should] Its own design | **FAIL** (should) | Opinion: in v1 I gave a watch note. v2 made it worse. In `silhouette-64-x4.png` the round mid-height nubs and the pointed, flared hem corners make the front silhouette almost the same as a well-known app-logo ghost, and the cream ghost on a cream-yellow card (`hero.png`) adds to it. In colour the face and tie separate it. In silhouette and on a store icon it does not. |

**Overall: FAIL** (I2 must fails. I1 and I3 pass. I4 should fails.)

## Narrowest fix list

1. **Arms (fixes I2 and I4, and the ear read).** Remove the cylinder and its end cap. Make each arm a flat, tapered flap that grows out of the body surface with no visible joint. It should droop down and out about 25-35°, be wider at the root than at the tip, and have a round tip. Put the root about 10-15% lower than now, so that at the 26 m camera the arms sit below the eye line and do not read as ears. The proof files are `turn-front.png`, `hero.png`, `silhouette-64-x4.png` and `lineup-grass-crop-x3.png`.
2. **Hem corners (fixes I4).** Do not let the 2 outer hem corners flare out to points. Round them in like the centre lobes. Keep the 2 notches.
3. **Hem notch (fixes I2).** Add 2 vertices to each notch so the top of the trough is a curve, not a flat segment between 2 corners (`crops/hem-notch-34.png`).
4. **Crown and shoulder (fixes I2).** Move rings to the shoulder turn (about 40-55% up the dome), where the corners show in `hero.png`. Take them from the flat sides if needed. If 450 triangles cannot hold this, that is Viet's call (V5).
5. **Tie at game camera (I3 game read, BMGD owns B1).** Make the tie shorter, start it lower, and use the darker palette lilac, so that at 26 m it reads as a stripe on the chest and not as a mouth under the eyes.
6. Optional: eyes turned in 4-5° (my v1 fix 5).

Re-render `hero.png`, `turn-front.png`, `turn-34.png`, `variants.png`, `silhouette-64*.png`, `crops/hem-notch-34.png` and `lineup-*-crop-x3.png`, and I will score again.
