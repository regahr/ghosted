# Ghostie after 5 passes: how do we finish it?

Pictures:
- `e-tie-history.png`: the tie variant from v1 to v5.
- `e-options.png`: one panel for each option.

All files are local and unpushed. The folder is not a git repo, so there is no commit sha. The base folder is
`design/`.

## Your rule for the Ghostie

Slack C0CHA2A1DM1, ts 1795604718.933169, (private Slack thread)
> "do it after ghostie, let 3d artis finish with ghostie first"

I followed it, but the 3D version is not converging. So I ask before I spend another pass.

## Where it stands

| Version | Gate | What failed |
|---|---|---|
| v1 | FAIL 5 of 5 seats | faceted look, pink shadow, tie read as a mouth, stiff pose |
| v2 | FAIL 3 of 5 | corners, arms read as ears, tie read as a mouth |
| v3 | FAIL 3 of 5 | arms read as ears, arm seams, tie read as a strap |
| v4 | not gated in full | the builder found that the arm join cannot close with separate arm meshes; tie read as a quill or horn (`acceptance/ghostie/v4-tie-bmgd.md`, `v4-tie-illustrator.md`) |
| v5 | not gated yet | one-mesh body with skinned arms; the arm hook is gone. New: an ink crease line across the body, and the tie sticks out sideways below the eyes |

What now passes and stays:
- the body and the crown;
- the colours (Lena PASS v2 and v3);
- the pose and motion (Emil PASS v2 and v3);
- the arms below the eyes at the game camera (eye gap 3.8-6.6 px, `assets/ghostie/selfcheck.md`);
- 568-596 triangles of 600, in 1 non-swap mesh.

The tie is the part that keeps failing:
- BMGD, `acceptance/ghostie/v4-tie-bmgd.md`: "My own v3 fix asked for exactly what v4 built. It left out how wide the
  blade must be and that the tip must be a V. The miss is in my brief, not in the build."
- My own read of v5, `assets/ghostie/variants.png`: the tie sticks out sideways just below the eyes, so it can read as
  a party horn in the mouth.

Each tie shape was written in words and then built in Blender. That is the problem your sketch-first rule fixes
(ts 1795604691.829739: "illustrator always provide draft sketch first, then 3d artist build based on it").

## Cost so far (Fact, from the agent run totals)
- Blender passes: about 310k-680k tokens each.
- Full 5-seat gate rounds: about 520k-560k tokens each.

## Options (picture: e-options.png)

1. **Sketch it now.** My pick.
   - The Illustrator sketches the Ghostie with the 3 accessories and a game-camera thumbnail next to Kit.
   - The seats score the sketch, and you accept it.
   - Viet rebuilds v6 to match it, and keeps the v5 one-mesh body.
   - Then the 5-seat gate, then card 2.
   This applies your sketch rule now, not at Ricky, and it decides the tie on paper.
2. **Keep going in 3D,** as you asked first. v6 fixes the crease line and tries the tie again, or a hanging tie like
   Kit's. The tie has failed 5 shapes so far.
3. **Ship 2 variants now.** Drop the tie variant for now. v6 fixes only the crease line, and the gate scores the
   glasses and headset ghosts. The tie comes back later through a sketch. This is the fastest way to card 2, but the
   ghosts lose one recruiter cue.

## What is not proved
- The crease line fix is not built yet. The builder thinks the outline shows through at the concave arm join.
- I have not seen an Illustrator sketch yet, so its quality is not known.
