"""
LLM-powered cluster explanations via OpenRouter.

Generates concise, trader-focused narrative summaries for each news
cluster.  Uses free models on OpenRouter (OpenAI-compatible API).

When no API key is configured or the service is unavailable, methods
return ``None`` gracefully — the frontend simply hides the explanation.
"""

from __future__ import annotations

import logging
import os
from typing import Optional

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

_OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
_MODEL = "meta-llama/llama-3.3-70b-instruct:free"
_TIMEOUT = 30  # seconds


class ClusterExplainer:
    """Generate narrative explanations for news theme clusters."""

    def __init__(self) -> None:
        self._api_key: Optional[str] = os.getenv("OPENROUTER_API_KEY")

    @property
    def available(self) -> bool:
        """True if an API key is configured."""
        return bool(self._api_key)

    def explain_clusters(
        self,
        clusters: list[dict],
        commodity_name: str,
    ) -> list[dict]:
        """
        Add an ``explanation`` field to each cluster dict.

        Sends a single LLM request for all clusters of one commodity
        to minimize API calls.  Returns the same list with
        ``explanation`` added (or ``None`` if unavailable).
        """
        if not self.available or not clusters:
            for c in clusters:
                c["explanation"] = None
            return clusters

        prompt = self._build_prompt(clusters, commodity_name)

        try:
            raw = self._call_llm(prompt)
            if raw:
                explanations = self._parse_response(raw, len(clusters))
            else:
                explanations = [None] * len(clusters)
        except Exception as exc:
            logger.warning("LLM explainer failed: %s", exc)
            explanations = [None] * len(clusters)

        for cluster, explanation in zip(clusters, explanations):
            cluster["explanation"] = explanation

        return clusters

    # ------------------------------------------------------------------
    # Prompt construction
    # ------------------------------------------------------------------

    @staticmethod
    def _build_prompt(clusters: list[dict], commodity_name: str) -> str:
        """Build a single prompt covering all clusters for one commodity."""
        cluster_blocks = []
        for i, c in enumerate(clusters, 1):
            headlines = "\n".join(
                f"  - {a['title']}" for a in c.get("articles", [])[:5]
            )
            price_info = ""
            if c.get("price_delta_pct") is not None:
                direction = "up" if c["price_delta_pct"] >= 0 else "down"
                price_info = f"Price moved {direction} {abs(c['price_delta_pct']):.1f}% during this period."

            divergence_info = ""
            if c.get("divergence"):
                divergence_info = f"DIVERGENCE: {c['divergence']}."

            cluster_blocks.append(
                f"CLUSTER {i}: {c['theme']}\n"
                f"Articles: {c['article_count']} | "
                f"Sentiment: {c['sentiment_label']} ({c['sentiment_avg']:+.2f})\n"
                f"{price_info} {divergence_info}\n"
                f"Headlines:\n{headlines}"
            )

        clusters_text = "\n\n".join(cluster_blocks)

        return (
            f"You are a commodity market analyst writing for traders. "
            f"Analyze these news theme clusters for {commodity_name} and "
            f"write a brief explanation for EACH cluster.\n\n"
            f"Rules:\n"
            f"- One explanation per cluster, 1-2 sentences max\n"
            f"- Focus on WHAT is happening and WHY it matters for {commodity_name}\n"
            f"- If there is a divergence between sentiment and price, call it out\n"
            f"- Use plain language a trader would use, not academic jargon\n"
            f"- NEVER give buy/sell recommendations or price predictions\n"
            f"- Start each explanation with the cluster number: [1], [2], etc.\n\n"
            f"{clusters_text}\n\n"
            f"Write your explanations now, one per cluster:"
        )

    # ------------------------------------------------------------------
    # LLM call
    # ------------------------------------------------------------------

    def _call_llm(self, prompt: str) -> Optional[str]:
        """Call OpenRouter and return the raw response text."""
        resp = requests.post(
            _OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://commodity-pulse.vercel.app",
                "X-Title": "Commodity Pulse",
            },
            json={
                "model": _MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 500,
                "temperature": 0.3,
            },
            timeout=_TIMEOUT,
        )

        if resp.status_code == 429:
            logger.warning("OpenRouter rate limited (429)")
            return None

        resp.raise_for_status()
        data = resp.json()

        choices = data.get("choices", [])
        if not choices:
            logger.warning("OpenRouter returned no choices")
            return None

        return choices[0].get("message", {}).get("content", "")

    # ------------------------------------------------------------------
    # Response parsing
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_response(raw: str, num_clusters: int) -> list[Optional[str]]:
        """
        Parse the LLM response into per-cluster explanations.

        Expected format: [1] explanation... [2] explanation...
        Falls back to splitting by newlines if markers aren't found.
        """
        explanations: list[Optional[str]] = [None] * num_clusters

        for i in range(num_clusters):
            marker = f"[{i + 1}]"
            next_marker = f"[{i + 2}]"

            start = raw.find(marker)
            if start == -1:
                continue

            start += len(marker)
            end = raw.find(next_marker, start) if i < num_clusters - 1 else len(raw)
            if end == -1:
                end = len(raw)

            text = raw[start:end].strip().strip("-:").strip()
            if text:
                explanations[i] = text

        # Fallback: if no markers found, try splitting by double newlines
        if all(e is None for e in explanations):
            lines = [l.strip() for l in raw.split("\n\n") if l.strip()]
            for i, line in enumerate(lines[:num_clusters]):
                # Strip any leading marker patterns
                clean = line.lstrip("0123456789.)[]-: ").strip()
                if clean:
                    explanations[i] = clean

        return explanations
