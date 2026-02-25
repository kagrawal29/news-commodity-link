# Commodity Pulse — User Feedback & Feature Requests

All feedback is collected here, evaluated against the core vision, and routed to the roadmap.

**Core Vision**: Turn commodity news noise into trading conviction in 5 minutes.

---

## Feedback Format

Each entry follows:
- **Source**: Who requested it
- **Date**: When
- **Category**: Bug / Feature / UX / Performance
- **Priority**: P0 (critical) / P1 (high) / P2 (medium) / P3 (nice-to-have)
- **Status**: New / Accepted / In Progress / Shipped / Deferred / Rejected
- **Phase**: Which roadmap phase it belongs to

---

## Active Feedback

### FB-001: News Theme Clusters with Price Overlay
- **Source**: Raj (user)
- **Date**: 2026-02-24
- **Category**: Feature
- **Priority**: P1
- **Status**: Accepted
- **Phase**: 3
- **Description**: Group news articles by theme (Fed policy, geopolitics, etc.), display as cluster cards with aggregate sentiment + price delta. Hover over cluster highlights corresponding time window on price chart.
- **Core alignment**: Direct — makes the news-price correlation interactive and visual.

### FB-002: LLM-Powered Correlation Explainers
- **Source**: Raj (user)
- **Date**: 2026-02-24
- **Category**: Feature
- **Priority**: P1
- **Status**: Accepted
- **Phase**: 3
- **Description**: AI-generated 1-2 sentence explanation of WHY news impacts the specific commodity. E.g., "Rate cut uncertainty strengthens GBP, reducing safe-haven demand for Gold."
- **Core alignment**: Direct — turns opaque sentiment scores into actionable trading logic.

### FB-003: Historical Precedent Engine
- **Source**: Raj (user)
- **Date**: 2026-02-24
- **Category**: Feature
- **Priority**: P2
- **Status**: Accepted
- **Phase**: 3
- **Description**: Click/hover on confidence score to see 2-3 semantically similar past events with actual price outcomes and mini sparklines.
- **Core alignment**: Strong — adds the "Validate" step to the core loop.

### FB-004: Landing Page
- **Source**: Raj (user) + Operator (explicitly requested)
- **Date**: 2026-02-24
- **Category**: Feature
- **Priority**: P2 (user-approved, shipping as standalone item)
- **Status**: In Progress
- **Phase**: Standalone (decoupled from Phase 5)
- **Description**: Cyberpunk-themed landing page with headline "Turn news noise into trading conviction in 5 minutes", dashboard screenshots, feature highlights, waitlist signup.
- **Core alignment**: Growth — needed for sharing with trader network. Operator requested "a complete cycle" (product + marketing page).
- **Architect note**: Landing page sells the vision, product delivers incrementally. Ship now with "Try the Live Beta" CTA → update as Phase 3 features land. Living document, not a one-time launch artifact.

### FB-005: Commodity-Specific News Filtering
- **Source**: Raj (user)
- **Date**: 2026-02-24
- **Category**: Bug/UX
- **Priority**: P1 (elevated from P2 — data quality issue; same news across commodities undermines trading decisions)
- **Status**: Accepted
- **Phase**: 3
- **Description**: Same news articles showing across different commodities. Each commodity should have unique, relevant news.
- **Core alignment**: Direct — data quality affects trading decisions. Must be fixed before Phase 3 intelligence features build on top of news data.
- **Production data (Raj, 2026-02-24)**: Crude Oil and Natural Gas get 20 commodity-specific articles (Oilprice.com RSS) — this is the gold standard. Silver, Copper, Platinum, Wheat, and Corn all share identical "Economy News" articles with no commodity-specific content. Fix: add commodity-specific RSS feeds (Kitco for metals, AgWeb for agriculture, etc.) following the Oilprice.com pattern.

### FB-006: News Source Variety
- **Source**: Raj (user)
- **Date**: 2026-02-24
- **Category**: UX
- **Priority**: P3
- **Status**: Accepted
- **Phase**: 3
- **Description**: All articles show "Economy News" as source. Show actual source names (Reuters, Bloomberg, etc.) for credibility.
- **Core alignment**: Moderate — source credibility matters for trading decisions.

