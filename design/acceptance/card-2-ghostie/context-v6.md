# Ghostie 3D v6: closest yet, but the outline is polygonal at 600 triangles

Pictures:
- `m-v6-evidence.png`: v6 against the sketch, plus crops of the dome and the hem, plus the game camera.
- `n-budget-options.png`: one panel for each option.

All files are local and unpushed. The folder has no git repo, so there is no commit sha. The base folder is
`design/`.

## What v6 is
v6 is the final model, built to sketch v2 and the body map (`assets/ghostie/v6/`). Before modelling, Viet ran the
ready check and the skill steps (`v6/ready.md`, `v6/direction.md` and the output in `v6/skill/`).

**What passes, per Viet's self-check (`v6/selfcheck.md`):**
- an upright, symmetric mesh, with the tilt on the float node;
- 1 skinned mesh;
- the eyes on the body-map line;
- the tie, with its collar joined to the knot, at 40 triangles;
- the glasses, with an ink edge that reads at 1x;
- the headset, centred, with 2 level cups, at 584 triangles;
- the palette;
- Blender matching three.js (mean difference 0.73/255).

## What I decided as chair (the seat that owns each item)
- **Wave shoulder** (Viet, the 3D method): use a sculpted wave pose shape (a morph target). It costs 0 triangles.
  Bone weights alone failed 3 times (`v6/selfcheck.md`).
- **The rest arm on a ghost turned 34°** (Emil, the pose): Emil sets a stronger forward swing, so the tip stays under
  the eyes. Measured: -1.8 px (`v6/measure.md`).

## Your call: the budget
- The outline has failed on facets in every version: v1 failed on 8 segments
  (`acceptance/ghostie/v1/illustrator.md` L15), and v2 and v3 failed on crown corners.
- v6 at 600 still shows straight steps on the dome and a zigzag hem at 2x (`v6/crops/dome-front-x2.png`,
  `hem-front-x2.png`).
- Viet, `v6/selfcheck.md`: a smooth card read needs about 800 per variant.
- Card 2 showed you 600 as a chair call you could overrule. This would change it again.

## Options (picture: n-budget-options.png)
1. **Raise the cap to 800 per ghost.** My pick.
   - 24 ghosts come to 19.2k triangles, about 8 Kits.
   - v7 gets a smooth dome and round hem scallops, like the sketch, plus the wave shape and the rest pose.
   - Then the 5-seat 3D gate, then the 3D card.
2. **Keep 600 and accept the steps.** Add the wave shape and the rest pose, then the 3D gate.
3. **Keep 600 and draw only a smoother ink outline at run time.** The outline is smooth, the shading stays faceted,
   and the extra triangles are hidden in the outline.
