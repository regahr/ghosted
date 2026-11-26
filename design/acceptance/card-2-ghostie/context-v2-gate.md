# Sketch v2: 5 of 5 seats fail it on small visible flaws

Pictures:
- `k-v2-flaws.png`: the flaws, as 2x crops.
- `l-v2-options.png`: one panel for each option.

All files are local and unpushed. The folder has no git repo, so there is no commit sha. The base folder is
`design/`.

## Why I ask before fixing
The council rule "No blind iterations" (`~/.claude/skills/council/SKILL.md`, from your ts 1795607727.200129) says that
when the same item fails twice, I stop and bring it to you. The headset failed in sketch v1 (it slipped down one side)
and again in v2 (it sits on the forehead).

## What passes
- The body map, its proportions and its landmarks. Viet: they match the real blockout within 1 unit.
- The palette and the value against the grass and the path (Lena).
- No mouth, the tone, the tie that reads as a tongue (your ruling), and where the accessories sit (BMGD).
- The wave, which clears the tie (Emil).
- The budget path to 600 for the headset (Viet): a cheaper cup and a thin band.

## What blocks (seat files in `acceptance/ghostie/sketch-v2-gate/`)
1. **Headset band** (`emil.md`, `lena.md`, `illustrator.md`, `bmgd.md`, `viet.md`): it has no ink and sits inside the
   crown outline, so it reads as a stripe on the forehead.
2. **Glasses at the game camera** (`lena.md`, `bmgd.md`): the pale rims have no ink. In the real render they are a ring
   under 1 px, so the ghost looks tired or bruised. The fix is thicker rims with an ink edge.
3. **Rest pose** (`emil.md`, `bmgd.md`): a hook, like a claw, under the drooping arm.
4. **3/4 view** (`viet.md`): the far arm is missing, so it disagrees with the 3D.
5. **Side view** (`illustrator.md`, `bmgd.md`, `viet.md`): the tie is drawn face-on, not edge-on, and the arm oval reads
   as a hole.
6. **Labels on the body map:** a stray tick, two body heights (265 and 280), and a double line. The sheet's
   game-camera tiles should be the real render.

## Root cause
- The Illustrator's own self-check (`assets/ghostie/sketch/flaws.md`) said "none seen" on these panels.
- My own 2x read (`acceptance/ghostie/chair-read-sketch-v2.md`) missed the headset and the arm hook.
- The new whole-picture check by 5 independent seats caught them. So the gate works, but the builder's check and mine
  do not.

## Options (picture: l-v2-options.png)
1. **One 2D fix pass (sketch v3).** My pick. The Illustrator fixes the merged list above. I check at 2x, then only the
   seats whose items changed check again, then card 2 comes to you. No Blender work.
2. **Fix in 3D directly.** You accept v2 together with the fix list, Viet builds the final model with the fixes, and
   the 3D gate checks them.
3. **Park the Ghostie.** I keep v2 and the fix list on file, start Recruiter Ricky with a body map first, and come back
   to the Ghostie later.
