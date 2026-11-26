# The centred tie reads as a mouth at the game camera

Pictures:
- `i-evidence.png`: real renders of the tie, at card size and at the game camera.
- `j-tie-options.png`: one panel for each option.

All files are local and unpushed. The folder has no git repo, so there is no commit sha. The base folder is
`design/`.

## What I promised
Slack ts 1795609829.506569 (my question): "If the centred tie still reads as a mouth there, I stop and bring you the
evidence, with no more tie shapes." You picked that option, ts 1795614083.836699: "ok ur pick".

## The evidence (real three.js render, not an estimate)
- `assets/ghostie/blockout/measure.md`: at 1x, on screen, below the eye dots:
  - collar top +4.1 px;
  - knot top +4.5 px;
  - V point +13.7 px.
- `assets/ghostie/blockout/crops/tie-ghost-gamecam-x9.png`. Viet's read (Opinion):
  > "the collar's dark ink edge makes a short line under the eyes that reads as a lip. The lilac tie hangs below it as a rounded tongue."
- At card size, `assets/ghostie/blockout/front-variants.png`, it reads as a tie.
- This matches BMGD in v2, `acceptance/ghostie/v2/bmgd.md` L24:
  > "Any centred mark on the front, below the eyes, lands in the mouth zone, however low it sits on the body."
- The glasses and the headset read at both sizes. The headset is now centred, with 2 cups.

Six tie placements have now failed at the game camera: centred, low, over the shoulder, blown up, askew, and centred
with a collar. So the conflict is the tie itself against the top-down camera and the no-mouth rule. It is not a drawing
problem.

## Options (picture: j-tie-options.png)
1. **Swap the tie for a held prop.** My pick.
   - The 3rd variant holds a recruiter prop in `arm_R` at the side: a clipboard, a coffee mug or a phone. Nothing sits
     in the face zone.
   - The Illustrator sketches the 3 props, and Viet renders a blockout at the game camera before you see them.
   - The glasses and the headset stay.
2. **Tie at card size only.** In game, the tie ghost shows no tie, so it is a plain ghost and 2 variants read in game.
3. **Change the no-mouth rule.** The bible's "a ghost never replies" (`bible.md` L30) goes, and the tie stays as built.

## Also found (no decision needed)
The 2-cup headset is 656 triangles, over the 600 cap (`assets/ghostie/blockout/ingame_report.json`). The final model
needs a cheaper cup or band. That is Viet's fix.
