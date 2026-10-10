# Backlog

What's planned, what's broken, and what needs doing on a schedule.

**Update this file when an item is finished — move it to the bottom with a date.**

---

## 1. Blocking the analysis

### Tool 1 exports only the current year

`df_current_us` merges the current year's observations onto a **static** seasonal band
keyed by week-of-year, so the CSV holds ~52 rows. Tool 2's inventory↔price correlation
therefore runs on ~42 overlapping weeks, which after the 4-week return overlap is an
effective sample of **9**. The 95% interval came back [−0.692, +0.634] — wide enough to
contain nearly every correlation that exists. That isn't a weak result; it's no result.

**The fix:** compute the seasonal z-score with a **rolling** band — for each date, the
same week-of-year across the five prior years — and export the whole history. That
turns 42 observations into ~900 and makes the question answerable.

This is the single highest-value item on the list. Everything about the
inventory→price relationship is currently unmeasurable.

### Is the inventory analysis even in the right tool?

Tool 2's question is "how do the two crude benchmarks relate to each other." Cells 5–7
ask "does US inventory predict WTI." Different questions sharing a notebook because the
data happened to be nearby.

Consider moving the inventory×price analysis into Tool 1 (which owns the inventory data
and needs the rolling-z rework anyway) or into a tool of its own. Would also resolve the
oddity of WTI-only panels in a WTI–Brent notebook.

---

## 2. Bugs and oddities

### Negative Brent–WTI spread, spring 2026

The spread printed negative for a stretch after the Hormuz closure — WTI above Brent.
That's backwards: Brent is the waterborne barrel most exposed to a Gulf disruption.
Either something real happened (US export logistics seizing, a Cushing squeeze) or
there's a data artifact. Worth tracing to the underlying prints.

### `*_outline` text files are stale

All six plain-text outlines predate the enhancement pass *and* the chart_style rework.
Regenerate them against the current notebooks — but only after Tools 3–6 are reworked,
or they'll go stale again immediately.

---

## 3. Tools to build

### Tool 7 — 3-2-1 crack spread tracker

```
spread = (2 × RBOB + 1 × ULSD) ÷ 3 − WTI
```

- Tickers: `RB=F`, `HO=F`, `CL=F`
- RBOB and ULSD quote in $/gal — convert at **42 gal/bbl** before combining
- Seasonal band like Tools 1 and 3
- Flag the summer/winter spec transition and turnaround windows
- Curriculum tie-in: `crack_spread_explainer`, `refining_margin_waterfall` plates
- Follow Tool 2's patterns: `chart_style`, `getmtime` globs, observed-only arithmetic

### Tool 8 — SPR tracker

EIA US Strategic Petroleum Reserve plus IEA international public stock obligations.
Shown alongside commercial crude, the two together are the real cushion.

### Later

- Refinery utilization tracker + turnaround calendar
- Product supplied / implied demand (gasoline, distillate, jet)
- Basin-level production (EIA Drilling Productivity Report / STEO)
- A weekly brief that reads every commentary log and assembles one summary

---

## 4. Recurring maintenance

| Item | Cadence | What to do |
|---|---|---|
| **M2 ticker roll** (Tools 2, 4) | each roll | Advance `WTI_M2_TICKER` / `NG_M2_TICKER` one month code. Tell: M1 and M2 print the same price, spread $0.00. |
| **`identify_contract` candidates** (Tool 2) | quarterly | Refresh the hardcoded list — those contracts expire out from under it. |
| **Baker Hughes download** (Tool 6) | weekly (Fri) | Manual XLSB into `data/`; the notebook detects it by mtime. |
| **EIA facet check** | when a call returns no rows | Query `/facet/{id}/`. Don't guess codes. |
| **Archive/current overlap** (Tool 6) | on each new BH archive | Confirm the dedup window still covers it (currently Jan 2024–Aug 2025). |

---

## 5. Chart rework — Tools 3, 4, 5, 6

Tool 2 is done and is the reference. The remaining four need the same transformation,
which is now well-defined enough to review rather than retype:

1. Drop `plt.style.use("seaborn-v0_8-darkgrid")`; add `cs.apply_style()`.
2. Replace every hex with a `chart_style` constant; hue by commodity.
3. Delete every inline `fontsize=` / `fontweight=`.
4. Replace hand-offset annotations with `cs.label_series()` — name and value at the
   right edge, no leader lines.
5. Kill the remaining `twinx()`.
6. Events via an `EVENTS` dict and `cs.event_marker()`, never a price-threshold
   heuristic.
7. ISO-dated output filenames.
8. `cs.footer()` on every chart; `cs.finish(..., tight=False)` for GridSpec figures.
9. Set figsize to the data density — not 13 inches out of habit.

**Tool 3 needs more than cosmetics.** Six storage regions on one axis is a *form*
problem no palette can fix. It wants small multiples: six panels on a shared y-scale,
each with one region highlighted and the others ghosted in `RULE` gray behind it.

---

## 6. Infrastructure

- **`nbstripout`** — clear notebook outputs on commit automatically. Not a nicety:
  committed output once leaked six characters of a live API key into the public repo.
- **Tool 7+ should start from a template** rather than copying an existing notebook,
  so stale patterns stop propagating.

---

## 7. Completed

| Date | Item |
|---|---|
| 2026-10-10 | Tool 2 reworked: observed-only spread (198 of 4,977 sessions were one-sided and had been forward-filled), 2016+ percentile window, `twinx` → stacked panels, Fisher-z correlation intervals, `chart_style` throughout, ISO filenames, `EVENTS` dict |
| 2026-10-10 | EIA API key rotated after a 6-character prefix was found in committed notebook output |
| 2026-10-10 | `chart_style.py` + `docs/chart_style.md` + D15 — Okabe–Ito palette, one hue per commodity, line style as the second channel |
| 2026-10-10 | Tool 2 tuple-return bug — already fixed; this entry was stale |
| 2026-10-10 | `oil_gas_tools` Project created on claude.ai with the repo connected |
| 2026-10 | Initial repo pushed — commit `e4b22cf`, 54 files |
| 2026-10 | Documentation set: `CLAUDE.md`, `README.md`, `docs/` |
| 2026-09 | Diagram atlas — 34 plates, 22 recovered from transcript |
| 2026-09 | Reference guide extended through downstream — 24pp, 29 tables |
| 2026-09 | Enhancement pass: composite signals removed, 10yr percentile windows, commentary logs |
| 2026-09 | Glob `getmtime` fix across Tools 2, 4, 5, 6 |
| 2026-09 | Tools 3, 4, 5, 6 built cell by cell |
