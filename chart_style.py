"""
chart_style.py — one visual system for every chart in oil_gas_tools.

Import this at the top of each notebook, call apply_style() once, and then
stop making styling decisions. The helpers below cover the four patterns that
repeat across all six tools: seasonal bands, event markers, right-edge series
labels, and the source/as-of footer.

    import sys
    from pathlib import Path
    sys.path.append(str(Path.cwd().parent))

    import chart_style as cs
    cs.apply_style()

Design notes, and the reasoning behind every number here, are in
docs/chart_style.md.
"""

from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


# ----------------------------------------------------------------------------
# 1. PALETTE
# ----------------------------------------------------------------------------
# The Okabe-Ito colorblind-safe set. Validated on all pairs: worst-case
# separation is dE 11.0 under deuteranopia against a target of 8, and every
# color clears the lightness band and chroma floor. Do not add a sixth hue
# without re-validating -- see docs/chart_style.md.
#
# No hue family is off-limits in principle; the earlier set was replaced for
# look and for one measured defect, not because reds or purples are banned.
# Any replacement just has to clear the validator.

BLUE       = "#0072B2"   # slot 1
VERMILLION = "#D55E00"   # slot 2
GREEN      = "#009E73"   # slot 3
SKY        = "#56B4E9"   # slot 4
ROSE       = "#CC79A7"   # slot 5

# Non-series colors. These are never categorical slots.
GRAY       = "#5A5F66"   # neutral series: a benchmark, a prior year, "other"
INK        = "#1A1D21"   # primary text
INK_MUTED  = "#6B7076"   # secondary text, tick labels, footers
RULE       = "#D8DBDF"   # grid lines, spines
SURFACE    = "#FCFCFB"   # figure and axes background
BAND       = "#C9CDD2"   # seasonal range fill

# Fixed assignment order. Assign by position, never cycle, never reorder when
# a series is filtered out -- a color belongs to an entity, not to a rank.
CATEGORICAL = [BLUE, VERMILLION, GREEN, SKY, ROSE]

# ---- One hue per commodity, project-wide -----------------------------------
# A commodity keeps the same color in every tool, so Henry Hub is green in
# Tool 3, Tool 4 and Tool 5 alike. Assignment is global, not per-chart, which
# means no chart can ever contradict another.
#
# Hue is reserved for IDENTITY -- which thing this is. It is never also used
# to distinguish a series from something derived from that series. See
# LINE STYLES below.

COLOR_WTI        = BLUE         # US crude benchmark
COLOR_BRENT      = VERMILLION   # international crude benchmark
COLOR_HENRY_HUB  = GREEN        # US natural gas
COLOR_TTF        = SKY          # European gas
COLOR_JKM        = ROSE         # Asian LNG

# Derived or secondary quantities. These appear alone on their own panel, so
# they may reuse a hue without colliding.
COLOR_SPREAD     = GREEN        # Brent-WTI, crack spread, M1-M2
COLOR_INVENTORY  = BLUE         # crude stocks
COLOR_RIGS_OIL   = VERMILLION
COLOR_RIGS_GAS   = GREEN
COLOR_FIVE_YR    = GRAY


# ----------------------------------------------------------------------------
# LINE STYLES -- the second encoding channel
# ----------------------------------------------------------------------------
# Hue says WHICH commodity. Line style says WHAT KIND of series it is.
# A 50-day moving average of WTI is still WTI, so it keeps WTI's blue and
# takes the DERIVED dash. Giving it a new hue would encode "is a moving
# average" as though that were a different product.
#
#     ax.plot(x, wti,     color=cs.COLOR_WTI, **cs.PRIMARY,  label="WTI")
#     ax.plot(x, wti_ma,  color=cs.COLOR_WTI, **cs.DERIVED,  label="WTI 50d MA")

PRIMARY   = {"linestyle": "-",  "linewidth": 2.0, "alpha": 1.00}
DERIVED   = {"linestyle": "--", "linewidth": 1.6, "alpha": 0.90}
PROJECTED = {"linestyle": ":",  "linewidth": 1.6, "alpha": 0.85}
CONTEXT   = {"linestyle": "-",  "linewidth": 1.1, "alpha": 0.45}  # prior years

# Diverging pair, for polarity around a reference (above/below zero).
# Warm and cool poles with a neutral midpoint -- never a rainbow,
# never a hue at the midpoint.
DIVERGE_HIGH = BLUE
DIVERGE_LOW  = VERMILLION
DIVERGE_MID  = RULE

# Status colors. Reserved -- never reused as a series color.
GOOD     = "#1B7F4D"
WARNING  = "#B25C00"
CRITICAL = "#B3261E"


