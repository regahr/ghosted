# Where do the tie and the headset go on a ghost?

Picture: `h-placement.png`, one panel for each option. All files are local and unpushed. The folder has no git repo,
so there is no commit sha. The base folder is `design/`.

## Your question
Slack ts 1795609768.465229, (private Slack thread)
> "so u guys don't know where the headset position and tie position should be? why tie position far right and why
> only half visible on headset?"

## Answer: no. Nobody decided it.
A ghost has no ears and no neck. Nobody set where its "ears" and "neck" are, so each version placed the parts in a new
way.

- **Headset.** The only spec is `seats/illustrator.md` L70:
  > "3 variants by one faded accessory (`#c8c0d8`): tie, glasses (2 Torus), headset."
  It gives no position. The v1 builder put the band down one side to one cup. Every later version and the sketch
  copied it, and no seat asked why.
- **Tie.** It is far right as a workaround. BMGD found that the top-down camera turns any centred mark under the eyes
  into a mouth, `acceptance/ghostie/v2/bmgd.md` L24:
  > "Any centred mark on the front, below the eyes, lands in the mouth zone, however low it sits on the body."
  So the tie was moved away from the centre. My sketch brief allowed it, `acceptance/ghostie/sketch-brief.md` L53:
  > "Others can be off-centre or blown aside."
  This treated a camera problem by moving the tie to a place no tie sits.

## Options (picture: h-placement.png)
1. **Keep today's placement:** the one-sided headset and the tie far right.
2. **Decide a ghost body map first.** My pick.
   - The ears sit on the eye line, at the sides. The headset is centred over the crown, with a cup on each side.
   - Move the eyes up on the dome. A small collar marks the neck line.
   - The tie is centred, hanging from the collar.
   - Before you see it, the tie must pass a REAL game-camera render with no mouth read, not a 2D estimate.
   - If the centred tie still reads as a mouth in that render, I stop and bring you the evidence, with no more tie
     shapes (the no-blind-iterations rule).

## Not proved
- Raised eyes plus a collar may not stop the mouth read from the top-down camera. Only the real render shows it.
