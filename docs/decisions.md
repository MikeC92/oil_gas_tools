# Decisions

Why things are the way they are. Each entry records the choice, the reasoning, and
what was rejected — so a future session doesn't "fix" something that was deliberate.

**Add an entry when a non-obvious choice is made.**

---

## D1 — Build cell by cell in chat, not as finished notebooks

**Decision:** code is handed over in reviewable pieces and typed manually, with a
plain-text cell-by-cell outline written before each tool.

**Why:** in the owner's words — *"I'd prefer to have the chance to type the code
manually even if I run into errors simply for the slower pace to force
learning/thinking about code structure and design."*

**Rejected:** generating complete `.ipynb` files. It was also technically brittle —
JSON notebook assembly repeatedly failed on unicode em-dashes, f-strings nested inside
raw strings, and triple-quoted `print(f"""...""")` blocks terminating the outer string.

**Implication for Claude Code:** don't silently rewrite notebooks end-to-end. Propose
the change, explain it, let it be typed.

---

## D2 — No composite signals

**Decision:** Tools 1 and 3 do not produce a single blended "signal" number.

**Why:** the owner identified the flaw independently — *"Does the us_total already
include South Central? If so, when we make our composite signal, are we double
counting?"* Yes. EIA's `us_total` is the sum of the regions, so averaging the regional
z-scores with the national one double-counts whichever region is largest.

**What replaced it:** Tool 1 uses an explicit, documented weighted bias (40% US total /
60% Cushing) with the weights and the rationale written inline. Tool 3 reports regional
z-scores separately and lets the reader integrate them.

**Principle established:** if a number can't be explained in one sentence of plain
arithmetic, it doesn't go in the output.

---

## D3 — Percentile windows are longer than chart windows

**Decision:** two separate constants.

```python
YEARS_HISTORY    = 5    # the seasonal band drawn on the chart
YEARS_PERCENTILE = 10   # the window the percentile rank is computed over
```

**Why:** five years of week-of-year observations is ~5 data points per bucket, which
makes a percentile rank nearly meaningless. Ten years doubles the sample without
reaching so far back that the shale-era supply regime stops being comparable. The
chart stays at five years because ten years of overlapping bands is unreadable.

---

## D4 — Baker Hughes is manual, deliberately

**Decision:** auto-download was removed from Tool 6 entirely.

**Why:** the published direct link is a hardcoded UUID that serves whatever file was
behind it when the URL was minted. It returned April data in August without erroring —
the worst failure mode, because it looks like success. The owner's preference: *"I like
to use the full manual method, more-or-less ignoring the link entirely."*

**What replaced it:** `load_bh_workbook()` checks for a manually placed file first,
falls back to the cache, and `_cache_is_stale()` compares mtimes so a newer manual
download automatically triggers a reparse.

**Do not re-add auto-download.** This is a decision, not an unfinished feature.

---

## D5 — Identify futures contracts by price, not metadata

**Decision:** Tool 2's `identify_contract()` downloads candidate contracts and matches
whichever close is within $0.05 of the continuous contract's close.

**Why:** yfinance's `underlyingExchangeSymbol` and `expireIsoDate` on continuous
contracts are inconsistent and sometimes simply wrong. Price is the ground truth —
a continuous front-month contract *is* some specific contract, and that contract trades
at the same price.

**Guard:** both result variables initialize to `None` when the cache is current, so the
alignment comparison is explicitly guarded rather than relying on truthiness of
possibly-undefined names.

---

## D6 — Load the newest file by mtime, never alphabetically

**Decision:** every cross-tool CSV read sorts by `os.path.getmtime`.

**Why:** alphabetical sorting of `crude_inventory_2026-05-*.csv` vs
`crude_inventory_2026-06-*.csv` is fine, but filenames containing month *names* break:
`May` sorts after `June` because `M` > `J`. This caused Tool 2 to display $90 WTI
while the market was at $69 — one of three compounding layers in that failure (the
others: stale saved cell outputs, and `df_combined` truncated at the inventory cutoff
date).

**Applied in:** Tools 2, 4, 5, 6. Required in Tool 7 and beyond.

---

## D7 — Shaded uncertainty regions were replaced with lines