# ----------------------------------------------------------------------------
# 2. TYPOGRAPHY SCALE
# ----------------------------------------------------------------------------
# Four sizes, not six. Every size below is derived from BASE so the whole
# system scales by changing one number.

BASE = 10.0

SIZE_FIGURE_TITLE = BASE * 1.5   # 15.0  suptitle
SIZE_AXES_TITLE   = BASE * 1.2   # 12.0  per-panel title
SIZE_LABEL        = BASE * 1.0   # 10.0  axis labels
SIZE_TICK         = BASE * 0.95  #  9.5  tick labels, legend
SIZE_ANNOTATION   = BASE * 0.9   #  9.0  callouts, series labels, footer

# Segoe UI ships on every Windows install and is a clean humanist sans.
# matplotlib walks this list and uses the first one it finds, so the file
# still works on a machine that has none of them.
FONT_STACK = ["Segoe UI", "Inter", "Source Sans Pro", "DejaVu Sans"]


# ----------------------------------------------------------------------------
# 3. THE STYLE
# ----------------------------------------------------------------------------

def apply_style() -> None:
    """Set the rcParams baseline. Call once per notebook, after imports.

    Everything this sets is a default -- any individual call can still
    override it. The point is that it should rarely need to.
    """
    mpl.rcParams.update({
        # -- type ---------------------------------------------------------
        "font.family":        "sans-serif",
        "font.sans-serif":    FONT_STACK,
        "font.size":          BASE,
        "figure.titlesize":   SIZE_FIGURE_TITLE,
        "figure.titleweight": "semibold",
        "axes.titlesize":     SIZE_AXES_TITLE,
        "axes.titleweight":   "semibold",
        "axes.titlepad":      10,
        "axes.labelsize":     SIZE_LABEL,
        "axes.labelcolor":    INK,
        "axes.labelpad":      6,
        "xtick.labelsize":    SIZE_TICK,
        "ytick.labelsize":    SIZE_TICK,
        "legend.fontsize":    SIZE_TICK,
        "text.color":         INK,

        # -- surfaces -----------------------------------------------------
        "figure.facecolor":   SURFACE,
        "axes.facecolor":     SURFACE,
        "savefig.facecolor":  SURFACE,

        # -- spines: keep two, drop two -----------------------------------
        # The top and right spines enclose the data without carrying any
        # information. Removing them is the single biggest readability win.
        "axes.edgecolor":     RULE,
        "axes.linewidth":     0.8,
        "axes.spines.top":    False,
        "axes.spines.right":  False,

        # -- grid: horizontal only, behind the data -----------------------
        # Vertical gridlines on a time axis add noise; the x tick marks
        # already locate a date. Values need horizontal reference lines.
        "axes.grid":          True,
        "axes.grid.axis":     "y",
        "axes.axisbelow":     True,
        "grid.color":         RULE,
        "grid.linewidth":     0.7,
        "grid.alpha":         0.9,

        # -- ticks: short, muted, outward ---------------------------------
        "xtick.color":        INK_MUTED,
        "ytick.color":        INK_MUTED,
        "xtick.labelcolor":   INK_MUTED,
        "ytick.labelcolor":   INK_MUTED,
        "xtick.direction":    "out",
        "ytick.direction":    "out",
        "xtick.major.size":   4,
        "ytick.major.size":   4,
        "xtick.major.width":  0.8,
        "ytick.major.width":  0.8,

        # -- marks --------------------------------------------------------
        "lines.linewidth":    2.0,
        "lines.markersize":   5,
        "lines.solid_capstyle": "round",
        "patch.linewidth":    0,

        # -- legend: no box, it competes with the data --------------------
        "legend.frameon":     True,
        "legend.framealpha":  0.92,
        "legend.facecolor":   SURFACE,
        "legend.edgecolor":   RULE,
        "legend.borderpad":   0.6,
        "legend.handlelength": 1.6,
        "legend.labelspacing": 0.4,

        # -- output -------------------------------------------------------
        "figure.dpi":         110,
        "savefig.dpi":        150,
        "savefig.bbox":       "tight",
        "figure.autolayout":  False,   # we call fig.tight_layout() explicitly
    })

    # Make the default color cycle the categorical order, so a bare
    # ax.plot() with no color= still lands on-system.
    mpl.rcParams["axes.prop_cycle"] = mpl.cycler(color=CATEGORICAL)


# ----------------------------------------------------------------------------
# 4. HELPERS
# ----------------------------------------------------------------------------

