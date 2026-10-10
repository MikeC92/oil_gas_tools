# Chart style

The visual system for every chart in this repo, and the reasoning behind it.

Companion file: `chart_style.py` at the project root.

---

## 1. Why a style file exists at all

The six notebooks produced fourteen charts. Before this file, those charts carried
**99 inline `fontsize=` arguments across six different values**, 49 `fontweight=`
arguments, one `tight_layout()` call, and `seaborn-v0_8-darkgrid` as the only shared
decision. Every chart had been styled by hand, separately, by eye.

That is the problem this file solves, and the problem has a name: **separation of
concerns.** A plotting cell should answer *what am I showing?* It should not also
answer *what size is a tick label?* Those are different questions, they change at
different rates, and mixing them means the second question gets re-answered — slightly
differently — every time you write a chart.

So the system splits in two:

| Lives in `chart_style.py` | Lives in the notebook |
|---|---|
| Colors, fonts, sizes, spines, grid | Which series to plot |
| How a seasonal band looks | What the band's values are |
| How an event marker is drawn | Which events matter |
| Where labels go and how they avoid collisions | What the labels say |
| Output dpi, background, layout | The title and the takeaway |

The left column is **configuration**. The right column is **content**. The left
column changes once and propagates to fourteen charts. That propagation is the whole
point — it's why changing one hex value in section 3 below fixes a colorblindness
defect everywhere at once, instead of in fourteen places you have to remember to find.

### Where it sits in the repo

```
oil_gas_tools/
├── config.py          ← secrets        (gitignored)
├── chart_style.py     ← presentation   (committed)
├── notebooks/         ← logic
├── data/              ← state          (gitignored)
└── charts/            ← output         (gitignored)
```

Four root-level concerns, each in its own place. `chart_style.py` imports nothing from
the project and nothing in the project imports from it except notebooks — it's a leaf.
That means you can edit it without fear of breaking anything upstream, and you can
delete a notebook without affecting it.

The import pattern is the same one `config.py` already uses:

```python
import sys
from pathlib import Path
sys.path.append(str(Path.cwd().parent))

import chart_style as cs
cs.apply_style()
```

### If you've used Tableau, Shiny, or Excel, you've already met this idea

You have done this before under other names:

- **Tableau** — a workbook *theme* plus a custom color palette defined in
  `Preferences.tps`. You set the palette once and every worksheet in the workbook
  draws from it. `apply_style()` is `Preferences.tps`; the semantic aliases
  (`COLOR_WTI`) are a Tableau custom palette with named members.
- **R Shiny** — `bslib::bs_theme()` and a CSS file. You don't set a font size on each
  `plotOutput`; you set it once on the theme and the app inherits. `rcParams` is
  matplotlib's theme object, and it works by exactly the same inheritance logic:
  a default that any individual call may override, but rarely needs to.
- **Excel** — a chart template (`.crtx`) and the workbook's theme colors. Same
  concept, same benefit, much weaker tooling.
- **ggplot2**, if you get to it at work — `theme_set()` and `scale_color_manual()`.
  The closest analogue of all, because ggplot's grammar makes the config/content
  split explicit in a way matplotlib doesn't.

The reason this pattern keeps reappearing is that it's the right answer. Any system
that produces more than about three visuals converges on it.

---

## 2. The thing worth understanding about matplotlib specifically

matplotlib has two APIs layered on each other, and mixing them is the source of most
confusion:

- **`plt.something()`** — the stateful, MATLAB-inherited API. `plt.plot()` draws on
  "the current axes," wherever that happens to be. Convenient for one quick chart,
  bad for anything with panels.
- **`fig, ax = plt.subplots()`** then **`ax.something()`** — the object API. You hold
  references to the figure and the axes and call methods on them explicitly.

**This repo uses the object API everywhere.** Every helper in `chart_style.py` takes
an `ax` as its first argument for that reason. It's more typing and it's worth it:
the moment you have two panels, the stateful API stops being able to express what you
mean.

The object hierarchy, which is worth holding in your head:

