"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

const FEATURES = [
  {
    icon: "💰",
    title: "Real-Time Prices",
    description: "Live commodity futures data across 8 major markets with 30-second polling updates.",
    color: "#00FF88",
  },
  {
    icon: "🧠",
    title: "AI Sentiment Analysis",
    description: "VADER NLP scores every headline. See weighted sentiment, confidence levels, and trend direction.",
    color: "#00FFFF",
  },
  {
    icon: "📰",
    title: "News Intelligence",
    description: "Aggregated from Reuters, Investing.com, Kitco, Oilprice.com, and Yahoo Finance RSS feeds.",
    color: "#FF00FF",
  },
  {
    icon: "⌨️",
    title: "Keyboard Shortcuts",
    description: "Press G for Gold, O for Oil, S for Silver. Navigate 8 commodities without touching the mouse.",
    color: "#FFD700",
  },
];

const INTELLIGENCE_STEPS = [
  { step: "01", label: "SCAN", description: "Aggregate news from 15+ RSS feeds across all commodity sectors", color: "#00FFFF" },
  { step: "02", label: "FILTER", description: "Keyword matching isolates commodity-relevant articles from general noise", color: "#00d4ff" },
  { step: "03", label: "SCORE", description: "VADER sentiment + keyword boosting assigns [-1, +1] scores per headline", color: "#8338ec" },
  { step: "04", label: "CORRELATE", description: "Map sentiment distribution against live price movements and trend data", color: "#FF00FF" },
  { step: "05", label: "SIGNAL", description: "Confidence-weighted aggregate tells you: bullish, bearish, or noise", color: "#FF4444" },
  { step: "06", label: "DECIDE", description: "5 minutes from market open to trading conviction, backed by data", color: "#00FF88" },
];

const COMMODITIES = [
  { icon: "🥇", name: "Gold", ticker: "GC=F" },
  { icon: "🥈", name: "Silver", ticker: "SI=F" },
  { icon: "🛢️", name: "Crude Oil", ticker: "CL=F" },
  { icon: "🔥", name: "Natural Gas", ticker: "NG=F" },
  { icon: "🪙", name: "Copper", ticker: "HG=F" },
  { icon: "✨", name: "Platinum", ticker: "PL=F" },
  { icon: "🌾", name: "Wheat", ticker: "ZW=F" },
  { icon: "🌽", name: "Corn", ticker: "ZC=F" },
];

