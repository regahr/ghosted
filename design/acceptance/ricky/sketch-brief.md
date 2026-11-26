# Recruiter Ricky: body map and sketch brief (chair, 2026-11-25)

Rega, ts 1795620541.639459: "go". Pipeline: council skill, "Game art pipeline", steps 0, 1a, 1b and 1, plus "Ready
check before any drawing", "Judge a sketch as a sketch" and "Rega is the gate". No seat gate rounds: the chair checks
at 2x, then the sketch goes to Rega.

## Decided needs (sources)
- **Role:** Recruiter Ricky runs the Recruiter Call node. He opens with "Super excited to connect!", then forgets you.
  His lost threads become the Ghosties (`seats/bmgd.md` L41).
- **Tone:** comic and kind (bible). He is cheerful and busy, not evil.
- **Look:**
  - a dark suit `#2E2C3D` (palette row 17), with a headset and a tie in a bright accent colour (`bible.md`,
    "Recruiter colour");
  - the bible says "coral", but coral is NOT a palette row. Pick an existing row from `seats/lena-park.md` for the
    accent and give the reason;
  - it must not look like the heal-door orange `#F2994A` (BMGD's flag);
  - it must read as different from Kit's red tie `#D4503A`, either by hue or by placement.
- **Skin:** row 15 `#F2C79E`, ink row 22, shade a neutral grey multiplier only.
- **Size:** the hero Kit is 0.95 m (`assets/kit/LOCKED.md`). Ricky is about 1.05 times Kit (`seats/viet-tran.md` L63).
  Use the same toy-pawn family as Kit, so he sits in the same world.
- **Budget for the 3D:** a human NPC gets 1,400 triangles or fewer (`acceptance/checklist.md` V5).
- **Drain to a Ghostie, in 3 steps** (`bible.md`, Ghost row). Draw one strip: Ricky, then step 1, step 2, then the
  locked Ghostie (`assets/ghostie/LOCKED.md`, `assets/ghostie/v7/front-variants.png`).
  - The colour drains to white, the legs fade, and he floats.
  - His headset and tie must become the Ghostie's centred 2-cup headset and centred tie.
  - So place them where the Ghostie body map puts them, on Ricky's own landmarks: cups on the ears, the tie under a
    collar (`assets/ghostie/sketch/body-map.md`).
- **Legibility risk to fix on Ricky:** in greyscale, the dark suit is close to Kit's trousers (1.27:1, from the Kit gate
  notes). Show a greyscale thumbnail of Ricky next to Kit and next to a Ghostie, on grass. Give Ricky a value break that
  separates him, for example a lighter shirt V, cuffs or the accent.
- **Game camera:** 26 m, pitch 42°, yaw 20°. Thumbnails sit next to Kit, using `assets/kit/` and the Ghostie v7
  lineup crops for scale.
- **Motion parts for the 3D:**
  - a hop like Kit's;
  - one "on the phone" gesture: the hand to the headset;
  - the drain.
  Draw the arm joins clearly.
- **Palette:** only existing rows. A new colour needs Lena's row first, so ask the chair.

## What to make (folder `design/assets/ricky/sketch/`)
1. **`ready.md` first.** If any need is missing or unclear, STOP and report. Do not draw.
2. **`explore.png`.** References, 8-12 rough thumbnails, then 2-3 directions and your pick with a reason (step 1b).
3. **`body-map.png` and `body-map.md`.** Step 1a:
   - proportions in head-heights;
   - landmarks: eyes, mouth, ears, neck, shoulders, hands, feet;
   - an attachment point for the headset and for the tie;
   - a game-camera check.
4. **`ricky-sheet.png`.** An upright, neutral turnaround (front, 3/4, side, back), plus:
   - the drain strip;
   - the phone gesture;
   - a 64 px silhouette;
   - the greyscale lineup with Kit and a Ghostie;
   - game-camera thumbnails next to Kit;
   - the palette rows used.
   Use hand-drawn Bezier curves.
5. **SVG sources** in `src/`, rendered with `magick`.

It is a sketch for the 3D builder, not final art: the line polish is not judged. Before you report, check at 2x that
the shape, the proportions, the placements, the views agreeing and the game-camera read are clear and right. Write
`notes.md`: what works, what is open, each claim with a file, marked Fact or Opinion. No web, no image generation, no
other service. Work only in `assets/ricky/sketch/`.
