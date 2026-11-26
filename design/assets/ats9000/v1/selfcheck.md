# ATS-9000 v1 self-check (Viet Tran, builder, 2026-11-26)

Rules: every claim names an image. A visible fault is never PASS. Rega is the gate; the chair checks at 2x first.
Paths are in `assets/ats9000/v1/`. Build: `python3 make_textures.py`, then
`Blender -b --factory-startup -P build_ats.py`, `Blender -b ats.blend -P render_ats.py`, `node shoot_ingame.mjs`,
`python3 make_sheets.py`.

## Method steps run before modelling (council "Offer is not use")
- `ready.md` (no missing need; 12a belt cleats and 12b no bellows bob are my readings, flagged).
- `direction.md` (step 1 intent, step 2 hardest parts, step 4 joins, step 5 targets).
- Skill tool outputs in `skill/`: `host-probe.txt`, `host.json`, `search-*.txt` (4), `design-context.txt`,
  `resolve-*.txt` (6).
- Tiny tests first (`tests/`): bevelled head + screen + one tread built alone, then rendered in Blender and in three.js
  from the glb: `tests/test-blender-vs-three.png` (5 screen states by UV, the scan line hidden in found / not fit /
  loading, the hub turned, the belt scrolled; both engines agree). It found the lopsided head outline (fixed: the
  outline is now simplified on one half and mirrored).
- Blockout (`blockout/`): 1.25 m measured 93 px, so the final is 1.22 m (`measure.md`).

## Counts (Fact: `ats_build_report.json`; three.js `ingame_report.json` `visibleTris`)
| State | body | stamp | screen | Visible total | Cap |
|---|---|---|---|---|---|
| rest / wind-up / CV in the slot | 803 | 68 | 4 | **875** | 900 |
| found, not fit, loading (scan line hidden) | 803 | 68 | 2 | **873** | 900 |

- Body by part: head 156, body arch 172, lip 10, neck core 24, 3 neck rings 132 (12 sides), treads 104, hub discs 36,
  shoulder hub 34, antenna 82, decals 53 (slot, lip ink, hub rim, pivot dot, vents, hatch).
- Stamp: bar 28, block 28, rubber 12. Screen: 2 + 2. CV prop (not part of the robot): 10.
- Non-swap meshes: **3** (`body`, `stamp`, `screen`). Prop: `cv` (hidden by default).
- Blender vs three.js: mean difference 1.29/255 (3/4) and 1.28/255 (front); 0.63 % and 0.67 % of pixels differ by
  more than 40 (`compare-ingame.png`, `compare-ingame-front.png`).

## Brief requirements
| # | Requirement | Verdict | Proof |
|---|---|---|---|
| 1 | Budget: 900 visible tris or fewer, at most 3 non-swap meshes | PASS: 875, 3 meshes | `ats_build_report.json`; `ingame_report.json` `visibleTris` |
| 2 | B turnaround: monitor head on a bellows neck (3 ink rings on a grey core), mailbox-arch body | PASS | `turnaround.png`; `compare-sketch.png` (front, 3/4, side, back) |
| 3 | Front CV slot with a lip tray | PASS | `crops/slot-lip-front-x2.png`, `crops/slot-lip-34-x2.png` |
| 4 | Ink treads | PASS | `crops/tread-left-front-x2.png`, `crops/tread-side-x2.png` |
| 5 | Stamp arm on the robot's LEFT, one hinge | PASS (viewer-right in front; one node `stamp_pivot`) | `turn-front.png`; `stamp.png` |
| 6 | Antenna on the right top corner | PASS (viewer-left in front) | `crops/antenna-front-x2.png`; `turn-back.png` |
| 7 | Faces the camera; 1.21 x Kit, measured the Ricky way | PASS: 91 px at Kit's depth (1.213), 90 at Kit's spot (1.200) | `measure.md`; `ingame_report.json` |
| 8 | Neck shows at the game camera, measured in px | PASS for "shows": a dark band 8-9 px tall, 12-13 px wide | `measure.md`; `crops/gamecam-neck-x6-*.png` |
| 9 | Screen: one mesh on the head front, 5 states by UV, scan line scrolls, never angry | PASS | `screens.png`; `tests/test-blender-vs-three.png` |
| 10 | Colours: rows 18, 22, 12, 13, 23; 21 only as CV text; neutral shade | PASS (cleat lines = row 18 x 0.85; ball off = gold x 0.62) | `make_textures.py`; `build_ats.py` `PAL`; `slot.png` (red only on the CV) |
| 11 | Box edges bevelled about 0.02 m | PASS on the head and body (0.02 m); the stamp block uses its rounded profile corners (r 3 u) instead, see weak 7 | `ats_build_report.json` `bevel_m`; `crops/head-corner-34-x2.png` |
| 12 | Stamp rests at 45, winds up to 140, slams to 0 | PASS; wind-up clears the head | `stamp.png` (Blender side and 3/4, three.js wind-up); `crops/stamp-windup-clearance-x2.png` |
| 13 | A CV slides into the slot | PASS | `slot.png` (out, half, in, stamped; three.js half) |
| 14 | Tread hubs spin, belts scroll | PASS (one UV rotation turns all 6 hubs; the belt U scrolls) | `treads-antenna.png`; `tests/test-blender-vs-three.png` |
| 15 | Antenna ball blinks | PASS (gold 13 / gold x 0.62) | `treads-antenna.png` |
| 16 | Optional bellows bob | NOT BUILT (optional; it needs a bone or a morph on the static body) | `ready.md` 12b |
| 17 | Open risk: does the neck band read as a second mouth? | **It does read as a mouth.** Reported, not redesigned | `measure.md` "The neck read"; `crops/gamecam-neck-x3-grass.png` |
| 18 | Deliverables | PASS: turnaround, hero, stamp, slot, screens, silhouettes, grey, in-game + compare, lineups grass/path colour/grey x3 and 1x, compare-sketch, crops | this folder; `crops/` |

