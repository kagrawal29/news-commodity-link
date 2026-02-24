"use client";

import { SentimentResponse } from "@/lib/api";

interface SentimentPanelProps {
  sentiment: SentimentResponse;
  commodityName: string;
}

function sentimentColor(label: string): string {
  if (label === "positive") return "#00FF88";
  if (label === "negative") return "#FF4444";
  return "#888888";
}

function sentimentIcon(label: string): string {
  if (label === "positive") return "▲";
  if (label === "negative") return "▼";
  return "●";
}

export default function SentimentPanel({ sentiment, commodityName }: SentimentPanelProps) {
  const { summary, trend } = sentiment;
  const color = sentimentColor(summary.label);

  return (
    <div
      className="rounded-xl p-6 border overflow-hidden relative"
      style={{
        background: "linear-gradient(145deg, #1a1a2e, #0d0d22)",
        borderColor: `${color}30`,
        boxShadow: `0 0 25px ${color}0C, inset 0 0 25px ${color}04`,
      }}
    >
      {/* Top beam */}
      <div
        className="absolute top-0 left-0 right-0 h-0.5"
        style={{ background: `linear-gradient(90deg, transparent, ${color}60, transparent)` }}
      />

      <div className="flex flex-wrap gap-8 justify-between items-start">
        {/* Main score */}
        <div className="text-center min-w-[140px]">
          <div className="text-xs text-gray-400 uppercase tracking-widest mb-1">
            Overall Sentiment
          </div>
          <div
            className="text-4xl font-extrabold font-display animate-glow-pulse"
            style={{ color, textShadow: `0 0 20px ${color}70, 0 0 40px ${color}30` }}
          >
            {sentimentIcon(summary.label)} {summary.weighted_avg >= 0 ? "+" : ""}
            {summary.weighted_avg.toFixed(2)}
          </div>
          <div
            className="text-sm font-semibold uppercase tracking-widest mt-1"
            style={{ color }}
          >
            {summary.label}
          </div>
        </div>

        {/* Distribution */}
        <div className="min-w-[180px]">
          <div className="text-xs text-gray-400 uppercase tracking-widest mb-2">
            Distribution ({summary.article_count} articles)
          </div>
          <div className="flex h-2.5 rounded-full overflow-hidden bg-bg-highlight mb-2">
            <div
              className="rounded-l-full"
              style={{
                width: `${summary.positive_pct}%`,
                background: "linear-gradient(90deg, #00FF8880, #00FF88)",
                boxShadow: "0 0 8px #00FF8840",
              }}
            />
            <div style={{ width: `${summary.neutral_pct}%`, background: "#888" }} />
            <div
              className="rounded-r-full"
              style={{
                width: `${summary.negative_pct}%`,
                background: "linear-gradient(90deg, #FF4444, #FF444480)",
                boxShadow: "0 0 8px #FF444440",
              }}
            />
          </div>
          <div className="flex justify-between text-xs">
            <span className="text-cyber-green">▲ {summary.positive_pct.toFixed(0)}%</span>
            <span className="text-gray-500">● {summary.neutral_pct.toFixed(0)}%</span>
            <span className="text-cyber-red">▼ {summary.negative_pct.toFixed(0)}%</span>
          </div>
        </div>

        {/* Confidence */}
        <div className="min-w-[140px]">
          <div className="text-xs text-gray-400 uppercase tracking-widest mb-2">
            Signal Confidence
          </div>
          <div
            className="text-3xl font-bold"
            style={{ color: "#00FFFF", textShadow: "0 0 12px rgba(0,255,255,0.5)" }}
          >
            {(summary.confidence * 100).toFixed(0)}%
          </div>
          <div className="h-2 rounded-full bg-bg-highlight mt-2 overflow-hidden">
            <div
              className="h-full rounded-full"
              style={{
                width: `${Math.max(5, summary.confidence * 100)}%`,
                background: "linear-gradient(90deg, #00FFFF, #FF00FF)",
                boxShadow: "0 0 10px rgba(0,255,255,0.3)",
              }}
            />
          </div>
        </div>

        {/* Trend */}
        <div className="min-w-[120px]">
          <div className="text-xs text-gray-400 uppercase tracking-widest mb-2">
            Trend
          </div>
          <div className={`text-xl font-bold ${
            trend.direction === "improving" ? "text-cyber-green"
            : trend.direction === "declining" ? "text-cyber-red"
            : "text-gray-500"
          }`}>
            {trend.direction === "improving" ? "↗ Improving"
             : trend.direction === "declining" ? "↘ Declining"
             : "→ Stable"}
          </div>
          <div className="text-xs text-gray-500 mt-1">
            Slope: {trend.slope.toFixed(4)}
          </div>
        </div>
      </div>
    </div>
  );
}
