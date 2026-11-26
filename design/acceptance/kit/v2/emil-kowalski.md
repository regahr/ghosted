Emil Kowalski (Principal Designer): Kit v2, items E1-E2

## Offer

| Tool (path) | How it changes the answer |
|---|---|
| `~/.claude/skills/emil-design-eng/SKILL.md` (Springs, "Elements that should feel alive"; "Never animate from scale(0)") | Sets the bar for E1: a still pose must already hint at the spring it will move on. |
| `design/seats/emil-kowalski.md` L17-32 (rig), L36-38 (idle), L40-49 (hop) | The spec that E2 is checked against, node by node. |
| `~/.claude/skills/improve-animations/AUDIT.md` | Not used here. There is no motion yet to audit. Run it on the first build. |

The brief blocks none of my tools.

## Scores

| Item | Verdict | Evidence |
|---|---|---|
| E1 [must] rest pose alive and kind, not stiff | **PASS (narrow)** | **Fact:** `assets/kit/hero.png` and `turn-34.png` show a soft smile, eye highlights, blush, a curled sprout and a head tilt toward the briefcase (`build_kit.py` L549-550: -3, 5, -4 deg). It reads kind and alive. **Opinion:** the body alone is stiff. In `turn-front.png` both arms hang at the same angle, both legs are locked parallel and both feet point straight ahead. The face carries the pose, and the body does not. |
| E2 [should] rig allows hop, squash and stretch, sprout spring | **PASS** | **Fact:** `kit.glb` nodes are root > bounce > body (origin at the feet, y 0) > head (pivot at the neck, y 0.6) > sprout (pivot at its root on the crown, `build_kit.py` L386-396) and 5 face sets. The briefcase pivots at the grip (L545). This matches my spec, `design/seats/emil-kowalski.md` L19-25. Per-expression sprout rest rotation and scale sit in face-node extras (`build_report.json`, kit.glb). |

## Fix notes (none block the gate)

1. **E1, one asymmetry in the body (Opinion).** Drop the briefcase shoulder 2-3 deg, turn the free hand a little forward and open it, and toe out one foot 8-10 deg. Today the face alone carries the life. At the 26 m camera (`ingame-world-crop-x3.png`) the face is hardly visible, so the body must also carry it.
2. **E2, blink has no node (Fact vs spec).** My spec `emil-kowalski.md` L37 needs eyes scaleY 0.1 for 110 ms. The eyes are merged into each `face_*` mesh, so blink is not possible. Add a `face_blink` set, or split the eyes into their own node with a pivot at the eye centre.
3. **E2, sprout spring target (Opinion).** The game must use the face's `sprout_quat_three_xyzw` and `sprout_scale_three_y` as the spring's rest value and spring toward it on an expression swap. It must not set them directly, or the sprout snaps. Also keep squash on `bounce` only: the head has a rest rotation, so a non-uniform scale above it shears the head a little. This is acceptable inside the 0.88-1.10 clamp, but do not scale `body` too.

## Overall

Kit v2 passes E1 (must) and E2 (should). E1 is a narrow pass: fix note 1 is the first polish item for the build.
