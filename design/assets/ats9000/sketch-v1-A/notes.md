# ATS-9000 sketch v1: notes for the chair and the 3D builder (Illustrator, 2026-11-26)

Brief: `design/acceptance/ats9000/sketch-brief.md`. Ready check: `ready.md` (no missing needs). Paths are relative to
`runs/jobless-roguelike/design/assets/ats9000/sketch/` unless they say otherwise.
Build: `cd src && python3 build.py` (about 40 s), then `sh src/crops.sh` from this folder for the 2x crops.

## 1. Direction and pick
- **Fact:** 10 thumbnails and 3 developed directions, each with a game-camera tile next to a real Kit render:
  `explore.png`, `crops/ex-thumbs.png`, `crops/ex-directions.png`.
- **Fact:** the picked direction is A, "Inbox Bot": screen face, a funnel hopper on the head top, a flared box body,
  2 ink treads, one stamp arm, one antenna (`src/ats.py` `model()`, defaults).
- **Opinion (the reason):** A is the only direction where the three "reads your CV" parts all show at the game camera
  at once: the screen face, the hopper mouth (a dark oval seen from pitch 42) and the stamp arm
  (`crops/sheet-gamecam.png`). B's front slot sits where a mouth would be and reads as a grin. C's open-top head reads
  as a bin ("your CV goes in the trash"), which is a mean joke; the brief asks for kind.
- **Fact:** thumbnail 2 (BMGD's back hopper) shows the problem: the hopper is hidden behind the head at the game camera
  (`crops/ex-thumbs.png`, tile 2).

## 2. Size at the game camera
- **Fact:** target 90 px = 1.2 x Kit's 75 px (`sketch-brief.md` "Size"; `assets/ricky/v1/measure.md` scale table).
- **Fact:** method = Ricky's metric estimate: project the sketch model, height x 74.97 px/m + 2 x 1.6 px outline
  (`src/build.py` L37-50). It was right for Ricky: 67 px estimated, 66 px real (`assets/ricky/v1/measure.md`).
- **Fact:** calibrated in the lineup facing (net yaw 5: the camera yaw 20 minus the 15 deg turn the lineup gives each
  character, `assets/ricky/v1/ingame.html` L303), because Kit's 75 px and Ricky's 79 px were measured there.
  Result: 1 u = 3.85 mm, height 1.19 m (`src/build.py` L47-51).
- **Fact:** the rendered 1x tiles measure 91 x 62 px at yaw 5 and 97 x 65 px at yaw 20 (bounding box of the alpha,
  `src/build.py` `measure_px`; printed on `ats-sheet.png`, `crops/sheet-gamecam.png`). A box reads taller at yaw 20
  because its corner turns toward the camera.
- **Open (chair):** which way the ATS faces in its scene is not decided. If it faces the camera like the lineup, it is
  91 px (1.21 x Kit). If it is turned 20 deg, it is 97 px (1.29 x Kit). Viet's blockout measures the real value.

## 3. Palette (rows of `design/seats/lena-park.md` only)
| Row | Hex | Use |
|---|---|---|
| 18 robot | `#8E9BA8` | body, head, hopper, shoulder hub, stamp block |
| 22 ink | `#2B1E16` | outline, screen, neck, treads, stamp rubber, hopper inside, antenna stalk |
| 12 cream | `#FFE8A6` | eyes, scan line (13.34:1 on ink) |
| 13 gold | `#F0B43C` | antenna ball; blink "off" = gold x 0.62 (a multiplier, not a new colour) |
| 23 panel | `#FFF8EE` | the CV prop paper only |
| 21 red-ink | `#B23A26` | **flag:** only the printed words "NOT A FIT" on the CV prop (that is text, the row's use). Never on the robot |

- **Fact:** shade = base x 0.85, a neutral grey multiplier (`src/ats.py` `shade`, `SHADE_K`).
- **Fact:** no teal, and none of BMGD's `#8FA3B8` / `#E0533D` or Viet's `#2b3a4a` / `#ffd166` (`src/ats.py` `ROW`, L15).
- **Fact (computed, `src/build.py` `ratio`, printed on the sheet):** body vs grass 1.74:1, body vs path 1.94:1,
  body vs ink 5.70:1, gold vs body 1.53:1, ink treads vs grass 9.90:1.
- **Opinion:** the mid-grey body carries no edge on grass by itself, as Lena warned (`seats/lena-park.md` L82). The
  ink outline, the ink treads and the ink screen band carry it (`crops/sheet-lineup.png`, grey half): in grey the ATS
  is a mid box with a dark base and a dark face band, apart from Kit (mid), Ricky (dark) and the Ghosties (light).

## 4. Body map, motion and joins
- **Fact:** all landmarks, attachment points and joins are in `body-map.md` and `body-map.png`.
- **Fact:** motion panels on `ats-sheet.png` (`crops/sheet-scan-stamp.png`, `crops/sheet-hopper-treads.png`):
  scan (3 positions, flat "reading" eyes), stamp (rest 22 deg, wind-up 150, slam 0 onto a CV, with the stamped CV
  prop), hopper (CV above, half in, gone + reading), treads (hub spin) + antenna (on / off).
- **Fact:** screen states (`crops/sheet-screens.png`): idle, reading, found, notfit, loading. The body never changes.
- **Opinion:** "notfit" uses soft, low eyes (sorry, not angry), so the stamp beat stays kind.

## 5. For the 3D builder (Viet)
- **Opinion, budget estimate (900 tris, at most 3 non-swap meshes):**
  - mesh 1, static body: head 140, neck 12, body 120, hopper (16 sides, inner wall + rim) 96, 2 treads 220,
    shoulder hub 64, antenna socket + stalk + ball 76;
  - mesh 2, stamp arm, one hinge at the hub axis: bar 12, block 44, rubber 12;
  - mesh 3, screen quad: 2 tris, with the eyes / scan line as a texture (V scroll for the scan, a swap per state);
  - total about 800.
  Tread roll = UV scroll on the belt plus spinning hub decals; antenna blink = emissive on / off. Viet's call.
- **Opinion, the extrusion edges:** the sketch extrudes the front profiles with sharp depth edges. In 3D, give every
  box a small bevel (about 0.02 m) so the ink outline does not show facets.
- **Fact, the sketch only:** the turned hopper shows a lighter band at its base. That is the 6 u straight collar
  catching the light (`src/ats.py` `HOPPER`, L87). Keep the collar as a ring, or drop it; it is not a colour change.
- **Fact:** the views come from one model, so the front, 3/4, side and back agree by construction
  (`src/ats.py` `render`, `src/build.py` `sheet`).

## 6. Self-check at 2x (crops in `crops/`, every panel)
- **Fact:** the turnaround is upright and neutral; the only asymmetry is by design: the stamp arm (robot's left) and
  the antenna (robot's right top corner) (`crops/sheet-front.png`, `sheet-34.png`, `sheet-side.png`, `sheet-back.png`).
- **Fact:** a light name plate under the screen was cut after the first build. At 90 px it read as a grin under the face
  (my read of the first build; that crop was overwritten by the rebuild). The option is kept as `model({"plate": True})`.
- **Opinion, open point:** in the FRONT view the stamp, hanging at rest beside the tread, can read as a third foot
  (`crops/bm-front.png`). At the game camera and in the 3/4 view it reads as an arm (`crops/sheet-gamecam.png`,
  `sheet-34.png`). If Rega or the chair wants it clearer, a rest angle near 45 deg lifts the stamp to body height.
  This is not done, because no extra iteration was asked for.
- **Not fails (sketch rules):** label positions, guide ticks and ink weights.