### FB-007: Favicon
- **Source**: Raj (user)
- **Date**: 2026-02-24
- **Category**: UX
- **Priority**: P3
- **Status**: New
- **Phase**: 2
- **Description**: Add custom Commodity Pulse favicon to browser tab.
- **Core alignment**: Low — polish item.
- **Production note**: Confirmed 404 on favicon.ico in production (Raj, 2026-02-24).

### FB-008: Mobile Responsive Layout
- **Source**: Raj (production test, 2026-02-24)
- **Date**: 2026-02-24
- **Category**: Bug/UX
- **Priority**: P2 (desktop is the core trading workflow; mobile is secondary access)
- **Status**: Accepted
- **Phase**: 2 (pulled forward — address alongside atmosphere work)
- **Description**: Sidebar doesn't collapse on mobile (390x844). Takes ~60% screen width, price text truncated ("$5,1" instead of "$5,177"), chart too narrow, filter buttons partially cut off. Needs hamburger menu / collapsible sidebar. Root cause: Sidebar.tsx uses fixed `w-64 shrink-0`.
- **Core alignment**: Moderate — desktop-first workflow, but broken mobile hurts demos and sharing.
- **Architect note**: Scoped fix — responsive breakpoints + hamburger toggle on Sidebar.tsx only. Do NOT refactor the full layout system. Keep it surgical.

### FB-009: Daily Briefing / "Top 3 Things to Know"
- **Source**: Product-owner (concept) + Raj (workflow validation, 2026-02-25)
- **Date**: 2026-02-25
- **Category**: Feature
- **Priority**: P1
- **Status**: Accepted
- **Phase**: 2 (step 4 in conviction pipeline — composed from clusters + explainers)
- **Description**: Per-commodity summary synthesized from news clusters and LLM explainers. Format: "Gold today: Fed rates (5 articles, bullish), Dollar weakness (3 articles, bullish), Profit-taking (2 articles, bearish). Net: Bullish, 0.75 confidence." This is the decision support layer — answers "what should I DO?"
- **Core alignment**: Direct — this IS the core promise. Turns noise into conviction. Closes the gap between "I see data" and "I have a bias for the day."
- **Architect note**: Not a standalone feature — it's the composition of clusters + explainers. Cannot exist without layers 2 and 3. Build order: clusters → explainers → briefing.

### FB-010: Sentiment Trend Line
- **Source**: Raj (workflow analysis, 2026-02-25 — "compared to what" gap)
- **Date**: 2026-02-25
- **Category**: Feature
- **Priority**: P2
- **Status**: Accepted
- **Phase**: 2 (step 5 in conviction pipeline)
- **Description**: Show sentiment direction over hours/days for each commodity. Answers: "Is -0.08 unusual? Worse than yesterday? Trending down or recovering?" Raj's conviction model includes sentiment SHIFT as a trade trigger — a snapshot score without trend context is incomplete.
- **Core alignment**: Direct — sentiment shift is one of three components in Raj's conviction model (theme convergence + price confirmation + sentiment shift → trade).
- **Architect note**: Simpler than precedent engine — uses existing sentiment data, just needs time-series storage and a sparkline visualization. High value, low complexity.

### FB-011: Priority Realignment — Intelligence Before Atmosphere
- **Source**: Raj (workflow feedback, 2026-02-25) + team lead (strategic decision)
- **Date**: 2026-02-25
- **Category**: Strategic
- **Priority**: P0 (process change)
- **Status**: Accepted
- **Phase**: N/A (cross-phase decision)
- **Description**: Raj's feedback confirms intelligence features (conviction pipeline) are the product. Atmosphere features (particles, music, animations) are polish. The conviction pipeline leapfrogs atmosphere in priority. Old Phase 2 (atmosphere) → new Phase 3. Old Phase 3 (intelligence) → new Phase 2.
- **Core alignment**: Direct — this realignment ensures the team builds what closes the "15 min → 5 min" gap before investing in visual polish.
- **Architect note**: FB-009 was already assigned to Daily Briefing feature, so this is FB-011. Team lead originally requested FB-009 for this entry.

### FB-012: News-First Layout Redesign
- **Source**: Operator (via Raj, 2026-02-25)
- **Date**: 2026-02-25
- **Category**: UX / Strategic
- **Priority**: P1
- **Status**: Accepted
- **Phase**: 2 (after cluster validation, before LLM explainers)
- **Description**: Major layout pivot. Three components:
  1. **News-first layout** — Clusters/intelligence as primary content (60% left panel), prices secondary. "Live prices I can see everywhere" — the differentiator is the WHY, not the WHAT.
  2. **Click-to-expand clusters** — Clicking a cluster shows inline price chart + text inference ("Gold rallied 1.2% as Fed rate cut expectations drove ETF inflows"). No external redirects. Everything in one view.
  3. **Ambient music/animation** — Premium feel, subtle, don't affect load time.
