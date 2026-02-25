# Commodity Pulse — Product Roadmap

**Core Vision**: Turn commodity news noise into trading conviction in 5 minutes.
**Core Loop**: Scan → Understand → Validate → Trade
**Monetization gate**: Intelligence layer = $50-100/month. Dashboard without intelligence = $0. (Source: Raj interview, 2026-02-25)

---

## Phase 1 — Core Dashboard (SHIPPED)
- [x] FastAPI backend (5 endpoints, 8 commodities)
- [x] Next.js cyberpunk dashboard
- [x] Price cards with real-time data
- [x] Price history charts
- [x] News feed with sentiment scoring
- [x] Sentiment filtering (bullish/bearish/neutral)
- [x] Sentiment analysis panel (score, distribution, confidence, trend)
- [x] Keyboard shortcuts (G=Gold, S=Silver, O=Oil, etc.)
- [x] Framer Motion page transitions

## Phase 2 — Conviction Pipeline (NEXT) ← promoted from Phase 3
Phase 2 is a single pipeline, not independent features. Each layer feeds the next.
Ship incrementally: validate each layer with user testing before building the next.

**Raj's conviction model:** Theme convergence + price confirmation + sentiment shift → trade.
**Priority shift rationale:** "The intelligence features ARE the product. Everything else is nice to have." — Raj (FB-011)

**Validation results (Raj, 2026-02-25):**
- VR-001: 8.0/10. Clusters validated. Time-to-conviction: 10-15 min → 2-3 min (5x). Divergence detection = standout.
- VR-002: Pressure test. Scanning faster, not trading yet. Trust/data quality = #1 friction. Explainers 5/10 overall, critical for divergences only.
- VR-003: 8.8/10. Data quality fix validated. 100% relevant articles. "The features were always good. They were just drowning in bad data." Headline summaries + explainers → 9.5+.

Build order:
1. [x] **[P1]** Commodity-specific news feeds (FB-005) — SHIPPED. All 8 commodities get unique articles.
2. [x] **[P1]** News theme clusters with price overlay — SHIPPED & VALIDATED (8.0/10). Divergence detection is the standout.
   - [x] **[P1]** Cluster quality fix (pass 1) — SHIPPED. Tightened keyword matching (phrase-only for non-Google RSS, weak keyword gating in clusterer).
   - [x] **[P0]** Deep data quality fix — SHIPPED & VALIDATED (VR-003: 8.0→8.8/10). Dropped Investing.com general feed. 100% relevant articles. Trust restored.
3. [ ] **[P1]** Cluster headline summaries — 1-line compressed narrative per cluster. Surface top article title as cluster "face." No LLM needed. Raj: "solves 80% of explainer problem at zero cost."
4. [x] **[P1]** LLM correlation explainers — SHIPPED (OpenRouter + Llama 3.3 70B free tier, batched 1 call/commodity). Production fixes SHIPPED (caching + description visibility). Rescoped to divergences + cross-theme synthesis.
   - [ ] **[P1]** Divergence prompt enhancement — "Invisible Buyer Checklist" (FB-023). Add commodity-specific invisible factors (central bank buying, ETF flows, dollar correlation, etc.) to divergence prompt. "Differential diagnosis" approach: list 2-3 plausible explanations, don't predict. Pure prompt engineering, zero infrastructure cost.
5. [ ] **[P1]** Daily Briefing / "Top 3 things to know" — the DECISION layer. Composed from clusters + headline summaries + explainers.
6. [ ] **[P2]** Deeper chart-news timeline correlation — when did cluster form vs when did price move? Enhancement to existing overlay.
7. [ ] **[P2]** Sentiment trend line — the CONTEXT layer. Shows sentiment direction over hours/days.
8. [ ] **[P2]** Historical precedent engine — the VALIDATION layer. Cherry on top. Needs embeddings infrastructure.

> **Parked ideas:**
> - Cross-commodity correlation signals — VALIDATED with live data (FB-024). Iran simultaneously driving Gold (safe haven, DIVERGENCE) and Oil (supply risk, THESIS). Raj: "Your biggest risk factor right now is the same event in both markets." Simple version: keyword overlap detection across commodity clusters. Task #45.
> - Time horizon tagging per cluster: short (24h TA), medium (weeks policy), long (months structural). Cheap keyword rules. (FB-019, Operator)
> - Cascading effect chains: "Venezuela reserves → US intervention → sanctions → supply." Multi-step LLM reasoning. Phase 4+. (FB-019, Operator)
> - Article sentiment dots in expanded divergence clusters (FB-025). Red/green dots showing the split within a divergence cluster. Raj: "The split is what makes a divergence interesting."

