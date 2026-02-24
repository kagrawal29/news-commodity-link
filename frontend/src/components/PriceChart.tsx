"use client";

import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ReferenceArea,
} from "recharts";
import { PriceHistoryResponse, NewsCluster } from "@/lib/api";

interface PriceChartProps {
  data: PriceHistoryResponse | null;
  commodityName: string;
  highlightCluster?: NewsCluster | null;
}

export default function PriceChart({ data, commodityName, highlightCluster }: PriceChartProps) {
  if (!data || !data.data.length) {
    return (
      <div className="text-gray-500 text-center py-12">
        No price data available.
      </div>
    );
  }

  const chartData = data.data.map((d) => ({
    date: new Date(d.Date).toLocaleDateString("en-US", { month: "short", day: "numeric" }),
    rawDate: new Date(d.Date).getTime(),
    close: d.Close,
    high: d.High,
    low: d.Low,
  }));

  // Find chart indices that match the cluster's time window
  let refStart: string | undefined;
  let refEnd: string | undefined;

  if (highlightCluster) {
    const clusterStart = new Date(highlightCluster.start_time).getTime();
    const clusterEnd = new Date(highlightCluster.end_time).getTime();

    // Find the first and last chart points within (or nearest to) the cluster window
    let startIdx = -1;
    let endIdx = -1;

    for (let i = 0; i < chartData.length; i++) {
      const t = chartData[i].rawDate;
      if (t >= clusterStart - 86400000 && startIdx === -1) {
        startIdx = i;
      }
      if (t <= clusterEnd + 86400000) {
        endIdx = i;
      }
    }

    // If cluster spans less than what we can see, ensure at least 1 bar
    if (startIdx === -1) startIdx = 0;
    if (endIdx === -1) endIdx = chartData.length - 1;
    if (endIdx < startIdx) endIdx = startIdx;

    refStart = chartData[startIdx]?.date;
    refEnd = chartData[endIdx]?.date;
  }

  const highlightColor =
    highlightCluster?.sentiment_label === "positive"
      ? "rgba(0,255,136,0.12)"
      : highlightCluster?.sentiment_label === "negative"
      ? "rgba(255,68,68,0.12)"
      : "rgba(0,255,255,0.08)";

  return (
    <div className="rounded-xl p-4 border border-cyber-cyan/10 bg-bg-card/50 relative">
      {/* Cluster label overlay */}
      {highlightCluster && (
        <div className="absolute top-3 right-4 z-10 text-xs font-display tracking-wider text-cyber-gold bg-bg-dark/80 px-3 py-1 rounded-lg border border-cyber-gold/20">
          {highlightCluster.theme}
          {highlightCluster.price_delta_pct !== null && (
            <span
              className={`ml-2 font-bold ${
                highlightCluster.price_delta_pct >= 0 ? "text-cyber-green" : "text-cyber-red"
              }`}
            >
              {highlightCluster.price_delta_pct >= 0 ? "+" : ""}
              {highlightCluster.price_delta_pct.toFixed(2)}%
            </span>
          )}
        </div>
      )}

      <ResponsiveContainer width="100%" height={380}>
        <AreaChart data={chartData}>
          <defs>
            <linearGradient id="priceGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#00FFFF" stopOpacity={0.15} />
              <stop offset="100%" stopColor="#00FFFF" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
          <XAxis
            dataKey="date"
            tick={{ fill: "#666", fontSize: 11 }}
            axisLine={{ stroke: "rgba(255,255,255,0.04)" }}
          />
          <YAxis
            tick={{ fill: "#00FFFF", fontSize: 11 }}
            axisLine={{ stroke: "rgba(255,255,255,0.04)" }}
            domain={["auto", "auto"]}
            tickFormatter={(v: number) => `$${v.toLocaleString()}`}
          />
          <Tooltip
            contentStyle={{
              background: "#1a1a2e",
              border: "1px solid rgba(0,255,255,0.3)",
              borderRadius: 8,
              color: "#e0e0e0",
              fontFamily: "Share Tech Mono, monospace",
              fontSize: 12,
            }}
            formatter={(value: number) => [`$${value.toLocaleString(undefined, { minimumFractionDigits: 2 })}`, commodityName]}
          />

          {/* Cluster time-window highlight */}
          {refStart && refEnd && (
            <ReferenceArea
              x1={refStart}
              x2={refEnd}
              fill={highlightColor}
              strokeOpacity={0}
            />
          )}

          <Area
            type="monotone"
            dataKey="close"
            stroke="#00FFFF"
            strokeWidth={2}
            fill="url(#priceGradient)"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
