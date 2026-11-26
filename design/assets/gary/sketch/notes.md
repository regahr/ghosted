# Gary the pigeon postman: sketch notes (Illustrator, 2026-11-26)

Files: `ready.md`, `explore.png`, `body-map.png`, `body-map.md`, `gary-sheet.png`, `silhouette-64.png`, and
`src/` (`gary.py` model, `build.py` sheets, all SVG sources). Rebuild: `cd src && python3 build.py`.
Code reused: the Juno sketch library chain (`assets/juno/sketch/src/juno.py` -> the Ricky library and the Dot render),
the Juno and Panel `build.py` helpers, and the Kit cut-out `assets/panel/sketch/src/_tmp/kit-cut.png` (read only).

## Pick: direction A, "round postie"
- **Opinion:** A is the only direction that reads as "bird plus post" at about 37 px. Two clear eyes sit over a gold
  beak that points down, and a navy kepi gives a dark top that no one else in the cast has. The blue wings and tail
  give the dark value that row 8 lacks on grass, and the satchel and strap read as a postman. Round and soft, he looks
  like the kindest courier.
- **Opinion:** B (pigeon-true) uses grey row 18, which is the ATS robot's row. At the game camera its small head loses
  the eyes, and its light bag sinks into the path.
- **Opinion:** C (the BMGD literal) has box wings that read as a backpack, and a ball with no tail reads as a chick.

## Colours (existing rows only)
| Row | Hex | Use |
|---|---|---|
| 8 | `#A8C4DC` | body, head, neck (chair call) |
| 9 | `#3D6B99` | wings and tail: the darker row the brief allows for the value |
| 26 | `#2F3E5C` | cap (chair call: 26 or 22, my pick 26, so the ink brim still shows) |
| 22 | `#2B1E16` | outline, eyes, brows, cap brim, envelope flap line |
| 13 | `#F0B43C` | beak, legs, feet (small areas, chair call) |
| 5 | `#7A4A2E` | mail bag, flap, strap (chair call: 5 or 24, my pick 5: it is the darkest element, 4.5:1 on grass) |
| 23 | `#FFF8EE` | envelope, cap badge, cere, eye glint |
| 7 | `#D4503A` | envelope stamp (chair call: 7 or 10, my pick 7: warm, and it does not echo Recruiter HQ) |

The shade is the base x 0.85 (neutral grey).

## Facts (from `src/build.py`, printed on the sheets)
- **Fact:** standing height 0.488 m = 0.5 x Kit. The span is 1.03 m = 1.06 x Kit (brief: about 1.0). 1 u = 2.29 mm.
- **Fact:** at the game camera he is 35 x 26 px standing (Kit 75 px) and 81 px wide in flight with the wings level
  (`src/_tmp/bodymap.json`).
- **Fact:** the eyes are clear. The lowest cap pixel is 2.6 / 2.9 px above the eye top at rest and 2.4 px in the sorry
  tilt. Each eye is 2.35 px tall.
- **Fact:** the contrast of row 8 against grass is 1.11:1 and against the path 1.24:1. The wings (row 9) are 3.42:1 on
  grass and 3.83:1 on the path, and the bag (row 5) is 4.52:1 on grass. **Opinion:** in the grey lineups he
  separates by the outline, the wings, the cap and the bag, as the brief asks.

## For the 3D builder (Viet)
- **Opinion, mesh split (fits the 3 non-swap meshes):**
  1. the body: egg, tail, head, neck blend, cap, brim, badge, beak, cere, legs, feet and strap;
  2. the left wing (arm and hand bones);
  3. the right wing.
  The swap parts are the eyes and lids, the brows, the envelope (2 sockets), and the bag with its flap (closed or
  open). The bag can merge into mesh 1 if the flap is a swap.
- **Opinion, budget:** about 900 triangles. A rough plan: body egg 180, head 160, tail 30, cap and brim 110, beak 30,
  legs and feet 60, strap 60, bag 24, each wing 2 x 60 + 3 feathers x 20 = 180 (360 for both). The total is about
  1,010, so the strap or the feathers must go lower (for example a flat strap ribbon of 36 triangles, and feathers of
  12 triangles each).
- **Sketch note:** the brim and the cap need an ink edge in 3D (the hull outline), or the navy cap merges with the
  ink brim at 1x.
- **Sketch note:** the folded wing hand lies over the arm. In 3D, give the hand a small offset outward so it does not
  z-fight.

## Open (for the chair)
1. **The span is 1.06 x Kit, not 1.0.** The hand segment can drop from 100 u to 87 u to reach 1.00. Opinion: keep
   1.06 for the flight read. The chair's call.
2. **The eyes are 2.35 px tall at 1x.** This is the family scale for a head of this size. Opinion: they read at 1x in
   the face crop (`body-map.png` E). If the chair wants more, the eye ovals can grow by 15 % with no other change.
3. **The motion keys are poses only.** The 0.6 s flap is split into 3 keys (up 50, level 5, down -35 deg). The
   timings of the hop, tilt and fly-off are Emil's.
4. **The lineup spots are mine** (grass: right of Kit; path: in front of the group; flying: beside the set and near
   the ATS). They are cheap to change.
