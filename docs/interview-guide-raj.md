# Commodity Pulse — User Interview Guide

**Subject**: Raj (27, commodity trader, Mumbai)
**Interviewer**: Financial Analyst Agent
**Goal**: Extract domain expertise on how traders consume news, assess impact, and correlate with price movements — to design Phase 3 intelligence features.

---

## Context for Interviewer

Raj is our power user. He trades Gold, Silver, Oil, and other commodities based on news. He's not technical but deeply understands market dynamics. We need to understand his **mental model** — how he connects news to trading decisions — so we can build it into the product.

Current product state:
- Dashboard shows price cards, price chart, news feed with sentiment scores, and sentiment analysis panel
- News and prices are shown separately — no visual link between them
- Each article has a sentiment score but no explanation of WHY it impacts the commodity
- Information can be overwhelming (20+ articles per commodity)

We're designing three features (Phase 3):
1. **News-price visual correlation** — show which news moved the price
2. **Quick impact summaries** — 1-2 sentence explanation per article/cluster
3. **Overall movement summary** — digest that prevents information overload

---

## Interview Sections

### Section 1: Morning Routine & Workflow (5 min)

> Understanding how Raj naturally consumes information before we design for it.

1. **Walk me through your morning trading routine.** What do you look at first? What sources? What order?

2. **When you sit down to check a commodity (say Gold), what's the first thing you want to know?** Price? News? Both?

3. **How much time do you typically spend before making a trading decision?** What percentage is research vs. gut?

4. **Do you check all 8 commodities every day, or focus on 2-3?** What determines your focus?

### Section 2: News-to-Trade Mental Model (10 min)

> This is the core. We need to understand the cognitive process between "I read a headline" and "I make a trade."

5. **When you read a headline like "Fed signals rate pause", what goes through your mind?** Walk me through the chain of reasoning to a trade.

6. **How do you determine which news actually matters for a specific commodity?** Not all news moves prices — what's your filter?

7. **Can you give me an example of a recent news event that made you take action?** What was the news? What did you trade? Why?

8. **How do you assess the MAGNITUDE of impact?** What makes something a 1% move vs. a 5% move in your mental model?

9. **How do you handle conflicting signals?** E.g., bullish news for Gold + bearish technical setup. What wins?

10. **Do you think about news impact differently for different commodities?** (e.g., Oil is geopolitics-driven, Gold is macro-driven, Wheat is weather-driven)

### Section 3: Information Overload & Prioritization (5 min)

> Designing the right level of abstraction — not too much, not too little.

11. **When you see 20 news articles about Gold, what do you actually do?** Read all? Scan headlines? Focus on top 3?

12. **What would the PERFECT summary look like?** If you had 30 seconds to understand "what happened to Gold today", what would you want to see?

13. **Do you care about individual articles, or more about the THEME?** (e.g., "3 articles about Fed policy" vs. reading each one)

14. **What information do you wish you had that you currently don't?** What's the gap in your workflow?

### Section 4: Visual & Interaction Preferences (5 min)

> How should we present the news-price link visually?

15. **If I could draw a line from a news event to the exact price movement it caused, would that be useful?** How would you use it?

16. **Would you rather see:**
    - (A) Individual articles with impact arrows pointing to price chart
    - (B) Grouped themes with aggregate impact ("Fed policy cluster: -2.3% on Gold")
    - (C) A timeline view where news dots sit on the price chart
    - (D) Something else entirely?

17. **How important is it to know the SOURCE of the news?** (Reuters vs. random blog — does it change your trust level?)

18. **Would you want to see HOW the AI calculated the impact?** Or just the conclusion?

### Section 5: Trust & Edge Cases (5 min)

> Building confidence in AI-generated insights.

19. **If the dashboard told you "Gold will drop 2% because of this news", would you trust it?** What would make you trust it more?

20. **What would make you STOP using a tool like this?** What's the dealbreaker?

21. **How do you currently validate your trading thesis?** What's your "second opinion" source?

22. **Have you ever been burned by acting on news too quickly?** What happened? What would have helped?

### Section 6: Quick Fire Round (2 min)

23. **Most important commodity for you right now?** Why?
24. **Biggest pain point in your current workflow?**
25. **If this tool could do ONE thing perfectly, what should it be?**
26. **Would you pay for this? What's it worth per month?**

---

## Post-Interview Analysis Framework

After the interview, the analyst should produce:

1. **Raj's Mental Model Map**: News → Assessment → Decision → Trade
2. **Information Hierarchy**: What he looks at first, second, third
3. **Feature Requirements Matrix**: Map interview answers to Phase 3 features
4. **Design Implications**: Specific UI/UX recommendations based on workflow
5. **Priority Refinement**: Any changes to FB-001, FB-002, FB-003 priorities based on domain insight
