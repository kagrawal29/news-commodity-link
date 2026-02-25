# Commodity Pulse — Intelligence Design Principles

**Source**: Raj user interview (2026-02-25), product-owner review
**Scope**: All conviction pipeline features — clusters, explainers, briefings, precedents, and any future intelligence layer.

---

## The One Rule

**Present evidence and patterns. Never predict outcomes or recommend actions.**

We are the analyst. The trader decides.

---

## Do / Don't Reference

| DO | DON'T |
|----|-------|
| "5 of 7 articles in this cluster are hawkish" | "Gold will drop 2%" |
| "Similar patterns preceded 1-3% moves in 6/10 instances" | "BUY" / "SELL" / "HOLD" |
| "News: BULLISH / Price: DECLINING — divergence" | "The market is wrong" or "Price will correct" |
| "Fed Rate Expectations (4 articles, bearish, -0.8%)" | "Cluster 1" or "Topic A" |
| "This matters for Gold because rate hikes increase the opportunity cost of holding zero-yield assets" | "This is bad for Gold" (without the causal chain) |
| Show confidence as a base rate: "0.75 confidence" | Show confidence as certainty: "We're 75% sure Gold will fall" |

---

## Design Constraints

1. **No action signals.** No BUY/SELL/HOLD anywhere in the UI. Ever. This is a dealbreaker that causes immediate user churn.

2. **No specific price predictions.** Base rates are fine ("1-3% range in similar cases"). Point estimates are not ("Gold will drop 2.3%").

3. **Show divergence, don't resolve it.** When news sentiment and price direction conflict, label the conflict. Don't pick a side. Traders respect tools that show reality.

4. **Use domain vocabulary.** Cluster names must be descriptive and commodity-relevant: "OPEC Supply Pressure", "Safe Haven Demand", "Fed Rate Expectations." Never generic labels.

5. **Show your work.** Transparency builds trust. "Labeled 'Fed Hawkish' because 3 articles mention rate hikes, 2 mention inflation persistence." Black boxes destroy trust.

6. **Evidence hierarchy.** Present information in layers: theme first (what's the story?), then supporting articles (what's the evidence?), then causal chain (why does it matter?). Let the trader drill down, not drown.

---

## Why This Matters

> "The moment the tool starts making specific price calls, I'd question everything else it says." — Raj

> "If it actually delivers conviction in 5 minutes, easily $50-100/month. Without the intelligence layer, $0." — Raj

The trust model IS the business model. Break trust → lose the user → $0 revenue. Maintain trust → daily usage → $50-100/month.
