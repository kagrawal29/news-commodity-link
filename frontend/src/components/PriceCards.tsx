"use client";

import { motion } from "framer-motion";
import { CommodityInfo, PriceData } from "@/lib/api";

interface PriceCardsProps {
  prices: Record<string, PriceData>;
  commodities: Record<string, CommodityInfo>;
  selected: string;
}

export default function PriceCards({ prices, commodities, selected }: PriceCardsProps) {
  const displayKeys = [
    selected,
    ...Object.keys(commodities).filter((k) => k !== selected).slice(0, 3),
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {displayKeys.map((key, i) => {
        const info = commodities[key];
        const price = prices[key];
        if (!info) return null;

        const isPositive = price ? price.change >= 0 : true;
        const glowColor = isPositive ? "0,255,136" : "255,68,68";

        return (
          <motion.div
            key={key}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.08 }}
            whileHover={{ y: -4, scale: 1.02 }}
            className="relative rounded-xl p-5 text-center overflow-hidden border animate-border-glow"
            style={{
              background: `linear-gradient(145deg, #1a1a2e, #0f0f28)`,
              borderColor: `rgba(${glowColor}, 0.2)`,
              boxShadow: `0 0 20px rgba(${glowColor}, 0.08), inset 0 0 20px rgba(${glowColor}, 0.03)`,
            }}
          >
            {/* Top beam */}
            <div
              className="absolute top-0 left-0 right-0 h-0.5"
              style={{
                background: `linear-gradient(90deg, transparent, rgba(${glowColor}, 0.5), transparent)`,
              }}
            />

            <div className="text-3xl mb-1">{info.icon}</div>
            <div className="text-white font-bold text-sm">{info.name}</div>

            {price ? (
              <>
                <div className="text-cyber-cyan text-2xl font-extrabold mt-2"
                  style={{ textShadow: "0 0 12px rgba(0,255,255,0.5)" }}>
                  ${price.price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                </div>
                <div
                  className={`text-sm font-semibold mt-1 ${isPositive ? "text-cyber-green" : "text-cyber-red"}`}
                  style={{ textShadow: `0 0 8px rgba(${glowColor}, 0.3)` }}
                >
                  {isPositive ? "▲" : "▼"} {price.change >= 0 ? "+" : ""}
                  {price.change.toFixed(2)} ({price.change_pct >= 0 ? "+" : ""}
                  {price.change_pct.toFixed(2)}%)
                </div>
              </>
            ) : (
              <div className="text-gray-500 text-sm mt-3">Loading...</div>
            )}
          </motion.div>
        );
      })}
    </div>
  );
}
