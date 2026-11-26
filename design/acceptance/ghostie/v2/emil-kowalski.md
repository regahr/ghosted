# Emil Kowalski (Principal Designer): Ghostie v2, E1 and E2

Judged from the PNGs, the node tree in `assets/ghostie/ghostie.glb` and `pose()` in `assets/ghostie/ingame.html`. The builder notes (`changes.md`, `selfcheck.md`) were read as claims only, and each claim used here was checked against a file.

## Offer

| Tool (path) | How it changes the answer |
|---|---|
| `~/.claude/skills/emil-design-eng/SKILL.md`, "Should this animate at all?" frequency table | The wave plays only inside the 750 ms ghosting beat (bible L36), at the 26 m camera. A flaw that shows only in the wave pose at close-up costs little. |
| same file, "Spring Animations" (bounce 0.1-0.3) and "Slow motion testing" | The wave must run on a soft spring and be checked at 0.25x in the first build. Stills cannot prove motion feel. |
| `seats/emil-kowalski.md` sections 5 and 7 | The targets: float y ±0.06 m 2.4 s, x ±0.03 m 3.7 s, yaw ±8° 5.1 s; wave ±20°, 2 times. |
| `~/.claude/skills/improve-animations/AUDIT.md` | For the first build, not for stills. |

The brief blocks none of my tools.

## Fix 7 check (rig)

- `float` rest rotation: PASS. **Fact:** `ghostie.glb` node 8 `float` quaternion (0.0262, -0.0011, -0.0436, 0.9987) = X 3.0°, Z -5.0°. That is lean 3° and roll 5°, as asked.
- `arm_L` rest rotation: PASS. **Fact:** node 4 quaternion = about Z +12.0°, X +4.8°. At +x, this lifts the arm about 12°. Asked: 10-15° up.
- `arm_R` rest rotation: PASS. **Fact:** node 5 quaternion = Z +8.4°, Y +8.2°. At -x, this lowers the arm about 8° and turns it forward about 8°. Asked: 8-10° down, slightly forward.
- `pose()` keeps the tilt: PASS. **Fact:** `ingame.html` L115 stores `restQ`, and L119 does `quaternion.copy(restQ).premultiply(yaw)`. The yaw is added on top, around the world up axis, so the lean and roll stay at all times. L117 keeps the x/y float on position only.

## Items

- **E1. The rest pose reads alive and kind: PASS.**
  - **Fact:** `turn-front.png` shows the body rolled clockwise. The left eye sits about 20 px higher than the right, and the hem is lower on the right. The v1 mirror symmetry (`v1/turn-front.png`, level eyes, matching arms) is gone.
  - **Fact:** `hero.png`, `turn-34.png` and `ingame.png` show the lean and roll in 3/4. The outline is no longer a vertical stack, and the near arm and far arm sit at different heights.
  - **Fact:** `lineup-grass-crop-x3.png` shows the three ghosts at the 26 m camera, each at a slightly different lean and yaw. Next to Kit they read as drifting, not standing.
  - **Opinion:** it now reads alive: a small head-cock, like the ghost is listening. It still reads kind: round dome, soft wide eyes, no mouth, small next to Kit.
  - **Opinion, not blocking:** the roll goes the wrong way for the arms. A -5° roll lowers the `arm_L` side, so the 12° lift nets to about 7°. In `turn-front.png` and `hero.png`, both arms look close to level, and the "ready to wave" lean mostly does not read. The tilt carries the life, not the arms.
- **E2. The parts allow the float, the wave and the 3-step drain: PASS.**
  - Float: PASS. **Fact:** the tree is root > float > body, eyes, arm_L, arm_R, arm_collars, acc_* (`ghostie.glb` nodes 8-9). `float` has `float_rest_m` 0.22, and `ingame.html` L117-119 drives x ±0.03 m / 3.7 s, y ±0.06 m / 2.4 s and yaw ±8° / 5.1 s. This matches section 7.
  - Wave: PASS. **Fact:** `arm_L` is its own node, with its pivot at the body surface (translation 0.193, 0.16) and `pivot_axis_blender` in its extras. `ingame.html` L120-122 swings it about the axis made by crossing the arm direction with world up, so the arm flaps up and down from its rest angle. **Fact:** `_close-wave.png` and `_ingame-wave.png` show the arm lifted about 25°, and Blender and three.js match.
  - Wave with the new arm shape: PASS (**Opinion**). The v2 arm is a short round mitten (tip 68 mm, `changes.md`, seen in `_close-wave.png`). A stub that flaps up and down reads as a small "hi", which fits a shy ghost better than a long arm would. It is at the low end of readable: at ±20° and 26 m it is a few pixels. Drive it on a soft spring (bounce about 0.2) and check it at 0.25x in the first build.
  - Drain: PASS (**Opinion**, no render shows it). **Fact:** the body and arms use their own `ghost` material, all opaque (`ghostie.glb` materials, no `alphaMode`). `rgbToon` makes a `MeshToonMaterial` with `color` (`ingame.html` L35-36), so the colour can tween to off-white. `float` can rise from 0 to its 0.22 m rest. The tie stays as the link to Ricky (bible L28-30). Any fade still needs `transparent = true` at runtime. This is a build note, as in v1.
- **Wave pose ink at the root: does not block (known limit, as in v1).**
  - **Fact:** `_close-wave.png` shows the raised arm's top ink stroke start inside the body face, with no ink where the arm root meets the body. `selfcheck.md` L53 says why: the collar is fixed to the body.
  - **Fact:** at rest the root is closed (`crops/arm-root-front.png`), so the v1 stray stroke in `hero.png` is fixed.
  - **Opinion:** the wave lives about 320 ms inside a 750 ms beat at the 26 m camera. Nobody sees this in play. Keep the rule: never use the wave pose on a card.

## Optional polish (not a gate item)

1. Flip the `float` roll to +5° on three.js z (the `arm_L` side goes up). The tilt and the raised arm then add up, and the "ready to wave" lean reads in `hero.png`. One constant, no mesh change. Re-render `hero.png` and `turn-front.png` if this is done.

**Overall: PASS** (E1 and E2 pass. The wave-pose root ink is a known limit: no wave pose on a card.)