```
Figure                     the whole canvas; owns dpi, background, suptitle, savefig
└── Axes                   one plot panel; owns title, limits, spines, grid, legend
    ├── Axis (x, y)        one dimension; owns ticks, tick labels, formatter, scale
    ├── Line2D / Patch     the marks — what you actually drew
    └── Text / Annotation  labels, callouts, titles
```

`rcParams` sets defaults for all of these at once. When `apply_style()` sets
`"axes.spines.top": False`, it's reaching into every Axes created afterward. Note the
*afterward* — rcParams are read at creation time, so `apply_style()` must run before
`plt.subplots()`, which is why it goes in the imports cell.

---

## 3. The palette

```
#0072B2  BLUE        slot 1
#D55E00  VERMILLION  slot 2
#009E73  GREEN       slot 3
#56B4E9  SKY         slot 4
#CC79A7  ROSE        slot 5

#5A5F66  GRAY        neutral — benchmarks, prior years, "other". Not a slot.
```

This is the **Okabe–Ito** palette, designed for colorblind safety and standard in
scientific publishing. It replaced the previous set (`#E8593C` red-orange, `#185FA5`
blue, `#5F5E5A` gray, `#BA7517` amber, `#1D9E75` green, `#7F77DD` violet).

**No hue family is off-limits.** The old set went for two reasons — its look wasn't
preferred, and it carried one measured defect (below). Neither reason generalizes to
"reds and purples are banned." If a future palette wants a deep red or a violet, the
only hard requirement is that the whole set clears the validator. Treat the colors
below as the current answer, not a permanent one.

### Why it changed, measured rather than argued

The old palette was run through a validator that computes perceptual distance in
OKLab, simulating three kinds of color vision deficiency. Results on all pairs:

| Check | Old palette | New palette |
|---|---|---|
| Lightness band | PASS | PASS |
| Chroma floor | PASS | PASS |
| **CVD separation (all pairs)** | **FAIL — ΔE 3.2** | PASS — ΔE 11.0 |
| **Normal-vision separation** | **FAIL — ΔE 10.7** | PASS — ΔE 16.4 |
| Contrast vs surface | PASS | PASS (2 WARN) |

The failing pair was amber `#BA7517` against red-orange `#E8593C`. Under
deuteranopia — the most common color vision deficiency, roughly 6% of men — their
perceptual distance was **3.2**, against a target of 8. They were effectively the same
color. On any chart where both appeared, one series was invisible to those readers.
Under full color vision the distance was 10.7, below the floor of 15; even readers
with no deficiency would struggle.

**The lesson is the method, not the palette.** Nobody can eyeball ΔE in OKLab space.
Palettes that look fine to the person who picked them routinely fail, because the
person picking has normal color vision and is looking at large swatches rather than
two-pixel lines. The fix is to compute it.

### One hue per commodity, assigned project-wide

```python
COLOR_WTI       = BLUE         # US crude benchmark
COLOR_BRENT     = VERMILLION   # international crude benchmark
COLOR_HENRY_HUB = GREEN        # US natural gas
COLOR_TTF       = SKY          # European gas
COLOR_JKM       = ROSE         # Asian LNG
```

Assignment is **global, not per-chart**. Henry Hub is green in Tool 3, Tool 4 and
Tool 5 alike, so no two charts in the repo can contradict each other and you build a
reading habit across the whole suite.

### Rules that come with it

- **Assign by entity, never cycle.** A sixth series does not get a generated sixth
  color — it folds into "Other," or the chart becomes small multiples.
- **Color belongs to an entity, not a rank.** If you filter out Brent, WTI stays blue.
  It does not get promoted because it's now first.
- **Status colors are reserved.** `GOOD`, `WARNING`, `CRITICAL` never double as series
  colors, and they always ship with a word, never color alone.
- **Adding a sixth hue requires re-validating.** The all-pairs constraint gets
  quadratically harder with each addition. Five is near the practical limit for lines
  on one axis.

---

## 3a. Two channels: hue and line style

An earlier draft of this file gave WTI `BLUE` and Brent `SKY` — two blues, on the
theory that related commodities should read as related hues. That was wrong, and the
reason it was wrong is worth keeping.

