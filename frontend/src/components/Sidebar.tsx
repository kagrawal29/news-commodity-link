"use client";

import { CommodityInfo } from "@/lib/api";

const TIMEFRAMES = [
  { key: "1d", label: "1 Day" },
  { key: "7d", label: "7 Days" },
  { key: "30d", label: "30 Days" },
  { key: "90d", label: "90 Days" },
  { key: "1y", label: "1 Year" },
];

interface SidebarProps {
  commodities: Record<string, CommodityInfo>;
  selected: string;
  onSelect: (key: string) => void;
  timeframe: string;
  onTimeframeChange: (tf: string) => void;
}

export default function Sidebar({
  commodities,
  selected,
  onSelect,
  timeframe,
  onTimeframeChange,
}: SidebarProps) {
  return (
    <aside className="w-64 shrink-0 border-r border-cyber-cyan/10 bg-gradient-to-b from-bg-card to-[#0d0d1a] p-5 flex flex-col">
      {/* Brand */}
      <div className="text-center mb-6">
        <div className="text-3xl mb-1">📈📰</div>
        <h1 className="font-display text-cyber-cyan text-lg font-extrabold tracking-wider animate-glow-pulse">
          COMMODITY PULSE
        </h1>
        <p className="text-xs text-gray-500 mt-1">News × Price Correlation</p>
      </div>

      <hr className="border-cyber-cyan/10 mb-5" />

      {/* Commodity selector */}
      <div className="text-cyber-magenta text-xs font-bold tracking-wide mb-2">
        🔍 SELECT COMMODITY
      </div>
      <nav className="space-y-1 mb-6">
        {Object.entries(commodities).map(([key, info]) => (
          <button
            key={key}
            onClick={() => onSelect(key)}
            className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-all duration-200 ${
              selected === key
                ? "bg-cyber-cyan/10 text-cyber-cyan border border-cyber-cyan/30 shadow-[0_0_12px_rgba(0,255,255,0.1)]"
                : "text-gray-400 hover:text-gray-200 hover:bg-white/5"
            }`}
          >
            {info.icon} {info.name}
          </button>
        ))}
      </nav>

      {/* Timeframe selector */}
      <div className="text-cyber-gold text-xs font-bold tracking-wide mb-2">
        ⏰ TIMEFRAME
      </div>
      <div className="space-y-1 mb-6">
        {TIMEFRAMES.map((tf) => (
          <button
            key={tf.key}
            onClick={() => onTimeframeChange(tf.key)}
            className={`w-full text-left px-3 py-1.5 rounded-lg text-sm transition-all duration-200 ${
              timeframe === tf.key
                ? "bg-cyber-gold/10 text-cyber-gold border border-cyber-gold/30"
                : "text-gray-400 hover:text-gray-200 hover:bg-white/5"
            }`}
          >
            {tf.label}
          </button>
        ))}
      </div>

      {/* Footer */}
      <div className="mt-auto pt-4 border-t border-cyber-cyan/10">
        <p className="text-[0.65rem] text-gray-600 text-center leading-relaxed">
          Powered by yfinance • GNews • RSS
          <br />
          Built with Next.js + FastAPI
        </p>
      </div>
    </aside>
  );
}