## Whole-picture check at 2x (every panel)
- Fixed during the build (Facts, before and after in the render history):
  - lopsided head outline (the tiny test);
  - a hard step in the bevel band along the head and body bottoms (flat chamfer normals on long runs now);
  - a block bevel corner and a thin ink sliver peeking beside the stamp rubber (`crops/stamp-block-34-x2.png`);
  - the lip tray did not read in front (ink lip edge added, `crops/slot-lip-front-x2.png`);
  - the shoulder hub vanished into the grey body in side view (ink rim added, `crops/stamp-arm-side-x2.png`);
  - the stamp 3/4 frames were cut by the frame edge (`stamp.png`).
- Still open: see "Weak points". None of them is scored PASS above where it touches an item.

## Weak points (honest)
1. **The neck reads as an open mouth at the game camera** (Opinion; `crops/gamecam-neck-x6-grass.png`). The body
   crown rounds the bottom of the dark band, so it is a dark half-disc under the eyes. The slot then reads as a
   second mouth. This is the sketch's open risk; it is Rega's call (options below).
2. **Screen and neck almost touch at 1x** (Fact: 1-2 px of grey head between them, `measure.md`). This makes weak 1
   stronger: the dark screen and the dark neck read as one face block.
3. **The grey reads neutral, not blue-grey** (Opinion; `compare-sketch.png`). Same hex (#8E9BA8) as the sketch, but
   Kit's warm sun and ground light take the blue out. Kit and Ricky use the same light.
4. FIXED 2026-11-26 (line 3 u -> 7.5 u, `crops/scanfix/`). Was: at 1x the scan line at rest broke into two short cream dashes under the eyes (Opinion: they can read as lower
   lids; `crops/gamecam-neck-x6-path.png`). The line is under 1 px tall at the game camera.
5. The antenna ball is an 8-sided low sphere; it shows facets on the hero card (`hero.png`).
6. In the side slam frame the rubber draws a little below the tread line, because it is nearer the camera
   (`stamp.png` top right). Fact: its bottom is 2 u above the ground (y 338 vs 340).
7. The stamp block is not bevelled 0.02 m: the bevel left a notch beside the rubber twice, so the block now uses its
   rounded profile corners. Small round corners read on the card (`crops/stamp-block-34-x2.png`).
8. A small lighter facet at the head's bottom corners where the bevel band turns (`crops/head-corner-34-x2.png`,
   `turn-front.png`); visible at 2x only.

## For Rega (weak 1; not my call, no build started)
1. Keep it as it is: the neck reads as a big open smile under the eyes. Cheap: no change.
2. Grey rings on an ink core (the sketch's own alternative, `sketch/notes.md` 4): the band breaks into stripes, less
   like a mouth, but a thinner dark read at 1x. Cheap: a material swap.
3. Raise the screen inside the head, so more grey head shows between the screen and the neck (weak 2). Cheap: a UV
   and quad move.
My pick: 2 + 3 together, if Rega sees the mouth. Each needs a new render pass that Rega asks for.
