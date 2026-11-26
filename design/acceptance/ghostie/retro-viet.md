# Ghostie v1-v5 retro (Viet Tran, 3D design lead, builder)

- Asked by Rega (Slack ts 1795606908.092349): "why each version become worse? did she don't offer her skill when start?"
- Each claim is marked Fact (with a file) or Opinion.
- Paths: A = `design/assets/ghostie/`, G = `design/acceptance/ghostie/`, SK = `~/.claude/plugins/cache/3dviz-pro-max/3dviz-pro-max/0.1.0/skills/3dviz-pro-max/`.

## Short answer

Not every version got worse:
- **Fact:** the gate fails went from 5 seats (v1) to 3 seats (v2 and v3).
- **Fact:** Lena and Emil passed from v2 on (`G/v2/lena-park.md`, `G/v2/emil-kowalski.md`, `G/v3/*`: "Overall: PASS").

But two parts got worse again and again: **the tie** (5 shapes) and **the arms** (4 joins). Each fix made a new fault in another place.

The main causes:
- I did not solve the 2 hardest parts first.
- I did not use the method steps of my own skill at the start. I offered 3 reference files, but I did not run the steps.
- My self-checks passed items that the renders failed.

## 1. Did each version get worse?

| Version | Better | Worse or new fault |
|---|---|---|
| v1 | (start) | **Fact:** 5 of 5 seats fail (`G/v1/*`): faceted outline, pink shade tint (my choice), tie reads as a mouth, T-pose stiffness, arms gone in 3/4. **Fact:** my self-check scored V1-V3 PASS (`A/v1/selfcheck.md` lines 11-13) while I listed the same faults as weak points. |
| v2 | **Fact:** Lena and Emil pass. Off-white restored, rest pose alive (`G/v2/lena-park.md`, `G/v2/emil-kowalski.md`). Headset band fixed. | **Fact:** I added `arm_collars` as a 4th non-swap mesh, so V5 failed (`G/v2/viet-tran.md`, V5). The pale collar strip and octagon arm end were new faults. The tie still reads as a mouth (`G/v2/bmgd.md`). |
| v3 | **Fact:** crown and hem rounder; mesh count back to 3; tie off the face centre (`G/v3/viet-tran.md` items 2-4). | **Fact:** the tie lost its tie read: "strap, sash, ribbon", "scratch at 26 m" (`G/v3/bmgd.md`). The arms still read as ears at 26 m (`G/v3/viet-tran.md` V1). Ink spur and hook under the near arm (`G/v3/illustrator.md` I2). |
| v4 | **Fact:** arm tips below the eyes on screen, measured (`A/v4/selfcheck.md` table). Cup ink is one stroke. Notch apex round. | **Fact:** the tie reads as a "quill, feather, pennant", "hair bow" (`G/v4-tie-bmgd.md` line 11) and a "horn" (`G/v4-tie-illustrator.md` line 15). The arm "C" hook stayed (`A/v4/selfcheck.md` V2). |
| v5 | **Fact:** body and arms are one skinned mesh; hook and end-on slot gone (`A/selfcheck.md` "Arm join"); 1 non-swap mesh. | **Fact:** a new thin crease line from the arm root across the body, and a pale wedge at the lower root (`A/selfcheck.md` "Still weak" 1-2). Tie read still open. |

## 2. Root cause of each regression

