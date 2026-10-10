# oil_gas_tools

A six-notebook Python suite for tracking the weekly data that moves oil and natural
gas markets — paired with a written curriculum covering the value chain from reservoir
geology to petrochemicals.

Built as a self-directed learning project: every tool pulls live data from a public
source, compares it against its own history, and writes a timestamped commentary entry
so the record accumulates week over week.

---

## The tools

| # | Notebook | What it answers |
|---|---|---|
| 1 | `eia_inventory_tracker` | Are US crude and Cushing stocks high or low for this week of the year? |
| 2 | `wti_brent_monitor` | Where are WTI and Brent, how wide is the spread, and does inventory explain it? |
| 3 | `gas_storage_tracker` | Is natural gas storage tight or loose, nationally and by region? |
| 4 | `futures_curve_monitor` | Is the curve in contango or backwardation, and how is the roll priced? |
| 5 | `lng_export_monitor` | Are US LNG exports running, and is the arb to Europe/Asia open? |
| 6 | `rig_count_tracker` | Is drilling activity rising or falling, and in which basins? |

Each notebook ends with a chart saved to `charts/` and a commentary entry appended to
a log in `data/`.

### Data sources

- **EIA API v2** — weekly petroleum stocks, weekly gas storage, monthly LNG exports
- **yfinance** — WTI, Brent, Henry Hub, RBOB, ULSD, TTF, FX
- **Baker Hughes** — North America rig counts (manual XLSB download)

---

## Educational materials

- **`educational_files/OilGas_Reference_Guide.docx`** — 24 pages, 29 tables, covering
  upstream, midstream and downstream with US and global counterpart comparisons.
- **`educational_files/oil_gas_diagram_atlas.html`** — 34 self-contained plates:
  petroleum system cross-sections, drilling and fracturing anatomy, gathering and
  processing flows, the LNG chain, crude distillation, petrochemical routes, terminal
  structure, refining margin waterfalls, KPI frameworks, and two interactive plates
  (Darcy's law, production decline curves). Open it in any browser — no dependencies.
- **`educational_files/Archive/oil_gas_diagrams_source/`** — the individual SVG
  sources, styled inline so they drop cleanly into Word, PowerPoint or LibreOffice.

---

## Setup

```bash
git clone https://github.com/MikeC92/oil_gas_tools.git
cd oil_gas_tools
```

Create a Python 3.11 environment and install:

```bash
pip install pandas numpy matplotlib requests yfinance openpyxl python-docx
```

Get a free EIA API key at <https://www.eia.gov/opendata/register.php>, then create
`config.py` in the project root:

```python
EIA_API_KEY = "your_key_here"
```

`config.py` is gitignored and must stay that way.

Create the output directories (they are gitignored, so they don't come with the clone):

```bash
mkdir -p data charts
```

Then open any notebook in `notebooks/` and run it top to bottom.

---

## Running order

Tool 2 reads Tool 1's inventory CSV, and Tools 4/5/6 read from each other's exports.
On a cold start, run them in numerical order once so the caches exist. After that each
notebook can be run on its own cadence — Tool 1 and 3 after the Wednesday and Thursday
EIA releases, Tool 6 after the Friday Baker Hughes release, Tools 2 and 4 any day.

---

## Repository layout

```
notebooks/            the six tools, plus plain-text cell-by-cell outlines
educational_files/    reference guide, diagram atlas, SVG sources
docs/                 curriculum progress, backlog, design decisions
data/      (ignored)  CSV caches and commentary logs
charts/    (ignored)  generated PNGs
config.py  (ignored)  EIA API key
```

`CLAUDE.md` holds the operational detail — environment, known fragile points, and the
maintenance quirks worth knowing before debugging anything.

---

## A note on maintenance

Three things go stale on their own and are worth knowing about up front:

1. **M2 futures tickers** in Tool 4 are explicit contracts and must be advanced when
   the front month rolls. The tell is M1 and M2 printing the same price.
2. **EIA facet codes** have changed without notice more than once. When a call returns
   no rows, query the facet metadata endpoints rather than guessing.
3. **Baker Hughes** data is downloaded manually by design — the published direct link
   serves a stale file.

Details and diagnostics for all three are in `CLAUDE.md`.
