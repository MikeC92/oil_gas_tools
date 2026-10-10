# Backlog

What's planned, what's broken, and what needs doing on a schedule.

**Update this file when an item is finished — move it to the bottom with a date.**

---

## 1. Bugs to fix

### Tool 2 — remaining tuple-return bug in Cell 2

`fetch_price_with_cache()` was changed to return `(dataframe, refreshed_flag)`. Three
return paths were updated; one was missed:

```python
return (df_cache, False)      # ✅ cache current
return df_cache               # ❌ the "no new data" path (if raw.empty) — needs (df_cache, False)
return (df_combined, True)    # ✅ downloaded
```

The bad path only fires when a download succeeds but returns an empty frame, so it is
latent rather than constant. It will raise on unpacking when it does fire.

### `*_outline` text files are out of date

All six plain-text cell-by-cell outlines in `notebooks/` predate the enhancement pass
(composite-signal removal, percentile window extension, commentary logs, the glob fix).
They need a refresh against the current notebooks.

---

## 2. Tools to build

### Tool 7 — 3-2-1 crack spread tracker (next)

```
spread = (2 × RBOB + 1 × ULSD) ÷ 3 − WTI
```

- Tickers: `RB=F` (RBOB), `HO=F` (ULSD), `CL=F` (WTI)
- RBOB and ULSD quote in $/gal — convert at **42 gal/bbl** before combining
- Overlay the seasonal band (5yr) the way Tools 1 and 3 do
- Flag the summer/winter spec transition and turnaround windows
- Curriculum tie-in: `crack_spread_explainer` and `refining_margin_waterfall` plates
- Reuse the `getmtime` glob pattern — do not reintroduce alphabetical sorting

### Tool 8 — SPR tracker

- EIA US Strategic Petroleum Reserve stocks
- IEA international public stock obligations for context
- Worth showing alongside commercial crude: the two together are the real cushion

### Later ideas

- Refinery utilization tracker (EIA weekly `WPULEUS3`-equivalent + turnaround calendar)
- Product supplied / implied demand tracker (gasoline, distillate, jet)
- Basin-level production tracker (EIA Drilling Productivity Report / STEO)
- Cross-tool dashboard that reads every commentary log and produces one weekly brief

---

## 3. Recurring maintenance

| Item | Cadence | What to do |
|---|---|---|
| **M2 ticker roll** (Tools 2, 4) | Monthly / each roll | Advance `WTI_M2_TICKER` and `NG_M2_TICKER` one month code. Tell: M1 and M2 print identical prices, spread = $0.00. |
| **`identify_contract` candidate lists** (Tool 2) | Quarterly | Refresh the hardcoded candidate contracts, e.g. `["CLX26.NYM","CLZ26.NYM","CLF27.NYM"]` — these expire out from under the function. |
| **Baker Hughes download** (Tool 6) | Weekly (Fri) | Manual XLSB download into `data/`. The notebook auto-detects a newer file by mtime. |
| **EIA facet-code check** | When a call returns no rows | Query `/facet/{id}/` and sample live records. Do not guess codes. |
| **Archive/current overlap** (Tool 6) | When Baker Hughes publishes a new archive | Confirm the dedup window still covers the overlap (currently Jan 2024–Aug 2025). |

---

## 4. Infrastructure / process

- **Claude Project** — create one pointing at this repo so chat sessions start with
  this context loaded.
- **Commentary log consolidation** — the six logs are separate files; a single reader
  that assembles them into one weekly summary would be useful.
- **Notebook output hygiene** — consider clearing cell outputs before commit. They
  bloat diffs and have already caused a stale-data misdiagnosis. (Trade-off: the saved
  outputs are also a record of what the tool said that week. Undecided — see
  `decisions.md`.)

---

## 5. Completed

| Date | Item |
|---|---|
| 2026-10 | Initial repo pushed — commit `e4b22cf`, 54 files, `.gitignore` verified clean |
| 2026-10 | Documentation set created: `CLAUDE.md`, `README.md`, `docs/` |
| 2026-09 | Diagram atlas assembled — 34 plates, 22 recovered from transcript |
| 2026-09 | Reference guide extended through downstream — 24pp, 29 tables |
| 2026-09 | Enhancement pass: composite signals removed, percentile windows extended to 10yr, commentary logs added to all six tools |
| 2026-09 | Glob `getmtime` fix applied to Tools 2, 4, 5, 6 |
| 2026-09 | Tools 3, 4, 5, 6 built cell by cell |
