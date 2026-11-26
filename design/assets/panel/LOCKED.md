# The Panel is locked (v1)

Rega's acceptance: card 8, "1" (ts 1795668396.770149).

The game uses these files from `assets/panel/v1/`:
- `panel.glb`, with 4 non-swap meshes:
  - table with chairs, 90 triangles;
  - Culture Fit, 845;
  - Whiteboard, 755;
  - the box, 10.
- 19 swap meshes: eyes, brows and mouths, 3 marker poses, and 2 box icons.

## The numbers (`v1/panel_build_report.json`, `measure.md`)
- **Triangles:** 1,867 in game at idle, at most 1,891, of 2,000.
- **Table top:** 0.733 m (0.75 times Kit).
- **Seated heads:** 23 px at the game camera.
- **Forehead band:** 4-7 px. The side hair sits 8-11 px above the eye top. No fringe.

## Design source
- The sketch: `assets/panel/sketch/`, direction A, "bow, flat-top, black cube".
- The chair calls are in `acceptance/panel/brief.md`.

## What the game build must do
- **Idle face:** both people use the TALK mouth at the game camera. Cards keep the rest lines.
- **Culture Fit nod** (-8° to +6°): at the lowest frame she shows the talk mouth, and the grin shows only on the way up
  (chair call, card 8).
- **Whiteboard:** marker up, click, and point.
- **The box:** it blinks between the camera-off and muted icons, about 0.5 s on and 0.5 s off.
- **All lean in:** 14°, with both heads turning 12° chin-up so the faces stay on the player.

## Known limits accepted
- The mouths sit about 4 u higher than in the sketch, so close under the eyes at card size.
- At card size the hands and cuffs look like hexagons.
- Whiteboard's "click" is the same pose as "marker up".
- At card size there is a darker toon band on the lower face.
- Culture Fit's tilt smirk does not show at 1x.

## Asset files (local on this machine)
- **Blender source:** `design/assets/panel/v1/panel.blend`
- **Game file:** `design/assets/panel/v1/panel.glb`
- **Build script:** `design/assets/panel/v1/build_panel.py`
