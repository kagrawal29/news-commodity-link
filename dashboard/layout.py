"""
Main layout controller for the Commodity News x Price Correlation Dashboard.

Applies the dark cyberpunk theme, renders the sidebar commodity selector, and
orchestrates the main content area (price cards, news feed, and chart
placeholders).
"""

from __future__ import annotations

import textwrap

import pandas as pd
import streamlit as st

from config.commodities import COMMODITIES
from config.settings import COLORS, TIMEFRAME_OPTIONS
from dashboard.charts import (
    commodity_card_sparkline,
    correlation_timeline,
    multi_commodity_overlay,
    news_volume_chart,
    price_chart,
    sentiment_gauge,
    sentiment_heatmap,
)
from dashboard.components import (
    render_news_feed,
    render_price_card,
    render_section_header,
    render_sentiment_summary,
)
from data.cache_manager import CacheManager
from data.news_fetcher import NewsFetcher
from data.price_fetcher import PriceFetcher
from nlp.analyzer import SentimentAnalyzer


def _html(text: str) -> str:
    """Strip common leading whitespace so Markdown won't treat HTML as a code block."""
    return textwrap.dedent(text).strip()


# ------------------------------------------------------------------
# Theme injection (dark neon / cyberpunk)
# ------------------------------------------------------------------

_CUSTOM_CSS = f"""
<style>
    /* ---- Global background with animated gradient ---- */
    .stApp {{
        background: #0a0a0a;
        background-image:
            radial-gradient(ellipse at 20% 50%, {COLORS['neon_cyan']}06 0%, transparent 50%),
            radial-gradient(ellipse at 80% 20%, {COLORS['magenta']}06 0%, transparent 50%),
            radial-gradient(ellipse at 50% 80%, {COLORS['electric_blue']}04 0%, transparent 50%);
    }}

    /* ---- Animated grid overlay ---- */
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image:
            linear-gradient({COLORS['neon_cyan']}05 1px, transparent 1px),
            linear-gradient(90deg, {COLORS['neon_cyan']}05 1px, transparent 1px);
        background-size: 60px 60px;
        animation: gridDrift 20s linear infinite;
        pointer-events: none;
        z-index: 0;
    }}

    @keyframes gridDrift {{
        0% {{ transform: translate(0, 0); }}
        100% {{ transform: translate(60px, 60px); }}
    }}

    /* ---- Scan line effect ---- */
    .stApp::after {{
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg,
            transparent 0%,
            {COLORS['neon_cyan']}40 20%,
            {COLORS['neon_cyan']}80 50%,
            {COLORS['neon_cyan']}40 80%,
            transparent 100%);
        animation: scanLine 4s ease-in-out infinite;
        pointer-events: none;
        z-index: 9999;
        box-shadow: 0 0 15px {COLORS['neon_cyan']}50, 0 0 30px {COLORS['neon_cyan']}20;
    }}

    @keyframes scanLine {{
        0% {{ top: -3px; opacity: 0; }}
        10% {{ opacity: 1; }}
        90% {{ opacity: 1; }}
        100% {{ top: 100vh; opacity: 0; }}
    }}

    /* ---- Sidebar ---- */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COLORS['bg_card']} 0%, #0d0d1a 100%);
        border-right: 1px solid {COLORS['neon_cyan']}20;
        box-shadow: 4px 0 25px {COLORS['neon_cyan']}08;
    }}

    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] label {{
        color: {COLORS['text_secondary']};
    }}

    /* ---- Headings ---- */
    h1, h2, h3, h4, h5, h6 {{
        color: {COLORS['text_primary']} !important;
    }}

    /* ---- Default text ---- */
    .stMarkdown p, .stMarkdown li {{
        color: {COLORS['text_secondary']};
    }}

    /* ---- Radio / selectbox highlight ---- */
    div[data-baseweb="radio"] label {{
        color: {COLORS['text_secondary']} !important;
    }}

    div[data-baseweb="select"] {{
        background-color: {COLORS['bg_highlight']};
    }}

    /* ---- Scrollbar ---- */
    ::-webkit-scrollbar {{
        width: 6px;
    }}
    ::-webkit-scrollbar-track {{
        background: transparent;
    }}
    ::-webkit-scrollbar-thumb {{
        background: {COLORS['magenta']}50;
        border-radius: 3px;
    }}

    /* ---- Metric overrides ---- */
    [data-testid="stMetricValue"] {{
        color: {COLORS['neon_cyan']} !important;
    }}

    /* ---- Hide default Streamlit footer / hamburger for cleaner look ---- */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    /* ---- Neon glow keyframes ---- */
    @keyframes neonPulse {{
        0%, 100% {{ text-shadow: 0 0 10px {COLORS['neon_cyan']}60; }}
        50% {{ text-shadow: 0 0 25px {COLORS['neon_cyan']}AA, 0 0 50px {COLORS['neon_cyan']}50, 0 0 80px {COLORS['neon_cyan']}20; }}
    }}

    .neon-title {{
        animation: neonPulse 3s ease-in-out infinite;
    }}

    /* ---- Floating orb accents ---- */
    @keyframes floatOrb1 {{
        0%, 100% {{ transform: translate(0, 0) scale(1); opacity: 0.15; }}
        33% {{ transform: translate(30px, -20px) scale(1.1); opacity: 0.25; }}
        66% {{ transform: translate(-20px, 15px) scale(0.9); opacity: 0.1; }}
    }}
    @keyframes floatOrb2 {{
        0%, 100% {{ transform: translate(0, 0) scale(1); opacity: 0.1; }}
        50% {{ transform: translate(-40px, -30px) scale(1.15); opacity: 0.2; }}
    }}

    /* ---- Border glow animation for containers ---- */
    @keyframes borderGlow {{
        0%, 100% {{ border-color: {COLORS['neon_cyan']}30; box-shadow: 0 0 10px {COLORS['neon_cyan']}10; }}
        50% {{ border-color: {COLORS['magenta']}40; box-shadow: 0 0 20px {COLORS['magenta']}15; }}
    }}

    /* ---- Shimmer effect for loading states ---- */
    @keyframes shimmer {{
        0% {{ background-position: -200% center; }}
        100% {{ background-position: 200% center; }}
    }}

    /* ---- Button glow ---- */
    .stButton > button {{
        background: linear-gradient(135deg, {COLORS['neon_cyan']}20, {COLORS['magenta']}20) !important;
        border: 1px solid {COLORS['neon_cyan']}40 !important;
        color: {COLORS['neon_cyan']} !important;
        transition: all 0.3s ease !important;
        text-shadow: 0 0 8px {COLORS['neon_cyan']}60;
    }}
    .stButton > button:hover {{
        border-color: {COLORS['neon_cyan']}80 !important;
        box-shadow: 0 0 20px {COLORS['neon_cyan']}30, 0 0 40px {COLORS['magenta']}15 !important;
        transform: translateY(-1px);
    }}
</style>
"""


