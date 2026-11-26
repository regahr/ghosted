# Emil Kowalski (Principal Designer): Ghostie v3, E1 and E2

I judged from the PNGs, the node tree in `assets/ghostie/ghostie.glb` (read with a local Python script) and `pose()` in `assets/ghostie/ingame.html`. I read the builder notes (`changes.md`, `selfcheck.md`) as claims only, and checked each claim I use against a file. All paths below are under `assets/ghostie/`.

## Offer

| Tool (path) | How it changes the answer |
|---|---|
| `~/.claude/skills/emil-design-eng/SKILL.md`, "Should this animate at all?" frequency table | The wave plays only inside the 750 ms ghosting beat, at the 26 m camera. A flaw that shows only in the wave pose at close-up costs little. |
| same file, "Spring Animations" (bounce 0.1-0.3) and "Slow motion testing" | The wave runs on a soft spring and gets checked at 0.25x in the first build. Stills cannot prove how the motion feels. |
| `seats/emil-kowalski.md` sections 5 and 7 | The motion targets. The float is unchanged. The v2 wave target (±20° about rest) now needs a new value, see E2. |
| `~/.claude/skills/improve-animations/AUDIT.md` | Use in the first build, not on stills. |

The brief blocks none of my tools.

## Rig check

- `float` rest rotation: PASS. **Fact:** `ghostie.glb` node 8 quaternion (0.0262, 0.0011, 0.0436, 0.9987) = X +3.0°, Z +5.0°. The roll is flipped from v2 (-5°) to +5°, as the brief asks.
- `arm_L` rest rotation: PASS. **Fact:** node 4 quaternion = X +3.4°, Z +4.9°. That is about 6° up on the +x side, on top of the 30° droop in the mesh (`changes.md` "net 24°"). Translation y 0.10 (v2: 0.16), so the root is lower.
- `arm_R` rest rotation: PASS. **Fact:** node 5 quaternion = Z +3.0°, Y +8.0°. On the -x side, this lowers the arm 3° and turns it forward 8°. `arm_L` stays higher than `arm_R`.
- Roll and arms add up: PASS. **Fact (from the numbers):** in world terms, +5° roll lifts the `arm_L` side and lowers the `arm_R` side. So `arm_L` hangs about 19° below level, and `arm_R` about 38° below level. In v2 the roll cancelled the lift. Now the roll adds to it.
- `pose()`: PASS. **Fact:** `ingame.html` L117 stores `restQ`. L121 does `quaternion.copy(restQ).premultiply(yaw)`, so the lean and roll stay during the float. L119 moves x/y on position only. L122-124 swing `arm_L` about `h = armDir x up`, in the vertical plane of the arm.
- Node tree: PASS. **Fact:** `float` children are acc_glasses, acc_headset, acc_tie, arm_L, arm_R, body, eyes (node 8). `arm_collars` is gone.

## Items

- **E1. The rest pose reads alive and kind: PASS.**
  - **Fact:** `turn-front.png`: the hem is lower on the viewer's left (about y 835) than on the right (about y 800). The viewer-right arm sits about 55 px higher (y 640-710) than the viewer-left arm (y 700-770). The tilt and the higher arm are on the same side.
  - **Fact:** `lineup-grass-crop-x3.png`: the three ghosts at the 26 m camera each have a different lean and yaw. They read as drifting next to Kit.
  - **Opinion:** the pose reads alive. In v2, the life came only from the head tilt. Now it also comes from the arms. It still reads kind: a round dome, wide soft eyes, no mouth, small next to Kit.
  - **Opinion:** the "ready to wave" lean reads on `turn-front.png`. One side lifts and the other arm hangs. It reads only weakly on `hero.png`. There the near arm is a short flap that points out at about 30° down (x 790-890, y 660-740), and the far arm shows only as a nub (x 330-345). On the card it reads as "relaxed, one arm out", not "about to wave". That is enough for E1. The lean was a polish note, not a gate item.
- **E2. The parts allow the float, the wave and the 3-step drain: PASS.**
  - Float: PASS. **Fact:** the tree is root > float > all parts (nodes 8-9). `float_rest_m` is 0.22, and L119-121 drive x ±0.03 m / 3.7 s, y ±0.06 m / 2.4 s and yaw ±8° / 5.1 s.
  - Wave rig: PASS. **Fact:** `arm_L` is its own node, with its pivot at the root (translation 0.211, 0.10) and `pivot_axis_blender` in its extras. **Fact:** `_close-wave.png` (Blender) and `_ingame-wave.png` / `crops/arm-wave-threejs.png` (three.js) show the same pose with the arm lifted 30° (`render_ghostie.py` L184 `WAVE_DEG = -30`; `shoot_ingame.mjs` L21 `wave: 30`). Blender and three.js match.
  - Friendly wave with the new arm: PASS, with a build note (**Opinion**). The arm now hangs about 19° below level at rest. The v2 spec of ±20° about rest takes the tip from about 39° down to about level. It never goes above the root, so it reads as a flipper pat, not as a "hi". In `_close-wave.png`, the 30° lift brings the flap to just above level. For a friendly wave, the swing must reach 35-45° up from rest, so the tip clears the root. This is one number in the first build. It needs no mesh change.
  - Drain: PASS (**Opinion**, no render shows it). **Fact:** the materials `ghost`, `tie`, `ink` and `acc` have no `alphaMode`, so they are opaque. `rgbToon` makes a `MeshToonMaterial` with `color` (`ingame.html` L35-36), so the colour can tween to off-white. `float` can rise from its 0.22 m rest. Any fade needs `transparent = true` at runtime. This is a build note, as in v1 and v2.
- **Wave-pose ink at the root: does not block (a known limit, worse than in v2).**
  - **Fact:** `_close-wave.png` and `_ingame-wave.png` show a long ink stroke on the body face, from about (930, 640) to (1080, 800) out of 1200. This is the lifted flap's top outline, drawn over the body. `selfcheck.md` V2 item 2 reports the same root stroke at rest, end-on (`crops/arm-end-on-side.png`).
  - **Fact:** at rest the root is clean in `crops/arm-root-front.png`, apart from the small sliver that Viet reports there.
  - **Opinion:** the wave lives about 320 ms inside a 750 ms beat at 26 m. Nobody sees this stroke in play. Keep the rule: never use the wave pose on a card. At a 35-45° lift, the stroke will grow, so check it once at the game camera in the first build.
- **Not my item, seen while judging (Opinion, for Viet and the Illustrator):** `ingame.png` has a faint dotted line on the body face (about x 260-360, y 670-800). In `turn-front.png`, the tie has a thin dark sliver next to its blade (x 580-615, y 470-520). Near the eyes, that reads more like a scratch than a tie.

## Optional polish (not gate items)

1. In the build, change the wave target from ±20° about rest to an upward swing of 0 to +40° from rest, 2 times, on a soft spring (bounce about 0.2). Check it at 0.25x.
2. If the card should say "about to wave", turn the hero camera about 10° so that the near arm shows its flat face, or lift `arm_L` rest by 4-6° more. This is one constant each. Do it only if the Illustrator and Viet do not object, because it moves the arm toward the eye line (the ear concern).

**Overall: PASS** (E1 and E2 pass. The wave needs a larger upward swing in the build. The root ink in the wave pose is a known limit: no wave pose on a card.)
