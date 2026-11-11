# Dartmouth, Massachusetts: Municipal Financial Baseline, FY2016 to FY2027

Prepared November 10, 2026 and corrected November 11, 2026 for an independent civic transparency initiative. This folder is a reusable, source-linked baseline of the Town of Dartmouth's finances: revenues, spending, reserves, debt, long-term obligations, enterprise funds, audits, governance and a comparison with similar Massachusetts towns.

Start with the report: [`dartmouth-municipal-financial-baseline-fy2016-fy2027.md`](dartmouth-municipal-financial-baseline-fy2016-fy2027.md).

Nothing in this folder is a finding of misconduct. Unusual figures are reported as facts with their documented context, and where a cause is not documented the text says so.

## Contents

| Path | What it is |
|---|---|
| `dartmouth-municipal-financial-baseline-fy2016-fy2027.md` | Full report: executive summary, year-by-year tables, department and fund analysis, governance map, peer comparison, audits, documented concerns, hypotheses, top 10 opportunities, information gaps, records requests, document inventory, methods |
| `data/` | 18 CSV tables (UTF-8, comma-delimited, header row) described below |
| `charts/` | Eight PNG charts generated from the tables |
| `scripts/` | The Python scripts that built the tables, charts and report (see "Regenerating") |

## Evidence labels

| Label | Meaning |
|---|---|
| Verified | Taken directly from a primary record that is linked with its date and page or section |
| Derived | Arithmetic on verified figures (inflation adjustment, per-resident amounts, sums, percentage changes) |
| Hypothesis | A reasonable inference that is not confirmed; each names the record that would test it |
| Unavailable | Looked for and not located in public sources as of November 10, 2026 |

Classifications used in `13_documented_concerns.csv`: "Verified fact (primary record)", "Documented statement by Town official or committee", "Verified inconsistency; cause not established", and "Not located in public sources".

## Review status and repository statuses

The figures were extracted by an AI research assistant and checked against the original records: page-level text matches for audited figures, cross-footing for budgets, and structured Federal Audit Clearinghouse fields for audit attributes. They have not yet been independently checked by a person. The repository's [research standards](https://github.com/MollyB1589/townofdartmouth/blob/main/research/RESEARCH_STANDARDS.md) reserve "Verified finding" for claims that are independently checked and require a human-reviewed audit trail for AI-assisted work, so this folder should be taken in as follows.

| Label in this folder | Repository status on intake | After a human spot-check of the cited page |
|---|---|---|
| Verified | Needs verification | Verified finding |
| Verified (secondary source) | Needs verification | Needs verification until a primary record is obtained |
| Hypothesis (H1 to H7 in the report) | Hypothesis | Hypothesis until the named record is obtained |
| Unavailable | Needs verification (records request pending) | Unchanged until records are produced |
| Rows of `12_source_inventory.csv` | Source collected | Source collected |
| Entries in the corrections log | Closed / corrected | Closed / corrected |

A practical spot-check: pick rows from `02_audited_statements_fy2016_fy2025.csv`, open the `source_url` at the listed PDF page and confirm the value; the ten audit attributes in `11_audit_filing_timeline.csv` can be confirmed on the page listed in `auditors_summary_pdf_page`.