def seasonal_band(ax, x, lo, hi, series, years=5, color=None, alpha=0.40):
    """Fill the historical range behind the current series.

    `series` is required and is not decoration: a band labelled only
    "5-yr range" leaves the reader asking "range of what?" when more than one
    line is on the axes. The label comes out as "WTI 5-yr range".

    Pass `color` to tint the band toward its series' hue -- worth doing
    whenever a chart carries more than one band. The default is neutral gray,
    which is right when there is only one.

    Drawn at zorder=1 so the data always sits on top of it.
    """
    if not series:
        raise ValueError(
            "seasonal_band needs a series name so the band's label says what "
            'it is the range of, e.g. series="WTI".'
        )

    return ax.fill_between(
        x, lo, hi,
        color=color if color is not None else BAND,
        alpha=alpha, linewidth=0, zorder=1,
        label=f"{series} {years}-yr range",
    )


def event_marker(ax, x, text, color=INK_MUTED, y=1.0, align="left"):
    """Mark a point in time with a rule and a label at the top of the axes.

    Deliberately draws NO fill. A one-sided shaded region starting at an
    event reads as a lopsided color jump -- if a period genuinely needs
    shading, use regime_span(), which requires both ends.
    """
    ax.axvline(x, color=color, linewidth=1.1, linestyle="--",
               alpha=0.8, zorder=2)

    offset = 4 if align == "left" else -4
    ax.annotate(
        text,
        xy=(x, y), xycoords=("data", "axes fraction"),
        xytext=(offset, -10), textcoords="offset points",
        ha=align, va="top",
        fontsize=SIZE_ANNOTATION, color=color,
        bbox=dict(boxstyle="round,pad=0.3", facecolor=SURFACE,
                  edgecolor="none", alpha=0.85),
        zorder=6,
    )


def regime_span(ax, x_start, x_end, label=None, color=BAND, alpha=0.30):
    """Shade a bounded period. Both ends are required, by design.

    This is the only shading helper. Passing an open-ended region is not
    supported -- see docs/chart_style.md, 'Shading has two ends'.
    """
    if x_start is None or x_end is None:
        raise ValueError(
            "regime_span needs both x_start and x_end. An open-ended fill "
            "reads as a one-sided color jump; use event_marker() instead."
        )

    ax.axvspan(x_start, x_end, color=color, alpha=alpha,
               linewidth=0, zorder=0)

    if label:
        mid = x_start + (x_end - x_start) / 2
        ax.annotate(
            label,
            xy=(mid, 1.0), xycoords=("data", "axes fraction"),
            xytext=(0, -10), textcoords="offset points",
            ha="center", va="top",
            fontsize=SIZE_ANNOTATION, color=INK_MUTED, zorder=6,
        )


def label_series(ax, entries, gutter=0.14, min_gap_pts=12):
    """Label each series at its right end, in reserved space outside the data.

    This is the fix for callouts landing on top of the lines. Instead of
    annotating in the plot area and hoping for the best, we widen the x-axis
    by `gutter` and write the labels into that empty margin, then nudge any
    two labels that would collide vertically.

    entries: list of (x_last, y_last, text, color)

    Returns nothing; mutates the axes.
    """
    if not entries:
        return

    x0, x1 = ax.get_xlim()
    ax.set_xlim(x0, x1 + (x1 - x0) * gutter)

    # Work in display pixels so the collision test matches what the eye sees,
    # not what the data units say. Only y is transformed -- x may be a
    # Timestamp, which the affine transform will not accept.
    placed = []
    for x, y, text, color in sorted(entries, key=lambda e: e[1]):
        y_px = ax.transData.transform((0.0, y))[1]

        # Walk upward until this label clears the one below it.
        y_adj = y_px
        while placed and (y_adj - placed[-1]) < min_gap_pts:
            y_adj = placed[-1] + min_gap_pts
        placed.append(y_adj)

        # Keep the anchor on the data point and nudge only the text, so the
        # label still reads as belonging to that line.
        ax.annotate(
            text,
            xy=(x, y), xycoords="data",
            xytext=(10, y_adj - y_px), textcoords="offset points",
            ha="left", va="center",
            fontsize=SIZE_ANNOTATION, color=color, fontweight="semibold",
            annotation_clip=False, zorder=5,
        )


