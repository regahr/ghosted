BMGD (Game Designer): Ghostie sketch v2 gate, item SK4 and the whole-picture check. 2026-11-25.

## Offer
- `bmad-game-dev-studio/0.7.2/src/workflows/2-design/gds-create-narrative/checklist.md` line 54 ("Each has distinct role in story"). I use it as the role test for each variant: the accessory must say "this was a recruiter", and the ghost has no mouth. This test is what makes the glasses variant fail below.
- My lore table `design/seats/bmgd.md` lines 39 and 41 says what a Ghostie is: one of Ricky's lost threads, a recruiter who never replied.
- Nothing else in my skill reads pictures. The brief did not block any of my tools. I made 2x and 3x crops in my scratchpad only. I did not edit any asset.

Sources:
- `design/acceptance/checklist.md` line 26 (SK4).
- `design/bible.md` line 29 (Ricky has a coral headset and tie), line 30 (no mouth) and lines 38-46 (Ghostie ruling: the tie that reads as a tongue is accepted).
- `assets/ghostie/sketch/body-map.md` lines 16, 24-26 (ear points and attachment points).
- `~/.claude/skills/council/SKILL.md` lines 185-195 (whole-picture check).

## SK4: FAIL (one narrow cause: the glasses variant)

| Check | Result | Evidence |
|---|---|---|
| No mouth | PASS | **Fact:** the mouth zone is empty in every view and variant on `ghostie-sheet.png` and in `body-map.png` B (dashed box, x 132-168, y 136-160). |
| Tie reads as a tongue at the game camera | PASS (accepted joke) | **Fact:** `lineup-grass-crop-x3.png`, left ghost: a lilac stripe hangs centred under the eyes. Rega accepts this (`bible.md` lines 41-43). **Opinion:** "the recruiter sticks its tongue out at you" fits the tone. It mocks the player and does not make the ghost a victim. |
| Tie variant role | PASS | **Opinion:** a tie under a collar is Ricky's kit (`bible.md` line 29). It says "office recruiter" at card size (`tie-options.png`, close-up). |
| Headset variant role | PASS | **Fact:** `lineup-grass-crop-x3.png`, right ghost: the band shows across the dome and one cup shows at the side. **Opinion:** it is Ricky's headset, so it is the best "recruiter" read of the three. |
| Glasses variant role | **FAIL** | **Fact:** `lineup-grass-crop-x3.png`, middle ghost: the rims are a 1 px grey ring round each eye in the x3 crop, so they are under 1 px at 1x. In the 1x tile on `ghostie-sheet.png` (game camera row, tile 2) only a faint halo shows. **Opinion:** at the game camera this ghost reads as a plain ghost with tired or bruised eyes, so it does not read as a glasses variant. Even at card size, round glasses only say "office person", not "recruiter". Tired, sad eyes also push the tone towards the ghost as a victim, and in v1 I named that as the one read that flips the joke (`sketch-bmgd.md`, item 4). |
| Tone | PASS | **Opinion:** the soft dome, the two oval eyes, the small wave and the loose tie make a sheepish office ghost, not a menacing one. |
| Body map placement | PASS, with one drawing flaw | **Fact:** the headset cups sit on the ear points (eye line, side edges; `body-map.md` line 16, `body-map.png` C). The tie hangs from a collar at the neck line. Each glasses rim sits round one eye. All 3 make sense. **Fact:** the headset band top is at y 46, which is 10 units under the crown (`body-map.md` line 24). See the flaw list. |

The decision on the glasses is Rega's. The Illustrator owns the variants, and I own the role. Options:
1. **Keep the glasses, but make them read.** Thicker rims with an ink edge, sized to stay at least 1 px at 1x. Lena checks the value. This is the less expensive option.
2. **Swap the glasses for a recruiter sign that reads at 26 m,** for example a phone held to the ear ("Let me circle back") or a coffee mug. This is a new sketch item for the Illustrator.
3. **Ship 2 variants (tie and headset)** and drop the glasses.

