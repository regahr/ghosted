# Emil Kowalski (Principal Designer): GHOSTED motion and feel

Feel and timing targets. Viet Tran keeps final say on 3D motion. H = hero height (about 1.0 m).

## Offer

| Tool (path) | How it changes the answer |
|---|---|
| `~/.claude/skills/emil-design-eng/SKILL.md` L72-75 (frequency table) | Walk and ghosting are seen most, so they get the least motion. The offer is rare, so it gets the most. |
| same file, L184-193 (springs, bounce 0.1-0.3) and L195 (interruptibility) | All pops are springs. A re-click during a walk keeps velocity. |
| same file, L597-599, L531 | Slow wind-ups, fast recoveries. Reduced-motion path. |
| `~/.claude/skills/choreograph/SKILL.md` L123 (attention loops) | Idle fidget timing. |
| `~/.claude/skills/improve-animations/AUDIT.md` | Audit of the first build at 0.25x speed. |

The brief blocks none of my tools.

## 1. Rig (three.js)

**Opinion.** Three nested groups:
- `root` (Group): world position and yaw only.
- `bounce` (Group): pivot at the feet. Bob and squash go here, so feet stay on the floor.
- `body`: capsule torso, sphere head, 2 small capsule feet.
- Blob shadow on `root`. It scales to 0.9 at the top of a hop.

Squash keeps volume: `sx = sz = 1 / sqrt(sy)`. **Clamp sy to 0.88-1.10.** A toy is stiff vinyl.

Spring in `useFrame`: semi-implicit Euler, clamp dt to 1/30 s. Two presets:

| Preset | Stiffness | Damping | About |
|---|---|---|---|
| `settle` | 300 | 30 | 0.35 s, no visible bounce |
| `pop` | 420 | 18 | 0.45 s, bounce 0.3 |

## 2. Idle (seen all the time, so keep it tiny)

- Breath: `bounce.scale.y` 1.000 to 1.015, sine, period 3.2 s. Nothing else moves.
- Blink: random every 3-6 s, eyes scaleY to 0.1, 110 ms.
- Fidget (hero only): first after 8 s with no input, then every 12-20 s at random: look at phone, sigh (sy 0.97), 900 ms. A click stops it. **Fact:** attention loops wait, then repeat rarely (`choreograph/SKILL.md` L123).

## 3. Walk: a toy hop

| Value | Target |
|---|---|
| Top speed | 1.8 m/s |
| Step | one hop per 0.45 m (4 hops/s at top speed) |
| Bob height | 0.035 H, shape `abs(sin(phase * PI))` |
| Side roll | +/- 4 deg, one cycle per 2 hops |
| Forward lean | 6 deg at top speed, scales with speed |
| Landing squash | sy 0.95 for 70 ms each hop |

**Opinion:** drive the phase by distance moved, not time, so feet never slide.

## 4. Click-to-move response

- First visible motion within **1 frame** of the click. No wind-up (**Fact:** frequent actions get little motion, L72-75).
- Turn: yaw on the `settle` spring, about 180 ms. Above 120 deg, do a quick hop-turn (one hop, in place).
- Speed up from 0 to top in 150 ms. Slow down over the last 0.3 m in 120 ms.
- Arrival: one `settle` squash, sy 0.96 to 1.
- Re-click while walking: retarget, keep velocity. Never restart from zero (**Fact:** L195).
- Floor marker: ring, starts scale 0.6 (never 0, **Fact:** L217), opacity 1 to 0, 300 ms, `cubic-bezier(0.23, 1, 0.32, 1)`.

## 5. Reactions

Camera still, no shake, no red.

**Ghosting (most frequent). Total 750 ms. Skip at any time.**

| ms | Hero | Ghost |
|---|---|---|
| 0-80 | Hold (freeze) | Rises from y -0.2 m, opacity 0 to 0.85, scale 0.6 to 1 |
| 80-240 | Small anticipation, sy 0.94 | Pops on `pop` spring |
| 240-560 | Double take: head yaw 25 deg to the ghost, body sy 1.06 on `pop` | Waves (arm yaw +/- 20 deg, 2 times) |
| 560-750 | Back to idle on `settle` | Drifts up 0.6 m, fades out, 250 ms ease-out |

Many ghosts: stagger 40-70 ms, not uniform.

**Rejection. Total 800 ms. Skip at any time.** Deflate: sy 0.92 over 200 ms ease-out, head tilts down 10 deg. Hold 300 ms. Recover on `pop` with bounce 0.15, then a shrug (0.02 H, 150 ms). The hero always recovers.

**Offer (rare, so big). Total 1.8-2.2 s. Skip after 600 ms.**
- Crouch: sy 0.88, 180 ms (slow wind-up, **Fact:** L597-599).
- Jump: stretch sy 1.10 at take-off. Height 0.35 H. Air time 420 ms. One 360 deg yaw spin in the air.
- Land: sy 0.88, then `pop` (bounce 0.3).
- Nearby NPCs turn to the hero (stagger 60 ms) and clap: 3 hops each.

## 6. NPCs

- Same rig. Top speed 0.8x the hero. Random idle phase per NPC, so no two breathe together.
- They react only to the offer, so the beat stays on the hero.

## 7. Ghost float (idle)

Three sines, periods with no shared factor:
- y: +/- 0.06 m, 2.4 s
- x: +/- 0.03 m, 3.7 s
- yaw: +/- 8 deg, 5.1 s, always within 15 deg of the camera

## 8. What stays still

Camera during reactions. HUD and all text. Room, furniture, trees, props (no wobble). The world while a mini game runs. Shadows only scale.

## 9. Reduced motion

**Fact:** reduced motion means gentler, not zero (`emil-design-eng` L531). **Opinion:** no bob, no squash, no float, no spin. Reactions become a pose swap plus a 200 ms fade.

## 10. Feel check

Play each reaction at 0.25x. Look again the next day. Run `improve-animations/AUDIT.md` on the first build.

## Questions for Rega

1. **Walk style?** (a) Toy hop, bob 0.035 H (b) Waddle, side roll and no hop (c) Glide, no bob. **Pick: a.**
2. **Can the offer be skipped?** (a) After 600 ms (b) At once (c) Never. **Pick: a.**
3. **Many ghosts at once?** (a) Up to 5 ghosts plus a counter (b) One ghost per ghosting, no cap (c) One big ghost with a number. **Pick: a.**
