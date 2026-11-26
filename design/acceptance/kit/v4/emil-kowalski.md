Emil Kowalski (Principal Designer): Kit v4, items E1-E2

## Offer

| Tool (path) | How it changes the answer |
|---|---|
| `~/.claude/skills/emil-design-eng/SKILL.md` (Spring Animations: "Elements that should feel alive", "Interruptibility advantage"; Cohesion: "match the motion to the mood") | The bar for E2. Each per-expression sprout shape must be a spring target, not a value set in one frame. This is the base for fix note 1. |
| `design/acceptance/kit/v3/emil-kowalski.md` (fix notes 1-3) | The v3 notes that this v4 pass checks again. |
| `~/.claude/skills/improve-animations/AUDIT.md` | Not used. There is still no game motion to audit. Run it on the first in-game hop. |

The brief blocks none of my tools. I judged only from the PNGs, the `kit.glb` node data, the `build_kit.py` v3-to-v4 diff and `ingame.html`. I did not use `changes.md` or `selfcheck.md` as evidence.

## Scores

| Item | Verdict | Evidence |
|---|---|---|
| E1 [must] The rest pose reads as alive and kind, not stiff | **PASS** | **Fact:** `build_kit.py` L291 moves the case wrist WL from x 0.256 to 0.286, and L335 sets `CASE_OUT = 0.056` (v3: 0.012). In `assets/kit/turn-front.png` the case arm now angles out about as far as the free arm, but the two hands stay at different heights (free hand at the hip, case hand lower), the head tilt stays (glb `head` rotation is non-zero) and the shoes still toe out. In `turn-side.png` the case hangs straight under the fist. **Opinion:** `hero.png` and `turn-34.png` still read as a kind, slightly shy person who waits. The case now reads as light and swung a little clear of the leg, not as held out with effort. It is not stiff and not awkward. The front view lost a little of the v3 "one arm free, one arm weighted" contrast, so this is a pass with less margin than v3. |
| E2 [should] The rig allows the hop, squash and stretch, and the sprout spring | **PASS** | **Fact:** the `kit.glb` tree is unchanged: root > bounce > body > {briefcase, head > {eyes_x5, face_x5, sprout}}. `bounce` is an empty node for squash. The five `eyes_*` nodes sit at head-local (0, 0.167, 0.175) for the blink. The briefcase mesh Z bounds are -0.231 to +0.002, so its origin is at the handle top and it can swing as a pendulum. The new sprout shapes are transform data only, with no new mesh: `face_rejected` extras quat (0, 0, 0.469, 0.883) = 56 deg bend; `face_focused` extras `sprout_scale_three_xyz` [0.4, 1.12, 0.4] = thin and stiff. Every channel can be interpolated, so a spring can carry each shape. `ingame.html` L74-75 reads these extras. |

## Fix notes (none block the gate)

1. **The sprout still snaps, and v4 adds a third channel (Fact, game-side).** `ingame.html` L74-75 `setExpr` still writes `quaternion.fromArray(...)` and `scale.fromArray(...)` directly. Focused now jumps the x/z scale from 1.0 to 0.4 in one frame. The game must use these values as spring targets only: slerp the quaternion and lerp all three scale axes with one critically damped spring (bounce about 0.2, about 350 ms). Give the shrink to 0.4 a small overshoot (to about 0.36, then settle), so "focused" reads as a twang and not a swap.
2. **The focused sprout thins its own outline (Opinion, check it).** `ingame.html` L65-66 adds the outline hull as a child of the `sprout` node, so the 0.4 x/z scale also scales the hull. At game distance (`expr-gamecam-strip.png`, focused) the sprout already reads as a thin wire. If the outline width is in object space, it drops to about 40% on that one part. Either keep the x/z scale at 0.55 or more, or divide the outline width by the node scale.
3. **Do not push the case further out, and let it swing (Opinion).** v4 is at the edge: one more step and both arms flare the same way, and the pose goes symmetric and stiff. Keep `CASE_OUT` at 0.056 or less. In the game, give the briefcase a lagged pendulum on its top pivot (rotate about local X/Z, spring bounce about 0.3, max about 12 deg) during the hop. That swing is what will make the carried case read as weight. Keep squash on `bounce` only (clamp 0.88-1.10), as in v3.

## Overall

Kit v4 **PASSES** E1 (must) and E2 (should). The wider case arm does not make the pose stiff or awkward, but it uses up most of the margin, so hold it there. The per-expression sprout shapes are good rig design, because they are pure transform data that a spring can carry. The viewer still sets them directly (fix note 1), and the game build must fix that.
