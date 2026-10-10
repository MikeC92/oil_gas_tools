# Curriculum

Where the learning stands. This is the shared map between Claude Chat (which teaches
the topics) and Claude Code (which builds the tools), so both know what has been
covered and what comes next.

**Update this file when a topic is completed or a new one is started.**

Status key: ✅ covered · 🔄 in progress · ⬜ planned

---

## Layer 1 — Upstream ✅

| Topic | Status | Diagram plates |
|---|---|---|
| Petroleum system: source, reservoir, seal, trap, migration | ✅ | `petroleum_system_cross_section` |
| Porosity, permeability, Darcy's law | ✅ | `porosity_permeability_explainer`, `darcys_law_interactive` |
| Seismic survey and exploration workflow | ✅ | `seismic_survey_explainer`, `upstream_workflow` |
| Well logging and appraisal | ✅ | `well_logging_appraisal` |
| Drilling anatomy: vertical, directional, horizontal | ✅ | `drilling_anatomy` |
| Hydraulic fracturing: stages, proppant, fluid | ✅ | `hydraulic_fracturing_explainer` |
| Production decline curves, type curves | ✅ | `production_decline_curves` (interactive) |
| Enhanced oil recovery methods | ✅ | `eor_methods_comparison` |
| Upstream KPIs: F&D cost, G&A, lifting cost, reserve replacement | ✅ | `upstream_kpi_framework` |

**Interactive note:** Darcy's law plate needed a fixed logarithmic y-axis (ratio to
baseline, 1e-6 to 1e5). With auto-scaling, changing pressure/viscosity/length scaled
the curve and the axis identically, so the sliders looked dead.

---

## Layer 2 — Midstream ✅

| Topic | Status | Diagram plates |
|---|---|---|
| Value chain overview | ✅ | `og_value_chain`, `midstream_overview_map` |
| Gathering, compression, processing | ✅ | `gathering_processing_flow` |
| NGL composition and fractionation | ✅ | `us_ngl_composition_2024` |
| Pipeline hydraulics | ✅ | `pipeline_hydraulics_schematic` |
| US midstream geography and basin takeaway | ✅ | `us_midstream_geography`, `us_natural_gas_flow_2024` |
| Cushing as a physical and financial hub | ✅ | `cushing_hub_mechanics` |
| Midstream business models: fee-based vs commodity-exposed | ✅ | `midstream_business_model` |
| LNG value chain: liquefaction, shipping, regas | ✅ | `lng_value_chain` |
| Tanker classes and the freight market | ✅ | `tanker_vessel_classes`, `tanker_freight_market` |

---

## Layer 3 — Downstream ✅

| Topic | Status | Diagram plates |
|---|---|---|
| Crude distillation: cut points, the column | ✅ | `crude_distillation_column` |
| Refinery process flow: cracking, reforming, treating | ✅ | `refinery_process_flow` |
| Nelson Complexity Index, utilization, capture rate | ✅ | — |
| Refining margins and the waterfall from crack to EBITDA/bbl | ✅ | `refining_margin_waterfall` |
| Crack spread mechanics and refiner hedging | ✅ | `crack_spread_explainer`, `crack_spread_hedge_mechanics` |
| Utilization seasonality and turnaround windows | ✅ | `refinery_utilization_seasonality` |
| Petrochemicals: feedstock to olefins, steam cracking | ✅ | `petrochemical_feedstock_to_olefins` |
| Molecular structures: ethane vs ethylene, saturation | ✅ | `ethane_vs_ethylene_bonds` |
| Product distribution: batching, terminals, racks | ✅ | `product_pipeline_batching`, `fuel_terminal_structure` |
| Downstream KPIs and financial metrics | ✅ | — |

**Threads opened and worth returning to:**
- Diesel's current dislocation — refiner economics vs retail station economics.
- Whether a reformer can take both gas and liquid feedstock (yes — this is why the
  fuels/plastics split is a commercial decision, not purely a technical one).
- Product mix breakdown by percentage, viewed both in BOE and in Bcf.

---

## Layer 4 — Commercial ⬜ (next up)

Per the reference guide footer, this is the next layer. Topics queued:

| Topic | Status |
|---|---|
| Market structure: who trades what, and where | ⬜ |
| Trading counterparties: producers, refiners, merchants, financials | ⬜ |
| Brokers, clearing, and how a physical deal actually closes | ⬜ |
| Company-by-company mapping — who occupies which link in the chain | ⬜ |
| Services and partnerships: the service companies, the supply chain | ⬜ |
| Prototypical firm KPIs tracked over time | ⬜ |
| End purchasers — who ultimately buys the barrel | ⬜ |
| US production mix (pie chart — oil vs gas vs NGL) | ⬜ |
| Coal — where it sits relative to gas in the power stack | ⬜ |
| Renewables — the substitution and complementarity picture | ⬜ |
| Industry validation: do practitioners build tools this way? | ⬜ |

---

## Layer 5 — Financial / valuation ⬜

| Topic | Status |
|---|---|
| Reserve-based lending and PV-10 | ⬜ |
| Segment reporting — how an integrated major breaks out results | ⬜ |
| Midstream MLP structure, distributable cash flow | ⬜ |
| Refiner valuation: EV/complexity-barrel, mid-cycle margins | ⬜ |

---

## How the tools map to the curriculum

| Curriculum concept | Tool that measures it |
|---|---|
| Inventory as the balance of supply and demand | Tool 1 |
| Quality and location differentials | Tool 2 (Brent–WTI) |
| Seasonal gas balance, injection/withdrawal cycle | Tool 3 |
| Storage economics, carry, roll yield | Tool 4 |
| Global gas arbitrage | Tool 5 |
| Upstream capital cycle | Tool 6 |
| Refining margin | Tool 7 (planned) |

Each new curriculum layer should ask: *what would measure this?* That question is what
generates the backlog.
