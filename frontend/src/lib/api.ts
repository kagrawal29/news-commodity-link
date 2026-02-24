// In production (Vercel), frontend and API share the same domain — use "".
// In development, .env.development sets NEXT_PUBLIC_API_URL=http://localhost:8000.
const API_BASE = process.env.NEXT_PUBLIC_API_URL || "";

async function fetchAPI<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`API error ${res.status}: ${path}`);
  }
  return res.json();
}

export interface CommodityInfo {
  name: string;
  ticker: string;
  icon: string;
}

export interface PriceData {
  commodity: string;
  price: number;
  change: number;
  change_pct: number;
  volume: number;
  timestamp: string;
}

export interface PriceRecord {
  Date: string;
  Open: number;
  High: number;
  Low: number;
  Close: number;
  Volume: number;
  Change: number;
  Change_Pct: number;
}

export interface PriceHistoryResponse {
  commodity: string;
  timeframe: string;
  data: PriceRecord[];
}

export interface ScoredArticle {
  title: string;
  description: string;
  source: string;
  url: string;
  published_date: string;
  sentiment_score: number;
  sentiment_label: "positive" | "negative" | "neutral";
}

export interface NewsResponse {
  commodity: string;
  articles: ScoredArticle[];
  count: number;
}

export interface SentimentSummary {
  weighted_avg: number;
  simple_avg: number;
  label: string;
  confidence: number;
  article_count: number;
  positive_count: number;
  negative_count: number;
  neutral_count: number;
  positive_pct: number;
  negative_pct: number;
  neutral_pct: number;
}

export interface SentimentResponse {
  commodity: string;
  summary: SentimentSummary;
  rolling: Array<{
    window_start: string;
    window_end: string;
    avg_sentiment: number;
    article_count: number;
  }>;
  trend: {
    direction: "improving" | "declining" | "stable";
    slope: number;
    data_points: number;
  };
}

export interface ClusterArticle {
  title: string;
  source: string;
  url: string;
  published_date: string;
  sentiment_score: number;
  sentiment_label: "positive" | "negative" | "neutral";
}

export interface NewsCluster {
  theme: string;
  headline: string;
  description: string;
  article_count: number;
  sentiment_avg: number;
  sentiment_label: "positive" | "negative" | "neutral";
  start_time: string;
  end_time: string;
  price_delta: number | null;
  price_delta_pct: number | null;
  divergence: string | null;
  explanation: string | null;
  articles: ClusterArticle[];
}

export interface ClustersResponse {
  commodity: string;
  clusters: NewsCluster[];
  total_articles: number;
  clustered_articles: number;
}

export const api = {
  getCommodities: () =>
    fetchAPI<Record<string, CommodityInfo>>("/api/commodities"),

  getLatestPrice: (commodity: string) =>
    fetchAPI<PriceData>(`/api/prices/${commodity}`),

  getPriceHistory: (commodity: string, timeframe = "30d") =>
    fetchAPI<PriceHistoryResponse>(
      `/api/prices/${commodity}/history?timeframe=${timeframe}`
    ),

  getNews: (commodity: string) =>
    fetchAPI<NewsResponse>(`/api/news/${commodity}`),

  getSentiment: (commodity: string) =>
    fetchAPI<SentimentResponse>(`/api/sentiment/${commodity}`),

  getClusters: (commodity: string) =>
    fetchAPI<ClustersResponse>(`/api/news/${commodity}/clusters`),
};