| Regression | Cause | Whose |
|---|---|---|
| Faceted outline (v1-v3) | **Fact:** I fitted the 300-triangle checklist budget in v1 and spent triangles on columns, not profile rings. **Opinion:** the budget was too low for a round hand-made card read. I should have asked to raise it in v1, not in the v1 judge round (`G/v1/viet-tran.md`). | Checklist budget, plus my build choice |
| Pink shade (v1) | **Fact:** I tinted the shadow band (184,170,255) to follow the Illustrator's "lavender shadow" (`A/v1/changes.md` decision 3). **Opinion:** under the warm light it went pink; I saw that and kept it. | My build |
| Collar mesh, V5 fail (v2) | **Fact:** I added a separate collar node to draw the root ink. I did not re-count non-swap meshes. | My build and my self-check |
| **Arms (v1-v4): separate meshes** | **Fact:** I built the arms as separate nodes in v1 for the wave, without deciding the join type that my skill asks for (SK `SKILL.md` line 33: "decide whether the object needs a continuous skin"). **Opinion:** an inverted-hull outline cannot close the ink where a separate flap lies in front of the body. So every fix on the flap shape (v2 tube, v3 flat flap, v4 curved flap) moved the fault and could not remove it. I named this "method" only in v4; the right point was v1. | **Method (mine)**. The v3 brief "no collar, no visible joint" with separate meshes was not possible with this outline, and I did not say so then. |
| Arms as ears (v2-v3) | **Fact:** the v3 brief said "root 10-15% lower" in world units. **Opinion:** the 26 m camera looks down, so world height is the wrong measure. As 3D lead I should have measured screen y in v2; I first did it in v4. | Brief wording, and my missing measurement |
| **Tie: 5 shapes** | v1/v2 centred chest stripe → mouth at the top-down camera. **Opinion:** I placed it like Kit's tie without testing the 26 m view for "mouth zone".<br>v3: I followed "flip over the shoulder" but built the wide end at the knot and a thin strap. **Opinion:** my shape error; I did not compare with Kit's tie.<br>v4: knot low, thin blade, flag tip at the crown corner → quill/horn/bow. **Opinion:** I read "blade widens" but kept the blade thin, and put the lift at the crown corner.<br>v5: built to the chair's detailed spec; read still open. | Mostly **my build** (shape never checked against Kit until v4's `crops/tie-vs-kit.png`). The v3 brief direction (over-the-shoulder joke) added risk, but it was a valid choice. |
| Crease line (v5) | **Fact:** after the boolean union, the hull shows at the concave join (`A/selfcheck.md`). **Opinion:** a union without a fillet or edge-loop cleanup is a quick method; a modelled join would avoid it. | My build |
| Self-checks too kind | **Fact:** v1 PASS on V1-V3 with the same faults listed as weak (`A/v1/selfcheck.md` lines 11-13). In v2 I missed the mesh count. | My process |

## 3. My skill at the start: used or not?

My v1 Offer named `references/object-craft.md`, `templates/checklists/visual-anti-slop.md` and `style-low-poly.json` (Fact: my v1 report). Steps 1-5 of SK `SKILL.md`:

| Step or script | Used? | Evidence and why not |
|---|---|---|
| Step 1: intent, visual direction, references (`SKILL.md` line 17) | **Partly.** | **Fact:** I looked at the mock cast sheet (`design/out/ghosted-sheet-2-cast.png`) and Kit's renders before v1. **Fact:** I wrote no direction or reference set to a file; `A/v1/changes.md` has no reference section. **Opinion:** I treated "match Kit's pipeline" as the direction. I had no references for a cute sheet ghost or for a blown tie. |
| Step 2: solve the hardest object early (`SKILL.md` line 24) | **No.** | **Fact:** I built the body first and the arms and tie last in `A/v1/build_ghostie.py` (body, then eyes, then arms, then accessories). **Opinion:** the hardest parts were the arm join and the tie read, and I solved them last in every version. |
| Step 4: continuity at the join (`SKILL.md` line 33) | **No, until v5.** | **Fact:** v1-v4 arms are separate meshes (`A/v1`-`A/v4` `build_ghostie.py`, `arms[nm] = new_obj(...)`). I named the reference in my judge Offer but did not apply it as builder. |
| `scripts/search.py`, `resolve.py`, `design-context.py` (`SKILL.md` lines 37-39) | **No.** | **Fact:** no output or call in `A/` or in my scratchpad files. My files there are `tint.py`, `helpers.py`, `dbg.py`, `dbg2.py` and `skintest/t.py`; the scratchpad is shared with other runs. **Opinion:** the brief handed me Kit's pipeline to reuse and I read that as "no design research needed". The catalog might have had a creature or cloth record for arm joins and fabric accessories; I did not check. |
| `scripts/host-probe.py` (`SKILL.md` line 45) | **No.** | **Fact:** no `host.json` anywhere in `A/`. **Opinion:** the tools were known from the brief (Blender 4.3, three r170). It would have changed little. |
| `visual-anti-slop.md` | Yes, at self-check only. | **Fact:** cited in each `A/*/selfcheck.md`. **Opinion:** I used it to grade, not to design, and I graded too kindly in v1. |

So, to Rega's question: I offered my skill. I did not *use* its method steps at the start (**Fact**, table above). I reused Kit's build path and fixed faults one by one.

## 4. What would have prevented the 5 passes

**Opinion:**
- **A 2D sketch pass first: yes, for the tie and the arms.**
  - One sheet: front, 3/4, the 26 m top-down thumbnail, and Kit's tie beside it.
  - That sheet would have shown the mouth-zone problem, the ear read and the quill shape before any modelling.
- **Step 2 and step 4 at the start:**
  - Name the arm join and the tie as the hard parts.
  - Choose a continuous skinned body with arms in v1.
  - Prove both on a tiny case before the body polish.
- **Budget first:** state in v1 that 300 cannot be round, and ask for the raise before building.
- **Screen-space checks** at the game camera (eye y vs arm y; anything centred below the eyes) as numbers from v1.
- **A strict self-check:** any visible fault means not PASS. The v1 self-check broke this rule, and the seats had to catch it.
