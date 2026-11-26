BMGD (Game Designer): GHOSTED, hero, cast, world

## Offer

- `gds-create-narrative/steps/step-04-characters.md`: each NPC gets a loop role and an arc. Its rule "FORBIDDEN to create characters without user input" (line 46) is blocked by this brief (no contact). So this is a draft; open points are the questions.
- `step-05-world.md`, `step-06-dialogue.md`: districts with a narrative job; text register.
- `gds-create-narrative/checklist.md` lines 37-69: my self-check.
- Later: full `gds-create-narrative` doc after Rega answers.

## Facts I build on

- **Fact**: mock hub buildings Job Board Cafe, ATS Tower, Recruiter HQ (`concept/index.html` lines 237-239); HUD currency "Copium" (line 113); hero is a blue capsule, peach head, red tie, brown case (`concept/out/shots/02-hub.png`).
- **Fact**: my council seat called it "Insight" (`runs/jobless-roguelike/seats/bmgd.md` line 25). See Q3.

## Hero (Opinion)

**Name:** player types it. Default **Kit**.
**Backstory:** (1) Kit was a designer at Crunchr, a snack startup. (2) Crunchr "pivoted to AI" and cut the team by a "Quick sync" invite. (3) Severance: 12 weeks of savings and a lifetime snack box ("Snacks: unlimited").
**Personality:** sunny, over-prepared, has a spreadsheet of every application.
**Wants:** a job where someone replies. **Arc:** "any job, please" to "I know my worth" (unlocks Salary Tug).

**Build (1.0 m, 2.5 head-heights, under 1.2k tris):**

| Part | Primitive | Size (m) | Hex |
|---|---|---|---|
| Head | sphere 16x12 | r 0.20 | #F4C9A0 |
| Hair cap | half sphere, scale y 0.6 | r 0.21 | #4A3226 |
| Body | capsule 12 seg | r 0.22, len 0.36 | #3B6FD4 |
| Arms x2 | capsule 8 seg | r 0.06, len 0.22 | #3B6FD4 |
| Feet, eyes | sphere | r 0.08, r 0.025 | #2E2A33 |
| Tie / case | box | 0.06x0.18x0.02 / 0.22x0.16x0.07 | #E0533D / #7A4A2A |

Low Morale: a 3-sphere rain cloud (#9AA6B8) follows Kit only.

## Cast, 8 NPCs (Opinion)

| NPC | Loop job | Build | Hex |
|---|---|---|---|
| **Ghosties** ("Brenda from Talent" etc.) | Ghost result, collectible | cylinder r 0.25 h 0.3 + sphere r 0.25, 2 eyes; bob 0.1 m, opacity 0.85; one InstancedMesh | #FFF8E7, eyes #2E2A33 |
| **ATS-9000** | ATS Catch gate. Literal, not evil | box head 0.5, visor slit, box body 0.6, cone hopper | #8FA3B8, visor #E0533D |
| **Recruiter Ricky** | Recruiter Call. "Super excited to connect!", then forgets; his lost threads become Ghosties | capsule, headset torus | #F2994A |
| **Auntie Dot** (mentor) | Meta hub: Copium buys Skills. Ex-recruiter who once ghosted someone; now answers everyone | short capsule, bun sphere | #8C6BB1, hair #DADADA |
| **Brett Bullet-Points** (rival) | One week ahead in your funnel. Talks in bullets. Likes your post first in week 12 | capsule 1.15 m, torus halo | #6FBF73, halo #2E9E5B |
| **Juno** (barista) | Cafe heal node (+Morale). A line on each cup | capsule, apron box, cup cylinder | #E0533D apron, #FFF1DC cup |
| **The Panel** | Panel Plates: Ms. Culture Fit, Mr. Whiteboard, The Camera-Off One (black box) | table box 2.0 x 0.1 x 0.6, 2 sphere heads + 1 box | #C9A27A, box #2E2A33 |
| **Gary** (pigeon postman) | Brings each result, 0.6 s flap | sphere, cone beak, 2 box wings | #9AA6B8, beak #F2B84B |

## World (Opinion)

**City:** **Port Pending**. Everything is "under review".

| District | Weeks | Funnel beat | Landmarks | Ground hex |
|---|---|---|---|---|
| Applyside | 1-4 | CV, cover letter, ATS | Job Board Cafe, ATS Tower, Print-n-Pray copy shop | #C8E08A |
| Callback Quarter | 5-8 | Recruiter call, take-home, coffee chat | Recruiter HQ, Take-Home Depot | #E3D3EE |
| Panel Heights | 9-11 | Panel, references, negotiation | Salary Bridge | #CFE3F0 |
| LinkedUp Tower | 12 | Offer, the post | Rooftop with a beacon | #FCE5C8 |

M1: Applyside only, with all 5 M1 rooms (as in the mock).

**Across 12 weeks:** light follows time. Weeks 1-4 morning (sun #FFF4D6), 5-8 dusk (#FFC98A), 9-11 night with lit windows (#FFD76E, sky #2B3550), 12 dawn (#FFB7A0). Each ghost of the run stays near its building (cap 24). After week 6, "NOW HIRING" signs get "*internally". Full Hope meter: the Tower beacon turns on, seen from every district.

**World serves the loop:** district = funnel stage, so the map shows progress. Door colour = node type: #3B6FD4 application, #F2994A heal, #8C6BB1 event, #6FBF73 meetup. Street ghosts show reward, not failure. Gary brings every result, so each "no" has one short, soft beat.

## Text samples (Opinion, comic and kind)

1. Ghostie: "Your application is very important to us." *poof* +5 Copium.
2. "Seen 3 weeks ago. Brenda from Talent joins your ghost collection."
3. "They chose a candidate with 10 years in a 3-year-old framework. +1 Copium."
4. "The role went to an internal candidate: the CEO's houseplant. +3 Copium."
5. ATS-9000: "KEYWORD 'SYNERGY' NOT FOUND. PLEASE BE MORE SYNERGY."
6. Auntie Dot: "No is an answer. Silence is their homework, not yours."
7. Auntie Dot: "Every ghost is a door that forgot to close. Walk on through."
8. Juno's cup: "You are not a PDF."
9. Brett: "• 400 applications • 0 replies • Thriving."
10. Run end: "You go home and sleep. Port Pending will still be here."

## Questions for Rega

1. Hero: (a) player names, default Kit; (b) fixed Kit; (c) 1 of 3 presets. **My pick: (a).**
2. City name: (a) Port Pending; (b) Hireton; (c) Applyburg. **My pick: (a).**
3. Currency: (a) Copium (mock); (b) Insight (council seat); (c) Closure. **My pick: (a)**: Rega saw the mock and said "i love the name, the concept" (brief line 5). Risk: it can tease the player, so lines pair it with a system joke.
