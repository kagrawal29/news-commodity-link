# Divergence Card — Visual Treatment Spec

**Author**: Priya (Designer)
**Date**: 2026-02-25
**Status**: v3 — USER VALIDATED. Raj confirmed all 4 design questions + added 3 refinements.
**Dependency**: Ships on current layout (before Task #34 layout redesign). Gated behind Task #41.
**Source**: FB-021 (hierarchy flip) + Raj validation (sort, glow, article split dots)

---

## Why This Matters

Divergence detection is the product's signature feature. Raj's exact words:

> "I spent 20 seconds on the DIVERGENCE flag — immediately synthesized 'safe-haven demand not enough to offset supply pressure.'" (VR-002)

> "The divergence card should be the thing a trader screenshots and sends to their group chat. That's the viral moment." (FB-021)

This is where traders make money — on the gap between narrative and reality. Currently, a divergence cluster looks almost identical to any other cluster. The divergence text is buried at the bottom as small italic gold text. Raj wants the opposite: **lead with the conflict**.

---

## The Hierarchy Flip (FB-021)

Raj's key insight: the conflict IS the headline. Don't bury it.

```
CURRENT HIERARCHY:                    RAJ'S DESIRED HIERARCHY:

1. Theme name (biggest)               1. CONFLICT LINE (biggest)
2. Headline summary                       "News: BEARISH / Price: RISING"
3. Sentiment · articles · price        2. Explainer (when available)
4. DIVERGENCE badge (small, buried)       "Why this is weird"
5. Divergence detail (italic, tiny)    3. Theme name
6. Explainer (cyan border)            4. Headline summary
7. Keywords (transparency)             5. Sentiment · articles · price
                                       6. Keywords (evidence)
```

Lead with what's weird. Then explain why. Then provide context.

---

## Mockups

### Normal Cluster (unchanged — for comparison)

```
┌──────────────────────────────────────────────────────┐  ← 1px sentiment border
│                                                      │
│  OPEC Supply Pressure                      [THESIS]  │
│  "Saudi signals production cut extension"            │
│                                                      │
│  BEARISH -0.64  ·  4 articles  ·  +1.8%             │
│                                                      │
│  ┃ "OPEC signaling extended cuts normally..."        │  ← cyan left border
│                                                      │     (explainer, when avail.)
│  Matched: 2 mention opec, 2 mention saudi            │  ← keywords always shown
│                                                      │
└──────────────────────────────────────────────────────┘
```

### Divergence Cluster — Collapsed

```
╔══════════════════════════════════════════════════════════╗
║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓║  ← gold top beam
║                                                          ║  ← 2px GOLD border
║                                                          ║     gold glow
║   News: BEARISH  /  Price: RISING           ◆ DIVERGENCE ║  ← LINE 1: conflict
║                                                          ║     conflict = biggest text
║   OPEC Supply Pressure                         [THESIS]  ║  ← LINE 2: theme + conviction
║   "Saudi signals production cut extension"               ║  ← LINE 3: headline summary
║                                                          ║
║   BEARISH -0.64  ·  4 articles  ·  +1.8%                ║  ← LINE 4: data badges
║                                                          ║
╚══════════════════════════════════════════════════════════╝

Visual properties:
- Border: 2px gold (#FFD700/30)
- Top beam: gold gradient
- Glow: 0 0 20px rgba(255,215,0,0.15)
- ◆ DIVERGENCE badge: subtle pulse animation (badge only, NOT card)
- Card is taller than normal clusters (more vertical padding: p-5 vs p-4)
- Conflict line is text-base font-bold (largest text in card)
  "News:" and "Price:" in gold, "BEARISH" in red, "RISING" in green
```

### Divergence Cluster — Collapsed (with explainer available)

```
╔══════════════════════════════════════════════════════════╗
║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓║
║                                                          ║
║   News: BEARISH  /  Price: RISING           ◆ DIVERGENCE ║  ← conflict (biggest)
║                                                          ║
║   ┃ "OPEC signaling extended cuts would normally         ║  ← explainer sits here
║   ┃  support prices, but oil is rising on demand         ║     GOLD left border
║   ┃  optimism instead."                                  ║     between conflict
║                                                          ║     and theme name
║   OPEC Supply Pressure                         [THESIS]  ║  ← theme
║   "Saudi signals production cut extension"               ║  ← headline
║                                                          ║
║   BEARISH -0.64  ·  4 articles  ·  +1.8%                ║  ← data
║                                                          ║
╚══════════════════════════════════════════════════════════╝

Reading flow:
1. CONFLICT — "News is bearish but price is rising" (what's weird)
2. EXPLAINER — "Because demand optimism is winning" (why it's weird)
3. THEME — "OPEC Supply Pressure" (what topic)
4. HEADLINE — "Saudi signals production cut..." (the story)
5. DATA — sentiment, articles, price delta (the evidence)

This is Raj's exact model: conflict → interpretation → context → evidence.
```

### Divergence Cluster — Hovered

```
╔══════════════════════════════════════════════════════════╗
║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓║
║                                                          ║  gold glow INTENSIFIED
║   News: BEARISH  /  Price: RISING           ◆ DIVERGENCE ║  (0 0 30px)
║                                                          ║
║   ┃ "OPEC signaling extended cuts..."                    ║  Card lifts -2px
║                                                          ║
║   OPEC Supply Pressure                         [THESIS]  ║  → Chart shows gold
║   "Saudi signals production cut extension"               ║    ReferenceArea
║                                                          ║    highlight band
║   BEARISH -0.64  ·  4 articles  ·  +1.8%                ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

Hover adds: glow intensify + translateY: -2px lift + chart highlight
Same as collapsed otherwise. No content changes on hover.
```

### Divergence Cluster — Expanded

```
╔══════════════════════════════════════════════════════════╗
║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓║
║                                                          ║
║   News: BEARISH  /  Price: RISING           ◆ DIVERGENCE ║
║                                                          ║
║   ┃ "OPEC signaling extended cuts would normally         ║  ← explainer (gold border)
║   ┃  support prices, but oil is rising on demand         ║
║   ┃  optimism instead. The divergence suggests the       ║
║   ┃  market is pricing in demand recovery over           ║
║   ┃  supply constraints."                                ║
║                                                          ║
║   OPEC Supply Pressure                         [THESIS]  ║
║   "Saudi signals production cut extension"               ║
║                                                          ║
║   BEARISH -0.64  ·  4 articles  ·  +1.8%                ║
║                                                          ║
║   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ║
║                                                          ║
║   ARTICLES                                               ║
║   +0.34  Saudi extends voluntary production cuts         ║
║          Reuters · 2h ago                                ║
║   -0.21  OPEC output falls below quota as Russia...      ║
║          Oilprice.com · 5h ago                           ║
║   +0.12  China crude imports surge to 3-month high       ║
║          Yahoo Finance · 8h ago                          ║
║   -0.45  Russia tanker rates hit 6-year highs...         ║
║          Investing.com · 12h ago                         ║
║                                                          ║
║   Matched: 2 mention opec, 2 mention saudi, 2 tanker    ║  ← keywords (always shown)
║                                                          ║
╚══════════════════════════════════════════════════════════╝

Expanded adds: article list + keyword evidence.
Explainer is ALWAYS visible (collapsed AND expanded) — not hidden behind expand.
Keywords are ALWAYS visible (collapsed AND expanded) — per architect flag.
Articles are expand-only content.
```

---

## Side-by-Side: Normal vs Divergence

```
    NORMAL CLUSTER                   DIVERGENCE CLUSTER
┌─────────────────────────┐    ╔══════════════════════════════╗
│ 1px sentiment border    │    ║ 2px GOLD border              ║
│                         │    ║ gold glow + top beam         ║
│ Theme          [BADGE]  │    ║                              ║
│ "Headline..."           │    ║ News: BEAR / Price: RISE  ◆  ║  ← CONFLICT FIRST
│                         │    ║                              ║
│ BULLISH +0.41  2 art    │    ║ ┃ "Explainer text..."        ║  ← WHY (gold border)
│                         │    ║                              ║
│ ┃ Explainer (cyan)      │    ║ Theme              [BADGE]   ║
│                         │    ║ "Headline..."                ║
│ Keywords                │    ║                              ║
│                         │    ║ BEARISH -0.64  4 art  +1.8%  ║
└─────────────────────────┘    ║                              ║
  ↑ theme-first               ║ Keywords                     ║
  ↑ cool tones                ╚══════════════════════════════╝
  ↑ standard height              ↑ conflict-first
                                 ↑ warm gold tones
                                 ↑ taller, more padding
                                 ↑ ◆ badge pulses
```

**The screenshot test (Raj's litmus)**: The conflict line at the top + gold border = the viral moment. A trader screenshots this card because the conflict is immediately legible. "News: BEARISH / Price: RISING" is the tweet. The rest is context.

---

## Animation: Badge Pulse + Ambient Glow

Two layers of animation, both subtle. Raj: "like a slow heartbeat, not a strobe."

### Layer 1: ◆ Badge Pulse (draws direct attention)

```css
@keyframes badgePulse {
  0%, 100% {
    text-shadow: 0 0 4px rgba(255, 215, 0, 0.3);
    opacity: 0.9;
  }
  50% {
    text-shadow: 0 0 12px rgba(255, 215, 0, 0.6);
    opacity: 1;
  }
}

.divergence-badge {
  animation: badgePulse 2.5s ease-in-out infinite;
}
```

The ◆ diamond gently breathes. Faster cycle (2.5s) — catches direct attention.

### Layer 2: Ambient Glow Breathe (catches peripheral vision)

```css
@keyframes glowBreathe {
  0%, 100% {
    box-shadow: 0 0 15px rgba(255, 215, 0, 0.10);
  }
  50% {
    box-shadow: 0 0 25px rgba(255, 215, 0, 0.18);
  }
}

.divergence-card {
  animation: glowBreathe 4s ease-in-out infinite;
}
```

The card's box-shadow subtly expands and contracts. Slower cycle (4s) — peripheral, subliminal. Raj: "If it's static, my eye will learn to skip it. If it breathes, it stays alive."

### What does NOT animate

- Card border (static 2px gold)
- Card background
- Any text content
- Border color

The border is stable structure. The glow is alive ambience. The badge is active signal. Three layers, three speeds, three purposes.

---

## Conflict Line Typography

The conflict line is the biggest text in the divergence card. Spec:

```
"News: BEARISH  /  Price: RISING"
 ^^^^               ^^^^^
 gold               gold
        ^^^^^^^          ^^^^^^
        signal-red       signal-green
```

| Element | Style |
|---------|-------|
| "News:" | `text-cyber-gold text-base font-bold` |
| Sentiment word ("BEARISH") | Sentiment-colored: `text-cyber-red` if negative, `text-cyber-green` if positive |
| "/" separator | `text-gray-500` |
| "Price:" | `text-cyber-gold text-base font-bold` |
| Direction word ("RISING") | Price-direction-colored: `text-cyber-green` if price up, `text-cyber-red` if price down |
| "◆ DIVERGENCE" | `text-cyber-gold text-xs font-bold tracking-widest` — right-aligned, badge-pulsing |

The mixed colors in the conflict line ARE the divergence — red and green in the same line. The visual contrast tells the story before you read the words.

### Deriving the Conflict Line

The conflict line is constructed from existing cluster data:

```typescript
// Pseudo-code for the conflict line
const sentimentWord = cluster.sentiment_label === "positive" ? "BULLISH" : "BEARISH";
const priceWord = cluster.price_delta_pct >= 0 ? "RISING" : "FALLING";

// Only show conflict line when cluster.divergence is truthy
// "News: BULLISH / Price: FALLING" or "News: BEARISH / Price: RISING"
```

---

## Explainer + Description Display Rules

Per architect flag (design-principles.md: "show your work"), BOTH explanation and description are always visible when they exist. Description is the evidence that grounds the LLM narrative.

| Condition | Collapsed | Expanded |
|-----------|-----------|----------|
| `explanation` + `description` | Explanation (gold border) + description below (gray, secondary) | Same + articles |
| `explanation` only | Explanation (gold border) | Same + articles |
| `description` only | Description (gray, no border) | Same + articles |
| Neither | Just conflict + theme + data | Same + articles |

**Hierarchy within the collapsed card** (when both exist):

```
1. Conflict line
2. Explanation (gold ┃ border, text-sm, text-gray-300)
3. Theme name
4. Headline
5. Data badges
6. Description/keywords (text-xs, text-gray-500)
```

The explanation is intelligence. The description is evidence. Both earn their space.

---

## CSS Token Spec (for dev)

```typescript
const DIVERGENCE_STYLE = {
  // Card treatment
  border: "border-2 border-cyber-gold/30",
  glow: "0 0 20px rgba(255,215,0,0.15)",
  glowHover: "0 0 30px rgba(255,215,0,0.2)",
  glowExpanded: "0 0 35px rgba(255,215,0,0.25)",
  topBeam: "linear-gradient(90deg, transparent, rgba(255,215,0,0.5), transparent)",
  padding: "p-5",  // taller than normal cards (p-4)

  // Explainer border
  explanationBorder: "border-l-2 border-cyber-gold/40",

  // Chart highlight
  chartHighlight: "rgba(255,215,0,0.08)",
};
```

### Implementation Changes: ClusterCards.tsx

**1. New component: ConflictLine**

```typescript
function ConflictLine({ cluster }: { cluster: NewsCluster }) {
  if (!cluster.divergence) return null;

  const sentimentWord = cluster.sentiment_label === "positive" ? "BULLISH" : "BEARISH";
  const sentimentColor = cluster.sentiment_label === "positive" ? "text-cyber-green" : "text-cyber-red";
  const priceUp = (cluster.price_delta_pct ?? 0) >= 0;
  const priceWord = priceUp ? "RISING" : "FALLING";
  const priceColor = priceUp ? "text-cyber-green" : "text-cyber-red";

  return (
    <div className="flex items-center justify-between mb-3">
      <div className="text-base font-bold">
        <span className="text-cyber-gold">News: </span>
        <span className={sentimentColor}>{sentimentWord}</span>
        <span className="text-gray-500 mx-2">/</span>
        <span className="text-cyber-gold">Price: </span>
        <span className={priceColor}>{priceWord}</span>
      </div>
      <span className="text-xs font-bold tracking-widest text-cyber-gold divergence-badge">
        ◆ DIVERGENCE
      </span>
    </div>
  );
}
```

**2. Card render order (when divergence exists)**

```
<ConflictLine />                    ← NEW: conflict first
{explanation && <ExplainerBlock />} ← MOVED UP: gold border
<ThemeName + ConvictionBadge />     ← was first, now third
<HeadlineSummary />                 ← unchanged position relative to theme
<DataBadges />                      ← unchanged
{description && <Keywords />}       ← ALWAYS visible (not hidden by explanation)
```

**3. Remove from current render:**
- Remove the inline `DIVERGENCE` badge from the data pill row (lines 127-131)
- Remove the standalone divergence detail text (lines 134-139) — replaced by ConflictLine

**4. Card-level overrides when divergence exists:**
- Border class: swap from `${colors.border}` to `"border-2 border-cyber-gold/30"`
- Box shadow: swap from `${colors.glow}` to gold glow values
- Padding: `p-5` instead of `p-4`
- Add `whileHover={{ y: -2 }}` (divergence only)
- Add gold top beam `div` (same pattern as PriceCards)
- Add `divergence-card` class to the `motion.div` for the glow breathe animation

> **DEV NOTE (easy to miss):** The explainer left border changes color based on divergence state. When `cluster.divergence` is truthy, use `border-cyber-gold/40`. When falsy, use `border-cyber-cyan/20`. This single conditional is what makes the divergence card feel cohesive (all gold) vs a normal card (cyan accents). Apply this to the `border-l-2` on the explanation `div`.

**5. Animations CSS** — add to globals.css:
```css
.divergence-badge {
  animation: badgePulse 2.5s ease-in-out infinite;
}
@keyframes badgePulse {
  0%, 100% { text-shadow: 0 0 4px rgba(255,215,0,0.3); opacity: 0.9; }
  50% { text-shadow: 0 0 12px rgba(255,215,0,0.6); opacity: 1; }
}

.divergence-card {
  animation: glowBreathe 4s ease-in-out infinite;
}
@keyframes glowBreathe {
  0%, 100% { box-shadow: 0 0 15px rgba(255,215,0,0.10); }
  50% { box-shadow: 0 0 25px rgba(255,215,0,0.18); }
}
```

**6. Sort clusters before render** — apply `sortClusters()` (see Sort Order section) to `clusters.clusters` before `.map()`.

**7. Article split dots** — pass `showDot={!!cluster.divergence}` to `ClusterArticleRow` in expanded section.

### Implementation in PriceChart.tsx

When hovered cluster has `divergence` truthy, use `rgba(255,215,0,0.08)` as ReferenceArea fill instead of sentiment color.

---

## Behavioral Spec

### Card Physical Size

Divergence cards are TALLER than normal clusters:
- Normal cluster padding: `p-4`
- Divergence cluster padding: `p-5`
- Conflict line adds ~32px of height
- Explainer (when present) adds ~48-72px
- Result: divergence card is roughly 1.5-2x the height of a normal cluster

This matches Raj's request: "visually larger/taller than normal clusters."

### Entry Animation

Normal clusters: fade in + translate up (`opacity: 0→1, y: 8→0`).

Divergence clusters: same entry + badge pulse begins + ambient glow breathing begins. Two animations running simultaneously — badge at 2.5s cycle (direct attention), glow at 4s cycle (peripheral awareness).

### Hover

| Property | Normal cluster | Divergence cluster |
|----------|---------------|-------------------|
| Glow intensity | Subtle increase | `0 0 30px rgba(255,215,0,0.2)` |
| Lift | None | `translateY: -2px` |
| Cursor | pointer | pointer |
| Chart highlight fill | Sentiment-colored | Gold `rgba(255,215,0,0.08)` |

### Expanded

Expanded adds: article list below a divider. Everything else (conflict, explainer, theme, headline, data, keywords) is ALREADY visible in collapsed state. Expanding only reveals the article evidence trail.

### What Does NOT Happen (per Raj)

- No modals or popups. Everything is inline.
- No sound effects. The visual treatment is enough.
- No border animation or background animation. Border stays static 2px gold.
- No auto-expand. The trader clicks when ready.

### What DOES Animate (per Raj validation)

- ◆ badge pulse (2.5s cycle) — direct attention signal
- Ambient glow breathe (4s cycle) — peripheral "stays alive" signal. Raj: "If it's static, my eye will learn to skip it."
- Hover lift (`translateY: -2px`) — on user interaction only

---

## Reading Flow (Updated for Hierarchy Flip)

```
SCAN (0-2 seconds):
Eyes land on the gold card. It's taller, warmer, the ◆ badge pulses gently.
Trader immediately knows: "Something doesn't add up here."

READ (2-5 seconds):
Conflict line: "News: BEARISH / Price: RISING" — the what.
Explainer: "Demand optimism is winning over supply fear" — the why.
Theme: "OPEC Supply Pressure" — the context.
In 5 seconds, the trader has: conflict + explanation + topic.

INVESTIGATE (5-15 seconds, if they click to expand):
Articles reveal the evidence trail.
Chart zooms to the time window (on layout redesign).
Keywords show matching methodology.

DECIDE:
"Oil: bearish supply news but demand is stronger. Don't short.
Wait for demand narrative to break before going bearish."
Opens TradingView with conviction.
```

This is the card a trader screenshots. Conflict line + explainer in one view = the viral moment.

---

## Sort Order (Raj-validated)

Divergence clusters ALWAYS float to top. Raj: "No question."

```
Sort priority:
1. Divergence clusters (sorted by article count within group)
2. THESIS clusters (3+ articles, non-divergence)
3. ATTENTION clusters (2 articles)
4. NOTICE clusters (1 article)
```

If multiple divergence clusters exist, rank by article count within the divergence tier. More articles = more signal conviction.

### Implementation

In `ClusterCards.tsx`, sort the clusters array before rendering:

```typescript
function sortClusters(clusters: NewsCluster[]): NewsCluster[] {
  return [...clusters].sort((a, b) => {
    // Divergence clusters first
    const aDivergence = a.divergence ? 1 : 0;
    const bDivergence = b.divergence ? 1 : 0;
    if (aDivergence !== bDivergence) return bDivergence - aDivergence;

    // Within same tier, sort by article count (descending)
    return b.article_count - a.article_count;
  });
}
```

---

## Expanded State: Article Sentiment Split

Raj: "In a divergence cluster, I want to see the SPLIT — which headlines are fighting the price and which are aligned. That split IS the story."

### Current Article Row

```
+0.34  Saudi extends voluntary production cuts
       Reuters · 2h ago
```

### Proposed Article Row (divergence clusters only)

```
● +0.34  Saudi extends voluntary production cuts          ← green dot
         Reuters · 2h ago
● -0.21  OPEC output falls below quota as Russia...       ← red dot
         Oilprice.com · 5h ago
● +0.12  China crude imports surge to 3-month high        ← green dot
         Yahoo Finance · 8h ago
● -0.45  Russia tanker rates hit 6-year highs...          ← red dot
         Investing.com · 12h ago
```

A small colored circle (8px) before the sentiment score:
- `●` green for positive articles (aligned with bullish narrative)
- `●` red for negative articles (aligned with bearish narrative)
- `●` gray for neutral

On non-divergence clusters, the dots are optional (current score coloring is sufficient). On divergence clusters, the dots make the split visible at a glance — how many articles are bullish vs bearish? The visual ratio IS the divergence.

### Implementation

In `ClusterArticleRow`, when the parent cluster has `divergence` truthy, render a colored dot before the score:

```typescript
function ClusterArticleRow({ article, showDot }: { article: ClusterArticle; showDot?: boolean }) {
  const dotColor =
    article.sentiment_label === "positive" ? "bg-cyber-green"
    : article.sentiment_label === "negative" ? "bg-cyber-red"
    : "bg-gray-500";

  return (
    <a ...>
      {showDot && (
        <span className={`w-2 h-2 rounded-full shrink-0 mt-1.5 ${dotColor}`} />
      )}
      <span className={`text-xs font-mono font-bold shrink-0 mt-0.5 ${scoreColor}`}>
        ...
      </span>
      ...
    </a>
  );
}
```

Pass `showDot={!!cluster.divergence}` from the parent.

---

## Validation Status — USER VALIDATED

All 4 questions answered by Raj. All original design directions confirmed + 3 refinements added:

- [x] Gold border + glow — CONFIRMED. "Gold = this is special, look closer." Intriguing, not alarming.
- [x] Conflict line leads (hierarchy flip) — CONFIRMED. Format is clear and scannable.
- [x] Color-coded conflict text (red/green clash) — CONFIRMED. "Even before I read the words, the red/green clash tells me something's off."
- [x] Explainer between conflict and theme — CONFIRMED. "Conflict → Why → Context matches how my brain processes."
- [x] Explainer bar in gold — CONFIRMED. "Ties it to the divergence card identity."
- [x] Sort to top — CONFIRMED. "ALWAYS on top. No question."
- [x] Card is taller/larger — CONFIRMED by padded hierarchy.
- [x] Badge pulses (not card border) — CONFIRMED.
- [x] No modals, no popups, no sound — CONFIRMED.
- [x] Screenshot-worthy — CONFIRMED. "If I saw that card at 8am, I'd screenshot it."

**Added per Raj validation (v3):**
- [x] Ambient glow breathe (4s cycle) — "If it's static, my eye will learn to skip it."
- [x] Divergence sort priority (divergence → THESIS → ATTENTION → NOTICE)
- [x] Article sentiment split dots in expanded state — "That split IS the story."
