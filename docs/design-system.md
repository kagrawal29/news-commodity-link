# Commodity Pulse — Design System

**Author**: Priya (UI/UX Designer)
**Date**: 2026-02-25
**Status**: Draft v1 — Initial audit + proposed system

---

## 1. Color System

### Current State (Audit)

The palette has strong semantic intent but inconsistent application.

| Token | Hex | Semantic Intent | Issues |
|-------|-----|-----------------|--------|
| `cyber-cyan` | `#00FFFF` | Primary brand, data, neutral info | Overused — brand, headings, chart line, Y-axis ticks, loading states, filter active. Doing too many jobs. |
| `cyber-magenta` | `#FF00FF` | Alert, accent | Underused. Only in sidebar label, tagline, scrollbar thumb, and neutral article borders. Inconsistent meaning. |
| `cyber-green` | `#00FF88` | Bullish, positive, profit | Consistent. Well-applied. |
| `cyber-red` | `#FF4444` | Bearish, negative, loss | Consistent. Well-applied. |
| `cyber-gold` | `#FFD700` | Premium, important, divergence | Good. Used for divergence badges and timeframe. |
| `cyber-blue` | `#00d4ff` | ? | Only used on landing page steps + news source badge. No dashboard role. |
| `cyber-purple` | `#8338ec` | ? | Only used on landing page step 03. Ghost token. |
| `cyber-amber` | `#ffbe0b` | ? | Only used on landing page step. Ghost token. |

**Critical inconsistency**: Neutral articles use magenta border in NewsFeed.tsx but gray in ClusterCards.tsx. The scrollbar is magenta — random.

### Proposed Color System

Every color earns its semantic role. If it doesn't have a clear meaning, remove it.

#### Core Palette

| Token | Hex | Role | Usage |
|-------|-----|------|-------|
| `brand-cyan` | `#00FFFF` | Primary brand. The "pulse" in Commodity Pulse. | Logo, primary CTAs, chart lines, active nav states |
| `signal-green` | `#00FF88` | Bullish / positive / profit | Sentiment positive, price up, bullish clusters |
| `signal-red` | `#FF4444` | Bearish / negative / loss | Sentiment negative, price down, bearish clusters |
| `signal-gold` | `#FFD700` | High importance / divergence / premium | Divergence badges, conviction=THESIS, premium features |
| `accent-magenta` | `#FF00FF` | Accent. Sparse. Eye-catch for alerts. | Breaking news, divergence flash, hover accents — NOT for neutral content |
| `neutral-400` | `#9CA3AF` | Secondary text | Labels, descriptions, timestamps |
| `neutral-600` | `#4B5563` | Tertiary text | Footnotes, disabled states, metadata |

#### Remove

