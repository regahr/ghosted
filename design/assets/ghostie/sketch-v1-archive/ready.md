# Ready check: Ghostie sketch and paint-over (Illustrator, 2026-11-25)

Rule: `~/.claude/skills/council/SKILL.md` lines 183-209. Brief: `design/acceptance/ghostie/sketch-brief.md`.
Paths below are relative to `runs/jobless-roguelike/design/`.

| # | Need | State | Source |
|---|---|---|---|
| 1 | Goal: one sheet that fixes the final shape before more Blender work; the tie is the hard part | decided | `acceptance/ghostie/sketch-brief.md` lines 6-9 |
| 2 | Who sees it: the 5 design seats at the sketch gate, then Rega; Viet builds from it | decided | council `SKILL.md` lines 236-243 |
| 3 | Role and tone: recruiter who never replied, comic and kind, NO MOUTH | decided | `bible.md` line 30; brief line 12 |
| 4 | Card size view | decided | `assets/ghostie/v5/hero.png` (1200 px), `v5/variants.png` (600 px panels); brief line 15 |
| 5 | Game camera view: top-down, 26 m, body about 27 px at 1x | decided | brief line 16; `assets/ghostie/v5/lineup-grass-crop-x3.png` |
| 6 | Budget: 600 tris per variant, body+arms about 508, tie 90 or fewer | decided | brief lines 30-33; `assets/ghostie/v5/build_report.json` |
| 7 | Palette: body `#F8F4EA` (16), accessory `#C8C0D8` (27), tie `#C9A6D6` (10), ink `#2B1E16` (22) | decided | `seats/lena-park.md` lines 31, 37, 43, 48 |
| 8 | Shade: neutral grey band (multiplier 178/255, no hue) | decided | `acceptance/ghostie/v3/lena-park.md` lines 19-20. In the sketch I show it as a flat neutral tint of the body; Lena checks value |
| 9 | Kept shape: dome, crown, 5-scallop hem, size, tilted rest pose (hem lower on viewer-left, viewer-right arm higher), arm tips below eye dots at game camera | decided | brief lines 17-21; `acceptance/ghostie/v3/emil-kowalski.md` lines 27-31; `assets/ghostie/v5/selfcheck.md` eye-vs-arm table |
| 10 | Variants: tie, glasses, headset; glasses and headset keep their shape, clean-up only | decided | brief lines 28-29 |
| 11 | Moving parts and joins: float bob; `arm_L` (+x, viewer-right in front view, the higher arm) waves 0 to +40 deg up from rest; arms are one skinned body mesh, drawn as soft flaps with no seam | decided | brief lines 34-35; `acceptance/ghostie/fix-brief-v5.md` lines 7-12; `acceptance/ghostie/v3/emil-kowalski.md` lines 19-35 |
| 12 | Hardest part: the tie. Tests: at game camera two eye dots and nothing centred below; at card size knot + blade + V point, never quill, horn, hair bow, strap, party horn, tongue; compare to Kit | decided | brief lines 36-40; `acceptance/ghostie/v4-tie-bmgd.md`, `v4-tie-illustrator.md` |
| 13 | Reference: Kit's tie | decided | `assets/kit/hero.png` (tie at about x 505-565, y 585-740) |
| 14 | 3D faults to mark on the paint-over: crease line from near arm root, pale root wedge, hem hook under near arm | decided | brief lines 41-44; `assets/ghostie/v5/selfcheck.md` "Still weak" 1-3 |
| 15 | Deliverables and folder | decided | brief lines 46-63 |
| 16 | Tools: hand-written SVG Bezier paths, `magick` (MSVG renderer, checked locally) to render and composite; no web, no image generation | decided | brief lines 65-69; caller's task message |
| 17 | My own skill steps: illustrator `SKILL.md` § 9.2 (thumbnail and squint checks), § 1.3 "Story First" (one word per prop), § 10 #1 "Over-detailing" (fewest marks) | decided | `~/.claude/skills/illustrator/SKILL.md` |
| 18 | Checklist the work must pass: sketch gate items (shape and silhouette; buildable in budget and views agree; palette and value; role and tone at game camera; pose and motion parts) | decided | council `SKILL.md` lines 239-241 |
| 19 | Who picks the tie | decided: I pick and mark it (brief line 50); shape language is the Illustrator's call (council `SKILL.md` "Who decides what", game art 2D row); Rega accepts or redoes the sketch at step 3 | |

Nothing is missing or unclear. I start.

Small calls I make myself (inside my decision rights, flagged for the gate):
- Sheet backgrounds use the card cream sampled from `v5/hero.png` (`#FDE6C8`) and grass `#BDD662` (`acceptance/ghostie/v3/lena-park.md` line 24). They are context, not character colours.
- Kit's tie red is sampled from `assets/kit/hero.png` at (530, 660): `#E14417`. Used only in the comparison.