How this folder lines up with the intake checklist in [repository issue 1](https://github.com/MollyB1589/townofdartmouth/issues/1):

| Checklist item | Where it is covered |
|---|---|
| Report and original cited source URLs | The report; `12_source_inventory.csv` |
| Classify each source | `source_type` column in `12_source_inventory.csv` (Town record, state or federal data, independent audit, state review, news report, project repository) |
| Approved budgets versus actual expenditures | "Three accounting bases" below; `basis_note` in table 01, `basis` in table 03, and the actual and budget column names in table 04 |
| Normalize fiscal years, fund types, dollars and units | Conventions section; `unit` columns; real FY2026 dollars and per-resident columns |
| Missing data and additional records requests | `16_information_gaps.csv`; `15_records_requests.csv` |
| Testable hypotheses, not accusations | Report section "Hypotheses that are not yet established" (H1 to H7, each with the record that would test it) |
| Source register with page, section and URL | `12_source_inventory.csv`; page references in tables 02, 05, 11 and 13 |
| Identified-person allegations | None are made |

## Corrections log

Corrections made during preparation, recorded rather than silently rewritten. No version containing the earlier statements was published.

| Date | Item | Earlier draft statement | Corrected statement | How the error was found |
|---|---|---|---|---|
| 2026-11-10 | Low-risk auditee status (C02, table 11) | Not low-risk in six of ten years | Not low-risk in all ten years, FY2016 to FY2025 | Text extraction drops check marks; re-read from page images and the Clearinghouse structured field |
| 2026-11-11 | Board of Public Works (C21, table 17) | Two of three seats vacant in August 2026 | The Board was expanded from three to five members effective July 1, 2026; the two vacancies were the new seats and were filled on August 3, 2026 | The Department of Public Works page still describes a three-person board; the Fall 2025 Town Meeting article, the Town notice and the Board of Public Works page show five |
| 2026-11-11 | Records request R09 | Covered all departments | Excludes the Department of Public Works, already requested on 2026-11-10 | Second request log found in the repository |
| 2026-11-11 | ClearGov portal (G05, G07) | Described as periodic budget uploads | Town describes budget, revenue, expenditure and line-item data updated monthly, enterprise funds excluded in the first phase; portal contents not reviewed | Budget Information page re-read |

## Three accounting bases

These should not be mixed in one calculation.

| Basis | Origin | Used for |
|---|---|---|
| State Schedule A (statutory) | Annual report the Town files with the Massachusetts Division of Local Services (DLS) | Longest consistent series, FY2016 to FY2026, and the only one comparable across towns. FY2026 is unaudited |
| Audited statements (GAAP) | Independent audits filed with the Federal Audit Clearinghouse, FY2016 to FY2025 | Fund balances, debt, pension and OPEB liabilities, enterprise fund results, budget-to-actual schedules |
| Town budget documents | "Schedule A" operating budget voted by Town Meeting | Department-level detail. Narrower than the state report: it excludes state and county assessments, transfers and separate warrant articles |

## Data dictionary

Dollar amounts are whole US dollars unless a column name or `unit` says otherwise. Empty cells mean the figure is not available for that year. `source_id` values are keys into `12_source_inventory.csv`.

| File | Rows | Columns | Notes |
|---|---:|---|---|
| `01_year_by_year_baseline_long.csv` | 1,028 | `fiscal_year`, `metric`, `value`, `unit`, `basis_note`, `source_id` | One row per metric and year. The main time series |
| `01_year_by_year_baseline_wide.csv` | 96 | `metric`, `unit`, `source_id`, `FY2016` to `FY2027` | Same data, one row per metric |
| `02_audited_statements_fy2016_fy2025.csv` | 443 | `fiscal_year`, `item`, `value`, `pdf_page`, `text_match_check`, `report_pdf_url` | Every audited figure with the PDF page it was read from. `text_match_check` records whether the literal value appears in the extracted text of that page |
| `03_general_fund_by_function.csv` | 247 | `fiscal_year`, `classification`, `category`, `basis`, `amount_usd`, `share_of_total_pct`, `amount_fy2026_dollars`, `per_capita_fy2026_dollars`, `source_id`, `validation_note` | Two classifications: state function (FY2016 to FY2026) and Town budget category (FY2016 to FY2027). `basis` is actual or budget |
| `04_department_budget_fy2022_fy2027.csv` | 58 | `section`, `department`, `FY2022_actual` to `FY2025_actual`, `FY2026_budget_revised`, `FY2027_budget`, `change_fy2022_to_fy2027_usd`, `change_fy2022_to_fy2027_pct`, `source_id` | 49 departments and lines plus category totals. Compares an actual year with a budget year |
| `05_enterprise_funds_audited.csv` | 33 | `fiscal_year`, `fund`, `operating_revenues`, `operating_expenses`, `operating_income_loss`, `transfers_net`, `change_in_net_position`, `ending_net_position`, `unrestricted_net_position`, `pdf_page`, `text_match_check`, `report_pdf_url` | Sewer, water, solid waste (separate fund from FY2023) and other enterprise funds |
| `06_peer_comparison_fy2025.csv` | 19 | `municipality`, `peer_group`, then about 50 measures (per-resident spending by function, tax bill, rates, levy, state aid, debt, reserves, staffing, growth since FY2016, school per-pupil measures) | Dartmouth, Dartmouth plus fire district levies (estimate), 11 statistical peers, 5 South Coast neighbors, and the median of the 11 |
| `07_peer_timeseries_long.csv` | 8,904 | `municipality`, `peer_group`, `fiscal_year`, `metric`, `value`, `source_id` | State data for all 17 municipalities over time |
| `08_school_per_pupil_dese.csv` | 4,994 | `district`, `peer_group`, `school_year_ending`, `category`, `indicator`, `value`, `source_id` | State education department per-pupil spending by function, enrollment and staffing |
| `09_fire_district_levies.csv` | 44 | `fiscal_year`, `dls_district_code`, `district`, levy by property class, `total_levy`, `residential_rate_per_1000`, `commercial_rate_per_1000`, `source_id` | The three fire districts are separate governments outside the Town budget and audit |
| `10_federal_awards_by_program.csv` | 208 | `audit_year`, `assistance_listing`, `federal_program_name`, `cluster_name`, `amount_expended`, `is_major_program`, `is_direct`, `passthrough_to_subrecipients`, `fac_report_id`, `source_id` | Federal Audit Clearinghouse award records |
| `11_audit_filing_timeline.csv` | 10 | `fiscal_year`, `fiscal_year_end`, `fac_report_id`, `auditor`, report and acceptance dates, `standard_9_month_due_date`, `days_after_standard_due_date`, `opinion`, `low_risk_auditee`, `findings_in_fac`, `federal_awards_expended`, `report_pdf_url`, `fac_summary_url`, `auditors_summary_pdf_page`, `note` | `low_risk_auditee` is the Clearinghouse data field, confirmed against the page image of each auditor's summary at `auditors_summary_pdf_page` |
| `12_source_inventory.csv` | 106 | `source_id`, `source_type`, `title`, `publisher`, `document_date`, `url`, `pages_or_section`, `notes` | 103 documents and datasets plus 3 alias rows that point to the same URL under a second ID |
| `13_documented_concerns.csv` | 22 | `concern_id`, `category`, `documented_concern`, `classification`, `source_ids`, `page_or_section`, `context_and_limits`, `source_urls`, `source_dates`, `standard_note` | C01 to C22 |
| `14_top10_opportunities.csv` | 10 | `rank`, `opportunity`, `documented_dollar_base`, `illustrative_sensitivity`, two 1-to-5 scores, `priority_score`, `evidence_status`, `questions_to_investigate`, `source_ids`, `source_urls`, `source_dates`, `related_records_requests`, `standard_note` | Ranked by financial scale times evidence quality |
| `15_records_requests.csv` | 16 | `request_id`, `priority`, `topic`, `records_to_request`, `period`, `likely_custodian`, `preferred_format`, `why_needed`, `related_concerns_and_opportunities`, `legal_basis`, `overlap_with_2026_11_10_request` | R01 to R16. Custodians are the likely holders, not confirmed. The overlap column checks each request against both requests logged in the repository on 2026-11-10 (financial records; DPW staffing and payroll) |
| `16_information_gaps.csv` | 20 | `gap_id`, `area`, `gap_description`, `significance`, `workaround_used_in_this_baseline`, `source_ids`, `related_records_request`, `source_urls` | G01 to G20 |
| `17_town_governance_map.csv` | 20 | `body_or_office`, `type`, `composition_or_appointment`, `financial_responsibilities`, `source_ids`, `notes`, `source_urls` | Who is responsible for what |

## Charts

| File | Shows |
|---|---|
| `charts/01_general_fund_spending_nominal_vs_real.png` | General fund spending, nominal and in FY2026 dollars |
| `charts/02_operating_budget_by_category.png` | Town operating budget by category, FY2016 to FY2027 |
| `charts/03_reserves.png` | Free cash, stabilization and unassigned fund balance |
| `charts/04_debt_pension_opeb.png` | Debt outstanding, net pension liability and net OPEB liability |
| `charts/05_enterprise_funds.png` | Enterprise fund operating results and reserves |
| `charts/06_peer_comparison.png` | Dartmouth against the peer set, FY2025 |
| `charts/07_audit_timeliness.png` | Days from the standard due date to federal acceptance of each audit |
| `charts/08_fire_district_levies.png` | Fire district tax levies, FY2016 to FY2026 |

## Conventions

- **Fiscal year.** July 1 to June 30. FY2026 ended June 30, 2026.
- **Inflation.** Fiscal-year average of the national consumer price index for all urban consumers (BLS series CUUR0000SA0), expressed in FY2026 dollars. This is a general price index, not a municipal cost index.
- **Population.** Census estimate for the calendar year before the fiscal year, as published by DLS, held at the 2024 estimate from FY2025 on.
- **Free cash.** Labelled by the fiscal year in which it becomes available to appropriate; it is certified as of the preceding July 1.
- **Fire districts.** District tax levies are added to Dartmouth in one comparison row as an estimate of fire protection cost. District spending was not reviewed.
- **FY2026 and FY2027.** FY2026 state figures are as filed by the Town and unaudited. FY2027 figures are the adopted budget, certified free cash and certified retained earnings only.
- **Audit page numbers.** PDF page numbers count pages of the file as downloaded from the Federal Audit Clearinghouse, not the printed page numbers.

## Peer selection

State data for FY2025 were screened for municipalities with a population of 24,000 to 45,000, income per resident between 75% and 130% of Dartmouth's, and equalized property value per resident between 65% and 145% of Dartmouth's. Eight that have a city form of government were excluded. The 11 remaining statistical peers are Tewksbury, Billerica, Dracut, North Attleborough, Stoughton, Saugus, Danvers, Wakefield, Norwood, Milford and Middleborough. Five South Coast neighbors (Fairhaven, Westport, Somerset, Swansea, Wareham) are shown for local context and are not in the median. The screen is this project's method, not an official grouping.

## Known limits

- No transaction-level review, no review of school line items, no review of fire district finances, no legal analysis of procurement compliance, and no interviews.
- Lower spending per resident is not the same as greater efficiency. It can also reflect different service arrangements, deferred capital investment or deferred funding of retiree obligations.
- Services differ between towns: Dartmouth's fire protection is in separate districts and its water, sewer and solid waste are in enterprise funds.
- Department-level actual spending before FY2022 was captured only at category level, because the earlier budget documents are scanned images.
- The "illustrative sensitivity" figures in the opportunities table are arithmetic on the documented base. They are not savings estimates, and no savings figure has been verified.
- No person has yet re-checked the figures against the cited pages (see "Review status and repository statuses").
- The ClearGov budget portal was not reviewed; its contents may fill some of the gaps listed in table 16 for the general fund.
- Corrections made during preparation are in the corrections log above.

## Regenerating

The `scripts/` folder holds the code used to build this folder, for transparency about method:

| Script | Writes |
|---|---|
| `build1.py`, `build2.py` | Tables 01, 06, 07, 08, 09 from state downloads |
| `build3.py` | Tables 02, 04, 05, 10, 11 from the audit packages, Clearinghouse records and Town budgets |
| `build4.py` | Tables 03 and 12 |
| `build5.py` | Tables 13 to 17 |
| `build6_charts.py` | The eight charts |
| `build7_lib.py`, `build7_report.py` | The report |
| `sources.py` | The source registry behind table 12 |

The scripts read cached downloads (state report exports, audit PDFs and their extracted text, Town documents) from a working directory that is not included here, and they use absolute paths from the environment in which they were run. To rerun them, download the originals listed in `data/12_source_inventory.csv` and adjust the paths at the top of each script.

## How to cite

Cite the original document, not this folder, for any figure: each table row carries a `source_id` or URL, and `12_source_inventory.csv` gives the title, publisher, date and direct link.
