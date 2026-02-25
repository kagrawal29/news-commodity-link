# Commodity Pulse — News-First Layout Redesign Spec

**Author**: Priya (Designer) + Architect alignment
**Task**: #34 (FB-012, FB-013)
**Date**: 2026-02-25
**Status**: v2 — Approved by architect with 3 flags addressed (see changelog)

---

## 1. Design Goal

Shift the dashboard from a **data terminal** (prices first, intelligence buried) to an **intelligence terminal** (narratives first, prices as context).

**Raj's words**: "Live prices I can see everywhere. Tell me the narrative."

**Success metric**: Raj scans cluster cards and has a directional thesis within 90 seconds of opening the dashboard — before looking at the chart.

---

## 2. Layout Architecture

### Desktop (1280px+)

```
┌────────┬──────────────────────────────────┬─────────────────────────┐
│SIDEBAR │     INTELLIGENCE PANEL (60%)      │   CONTEXT PANEL (40%)   │
│ 256px  │     scrollable                    │   sticky                │
│        │                                   │                         │
│ BRAND  │ ┌───────────────────────────────┐ │ ┌─────────────────────┐ │
│        │ │ ★ DAILY BRIEFING              │ │ │ GOLD     $2,341.50  │ │
│ ────── │ │ "3 things to know about Gold" │ │ │ ▲ +1.2%  (+$27.80) │ │
│        │ │ 1. OPEC supply cut (bearish)  │ │ │                     │ │
│  Gold● │ │ 2. Fed rates (bullish)        │ │ │ 30d ▸ 7d ▸ 1d      │ │
│  Silver│ │ 3. Safe haven demand (bullish)│ │ └─────────────────────┘ │
│  Oil   │ │ Net: BULLISH, 0.72 confidence │ │                         │
│  Gas   │ └───────────────────────────────┘ │ ┌─────────────────────┐ │
│  Copper│                                   │ │                     │ │
│  Plat. │ ── NEWS THEMES ────────────────── │ │    PRICE CHART      │ │
│  Wheat │                                   │ │                     │ │
│  Corn  │ ┌───────────────────────────────┐ │ │  Cluster hover =    │ │
│        │ │ OPEC Supply Pressure  [THESIS]│ │ │  highlight window   │ │
│ ────── │ │ "Saudi signals production cut │ │ │                     │ │
│        │ │  extension through Q3"        │ │ │  Cluster click =    │ │
│ 1 Day  │ │ BEARISH -0.64 · 4 articles   │ │ │  zoom to window     │ │
│ 7 Days │ │ +1.8% · ◆ DIVERGENCE         │ │ │                     │ │
│30 Days●│ └───────────────────────────────┘ │ └─────────────────────┘ │
│90 Days │                                   │                         │
│ 1 Year │ ┌───────────────────────────────┐ │ ┌─────────────────────┐ │
│        │ │ Fed Rate Expectations  [ATTN] │ │ │ SENTIMENT COMPACT   │ │
│ ────── │ │ "Fed minutes show hawkish     │ │ │ ▲ +0.34 BULLISH     │ │
│ footer │ │  split on rate cut timing"    │ │ │ ████░░░░░ 62% pos   │ │
│        │ │ BULLISH +0.41 · 2 articles    │ │ │ Conf: 71% · ↗ Imp. │ │
│        │ └───────────────────────────────┘ │ └─────────────────────┘ │
│        │                                   │                         │
│        │ ┌───────────────────────────────┐ │ ┌─────────────────────┐ │
│        │ │ Safe Haven Demand    [NOTICE] │ │ │ RELATED PRICES      │ │
│        │ │ "Gold ETF inflows hit 3-month │ │ │ Silver  $31.20 +0.4%│ │
│        │ │  high amid ME tensions"       │ │ │ Oil     $82.10 -0.8%│ │
│        │ │ BULLISH +0.22 · 1 article     │ │ │ Copper  $4.21  +0.2%│ │
│        │ └───────────────────────────────┘ │ └─────────────────────┘ │
│        │                                   │                         │
│        │ ── LATEST NEWS ────────────────── │                         │
│        │ [Filterable article list]          │                         │
│        │ [Scrollable, max-height]           │                         │
└────────┴──────────────────────────────────┴─────────────────────────┘
```

### Key Structural Decisions

