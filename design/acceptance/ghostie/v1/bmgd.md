BMGD (Game Designer): Ghostie v1, card 2, items B1-B2

## Offer

- `.../bmad-game-dev-studio/0.7.2/src/workflows/2-design/gds-create-narrative/checklist.md` line 54 ("Each has distinct role in story") and line 111 ("Tone matches GDD art/audio direction"). I use them as the test for B1 (role) and B2 (tone).
- `seats/bmgd.md` Cast table (Ghosties row) and text samples 1-2. This is my own spec for the Ghostie's loop job: a collectible result, "Brenda from Talent".
- No tool of mine is blocked by this brief.

## Items

- **B1. FAIL.** Name, role and most of the tone match. One bible point breaks at game size.
  - Fact: bible says "It has no mouth, because 'a ghost never replies'" (`design/bible.md` line 30).
  - Fact: `hero.png`, `variants.png` show no mouth. Two ink dot eyes, an ink outline and a scalloped hem. The tie, the glasses and the headset read clearly at card size.
  - Fact: `lineup-grass-crop-x3.png`, `lineup-path-crop-x3.png`, left ghost (tie): at the game camera the faded lavender tie sits just under the eyes. It reads as a small open mouth or a nose, not as a tie.
  - Opinion: this breaks the joke the bible names as a default ("The ghost with no mouth", line 51). A ghost that seems to say "oh" is a ghost that replied.
  - Fact: role. Body 27 px against Kit's 55 px (`ingame_report.json`, `lineup-grass`). The ghost reads as a small collectible, not a threat. That fits the Cast row ("Ghost result, collectible", `seats/bmgd.md`).
  - Opinion: the colour drifts from off-white `#F8F4EA`. I sampled (244,228,200), cream, in `hero.png`, and (233,208,203), pink, in `lineup-grass.png`. I do not fail B1 on this. It is Lena's and the Illustrator's item. I flag it.
- **B2. PASS.** Comic and kind. Nothing mocks the player.
  - Fact: `variants.png`, `hero.png`: round dome, small dot eyes, stub arms, a soft floating shadow. There are no teeth, brows or sneer.
  - Fact: `lineup-grass-crop-x3.png`: three small ghosts stand next to a smiling Kit, all half his height. The pink cast under warm light reads as a blush, not as a threat.
  - Opinion: the wide-set eyes give a vacant, sheepish look. That is right: the company looks a bit embarrassed, it does not look cruel.

## Does the read serve the loop? (Opinion)

- Expression: yes. Blank and a bit sheepish fits "they meant to reply". You laugh at it. It does not sting.
- Size next to Kit: yes. At half Kit's height and below his eye line, 24 of them read as a collection, not as a crowd that hunts him.
- Faded accessory per variant: it works at card size, and only partly in game.
  - Glasses: they still read as glasses in game (`lineup-grass-crop-x3.png`, middle). Good.
  - Headset: the band is a faint line and the ear cup is almost lost (right ghost). Without the headset this reads as a plain ghost, so you lose "that's the recruiter". This is weak, but it is not a must fail for me. The "Seen ✓" billboard (not built, `changes.md` point 5) can carry the joke.
  - Tie: see B1. It reads as a mouth.
- Faded, ink-free accessories as the "recruiter faded" story beat (`changes.md` point 4) is a good idea. But "faded" must still read as the object at 26 m, or the joke is lost.

## Narrowest fixes

1. Tie variant (needed for B1): make the tie read as a tie at the game camera and keep it out of the mouth zone. Move it lower on the body, so its top sits clearly below the eye line in the 26 m view. Also add a wider knot (a triangle that reads at 2-3 px), or raise its value contrast one step. Re-shoot `lineup-grass*.png` and `lineup-path*.png`.
2. Headset (advisory): make the ear cup a little larger, or one step darker, so it reads in game.
3. Colour (advisory, for Lena and the Illustrator): confirm the cream lit band and the pink in-game cast against `#F8F4EA`.

**Overall: FAIL** (B1 only, tie variant reads as a mouth in game. Fix 1 alone clears my items.)
