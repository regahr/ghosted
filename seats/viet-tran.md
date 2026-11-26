Viet Tran (3D Design Lead (3DViz Pro Max)):

# Seat answer: jobless roguelike, 3D world

`<3dviz>` = `~/.claude/plugins/cache/3dviz-pro-max/3dviz-pro-max/0.1.0/skills/3dviz-pro-max`.
Design lead for games is this seat (Fact: `~/.claude/skills/council/SKILL.md` line 125).

## Offer

- `<3dviz>/data/knowledge/style-profile/style-toy-miniature.json` and `style-tilt-shift-diorama.json`: give the look and the camera numbers below.
- `<3dviz>/data/knowledge/style-profile/style-low-poly.json` line 52: triangle budgets.
- `<3dviz>/data/knowledge/style-profile/style-cel-shaded.json` line 52: toon ramp numbers.
- `<3dviz>/templates/kits/kit-core.js` lines 32, 131: seeded RNG and `scatterInstances` (one InstancedMesh per prop type).
- `<3dviz>/templates/kits/kit-lod.js` line 9: draw-call lesson. Sets my budget gate.
- `<3dviz>/templates/kits/layout/village-layout.js` lines 1-6: seeded plan that is the same in Node and browser. Pattern for room generation.
- `<3dviz>/templates/rigs/camera-orbit-follow.js` lines 13-14, 34+: clamped orbit, 0.9 s focus tween, parked loop. Pattern for the station camera.
- `<3dviz>/templates/checklists/visual-anti-slop.md`, `inspection-per-frame.md`, `scripts/capture.py`: proof gate per milestone.
- Blocked: no build exists yet, so `capture.py` and `host-probe.py` have nothing to check. Use them from M1.

## 1. Verdict

**Go with changes.** 3D works if each room is a small toy diorama on a fixed camera. An open 3D city will break the budget and the schedule (Opinion).

## 2. Recommendations

**World (Opinion).** The run map is a city block diorama. Each node is a building (job board cafe, career fair hall, recruiter tower, HR lobby, interview floor). Each building floor is one roguelike room. The last building is the "LinkedIn tower". Its roof is the "I got the job" post scene.

**Art style.** Toy miniature with cel shading. Fact: toy profile says "keep one repeated scale cue in every view" (`style-toy-miniature.json` line 52). Fact: toon ramp 2 bands for props, 3 for faces, terminator N·L 0.45 (`style-cel-shaded.json` line 52). Opinion: warm, bright palette. Ghosting is funny, not sad: recruiters fade into cartoon ghosts.

**Camera.** Fixed 3/4 view, narrow lens. Fact: tilt-shift profile uses 22° FOV and clamped 25-55° polar orbit (`style-tilt-shift-diorama.json` line 60). Opinion: use 25-30° FOV, small orbit (±20° yaw) only. No free camera. Depth-of-field blur is a desktop-only option.

**Stack.** React Three Fiber + drei, in one client-only route (`/play`, `dynamic(..., { ssr: false })`). Opinion: R3F fits Next.js and React UI overlays; Babylon is a heavier second engine and does not share React state. Fact: the skill scaffold pins three 0.180.0 (`<3dviz>/templates/scaffold-vite-threejs/package.json` line 12). Use `frameloop="demand"` when the room is still (Fact: parked-loop rule, `camera-orbit-follow.js` line 14).

**Asset budget per room (Opinion, from the facts above):**
- Draw calls: target 80, hard cap 150.
- Visible triangles: cap 150k. Hero figure 2,500. Props 120-400 each (Fact: `style-low-poly.json` line 52).
- Textures: one 256x256 palette atlas plus at most 4 MB GPU texture memory. KTX2.
- Meshes: GLB with meshopt or Draco.
- Load: first room playable at at most 3 MB gzip (JS + assets). Each new room pack at most 500 KB.
- Frame rate: 60 fps desktop, 30 fps mid phone. Device pixel ratio cap 1.5.

**Procedural rooms (Opinion).** One modular kit on a 2 m grid: floor, wall, door, window, desk, chair, plant, printer, coffee machine, water cooler. 12-20 hand-made room shells. A seeded layout fills props and stations. The seed comes from the run id in Supabase, so a run can replay. Checks before a room shows: door clearance, a walk path from entry to exit (flood fill), and every station can be reached.

**Mini games in the world (Opinion).** Each mini game is a station object in the room (photocopier, coffee machine, arcade kiosk, interview desk). The player walks to it. The camera tweens 0.9 s to the station. The mini game opens as a 2D overlay or a small sealed 3D scene. The world loop parks while it runs. Contract: `start(seed, difficulty) -> result`. No mini game depends on the room scene. This keeps many mini games cheap.

**Ending.** The final roof scene renders a share card: the hero figure on the tower, with run stats. Capture one frame from the canvas only at that moment.

## 3. Risks

1. **Draw calls explode in generated rooms.** Fact: one mesh per object gave 4,773 draw calls at 5 fps (`kit-lod.js` line 9). Mitigation: one InstancedMesh per prop type, merge the static shell, fail the build if `renderer.info.render.calls` > 150.
2. **Art scope grows past the team.** Mitigation: one modular kit and one palette atlas. New floors change palette and layout, not meshes (Opinion).
3. **Next.js load and hydration cost.** Mitigation: three code only in `/play`, Suspense per room pack, preload the next room during a mini game (Opinion).

## 4. Milestones

- **M1 first playable:** one office floor, 3 seeded rooms, click-to-move hero, 1 station opens 1 mini game, toon shader, dev budget meter. Proof: `capture.py` overview and close-up of each room.
- **M2:** city map diorama, 3 buildings (acts), 8 room shells, 8 stations, room transitions, ghost recruiter effect.
- **M3:** LinkedIn tower and share card, 12 shells, home apartment hub with cosmetic unlocks.
- **Complete:** 5 districts, 20 shells, 25+ stations, phone pass at 30 fps, reduced-motion mode (Fact: scaffold reads `prefers-reduced-motion`, `scaffold-vite-threejs/main.js` line 89), budget gate in CI.

## 5. Questions for Rega

1. Device? (a) desktop only (b) desktop first, phone works (c) phone first. **Pick: b.**
2. Look? (a) toy diorama with toon shading (b) flat low-poly (c) retro pixel 3D. **Pick: a.**
3. How does the hero move? (a) click-to-move, fixed camera (b) WASD third-person (c) no walking, hop between nodes. **Pick: a.**
4. Who is the hero? (a) preset toy figure you dress up (b) figure with your Google photo on a badge (c) faceless figure. **Pick: a.**
5. Mini game view? (a) all 2D overlays (b) all in the 3D room (c) 2D by default, 3D for 3-5 key games. **Pick: c.**

Note to chair: Rega's rule asks for a link per cited line and a diagram per option. Add those when these become the interview.
