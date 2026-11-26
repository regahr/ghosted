# Lena Park (UI/UX Lead, UI/UX Pro Max): jobless roguelike

Skill root `S` = `~/.claude/plugins/cache/ui-ux-pro-max-skill/ui-ux-pro-max/2.15.0/.claude/skills/ui-ux-pro-max`.

## Offer

- `S/scripts/search.py "game entertainment playful retro cathartic" --design-system`: I ran it. It gives the palette, fonts and style below. In the build, `--persist` writes `design-system/<slug>/MASTER.md`. I did not persist (review only).
- `S/data/colors.csv` lines 13, 120 and `S/data/typography.csv` lines 6, 52: palette and font candidates.
- `S/data/ux-guidelines.csv`: motion, font, focus, sign-in rules.
- `S/data/stacks/threejs.csv`, `--stack nextjs`: canvas, touch, renderer rules.
- `S/references/quick-reference.md`, `S/references/pro-rules.md`: the pre-delivery checklist. I own this gate at each milestone.
- The brief blocks none of my tools.

## 1. Verdict

**Go with changes.** **Fact:** the tool's style "3D & Hyperrealism" is tagged accessibility risk high, performance cost high (`S/data/styles.csv`). Changes: DOM HUD over the canvas, one input model for all mini games, reduced motion from M1.

## 2. Recommendations (my area)

**Start design system** (Viet Tran leads the design for games and can change it with a reason).
- Palette, Gaming row. **Fact** (`S/data/colors.csv` line 13): bg `#0F0F23`, card `#1E1C35`, text `#E2E8F0`, primary `#7C3AED`, secondary `#A78BFA`, CTA `#F43F5E` with black text, destructive `#EF4444`.
- Contrast I measured (WCAG formula). **Fact:** text on bg 15.3:1, secondary on bg 6.9:1, CTA 5.7:1. Primary `#7C3AED` as text on bg is 3.31:1, and border `#4C1D95` on bg is 1.72:1. Rule: never use primary as body text. Use `#A78BFA` for links and focus rings (4.5:1 rule, `S/references/quick-reference.md` line 9).
- Font pair. **Fact** (`S/data/typography.csv` line 6): Fredoka (headings) + Nunito (body), mood "playful, friendly, fun". **Opinion:** this fits "cathartic, never painful" better than pixel fonts. Use Press Start 2P (line 52) only for large score numbers.
- Body text 16px minimum (**Fact**, SKILL.md priority table, "Base 16px").

**HUD.** **Opinion:** draw the HUD in HTML/CSS over the canvas, not inside WebGL. Show 4 items maximum: Morale (HP), Savings (currency), Applications sent / replies, Run day. Show each stat with an icon, a label and a number, never colour alone (**Fact**, SKILL.md priority 10). Ghosting events go to an `aria-live` log.

**Menus.** **Opinion:** Title, Run map, Pause (Esc, any scene), Settings, Results. Settings: reduced motion, text size 100/125/150%, volume, colour-blind mode.

**Mini game UI pattern.** **Opinion:** one shared frame for every mini game: title, a 1-line rule, a 3-2-1 start the player can skip, the timer as a bar plus a number, and a result card. Controls: keyboard (arrows/WASD + Space + Enter), mouse and touch for each game. No game needs only drag or only precise timing. "Relaxed" gives 1.5x time.

**Google sign-in screen.** **Opinion:** use Google's standard button. **Fact** (`S/data/ux-guidelines.csv` line 108): OAuth is the correct non-cognitive method for WCAG 2.2 AA accessible authentication. Add "Play as guest" with a later account link, so the first run starts in less than 10 s. Errors show next to the button, with retry.

**LinkedIn post composer screen.** Prefill it from run data (job, days, rejections survived). Visible field label, a 3000-character counter, a preview card, and two buttons: "Copy text", "Share". Do not copy LinkedIn branding; use a parody name.

**Desktop vs mobile.** **Opinion:** desktop first (1280x720). Mobile in landscape, touch controls 48x48 px minimum (**Fact**, `S/references/quick-reference.md` line 37: 44pt/48dp). **Fact** (`S/data/stacks/threejs.csv`): one WebGLRenderer per page, pixel ratio max 2, touch and mouse.

**Reduced motion.** **Fact** (`S/data/ux-guidelines.csv` lines 8, 10): respect `prefers-reduced-motion`; animate 1-2 key elements per view. In reduced mode: no camera shake, no screen flash, fades in place of zooms. Emil decides motion; I set this floor.

**CLS and loading.** **Fact** (`S/references/quick-reference.md` lines 58, 66; `ux-guidelines.csv` line 76): reserve space for async content, keep CLS below 0.1, use `font-display: swap` with a matched fallback (`next/font`). **Opinion:** real progress bar; first scene playable under 5 s on desktop; load mini games on demand.

## 3. Top 3 risks

1. **The canvas hides everything from keyboard and screen readers.** Mitigation: DOM HUD and menus, a 2px `#A78BFA` focus ring, a keyboard-only playtest per milestone.
2. **Many mini games mean many control schemes.** Mitigation: the shared frame; a game ships only after my checklist.
3. **Mobile GPU and touch fail.** Mitigation: threejs rules, a "low" preset, one real mid-range phone test before M2.

## 4. Milestones (my area)

- **M1 first playable:** tokens as CSS variables; sign-in + guest; HUD with 4 stats; Pause/Settings with reduced motion; 2 mini games in the shared frame; keyboard path end to end; CLS < 0.1.
- **M2:** mobile controls; text size; colour-blind mode; 6+ mini games; loading screen; Lighthouse accessibility 90+.
- **M3:** LinkedIn composer and results screens; run history; checklist run on all screens.
- **Complete:** every mini game passes the checklist; keyboard, touch and reduced-motion parity; screen-reader pass of menus.

## 5. Questions for Rega

1. Where do you play most? (a) Desktop only (b) Desktop first, mobile landscape later (c) Mobile first. **My pick: b.**
2. The last step: (a) a fake in-game post only (b) in-game post, then "Copy text" (c) opens the real LinkedIn share window. **My pick: b, with c as a second button.**
3. Look: (a) dark neon (Gaming palette) (b) bright pastel (Casual Puzzle palette) (c) office grey that turns bright as you win. **My pick: a.**
4. Must play without Google sign-in? (a) Yes, guest mode (b) No, sign-in first. **My pick: a.**
5. Mini game timing: (a) always a timer (b) a timer with a relaxed toggle (c) no timers. **My pick: b.**
