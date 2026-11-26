# ATS-9000 sketch v2: direction B "Mailbox Bot" + neck (Illustrator, 2026-11-26)

Brief: `design/acceptance/ats9000/sketch-brief-B.md`. Rega, ts 1795628417.229379: "B looks cool to me, just need to
give it a neck". Chair calls: `acceptance/ats9000/chair-calls.md`. Ready check: `ready.md` (no missing needs).
v1 (direction A) and the explore sheet are archived as they were in `../sketch-v1-A/`.
Paths are relative to `runs/jobless-roguelike/design/assets/ats9000/sketch/`.
Build: `cd src && python3 build.py` (about 35 s), then `sh src/crops.sh` from this folder for the 2x crops.

## 1. What changed from B in the v1 explore sheet
- **Fact:** there is a NECK now. It is a bellows of 3 ink rings on a grey core, 50 u tall (0.19 m). It is in every view
  and at the game camera (`crops/sheet-front.png`, `sheet-34.png`, `sheet-side.png`, `sheet-back.png`,
  `sheet-gamecam.png`, `bm-gamecam.png`). Source: `src/ats.py` `NECK_CORE`, `NECK_RINGS` (L61-62).
- **Fact:** the head grew from 0.8 x 168 u to 176 x 90 u, and the eyes from 13 x 21 u to 20 x 30 u (`src/ats.py`
  `HEAD` L55, `screen_marks`). At 1x facing the camera, each eye is about 4-5 px tall (`crops/sheet-gamecam.png`).
- **Fact:** the head is shallow, 68 u deep (Z +-34; v1 was 112 u). Reason: at pitch 42 a deep head hides the neck top
  (`body-map.md` D). Without this change, the first v2 try (a 2-ring sliver) showed only one ring under the head.
- **Fact:** the body is a mailbox arch (round crown, straight sides), so the neck sits on a crown (`src/ats.py`
  `BODY` L64).
- **Fact:** the slot is kept as the mouth, with a lip tray under it. The hopper motion became "a CV slides into the
  slot" (`crops/sheet-slot-treads.png`).
- **Fact:** the stamp arm rests at 45 deg (chair call 3), its wind-up is 140 and its slam is 0
  (`src/ats.py` `REST_DEG` L84; `crops/sheet-scan-stamp.png`, `bm-side.png`).

## 2. Size at the game camera (chair call 1: 1.21 x Kit, facing the camera)
- **Fact:** target 1.21 x 75 = 90.75 px (`src/build.py` `TARGET` L40). Calibrated facing the camera (net yaw 5)
  with Ricky's metric method (`src/build.py` L47-49). Result: 1 u = 3.73 mm, height 1.25 m.
- **Fact:** the rendered 1x tile measures 92 x 61 px facing the camera (1.23 x Kit), and 99 x 63 px when turned to
  yaw 20 (`src/build.py` `measure_px`; printed on `ats-sheet.png`). 1 px over the target comes from the outline.
- **Opinion:** Viet's blockout measures the real value, as for Ricky (67 px estimated vs 66 px real,
  `assets/ricky/v1/measure.md`).

## 3. Palette (v1 rows, `design/seats/lena-park.md`)
| Row | Hex | Use |
|---|---|---|
| 18 robot | `#8E9BA8` | body, head, neck core, slot lip, shoulder hub, stamp block |
| 22 ink | `#2B1E16` | outline, screen, slot, neck rings (bellows), treads, stamp rubber, antenna stalk |
| 12 cream | `#FFE8A6` | eyes, scan line (13.34:1 on ink) |
| 13 gold | `#F0B43C` | antenna ball; blink "off" = gold x 0.62 |
| 23 panel | `#FFF8EE` | the CV prop paper only |
| 21 red-ink | `#B23A26` | only the printed words "NOT A FIT" on the CV prop (chair call 2) |
- **Fact:** shade = base x 0.85, a neutral grey multiplier (`src/ats.py` `shade`). No other colour.
- **Fact (computed, printed on the sheet):** body vs grass 1.74:1; head/body vs the ink neck 5.70:1; ink treads vs
  grass 9.90:1.

## 4. Self-check at 2x (every panel in `crops/`)
- **Fact:** the turnaround is upright and neutral. The only asymmetry is by design: the stamp arm (robot's left) and
  the antenna (robot's right top corner).
- **Fact:** the views come from one model, so they agree by construction (`src/ats.py` `render`).
- **Fact:** the neck shows as a dark band between the head and body at 1x and x3 (`crops/sheet-gamecam.png`), and in
  the grey lineup (`crops/sheet-lineup.png`).
- **Opinion, risk 1:** at the game camera the dark neck band shows as a curved lens under the screen (the body crown
  cuts its lower edge). At x3 it can read as a second, smiling mouth above the slot (`crops/sheet-gamecam.png`).
  Alternative: grey rings on an ink core. That shows the ring structure better up close, but at 1x it is only a thin
  band (my read of the first v2 render). I kept the ink rings because separating the head from the body is the
  brief's point. Rega's call if she sees the double mouth.
- **Opinion, risk 2:** at rest 45 deg, the stamp block in the FRONT view still hangs at the lower third of the body
  (y about 270-310, `crops/sheet-front.png`). In the side and 3/4 views it clearly reads as an arm held forward.
- **Not fails (sketch rules):** label positions (the slot panel's note touches the treads), guide ticks, ink weights.

## 5. For the 3D builder (Viet)
- **Opinion, budget estimate (900 tris, at most 3 non-swap meshes):**
  - mesh 1, static: head 140, body arch + lip 150, neck core 32 + 3 rings 3 x 40, treads 220, shoulder hub 64,
    antenna 76;
  - mesh 2, the stamp arm: about 70;
  - mesh 3, the screen quad: 2 tris, with eyes and scan line as a texture;
  - total about 870.
  If it runs over, use 12-sided rings and a 12-sided core (about -60).
- **Chair call 5:** bevel the box edges about 0.02 m. The shade bands on the sheet are lighting, not colour.
- The bellows may squash-bob 2-3 u as an idle; Emil's call.
