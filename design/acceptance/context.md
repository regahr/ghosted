# Acceptance panel and final art: 2 decisions for Rega

Run: `runs/jobless-roguelike/design/`. Pictures: `a1-panel.png` and `a2-art.png`. Each picture shows one panel for each
option.

## Your message

Slack C0CHA2A1DM1, ts 1795594231.633739,
(private Slack thread)
> "anyway does the in game will see the same or it's still a draft? not yet finalized, because for me it looks so
> much slopped, can have a acceptance panel for each designs ya"

The message has 4 screenshots: ATS-9000, the Ghosties, Recruiter Ricky and Take-Home Phones.

## Answer: it is a draft, and the game would look like this today

The sheets come from the same three.js code that a game build would use (`design/render.html`, local and not in a
git repo, no commit sha). So with no change, the game would look like the sheets. That is why it is not final.

Flaws I can see in your 4 screenshots:
- **Shadows:** the shadows are grainy, and they show as streaks on the robot and blotches under the ghost.
- **Ghost tie:** it reads as a grey box on the ghost's body.
- **Bands:** the headset band and the headphone band cut through the hair and the head.
- **Shapes:** every part is a plain sphere, capsule or box, so nothing has a hand-made silhouette.

The bible already says these models are not final:
- `design/bible.md` L40: "The meshes are not merged yet. In this mock the hero is about 3.5k triangles across
  about 25 draw calls. The budget is 2.5k triangles in 1 merged mesh, so the build must merge the parts."
- `design/bible.md` L43: "The motion is specified, not animated. The sheets show still poses only."

## Sources for the options

- Council rules, `~/.claude/skills/council/SKILL.md` (local, not in git) L142: "| Which version ships | Rega |".
- The same file, L123: "| Pre-delivery checklist before anything ships | Lena Park |".
- Viet Tran's skill checklist,
  `~/.claude/plugins/cache/3dviz-pro-max/3dviz-pro-max/0.1.0/skills/3dviz-pro-max/templates/checklists/visual-anti-slop.md`
  L10: "**Does the important object read correctly?** Check silhouette, proportions, negative space".
- Illustrator's seat file, `design/seats/illustrator.md` L27: "**Silhouette test.** Solid black, 64 px tall."
- Blender: `/Applications/Blender.app` is on this machine. `Blender --version` prints "Blender 4.3.0".

## A1. What is the acceptance panel? (picture: a1-panel.png)

Options:
- (a) The seats are the panel.
- (b) You are the panel.
- (c) The seats score each design first, then you accept or redo it.

**My pick: c.** The council rule says you decide what ships (L142). The seats filter out the weak drafts, so
you see only the designs that passed.

The checklist each design must pass:
- Viet's anti-slop list, items 1-6 (shape, construction, detail, material, form, light).
- The Illustrator's 64 px silhouette test.
- Lena's contrast and colour-blind checks, plus her pre-delivery list.
- BMGD's check that the design serves the loop and the text register.
- Emil's check of the pose and the feel.

## A2. How do the designs become final art? (picture: a2-art.png)

Options:
- (a) Polish the code models.
- (b) Model each asset in Blender with a script, then export glTF.
- (c) Restyle a free CC0 asset pack.

**My pick: b.** Blender 4.3 is already on this machine. It gives real silhouettes, and the game loads the same
files that you accept. The cost: each asset takes more time.

With (c), the art would come from someone else, so the game would have less of its own identity.

## What happens next

If you pick c and b:
1. Write the checklist.
2. Model Kit first in Blender.
3. Have the seats score Kit.
4. Post Kit as card 1 for your accept or redo.
5. Then the Ghosties, Ricky, ATS-9000 and the other NPCs, one card at a time, then the districts.
