"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  api,
  CommodityInfo,
  PriceData,
  PriceHistoryResponse,
  NewsResponse,
  SentimentResponse,
  ClustersResponse,
  NewsCluster,
} from "@/lib/api";
import PriceCards from "./PriceCards";
import PriceChart from "./PriceChart";
import ClusterCards from "./ClusterCards";
import NewsFeed from "./NewsFeed";
import SentimentPanel from "./SentimentPanel";

interface DashboardProps {
  commodityKey: string;
  commodityInfo: CommodityInfo;
  timeframe: string;
  allCommodities: Record<string, CommodityInfo>;
}

export default function Dashboard({
  commodityKey,
  commodityInfo,
  timeframe,
  allCommodities,
}: DashboardProps) {
  const [prices, setPrices] = useState<Record<string, PriceData>>({});
  const [history, setHistory] = useState<PriceHistoryResponse | null>(null);
  const [news, setNews] = useState<NewsResponse | null>(null);
  const [sentiment, setSentiment] = useState<SentimentResponse | null>(null);
  const [clusters, setClusters] = useState<ClustersResponse | null>(null);
  const [hoveredCluster, setHoveredCluster] = useState<NewsCluster | null>(null);
  const [loading, setLoading] = useState(true);

  // Fetch all data when commodity or timeframe changes
  useEffect(() => {
    setLoading(true);
    setHoveredCluster(null);

    const displayKeys = [
      commodityKey,
      ...Object.keys(allCommodities).filter((k) => k !== commodityKey).slice(0, 3),
    ];

    Promise.all([
      // Prices for the 4 display cards
      Promise.all(
        displayKeys.map((k) =>
          api.getLatestPrice(k).then((p) => [k, p] as const).catch(() => null)
        )
      ),
      api.getPriceHistory(commodityKey, timeframe).catch(() => null),
      api.getNews(commodityKey).catch(() => null),
      api.getSentiment(commodityKey).catch(() => null),
      api.getClusters(commodityKey).catch(() => null),
    ]).then(([priceResults, hist, newsData, sentData, clusterData]) => {
      const priceMap: Record<string, PriceData> = {};
      for (const r of priceResults) {
        if (r) priceMap[r[0]] = r[1];
      }
      setPrices(priceMap);
      setHistory(hist);
      setNews(newsData);
      setSentiment(sentData);
      setClusters(clusterData);
      setLoading(false);
    });
  }, [commodityKey, timeframe, allCommodities]);

  // Poll prices every 30 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      const displayKeys = [
        commodityKey,
        ...Object.keys(allCommodities).filter((k) => k !== commodityKey).slice(0, 3),
      ];
      Promise.all(
        displayKeys.map((k) =>
          api.getLatestPrice(k).then((p) => [k, p] as const).catch(() => null)
        )
      ).then((results) => {
        setPrices((prev) => {
          const next = { ...prev };
          for (const r of results) {
            if (r) next[r[0]] = r[1];
          }
          return next;
        });
      });
    }, 30000);
    return () => clearInterval(interval);
  }, [commodityKey, allCommodities]);

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={commodityKey}
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -12 }}
        transition={{ duration: 0.3 }}
      >
        {/* Header */}
        <header className="text-center mb-8">
          <div className="text-5xl mb-2 animate-float">{commodityInfo.icon}</div>
          <h1 className="font-display text-4xl font-extrabold text-cyber-cyan animate-glow-pulse tracking-widest">
            {commodityInfo.name}
          </h1>
          <p className="text-sm text-gray-500 mt-2">
            Ticker:{" "}
            <span className="text-cyber-gold">{commodityInfo.ticker}</span>
            {" ◆ "}
            Timeframe:{" "}
            <span className="text-cyber-magenta">{timeframe}</span>
          </p>
        </header>

        {loading ? (
          <div className="text-center py-20 text-cyber-cyan animate-pulse font-display">
            LOADING DATA...
          </div>
        ) : (
          <>
            {/* Price Cards */}
            <SectionHeader title="LIVE PRICES" icon="💰" color="text-cyber-green" />
            <PriceCards
              prices={prices}
              commodities={allCommodities}
              selected={commodityKey}
            />

            {/* Price Chart */}
            <SectionHeader title="PRICE CHART" icon="📈" color="text-cyber-blue" />
            <PriceChart
              data={history}
              commodityName={commodityInfo.name}
              highlightCluster={hoveredCluster}
            />

            {/* News Theme Clusters */}
            {clusters && clusters.clusters.length > 0 && (
              <>
                <SectionHeader title="NEWS THEMES" icon="🎯" color="text-cyber-cyan" />
                <ClusterCards
                  clusters={clusters}
                  onClusterHover={setHoveredCluster}
                />
              </>
            )}

            {/* Sentiment */}
            {sentiment && (
              <>
                <SectionHeader title="SENTIMENT ANALYSIS" icon="🧠" color="text-cyber-gold" />
                <SentimentPanel sentiment={sentiment} commodityName={commodityInfo.name} />
              </>
            )}

            {/* News Feed */}
            <SectionHeader title="LATEST NEWS" icon="📰" color="text-cyber-magenta" />
            <NewsFeed news={news} />
          </>
        )}
      </motion.div>
    </AnimatePresence>
  );
}

function SectionHeader({ title, icon, color }: { title: string; icon: string; color: string }) {
  return (
    <div className="mt-8 mb-4">
      <h2 className={`font-display text-lg font-bold tracking-wider ${color}`}>
        <span className="inline-block animate-float">{icon}</span> {title}
      </h2>
      <div
        className="h-0.5 mt-2 rounded-full"
        style={{
          background: "linear-gradient(90deg, currentColor 0%, transparent 80%)",
        }}
      />
    </div>
  );
}
