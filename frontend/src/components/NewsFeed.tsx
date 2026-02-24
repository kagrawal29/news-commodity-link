"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { NewsResponse, ScoredArticle } from "@/lib/api";

type Filter = "all" | "positive" | "negative" | "neutral";

interface NewsFeedProps {
  news: NewsResponse | null;
}

const FILTER_STYLES: Record<Filter, string> = {
  all: "text-cyber-cyan border-cyber-cyan/30 bg-cyber-cyan/10",
  positive: "text-cyber-green border-cyber-green/30 bg-cyber-green/10",
  negative: "text-cyber-red border-cyber-red/30 bg-cyber-red/10",
  neutral: "text-gray-400 border-gray-600/30 bg-gray-600/10",
};

function sentimentColor(label: string) {
  if (label === "positive") return "cyber-green";
  if (label === "negative") return "cyber-red";
  return "gray-500";
}

function sentimentBadge(label: string) {
  if (label === "positive") return "BULLISH";
  if (label === "negative") return "BEARISH";
  return "NEUTRAL";
}

function timeAgo(dateStr: string): string {
  const diff = Date.now() - new Date(dateStr).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 60) return `${mins}m ago`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
}

export default function NewsFeed({ news }: NewsFeedProps) {
  const [filter, setFilter] = useState<Filter>("all");

  if (!news || !news.articles.length) {
    return (
      <div className="text-gray-500 text-center py-12">
        No news articles found. Try a different commodity or check back later.
      </div>
    );
  }

  const filtered = filter === "all"
    ? news.articles
    : news.articles.filter((a) => a.sentiment_label === filter);

  return (
    <div>
      {/* Filter tabs */}
      <div className="flex gap-2 mb-4">
        {(["all", "positive", "negative", "neutral"] as Filter[]).map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-3 py-1 rounded-lg text-xs font-bold uppercase tracking-wider border transition-all ${
              filter === f ? FILTER_STYLES[f] : "text-gray-500 border-gray-700/30 hover:border-gray-600/50"
            }`}
          >
            {f === "all" ? `All (${news.articles.length})` : `${f} (${news.articles.filter((a) => a.sentiment_label === f).length})`}
          </button>
        ))}
      </div>

      {/* Articles */}
      <div className="space-y-2.5 max-h-[600px] overflow-y-auto pr-2">
        {filtered.map((article, i) => (
          <ArticleCard key={i} article={article} index={i} />
        ))}
        {filtered.length === 0 && (
          <div className="text-gray-500 text-center py-8">
            No {filter} articles found.
          </div>
        )}
      </div>
    </div>
  );
}

function ArticleCard({ article, index }: { article: ScoredArticle; index: number }) {
  const color = sentimentColor(article.sentiment_label);
  const borderColor =
    article.sentiment_label === "positive" ? "rgba(0,255,136,0.3)"
    : article.sentiment_label === "negative" ? "rgba(255,68,68,0.3)"
    : "rgba(255,0,255,0.2)";

  return (
    <motion.a
      href={article.url}
      target="_blank"
      rel="noopener noreferrer"
      initial={{ opacity: 0, x: -8 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.03 }}
      whileHover={{ x: 4 }}
      className="block rounded-lg p-3.5 transition-all"
      style={{
        background: "linear-gradient(135deg, #1a1a2e, #0e0e24)",
        borderLeft: `3px solid ${borderColor}`,
      }}
    >
      <div className="flex justify-between items-center mb-1.5">
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold px-2 py-0.5 rounded bg-cyber-blue/20 text-cyber-blue">
            {article.source}
          </span>
          <span className={`text-xs font-bold px-2 py-0.5 rounded bg-${color}/20 text-${color}`}>
            {sentimentBadge(article.sentiment_label)} {article.sentiment_score >= 0 ? "+" : ""}{article.sentiment_score.toFixed(2)}
          </span>
        </div>
        <span className="text-xs text-gray-500">{timeAgo(article.published_date)}</span>
      </div>
      <div className="text-white text-sm font-semibold leading-snug">
        {article.title}
      </div>
      {article.description && (
        <div className="text-gray-400 text-xs mt-1 line-clamp-2">
          {article.description}
        </div>
      )}
    </motion.a>
  );
}
