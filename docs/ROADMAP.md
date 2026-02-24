# Commodity Pulse — Product Roadmap

**Core Vision**: Turn commodity news noise into trading conviction in 5 minutes.
**Core Loop**: Scan → Understand → Validate → Trade

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

## Phase 2 — Atmosphere & Experience (NEXT)
- [ ] Animated grid background with floating particles
- [ ] Loading screen with pulse animation
- [ ] Price spike visual reactions (glow, particles, screen shake)
- [ ] Synthwave music + sound effects (mutable, volume control)
- [ ] Hover effects on price/news cards (3D lift, glow)
- [ ] Breaking news slide-in animation

> **Architecture note (audio state):** No global state management exists yet. Music/sound state must persist across commodity switches (Dashboard re-renders via AnimatePresence). Recommended approach: React Context for audio state or a singleton audio manager module. Audio assets should be lazy-loaded, not bundled.

## Phase 3 — Intelligence Layer (PLANNED)
- [ ] **[P1]** Commodity-specific news filtering (per-commodity keywords) — prerequisite for other Phase 3 items
- [ ] **[P1]** News theme clusters with interactive price overlay
- [ ] **[P1]** LLM-powered correlation explainers ("Why this impacts Gold")
- [ ] **[P2]** Historical precedent engine (similar past events + outcomes)

## Phase 4 — Trading Tools (FUTURE)
- [ ] Real-time WebSocket price ticking
- [ ] Price alerts with browser notifications
- [ ] Portfolio P&L tracker
- [ ] Watchlist / pinned commodities
- [ ] AI-generated daily briefing

## Phase 5 — Growth (FUTURE)
- [ ] Landing page with waitlist
- [ ] Mobile responsive design
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
