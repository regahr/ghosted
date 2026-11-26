# GHOSTED: character and world bible, v1

- Date: 2026-11-25
- Ask: Slack C0CHA2A1DM1, ts 1795590208.679899: "i love the name, the concept, so, let's design the character and the world?"
- Seats: 5, each ran alone. Their files are in `seats/`:
  - Viet Tran (design lead for games)
  - BMGD (lore and cast)
  - Illustrator (character art, topic seat)
  - Lena Park (palette and contrast)
  - Emil Kowalski (motion)
- Pictures: `out/ghosted-sheet-1-kit.png`, `out/ghosted-sheet-2-cast.png`, `out/ghosted-sheet-3-world.png`.
- Source: `render.html` (three.js) and `shoot.mjs` (Playwright). Run `node shoot.mjs jobs.json sheets.html '<sheet list>'`.

## Locked earlier

- The name is GHOSTED. Rega approved the concept.
- Look: the warm toy diorama (pick 4a).
- Device: desktop first (pick 5b).

## Decisions

| Topic | Decision | From |
|---|---|---|
| Hero | The player names the hero; the default is **Kit**. Kit is an ex-designer at Crunchr, laid off by a "Quick sync" invite. Kit wants "a job where someone replies". | BMGD, Illustrator (both pick a) |
| Hero build | A wooden pawn toy, 0.95 m and 2.6 head-heights, with a hair sprout that carries the mood at game size. Blue shirt, red tie, briefcase, lanyard badge. | Viet (build), Illustrator (sprout, badge) |
| Expressions | Hopeful, ghosted, rejected but fine, focused, offer joy. | Illustrator |
| Outfits | 3 base outfits (colour swaps) and 4 unlocks, look only: Blazer (first panel), Lucky Hoodie (ghosted 25 times), Take-Home Phones (finish a take-home), Party Hat (first offer). | Illustrator |
| Cast | Ricky (the recruiter), the Ghosties, ATS-9000, Auntie Dot (mentor), Brett Bullet-Points (rival), Juno (barista, heal), the Panel, Gary (pigeon postman). | BMGD |
| Recruiter colour | A dark suit `#2E2C3D` with a coral headset and tie. | Lena (difference by value for colour-blind players). This also fixes BMGD's flag that Ricky and the heal door had the same orange. |
| Ghost | Opaque off-white `#F8F4EA` with an ink outline. It has no mouth, because "a ghost never replies". A recruiter drains into a ghost in 3 steps. | Lena (opaque), Illustrator (no mouth), Viet (drain, pick c) |
| City | **Port Pending**, where everything is "under review". | BMGD |
| Districts | Applyside (weeks 1-4), Callback Quarter (weeks 5-8), Panel Heights (weeks 9-11) and LinkedUp Plaza (week 12). Each district is one funnel stage on a 24 x 24 m block. | BMGD (names, funnel), Viet (blocks, landmarks) |
| Light | The light goes from morning to sunset over the Season: elevation 62° in week 1 down to 12° in week 12. A rejection never makes the light darker. | Viet. BMGD proposed a night-then-dawn arc, and Viet leads the look. |
| Currency | **Copium** | BMGD (pick a: Rega saw it in the mock) |
| Palette | Lena's 24 colours. HUD text sits on panel or ink cards only. | Lena |
| Motion | The hero hops like a toy at 1.8 m/s and moves on the frame of the click. Ghosted lasts 750 ms and rejected 800 ms, and both can be skipped. The offer lasts 2 s. The camera never shakes. | Emil (Viet has final say on 3D motion) |

## Art rule: no fringe (Rega, 2026-11-26)

No character's hair may read as a fringe or bangs at the game camera (26 m, pitch 42°).
- A clear band of forehead skin shows between the hairline and the brows: at least 4 px at 1x.
- Strand lines ON the hair are fine (Rega, ts 1795658703.410809). What fails is hair, or a hair edge, that hangs down
  over the forehead or beside the eyes at the temples.
- Sources: Ricky, ts 1795622664.391049 ("can erase the hair fringe?"), and Auntie Dot, ts 1795658373.096399 ("hair
  fringe detected").

## Art rule: mouths (Rega, 2026-11-26)

Rega likes Ricky's open grin: a filled dark mouth with a white teeth band along the top edge (ts 1795659302.700869). A
thin or broken ink smile line under a white crescent looks awkward. Use the Ricky style for open, grinning mouths.

## Auntie Dot

- **Locked: v1, after no-fringe pass 2** (ts 1795659821.728169). See `assets/auntie-dot/LOCKED.md`.

## Brett

- **Locked: v1, after the mouth pass** (ts 1795659740.072339). See `assets/brett/LOCKED.md`.

## ATS-9000

- **Locked: v1, direction B with a neck** (card 4, ts 1795631210.838989). See `assets/ats9000/LOCKED.md`.

## Ricky

- **Locked: v1** (card 3, ts 1795624795.450479). See `assets/ricky/LOCKED.md`.

## Ghostie ruling (Rega, 2026-11-25)

- **Locked: v7** (card 2, ts 1795620475.864169). See `assets/ghostie/LOCKED.md`.

- The ghost still has no mouth ("a ghost never replies").
- The tie variant's centred tie may read as a tongue at the 26 m game camera. Rega accepts this as a joke, ts
  1795615890.262169: "it's ok, i like it to see them to have tie that looks like tongue lol".
- So "nothing centred below the eyes" no longer fails the tie variant.
- Evidence: `acceptance/card-2-ghostie/i-evidence.png`.
- Body map: `assets/ghostie/sketch/body-map.md`. The eyes are high, the ears are on the eye line, the headset is
  centred with 2 cups, and the tie is centred under a collar.

## Art pipeline (Rega, 2026-11-25)

From Recruiter Ricky on, each character, NPC, prop and district follows these steps:
1. The Illustrator draws a 2D sketch.
2. All the seats approve the sketch.
3. Rega accepts it.
4. The 3D model is made, and it must match the sketch.

The Ghostie finishes in 3D without a sketch (ts 1795604718.933169). Kit stays locked. The steps are in
`acceptance/checklist.md` and in "Game art pipeline" in the council skill.

## Not proved, and what is not done yet

- The meshes are not merged yet. In this mock the hero is about 3.5k triangles across about 25 draw calls. The budget is 2.5k triangles in 1 merged mesh, so the build must merge the parts.
- Late-week light makes the grass look olive in the Panel Heights and LinkedUp shots. Tune it in M1.
- The map shot crops the top of the LinkedUp Tower.
- The motion is specified, not animated. The sheets show still poses only.

## Defaults Rega can change

Each default below is the pick of the seat that proposed it:
- Hero naming.
- The city name.
- Copium.
- The ghost with no mouth.
- Cosmetics are look only.
- The light arc.
