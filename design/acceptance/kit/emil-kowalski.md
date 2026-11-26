Emil Kowalski (Principal Designer): Kit v5, items E1-E2

## Offer

| Tool (path) | How it changes the answer |
|---|---|
| `~/.claude/skills/emil-design-eng/SKILL.md` (Spring Animations: "Elements that should feel alive", "Interruptibility advantage"; Cohesion: "match the motion to the mood") | The bar for E2: the case swing and the sprout must be spring-driven, so the rig must give each one a clean pivot and transform-only channels. |
| `design/acceptance/kit/v4/emil-kowalski.md` (fix notes 1-3) | The v4 notes this pass checks again: note 3 asked for no wider case and a pendulum pivot at the handle top. |
| `~/.claude/skills/improve-animations/AUDIT.md` | Not used. There is still no game motion to audit. Run it on the first in-game hop. |

The brief blocks none of my tools. I judged from the PNGs, the `kit.glb` node data and `build_kit.py`. I did not use `changes.md` or `selfcheck.md` as evidence.

## Scores

| Item | Verdict | Evidence |
|---|---|---|
| E1 [must] The rest pose reads as alive and kind, not stiff | **PASS** | **Fact:** `assets/kit/build_kit.py` L291-293: elbow EL (0.168, 0.068, 0.410), wrist WL (0.230, 0.100, 0.322) from shoulder SL (0.124, 0, 0.518, L290). From these points the upper arm is 22.2 deg out in the front plane and the elbow bends about 18 deg. L344 `CASE_OUT = 0.0`. `turn-side.png` shows the fist behind the hip line with the case straight under it. In `crops/arm-front-v4-v5.png` the v5 arm hangs closer to the torso than in v4. **Opinion:** the v3 contrast I asked for is back, and stronger. In `turn-front.png` and `turn-34.png` the free arm flares out with an open hand at hip height. The case arm hangs lower and closer, and the case hangs plumb, so it reads as weight. With the head tilt, the toe-out and the smile, `hero.png` reads as a kind, slightly shy person who waits. The bent elbow takes away the straight-rod look of v4. This is the best rest pose so far, and it now has margin. |
| E2 [should] The rig allows the hop, squash and stretch, the sprout spring, and the case pendulum | **PASS** | **Fact:** `kit.glb` tree is root > bounce > body > {briefcase, head > {eyes_x5, face_x5, sprout}}. `bounce` is an empty node for squash. The `briefcase` node is at (0.250, 0.294, -0.110). Its mesh Y bounds are -0.231 to +0.002 and its X/Z bounds are symmetric about 0. So the origin is at the handle top, centred, and sits at the grip point (`build_kit.py` L308-309, `HCL = WL + dL * 0.036`; 0.230 + 0.554 * 0.036 = 0.250). The pivot is inside the fist. The pendulum turns about the hand, not about the case centre. **Opinion:** my clearance estimate: the case's inner edge sits at about x 0.18 and the leg's outer edge at about x 0.12. A 12 deg swing toward the body moves the case bottom in by about 5 cm, and it still clears the leg. |

## Notes (none block the gate)

1. **The sprout still snaps (Fact, game-side, carried from v4 note 1).** `assets/kit/ingame.html` (not changed since v4) L74-75 `setExpr` still writes `quaternion.fromArray(...)` and `scale.fromArray(...)` directly. In the game, use these values only as spring targets. Use one critically damped spring with bounce about 0.2 over about 350 ms, and a small overshoot on the focused shrink.
2. **Freeze this arm (Opinion).** v5 resolves v4 note 3. Do not move WL, EL or `CASE_OUT` again without another E1 check, because the asymmetry is what makes the pose work.
3. **Case pendulum spec for the game (Opinion).** Rotate `briefcase` about its local X and Z, lagging the `bounce` node's vertical velocity. Use a spring with bounce about 0.3 and clamp it at about 12 deg. Keep squash on `bounce` only (0.88-1.10) so the case is never scaled. At about 12 deg the case still clears the leg. Above about 18 deg, test for clipping against the leg.

## Overall

Kit v5 **PASSES** E1 (must) and E2 (should). The relaxed, bent case arm with a plumb case brings back the "one arm free, one weighted" read with more margin than v3 or v4. The rig keeps the squash node and the transform-only sprout channels, and the briefcase origin now sits at the handle top inside the fist, which is the right pendulum pivot.