**Ask what happens when you add a 50-day moving average for each.** The blue family is
already spent distinguishing WTI from Brent, so the MA can't be a lighter blue. It
would have to take a new hue — green, say. But green already means "a different
commodity." You'd be using the hue channel to encode *"this is a moving average,"*
which is not a commodity at all. One channel, two incompatible jobs.

So the system splits them:

| Channel | Encodes | Values |
|---|---|---|
| **Hue** | *which thing* — identity | one color per commodity, fixed project-wide |
| **Line style** | *what kind of series* | `PRIMARY` `DERIVED` `PROJECTED` `CONTEXT` |

```python
PRIMARY   = {"linestyle": "-",  "linewidth": 2.0, "alpha": 1.00}  # the series
DERIVED   = {"linestyle": "--", "linewidth": 1.6, "alpha": 0.90}  # MA, smoothed
PROJECTED = {"linestyle": ":",  "linewidth": 1.6, "alpha": 0.85}  # futures, forecast
CONTEXT   = {"linestyle": "-",  "linewidth": 1.1, "alpha": 0.45}  # prior years
```

A 50-day average of WTI *is still WTI*, so it keeps WTI's blue and takes the dash:

```python
ax.plot(x, wti,    color=cs.COLOR_WTI, **cs.PRIMARY, zorder=3)
ax.plot(x, wti_ma, color=cs.COLOR_WTI, **cs.DERIVED, zorder=2)
```

This scales. Five commodities × four series kinds is twenty distinguishable lines from
five hues, and the grouping is read instantly — same color means same commodity, dash
means derived — without anyone consulting a legend.

**The general principle, worth carrying beyond this repo:** a visual channel encodes
one data dimension. When you find yourself wanting a channel to carry a second
dimension, that's the signal to reach for a *different* channel — line style, weight,
opacity, marker shape, position, a separate panel — not to subdivide the one you've
already assigned. It's the same error as a dual-axis chart, one level down.

### The gas storage problem

Tool 3 plots six regions. Six lines on one axis cannot be made readable by any
palette — this is a *form* problem, not a color problem. The right answer there is
**small multiples**: six small panels sharing a y-scale, each with one line, the other
five ghosted behind it in `RULE` gray for context. That's on the list for step 3.

---

## 4. Typography

Four sizes, all derived from one base so the whole system scales by changing a single
number:

```python
BASE = 10.0

SIZE_FIGURE_TITLE = BASE * 1.5   # 15.0
SIZE_AXES_TITLE   = BASE * 1.2   # 12.0
SIZE_LABEL        = BASE * 1.0   # 10.0
SIZE_TICK         = BASE * 0.95  #  9.5
SIZE_ANNOTATION   = BASE * 0.9   #  9.0
```

The previous charts used 9, 10, 11, 12, 13 and 15 with no relationship between them.
Six arbitrary sizes read as six arbitrary decisions. A ratio-derived scale reads as
one decision, which is why typographic scales exist at all.

**Font stack:** `["Segoe UI", "Inter", "Source Sans Pro", "DejaVu Sans"]`. matplotlib
walks the list and uses the first one present. Segoe UI ships on every Windows install
— clean, humanist, unremarkable in the way a chart font should be. The DejaVu Sans
fallback is matplotlib's default, so the file never breaks on a machine with none of
the others.

**Text wears text colors, never series colors** — with one exception. Values, axis
labels and titles are `INK` or `INK_MUTED`. The exception is the right-edge series
labels, which take their line's color precisely because they're acting as the legend.

---

## 5. Surfaces, spines and grid

```
Surface  #FCFCFB   figure and axes background — near-white, not pure white
Rule     #D8DBDF   grid lines and spines
Ink      #1A1D21   primary text
Muted    #6B7076   ticks, secondary text, footers
```

**Spines: keep left and bottom, drop top and right.** The top and right spines enclose
the data without carrying any information. Removing them is the single largest
readability gain available for near-zero effort.

