# GHOSTED

A browser roguelike about job hunting: you apply, you get ghosted, you keep going. The plan is Next.js on Vercel with
Supabase edge functions and Google sign-in. The final goal is a LinkedIn post.

This repo holds the design work so far:
- `brief.md`, `seats/` and `council-report.md`: the game council plan.
- `concept/`: the scripted three.js concept run (gameplay video and screenshots).
- `design/bible.md`: the character and world bible, with the rulings.
- `design/assets/<character>/`: each locked character has:
  - `LOCKED.md`: what is accepted, its numbers and its known limits;
  - the sketch (`sketch/`, hand-drawn SVG to PNG);
  - the Blender source (`.blend`), the game file (`.glb`) and the build script that rebuilds the model in Blender 4.3.
- `design/acceptance/`: the briefs, cards and decision history for each character.

All 9 characters are locked: Kit (the hero), the Ghosties, Recruiter Ricky, ATS-9000, Brett Bullet-Points, Auntie Dot, Juno, The Panel and Gary the pigeon postman.
Still to do: the 4 districts of Port Pending, then the game build.

## Before you push
Run `sh scripts/check-public.sh`. It fails if any file, including Blender files and PNG metadata, holds a Slack
link, a local home path, or a secret-looking token. The local git hook runs it before each commit.

Note: the `.blend` files here are cleaned copies, written without UI data and with relative paths. PNG text metadata is
stripped. Build scripts may still name paths relative to the original workspace.
