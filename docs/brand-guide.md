# Commodity Pulse — Brand Guide

**Author**: Priya (UI/UX Designer)
**Date**: 2026-02-25
**Status**: Draft v1

---

## 1. Positioning

### What Commodity Pulse IS

A **commodity intelligence terminal** for independent traders who want to understand WHY markets move, not just WHAT moved.

### What Commodity Pulse is NOT

- Not a Bloomberg terminal (too dense, too expensive, too enterprise)
- Not a trading app (we don't execute trades, recommend actions, or predict prices)
- Not a news aggregator (we don't just list articles — we synthesize narratives)
- Not a toy (this tool informs real trading decisions with real money)

### The Position

```
                     ENTERTAINMENT
                          ↑
                          |
                          |
SIMPLE ←─────────── COMMODITY ───────────→ COMPLEX
                      PULSE
                          |
                          |
                          ↓
                     PROFESSIONAL
```

We sit slightly below center on the professional axis and slightly right of center on complexity. We're closer to "professional" than "entertainment" — but we use premium visual design to make the professional experience FEEL exciting. We're closer to "complex" than "simple" — but we use layered information hierarchy so complexity reveals itself on demand.

**One-liner**: The analyst you'd hire if you could — compressed into a dashboard you open every morning.

### Who is this for?

Raj, 27, independent commodity trader in Mumbai. Monitors 8 commodity markets daily. Currently spends 15-20 minutes scanning Reuters, Investing.com, and TradingView before each session. Wants to compress that to 5 minutes with higher conviction.

He doesn't want a tool that thinks FOR him. He wants a tool that thinks WITH him.

---

## 2. Brand Voice

### Personality Traits

| Trait | How it sounds | How it doesn't sound |
|-------|--------------|---------------------|
| **Precise** | "5 articles. Net bullish. +0.34 sentiment." | "Several articles suggest positive sentiment..." |
| **Confident** | "DIVERGENCE: Bullish news, price declining" | "There might be a discrepancy between..." |
| **Respectful** | Shows the data, lets the trader decide | "You should BUY Gold" |
| **Crisp** | Headlines, not paragraphs | Long explanations nobody reads |
| **Domain-fluent** | "OPEC Supply Pressure", "Safe Haven Demand" | "Cluster 1", "Topic Group A" |

### Tone Scale

```
COLD ──────────|─── COMMODITY PULSE ─────────── WARM
               ↑
          Here. Precise, not robotic.
          Competent, not chatty.
          A senior analyst's morning brief,
          not a friend's text message.
```

### Writing Rules

1. **Use domain vocabulary.** "Bullish", "Bearish", "Divergence", "Conviction" — these are Raj's words. Mirror them.
2. **Numbers before words.** "4 articles, bearish, -0.8%" beats "Four articles with a bearish average sentiment score of negative zero point eight."
3. **Active voice.** "Fed rate pause drives gold higher" not "Gold prices were driven higher by the Federal Reserve's decision to pause rates."
4. **No hedging language.** Don't write "potentially" or "might suggest." Either show the data or don't.
5. **Never say BUY, SELL, HOLD, or predict prices.** This is a design principle, but it's also a voice principle. We SHOW evidence. We NEVER recommend.

---

## 3. Emotional Targets

Every screen should evoke specific emotions. Not by accident — by design.

### Dashboard Entry

**Target emotion**: Control. "I have my instruments in front of me."

The dashboard should feel like sitting down at a well-organized trading desk. Everything is where you left it. The current market state is immediately visible. You're in command.

### Cluster Scan

**Target emotion**: Recognition. "I can see the story instantly."

The cluster cards should feel like a briefing from a sharp analyst. Themes are named in YOUR language. Sentiment is color-coded. Article counts tell you signal strength. In 15 seconds, you know the narrative.

### Divergence Detection

**Target emotion**: Alertness. "Something doesn't add up — I need to look closer."

Divergence is the product's signature moment. When news says bullish but price says declining, this is WHERE traders make money — on the gap between narrative and reality. This moment should feel slightly elevated: a gold badge that draws the eye, a subtle expansion of the card, the sense that this is worth your attention.

### Post-Scan Confidence

**Target emotion**: Conviction. "I have a thesis. I know what I'm looking for when I open TradingView."

After scanning clusters + chart + divergence, the trader should leave with a directional bias. Not a trade signal — a thesis. "Gold bearish today, supply-driven, but watch the dollar." The product earns its $50-100/month if it delivers this feeling reliably every morning.

---

## 4. Audio Identity

### Why Audio Matters

Raj trades every morning. This is a daily ritual, not a one-time visit. Audio creates ambient presence — the difference between "I'm checking a website" and "I'm in my trading session."

### Audio Principles

1. **Audio is ambient, never intrusive.** Background, not foreground. The trader should forget the music is playing until they notice how focused they feel.
2. **Audio communicates state.** Entering the dashboard = audio presence begins. Exiting = silence. The transition itself signals "session active" vs "session over."
3. **No sudden sounds.** No jarring pings, no aggressive alerts. Even notifications should be soft — a gentle tone that says "something happened" without startling.
4. **User controls volume and presence.** Mute button always visible. Volume preference persists. Some traders will NEVER want audio. Respect that.

### Audio Design Spec

| Element | Genre/Style | Energy | Purpose |
|---------|-------------|--------|---------|
| **Ambient track** | Lo-fi electronic / dark ambient / minimal synthwave | Low-medium. Think Tycho, not Perturbator. | "You're in your trading cockpit." Sustained attention without distraction. |
| **Entry sound** | Soft digital chime, ascending | Brief, 1-2 seconds | "Dashboard is loaded, data is fresh." |
| **Divergence alert** | Low resonant tone, slightly dissonant | Brief, subtle | "Something needs your attention." Not alarming — intriguing. |
| **Commodity switch** | Soft click/transition whoosh | Micro, <0.5 seconds | Feedback for navigation. Confirms the action happened. |

### Audio Architecture (for dev)

- React Context or singleton audio manager (not component state — audio must persist across re-renders)
- Lazy-load audio assets (not bundled)
- Persist volume/mute preference in localStorage
- Audio starts only on user interaction (browser autoplay policy)
- Master toggle in sidebar or top-right corner

### NOT in scope
- Per-article sounds
- Price alert sounds (Phase 4)
- Victory/loss sounds
- Anything gamified

---

## 5. Visual Identity Principles

### Cyberpunk is a Means, Not an End

The cyberpunk aesthetic works because:
1. **Dark background** reduces eye strain for daily use
2. **Neon accents on dark** create clear visual hierarchy
3. **Monospace typography** matches the "data terminal" metaphor
4. **Glows and gradients** draw attention to what matters

It stops working when:
1. Neon is everywhere and nothing stands out
2. Animations compete for attention
3. The aesthetic becomes a gimmick instead of a tool
4. The user notices the design instead of the data

**Test**: Would Raj say "nice dashboard" or "I got my thesis in 2 minutes"? The second one means the design is working. The first one means we've made a pretty toy.

### The 10% Rule

No more than 10% of visible screen area should be "active" (glowing, animating, pulsing) at any given time. The rest is calm, dark, and readable. The active elements are where the user's eye should go.

### Depth Model

```
Layer 0: Page background (#0a0a0f) + grid
Layer 1: Cards (gradient surfaces)
Layer 2: Active/selected cards (elevated surface + glow)
Layer 3: Overlays (modals, expanded panels, tooltips)
```

Every element exists at one depth layer. Mixing layers (e.g., a card that glows like an overlay) creates visual confusion.

---

## 6. Landing Page vs Dashboard

### Current Problem

The landing page and dashboard feel like they were designed separately. The landing page is more polished (better hierarchy, better spacing) but uses inline styles heavily. The dashboard is more functional but visually flatter.

### Alignment Spec

| Property | Landing Page | Dashboard | Should be |
|----------|-------------|-----------|-----------|
| Card backgrounds | `linear-gradient(145deg, #1a1a2e, #0d0d22)` | Same | Same (good) |
| Card borders | Inline style `borderColor: ${color}20` | Tailwind classes | Tailwind classes everywhere |
| Section spacing | `py-24` (generous) | `mt-8 mb-4` (tight) | Landing generous, dashboard efficient — this is correct. Different contexts. |
| Typography | Better hierarchy (3xl→lg→sm) | Flatter | Dashboard needs the same hierarchy care |
| Emojis | Feature icons, commodity grid | Section headers, commodity icons | Acceptable on landing (marketing), reduce on dashboard (tool) |

### The Handoff Moment

When a user clicks "TRY IT NOW" on the landing page, the transition to the dashboard should feel like walking from a showroom into a cockpit. The aesthetic is continuous (same colors, fonts, depth) but the density increases. More data, less whitespace, same confidence.

---

## 7. Competitive Differentiation (Visual)

| Competitor | Visual character | How we differ |
|-----------|-----------------|---------------|
| Bloomberg Terminal | Dense, green-on-black, 1990s | We're modern dark UI with color semantics. Same information density, 10x more readable. |
| TradingView | Light mode, charts-first, social | We're dark mode, narrative-first, solo trader. Charts support the story, they aren't the story. |
| Investing.com | Cluttered, ad-heavy, overwhelming | We're noise-free. No ads, no distractions, no 47 sidebar widgets. |
| Finviz | Data tables, heat maps, functional | We're the same efficiency with premium feel. Data + design, not data OR design. |

### Our visual signature

The combination that makes Commodity Pulse recognizable:
1. **Dark background + neon accent system** (cyberpunk terminal)
2. **Cluster cards with conviction badges** (our unique interaction)
3. **Divergence visualization** (the gold badge on a dark card — our "signature move")
4. **Orbitron headlines** (authoritative, futuristic, distinctive)

---

## 8. Next Steps

1. **Immediate (pre-layout redesign)**: Apply design-system.md fixes — remove ghost colors, fix inconsistencies, reduce motion noise, normalize spacing. These are cleanup items that don't require layout changes.
2. **With layout redesign (Task #34)**: Apply information hierarchy changes, news-first layout, click-to-expand clusters. This is where the brand really comes alive.
3. **Post-layout**: Audio identity implementation (Task #35), skeleton loading states, enhanced divergence visualization.