| Token | Reason |
|-------|--------|
| `cyber-blue` (#00d4ff) | Too close to cyan. Confuses the hierarchy. Replace with cyan or remove. |
| `cyber-purple` (#8338ec) | No semantic role in the product. Landing page decoration only. |
| `cyber-amber` (#ffbe0b) | Too close to gold. Remove. |

#### Surface Palette

| Token | Hex | Role |
|-------|-----|------|
| `surface-base` | `#0a0a0f` | Page background |
| `surface-card` | `#1a1a2e` | Card backgrounds |
| `surface-elevated` | `#16213E` | Hover states, active cards, expanded panels |
| `surface-overlay` | `rgba(0,0,0,0.60)` | Mobile backdrop, modal overlays |

#### Glow System

Glows are FUNCTIONAL — they indicate state, not decoration.

| Glow | When to use |
|------|-------------|
| Cyan glow | Active/selected state (current commodity, active filter) |
| Green glow | Bullish cluster or positive divergence |
| Red glow | Bearish cluster or negative divergence |
| Gold glow | Divergence detected — attention required |
| No glow | Default state. Most things should NOT glow. |

**Rule**: If more than 3 elements glow simultaneously, something is wrong.

---

## 2. Typography

### Current State (Audit)

Two fonts: Orbitron (display) and Share Tech Mono (body). Good pairing — authoritative + technical.

**Issues**:
- Hierarchy is flat. Section headers are all `text-lg font-bold`. No differentiation between primary and secondary sections.
- Commodity header is `text-4xl` → section headers `text-lg` is a 2.5x jump with nothing in between.
- Body text alternates between `text-sm` and `text-xs` without rules.
- Everything in section headers uses `tracking-wider`/`tracking-widest` — when everything is spaced out, nothing gets emphasis.

### Proposed Type Scale

| Level | Font | Size | Weight | Tracking | Use |
|-------|------|------|--------|----------|-----|
| **Display** | Orbitron | `text-3xl` (30px) | 800 | `tracking-wider` | Page title only (commodity name) |
| **H1** | Orbitron | `text-xl` (20px) | 700 | `tracking-wider` | Primary section headers (NEWS THEMES, PRICE CHART) |
| **H2** | Share Tech Mono | `text-base` (16px) | 700 | `tracking-wide` | Sub-section labels, card titles (cluster theme names) |
| **Body** | Share Tech Mono | `text-sm` (14px) | 400 | normal | Article titles, descriptions, explanations |
| **Caption** | Share Tech Mono | `text-xs` (12px) | 400 | normal | Timestamps, sources, metadata, badges |
| **Micro** | Share Tech Mono | `text-[11px]` | 400 | normal | Footnotes, tech credits |

**Rule**: Orbitron is for display and section headers ONLY. Never for body text. It's hard to read at small sizes.

**Rule**: `tracking-widest` is reserved for badges and labels (BULLISH, DIVERGENCE, THESIS). Don't apply wide tracking to everything — it dilutes emphasis.

---

## 3. Spacing & Layout

### Current State (Audit)

Spacing is ad-hoc:
- Section header margins: `mt-8 mb-4`
- Card padding: `p-5` (price), `p-4` (cluster), `p-6` (sentiment), `p-3.5` (article) — four different values for the same purpose
- List spacing: `space-y-3` (clusters), `space-y-2.5` (articles), `space-y-1` (sidebar) — inconsistent

### Proposed Spacing Tokens

Use a 4px base grid (Tailwind's default):

| Token | Value | Usage |
|-------|-------|-------|
| `gap-section` | `mt-10 mb-5` (40px / 20px) | Between major sections |
| `gap-card` | `space-y-3` (12px) | Between sibling cards |
| `pad-card` | `p-5` (20px) | All card internal padding — ONE value |
| `pad-card-compact` | `p-3` (12px) | Nested cards, article rows |
| `gap-inline` | `gap-3` (12px) | Between inline badges/pills |

**Rule**: Card padding is ALWAYS `p-5`. If you need less padding, you're in a compact context — use `p-3`. No other values.

---

## 4. Card System

### Card Anatomy

Every card follows this structure:

```
┌──────────────────────────────────┐
│ top-beam (0.5px, sentiment color)│ ← status indicator
│                                  │
│  TITLE                BADGE      │ ← header row
│  subtitle / metadata             │ ← support row
│                                  │
│  [body content]                  │ ← optional
│                                  │
│  badge  badge  badge             │ ← footer pills
└──────────────────────────────────┘
```

### Card Variants

| Variant | Used for | Border | Glow |
|---------|----------|--------|------|
| **Metric card** | Price cards, sentiment stats | Sentiment-colored (green/red) | Subtle, on hover only |
| **Intelligence card** | Cluster cards, briefing items | Sentiment-colored | On hover + active |
| **Content card** | Article cards, news items | Left-border accent (3px) | None |
| **Container card** | Chart wrapper, sentiment panel | `cyan/10` default | None |

### Card Background

All cards use the same gradient: `linear-gradient(145deg, #1a1a2e, #0d0d22)`. This is currently consistent. Keep it.

---

## 5. Iconography

### Current State (Audit)

Using emoji throughout: section headers (💰📈🎯🧠📰), commodity icons (🥇🛢️🔥🌾🌽), landing page features.

**Problem**: Emoji render differently across OS/browser. A $50-100/month product should not rely on emoji for core UI. They're unpredictable, uncontrollable, and look different on Mac vs Windows vs Android.

### Proposed Approach

**Phase 1 (now)**: Keep emoji for commodity icons only — they're functional identifiers and users are accustomed to them. Remove emoji from section headers — they add visual noise without information.

**Phase 2 (with layout redesign)**: Replace commodity emoji with custom SVG icons or a consistent icon set (Lucide, Phosphor, or custom). Use 16x16 monochrome icons that match the monospace aesthetic.

**Section headers should use COLOR, not icons, as their differentiator.** The cyan glow on "NEWS THEMES" is already enough — the 🎯 adds nothing.

---

## 6. Motion Principles

### Current State (Audit)

Motion is applied liberally:
- `animate-float` on: commodity emoji, EVERY section header icon (6+ floating elements)
- `animate-glow-pulse` on: sidebar brand, commodity header, sentiment score (3 simultaneous glowing elements)
- `animate-border-glow` on: ALL price cards simultaneously (cyan↔magenta cycle, which conflicts with green/red semantic coloring)
- Scan line (`body::after`): runs continuously on a 4s loop
- Framer Motion: staggered card entry, hover lifts, expand/collapse — these are GOOD

**Diagnosis**: Too many ambient animations. When everything moves, nothing draws attention. The eye has nowhere to rest.

### Proposed Motion Rules

| Category | Allowed | Examples |
|----------|---------|---------|
| **Entry** | Yes — staggered, subtle | Cards fade in with 80ms stagger. Current implementation is good. |
| **Interaction** | Yes — responsive to user action | Hover lift on cards, expand/collapse on clusters, filter transitions |
| **State change** | Yes — communicates new data | Price update flash, new cluster appearance, divergence alert |
| **Ambient** | Sparingly — max 1 element | Scan line on page load (once, not looping). Brand glow in sidebar (subtle, single element). |
| **Decorative** | No | Floating emojis, gratuitous bouncing, border color cycling |

**Specific fixes**:
1. Remove `animate-float` from ALL section header icons. Keep it on the commodity header only.
2. Remove `animate-glow-pulse` from sidebar brand and sentiment score. Keep it on the commodity header only (the one thing that changes when you switch commodities).
3. Replace `animate-border-glow` (cyan↔magenta cycle) on price cards with a STATIC border that matches sentiment (green or red). The border should communicate direction, not just glow.
4. Make scan line one-shot on page load, or slow it to 12+ seconds so it's subliminal.

---

## 7. Component Patterns

### Badges

Badges communicate status. They are small, pill-shaped, always `text-xs font-bold tracking-wider`.

| Badge type | Example | Style |
|------------|---------|-------|
| Sentiment | `BULLISH +0.34` | Green bg/text, rounded |
| Conviction | `THESIS` | Cyan text, no bg |
| Divergence | `DIVERGENCE` | Gold bg/text, gold border — MOST PROMINENT badge |
| Source | `Reuters` | Blue bg/text, subtle |
| Count | `4 articles` | Gray text, no bg |

### Dividers

Section dividers use the gradient line pattern already in `SectionHeader`:
```
background: linear-gradient(90deg, currentColor 0%, transparent 80%)
```
This is consistent. Keep it.

### Loading States

**Current**: Plain text "LOADING DATA..." and "Loading..."
**Proposed**: Skeleton shimmer cards that match the card layout. The skeleton communicates "content is coming" without jarring text.

### Empty States

**Current**: "No theme clusters detected. Not enough articles to form patterns."
**Proposed**: Same text, but styled with a subtle border-dashed card at 50% opacity. The empty state should look like a ghost of the card that will appear.

---

## 8. Dashboard Information Hierarchy

### Current Order (Audit)

```
1. Commodity Header (name, ticker, timeframe)
2. LIVE PRICES (4 price cards)
3. PRICE CHART (area chart)
4. NEWS THEMES (cluster cards)
5. SENTIMENT ANALYSIS (score panel)
6. LATEST NEWS (article list)
```

### Problems

- **Prices are above clusters.** Raj said: "Live prices I can see everywhere." The differentiator (clusters/intelligence) is below the fold.
- **Chart is between prices and clusters.** It separates the two things that should be connected: cluster hover highlights the chart.
- **Sentiment panel is between clusters and news.** It's secondary data that interrupts the narrative flow: clusters → articles.

### Proposed Hierarchy (for news-first layout redesign, Task #34)

This is a separate design spec, not part of the design system. But the hierarchy should be:

```
LEFT PANEL (60%) — Intelligence:          RIGHT PANEL (40%) — Context:
1. Daily Briefing (when built)            1. Price Card (selected commodity)
2. News Theme Clusters                    2. Price Chart
3. Latest News (filtered)                 3. Sentiment Summary (compact)
```

The design system defines the components. The layout spec defines their arrangement. See Task #34 for layout proposal.

---

## 9. Audit Summary — What to Keep vs Change

### Keep (working well)
- Orbitron + Share Tech Mono pairing
- Green/Red semantic sentiment coloring
- Card gradient backgrounds (consistent)
- Cluster card interaction model (hover→chart highlight, click→expand)
- Conviction ladder visualization (NOTICE/ATTENTION/THESIS)
- Divergence badge prominence
- Gradient section dividers
- Staggered entry animations (Framer Motion)
- Mobile hamburger sidebar (works, responsive)

### Change (needs fixing)
- Remove ghost colors (blue, purple, amber) from palette
- Fix neutral article border inconsistency (magenta vs gray)
- Flatten card padding to one value (p-5 or p-3)
- Reduce type scale jump between commodity header and section headers
- Remove emoji from section headers
- Kill floating animation on section icons
- Kill glow-pulse on sidebar brand and sentiment score
- Replace border-glow animation on price cards with static sentiment borders
- Make scan line one-shot or much slower
- Add skeleton loading states
- Style empty states as ghost cards

### Add (missing)
- Defined spacing tokens
- Focus/keyboard navigation styling
- State change animations (price update flash, new cluster pulse)
- A proper favicon (currently SVG but no evidence of design intent)
