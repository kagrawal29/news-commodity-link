"use client";

import { useEffect, useState } from "react";
import { api, CommodityInfo } from "@/lib/api";
import Sidebar from "@/components/Sidebar";
import Dashboard from "@/components/Dashboard";

export default function Home() {
  const [commodities, setCommodities] = useState<Record<string, CommodityInfo>>({});
  const [selected, setSelected] = useState("gold");
  const [timeframe, setTimeframe] = useState("30d");
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    api.getCommodities().then(setCommodities).catch(console.error);
  }, []);

  // Keyboard shortcuts
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;
      const map: Record<string, string> = {
        g: "gold", s: "silver", o: "crude_oil", n: "natural_gas",
        c: "copper", p: "platinum", w: "wheat", r: "corn",
      };
      const key = map[e.key.toLowerCase()];
      if (key && commodities[key]) setSelected(key);
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [commodities]);

  if (!Object.keys(commodities).length) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-cyber-cyan animate-glow-pulse font-display text-2xl">
          LOADING...
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen">
      <Sidebar
        commodities={commodities}
        selected={selected}
        onSelect={setSelected}
        timeframe={timeframe}
        onTimeframeChange={setTimeframe}
        isOpen={sidebarOpen}
        onToggle={() => setSidebarOpen((prev) => !prev)}
      />
      <main className="flex-1 overflow-y-auto p-4 md:p-6 pt-16 md:pt-6">
        <Dashboard
          commodityKey={selected}
          commodityInfo={commodities[selected]}
          timeframe={timeframe}
          allCommodities={commodities}
        />
      </main>
    </div>
  );
}
