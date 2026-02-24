"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ClustersResponse, NewsCluster, ClusterArticle } from "@/lib/api";

interface ClusterCardsProps {
  clusters: ClustersResponse | null;
  onClusterHover: (cluster: NewsCluster | null) => void;
}

const SENTIMENT_COLORS: Record<string, { border: string; bg: string; text: string; glow: string }> = {
  positive: {
    border: "border-cyber-green/30",
    bg: "bg-cyber-green/5",
    text: "text-cyber-green",
    glow: "rgba(0,255,136,0.15)",
  },
  negative: {
    border: "border-cyber-red/30",
    bg: "bg-cyber-red/5",
    text: "text-cyber-red",
    glow: "rgba(255,68,68,0.15)",
  },
  neutral: {
    border: "border-gray-500/30",
    bg: "bg-gray-500/5",
    text: "text-gray-400",
    glow: "rgba(128,128,128,0.1)",
  },
};

function convictionLevel(count: number): { label: string; color: string } {
  if (count >= 3) return { label: "THESIS", color: "text-cyber-cyan" };
  if (count === 2) return { label: "ATTENTION", color: "text-cyber-gold" };
  return { label: "NOTICE", color: "text-gray-500" };
}

function sentimentBadge(label: string, avg: number): string {
  if (label === "positive") return `BULLISH +${avg.toFixed(2)}`;
  if (label === "negative") return `BEARISH ${avg.toFixed(2)}`;
  return `NEUTRAL ${avg.toFixed(2)}`;
}

export default function ClusterCards({ clusters, onClusterHover }: ClusterCardsProps) {
  const [expanded, setExpanded] = useState<string | null>(null);

  if (!clusters || !clusters.clusters.length) {
    return (
      <div className="text-gray-500 text-center py-12">
        No theme clusters detected. Not enough articles to form patterns.
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {/* Coverage stat */}
      <div className="text-xs text-gray-500 text-right mb-1">
        {clusters.clustered_articles} of {clusters.total_articles} articles matched themes
      </div>

      {clusters.clusters.map((cluster, i) => {
        const colors = SENTIMENT_COLORS[cluster.sentiment_label] || SENTIMENT_COLORS.neutral;
        const conviction = convictionLevel(cluster.article_count);
        const isExpanded = expanded === cluster.theme;

        return (
          <motion.div
            key={cluster.theme}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.08 }}
            onMouseEnter={() => onClusterHover(cluster)}
            onMouseLeave={() => onClusterHover(null)}
            className={`rounded-xl border transition-all duration-300 cursor-pointer ${colors.border}`}
            style={{
              background: "linear-gradient(145deg, #1a1a2e, #0d0d22)",
              boxShadow: isExpanded ? `0 0 25px ${colors.glow}` : `0 0 10px ${colors.glow}`,
            }}
          >
            {/* Card header */}
            <div
              className="p-4"
              onClick={() => setExpanded(isExpanded ? null : cluster.theme)}
            >
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-display text-sm font-bold tracking-wider text-white">
                  {cluster.theme}
                </h3>
                <span className={`text-xs font-bold tracking-wider ${conviction.color}`}>
                  {conviction.label}
                </span>
              </div>

              <div className="flex items-center gap-3 flex-wrap">
                {/* Sentiment badge */}
                <span className={`text-xs font-bold px-2 py-0.5 rounded ${colors.text} ${colors.bg}`}>
                  {sentimentBadge(cluster.sentiment_label, cluster.sentiment_avg)}
                </span>

                {/* Article count */}
                <span className="text-xs text-gray-400">
                  {cluster.article_count} article{cluster.article_count !== 1 ? "s" : ""}
                </span>

                {/* Price delta */}
                {cluster.price_delta_pct !== null && (
                  <span
                    className={`text-xs font-bold ${
                      cluster.price_delta_pct >= 0 ? "text-cyber-green" : "text-cyber-red"
                    }`}
                  >
                    {cluster.price_delta_pct >= 0 ? "+" : ""}
                    {cluster.price_delta_pct.toFixed(2)}%
                  </span>
                )}

                {/* Divergence warning */}
                {cluster.divergence && (
                  <span className="text-xs font-bold text-cyber-gold px-2 py-0.5 rounded bg-cyber-gold/10 border border-cyber-gold/20">
                    DIVERGENCE
                  </span>
                )}
              </div>

              {/* Divergence detail */}
              {cluster.divergence && (
                <div className="mt-2 text-xs text-cyber-gold/80 italic">
                  {cluster.divergence}
                </div>
              )}

              {/* LLM explanation */}
              {cluster.explanation && (
                <div className="mt-2.5 text-sm text-gray-300 leading-relaxed border-l-2 border-cyber-cyan/20 pl-3">
                  {cluster.explanation}
                </div>
              )}

              {/* Transparency: why this cluster matched */}
              {cluster.description && !cluster.explanation && (
                <div className="mt-2 text-xs text-gray-500 leading-relaxed">
                  {cluster.description}
                </div>
              )}
            </div>

            {/* Expanded article list */}
            <AnimatePresence>
              {isExpanded && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.2 }}
                  className="overflow-hidden"
                >
                  <div className="border-t border-white/5 px-4 pb-4 pt-3 space-y-2">
                    {cluster.articles.map((article, j) => (
                      <ClusterArticleRow key={j} article={article} />
                    ))}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        );
      })}
    </div>
  );
}

function ClusterArticleRow({ article }: { article: ClusterArticle }) {
  const scoreColor =
    article.sentiment_label === "positive"
      ? "text-cyber-green"
      : article.sentiment_label === "negative"
      ? "text-cyber-red"
      : "text-gray-500";

  return (
    <a
      href={article.url}
      target="_blank"
      rel="noopener noreferrer"
      className="flex items-start gap-2 py-1.5 px-2 rounded-lg hover:bg-white/5 transition-colors"
    >
      <span className={`text-xs font-mono font-bold shrink-0 mt-0.5 ${scoreColor}`}>
        {article.sentiment_score >= 0 ? "+" : ""}
        {article.sentiment_score.toFixed(2)}
      </span>
      <div className="min-w-0">
        <div className="text-sm text-white/90 leading-snug truncate">
          {article.title}
        </div>
        <div className="text-xs text-gray-600 mt-0.5">
          {article.source}
        </div>
      </div>
    </a>
  );
}
