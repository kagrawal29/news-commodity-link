"""
Reusable UI components for the dashboard.

Provides live price cards, a scrolling news feed, and metric displays
using the neon cyberpunk colour scheme defined in settings.
"""

from __future__ import annotations

import textwrap

import streamlit as st

from config.settings import COLORS


def _html(text: str) -> str:
    """Strip common leading whitespace so Markdown won't treat HTML as a code block."""
    return textwrap.dedent(text).strip()


# ------------------------------------------------------------------
# Price card
# ------------------------------------------------------------------

def render_price_card(commodity_info: dict, price_data: dict | None) -> None:
    """
    Display a glowing neon price card for a single commodity.

    Parameters
    ----------
    commodity_info : dict
        Entry from ``COMMODITIES`` (must have ``name``, ``icon``).
    price_data : dict | None
        Dict returned by ``PriceFetcher.get_latest_price()`` or ``None``
        if unavailable.
    """
    icon = commodity_info.get("icon", "")
    name = commodity_info.get("name", "Unknown")

    if price_data is None:
        st.markdown(
            _html(f"""
            <div style="
                background: linear-gradient(145deg, {COLORS['bg_card']}, #12122a);
                border: 1px solid {COLORS['neutral']}30;
                border-radius: 14px;
                padding: 22px;
                margin-bottom: 12px;
                text-align: center;
                position: relative;
                overflow: hidden;
            ">
                <div style="position: absolute; top: 0; left: 0; right: 0; height: 2px;
                     background: linear-gradient(90deg, transparent, {COLORS['neutral']}40, transparent);
                     animation: shimmer 2s ease-in-out infinite;
                     background-size: 200% 100%;"></div>
                <div style="font-size: 2rem; animation: floatOrb2 3s ease-in-out infinite;">{icon}</div>
                <div style="color: {COLORS['text_primary']}; font-size: 1.1rem;
                     font-weight: 700; margin-top: 4px;">{name}</div>
                <div style="color: {COLORS['neutral']}; font-size: 0.85rem;
                     margin-top: 8px;">Loading\u2026</div>
            </div>
            """),
            unsafe_allow_html=True,
        )
        return

    price = price_data["price"]
    change = price_data["change"]
    change_pct = price_data["change_pct"]

    is_positive = change >= 0
    arrow = "\u25B2" if is_positive else "\u25BC"
    change_color = COLORS["positive"] if is_positive else COLORS["negative"]
    glow_color = COLORS["neon_green"] if is_positive else COLORS["negative"]

    st.markdown(
        _html(f"""
        <div style="
            background: linear-gradient(145deg, {COLORS['bg_card']}, #0f0f28);
            border: 1px solid {glow_color}35;
            border-radius: 14px;
            padding: 22px;
            margin-bottom: 12px;
            text-align: center;
            position: relative;
            overflow: hidden;
            box-shadow: 0 0 20px {glow_color}15, inset 0 0 20px {glow_color}05;
            animation: borderGlow 4s ease-in-out infinite;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        " onmouseover="this.style.transform='translateY(-4px) scale(1.02)';
                       this.style.boxShadow='0 0 35px {glow_color}30, inset 0 0 25px {glow_color}10';"
           onmouseout="this.style.transform='translateY(0) scale(1)';
                      this.style.boxShadow='0 0 20px {glow_color}15, inset 0 0 20px {glow_color}05';">
            <!-- Animated top border beam -->
            <div style="position: absolute; top: 0; left: 0; right: 0; height: 2px;
                 background: linear-gradient(90deg, transparent, {glow_color}80, transparent);
                 animation: shimmer 3s ease-in-out infinite;
                 background-size: 200% 100%;"></div>
            <!-- Subtle corner orb -->
            <div style="position: absolute; top: -15px; right: -15px;
                 width: 50px; height: 50px; border-radius: 50%;
                 background: radial-gradient(circle, {glow_color}15, transparent 70%);
                 animation: floatOrb1 6s ease-in-out infinite;
                 pointer-events: none;"></div>

            <div style="font-size: 2.2rem; animation: floatOrb2 3.5s ease-in-out infinite;">
                {icon}
            </div>
            <div style="color: {COLORS['text_primary']}; font-size: 1.05rem;
                 font-weight: 700; margin-top: 4px; letter-spacing: 0.5px;">{name}</div>
            <div style="color: {COLORS['neon_cyan']}; font-size: 1.9rem;
                 font-weight: 800; margin-top: 10px;
                 text-shadow: 0 0 12px {COLORS['neon_cyan']}80, 0 0 25px {COLORS['neon_cyan']}30;">
                ${price:,.2f}
            </div>
            <div style="color: {change_color}; font-size: 0.95rem;
                 font-weight: 600; margin-top: 6px;
                 text-shadow: 0 0 8px {change_color}50;">
                {arrow} {change:+,.2f} ({change_pct:+.2f}%)
            </div>
        </div>
        """),
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------------
# News feed
# ------------------------------------------------------------------

def render_news_feed(articles: list[dict], max_items: int = 15) -> None:
    """
    Render a scrolling news feed with neon-styled cards.

    Parameters
    ----------
    articles : list[dict]
        News items (each must have ``title``, ``source``, ``published_date``,
        ``url``, and optionally ``description``).
    max_items : int
        Maximum number of articles to display.
    """
    if not articles:
        st.markdown(
            _html(f"""
            <div style="color: {COLORS['neutral']}; text-align: center;
                 padding: 40px 0; font-size: 1rem;">
                No news articles found. Try a different commodity or check back later.
            </div>
            """),
            unsafe_allow_html=True,
        )
        return

    # Scrollable container
    feed_html_parts: list[str] = []
    for article in articles[:max_items]:
        title = article.get("title", "Untitled")
        source = article.get("source", "Unknown")
        pub_date = article.get("published_date", "")
        url = article.get("url", "#")
        description = article.get("description", "")

        # Truncate description for card display
        if len(description) > 160:
            description = description[:157] + "..."

        # Format the date for display
        display_date = _format_date(pub_date)

        # Sentiment badge (if scored)
        sentiment_badge = ""
        sentiment_label = article.get("sentiment_label")
        sentiment_score = article.get("sentiment_score")
        if sentiment_label is not None:
            sent_color = _sentiment_color(sentiment_label)
            sent_icon = _sentiment_icon(sentiment_label)
            sentiment_badge = (
                f'<span style="background: {sent_color}20; '
                f'color: {sent_color}; padding: 2px 8px; '
                f'border-radius: 4px; font-size: 0.72rem; font-weight: 600; '
                f'margin-left: 6px;">'
                f'{sent_icon} {sentiment_score:+.2f}</span>'
            )

        # Border colour reflects sentiment
        border_color = COLORS["magenta"]
        if sentiment_label == "positive":
            border_color = COLORS["positive"]
        elif sentiment_label == "negative":
            border_color = COLORS["negative"]

        source_badge = (
            f'<span style="background: {COLORS["electric_blue"]}30; '
            f'color: {COLORS["electric_blue"]}; padding: 2px 8px; '
            f'border-radius: 4px; font-size: 0.75rem; font-weight: 600;">'
            f"{source}</span>"
        )

        feed_html_parts.append(
            f"""
            <a href="{url}" target="_blank" style="text-decoration: none; display: block;">
                <div style="
                    background: linear-gradient(135deg, {COLORS['bg_card']}, #0e0e24);
                    border-left: 3px solid {border_color};
                    border-radius: 10px;
                    padding: 14px 16px;
                    margin-bottom: 10px;
                    transition: all 0.3s ease;
                    box-shadow: 0 0 8px {border_color}08;
                    position: relative;
                    overflow: hidden;
                " onmouseover="this.style.background='linear-gradient(135deg, {COLORS['bg_highlight']}, #141430)';
                               this.style.boxShadow='0 0 18px {border_color}20';
                               this.style.transform='translateX(4px)';"
                   onmouseout="this.style.background='linear-gradient(135deg, {COLORS['bg_card']}, #0e0e24)';
                              this.style.boxShadow='0 0 8px {border_color}08';
                              this.style.transform='translateX(0)';">
                    <div style="display: flex; justify-content: space-between;
                         align-items: center; margin-bottom: 6px;">
                        <div>{source_badge}{sentiment_badge}</div>
                        <span style="color: {COLORS['text_secondary']};
                              font-size: 0.75rem;">{display_date}</span>
                    </div>
                    <div style="color: {COLORS['text_primary']};
                         font-size: 0.95rem; font-weight: 600;
                         line-height: 1.35;">{title}</div>
                    <div style="color: {COLORS['text_secondary']};
                         font-size: 0.8rem; margin-top: 6px;
                         line-height: 1.4;">{description}</div>
                </div>
            </a>
            """
        )

    scrollable_feed = _html(f"""
    <div style="
        max-height: 600px;
        overflow-y: auto;
        padding-right: 8px;
        scrollbar-width: thin;
        scrollbar-color: {COLORS['magenta']}40 transparent;
    ">
        {''.join(feed_html_parts)}
    </div>
    """)
    st.markdown(scrollable_feed, unsafe_allow_html=True)


# ------------------------------------------------------------------
# Section header
# ------------------------------------------------------------------

def render_section_header(title: str, icon: str = "", color: str | None = None) -> None:
    """Render an animated glowing section header with scanning beam."""
    c = color or COLORS["neon_cyan"]
    st.markdown(
        _html(f"""
        <div style="
            color: {c};
            font-size: 1.3rem;
            font-weight: 700;
            margin: 28px 0 12px 0;
            text-shadow: 0 0 12px {c}70, 0 0 25px {c}30;
            letter-spacing: 1px;
            text-transform: uppercase;
        ">
            <span style="display: inline-block; animation: floatOrb2 3s ease-in-out infinite;">
                {icon}
            </span> {title}
        </div>
        <div style="
            height: 2px;
            position: relative;
            background: linear-gradient(90deg, {c}60, {c}20, transparent);
            margin-bottom: 18px;
            border-radius: 1px;
            overflow: hidden;
        ">
            <div style="
                position: absolute; top: 0; left: -100%;
                width: 60%; height: 100%;
                background: linear-gradient(90deg, transparent, {c}FF, transparent);
                animation: sectionBeam 3s ease-in-out infinite;
            "></div>
        </div>
        <style>
            @keyframes sectionBeam {{
                0% {{ left: -60%; }}
                100% {{ left: 160%; }}
            }}
        </style>
        """),
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _format_date(date_str: str) -> str:
    """Best-effort human-friendly date string."""
    if not date_str:
        return ""
    try:
        from datetime import datetime
        dt = datetime.fromisoformat(date_str)
        return dt.strftime("%b %d, %H:%M")
    except (ValueError, TypeError):
        return date_str[:16]


def _sentiment_color(label: str) -> str:
    """Return the neon colour for a sentiment label."""
    return {
        "positive": COLORS["positive"],
        "negative": COLORS["negative"],
        "neutral": COLORS["neutral"],
    }.get(label, COLORS["neutral"])


def _sentiment_icon(label: str) -> str:
    """Return a small icon for a sentiment label."""
    return {"positive": "\u25B2", "negative": "\u25BC", "neutral": "\u25CF"}.get(
        label, "\u25CF"
    )


# ------------------------------------------------------------------
# Sentiment summary
# ------------------------------------------------------------------

def render_sentiment_summary(summary: dict, commodity_name: str = "") -> None:
    """
    Render a neon-styled sentiment overview panel.

    Parameters
    ----------
    summary : dict
        The ``summary`` key from ``SentimentAnalyzer.analyze()``.
    commodity_name : str
        Human-readable commodity name for display.
    """
    weighted_avg = summary.get("weighted_avg", 0.0)
    label = summary.get("label", "neutral")
    confidence = summary.get("confidence", 0.0)
    article_count = summary.get("article_count", 0)
    pos_pct = summary.get("positive_pct", 0.0)
    neg_pct = summary.get("negative_pct", 0.0)
    neu_pct = summary.get("neutral_pct", 0.0)

    sent_color = _sentiment_color(label)
    sent_icon = _sentiment_icon(label)

    # Confidence bar width
    conf_width = max(5, int(confidence * 100))

    st.markdown(
        _html(f"""
        <div style="
            background: linear-gradient(145deg, {COLORS['bg_card']}, #0d0d22);
            border: 1px solid {sent_color}30;
            border-radius: 14px;
            padding: 26px;
            margin-bottom: 16px;
            box-shadow: 0 0 25px {sent_color}12, inset 0 0 25px {sent_color}04;
            animation: borderGlow 5s ease-in-out infinite;
            position: relative;
            overflow: hidden;
        ">
            <!-- Animated top beam -->
            <div style="position: absolute; top: 0; left: 0; right: 0; height: 2px;
                 background: linear-gradient(90deg, transparent, {sent_color}60, transparent);
                 animation: shimmer 4s ease-in-out infinite;
                 background-size: 200% 100%;"></div>

            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 20px;">

                <!-- Main score -->
                <div style="text-align: center; min-width: 140px;">
                    <div style="color: {COLORS['text_secondary']}; font-size: 0.75rem;
                         text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 6px;">
                        Overall Sentiment
                    </div>
                    <div style="color: {sent_color}; font-size: 2.6rem; font-weight: 800;
                         text-shadow: 0 0 20px {sent_color}70, 0 0 40px {sent_color}30;
                         animation: neonPulse 3s ease-in-out infinite;">
                        {sent_icon} {weighted_avg:+.2f}
                    </div>
                    <div style="color: {sent_color}; font-size: 0.85rem; font-weight: 600;
                         text-transform: uppercase; margin-top: 4px;
                         letter-spacing: 2px;">
                        {label}
                    </div>
                </div>

                <!-- Distribution -->
                <div style="min-width: 180px;">
                    <div style="color: {COLORS['text_secondary']}; font-size: 0.75rem;
                         text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 10px;">
                        Distribution ({article_count} articles)
                    </div>
                    <div style="display: flex; height: 10px; border-radius: 5px; overflow: hidden;
                         background: {COLORS['bg_highlight']}; margin-bottom: 8px;
                         box-shadow: inset 0 0 6px rgba(0,0,0,0.4);">
                        <div style="width: {pos_pct}%; background: linear-gradient(90deg, {COLORS['positive']}80, {COLORS['positive']});
                             box-shadow: 0 0 8px {COLORS['positive']}40;"></div>
                        <div style="width: {neu_pct}%; background: {COLORS['neutral']};"></div>
                        <div style="width: {neg_pct}%; background: linear-gradient(90deg, {COLORS['negative']}, {COLORS['negative']}80);
                             box-shadow: 0 0 8px {COLORS['negative']}40;"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.75rem;">
                        <span style="color: {COLORS['positive']}; text-shadow: 0 0 6px {COLORS['positive']}40;">\u25B2 {pos_pct:.0f}%</span>
                        <span style="color: {COLORS['neutral']};">\u25CF {neu_pct:.0f}%</span>
                        <span style="color: {COLORS['negative']}; text-shadow: 0 0 6px {COLORS['negative']}40;">\u25BC {neg_pct:.0f}%</span>
                    </div>
                </div>

                <!-- Confidence -->
                <div style="min-width: 140px;">
                    <div style="color: {COLORS['text_secondary']}; font-size: 0.75rem;
                         text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 10px;">
                        Signal Confidence
                    </div>
                    <div style="color: {COLORS['neon_cyan']}; font-size: 1.8rem; font-weight: 700;
                         text-shadow: 0 0 12px {COLORS['neon_cyan']}70, 0 0 30px {COLORS['neon_cyan']}30;">
                        {confidence:.0%}
                    </div>
                    <div style="height: 8px; border-radius: 4px; background: {COLORS['bg_highlight']};
                         margin-top: 8px; overflow: hidden; box-shadow: inset 0 0 6px rgba(0,0,0,0.4);">
                        <div style="width: {conf_width}%; height: 100%;
                             background: linear-gradient(90deg, {COLORS['neon_cyan']}, {COLORS['magenta']});
                             border-radius: 4px;
                             box-shadow: 0 0 10px {COLORS['neon_cyan']}50;
                             animation: shimmer 3s ease-in-out infinite;
                             background-size: 200% 100%;"></div>
                    </div>
                </div>

            </div>
        </div>
        """),
        unsafe_allow_html=True,
    )