def value_callout(ax, x, y, text, color=INK, dx=10, dy=10):
    """A single annotated point, with a leader line and an opaque backing.

    Use sparingly -- one or two per chart, for the number that matters.
    Never label every point.
    """
    ax.annotate(
        text,
        xy=(x, y), xycoords="data",
        xytext=(dx, dy), textcoords="offset points",
        ha="left" if dx >= 0 else "right", va="center",
        fontsize=SIZE_ANNOTATION, color=color, fontweight="semibold",
        bbox=dict(boxstyle="round,pad=0.35", facecolor=SURFACE,
                  edgecolor=RULE, linewidth=0.7, alpha=0.95),
        arrowprops=dict(arrowstyle="-", color=RULE, linewidth=0.9,
                        shrinkA=0, shrinkB=3),
        zorder=6,
    )
    ax.plot([x], [y], marker="o", markersize=5, color=color,
            markeredgecolor=SURFACE, markeredgewidth=1.4, zorder=6)


def footer(fig, source, asof, note=None):
    """Stamp the source and the as-of date on the figure.

    Every chart carries this. A chart without a date on it is a chart that
    will eventually be read as current when it isn't.
    """
    text = f"Source: {source}   |   Data as of {asof}"
    if note:
        text += f"   |   {note}"
    fig.text(0.0, -0.02, text, ha="left", va="top",
             fontsize=SIZE_ANNOTATION, color=INK_MUTED)


def money(decimals=2, unit="$"):
    """Tick formatter for prices: money() -> $69.42"""
    return FuncFormatter(lambda v, _: f"{unit}{v:,.{decimals}f}")


def thousands(suffix=""):
    """Tick formatter for large counts: thousands(' Bcf') -> 3,412 Bcf"""
    return FuncFormatter(lambda v, _: f"{v:,.0f}{suffix}")


def finish(fig, path=None, pad=1.1, tight=True):
    """Lay out and optionally save. Call this instead of plt.tight_layout().

    Keeps layout and save settings in one place so every chart in the repo
    is written the same way.
    """
    if tight:
       fig.tight_layout(pad=pad)
    if path is not None:
        fig.savefig(path)
    return fig


# ----------------------------------------------------------------------------
# 5. SELF-TEST
# ----------------------------------------------------------------------------

def _demo(path="chart_style_demo.png"):
    """Render a sample chart exercising every helper. Run this after editing
    anything above:  python chart_style.py
    """
    import numpy as np
    import pandas as pd

    apply_style()

    rng = np.random.default_rng(7)
    n = 220
    dates = pd.date_range("2026-01-01", periods=n, freq="D")
    wti = 70 + np.cumsum(rng.normal(0, 0.55, n))
    brent = wti + 4.2 + np.cumsum(rng.normal(0, 0.18, n))

    wti_ma = pd.Series(wti, index=dates).rolling(50).mean()
    brent_ma = pd.Series(brent, index=dates).rolling(50).mean()
    lo, hi = wti - 7, wti + 7

    fig, ax = plt.subplots(figsize=(11, 5.5))

    # Band names its series and is tinted toward that series' hue.
    seasonal_band(ax, dates, lo, hi, series="WTI", color=COLOR_WTI, alpha=0.13)

    # Hue = commodity. Line style = kind of series. Each MA keeps its
    # parent's color, so the eye groups them without a second hue.
    ax.plot(dates, wti,      color=COLOR_WTI,   **PRIMARY, zorder=3)
    ax.plot(dates, brent,    color=COLOR_BRENT, **PRIMARY, zorder=3)
    ax.plot(dates, wti_ma,   color=COLOR_WTI,   **DERIVED, zorder=2)
    ax.plot(dates, brent_ma, color=COLOR_BRENT, **DERIVED, zorder=2)

    regime_span(ax, dates[60], dates[95], label="OPEC+ cut")
    event_marker(ax, dates[150], "Inventory build")

    value_callout(ax, dates[-1], wti[-1], f"${wti[-1]:,.2f}", color=COLOR_WTI,
                  dx=-78, dy=-30)

    # Right-edge labels replace the legend for the four lines; the band still
    # needs one, so a single-entry legend carries it.
    label_series(ax, [
        (dates[-1], wti[-1],              "WTI",          COLOR_WTI),
        (dates[-1], brent[-1],            "Brent",        COLOR_BRENT),
        (dates[-1], wti_ma.iloc[-1],      "WTI 50d",      COLOR_WTI),
        (dates[-1], brent_ma.iloc[-1],    "Brent 50d",    COLOR_BRENT),
    ])

    ax.set_title("Crude benchmarks and 50-day averages")
    ax.set_ylabel("$ / bbl")
    ax.yaxis.set_major_formatter(money())

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[:1], labels[:1], loc="lower left")

    footer(fig, "EIA, CME via yfinance", "2026-10-10",
           note="chart_style.py self-test")
    finish(fig, path)
    print(f"wrote {path}")


if __name__ == "__main__":
    _demo()