**Decision:** on event-annotated charts (e.g. the post-Hormuz-closure period in Tool
2), the shaded region was removed in favor of a single vertical line marking the event.

**Why:** a fill between an upper and lower series renders as a thin sliver when the two
series converge, which reads as a drawing artifact rather than as information. A line
says "this happened here" without implying a band that isn't being measured.

---

## D8 — SVGs are styled inline, with no `<style>` blocks

**Decision:** all styling is presentation attributes on the elements.

**Why:** CSS rules in an SVG `<style>` block have higher specificity than presentation
attributes, so contrast fixes applied as attributes silently reverted. Inlining also
makes the files portable — Word, PowerPoint and LibreOffice all drop `<style>` blocks
on import, which was turning carefully colored diagrams into black-and-white outlines.

**Also:** bare `&` must be escaped as `&amp;` ("F&D" and "G&A" broke a parse), and
`xmlns` must be present or nothing renders at all.

---

## D9 — Interactive charts get fixed axes

**Decision:** the Darcy's law plate uses a fixed logarithmic y-axis (ratio to baseline,
1e-6 to 1e5) rather than auto-scaling.

**Why:** with auto-scaling, moving the pressure, viscosity or length slider scaled the
curve and the axis by the same factor, so the plot looked identical and the sliders
appeared broken. Fixing the axis makes the actual sensitivity visible.

**Generalizes to:** any interactive where the manipulated variable is a multiplier.

---

## D10 — Commentary logs append, never overwrite

**Decision:** each tool's final cell appends a timestamped record to a log file in
`data/`.

**Why:** the point of running a tool weekly is the series of readings, not the latest
one. A log that overwrites is just a slower version of looking at the chart.

**Consequence:** the logs live in gitignored `data/`, so they are local-only. If the
written record becomes valuable enough to version, that's a decision to revisit.

---

## D11 — Defensive guards live in the notebooks

**Decision:** staleness warnings, contract-alignment checks and auto-stale cache
detection are cells in the notebooks, not external validation.

**Why:** every silent-wrong-data failure in this project looked like success until
something external contradicted it. A loud print inside the notebook is read by the
person running it, at the moment they'd otherwise trust the number.

**Examples:** Tool 2's `STALENESS WARNING` banner; Tool 4's per-session ticker
diagnostic; Tool 6's `_cache_is_stale()`; the `$15.90/MMBtu` sanity-check print on the
TTF conversion.

---

## D12 — Dimensional analysis goes in the comment

**Decision:** every unit conversion carries its dimensional analysis as a comment and a
sanity-check print.

**Why:** TTF showed $187/MMBtu because the conversion divided by 0.29307 instead of
multiplying. The arithmetic was correct; the direction was not. A worked example in a
comment — `46 EUR/MWh × 1.18 USD/EUR × 0.293 MWh/MMBtu ≈ $15.90/MMBtu` — catches that
in seconds.

---

## D13 — `config.py` for secrets, gitignored

**Decision:** the EIA API key lives in `config.py` at the project root, imported by
each notebook, and excluded by `.gitignore`.

**Why:** simplest thing that works without a dependency on `python-dotenv` or
environment-variable setup across Git Bash and VS Code's Jupyter kernel.

**The near-miss worth recording:** the ignore file was once named `gitgnore` — missing
the second `i` — so git read no ignore rules at all and `config.py` was staged for the
first commit. It was caught before any push. Compounding the problem, an attempted
cleanup of a case-variant file deleted the real `.gitignore` instead, because Windows
filesystems are case-insensitive.

**Standing practice:** before any commit, run

```bash
git status --short | grep -E "config\.py|data/|charts/|pycache"
```

Empty output is the only acceptable result.

---

## D14 — Open question: clear notebook outputs before commit?

**Not yet decided.**

**For clearing:** saved outputs bloat diffs enormously (16,990 insertions in the first
commit, much of it base64 PNG), and stale outputs have already caused a real
misdiagnosis — Tool 2's displayed prices looked current when they weren't.

**For keeping:** the saved output *is* the record of what the tool said that week,
which is the same reason the commentary logs exist.

