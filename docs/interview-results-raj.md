# Commodity Pulse — User Interview Results: Raj

**Subject**: Raj (27, commodity trader, Mumbai)
**Interviewer**: Architect agent
**Date**: 2026-02-25
**Method**: Structured interview across 2 sessions, covering all 26 questions from interview-guide-raj.md

---

## 1. Raj's Mental Model Map

```
NEWS EVENT
    ↓
FILTER: Is this surprising? Supply disruption? Policy shift?
    ↓ (if yes)              ↓ (if no)
CATEGORIZE               IGNORE (50% of all news)
    ↓
THEME: Do 2-3+ articles form a narrative?
    ↓ (if yes)              ↓ (if no)
BUILD THESIS              MENTAL NOTE, no action
    ↓
VALIDATE: Does price confirm? Do related markets align?
    ↓ (if yes)              ↓ (if conflict)
CONVICTION               WAIT — "compression before explosion"
    ↓
TRADE
```

**Key insight**: Conviction is never from a single article. It requires theme convergence (3+ articles) + price confirmation + sentiment shift. The product must mirror this layered decision process.

---

## 2. Information Hierarchy

What Raj looks at, in order:

| Priority | Information | Purpose | Current product support |
|----------|-----------|---------|------------------------|
| 1st | Price movers | "What happened overnight?" — picks which commodity to focus on | Good (price cards with change %) |
| 2nd | News headlines | "Why did it move?" — scans for surprise/disruption/policy | Good (news feed with timestamps) |
| 3rd | Theme convergence | "Are multiple sources saying the same thing?" | **GAP — no clustering** |
| 4th | Causal chain | "Why does this news impact this commodity specifically?" | **GAP — no explainers** |
| 5th | Price confirmation | "Is the market actually responding to this narrative?" | Partial (chart exists but not linked to news) |
| 6th | Related markets | "Is the thesis consistent across correlated assets?" | **GAP — no cross-commodity view** |
| 7th | Sentiment direction | "Is sentiment getting more bullish/bearish over time?" | **GAP — snapshot only, no trend** |
| 8th | Historical precedent | "What happened last time we saw this pattern?" | **GAP — no precedent engine** |

---

## 3. Feature Requirements Matrix

### 3a. News Clusters (Raj's #1 pick)

| Requirement | Source | Design implication |
|------------|--------|-------------------|
| Group by THEME, not by source or time | Q11, Q13 | Keyword-based topic clustering, not chronological |
| Show 3-4 themes max per commodity | Q12 ("3 themes ranked by intensity") | Cap cluster count, rank by article volume + sentiment magnitude |
| Aggregate sentiment per cluster | Q5, conviction model | Each cluster card shows net bullish/bearish + article count |
| Price delta per cluster | Q7 (Russia example) | Overlay price movement during cluster's time window on chart |
| Visual format: theme cards (option B) | Q16 | NOT individual arrows (A) or timeline dots (C). Grouped cards. |
| Show divergence, don't resolve it | Q9 | "News: BULLISH / Price: DECLINING — divergence" label. Never pick a side. |
| Named themes from domain vocabulary | Q7 | Use commodity-specific theme names: "OPEC Supply", "Fed Rates", "Safe Haven Flows" — not generic "Cluster 1" |