## Milestone — Design System Fixes (PRE-LAYOUT REDESIGN)
Consistency cleanup before the layout refactor. Clean up components, THEN rearrange them. (FB-020, Priya)

- [ ] **[P1]** Remove ghost colors, fix neutral border inconsistency, normalize card padding
- [ ] **[P1]** Reduce motion: kill floating section icons, kill sidebar glow-pulse, static sentiment borders on price cards
- [x] **[P1]** Divergence card visual elevation — SHIPPED. Hierarchy flip (conflict line first), gold warm tone, badge pulse, divergence sorts to top. Spec: `docs/divergence-card-spec.md`. Raj validated all 4 design questions.
- [ ] **[P2]** Remove emoji from section headers (color is sufficient differentiator)
- [ ] **[P3]** Skeleton loading states, ghost-card empty states

> **Design docs:** `docs/design-system.md` (authoritative system), `docs/brand-guide.md` (positioning + voice). 10% rule: no more than 10% of visible area should be active/glowing at any time.

## Milestone — News-First Layout Redesign (AFTER DESIGN SYSTEM FIXES)
Major layout pivot from operator. Design system must be clean before rearranging. **SPEC COMPLETE:** `docs/layout-redesign-spec.md` (approved by architect with 3 flags).

- [ ] **[P1]** Chart zoom prototype — de-risk biggest technical unknown (Recharts zoom animation). Do this BEFORE full layout build.
- [ ] **[P1]** News-first 60/40 layout — Intelligence panel (left, scrollable) + Context panel (right, sticky). Single price card, compact sentiment, related prices. (FB-012)
- [ ] **[P1]** Click-to-expand with chart zoom — Cluster click zooms chart to cluster time window. "WHY THIS MATTERS" section shows LLM explanation. (FB-013)
- [x] **[P1]** Divergence card hierarchy flip — SHIPPED (Task #43). Conflict line first, theme second. Divergence sorts to top. Per FB-021 + Raj validation.
- [ ] **[P2]** Ambient music + premium animations — subtle, don't affect load time (absorbed from Phase 3 atmosphere)
- [ ] **[P2]** Mobile: single column, chart/sentiment behind toggle buttons

> **Architecture note:** This is a full Dashboard.tsx + component hierarchy refactor. Current layout: prices → chart → clusters → sentiment → news (vertical scroll). New layout: clusters/intelligence as primary panel (left 60%) + prices/chart as context panel (right 40%). Click-to-expand composes with LLM explainers — explainer text appears inside the expanded cluster alongside a mini price chart.

## Phase 3 — Remaining Atmosphere (FUTURE) ← items not absorbed by layout redesign
- [ ] Animated grid background with floating particles
- [ ] Loading screen with pulse animation
- [ ] Price spike visual reactions (glow, particles, screen shake)
- [ ] Hover effects on price/news cards (3D lift, glow)
- [ ] Breaking news slide-in animation

> **Architecture note (audio state):** No global state management exists yet. Music/sound state must persist across commodity switches (Dashboard re-renders via AnimatePresence). Recommended approach: React Context for audio state or a singleton audio manager module. Audio assets should be lazy-loaded, not bundled.

## Phase 4 — Trading Tools (FUTURE)
- [ ] Real-time WebSocket price ticking
- [ ] Price alerts with browser notifications
- [ ] Portfolio P&L tracker
- [ ] Watchlist / pinned commodities
- [ ] AI-generated daily briefing

## Standalone — Landing Page (IN PROGRESS)
- [ ] Cyberpunk-themed landing page — user-approved, building now
- Headline: "Turn news noise into trading conviction in 5 minutes"
- Dashboard screenshots, feature highlights, waitlist signup
- Ships independently of Phase 3

## Phase 5 — Growth (FUTURE)
- [ ] ~~Landing page with waitlist~~ (moved to standalone, in progress)
- [ ] ~~Mobile responsive design~~ (moved to Phase 2 as P1)
- [ ] OLED pitch black mode
- [ ] Multi-user support
- [ ] Shareable dashboards

---

## Prioritization Criteria
1. **Core alignment** — Does it serve the Scan → Understand → Validate → Trade loop?
2. **User impact** — Would Raj use this in his morning trading routine?
3. **Technical feasibility** — Can we ship it in one build cycle?
4. **Dependency chain** — Does something else need to exist first?

## Feature Request Log
See [FEEDBACK.md](FEEDBACK.md) for all user feedback and feature requests.
