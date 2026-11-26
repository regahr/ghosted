# Illustrator (Illustrator): hero, outfits, ghost, character sheet

## Offer

- `~/.claude/skills/illustrator/references/standards.md` lines 7, 10 (thumbnails; 3 style approaches): used for the 3 base outfits and the silhouette test.
- `references/philosophy.md` line 26 ("Readability is King"): each state must read at game size.
- `references/risks.md` line 12 (do not copy existing characters): all shapes are generic primitives.
- The SKILL.md reference links (for example `references/7-standards-reference.md`) point to files that do not exist; the real names are short (`standards.md`). The brief blocks no tool.

## 1. Hero: "the Applicant"

1 H = head diameter = 1.0 unit. Total 2.6 H, near the mock scale (Fact: `concept/index.html` lines 250-251).

| Part | Primitive | Size | Position (y) |
|---|---|---|---|
| Head | Sphere(0.5, 16, 12) | 1.0 H | 1.95 |
| Sprout (hair tuft) | Cone(0.08, 0.28, 6), bent 20° back | 0.28 | 2.5 |
| Hair cap | Sphere(0.52), top 40% only, phiLength full | | 2.0 |
| Body | Capsule(0.42, 0.5, 4, 12) | 1.34 tall | 0.9 |
| Legs x2 | Capsule(0.13, 0.1, 2, 8), x ±0.17 | 0.36 | 0.18 |
| Arms x2 | Capsule(0.1, 0.35, 2, 8), rot z ±0.25 | 0.55 | 1.25 |
| Briefcase | Box(0.5, 0.35, 0.15) in left hand | | 0.7 |
| Lanyard badge | Box(0.16, 0.2, 0.02), white | | 1.25, z 0.42 |

About 1,500 triangles, plus at most 300 per cosmetic; cap 2.5k (Fact: Viet seat file line 36).

**Silhouette test.** Solid black, 64 px tall. Three cues must read: round head, sprout, briefcase on one side (Opinion). Fact: in the hub shot the head is about 25 px tall (`concept/out/shots/02-hub.png`). So **the sprout and the pose carry the mood at game size**; the face carries it in close-ups (Opinion).

**Shape language** (Opinion): hero = circles (kind). Ghosts = domes (soft, empty). The hiring system = boxes and sharp corners.

## 2. Face: 5 expressions

Each expression is one child group on the head front (z +0.48), at most 120 triangles. Show one, hide the others. Ink `#3b2a1e`, MeshBasicMaterial. Faces use 3 toon bands (Fact: Viet seat file line 28).

Base parts: eyes = Sphere(0.07) scaled (0.7, 1, 0.4), x ±0.15, y +0.02. Highlight = Sphere(0.02), white. Brows = Box(0.12, 0.025, 0.02). Mouth = Torus arc (r 0.08, tube 0.018). Cheeks = Circle(0.06), `#f28c8c`, opacity 0.6.

| Expression | Eyes | Brows | Mouth | Sprout | Extra |
|---|---|---|---|---|---|
| Hopeful | tall ovals, 1 highlight | up 0.04 | arc up, 0.8π | straight up | cheeks on |
| Ghosted | small dots (scale 0.5), no highlight | flat | flat line, Capsule(0.015, 0.08) | droops 70° | sweat drop: Sphere + Cone, `#9fd3ff` |
| Rejected-but-fine | closed "^ ^": torus arcs 0.6π | up 0.02 | wide arc, 0.9π | bent 30° | 1 sweat drop, right arm thumbs-up |
| Focused | ovals scaled y 0.5 | tilt 15° in | short line, x +0.04 | straight | none |
| Offer-joy | big, 2 highlights | up 0.06 | open "D": half Sphere ink + tongue `#e2574c` | springs, scale-y 1.3 | cheeks on, 12 confetti boxes in mock colours |

## 3. Outfits

Slots: torso colour, neck, head, back. **Base outfits are atlas colour swaps**: 0 extra triangles (Opinion).

Base (player picks at Season start):
1. **Smart Casual**: shirt `#3b82f6`, tie Box(0.16, 0.5, 0.05) `#e2574c`, legs `#3b2a1e`. This is the mock hero (Fact: `index.html` lines 250-252).
2. **Cosy Sweater**: torso `#e9d8b8`, scarf Torus(0.3, 0.06) `#22a06b` on neck.
3. **Night Owl**: torso `#4a4a58`, beanie: half Sphere(0.53) `#f2b134` on head.

Unlockable cosmetics (tied to the hunt, cosmetic only):
| Cosmetic | Unlock | Build | Colour |
|---|---|---|---|
| Interview Blazer | reach your first panel | Capsule shell r 0.45, open front; 2 lapel Boxes; 1 gold button Sphere(0.03) | `#2b3a67`, button `#f2b134` |
| Lucky Hoodie | get ghosted 25 times (ghosting is a reward) | half Torus behind head; pocket Box(0.4, 0.15, 0.04); white ghost decal on chest | `#8b5cf6` |
| Take-Home Headphones | finish a take-home | Torus arc band over head; 2 Cylinders(0.12, 0.08) | `#f2b134` |
| Offer Party Hat | get your first offer | Cone(0.18, 0.4, 8), stripes in atlas, Sphere pom | `#e2574c` / `#fffaf2` |

## 4. Ghost NPC

Story in colour (Opinion): a recruiter is a coral peg with a tie. When they ghost you, the colour drains to white, the legs fade, they float.

- Dome: half Sphere(0.4, 16, 8) + open Cylinder(0.4, 0.45, 0.35, 16). Hem: 5 Spheres(0.09) on the bottom ring (wavy edge).
- Height 1.0 H, smaller than the hero: a joke, not a threat.
- Opacity 0.88. Purple is also the "GHOSTED" text colour (Fact: `index.html` line 9).
- Face: 2 ink eye dots only. **No mouth: a ghost never replies.**
- 3 variants by one faded accessory (`#c8c0d8`): tie, glasses (2 Torus), headset.
- Float 0.3 up, bob 0.08 at 0.5 Hz (Emil owns final motion).

## 5. Colour per character

| Character | Main | Shadow band | Accent |
|---|---|---|---|
| Hero skin | `#ffd7b5` | `#f4b183` | cheeks `#f28c8c` |
| Hero hair | `#3b2a1e` | `#24180f` | none |
| Recruiter (alive) | `#e2574c` | `#c8553d` | tie `#fffaf2` |
| Ghost | `#fffaf2` | `#d9cff5` | `#8b5cf6` |

Fact for mock colours: `index.html` lines 8-9, 237, 251. New shades: Opinion.

## 6. Character sheet layout

1920x1080, `#fde7c8`, orthographic three.js render.
- **Top**: turnaround 0°, 45°, 90°, 180°; hero 400 px; guide lines each 0.5 H.
- **Middle**: 5 head close-ups, 180 px, labelled.
- **Bottom**: 3 base + 4 cosmetics, 3/4 view, 200 px, unlock line under each.
- **Right**: swatches, 64 px silhouette, ghost, recruiter-to-ghost in 3 steps.

## Questions for Rega

(Chair: add links and one diagram per option.)
1. Hero body: (a) one neutral peg, player names it; (b) 2 body presets; (c) a fixed named hero. **Pick: a.**
2. Ghost mouth: (a) no mouth, "never replies"; (b) small "o" mouth. **Pick: a.**
3. Cosmetics: (a) look only; (b) small perk each. **Pick: a.**