**Real-world validation (Raj's Russia Oil trade):**
The cluster should have displayed: "Russia Supply Disruption (3 articles, BEARISH supply, BULLISH price)" with a +1.2% price delta overlay. This would have reduced his decision time from 12 minutes to 2 minutes.

### 3b. LLM Explainers

| Requirement | Source | Design implication |
|------------|--------|-------------------|
| One sentence causal chain per article | Q5 (Fed example), "so what" gap | "Fed rate pause → dollar weakens → gold up (cheaper in dollar terms + lower opportunity cost)" |
| Commodity-SPECIFIC reasoning | Q5, Q10 | Same headline → different explanation per commodity. "Fed pause → Gold UP because..." vs "Fed pause → Copper DOWN because..." |
| Show the WHY, not a prediction | Q4 (trust model) | "This matters because..." NOT "This will cause..." |
| Transparency in methodology | Q4 (trust) | "Labeled 'Fed Hawkish' because 3 articles mention rate hikes, 2 mention inflation persistence" |

### 3c. Daily Briefing

| Requirement | Source | Design implication |
|------------|--------|-------------------|
| "Top 3 things to know about [commodity] right now" | Q12, Q25 | Composed from clusters + explainers |
| Ranked by intensity (article count + sentiment magnitude) | Q12 | Most impactful theme first |
| Net direction with confidence | Conviction model | "Net: Bullish, 0.75 confidence" — but NEVER "BUY" or "SELL" |
| Scannable in 30 seconds | Q12 | This is the 5-minute promise in one panel |

### 3d. Sentiment Trend Line

| Requirement | Source | Design implication |
|------------|--------|-------------------|
| Show direction over hours/days | "compared to what" gap | Sparkline or mini chart alongside current score |
| Answer "is this unusual?" | Same | Highlight when current sentiment deviates from recent baseline |

### 3e. Precedent Engine (lowest priority)

| Requirement | Source | Design implication |
|------------|--------|-------------------|
| Base rates, not predictions | Q4 (trust) | "Similar clusters preceded 1-3% pullbacks in 6/10 instances" |
| Historical context for magnitude | "how much" gap | Helps assess if a move is a 1% or 5% event |

---

## 4. Design Implications

### 4a. Critical UI/UX decisions (for dev)

1. **Cluster visualization: Option B confirmed.** Theme cards with article count, aggregate sentiment, and price delta. NOT individual article arrows (too noisy) or timeline dots (secondary).

2. **Never show BUY/SELL signals.** Dealbreaker for Raj. The tool is the analyst, the trader makes the decision. Cross the line from information to recommendation → user churn.

3. **Never make specific price predictions.** "Gold will drop 2%" destroys trust. "Similar patterns preceded 1-3% moves" builds trust. Base rates, not forecasts.

4. **Show divergence explicitly.** When news sentiment and price direction conflict, label it: "News: BULLISH / Price: DECLINING — divergence." Don't hide it, don't resolve it. Traders respect tools that show reality.

5. **Cluster names must use domain vocabulary.** "OPEC Supply Pressure", "Fed Rate Expectations", "Safe Haven Demand" — NOT "Cluster 1", "Topic A", "Group 3". The names are the narrative.

6. **Transparency = trust.** Show why a cluster is labeled what it is: "3 articles mention sanctions, 2 mention shipping disruptions → labeled 'Russia Supply Disruption'."

### 4b. Trust model

| Trust builder | Trust destroyer |
|--------------|----------------|
| Showing its work (methodology transparency) | Specific price predictions |
| Base rates from historical data | BUY/SELL recommendations |
| Letting the trader decide | Pretending to have answers the market doesn't |
| Accurate theme labeling | Generic or wrong theme names |
| Consistent, reliable data quality | Stale news or duplicated articles across commodities |

### 4c. Monetization signal

Raj would pay **$50-100/month** IF the intelligence layer delivers conviction in 5 minutes. Without it: $0 — free alternatives exist. The conviction pipeline is the entire value proposition and monetization gate.

---

## 5. Priority Refinement

### Confirmed priorities (no changes needed):

| Feature | Priority | Rationale |
|---------|----------|-----------|
| FB-005: Commodity-specific feeds | P1, prerequisite | Without unique news per commodity, clusters show identical themes — "embarrassing" (Raj) |
| News Clusters | P1, build first | Raj's #1 pick. "Tell me the narrative" is the one thing he wants done perfectly. Reduces 12 min → 2 min in his Russia Oil example. |
| LLM Explainers | P1, after clusters | Fills the "so what" gap. Content within the cluster container. |
| Daily Briefing | P1, after explainers | The decision layer. Composed from clusters + explainers. The "5-minute promise" in one panel. |
| Sentiment Trend | P2 | Valuable but not blocking. Can ship after core pipeline. |
| Precedent Engine | P2 | Cherry on top. Needs embeddings infra. Ship last. |

### New insight — build order gate:
Ship clusters → validate with Raj → if 12→5 min gap closes, remaining items become enhancements. If not, Raj tells us exactly what's still missing with real usage data.

---

## 6. Raj's Conviction Ladder (Product Spec)

This is the definitive model. Every feature in the conviction pipeline serves one rung:

```
1 article     → NOTICE          (current product handles this)
2 articles    → ATTENTION        (current product handles this)
3+ articles   → THEME/THESIS     ← NEWS CLUSTERS
+ causal chain → UNDERSTANDING   ← LLM EXPLAINERS
+ price confirm → CONVICTION     ← PRICE OVERLAY ON CLUSTERS
+ sentiment shift → READY        ← SENTIMENT TREND LINE
                → TRADE          (trader's decision, never the product's)
```

---

## 7. Key Quotes (for reference)

> "The price tells me the STORY before I know the PLOT."

> "I need the story first, then the explanation."

> "Three articles about Fed hawkishness isn't three separate pieces of information — it's ONE signal getting louder."

> "Show the conflict, don't resolve it."

> "The moment the tool starts making specific price calls, I'd question everything else it says."

> "Tell me the narrative. Not the data, not the score, not the prediction."

> "If it actually delivers conviction in 5 minutes, easily $50-100/month. Without the intelligence layer, $0."