**Grid: horizontal only, behind the data.** On a time axis the x tick marks already
locate a date; vertical gridlines add noise. Values need horizontal reference lines to
be read off the axis, so those stay. `axes.axisbelow: True` puts the whole grid behind
the marks — without it, gridlines draw *over* your lines, which is the single most
common matplotlib ugliness.

**What `seaborn-v0_8-darkgrid` was doing wrong:** a gray panel with white gridlines.
It's a style with an opinion, and that opinion competes with your data for attention.
Every color you place on it has to fight a mid-gray background for contrast. The
replacement is deliberately boring — a near-white surface and recessive gray rules —
so the data is the only thing with any visual weight.

---

## 6. Three rules that came from real complaints

### Labels go beside the data, never on it

Reading a WTI price off the old charts was impractical — callouts landed on top of the
lines, sometimes in a matching color.

The fix is `label_series()`. Rather than annotating inside the plot area and hoping,
it **widens the x-axis by 14% and writes labels into that reserved margin**, then
converts each label's position to display pixels, walks any colliding pair apart by a
minimum gap, and nudges the text — keeping the anchor on the data point so the label
still reads as belonging to its line.

That pixel detail matters. Collisions happen in *screen space*, not data space. Two
lines 50 cents apart collide on a chart spanning $10 and don't on one spanning $200.
Testing in data units gets it wrong at some zoom level; testing in pixels can't.

For a single emphasized number, `value_callout()` draws a leader line to an opaque
rounded box. Use it once or twice per chart. **Never label every point** — that's not
a chart with labels, it's a table pretending to be a chart.

Note: `label_series()` and a legend do the same job. Use one. Right-edge labels are
generally better for time series because the eye doesn't have to travel to a legend
box and back.

### Shading has two ends

A fill that begins at an event and runs to the right edge reads as a lopsided color
jump — the eye sees an arbitrary boundary on one side and none on the other.

So the module offers two helpers and no third option:

- **`event_marker()`** — a dashed vertical rule and a label at the top. No fill. This
  is the default for "this happened here."
- **`regime_span()`** — shades a period, and **raises `ValueError` if either end is
  missing.** An open-ended span isn't an option you have to resist; it's an option
  that doesn't exist.

This extends decision D7 in `decisions.md`, which replaced a shaded region with a line
for the same reason, into a rule the code enforces.

### A band has to say what it's a range of

"5-yr range" in a legend, on a chart carrying two price lines, leaves the reader asking
*range of what?* So `seasonal_band()` **requires a `series` argument** and builds the
label from it — "WTI 5-yr range". Omitting it raises `ValueError` rather than
silently producing an ambiguous legend entry.

When a chart carries more than one band, pass `color=` to tint each toward its
series' hue at low alpha. One band on a chart can stay neutral gray.

```python
cs.seasonal_band(ax, x, lo, hi, series="WTI", color=cs.COLOR_WTI, alpha=0.13)
```

The same logic applies to axis labels: `ax.set_ylabel("$ / bbl")` costs nothing and
answers a question the reader would otherwise have to infer. A time axis rarely needs
an x-label — the tick labels are dates — but a value axis always needs units.

### Never two y-axes

`twinx()` appears twice in the current notebooks. Both should go.

A dual-axis chart lets you make any two series appear correlated by choosing the
scales — which means the reader can't trust the apparent relationship, because it's a
property of your axis choice rather than the data. It is the most commonly cited
mistake in data visualization for exactly this reason.

The three honest alternatives:

1. **Two stacked panels** sharing the x-axis. Almost always the right answer.
2. **Index both series to a common base** (first value = 100) and use one axis. Right
   when the question is *relative* movement.
3. **Plot the derived quantity** — if you want rigs against price, plot the ratio, or
   plot one against the other as a scatter with time as a color ramp.

---

## 7. Helper reference