- **Core alignment**: Direct — reorients the entire UI around the intelligence layer, which is the product's differentiator and monetization gate.
- **Architect note**: This is a significant layout refactor (Dashboard.tsx, Sidebar.tsx, component hierarchy). Do NOT attempt alongside cluster validation. Sequence: deploy clusters on current layout → validate with Raj → THEN redesign layout. The redesign should absorb some Phase 3 atmosphere items (ambient music/animation) rather than treating them separately.
- **Dependency**: Requires cluster validation to pass first. Layout redesign builds on validated cluster UX.

### FB-013: Click-to-Expand Inline Inference
- **Source**: Operator (via Raj, 2026-02-25)
- **Date**: 2026-02-25
- **Category**: Feature
- **Priority**: P1
- **Status**: Accepted
- **Phase**: 2 (ships with layout redesign)
- **Description**: Clicking a cluster expands inline to show: mini price chart for the cluster's time window + text inference explaining the price movement ("Gold rallied 1.2% as Fed rate cut expectations drove ETF inflows"). No external article redirects — everything stays in one view.
- **Core alignment**: Direct — this IS the "Understand" step. Combines cluster (theme) + explainer (causal chain) + price overlay into a single interaction.
- **Architect note**: This partially overlaps with LLM explainers (FB-002/task #30). The inline text inference requires either LLM-generated text or well-crafted template sentences. Evaluate whether this replaces the standalone LLM explainer feature or composes with it.

### FB-014: Cluster Headline Summaries
- **Source**: Raj (UX pressure test, 2026-02-25)
- **Date**: 2026-02-25
- **Category**: Feature
- **Priority**: P1 (validated by Raj as "solves 80% of explainer problem at zero cost")
- **Status**: Accepted
- **Phase**: 2 (step 3 in conviction pipeline, before LLM explainers)
- **Description**: 1-line compressed narrative per cluster. Surface the top article's title as a "lead headline" — e.g., "Russia rerouting oil via supertankers to China; tanker rates hit 6-year high." Gives the trader the story in 15 seconds without expanding the cluster. Desired stack per cluster card: (1) headline summary, (2) keyword counts (transparency), (3) sentiment + price + divergence (signal). Story → Evidence → Signal.
- **Core alignment**: Direct — closes the "what's the story?" gap without LLM cost. Experienced traders don't need causal explanation for obvious themes; they need the narrative surfaced quickly.
- **Architect note**: No LLM needed for MVP — use top article title (already sorted by abs(sentiment_score)). Future enhancement: Haiku-compressed multi-headline narrative. This feature reduces the urgency of generic LLM explainers, allowing explainers to be rescoped to divergences and cross-theme synthesis only.

### FB-015: Deep Data Quality Fix — Drop Investing.com Feed
- **Source**: Raj (UX pressure test, 2026-02-25)
- **Date**: 2026-02-25
- **Category**: Bug / Data Quality
- **Priority**: P0 (trust prerequisite — "I need to trust the features I have")
- **Status**: Shipped (VR-003: 8.8/10, 100% relevant articles, trust restored)
- **Phase**: 2 (prerequisite for all intelligence features)
- **Description**: ~40% of articles are irrelevant noise. Root cause: `Investing.com/rss/news_14.rss` general Commodities feed shared across all 8 commodities. Leaks vaccine lawsuits, Spirit Airlines, Home Depot earnings into Gold/Oil feeds. Fix: drop the feed entirely. Specialized feeds (Mining.com, Oilprice.com, Google News RSS, Yahoo Finance) already provide commodity-specific content.
- **Core alignment**: Critical — noisy data undermines trust in clusters, sentiment scores, divergence detection, and every future intelligence feature.
- **Raj's quote**: "The friction isn't 'I need more features.' It's 'I need to trust the features I have.' Clean up the article relevance, and the existing clusters + divergence detection become much more powerful."
- **Validation**: VR-003 — 8.0 → 8.8. "The existing features were always good. They were just drowning in bad data."

### FB-016: HTML Artifacts in Google News Article Descriptions
- **Source**: Raj (VR-003 re-test, 2026-02-25)
- **Date**: 2026-02-25
- **Category**: Bug / Cosmetic
- **Priority**: P3 (unpolished but doesn't affect trading decisions)
- **Status**: New
- **Phase**: 2
- **Description**: Raw HTML tags (`<a href>`, `<font>`) appearing in article description text from Google News RSS entries. Fix: strip HTML tags in `data/news_fetcher.py` during RSS parsing.
- **Core alignment**: Low — cosmetic polish. Does not affect trading decisions.

### FB-017: Technical Analysis Content — Consensus Bar (not full cluster)
- **Source**: Raj (VR-003 re-test + follow-up, 2026-02-25)
- **Date**: 2026-02-25
- **Category**: Enhancement
- **Priority**: P2
- **Status**: Accepted (refined by Raj)
- **Phase**: 2
- **Description**: 45-55% of articles match existing themes. Unmatched articles are primarily TA content from FXStreet, FXEmpire. **Raj's refinement**: TA is opinion, not events. Should NOT be a full cluster card with equal visual weight. Instead: a lightweight "consensus bar" at the bottom of the themes section. Format: "Technical consensus: 3 of 4 analysts see bullish continuation." Visible but clearly secondary to event-driven clusters.
- **Core alignment**: Moderate — TA content is useful as a consensus check but not the same quality of signal as event-driven themes. The consensus bar respects this distinction.
- **Architect note**: Implementation: match TA articles using keywords ("technical analysis", "chart pattern", "support", "resistance", "RSI", "MACD", "fibonacci", "breakout"), classify their sentiment, present as a single summary line (not a cluster card). This also connects to FB-019 (macro vs micro separation) — TA is the "micro" layer. Keywords: "technical analysis", "chart pattern", "support", "resistance", "moving average", "RSI", "MACD", "fibonacci", "breakout", "rally", "pullback", "outlook", "forecast".

### FB-018: Article Freshness on 1D Timeframe
- **Source**: Raj (VR-003 re-test, 2026-02-25)
- **Date**: 2026-02-25
- **Category**: UX / Data Freshness
- **Priority**: P2
- **Status**: New
- **Phase**: 2
- **Description**: Raj needs fresh articles for morning trading routine. Some articles may be stale on 1-day timeframe view. Current news cache TTL is 1800s (30 min). Consider shorter cache for 1D, or add "last updated X min ago" timestamp to give user awareness of data freshness.
- **Core alignment**: Direct — stale data undermines the "5-minute morning conviction" use case.

---

## Validation Results

### VR-001: Cluster Validation by Raj (2026-02-25)
- **Score**: 8.0/10
- **Key metric**: Time-to-conviction improved from 10-15 min → 2-3 min (5x improvement)
- **Standout feature**: Divergence detection — "Bullish sentiment, price declining" labels were the most valuable single element.
- **Verdict**: Conviction pipeline is validated. Clusters work. Iterate to 9.0+.

**Three items for 9.0+:**

1. **Article filtering quality (quick fix)**
   - False keyword matches: S&P 500 articles appearing in Oil clusters
   - Generic/irrelevant articles still getting clustered
   - Fix: tighten keyword matching in `config/themes.py` and/or add negative keyword filters
   - Priority: P1 — data quality directly undermines trust

2. **LLM "so what" explainers (conviction gap)**
   - Raj can see the narrative (cluster themes) but still has to figure out what it MEANS himself
   - This is the "so what" gap from his original workflow analysis — now confirmed with real cluster usage
   - Validates that step 3 of the conviction pipeline (LLM explainers) is necessary, not optional
   - Priority: P1 — this is the remaining gap between "I see the story" and "I understand the implication"

3. **Deeper chart-news timeline correlation**
   - When did the cluster form (first article) vs when did price actually move?
   - Currently: hover shows ReferenceArea over cluster time window. Missing: temporal causality — did news lead or lag price?
   - Priority: P2 — enhancement to existing overlay, not a new feature

### VR-002: Post-Cluster UX Pressure Test by Raj (2026-02-25)
- **Context**: Detailed follow-up after extended cluster usage
- **Key metrics**:
  - Total workflow time: ~20 min → ~8 min (scanning + external validation)
  - Scanning only: 10-15 min → 2-3 min (5x improvement confirmed)
  - Validation step still external (TradingView, dollar index, related markets): 5-7 min unchanged
- **LLM explainer impact**: 5/10 overall. Critical for divergences and cross-theme conflicts. Unnecessary for straightforward themes.
- **#1 friction: TRUST / data quality.** ~40% of articles are irrelevant noise (vaccine lawsuits, Spirit Airlines in Gold feed). Root cause: `Investing.com/rss/news_14.rss` general Commodities feed shared across all 8 commodities.
- **Raj's quote**: "The friction isn't 'I need more features.' It's 'I need to trust the features I have.'"
- **Verdict**: Product is at "shows me the right narrative" — not yet at "gives me conviction." Gap: (a) trust in data quality, (b) cross-theme interpretation, (c) validate step still external.
- **Raj's priority order**: Data quality first → Explainers (divergence-focused) → Layout
- **Action**: Recommended priority shift to product-owner — fix Investing.com feed noise before continuing LLM explainers.

**Specific workflow observation (Gold):**
- 15 seconds to scan 4 theme cards and identify dominant narrative
- 20 seconds on DIVERGENCE flag — immediately synthesized "safe-haven demand not enough to offset supply pressure"
- Expanded Geopolitical Supply Risk cluster to identify WHICH geopolitical risk (Russia tankers vs Iran tensions — different implications)
- Used chart independently for momentum confirmation
- Result: had a thesis (Gold bearish, supply-driven) but would NOT trade without checking dollar and Gold/Silver ratio

### VR-003: Post-Data-Quality-Fix Validation by Raj (2026-02-25)
- **Score**: 8.8/10 (up from 8.0)
- **Key result**: 100% relevant articles. Trust restored. Noise dropped from ~40% to ~0%.
- **Raj's quote**: "The existing features were always good. They were just drowning in bad data."
- **Verdict**: Data quality fix validated. The Investing.com feed drop was the right call. Foundation is solid. Headline summaries + divergence explainers get him to 9.5+.

**Three minor issues identified:**

1. **HTML artifacts in Google News descriptions**
   - Raw HTML tags (`<a href>`, `<font>`) appearing in article description text from Google News RSS
   - Category: Cosmetic / Bug
   - Priority: P3 — unpolished but doesn't affect trading decisions
   - Fix: Strip HTML tags from article descriptions in `data/news_fetcher.py` (e.g., regex or `html.parser`)

2. **45-55% theme match rate — unmatched technical analysis articles**
   - Articles from FXStreet, FXEmpire (technical analysis / chart patterns) don't match any current theme keywords
   - Raj suggests adding a "Market Analysis" or "Technical Outlook" cluster theme
   - Category: Enhancement
   - Priority: P2 — would increase match rate to ~70-80% and surface TA content that traders value
   - Fix: Add new theme to `config/themes.py` with keywords: "technical analysis", "chart pattern", "support", "resistance", "moving average", "RSI", "MACD", "fibonacci", "breakout", "rally", "pullback"

3. **Article age on 1D timeframe**
   - Raj needs fresh articles for his morning trading routine
   - Some articles may be stale when viewing the 1-day timeframe
   - Category: UX / Data freshness
   - Priority: P2 — directly affects the "5-minute morning conviction" use case
   - Fix: Investigate cache TTL for news (currently 1800s / 30 min). Consider shorter TTL for 1D timeframe, or add "last updated" timestamp to the UI

### FB-019: Time Horizon Tagging & Cascading Effects
- **Source**: Operator (via Raj, 2026-02-25)
- **Date**: 2026-02-25
- **Category**: Feature / Strategic Vision
- **Priority**: P3 (future — requires LLM infrastructure maturity)
- **Status**: Parked
- **Phase**: Future (Phase 4+)
- **Description**: Not all news has the same time horizon of impact. Three dimensions:
  1. **Time horizon tagging per cluster** — "next 24 hours" catalyst vs "next 6 months" structural shift. Changes how trader weights it.
  2. **Macro vs micro separation** — Geopolitical/policy/structural (macro) should be visually distinct from daily price action/TA (micro). Different decision frameworks.
  3. **Cascading effect chains** — "Venezuela reserves → US intervention risk → sanctions timeline → supply impact" as a visual chain. Markets price in cascades immediately; showing the chain helps traders anticipate subsequent moves.
- **Core alignment**: Strong — this is the evolution from "commodity intelligence terminal" to "commodity intelligence platform." Directly serves the Understand → Validate loop.
- **Architect note**: The cascading effects concept is where LLM explainers could evolve beyond 1-2 sentence summaries into multi-step causal reasoning. However, this requires: (a) clean data (now achieved), (b) working explainers (shipping now), (c) temporal metadata on articles, (d) cross-cluster LLM reasoning. Build the foundation first. Time horizon tagging could be a simpler interim step — add a `time_horizon: "short" | "medium" | "long"` field to clusters, classifiable by simple keyword rules (TA terms = short, policy terms = medium, geopolitical/structural = long).
- **Connection to FB-017**: The "Technical Analysis" theme request is the micro side of this macro/micro split. TA = short-term, event-driven themes = medium/long-term. These could eventually be visually separated.

### FB-020: Design System Fixes (Pre-Layout Redesign)
- **Source**: Priya (designer audit, 2026-02-25)
- **Date**: 2026-02-25
- **Category**: UX / Design
- **Priority**: P1 (consistency fixes that improve trust before layout redesign)
- **Status**: Accepted
- **Phase**: 2 (pre-layout redesign)
- **Description**: Full design audit findings. Key fixes:
  1. Remove ghost colors (cyber-blue, cyber-purple, cyber-amber) — no semantic role
  2. Fix neutral article border inconsistency (magenta in NewsFeed vs gray in ClusterCards)
  3. Normalize card padding to one value (p-5 standard, p-3 compact)
  4. Reduce motion: remove animate-float from section icons, remove animate-glow-pulse from sidebar/sentiment, replace animate-border-glow with static sentiment borders
  5. Remove emoji from section headers (color is sufficient)
  6. Add skeleton loading states
- **Core alignment**: Moderate — visual consistency builds trust. Motion reduction ensures divergence (the signature moment) stands out.
- **Architect note**: These fixes are independent of the layout redesign and should ship first. They clean up the component library so the layout redesign can focus on arrangement, not consistency bugs. References: docs/design-system.md, docs/brand-guide.md.

### FB-021: Divergence Card Visual Elevation
- **Source**: Raj (detailed UX walkthrough, 2026-02-25) + Priya (design audit)
- **Date**: 2026-02-25
- **Category**: UX / Design
- **Priority**: P1 (the product's signature moment)
- **Status**: Accepted — Priya to spec mockup
- **Phase**: 2 (ships with design system fixes)
- **Description**: Divergence is undersold. Raj's detailed preferences:
  1. **Card expansion** — divergence cluster cards should be visually larger/taller than non-divergence cards. First thing the trader looks at every morning.
  2. **Badge pulse** — divergence badge (gold) should glow/pulse subtly. "Notification you can't miss, not Christmas lights."
  3. **Hierarchy flip** — lead with the conflict line ("News: BEARISH / Price: RISING") as the FIRST and LARGEST text. Current order (theme → data → divergence → keywords) should become: divergence line → theme → data → keywords.
  4. **Inline, not modal.** Part of the natural scan flow. No popups, no sound effects.
- **Core alignment**: Direct — divergence is where traders make money. It's the gap between narrative and reality. Raj: "The divergence card should be the thing a trader screenshots and sends to their group chat."
- **Architect note**: The divergence card hierarchy flip has implications for the explainer display. When a divergence cluster has an LLM explanation, the reading flow should be: conflict line (what's weird) → explainer text (why it's weird) → theme name → evidence. The explainer earns its highest value on divergence cards specifically.

### FB-022: Divergence Explainer Prompt — Raj's Mental Model
- **Source**: Raj (4-step divergence walkthrough, 2026-02-25)
- **Date**: 2026-02-25
- **Category**: Feature / Spec
- **Priority**: P1 (directly informs LLM explainer prompt design)
- **Status**: Accepted — spec for explainer prompt refinement
- **Phase**: 2 (refine after Task #41 ships)
- **Description**: Raj's 4-step divergence analysis process:
  1. (Instant) "News is bearish but price went up. Something else is stronger."
  2. (5-10s) Check OTHER clusters — are multiple themes diverging? "TWO themes bearish but price climbing = buying pressure from somewhere news isn't capturing."
  3. (30-60s) Check price chart — is this a pullback in an uptrend? "Bearish news during a rally = news lagging momentum, not price being wrong."
  4. (External) Check dollar, real yields, gold/silver ratio — the "validate" step.
  **Achievable now (simpler version):** "Bearish sentiment in a rising price environment often indicates news lagging momentum. Price trend (+3.79% over 30d) appears to be the stronger signal."
  **Ideal version (Phase 4+):** Include cross-asset context (DXY, real yields) and historical pattern matching ("when 3+ bearish articles appear during strong uptrend, price continues higher 68% of the time").
- **Core alignment**: Direct — this IS the "so what" gap. The simpler version replaces Steps 2-3 of Raj's process. The ideal version replaces all 4 steps.
- **Architect note**: The simpler version is achievable with current data: the batched prompt already has all clusters (cross-cluster reasoning), and price_delta_pct provides trend context. Prompt refinement needed: (1) instruct the LLM to cross-reference all clusters when divergence is detected, (2) instruct it to interpret whether news is leading or lagging the price trend, (3) do NOT resolve the divergence or pick a side — explain the tension.

### FB-023: Invisible Buyer Checklist — Commodity-Specific Divergence Factors
- **Source**: Raj (divergence mental model, 2026-02-25)
- **Date**: 2026-02-25
- **Category**: Feature / Spec
- **Priority**: P1 (directly enhances divergence explainer prompt quality — zero infrastructure cost)
- **Status**: Accepted — spec for `nlp/explainer.py` prompt enhancement
- **Phase**: 2 (ships with divergence explainer refinement, after Task #41)
- **Description**: Raj's codifiable mental model for what causes price to move when news can't explain it. A "differential diagnosis" approach to divergence.
  **Gold — "Invisible Buyer" Checklist** (when bearish news + rising price):
  1. Central bank buying (unreported, often shows up in price before news)
  2. ETF inflow acceleration (GLD, IAU — data lags by hours/days)
  3. Dollar weakness (inverse correlation — dollar falls, gold rises)
  4. Real yield decline (TIPS yields down = gold up, institutional flow)
  5. Momentum/technical breakout (price above key levels, TA-driven buying)
  6. Geopolitical hedging (institutional risk-off into gold, not always public)
  **Oil — "Supply/Demand Invisible" Checklist** (when bearish news + rising price):
  1. Inventory draws exceeding expectations (EIA/API data lags)
  2. Refinery demand surge (seasonal or crack spread driven)
  3. Sanctions enforcement tightening (reduces available supply quietly)
  4. Speculative positioning unwind (short covering, COT report lags)
  5. Contango → backwardation shift (front-month premium = physical demand)
  **Agriculture — Wheat/Corn/Soybeans Checklist** (Raj, 2026-02-25):
  *Tier 1 — Top movers (cover ~70% of ag divergences):*
  1. Weather model revisions — 6-10 day and 8-14 day forecasts flipping. GFS vs Euro model agreement/divergence. Drought forecast in Corn Belt = 20 cents overnight.
  2. USDA report surprises — WASDE monthly, weekly export sales, crop progress, planted acreage (March), quarterly grain stocks. 2% miss on ending stocks = 5-8% wheat move.
  3. Black Sea/Ukraine logistics — corridor closures, port disruptions, Russian export bans. "The ag equivalent of Iran for oil."
  *Tier 2 — Confirming factors:*
  4. Fund positioning (COT managed money) — max long + favorable weather turn = violent unwind.
  5. Export commitment pace — ahead or behind USDA annual projection = demand validation.
  6. Basis shifts — Gulf elevator cash basis tells real demand. Wide basis = strong demand regardless of futures.
  *Tier 3 — Background:*
  7. Currency moves — strong dollar = expensive US grain globally. Brazilian real especially (price competitor).
  8. Energy/input costs — ethanol mandate = ~40% of US corn demand. Oil crash → ethanol margin collapse → corn demand drop. (Cross-commodity link for ag.)
  **Key insight**: "Don't make it predict WHICH factor is causing the divergence. Instead, have it list the TOP 2-3 most likely explanations given the cluster data and price context. That's not a prediction. It's a differential diagnosis."
  **Critical constraints (Raj, 2026-02-25):**
  - **Cap at 2, max 3 possibilities.** "Two is a decision. Three is a choice. Four is confusion."
  - **Phrase as hypotheses, not facts.** GOOD: "Possible: central bank buying below news threshold." BAD: "Central banks are buying gold." BAD: "The explanation is dollar weakness."
  - **The word "Possible" is doing heavy lifting.** It says "here's what to investigate" not "here's the answer." Preserves trust.
  - **Target: 6 seconds from conflict to conviction.** Conflict line (1s) → Invisible Buyer diagnosis (3s) → Theme context (2s).
  **Implementation**: Add commodity-specific `invisible_factors` to the divergence prompt in `nlp/explainer.py`. When a cluster has `divergence=True`, append the relevant checklist to the LLM prompt so it can reason about which invisible factors might explain the gap. The output should list 2-3 plausible explanations, NOT pick a winner. Instruct the LLM: "Begin each explanation with 'Possible:' — frame as hypotheses to investigate, not conclusions."
- **Core alignment**: Direct — this closes the gap between "what's weird" (divergence detection) and "why it might be happening" (differential diagnosis). This IS the "so what" layer Raj has been asking for. Raj: "The three-layer stack (conflict → invisible buyer diagnosis → theme context) is the feature that gets this product from 8.8 to 9.5."
- **Architect note**: This is a pure prompt engineering enhancement — no infrastructure change, no new API calls, no new data sources. The `invisible_factors` are static per commodity sector (precious metals, energy, agriculture). The LLM already has cluster + price context in the batched prompt. We're just giving it a better reasoning framework. Connects to FB-022 (Raj's 4-step mental model) — this provides the domain knowledge for steps 2-3.
- **Connection to design principles**: The "differential diagnosis" framing is perfect for our trust model. We list possibilities, not predictions. "Possible: central bank buying below news threshold" is evidence-presenting, not recommending. Fully compliant with design-principles.md.

### FB-024: Cross-Commodity Signal Detection — Live Evidence (Iran)
- **Source**: Raj (live UAT observation, 2026-02-25)
- **Date**: 2026-02-25
- **Category**: Feature / Validation Evidence
- **Priority**: P2 (validates a parked idea with real production data)
- **Status**: Accepted — evidence logged, implementation in Task #45
- **Phase**: Future (after conviction pipeline is complete)
- **Description**: Live production observation: Iran is the dominant narrative driving Gold AND Oil simultaneously, but in different directions.
  - **Gold** → Geopolitical Tensions cluster: 2 articles mention Iran. DIVERGENCE (bearish news, price rising → safe haven demand).
  - **Oil** → Geopolitical Supply Risk cluster: 5 of 6 articles mention Iran. THESIS confidence (supply disruption risk → 7-month high).
  Same event, two commodities, different mechanisms. Currently, a trader must switch between commodities manually to discover this. The ideal dashboard surfaces it proactively: "Iran mentioned in 7 articles across Gold and Oil today. Your biggest risk factor is the same event in both markets."
  **Raj's framing**: This is a STRUCTURAL event (weeks/months), not a trading event (hours). Connects to FB-019 (time horizon tagging).
- **Core alignment**: Strong — addresses the "Validate" step of the core loop. Cross-commodity confirmation strengthens conviction.
- **Architect note**: Implementation approach: post-clustering aggregation. After clustering all 8 commodities, scan for shared dominant keywords/themes across commodity clusters. If a keyword (e.g., "Iran") appears as a top keyword in 2+ commodity clusters, surface as a cross-commodity alert. Simple version: "Iran: active in Gold (DIVERGENCE), Oil (THESIS)." No new data sources needed — just cluster keyword overlap analysis. Task #45 exists for this.
- **Connection**: Validates the parked "cross-commodity correlation signals" idea in ROADMAP.md with concrete production data.

### FB-025: Article Sentiment Dots in Expanded Divergence Clusters
- **Source**: Raj (divergence card validation, 2026-02-25)
- **Date**: 2026-02-25
- **Category**: UX Enhancement
- **Priority**: P2 (enhances divergence investigation step)
- **Status**: Accepted
- **Phase**: 2 (ships with or after divergence card elevation)
- **Description**: In expanded divergence clusters, show colored dots (red/green) next to individual articles to visualize the sentiment SPLIT within the cluster. In a 6-article cluster where 4 are bearish and 2 are bullish, the trader sees the 4:2 ratio visually. "The split is what makes a divergence interesting — which specific headlines are fighting the price?"
- **Core alignment**: Direct — helps the trader's investigation step. The split within a divergence cluster tells you HOW conflicted the narrative is.
- **Architect note**: Straightforward — each article already has `sentiment_score`. Render a small dot (green if score > 0.05, red if < -0.05, gray if neutral) before the article title in the expanded article list. No backend change needed.
