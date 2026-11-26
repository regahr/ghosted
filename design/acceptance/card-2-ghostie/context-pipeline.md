# What supports the 3D model before Blender?

Picture: `f-pipeline.png`, one panel for each option. All files are local and unpushed; the folder has no git repo, so
there is no commit sha.

## Your question
Slack C0CHA2A1DM1, ts 1795607226.717639, (private Slack thread)
> "ok, so before blender, illustration, any other things gonna support u to do 3d drawing?"

## Answer: yes, 5 things, besides the sketch
1. **A full brief before any drawing.** It gives the triangle budget, the real game camera, the motion parts from Emil
   and Lena's palette. The Ghostie budget went from 300 to 450 to 600 during the build, because nobody set it from the
   design first (`acceptance/checklist.md`, chair amendments 2 and 3).
2. **A reference board and a written direction (`direction.md`).** This is step 1 of Viet's own skill:
   - `~/.claude/plugins/cache/3dviz-pro-max/3dviz-pro-max/0.1.0/skills/3dviz-pro-max/SKILL.md` L17-19 (local):
     > "Choose a distinctive visual idea, useful references and the intended viewing distance."
   - Viet's retro, `acceptance/ghostie/retro-viet.md`: "I looked at the mock sheet and Kit, but wrote no direction
     or references down."
   - The references come from this machine or from images you send. Web search only if you hand it over.
3. **The skill's search and context tools,** run and saved before modelling:
   - SKILL.md L37-39 (local): `scripts/search.py`, `resolve.py`, `design-context.py`.
   - The retro says these were "Not run".
4. **A blockout.** A rough, cheap 3D shape at the game camera, with the joins decided (continuous skin or separate
   parts), before the detailed model.
   - SKILL.md L33 (local):
     > "At important joins, decide whether the object needs a continuous skin, a layered covering or separate articulated parts."
   - In the Ghostie this decision came only at v5. It is what fixed the arm hook.
5. **A paint-over.** The Illustrator draws over the blockout render to correct the shapes, and the seats do a quick
   check. This catches 3D-only faults on the cheap model: the mouth zone and the ear read from the top-down camera, and
   the outline at joins.

## Options (picture: f-pipeline.png)
1. **Sketch only.** This is the rule today. Faults that only show in 3D appear late, at the full gate.
2. **Brief, reference board, sketch, blockout, paint-over, final model.** My pick. It adds two cheap checks before
   the expensive Blender detail. It goes into the council skill's "Game art pipeline", next to your sketch rule.

## Not proved
- How much time the blockout and the paint-over add. I expect less than one failed Blender pass (310k-680k tokens on
  the Ghostie), but I have not measured it.
- How good the Illustrator's paint-over is. The first one will show that.

Your earlier question is still open: how to finish the Ghostie (`context-ghost5.md`).
