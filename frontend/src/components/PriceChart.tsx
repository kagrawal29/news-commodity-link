"use client";

import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";
import { PriceHistoryResponse } from "@/lib/api";

interface PriceChartProps {
  data: PriceHistoryResponse | null;
  commodityName: string;
}

export default function PriceChart({ data, commodityName }: PriceChartProps) {
  if (!data || !data.data.length) {
    return (
      <div className="text-gray-500 text-center py-12">
        No price data available.
      </div>
    );
  }

  const chartData = data.data.map((d) => ({
    date: new Date(d.Date).toLocaleDateString("en-US", { month: "short", day: "numeric" }),
    close: d.Close,
    high: d.High,
    low: d.Low,
  }));

  return (
    <div className="rounded-xl p-4 border border-cyber-cyan/10 bg-bg-card/50">
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
