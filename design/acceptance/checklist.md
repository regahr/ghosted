# GHOSTED design acceptance checklist, v1

Rega's call, 2026-11-25: "A1c A2b let's go" (Slack C0CHA2A1DM1, ts 1795594400.024269).

**Superseded 2026-11-25** (Rega, ts 1795619754.712759: "from now on, let me be the gate, propose only to me"). There are
no more seat gate rounds. The items below are now a checklist for the builder and the chair, and Rega is the gate.

How the gate worked (historical):
1. Each design is scored by the 5 design seats, each one on its own.
2. Each item gets PASS or FAIL, with one line of evidence. The evidence is a render file and what is seen in it.
3. One FAIL on a must item sends the design back.
4. Only a design that passes every must item goes to Rega as a card.
5. Rega accepts it or asks for a redo. Accepted means the design is locked for the build.

Sketch first (Rega, 2026-11-25, Slack C0CHA2A1DM1, ts 1795604691.829739: "illustrator always provide draft sketch
first, then 3d artist build based on it (after sketch approved by all)"):
- Start: from the next design after the Ghostie (Recruiter Ricky). Rega, ts 1795604718.933169: "do it after ghostie,
  let 3d artis finish with ghostie first". The Ghostie finishes its 3D gate without a sketch.
- Stage A, the sketch. The Illustrator draws a 2D model sheet: a turnaround (front, 3/4, side, back), every variant or
  expression, and a thumbnail at the game camera size next to Kit. All 5 seats score it on the sketch items below. Then
  Rega accepts it or asks for a redo.
- Stage B, the 3D model. Viet models to match the accepted sketch. All 5 seats score the 3D on items V, I, L, B and E,
  plus S1. Then Rega accepts it.

Sketch items (stage A):
- [must] SK1 (Illustrator): the shapes are designed curves, with no code primitives, and the silhouette reads at 64 px.
- [must] SK2 (Viet): it can be built in 3D within the triangle budget, and every view agrees with the other views.
- [must] SK3 (Lena): every colour is in the palette, and the value reads against the grass and the path.
- [must] SK4 (BMGD): the role, the tone and the bible rules hold at the game camera thumbnail.
- [must] SK5 (Emil): the pose reads alive, and the parts allow the specified motion.

Stage B item:
- [must] S1 (Viet and Illustrator): the 3D renders match the accepted sketch in shape, proportion and colour.

The renders that every design must include:
- Blender EEVEE renders: a turnaround of front, 3/4, side and back.
- A **game-engine render of the exported glTF**, made in three.js with the game's toon shading and outline.
  This proves that what Rega accepts is what Rega plays.
- A 64 px solid-black silhouette.
- A greyscale render, for the value and colour-blind check.

## Viet Tran (3D design lead): shape and build

Source: `3dviz-pro-max/templates/checklists/visual-anti-slop.md`, items 1-7.

- [must] V1. The object reads correctly: the silhouette, the proportions and the negative space are right.
- [must] V2. Construction fits the object: there are no parts that cut into each other, no floating parts and
  no gaps. Bands, straps and hair sit on the surface.
- [must] V3. The detail is right at the real view size: game camera at 26 m, and the card close-up.
- [must] V4. Materials and shading follow the toon style: 2 bands on props and 3 on faces. The shadows are
  clean, with no acne, streaks or blotches.
- [must] V5. The glTF is at most 2.5k triangles for the hero (300 for a ghost, 1.4k for a human NPC). It is 1
  merged mesh, or at most 3 meshes.
  Chair amendment, 2026-11-25: swap parts do not count toward the 3 meshes. These are the face sets and the sprout,
  which change per expression. The reason: the build brief asked for `sprout` and `briefcase` as their own nodes,
  so the old rule failed Kit only because of the brief.
  Chair amendment 2, 2026-11-25: the ghost budget is 450 visible triangles per variant, not 300. The reason: Ghostie v1
  failed V3 and I2 on a faceted outline (8 crown segments, 8-sided eyes) at 298 of 300, so a rounder outline cannot fit.
  The cost: 24 ghosts at 450 = 10.8k triangles. Viet proposed it (`acceptance/ghostie/viet-tran.md`). It is shown to
  Rega on card 2, and Rega can overrule it.
  Chair amendment 3, 2026-11-25: the ghost budget is 600 visible triangles per variant. The reason: v2 failed V3 and I2
  again on crown and hem corners at 442 of 450. The cost: 24 ghosts at 600 = 14.4k triangles, about 6 Kits. Shown to
  Rega on card 2.
  Amendment 4, 2026-11-25, Rega's call (ts 1795619841.598789, option 2): the ghost budget is 800 visible triangles per
  variant. That is 24 ghosts at 800 = 19.2k triangles, so that the dome and hem curves read round, like the sketch.
- [must] V6. The in-game render matches the Blender render in shape and colour.

## Illustrator: character art

- [must] I1. The 64 px silhouette shows the round head, the sprout and the briefcase.
- [must] I2. The shapes are hand-made. A part may start as a primitive, but each part has a designed profile:
  for example a shirt hem, sleeves that taper, a tie with a knot, hair locks.
- [must] I3. Each expression can be told apart at the card size. (For Kit, the face parts swap.)
- [should] I4. The design is its own. It copies no known character.

## Lena Park: legibility and access

- [must] L1. The hero's value differs from the grass (`#B5D67A`) and the path (`#EBD3A6`) by at least 3:1, or an
  outline separates them.
- [must] L2. In the greyscale render, the hero, the ghost and the recruiter can still be told apart.
- [must] L3. The colours come from the 24-colour palette in `design/seats/lena-park.md`, or a new colour is
  added there with a reason.

## BMGD: loop and register

- [must] B1. The design matches the bible (`design/bible.md`): its name, its role and its tone.
- [must] B2. The tone is comic and kind. Nothing mocks the player.

## Emil Kowalski: feel

- [must] E1. The rest pose reads as alive and kind, not stiff.
- [should] E2. The rig or parts allow the specified motion: the hop, squash and stretch, the sprout spring.
