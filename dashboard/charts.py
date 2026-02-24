"""
Visually trippy Plotly charts for the Commodity News × Price Correlation
Dashboard.

Every chart here is designed to feel ALIVE — neon glowing lines, pulsing
gradients, cyberpunk radial gauges, and electric colour palettes on dark
backgrounds.  No corporate beige allowed.

Public API
----------
- price_chart(df, commodity_key, chart_type="line")  -> go.Figure
- sentiment_gauge(score, label)                      -> go.Figure
- correlation_timeline(price_df, sentiment_df)       -> go.Figure
- commodity_card_sparkline(prices, commodity_key)     -> go.Figure
- sentiment_heatmap(matrix_df)                       -> go.Figure
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from config.settings import COLORS
from config.commodities import COMMODITIES

# ---------------------------------------------------------------------------
# Extended neon palette (supplements config COLORS with extra cyber tones)
# ---------------------------------------------------------------------------
NEON = {
    "green": "#00ff88",
    "cyan": COLORS["neon_cyan"],       # #00FFFF
    "blue": "#00d4ff",
    "pink": "#ff006e",
    "magenta": COLORS["magenta"],      # #FF00FF
    "amber": "#ffbe0b",
    "purple": "#8338ec",
    "gold": COLORS["gold"],            # #FFD700
    "lime": COLORS["lime"],            # #00FF00
    "orange": COLORS["orange"],        # #FFA500
}

# Rotate these for multi-series traces so every line is a different neon hue.
NEON_CYCLE = [
    NEON["green"], NEON["cyan"], NEON["pink"], NEON["amber"],
    NEON["purple"], NEON["blue"], NEON["magenta"], NEON["gold"],
]

BG_DARK = "#0a0a0a"
BG_CARD = COLORS["bg_card"]       # #1A1A2E
BG_GRID = "rgba(255,255,255,0.04)"


# ═══════════════════════════════════════════════════════════════════════════
# Shared layout helper
# ═══════════════════════════════════════════════════════════════════════════

def _base_layout(title: str = "", height: int = 420) -> dict:
    """Return a dark‑mode Plotly layout dict with neon styling."""
    return dict(
        title=dict(
            text=title,
            font=dict(family="Orbitron, monospace", size=16, color=NEON["cyan"]),
            x=0.5,
        ),
        paper_bgcolor=BG_DARK,
        plot_bgcolor=BG_DARK,
        height=height,
        margin=dict(l=50, r=30, t=50, b=40),
        font=dict(family="Share Tech Mono, Fira Code, monospace", color="#d0d0d0", size=11),
        xaxis=dict(
            gridcolor=BG_GRID,
            zerolinecolor=BG_GRID,
            showgrid=True,
            gridwidth=1,
        ),
        yaxis=dict(
            gridcolor=BG_GRID,
            zerolinecolor=BG_GRID,
            showgrid=True,
            gridwidth=1,
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#aaa", size=10),
        ),
    )


# ═══════════════════════════════════════════════════════════════════════════
# 1. Price chart — Candlestick or glowing Line
# ═══════════════════════════════════════════════════════════════════════════

def price_chart(
    df: pd.DataFrame,
    commodity_key: str,
    chart_type: str = "line",
) -> go.Figure:
    """
    Parameters
    ----------
    df : DataFrame with columns ['Open','High','Low','Close'] and a
         DatetimeIndex (or 'Date' column).
    commodity_key : key in COMMODITIES dict.
    chart_type : "line" | "candlestick"
    """
    info = COMMODITIES.get(commodity_key, {})
    name = info.get("name", commodity_key.title())
    icon = info.get("icon", "")

    fig = go.Figure()

    dates = df.index if isinstance(df.index, pd.DatetimeIndex) else df.get("Date", df.index)

    if chart_type == "candlestick" and {"Open", "High", "Low", "Close"}.issubset(df.columns):
        fig.add_trace(go.Candlestick(
            x=dates,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            increasing_line_color=NEON["green"],
            increasing_fillcolor="rgba(0,255,136,0.25)",
            decreasing_line_color=NEON["pink"],
            decreasing_fillcolor="rgba(255,0,110,0.25)",
            name=name,
        ))
    else:
        # Neon glowing line — draw a wider translucent "glow" line behind
        close = df["Close"] if "Close" in df.columns else df.iloc[:, 0]

        # Glow layer (wide, transparent)
        fig.add_trace(go.Scatter(
            x=dates, y=close,
            mode="lines",
            line=dict(color=NEON["cyan"], width=8),
            opacity=0.15,
            showlegend=False,
            hoverinfo="skip",
        ))
        # Mid‑glow
        fig.add_trace(go.Scatter(
            x=dates, y=close,
            mode="lines",
            line=dict(color=NEON["cyan"], width=4),
            opacity=0.35,
            showlegend=False,
            hoverinfo="skip",
        ))
        # Core bright line
        fig.add_trace(go.Scatter(
            x=dates, y=close,
            mode="lines",
            line=dict(color=NEON["cyan"], width=1.8),
            name=name,
            hovertemplate="<b>%{x}</b><br>$%{y:,.2f}<extra></extra>",
        ))

        # Gradient fill to zero
        fig.add_trace(go.Scatter(
            x=dates, y=close,
            fill="tozeroy",
            fillcolor="rgba(0,255,255,0.06)",
            line=dict(width=0),
            showlegend=False,
            hoverinfo="skip",
        ))

    fig.update_layout(
        **_base_layout(f"{icon} {name} Price", height=400),
        xaxis_rangeslider_visible=False,
        yaxis_title="Price (USD)",
    )

    return fig


# ═══════════════════════════════════════════════════════════════════════════
# 2. Sentiment gauge — radial indicator that looks ALIVE
# ═══════════════════════════════════════════════════════════════════════════

def sentiment_gauge(score: float, label: str = "Sentiment") -> go.Figure:
    """
    Parameters
    ----------
    score : float in [-1, 1] (VADER compound score).
    label : display name.
    """
    # Map -1…1 to colour
    if score > 0.05:
        bar_color = NEON["green"]
        emoji = "🟢"
    elif score < -0.05:
        bar_color = NEON["pink"]
        emoji = "🔴"
    else:
        bar_color = NEON["amber"]
        emoji = "🟡"

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        number=dict(
            font=dict(size=36, color=bar_color, family="Orbitron, monospace"),
            valueformat="+.2f",
        ),
        title=dict(
            text=f"{emoji} {label}",
            font=dict(size=14, color="#cccccc", family="Share Tech Mono, monospace"),
        ),
        gauge=dict(
            axis=dict(
                range=[-1, 1],
                tickvals=[-1, -0.5, 0, 0.5, 1],
                ticktext=["-1", "-0.5", "0", "+0.5", "+1"],
                tickfont=dict(color="#666", size=10),
                dtick=0.5,
            ),
            bar=dict(color=bar_color, thickness=0.7),
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
            steps=[
                dict(range=[-1, -0.5], color="rgba(255,0,110,0.20)"),
                dict(range=[-0.5, -0.05], color="rgba(255,0,110,0.08)"),
                dict(range=[-0.05, 0.05], color="rgba(255,190,11,0.08)"),
                dict(range=[0.05, 0.5], color="rgba(0,255,136,0.08)"),
                dict(range=[0.5, 1], color="rgba(0,255,136,0.20)"),
            ],
            threshold=dict(
                line=dict(color=NEON["cyan"], width=3),
                thickness=0.85,
                value=score,
            ),
        ),
    ))

    fig.update_layout(
        paper_bgcolor=BG_DARK,
        plot_bgcolor=BG_DARK,
        height=250,
        margin=dict(l=30, r=30, t=60, b=20),
        font=dict(family="Share Tech Mono, monospace", color="#aaa"),
    )

    return fig


# ═══════════════════════════════════════════════════════════════════════════
# 3. Correlation timeline — sentiment overlay on price
# ═══════════════════════════════════════════════════════════════════════════

def correlation_timeline(
    price_df: pd.DataFrame,
    sentiment_df: pd.DataFrame,
    commodity_key: str = "",
) -> go.Figure:
    """
    Parameters
    ----------
    price_df : DataFrame with 'Close' column and DatetimeIndex.
    sentiment_df : DataFrame with 'sentiment' column and DatetimeIndex.
                   Values in [-1, 1].
    commodity_key : optional key for titling.
    """
    info = COMMODITIES.get(commodity_key, {})
    name = info.get("name", commodity_key.title()) if commodity_key else "Commodity"

    fig = go.Figure()

    dates_p = price_df.index if isinstance(price_df.index, pd.DatetimeIndex) else price_df.get("Date", price_df.index)
    close = price_df["Close"] if "Close" in price_df.columns else price_df.iloc[:, 0]

    # ----- Price axis (left) — neon cyan glow -----
    fig.add_trace(go.Scatter(
        x=dates_p, y=close,
        mode="lines",
        line=dict(color=NEON["cyan"], width=6),
        opacity=0.12,
        showlegend=False,
        hoverinfo="skip",
        yaxis="y",
    ))
    fig.add_trace(go.Scatter(
        x=dates_p, y=close,
        mode="lines",
        line=dict(color=NEON["cyan"], width=2),
        name="Price",
        hovertemplate="$%{y:,.2f}<extra>Price</extra>",
        yaxis="y",
    ))

    # ----- Sentiment axis (right) — neon pink / green -----
    dates_s = sentiment_df.index if isinstance(sentiment_df.index, pd.DatetimeIndex) else sentiment_df.get("Date", sentiment_df.index)
    sent = sentiment_df["sentiment"] if "sentiment" in sentiment_df.columns else sentiment_df.iloc[:, 0]

    # Colour each bar by sign
    bar_colors = [
        NEON["green"] if v > 0.05 else (NEON["pink"] if v < -0.05 else NEON["amber"])
        for v in sent
    ]

    fig.add_trace(go.Bar(
        x=dates_s, y=sent,
        marker_color=bar_colors,
        opacity=0.55,
        name="Sentiment",
        yaxis="y2",
        hovertemplate="%{y:+.2f}<extra>Sentiment</extra>",
    ))

    layout = _base_layout(f"⚡ {name} — Price vs Sentiment", height=380)
    layout["yaxis"] = dict(
        title=dict(text="Price (USD)", font=dict(color=NEON["cyan"])),
        tickfont=dict(color=NEON["cyan"], size=10),
        gridcolor=BG_GRID,
        side="left",
    )
    layout["yaxis2"] = dict(
        title=dict(text="Sentiment", font=dict(color=NEON["pink"])),
        tickfont=dict(color=NEON["pink"], size=10),
        overlaying="y",
        side="right",
        range=[-1.1, 1.1],
        gridcolor="rgba(0,0,0,0)",
    )
    fig.update_layout(
        **layout,
        barmode="overlay",
        hovermode="x unified",
    )

    return fig


# ═══════════════════════════════════════════════════════════════════════════
# 4. Commodity card sparkline — tiny glowing line for metric cards
# ═══════════════════════════════════════════════════════════════════════════

def commodity_card_sparkline(
    prices: pd.Series | list,
    commodity_key: str,
    color_idx: int = 0,
) -> go.Figure:
    """
    A miniature sparkline chart designed to sit inside a glowing commodity card.

    Parameters
    ----------
    prices : recent close prices (last ~30 values work best).
    commodity_key : key in COMMODITIES dict.
    color_idx : index into NEON_CYCLE for line colour.
    """
    if isinstance(prices, pd.Series):
        vals = prices.values
    else:
        vals = np.asarray(prices)

    color = NEON_CYCLE[color_idx % len(NEON_CYCLE)]

    # Determine trend
    trend_up = vals[-1] >= vals[0] if len(vals) > 1 else True
    fill_color = "rgba(0,255,136,0.10)" if trend_up else "rgba(255,0,110,0.10)"

    fig = go.Figure()

    # Glow
    fig.add_trace(go.Scatter(
        y=vals, mode="lines",
        line=dict(color=color, width=5),
        opacity=0.15,
        showlegend=False, hoverinfo="skip",
    ))
    # Core
    fig.add_trace(go.Scatter(
        y=vals, mode="lines",
        line=dict(color=color, width=1.5, shape="spline"),
        showlegend=False,
        hoverinfo="skip",
    ))
    # Fill
    fig.add_trace(go.Scatter(
        y=vals, fill="tozeroy",
        fillcolor=fill_color,
        line=dict(width=0),
        showlegend=False, hoverinfo="skip",
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=80,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )

    return fig


# ═══════════════════════════════════════════════════════════════════════════
# 5. Sentiment heatmap across all commodities
# ═══════════════════════════════════════════════════════════════════════════

def sentiment_heatmap(matrix_df: pd.DataFrame) -> go.Figure:
    """
    Parameters
    ----------
    matrix_df : DataFrame where rows = dates (or time buckets),
                columns = commodity names, values = sentiment scores [-1,1].
    """
    # Custom neon diverging colour scale (pink → dark → green)
    neon_scale = [
        [0.0,  NEON["pink"]],           # -1 extreme negative
        [0.25, "rgba(255,0,110,0.40)"],
        [0.45, BG_CARD],                # near-zero → dark
        [0.55, BG_CARD],
        [0.75, "rgba(0,255,136,0.40)"],
        [1.0,  NEON["green"]],          # +1 extreme positive
    ]

    fig = go.Figure(go.Heatmap(
        z=matrix_df.values,
        x=matrix_df.columns.tolist(),
        y=[str(d) for d in matrix_df.index],
        colorscale=neon_scale,
        zmin=-1, zmax=1,
        xgap=3, ygap=3,
        hovertemplate=(
            "<b>%{x}</b><br>"
            "%{y}<br>"
            "Sentiment: %{z:+.2f}"
            "<extra></extra>"
        ),
        colorbar=dict(
            title=dict(text="Sent.", font=dict(color="#888", size=11)),
            tickfont=dict(color="#888", size=10),
            tickvals=[-1, -0.5, 0, 0.5, 1],
            outlinewidth=0,
            bgcolor="rgba(0,0,0,0)",
        ),
    ))

    layout = _base_layout("🔥 Sentiment Heatmap", height=max(300, 30 * len(matrix_df) + 100))
    layout["xaxis"] = dict(
        tickangle=-45,
        tickfont=dict(color=NEON["cyan"], size=11),
        side="top",
    )
    layout["yaxis"] = dict(
        tickfont=dict(color="#888", size=10),
        autorange="reversed",
    )
    fig.update_layout(**layout)

    return fig


# ═══════════════════════════════════════════════════════════════════════════
# 6. Bonus: multi‑commodity overlay for comparison
# ═══════════════════════════════════════════════════════════════════════════

def multi_commodity_overlay(
    price_dict: dict[str, pd.DataFrame],
    normalize: bool = True,
) -> go.Figure:
    """
    Overlay multiple commodity price series on one chart.

    Parameters
    ----------
    price_dict : {commodity_key: DataFrame_with_Close_column, ...}
    normalize : if True, rebase all series to 100 at the start.
    """
    fig = go.Figure()

    for i, (key, df) in enumerate(price_dict.items()):
        info = COMMODITIES.get(key, {})
        name = info.get("name", key.title())
        color = NEON_CYCLE[i % len(NEON_CYCLE)]

        dates = df.index if isinstance(df.index, pd.DatetimeIndex) else df.get("Date", df.index)
        close = df["Close"] if "Close" in df.columns else df.iloc[:, 0]

        if normalize and len(close) > 0:
            base = close.iloc[0]
            series = (close / base) * 100 if base != 0 else close
        else:
            series = close

        # Glow
        fig.add_trace(go.Scatter(
            x=dates, y=series,
            mode="lines",
            line=dict(color=color, width=6),
            opacity=0.12,
            showlegend=False,
            hoverinfo="skip",
        ))
        # Core
        fig.add_trace(go.Scatter(
            x=dates, y=series,
            mode="lines",
            line=dict(color=color, width=2, shape="spline"),
            name=name,
            hovertemplate=f"<b>{name}</b><br>" + "%{y:.1f}<extra></extra>",
        ))

    ylabel = "Normalised (base=100)" if normalize else "Price (USD)"
    fig.update_layout(
        **_base_layout("⚡ Commodity Comparison", height=420),
        yaxis_title=ylabel,
        hovermode="x unified",
    )

    return fig


# ═══════════════════════════════════════════════════════════════════════════
# 7. News volume bar chart — electric stacked bars
# ═══════════════════════════════════════════════════════════════════════════

def news_volume_chart(volume_df: pd.DataFrame) -> go.Figure:
    """
    Parameters
    ----------
    volume_df : DataFrame where rows = dates, columns = commodity names,
                values = article counts.
    """
    fig = go.Figure()

    for i, col in enumerate(volume_df.columns):
        color = NEON_CYCLE[i % len(NEON_CYCLE)]
        fig.add_trace(go.Bar(
            x=volume_df.index,
            y=volume_df[col],
            name=col,
            marker_color=color,
            opacity=0.8,
            hovertemplate=f"<b>{col}</b><br>" + "%{y} articles<extra></extra>",
        ))

    fig.update_layout(
        **_base_layout("📡 News Volume", height=340),
        barmode="stack",
        yaxis_title="Articles",
        hovermode="x unified",
    )

    return fig
