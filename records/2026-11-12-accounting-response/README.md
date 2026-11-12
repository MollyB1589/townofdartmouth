# Dartmouth accounting records received — November 12, 2026

**Source:** Seven Excel workbooks uploaded by the requester, reported as the Town of Dartmouth financial records provided in response to the original public-records request to Donna Fernandes.

**Intake status:** Files inventoried and mechanically profiled. **Original Excel workbooks are not committed to this public repository** pending a privacy and permissions review. This directory contains non-identifying summaries, not the original detailed data.

## What was received

| Workbook | Data rows | Scope / description |
| --- | ---: | --- |
| GF Expenditures 2022-2026.xlsx | 66,795 | General-fund vendor/invoice/ledger-style transactions |
| Other Funds Expenditures 2022-2026.xlsx | 17,060 | Other fund transactions |
| 2022-2027 WEF SEF Invoice Listing.xlsx | 13,233 | Water/sewer enterprise fund invoice listing |
| 2022-2027 SWEF Invoice Listing.xlsx | 8,211 | Solid waste enterprise fund invoice listing |
| 2022-2027 WMEF Invoice Listing.xlsx | 1,158 | Waterways enterprise fund invoice listing |
| 2022-2027 DCTV Invoice Listing.xlsx | 1,144 | DCTV invoice listing |
| Vendors Listing - Active.xlsx | 3,374 | Active vendor master list, **including street addresses** |

Total: **107,601 transaction rows**, plus **3,374 vendor-master rows**. Rows exclude header rows.

All six transaction listings **contain FY2027 records**, even the two files named "2022-2026." FY2027 is incomplete as of the receipt date and must not be compared as a completed fiscal year.

## Files saved in this public repository

- [`summary-by-source-year.csv`](summary-by-source-year.csv): record counts and signed sums of the amount field by workbook/fiscal year; *not reconciled audited expenditures*
- [`source-manifest.csv`](source-manifest.csv): workbook name, row counts and SHA-256 hashes to verify the source files exactly
- This README documenting source and analysis limitations

**NOT saved here:** the full workbooks. The active vendor list includes 3,370 populated vendor street-address fields; transaction descriptions can also contain names or other identifying detail. Public-record status does not mean indiscriminate republishing is appropriate. Keep the original files in private secure storage until each dataset is reviewed and approved for disclosure or redaction.

## Initial field inventory

All six transaction files have vendor ID/name, organizational description, general ledger account, fiscal year, transaction type, amount, warrant, invoice number, narrative description, and invoice date. The general-fund and other-funds exports also include accounting period. Type labels observed: `INV` (invoice), `DIR` (direct), `CRM` (credit memo), with negative amounts appearing in the data. The exact accounting definitions and effect on expenditure totals must be confirmed with the Town.

The active vendor list has vendor ID, alpha sort name, company name, status, street-address lines, city, state, ZIP, and DBA.

## Analysis cautions / blockers

1. Summaries are arithmetic sums of signed `AMOUNT` cells, **not necessarily reconciled spending**. They may reflect only vendor/payable items rather than total budgets, payroll, transfers, capital commitments or all cash paid.
2. Credits and certain negative postings are included in signed totals; confirm credit semantics.
3. The relationship and any potential double-counting among `Other Funds` and the dedicated enterprise invoice listings must be tested before combining them.
4. `FY2027` is year-to-date, not a full-year result.
5. Confirm the fiscal-year field means year ending June 30, and verify whether invoice dates are payment dates or voucher dates.
6. Match by GL account/org code to DPW divisions before attributing all entries to DPW, and reconcile against enterprise fund statements.
7. The files' two `2022-2026` titles understate the included FY2027 data; the manifest preserves the original names for evidentiary integrity.
8. Validate a sample against original Town records and preserve the received originals unchanged.

## Next steps

- [ ] Move untouched original workbooks into a private, access-controlled evidence store
- [ ] Privacy review and prepare redacted publication extracts; preserve original-to-redacted mapping privately
- [ ] Confirm with Town which posting types and dates represent actual vendor payments
- [ ] Map transaction GL accounts to funds, departments and DPW operational divisions
- [ ] Resolve overlaps between `Other Funds` and enterprise fund listings
- [ ] Reconcile summary by fiscal year/fund to Town financials
- [ ] Join approved vendor identifier/name fields without republishing personal addresses
- [ ] Update financial research and DPW audit with sourced, verified findings

**No wrongdoing or waste has been inferred from these unreviewed transactions.**