**Leaning:** clear outputs, lean on the commentary logs for the record, and if the
charts matter, commit the PNGs deliberately rather than as cell-output side effects.

---

## D15 — One chart style file, one hue per commodity

**Decision:** all chart styling moves to `chart_style.py` at the project root. The
palette becomes Okabe–Ito. Hue is assigned per commodity, project-wide, and line style
carries the series kind.

**Why a style file at all:** an inventory of the six notebooks found 99 inline
`fontsize=` arguments across six different values, 49 `fontweight=` arguments, one
`tight_layout()` call in fourteen plot cells, and `seaborn-v0_8-darkgrid` as the only
shared decision. Every chart had been styled separately, by eye. Styling is
configuration; what to plot is content; keeping them in the same cell meant the
configuration question got re-answered — slightly differently — fourteen times.

**Why the palette changed.** The old set was replaced partly on looks, but it also
carried a measured defect. Run through a perceptual validator in OKLab with color
vision deficiency simulation, on all pairs:

| Check | Old | New |
|---|---|---|
| CVD separation | **FAIL — ΔE 3.2** | PASS — ΔE 11.0 |
| Normal-vision separation | **FAIL — ΔE 10.7** | PASS — ΔE 16.4 |

The failing pair was amber `#BA7517` against red-orange `#E8593C`. Under deuteranopia
their perceptual distance was 3.2 against a target of 8 — effectively identical. On
any chart carrying both, one series was invisible to roughly 6% of male readers. Even
under full color vision the distance was below the legibility floor.

**No hue family is banned.** Reds, purples and browns are all available to a future
palette. The only hard requirement is that the set clears the validator. The current
colors are the current answer, not a permanent one.

**Why hue is per commodity and not per chart slot.** An earlier draft gave WTI `BLUE`
and Brent `SKY` — two blues, on the theory that related commodities should read as
related hues.

That is wrong, and Michael caught it: *"suppose we wanted to now plot a rolling 50 day
MA for WTI and Brent, what colors? Can't go to a related blue for association because
they're both blue, so then any 50 day MA needs to be like green, which feels like the
wrong data dimension to color on."*

Exactly right. Subdividing a hue family to separate two commodities spends the hue
channel on identity *twice*, leaving a derived series nowhere to go but a new hue —
which would encode "is a moving average" as though it were a different product. One
visual channel, two incompatible jobs.

**What replaced it:** hue encodes commodity and nothing else, fixed across all six
tools. Line style encodes what kind of series it is — `PRIMARY`, `DERIVED`,
`PROJECTED`, `CONTEXT`. A 50-day average of WTI keeps WTI's blue and takes the dash.
Five hues × four kinds yields twenty distinguishable lines with instant grouping.

The general rule, which outlives this palette: **a visual channel encodes one data
dimension.** Wanting a channel to carry a second dimension is the signal to reach for a
different channel, not to subdivide the one already assigned.

**Three rules the code now enforces rather than documents:**

- `regime_span()` raises `ValueError` if either end is missing. An open-ended fill
  starting at an event reads as a lopsided color jump. This extends D7 — which
  replaced a shaded region with a line for the same reason — into something the code
  won't let you do.
- `seasonal_band()` requires a `series` name and builds its label from it. A legend
  reading "5-yr range" on a two-line chart leaves the reader asking *range of what?*
- `label_series()` reserves a right-hand margin and writes labels into it, de-colliding
  in display pixels rather than data units. Callouts previously landed on top of the
  lines, sometimes in a matching color, which made prices unreadable. Pixels, not data
  units, because collisions happen in screen space — two lines 50¢ apart collide on a
  $10 chart and don't on a $200 one.

**Also found, deferred to the per-notebook pass:** `twinx()` appears twice and should
go in both cases (a dual-axis chart lets the axis scaling manufacture an apparent
correlation). Tool 3's six storage regions need small multiples — six lines on one
axis is a form problem that no palette can fix.

**Self-test:** `python chart_style.py` renders a demo exercising every helper. It has
already caught two bugs during authoring — a crash passing a pandas `Timestamp` into
matplotlib's affine transform, and collision-avoidance math that computed an
adjustment it never applied.

**Full rationale:** `docs/chart_style.md`.