My pick: 1. It is the smallest change and keeps 3 variants. If the rims still do not read in the blockout render, go to 2.

## Whole-picture check (every panel at 2x; my crops are in my scratchpad only)

| Panel | Flaw | Mark |
|---|---|---|
| Sheet: front | The left inside shade band ends in a hard flat edge above the left hem lobe. It does not follow the lobe. The same thing shows on the back view, the variants and body map B. Minor. | Fact (seen at 2x) |
| Sheet: 3/4 | The left side is a straight vertical wall and no near-arm shape shows, while the right side has a full arm. Next to the front view, this reads as a different body. The collar wings stay fully symmetric even though the body is turned. | Opinion |
| Sheet: side | The tie is drawn face-on, at full width, about one tie width inside the front outline. On a side view it should lie edge-on, on the front outline. As drawn, it looks painted on the side of the body. The collar shows as a dark wedge with a point that sticks out to the right. The end-on arm oval can read as a hole or a mouth-like pocket (known, Viet ruled on it in `sketch-viet.md` §5). | Fact (position); Opinion (read) |
| Sheet: back | None seen. The notch is centred on the hem. | Fact |
| Sheet: palette and rules | None seen. | Fact |
| Sheet: variant tie | None seen. | Fact |
| Sheet: variant glasses | None seen at card size. At the game camera the rims are lost (see SK4). | Fact |
| Sheet: variant headset | The dome's ink arc shows ABOVE the band at the top, while at the sides the band covers the outline and meets the cups. So the band changes plane and looks like a hairband worn in front of the head, not a band over the crown. This is the same drawing in body map C. | Fact (seen at 3x); Opinion (read) |
| Sheet: wave | None seen. The faint blue line of the rest arm crosses the arm root (it is a label). | Fact |
| Sheet: rest pose | Where the drooping arm_R (viewer left) meets the body under the arm, the outline makes a sharp upward point, like a hook or a claw. This is the "corner" type of flaw that Rega flagged in v1. | Fact (seen at 3x) |
| Sheet: 64 px silhouette | None seen. | Fact |
| Sheet: game camera row | The tie tile reads as a tongue (accepted, `bible.md` line 41). The glasses tile shows only a faint halo (SK4 fail). The headset tile shows a band that is faint but readable at x3. | Fact |
| Sheet: tie build spec | None seen. The panel is mostly empty. | Opinion |
| Body map A: explore | The blue mouth-box overlays look like a blue nose at this size. They are labels, but they hide how the face really reads at the camera. | Opinion |
| Body map B: front landmarks | The panel title says "body 265 crown-to-hem", but the notes on the same sheet say "Whole body = ... 280 units" (`body-map.md` line 13). Two body heights appear on one panel. A loose blue tick floats under the end of the head bracket, just above heading C. The "arm root bottom y 260" line runs a little under the drawn underside of the arm. | Fact |
| Body map B: notes | None seen. | Fact |
| Body map C: attachment | The headset band dips 10 units under the crown (the same flaw as on the sheet headset variant). The side tile has the same face-on tie as the sheet side view. | Fact |
| Body map D: game camera | Tile 1 (the v5 crop) is tan and beige, not the off-white of the other tiles. The caption says it is v5, but next to the other tiles it looks like a different colour. Tile 5 has the glasses halo only. | Fact (colour); Opinion (confusing) |
| Tie sheet: Ghostie card | The label "x3, mouth zone" overlaps the bottom edge of the first green tile. | Fact (seen at 4x) |
| Tie sheet: Kit card and close-ups | None seen. | Fact |
| Blockout lineup (reference render) | The glasses do not read (SK4). The lit ghost body samples `#F3E2C3`, which is warmer and more tan than the `#F8F4EA` of the sketch. This is outside my decisions (Lena: value and palette), and I list it only because I can see it. | Fact (pixel sample at 170,70) |

Open visible flaws that block the card: the glasses at the game camera, the headset band plane, the rest-pose arm hook and the side-view tie. The minor ones are the shade band end, the two body heights on body map B, the loose tick and the label overlap.
