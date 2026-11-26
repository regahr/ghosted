Viet Tran (3D Design Lead (3DViz Pro Max)):

# GHOSTED: world, hero, NPCs, camera, toon

`<3d>` = `~/.claude/plugins/cache/3dviz-pro-max/3dviz-pro-max/0.1.0/skills/3dviz-pro-max`; style files are in `<3d>/data/knowledge/style-profile/`.

## Offer

- `style-cel-shaded.json` lines 52-53, 60: toon ramp, outline, tone mapping (section 5).
- `style-toy-miniature.json` line 52 and `style-tilt-shift-diorama.json` lines 60, 159-164: scale cue, camera (sections 1, 6).
- `style-low-poly.json` line 52: triangle budgets (sections 3, 4).
- `<3d>/templates/rigs/lighting-sun.js` line 8: dusk key colour, end of the light arc (section 2).
- `<3d>/templates/kits/primitives/` (bevelled-box, door-with-step, inset-window, sign) and `kits/creatures/biped-walker.js`: building parts and walk cycle. Recolour and simplify them.
- Blocked: no build yet, so `scripts/capture.py` waits for the chair's first build.

## 1. World: 3 districts and a tower

Fact: the plan has "3 districts and a final floor" (`runs/jobless-roguelike/council-report.md` line 53). Fact: the mock shows Job Board Cafe, Recruiter HQ, ATS Tower (`concept/out/shots/02-hub.png`).

Opinion: each district is one diorama block: a 24 x 24 m slab, 0.8 m thick, bevelled edge, a cross of 4 m paths, 4 lots. 1 unit = 1 m. Scale cue: every door is 1.4 m (hero 0.95 m).

| District (weeks) | Landmarks, boxes W x D x H m | Instanced props | Ground / edge | Sky top / horizon |
|---|---|---|---|---|
| Job Board Quarter (1-4) | Job Board Cafe 6x5x4, red roof `#d9573b`; Print Shop 5x5x5; Home Flat 5x5x8 | cork boards, mailboxes, trees (icosahedron crown) | `#bcd98a` / `#f2b27a` | `#ffe9c7` / `#fff6e6` |
| ATS Industrial Park (5-8) | ATS Tower 7x7x14 `#4f86b8`, cylinder scanner on roof; Conveyor Shed 8x4x3; Recruiter HQ 6x6x10 | crates, cones, silos | `#c9c2b8` / `#a7b4c2` | `#dfe9f2` / `#f7efe2` |
| Interview Heights (9-11) | Glass Panel Office 8x6x12 `#9fd3d6`; Take-home Library 6x5x6, dome; Salary Bank 6x6x7, 4 columns | benches, coffee carts, lamps | `#e8d9c4` / `#c9a27e` | `#ffe0c2` / `#ffd3a8` |
| LinkedUp Plaza (12) | LinkedUp Tower 8x8x22, 6 stepped floors, roof stage 6x6, big thumb sign | flags, podium, balloons | `#f6e3c6` / `#e9965b` | `#ffc28a` / `#ffe4c4` |

Background: inverted sphere (r 200), vertex-colour gradient, 3 flat clouds.

## 2. Light per week

Fact: dusk key `#ffb46b` (`lighting-sun.js` line 8). Opinion: the Season goes from morning to sunset.

- Elevation = 62° - 4.5° x (week - 1); azimuth = 140° + 10° x (week - 1).
- Colour lerps `#fff3dc` to `#ffb46b`; intensity 2.6 to 3.0.
- Hemisphere fill 0.9: sky = district sky top, ground = district edge.
- A rejection never darkens the light (Opinion).

## 3. Hero: wooden pawn toy, about 2,150 tris

Opinion: 2.6 head-heights, 0.95 m tall. Keep the mock: blue body, red tie.