| Decision | Rationale |
|----------|-----------|
| **Intelligence panel scrolls, context panel is sticky** | Trader scrolls through narratives while chart stays visible for constant price reference. Chart responds to cluster hover/click without disappearing. |
| **Single price card (selected commodity only)** | Current 4-card layout wastes prime real estate. The sidebar already shows all commodities — clicking one switches the whole dashboard. No need to repeat 3 others. |
| **Chart is in context panel, not intelligence panel** | Chart supports the narrative, it doesn't lead it. Raj checks price AFTER reading the story. Chart responds to clusters via hover-highlight and click-zoom. |
| **Sentiment is compact (1 row)** | Current 4-metric horizontal layout is too wide. Compress to: score + distribution bar + confidence + trend in a single compact card. Slope number removed (meaningless to traders). |
| **Related prices at bottom of context panel** | Shows 3 other commodities as compact rows (name + price + change%). Gives cross-market context without full cards. Replaces the current 4-card grid. |
| **Daily briefing at top of intelligence panel** | When built (Task #33), this is the FIRST thing Raj sees. The "5-minute promise" in one card. Before clusters exist, this space is empty (no placeholder). |

---

## 3. Click-to-Expand Interaction (FB-013)

### The Interaction Model

Clusters have THREE states:

```
STATE 1: Collapsed (default)
┌──────────────────────────────────────┐
│ OPEC Supply Pressure        [THESIS] │
│ "Saudi signals production cut        │
│  extension through Q3"               │
│ BEARISH -0.64 · 4 articles · +1.8%  │
│ ◆ DIVERGENCE: Bearish news, +price   │
└──────────────────────────────────────┘
  → Chart: full timeframe, no highlight

STATE 2: Hovered
┌──────────────────────────────────────┐
│ (same content, subtle glow)          │
└──────────────────────────────────────┘
  → Chart: full timeframe + highlight band over cluster time window
  → Already implemented. Keep as-is.

STATE 3: Expanded (clicked)
┌──────────────────────────────────────┐
│ OPEC Supply Pressure        [THESIS] │
│ "Saudi signals production cut        │
│  extension through Q3"               │
│ BEARISH -0.64 · 4 articles · +1.8%  │
│ ◆ DIVERGENCE: Bearish news, +price   │
│ ──────────────────────────────────── │
│ ✦ WHY THIS MATTERS                   │
│ "OPEC signaling extended cuts would  │
│  normally support prices, but oil is  │
│  rising on demand optimism instead.   │
│  The divergence suggests the market   │
│  is pricing in demand recovery over   │
│  supply constraints."                 │
│ ──────────────────────────────────── │
│ ARTICLES                              │
│  +0.34  Saudi extends voluntary cuts  │
│         Reuters · 2h ago              │
│  -0.21  OPEC output falls below...    │
│         Oilprice.com · 5h ago         │
│  +0.12  China crude imports surge...  │
│         Yahoo Finance · 8h ago        │
│  -0.45  Russia tanker rates hit...    │
│         Investing.com · 12h ago       │
└──────────────────────────────────────┘
  → Chart: ZOOMS to cluster time window (animated)
  → Sentiment compact card: shows this cluster's sentiment only
```

### Chart-Cluster Sync Behavior

| Cluster State | Chart Behavior | Transition |
|---------------|---------------|------------|
| None selected | Full timeframe, default view | — |
| Hovered | Full timeframe + ReferenceArea highlight (existing) | Instant |
| Clicked/Expanded | Zoomed to cluster time window ± 2 days padding | 300ms ease-out animation |
| Collapsed (click again) | Zooms back out to full timeframe | 300ms ease-out animation |

**Why zoom, not just highlight?** Highlighting on a 30-day chart makes a 2-day cluster window very small. Zooming lets the trader see WITHIN the cluster's price movement — did the move happen at the start of the cluster or the end? Was it gradual or sudden? This is the temporal causality insight from VR-001 item 3.

### Explanation + Description Display Rules

Per design-principles.md ("show your work"), BOTH explanation and description are visible when they exist. The description (keyword evidence) grounds the LLM narrative in observable data. Hiding it makes the LLM a black box.

| Condition | Display |
|-----------|---------|
| `explanation` AND `description` exist | Explanation (primary, left border) + description below (secondary, text-xs, gray) |
| `explanation` only | Explanation with left border |
| `description` only | Description as secondary text (no border, gray) |
| Neither exists | Don't show the section at all |

For divergence cards specifically: the explanation gets a gold left border (not cyan) and sits between the conflict line and theme name. See `docs/divergence-card-spec.md` for the full hierarchy.

---

## 4. Component Breakdown

### New Components (to build)

| Component | Purpose | Content |
|-----------|---------|---------|
| `ContextPanel.tsx` | Right 40% sticky panel | Wraps PriceCard, PriceChart, SentimentCompact, RelatedPrices |
| `IntelligencePanel.tsx` | Left 60% scrollable panel | Wraps DailyBriefing (future), ClusterCards, NewsFeed |
| `SentimentCompact.tsx` | 1-row sentiment summary | Score + distribution bar + confidence + trend. Replaces full SentimentPanel on this layout. |
| `RelatedPrices.tsx` | Compact price list | 3 rows showing other commodities (name + price + change%). |
| `PriceCardSingle.tsx` | Single commodity price display | Selected commodity only. Name, price, change, change%. Larger than current cards. |

### Modified Components

| Component | Changes |
|-----------|---------|
| `Dashboard.tsx` | Complete refactor. New 2-panel layout. Section headers adjusted. |
| `ClusterCards.tsx` | Add chart-zoom callback (`onClusterClick` in addition to `onClusterHover`). Expanded state shows "WHY THIS MATTERS" section. |
| `PriceChart.tsx` | Add zoom-to-range capability. Accept `zoomRange` prop for cluster click. Animate between full range and zoomed range. |
| `SentimentPanel.tsx` | Keep for potential future use but replace in dashboard with `SentimentCompact`. |
| `PriceCards.tsx` | Keep for potential future use but replace in dashboard with `PriceCardSingle` + `RelatedPrices`. |

### Removed from Dashboard View

| Element | Reason | Replacement |
|---------|--------|-------------|
| 4-card price grid | Takes too much prime real estate, repeats sidebar info | Single price card (right panel) + related prices (compact list) |
| Full sentiment panel | Too data-dense for 40% panel, "slope" is meaningless | Compact 1-row sentiment |
| Commodity header with floating emoji | Redundant with sidebar selection + price card | Removed. Commodity name is in the price card. |

---

## 5. Compact Sentiment Design

Current sentiment panel is 4 horizontal blocks: Score, Distribution, Confidence, Trend. Too wide for a 40% panel.

### Compact Layout

```
┌────────────────────────────────────┐
│ SENTIMENT                          │
│                                    │
│ ▲ +0.34  BULLISH     71% conf.    │
│ ████████░░░░░░░░░ 62%·18%·20%     │
│                         ↗ Improving │
└────────────────────────────────────┘
```

### Content Rules

| Element | Display | Style |
|---------|---------|-------|
| Score | `▲ +0.34` or `▼ -0.21` | Large-ish, sentiment-colored (green/red/gray) |
| Label | `BULLISH` / `BEARISH` / `NEUTRAL` | Same color, uppercase, tracking-wider |
| Confidence | `71% conf.` | Cyan, right-aligned |
| Distribution bar | Full-width, 3-segment | Green/gray/red, same as current |
| Distribution text | `62%·18%·20%` | Below bar, small, gray |
| Trend | `↗ Improving` / `↘ Declining` / `→ Stable` | Right-aligned, sentiment-colored |

**Removed**: Slope number (`Slope: 0.0004`). No trader thinks in slope values. Direction + arrow is sufficient.

---

## 6. Mobile Layout (< 768px)

The 60/40 split collapses to a single column. The intelligence panel is primary. Context is on-demand.

```
┌──────────────────────────────────────┐
│ ☰  COMMODITY PULSE    GOLD $2,341 ▲ │ ← sticky top bar
├──────────────────────────────────────┤
│ [Daily Briefing - when built]        │
│                                      │
│ ── NEWS THEMES ─────────────────     │
│ ┌──────────────────────────────────┐ │
│ │ OPEC Supply Pressure     [THESIS]│ │
│ │ "Saudi signals production cut..."│ │
│ │ BEARISH -0.64 · 4 art. · +1.8% │ │
│ └──────────────────────────────────┘ │
│ ┌──────────────────────────────────┐ │
│ │ Fed Rate Expectations     [ATTN] │ │
│ │ "Fed minutes show hawkish..."    │ │
│ │ BULLISH +0.41 · 2 articles      │ │
│ └──────────────────────────────────┘ │
│                                      │
│ [📊 SHOW CHART]  [📈 SENTIMENT]     │ ← toggle buttons
│                                      │
│ ── LATEST NEWS ─────────────────     │
│ [Article list]                       │
└──────────────────────────────────────┘
```

### Mobile Decisions

| Decision | Rationale |
|----------|-----------|
| **Sticky top bar** with commodity name + price | Always visible context. Replaces separate price card. Hamburger menu for sidebar. |
| **Chart and sentiment are hidden by default** | On mobile, the narrative IS the product. Chart is a confirmation tool accessed on demand. |
| **Toggle buttons** for chart/sentiment | Placed between clusters and news feed. Tapping opens a slide-up panel. |
| **Expanded cluster does NOT zoom chart on mobile** | Chart is hidden. Expanded cluster shows articles + explanation inline only. |

---

## 7. Interaction Choreography

### Page Load Sequence

```
t=0ms     Context panel appears (price card + chart skeleton)
t=100ms   First cluster card fades in
t=180ms   Second cluster card fades in
t=260ms   Third cluster card fades in
t=300ms   Sentiment compact appears
t=400ms   Related prices appear
t=500ms   News feed fades in
```

The intelligence panel loads LEFT to RIGHT visually (clusters before chart fills in), establishing that the left panel is primary.

### Commodity Switch

```
t=0ms     Both panels fade out (opacity 0, y -12)
t=150ms   New data starts loading — skeleton state
t=300ms   New data arrives — staggered fade in (same as page load)
```

Keep the existing `AnimatePresence mode="wait"` pattern. It works.

### Cluster Expand/Collapse

```
EXPAND:
t=0ms     Card border glow intensifies
t=0ms     Content area height animates from 0 to auto (existing)
t=0ms     Chart begins zoom animation (300ms ease-out)
t=100ms   "WHY THIS MATTERS" text fades in
t=150ms   Article rows stagger in (30ms each)

COLLAPSE:
t=0ms     Article rows fade out (instant)
t=0ms     Chart begins zoom-out animation (300ms ease-out)
t=100ms   Content area height animates to 0
t=200ms   Border glow returns to default
```

---

## 8. Divergence Elevation

> **NOTE**: This section covers LAYOUT-LEVEL treatment only (border, glow, card size). The INTERNAL card hierarchy (content order, conflict line, typography) is fully specced in `docs/divergence-card-spec.md` (v2, incorporating FB-021 hierarchy flip). Dev should follow the divergence-card-spec for card internals.

### Layout-Level Treatment

| Property | Normal cluster | Divergence cluster |
|----------|---------------|-------------------|
| Border | 1px, sentiment-colored | 2px, gold |
| Glow | Subtle sentiment glow | Wider gold glow |
| Top beam | Sentiment-colored | Gold |
| Padding | `p-4` | `p-5` (taller card) |
| Hover lift | None | `translateY: -2px` |
| Entry animation | Standard stagger | Standard stagger + ◆ badge pulse |
| Chart highlight | Sentiment-colored fill | Gold fill `rgba(255,215,0,0.08)` |

### Internal Hierarchy (per divergence-card-spec.md)

Per Raj feedback (FB-021), divergence cards FLIP the content hierarchy:

```
1. Conflict line (biggest) — "News: BEARISH / Price: RISING  ◆ DIVERGENCE"
2. Explainer (when available, gold left border)
3. Theme name + conviction badge
4. Headline summary
5. Data badges (sentiment, articles, price delta)
6. Keywords (always visible — evidence/transparency)
```

The conflict IS the headline. Lead with what's weird, then explain why.

---

## 9. Implementation Notes for Dev

### CSS Architecture

The 60/40 split is a CSS Grid or Flexbox layout on the main content area:

```css
/* Grid approach (preferred) */
.dashboard-layout {
  display: grid;
  grid-template-columns: 1fr 0.67fr; /* ~60/40 */
  gap: 1.5rem; /* 24px */
  align-items: start;
}

.context-panel {
  position: sticky;
  top: 1.5rem;
  max-height: calc(100vh - 3rem);
  overflow-y: auto;
}

/* Mobile override */
@media (max-width: 768px) {
  .dashboard-layout {
    grid-template-columns: 1fr;
  }
  .context-panel {
    position: static;
    display: none; /* shown via toggle */
  }
}
```

### Chart Zoom Implementation

The `PriceChart` component needs a `zoomRange` prop:

```typescript
interface PriceChartProps {
  data: PriceHistoryResponse | null;
  commodityName: string;
  highlightCluster?: NewsCluster | null;  // existing: hover highlight
  zoomRange?: { start: string; end: string } | null;  // new: click zoom
}
```

When `zoomRange` is set, filter `chartData` to the specified date range (±2 days padding), and animate the domain transition using Recharts' `animationDuration` prop or a custom interpolation.

> **TECHNICAL RISK (architect flag):** Recharts does not have native zoom animation. Dev should prototype the zoom behavior FIRST, before building the full layout. Options in order of preference:
> 1. Filter `chartData` to zoom range + rely on Recharts' built-in `<Area animationDuration={300} />` for the area redraw. Simple, may look acceptable.
> 2. Custom interpolation between full domain and zoomed domain using `useState` + `requestAnimationFrame`. Smoother but more complex.
> 3. **Fallback**: If zoom animation proves too complex, skip animation entirely — instant zoom on click is still valuable. The interaction (click cluster → see zoomed chart) matters more than the transition.
>
> **Recommendation**: Prototype option 1 first. If the visual is jarring, try option 2. Don't let animation perfectionism block the layout shipping.

### State Management

```
Dashboard state:
  - hoveredCluster: NewsCluster | null  (existing)
  - expandedCluster: string | null      (existing in ClusterCards, lift to Dashboard)
  - chartZoomRange: { start, end } | null  (new, derived from expandedCluster)
```

When `expandedCluster` changes:
- If set: compute zoom range from cluster's `start_time`/`end_time`, pass to PriceChart
- If null: pass null to PriceChart (zoom out to full range)

---

## 10. What This Spec Does NOT Cover

| Out of scope | Why | Where it lives |
|-------------|-----|----------------|
| Daily Briefing card design | Not yet built (Task #33). Design when data shape is known. | Future spec |
| Audio implementation | Specced in brand-guide.md. Separate build (Task #35). | docs/brand-guide.md |
| Cluster card internals | Headlines + explainers are already shipping. Don't redesign cards during layout refactor — just reposition them. | Current ClusterCards.tsx |
| Sidebar changes | Sidebar works. Don't touch it in this pass. | — |
| Landing page updates | Landing page is independent. Update after dashboard redesign settles. | Future |

---

## 11. Definition of Done

- [ ] 60/40 split layout renders correctly on 1280px, 1440px, 1920px widths
- [ ] Intelligence panel scrolls independently; context panel is sticky
- [ ] Single price card in context panel shows selected commodity
- [ ] Chart responds to cluster hover (highlight) and click (zoom)
- [ ] Cluster expand shows articles + explanation (existing), chart zooms (new)
- [ ] Cluster collapse zooms chart back to full range
- [ ] Compact sentiment card replaces full panel
- [ ] Related prices show 3 other commodities in compact rows
- [ ] Mobile: single column, chart/sentiment hidden behind toggles
- [ ] Commodity switch animates both panels
- [ ] Divergence clusters have elevated visual treatment (gold border, wider glow)
- [ ] No regressions: all existing data still displays, keyboard shortcuts still work

---

## 12. Related Prices: Which 3 Commodities?

For MVP: keep the current "next 3 in the list" logic (alphabetical after selected). This matches existing behavior and avoids scope creep.

**Future opportunity**: Show the 3 most correlated commodities (Gold → Silver, Dollar-inverse, Oil). This connects to the parked cross-commodity correlation idea. Don't scope until the layout redesign ships and is validated.

---

## Changelog

**v2 (2026-02-25)** — Architect review incorporated:
- Flag 1: Section 8 clarified as layout-level treatment only. Internal card hierarchy defers to `divergence-card-spec.md` (hierarchy flip per FB-021).
- Flag 2: Display rules updated — show BOTH explanation AND description when both exist. Description is evidence that grounds the LLM narrative.
- Flag 3: Chart zoom technical risk documented. Prototype-first recommendation. Instant-zoom fallback defined.
- Added: Related Prices commodity selection rationale (section 12).
