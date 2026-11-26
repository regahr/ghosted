# Emil Kowalski (Principal Designer): Ghostie v1, E1 and E2

Judged from the PNGs, `ghostie.glb` and `ingame.html` `pose()`. Builder notes were read as claims only.

## Offer

| Tool (path) | How it changes the answer |
|---|---|
| `~/.claude/skills/emil-design-eng/SKILL.md`, frequency table and "Should this animate at all?" | The wave plays only inside the 750 ms ghosting beat, at the 26 m camera. A flaw seen only in the wave pose at close-up costs little. |
| same file, "Review your work the next day" and "Slow motion testing" | The float and wave are code, not renders. They must be checked at 0.25x in the first build. |
| `seats/emil-kowalski.md` sections 5 and 7 | The targets: float y ±0.06 m 2.4 s, x ±0.03 m 3.7 s, yaw ±8° 5.1 s; ghost wave ±20°, 2 times. |
| `~/.claude/skills/improve-animations/AUDIT.md` | To run on the first build, not on stills. |

The brief blocks none of my tools.

## Items

- **E1 rest pose alive and kind: FAIL.**
  - Fact: `turn-front.png` shows a perfectly upright body, two arms of the same shape sticking out flat at the same height, and level eyes. The pose is mirror-symmetric, like a T-pose.
  - Fact: `hero.png` and `turn-34.png` show the same: no tilt, no lean, both arms flat at one height.
  - Fact: `node 7 float` in `ghostie.glb` has `rotation` = none, and `arm_L` / `arm_R` have `rotation` = none (glTF node list). So the rest pose has no tilt and no asymmetry.
  - Opinion: it reads **kind** (round dome, wide-set eyes, no mouth, small next to Kit in `lineup-grass-crop-x3.png`). It does not read **alive**. At card size it looks like a mannequin, and the polygon crown makes that worse. The float gap and shadow are the only life in the still.
  - Opinion: at the 26 m camera (`lineup-grass-crop-x3.png`) the stiffness mostly disappears. But Rega accepts the card, and the card shows the rest pose.
- **E2 parts allow the motion: PASS.**
  - Float bob: PASS. Fact: node tree is root > float > body, eyes, arm_L, arm_R, acc_* (`ghostie.glb`), and `float` carries `float_rest_m` 0.22. Fact: `ingame.html` L118-119 drives `float.position` x ±0.03 m / 3.7 s, y ±0.06 m / 2.4 s and yaw ±8° / 5.1 s. This is exactly my section 7.
  - Arm wave: PASS. Fact: `arm_L` and `arm_R` are own nodes with a pivot on the body surface and `pivot_axis_blender` extras (`ghostie.glb`). Fact: `ingame.html` L120-122 swings `arm_L` by a `wave` angle. Fact: `_close-wave.png` and `_ingame-wave.png` show the arm lifted 30°, and Blender and three.js match. Opinion: drive `wave` as ±20°, 2 times, on the `pop` spring in the build.
  - Drain from recruiter in 3 steps: PASS (Opinion; no render shows it). The 3 steps are colour drains, legs fade, it floats (`seats/illustrator.md` L64; bible L30, Viet pick c). Fact: the body has its own `ghost` material, and `rgbToon` uses `MeshToonMaterial` with `color` (`ingame.html` L36-37), so the colour can tween from recruiter colours to white. Fact: `float` can rise from 0 to its 0.22 m rest. Fact: `acc_tie` and `acc_headset` echo Ricky's tie and headset (bible L29), so the identity carries across the swap. The legs belong to the recruiter mesh, not to this one. Fact: all 3 materials are opaque (no `alphaMode`), so any fade needs `transparent = true` at runtime. That is a build note, not a block.
- **Builder-flagged arm outline break: does not block (Opinion).**
  - Fact: `crops/arm-wave-blender.png` and `_close-wave.png` show the raised arm's top ink stroke start inside the body face, unconnected, and the arm root has no ink where it lies on the body.
  - Fact: `hero.png` shows a small stray stroke at the right arm root even at rest.
  - Opinion: the wave lives about 320 ms inside the ghosting beat (`seats/emil-kowalski.md` section 5), and at 26 m the arm is about 3 px of a 27 px body (`ingame_report.json`). Nobody sees it in play. It matters only if a card or a close-up shows the wave pose. So: never use the wave pose on a card. Keep it as a known limit, like Kit's head facets.

## Narrowest fixes for E1

All three are node rotations or one constant. No mesh, triangle or material change.

1. Give `float` a rest tilt: roll 4-6° and lean forward 3° toward the viewer. A still ghost then looks like it is drifting, not standing. `pose()` sets only `rotation.y`, so keep the tilt on x and z, or in a parent, so it survives.
2. Break the arm symmetry at rest: `arm_L` up 10-15° (ready to wave), `arm_R` down 8-10° and slightly forward. The wave then starts from a pose that already leans into it.
3. Re-render `hero.png`, `turn-*.png`, `variants.png` and `ingame*.png`. Check that the stray stroke at the arm root in `hero.png` is not worse.

Then E1 needs one re-check by me on the new `hero.png` and `turn-front.png`.

**Overall: FAIL** (E1 must item. E2 passes. The arm outline break is accepted as a known limit.)
