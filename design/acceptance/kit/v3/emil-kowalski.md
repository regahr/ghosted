Emil Kowalski (Principal Designer): Kit v3, items E1-E2

## Offer

| Tool (path) | How it changes the answer |
|---|---|
| `~/.claude/skills/emil-design-eng/SKILL.md` (Spring Animations: "Elements that should feel alive", "Interruptibility advantage") | Sets the bar for E2: the sprout must spring toward a rest value and must not be set directly. This is the base for fix note 1. |
| `design/acceptance/kit/v2/emil-kowalski.md` (fix notes 1-3) | The v2 notes that this v3 pass checks one at a time. |
| `~/.claude/skills/improve-animations/AUDIT.md` | Not used. There is still no game motion to audit. Run it on the first in-game hop. |

The brief blocks none of my tools. I judged only from the PNGs, `kit.glb` node data, `build_kit.py` and `ingame.html`. I did not use `changes.md` or `selfcheck.md` as evidence.

## Scores

| Item | Verdict | Evidence |
|---|---|---|
| E1 [must] The rest pose reads as alive and kind, not stiff | **PASS** | **Fact:** in `assets/kit/turn-front.png` the body is no longer symmetric. The free arm (Kit's right) comes out and forward. The case arm hangs straight down under the weight. `build_kit.py` L289-292 puts the shoulders at z 0.518 and 0.528 and the wrists at different positions. The right shoe toes out 9 deg (L325). The head tilt stays (L672). **Opinion:** `hero.png` and `turn-34.png` now read as a kind, slightly shy person who is waiting for something. The body helps the face, and in `ingame-world-crop-x3.png` the flared free arm still shows at game distance. In v2 this was a narrow pass. Now it is a clear pass. |
| E2 [should] The rig allows the hop, squash and stretch, and the sprout spring | **PASS** | **Fact:** the `kit.glb` tree is root > bounce > body > {briefcase, head > {eyes_x5, face_x5, sprout}}. Each `eyes_<expr>` is its own node at head-local (0, 0.167, 0.175). The mesh Y bounds are -0.0236 to +0.0239, so the pivot is at the eye centre and `scale.y = 0.1` closes the eyes in place. `ingame.html` L77 `kit.userData.blink` drives the eye nodes. The sprout pivots at its root (t 0, 0.37, -0.034). The face extras carry `sprout_quat_three_xyzw` and `sprout_scale_three_y`. `bounce` is an empty node, ready for squash. All v2 E2 gaps are closed. |

## Fix notes (none block the gate)

1. **Sprout snaps on an expression swap (Fact, game-side).** `ingame.html` L69-74 `setExpr` writes `nodes.sprout.quaternion.fromArray(...)` and `scale.set(...)` directly. That is fine for a still viewer. In the game, use those values as the spring *target* only (for example, slerp toward the target with a critically damped spring, bounce about 0.2, about 350 ms). Otherwise `ghosted` drops the sprout 74 deg in one frame, and the sprout is the most alive part of Kit.
2. **The open hand reads as a fist (Opinion).** In `turn-front.png` and `hero.png` the free right mitten (L310-314) reads as a round lump, not an open palm. The thumb lobe does not show at the front or 3/4 angle. Make the mitten flatter (y 0.021 to about 0.016) and move the thumb lobe about 1 cm further out. This is polish, not a gate item.
3. **Keep squash on `bounce` and blink on `eyes_*` (Opinion, carried over from v2).** Do not put a non-uniform scale on `body` or `head`: the head has a rest rotation (L672), so scaling under it shears the face. Clamp squash to 0.88-1.10. Run blink as scale.y 1 > 0.1 > 1 over 110 ms, at random 2.5-5 s gaps, and do not blink during the hop's squash frame.

## Overall

Kit v3 **PASSES** E1 (must) and E2 (should). All three v2 notes are fixed in the asset: the uneven stance, the eyes as their own node for blink, and the bounce node for squash. The sprout spring is set up as data, but the viewer still snaps it (fix note 1). The game build must fix that.