export default function LandingPage() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    setVisible(true);
  }, []);

  return (
    <div className="min-h-screen overflow-x-hidden">
      {/* Hero */}
      <section className="relative min-h-screen flex flex-col items-center justify-center px-6 text-center">
        {/* Glow orbs */}
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-cyber-cyan/5 rounded-full blur-[120px] pointer-events-none" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-cyber-magenta/5 rounded-full blur-[120px] pointer-events-none" />

        <div
          className={`transition-all duration-1000 ${visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}
        >
          <div className="text-6xl mb-6 animate-float">📈📰</div>
          <h1 className="font-display text-5xl md:text-7xl font-extrabold tracking-wider mb-4">
            <span className="text-cyber-cyan animate-glow-pulse">COMMODITY</span>
            <br />
            <span className="text-cyber-magenta">PULSE</span>
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 max-w-2xl mx-auto leading-relaxed mb-4">
            Every trading app shows you{" "}
            <span className="text-white font-bold">WHAT</span> happened.
          </p>
          <p className="text-xl md:text-2xl max-w-2xl mx-auto leading-relaxed mb-10">
            <span className="text-cyber-cyan font-bold">Commodity Pulse</span> tells you{" "}
            <span className="text-cyber-green font-bold">WHY</span> it matters.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/dashboard"
              className="group relative px-8 py-4 rounded-xl font-display text-lg font-bold tracking-wider text-bg-dark bg-cyber-cyan hover:bg-cyber-cyan/90 transition-all duration-300 shadow-[0_0_30px_rgba(0,255,255,0.3)] hover:shadow-[0_0_50px_rgba(0,255,255,0.5)]"
            >
              TRY IT NOW
              <span className="ml-2 inline-block transition-transform group-hover:translate-x-1">→</span>
            </Link>
            <a
              href="#features"
              className="px-8 py-4 rounded-xl font-display text-lg font-bold tracking-wider text-cyber-cyan border border-cyber-cyan/30 hover:bg-cyber-cyan/10 transition-all duration-300"
            >
              LEARN MORE
            </a>
          </div>
        </div>

        {/* Scroll indicator */}
        <div className="absolute bottom-8 animate-bounce text-gray-500 text-sm">
          ↓ SCROLL
        </div>
      </section>

      {/* Tagline band */}
      <section className="py-16 border-y border-cyber-cyan/10 bg-gradient-to-r from-transparent via-cyber-cyan/5 to-transparent">
        <p className="text-center text-lg md:text-xl text-gray-400 max-w-3xl mx-auto px-6 font-mono">
          &ldquo;Turn news noise into trading conviction in{" "}
          <span className="text-cyber-gold font-bold">5 minutes</span>.&rdquo;
        </p>
      </section>

      {/* Features */}
      <section id="features" className="py-24 px-6 max-w-6xl mx-auto">
        <h2 className="font-display text-3xl md:text-4xl font-extrabold text-center mb-4 tracking-wider">
          <span className="text-cyber-cyan">WHAT</span>{" "}
          <span className="text-white">YOU GET</span>
        </h2>
        <p className="text-gray-500 text-center mb-16 max-w-xl mx-auto">
          A complete commodity intelligence dashboard built for speed.
        </p>

        <div className="grid md:grid-cols-2 gap-6">
          {FEATURES.map((f, i) => (
            <div
              key={i}
              className="rounded-xl p-6 border transition-all duration-300 hover:-translate-y-1"
              style={{
                background: "linear-gradient(145deg, #1a1a2e, #0d0d22)",
                borderColor: `${f.color}20`,
                boxShadow: `0 0 20px ${f.color}08`,
              }}
            >
              <div className="text-4xl mb-3">{f.icon}</div>
              <h3 className="font-display text-lg font-bold tracking-wider mb-2" style={{ color: f.color }}>
                {f.title}
              </h3>
              <p className="text-gray-400 text-sm leading-relaxed">{f.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Intelligence Stack */}
      <section className="py-24 px-6 border-t border-cyber-cyan/10">
        <div className="max-w-4xl mx-auto">
          <h2 className="font-display text-3xl md:text-4xl font-extrabold text-center mb-4 tracking-wider">
            <span className="text-cyber-magenta">THE INTELLIGENCE</span>{" "}
            <span className="text-white">STACK</span>
          </h2>
          <p className="text-gray-500 text-center mb-16 max-w-xl mx-auto">
            Six steps from raw news to trading conviction. Fully automated.
          </p>

          <div className="space-y-4">
            {INTELLIGENCE_STEPS.map((s, i) => (
              <div
                key={i}
                className="flex items-start gap-5 rounded-xl p-5 border border-white/5 transition-all duration-300 hover:border-white/10"
                style={{ background: "linear-gradient(135deg, #1a1a2e, #0e0e24)" }}
              >
                <div
                  className="font-display text-2xl font-extrabold shrink-0 w-16 text-center"
                  style={{ color: s.color, textShadow: `0 0 15px ${s.color}50` }}
                >
                  {s.step}
                </div>
                <div>
                  <div className="font-display text-sm font-bold tracking-widest mb-1" style={{ color: s.color }}>
                    {s.label}
                  </div>
                  <p className="text-gray-400 text-sm leading-relaxed">{s.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Commodities */}
      <section className="py-24 px-6 border-t border-cyber-cyan/10">
        <div className="max-w-4xl mx-auto">
          <h2 className="font-display text-3xl md:text-4xl font-extrabold text-center mb-4 tracking-wider">
            <span className="text-cyber-gold">8 MARKETS</span>{" "}
            <span className="text-white">ONE DASHBOARD</span>
          </h2>
          <p className="text-gray-500 text-center mb-12 max-w-xl mx-auto">
            Metals, energy, and agriculture — all with live prices, news, and sentiment.
          </p>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            {COMMODITIES.map((c, i) => (
              <div
                key={i}
                className="rounded-xl p-4 text-center border border-white/5 bg-gradient-to-b from-bg-card to-bg-dark hover:border-cyber-cyan/20 transition-all duration-300"
              >
                <div className="text-3xl mb-2">{c.icon}</div>
                <div className="text-white font-bold text-sm">{c.name}</div>
                <div className="text-gray-600 text-xs font-mono">{c.ticker}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-24 px-6 border-t border-cyber-cyan/10">
        <div className="max-w-2xl mx-auto text-center">
          <h2 className="font-display text-3xl md:text-4xl font-extrabold tracking-wider mb-6">
            <span className="text-white">READY TO</span>{" "}
            <span className="text-cyber-green">TRADE SMARTER?</span>
          </h2>
          <p className="text-gray-400 mb-10 text-lg">
            Open the dashboard and see what&apos;s moving your markets — right now.
          </p>
          <Link
            href="/dashboard"
            className="inline-block px-10 py-5 rounded-xl font-display text-xl font-bold tracking-wider text-bg-dark bg-cyber-cyan hover:bg-cyber-cyan/90 transition-all duration-300 shadow-[0_0_40px_rgba(0,255,255,0.3)] hover:shadow-[0_0_60px_rgba(0,255,255,0.5)]"
          >
            LAUNCH DASHBOARD →
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 border-t border-white/5 text-center">
        <p className="text-gray-600 text-xs font-mono">
          COMMODITY PULSE — Built with Next.js + FastAPI + VADER NLP
        </p>
        <p className="text-gray-700 text-xs mt-1">
          Powered by yfinance • GNews • RSS • Recharts
        </p>
      </footer>
    </div>
  );
}