| Helper | Does |
|---|---|
| `apply_style()` | Sets all rcParams. Call once, before `plt.subplots()`. |
| `PRIMARY` / `DERIVED` / `PROJECTED` / `CONTEXT` | Line-style kwargs; splat with `**` |
| `seasonal_band(ax, x, lo, hi, series)` | Range fill at `zorder=1`; `series` required |
| `event_marker(ax, x, text)` | Dashed rule + top label, no fill |
| `regime_span(ax, start, end, label)` | Bounded shading; both ends required |
| `label_series(ax, entries)` | Right-edge labels in reserved margin, de-collided |
| `value_callout(ax, x, y, text)` | One emphasized point with a leader line |
| `footer(fig, source, asof, note)` | Source + as-of stamp |
| `money()` / `thousands()` | Tick formatters |
| `finish(fig, path)` | `tight_layout()` + `savefig()` in one place |

Every helper takes `ax` or `fig` first — object API, as in section 2.

### The footer is not optional

`footer()` stamps the source and the as-of date on every chart. A chart without a date
on it will eventually be read as current when it isn't — which is the same failure
class as the stale cell outputs that made Tool 2 show $90 WTI against a $69 market.
A date in the corner is the cheapest guard available against that.

### Self-test

```bash
python chart_style.py
```

Renders `chart_style_demo.png` exercising every helper on synthetic data. **Run it
after editing anything in the file.** It has already paid for itself once: it caught a
crash where a pandas `Timestamp` was passed into matplotlib's affine transform, and a
second bug where the collision-avoidance math computed an adjustment it never applied.
Both would otherwise have surfaced as a confusing failure inside a notebook.

---

## 8. Using it in a notebook

```python
# --- imports cell -----------------------------------------------------------
import sys
from pathlib import Path
sys.path.append(str(Path.cwd().parent))

import matplotlib.pyplot as plt
import chart_style as cs

cs.apply_style()          # before any figure is created

# --- plotting cell ----------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 5.5))

cs.seasonal_band(ax, df.index, df["lo"], df["hi"],
                 series="WTI", color=cs.COLOR_WTI, alpha=0.13)

ax.plot(df.index, df["wti"],    color=cs.COLOR_WTI,   **cs.PRIMARY, zorder=3)
ax.plot(df.index, df["brent"],  color=cs.COLOR_BRENT, **cs.PRIMARY, zorder=3)
ax.plot(df.index, df["wti_ma"], color=cs.COLOR_WTI,   **cs.DERIVED, zorder=2)

cs.event_marker(ax, pd.Timestamp("2026-06-08"), "Hormuz closure")

cs.label_series(ax, [
    (df.index[-1], df["wti"].iloc[-1],    "WTI",     cs.COLOR_WTI),
    (df.index[-1], df["brent"].iloc[-1],  "Brent",   cs.COLOR_BRENT),
    (df.index[-1], df["wti_ma"].iloc[-1], "WTI 50d", cs.COLOR_WTI),
])

ax.set_title("Crude benchmarks vs five-year seasonal range")
ax.set_ylabel("$ / bbl")
ax.yaxis.set_major_formatter(cs.money())

cs.footer(fig, "EIA, CME via yfinance", str(df.index[-1].date()))
cs.finish(fig, CHARTS_DIR / "wti_brent.png")
```

Note what is *absent*: no `fontsize`, no `fontweight`, no color hex, no
`tight_layout()`, no `savefig()` kwargs, no spine or grid handling. All of it moved
into the style file. The cell now says only what it's showing.

**`zorder=3` on the data lines is worth keeping** — it puts them above the band
(`zorder=1`) and the regime span (`zorder=0`), below the annotations (`zorder=5-6`).
That stack is the layering contract of the whole system.

---

## 9. When you add a tool

1. Import and `apply_style()`. Don't set a font size.
2. Use a commodity alias (`COLOR_HENRY_HUB`) if one fits; add one to `chart_style.py`
   if the commodity is new. Don't paste a hex into a notebook.
3. A moving average, a forecast, a prior year? **Same hue as its parent**, with
   `**DERIVED`, `**PROJECTED` or `**CONTEXT`. Never a new hue.
4. Needs a sixth *commodity* color? Stop — small multiples, or fold into "Other."
5. Tempted by `twinx()`? Two panels instead.
6. Marking a period? `regime_span()`, with both ends.
7. Band? Name its series. Value axis? Give it units.
8. `footer()` before `finish()`.
9. Run `python chart_style.py` if you touched the style file.