| Part | Primitive | Size m | Tris | Colour |
|---|---|---|---|---|
| Head | Sphere 16x12 | r 0.18 | 350 | `#f2c79b` |
| Hair | half Sphere 16x6, y x 0.7 | r 0.19 | 190 | `#4a3326` |
| Eyes | 2 Sphere 8x6, z x 0.5 | r 0.025 | 160 | `#2b211c` |
| Body | Capsule, 16 radial | r 0.2, h 0.62 | 320 | `#3d7dd8` |
| Collar | Torus 16x4 | r 0.13 | 130 | `#ffffff` |
| Tie | 2 Box | 0.06 x 0.2 | 24 | `#e04a3a` |
| Arms | 2 Capsule, 8 radial | r 0.05 | 220 | `#3d7dd8` |
| Hands | 2 Sphere 8x6 | r 0.055 | 160 | `#f2c79b` |
| Legs | 2 Cylinder 8 | r 0.06, h 0.14 | 100 | `#2f3e5c` |
| Shoes | 2 bevelled Box | 0.1x0.06x0.16 | 200 | `#3a2a22` |
| Briefcase | Box + Torus 8x4 | 0.22x0.16x0.06 | 90 | `#8a5a3b` |
| Badge | Box + Cylinder 6 | 0.06x0.08 | 40 | `#ffd166` |

Fact: hero budget 800-2,500 tris (`style-low-poly.json` line 52). Opinion: merge to one mesh with atlas UVs: 1 draw call plus 1 outline. Walk: legs ±25°, bob 0.03 m.

## 4. NPC figures (same pawn language, Opinion)

- **Recruiter** (1,400 tris): hero body x 1.05, cone skirt (Cylinder r 0.12 to 0.22), wide smile (half Torus), headset (Torus + Sphere), clipboard Box. `#e8708a`.
- **Ghost** (300 tris): LatheGeometry teardrop, 12 radial, 4-scallop hem, `#f6f1e3` at 0.85 opacity, 2 eye spheres, "Seen" tick badge. Bob 0.1 m at 0.6 Hz. Instanced, up to 12.
- **ATS robot** (900 tris): Box body 0.6x0.7x0.45 `#8fa3b8`, Box head with screen `#2b3a4a` and a moving scan line, 2 capsule treads, stamp arm "NOT A FIT", emissive antenna `#ffd166`.
- **Interviewer** (1,200 tris): pawn in cardigan `#7c8c6e`, round glasses (2 Torus), mug Cylinder. Panel of 3: change hair and cardigan colour.

## 5. Toon ramp and outline

Fact: "2 bands for props and 3 for faces with the terminator at N dot L = 0.45"; "inverted-hull pass at 1.5 px at 1080p", dropped under 12 px on screen (`style-cel-shaded.json` lines 52-53). Fact: tuned for Neutral tone mapping at exposure 1.0 (line 60).

- MeshToonMaterial, gradientMap 2 texels (props) or 3 (heads), NearestFilter.
- Shadow band: base x 0.72, hue 8° toward warm violet. No grey (Opinion).
- Outline: BackSide clone, pushed 0.012 m along normals, `#3b2a20`. Hero, NPCs, landmarks only.

## 6. Camera

Fact: tilt-shift uses 22° FOV and polar 25-55° (`style-tilt-shift-diorama.json` lines 60, 159-164). Opinion:
- **World shot**: FOV 26°, pitch -40°, 42 m from block centre. Play follow: 26 m, yaw ±20°, polar 35-50°.
- **Character sheet**: FOV 22°, camera 0.5 m high, 3.4 m away, target y 0.45. Views: front, 3/4 (35°), side, back. Background `#fde6c8`, floor disc r 0.8, a 1.4 m door as scale cue.

## 7. Questions for Rega

1. Hero? (a) one fixed hero, suit colour unlocks (b) 3 body types (c) blank pawn. **Pick: a.**
2. Season light? (a) morning to sunset arc (b) fixed noon (c) per district only. **Pick: a.**
3. Ghost? (a) sheet ghost (b) see-through recruiter (c) recruiter fades into a sheet. **Pick: c.**

Note to chair: Rega's rule needs a link per cited line and a diagram per option.