# ------------------------------------------------------------------
# Cached data-fetcher singletons
# ------------------------------------------------------------------

@st.cache_resource
def _get_cache() -> CacheManager:
    return CacheManager()


@st.cache_resource
def _get_price_fetcher() -> PriceFetcher:
    return PriceFetcher(cache=_get_cache())


@st.cache_resource
def _get_news_fetcher() -> NewsFetcher:
    return NewsFetcher(cache=_get_cache())


@st.cache_resource
def _get_sentiment_analyzer() -> SentimentAnalyzer:
    return SentimentAnalyzer()


# ------------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------------

def _render_sidebar() -> tuple[str, str]:
    """
    Draw the sidebar and return (selected_commodity_key, selected_timeframe).
    """
    with st.sidebar:
        st.markdown(
            _html(f"""
            <div style="text-align: center; padding: 16px 0 8px 0;">
                <span style="font-size: 2.2rem;">
                    \U0001f4c8\U0001f4f0
                </span>
                <div style="color: {COLORS['neon_cyan']}; font-size: 1.2rem;
                     font-weight: 800; margin-top: 4px;
                     text-shadow: 0 0 12px {COLORS['neon_cyan']}80;
                     letter-spacing: 1px;" class="neon-title">
                    COMMODITY PULSE
                </div>
                <div style="color: {COLORS['text_secondary']};
                     font-size: 0.78rem; margin-top: 2px;">
                    News &times; Price Correlation
                </div>
            </div>
            <hr style="border: none; border-top: 1px solid {COLORS['neon_cyan']}20;
                 margin: 12px 0 20px 0;">
            """),
            unsafe_allow_html=True,
        )

        # Commodity selector
        st.markdown(
            f"<div style='color:{COLORS['magenta']};font-weight:700;"
            f"font-size:0.85rem;margin-bottom:4px;'>"
            f"\U0001f50d SELECT COMMODITY</div>",
            unsafe_allow_html=True,
        )
        commodity_options = {
            key: f"{info['icon']} {info['name']}"
            for key, info in COMMODITIES.items()
        }
        selected_commodity = st.radio(
            "Commodity",
            options=list(commodity_options.keys()),
            format_func=lambda k: commodity_options[k],
            label_visibility="collapsed",
        )

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

        # Timeframe selector
        st.markdown(
            f"<div style='color:{COLORS['gold']};font-weight:700;"
            f"font-size:0.85rem;margin-bottom:4px;'>"
            f"\u23F0 TIMEFRAME</div>",
            unsafe_allow_html=True,
        )
        tf_options = {k: v["label"] for k, v in TIMEFRAME_OPTIONS.items()}
        selected_tf = st.radio(
            "Timeframe",
            options=list(tf_options.keys()),
            format_func=lambda k: tf_options[k],
            index=2,  # default to 30 Days
            label_visibility="collapsed",
        )

        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

        # Refresh button
        if st.button("\U0001f504 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

        # Footer
        st.markdown(
            _html(f"""
            <hr style="border: none; border-top: 1px solid {COLORS['neon_cyan']}15;
                 margin: 24px 0 12px 0;">
            <div style="color: {COLORS['text_secondary']}; font-size: 0.7rem;
                 text-align: center; opacity: 0.6;">
                Powered by yfinance &bull; GNews &bull; RSS<br>
                Built with Streamlit
            </div>
            """),
            unsafe_allow_html=True,
        )

    return selected_commodity, selected_tf


# ------------------------------------------------------------------
# Main content
# ------------------------------------------------------------------

def render_dashboard() -> None:
    """Top-level function: inject theme, render sidebar + main content."""

    # Inject custom CSS
    st.markdown(_CUSTOM_CSS, unsafe_allow_html=True)

    # Sidebar selections
    selected_commodity, selected_tf = _render_sidebar()
    commodity = COMMODITIES[selected_commodity]

    # Singletons
    price_fetcher = _get_price_fetcher()
    news_fetcher = _get_news_fetcher()

    # ---- Header with floating orbs ----
    st.markdown(
        _html(f"""
        <div style="position: relative; text-align: center; padding: 24px 0 12px 0;
             overflow: hidden;">
            <!-- Floating orb accents -->
            <div style="position: absolute; top: 10px; left: 15%;
                 width: 80px; height: 80px; border-radius: 50%;
                 background: radial-gradient(circle, {COLORS['neon_cyan']}20, transparent 70%);
                 animation: floatOrb1 8s ease-in-out infinite;
                 pointer-events: none;"></div>
            <div style="position: absolute; top: 5px; right: 20%;
                 width: 60px; height: 60px; border-radius: 50%;
                 background: radial-gradient(circle, {COLORS['magenta']}18, transparent 70%);
                 animation: floatOrb2 11s ease-in-out infinite;
                 pointer-events: none;"></div>
            <div style="position: absolute; bottom: 0; left: 45%;
                 width: 100px; height: 100px; border-radius: 50%;
                 background: radial-gradient(circle, {COLORS['electric_blue']}10, transparent 70%);
                 animation: floatOrb1 14s ease-in-out infinite reverse;
                 pointer-events: none;"></div>

            <span style="font-size: 3.2rem; display: inline-block;
                  animation: floatOrb2 4s ease-in-out infinite;">{commodity['icon']}</span>
            <h1 style="margin: 0; font-size: 2.2rem;
                 color: {COLORS['neon_cyan']};
                 text-shadow: 0 0 15px {COLORS['neon_cyan']}70, 0 0 40px {COLORS['neon_cyan']}30;
                 letter-spacing: 2px;"
                 class="neon-title">
                {commodity['name']}
            </h1>
            <p style="color: {COLORS['text_secondary']}; margin: 6px 0 0 0;
               font-size: 0.85rem;">
                Ticker: <span style="color: {COLORS['gold']};
                    text-shadow: 0 0 8px {COLORS['gold']}40;">{commodity['ticker']}</span>
                &nbsp;\u25C6&nbsp;
                Timeframe: <span style="color: {COLORS['magenta']};
                    text-shadow: 0 0 8px {COLORS['magenta']}40;">
                    {TIMEFRAME_OPTIONS[selected_tf]['label']}</span>
            </p>
        </div>
        """),
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # ---- Price overview (top row of cards) ----
    render_section_header("LIVE PRICES", "\U0001f4b0", COLORS["neon_green"])

    cols = st.columns(4)
    # Show selected commodity + 3 others for context
    display_keys = [selected_commodity] + [
        k for k in COMMODITIES if k != selected_commodity
    ][:3]

    price_dfs: dict[str, pd.DataFrame] = {}
    for col, key in zip(cols, display_keys):
        with col:
            info = COMMODITIES[key]
            price_data = price_fetcher.get_latest_price(info["ticker"])
            render_price_card(info, price_data)
            # Sparkline under each price card
            spark_df = price_fetcher.fetch_prices(info["ticker"], timeframe=selected_tf)
            if not spark_df.empty:
                price_dfs[key] = spark_df
                fig_spark = commodity_card_sparkline(
                    spark_df["Close"], key, color_idx=display_keys.index(key),
                )
                st.plotly_chart(
                    fig_spark, use_container_width=True,
                    config={"displayModeBar": False},
                )

    # ---- Price chart (Plotly) ----
    render_section_header("PRICE CHART", "\U0001f4c8", COLORS["electric_blue"])

    price_df = price_fetcher.fetch_prices(commodity["ticker"], timeframe=selected_tf)
    if not price_df.empty:
        chart_type = st.radio(
            "Chart style",
            ["line", "candlestick"],
            horizontal=True,
            label_visibility="collapsed",
        )
        plot_df = price_df.set_index("Date") if "Date" in price_df.columns else price_df
        fig = price_chart(plot_df, selected_commodity, chart_type=chart_type)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No price data available for this commodity and timeframe.")

    # ---- Multi-commodity price overlay ----
    if len(price_dfs) > 1:
        render_section_header("COMMODITY COMPARISON", "\u26A1", COLORS["purple"])
        overlay_dict = {}
        for k, df in price_dfs.items():
            overlay_dict[k] = df.set_index("Date") if "Date" in df.columns else df
        fig_overlay = multi_commodity_overlay(overlay_dict, normalize=True)
        st.plotly_chart(
            fig_overlay, use_container_width=True,
            config={"displayModeBar": False},
        )

    # ---- Fetch news & run sentiment analysis ----
    with st.spinner("Fetching news & analyzing sentiment..."):
        articles = news_fetcher.fetch_news(
            keywords=commodity["keywords"],
            rss_feeds=commodity["rss_feeds"],
            commodity_key=selected_commodity,
        )
        sentiment_analyzer = _get_sentiment_analyzer()
        sentiment_result = sentiment_analyzer.analyze(
            articles, commodity_keywords=commodity["keywords"]
        )

    # ---- Sentiment summary + gauge ----
    render_section_header("SENTIMENT ANALYSIS", "\U0001f9e0", COLORS["gold"])

    gauge_col, summary_col = st.columns([1, 2])
    with gauge_col:
        weighted_avg = sentiment_result["summary"].get("weighted_avg", 0.0)
        fig_gauge = sentiment_gauge(weighted_avg, f"{commodity['name']} Sentiment")
        st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})
    with summary_col:
        render_sentiment_summary(sentiment_result["summary"], commodity["name"])

    # ---- Correlation timeline (price vs sentiment) ----
    if not price_df.empty and sentiment_result.get("scored_articles"):
        render_section_header("PRICE vs SENTIMENT", "\u26A1", COLORS["neon_cyan"])
        scored = sentiment_result["scored_articles"]
        sent_records = []
        for art in scored:
            pub = art.get("published_date", "")
            score = art.get("sentiment_score")
            if pub and score is not None:
                try:
                    sent_records.append({"Date": pd.to_datetime(pub), "sentiment": score})
                except (ValueError, TypeError):
                    pass
        if sent_records:
            sent_df = pd.DataFrame(sent_records).set_index("Date").sort_index()
            # Resample to match price granularity (daily mean)
            sent_daily = sent_df.resample("D").mean().dropna()
            plot_price = price_df.set_index("Date") if "Date" in price_df.columns else price_df
            if not sent_daily.empty:
                fig_corr = correlation_timeline(plot_price, sent_daily, selected_commodity)
                st.plotly_chart(fig_corr, use_container_width=True, config={"displayModeBar": False})

    # ---- News feed (with sentiment scores) ----
    render_section_header("LATEST NEWS", "\U0001f4f0", COLORS["magenta"])
    render_news_feed(sentiment_result["scored_articles"])

    # ---- Sentiment heatmap & news volume (built from scored articles) ----
    scored_articles = sentiment_result.get("scored_articles", [])
    if scored_articles:
        daily_records: list[dict] = []
        for art in scored_articles:
            pub = art.get("published_date", "")
            score = art.get("sentiment_score")
            if pub and score is not None:
                try:
                    daily_records.append({
                        "date": pd.to_datetime(pub).strftime("%Y-%m-%d"),
                        "score": score,
                    })
                except (ValueError, TypeError):
                    pass

        if daily_records:
            rec_df = pd.DataFrame(daily_records)
            daily_agg = rec_df.groupby("date").agg(
                sentiment=("score", "mean"),
                count=("score", "count"),
            )

            # Sentiment heatmap (dates × selected commodity)
            render_section_header("SENTIMENT HEATMAP", "\U0001f525", COLORS["hot_pink"])
            heatmap_df = pd.DataFrame(
                {commodity["name"]: daily_agg["sentiment"]},
                index=daily_agg.index,
            )
            fig_heat = sentiment_heatmap(heatmap_df)
            st.plotly_chart(
                fig_heat, use_container_width=True,
                config={"displayModeBar": False},
            )

            # News volume chart
            render_section_header("NEWS VOLUME", "\U0001f4e1", COLORS["amber"])
            volume_df = pd.DataFrame(
                {commodity["name"]: daily_agg["count"]},
                index=daily_agg.index,
            )
            fig_vol = news_volume_chart(volume_df)
            st.plotly_chart(
                fig_vol, use_container_width=True,
                config={"displayModeBar": False},
            )
