from build7_lib import *
O=[]; P=O.append
A=lambda k,y: g(k,y)
# ---------- derived values ----------
e=lambda y: A('schedA_gf_exp_total_expenditures',y); r=lambda y: A('schedA_gf_rev_total_revenues',y)
realE={y:real(e(y),y) for y in range(2016,2027)}
peak=max(realE,key=realE.get)
pop=lambda y: A('population_estimate',y)
rpc={y:realE[y]/pop(y) for y in range(2016,2027)}
bv=[(y,A('budgetary_gf_rev_actual',y)-A('budgetary_gf_rev_final_budget',y),A('budgetary_gf_exp_final_budget',y)-A('budgetary_gf_exp_actual',y)) for y in range(2016,2026)]
rev_over=sum(1 for _,a,_ in bv if a>0); exp_under=sum(1 for _,_,b in bv if b>0)
rv=[a for _,a,_ in bv]
opeb_gap=[A('audit_opeb_actuarially_determined_contribution',y)-A('audit_opeb_employer_contribution',y) for y in range(2016,2026)]
assert all(x>0 for x in opeb_gap)
fc=[A('free_cash_certified',y) for y in range(2016,2028)]
peers=rd('06_peer_comparison_fy2025.csv'); dm=peers[0]; adj=peers[1]; med=[x for x in peers if x['peer_group']=='Summary'][0]
fl=lambda x: float(x) if x not in('',None) else None
sewer=ent['Sewer']; water=ent['Water']
sew_loss=sum(1 for y in sewer if sewer[y]['operating_income_loss']<0)
fed=lambda y: A('federal_awards_expended',y)
aud=rd('11_audit_filing_timeline.csv')
fn=[x for x in rd('03_general_fund_by_function.csv') if x['classification'].startswith('DLS')]
F={(x['fiscal_year'],x['category']):x for x in fn}
def fs(y,cat): return float(F[(str(y),cat)]['share_of_total_pct'])
cats=[c_ for (y,c_) in F if y=='2016']
EDU='Education'; FIX=[c_ for c_ in cats if c_.startswith('Fixed')][0]; DS='Debt service'
tcp=lambda k: pct(tc['2022'][k],tc['2027'][k])
dep=rd('04_department_budget_fy2022_fy2027.csv')
hl=[x for x in dep if x['department'].startswith('Health & Life')][0]
ggx=((tc['2027']['General Government']-510000)/tc['2022']['General Government']-1)*100
bill16,bill26=A('avg_single_family_tax_bill',2016),A('avg_single_family_tax_bill',2026)
ere=lambda y: A('enterprise_retained_earnings_certified',y)
erepct=lambda y: ere(y)/A('enterprise_budget_total_dls',y)*100
AUD25=lambda p: c('AUDIT-FY2025',f'PDF p. {p}')

# ---------- header ----------
P('# Dartmouth, Massachusetts: Municipal Financial Baseline, FY2016 to FY2027')
P('')
P('Prepared November 10, 2026 for an independent civic transparency initiative. Scope: Town of Dartmouth general fund, enterprise funds, debt, reserves, long-term obligations, audits and governance for fiscal years 2016 through 2026, with the adopted FY2027 budget. A Massachusetts fiscal year runs July 1 to June 30; FY2026 ended June 30, 2026.')
P('')
P('## How to read this report')
P('')
P('Every finding carries one of three evidence labels.')
P('')
P('- **Verified**: taken directly from a primary record (Town document, audited financial statement, state or federal dataset) that is linked with its date and page or section.')
P('- **Hypothesis**: a reasonable inference from verified facts that has not been confirmed. Each hypothesis names the record that would test it.')
P('- **Unavailable**: information that was looked for and not located in public sources as of November 10, 2026.')
P('')
P('Figures marked "derived" are arithmetic performed on verified figures (for example inflation adjustment, per-resident amounts, sums and percentage changes). No figure in this report is estimated without being labelled, and nothing here is a finding of misconduct. All tables are also provided as CSV files in the `data/` folder; the file `README.md` is the data dictionary.')
P('')
P(f'**Review status.** The figures were extracted by an AI research assistant and checked against the original records (page-level text matches for audited figures, cross-footing for budgets, structured Clearinghouse fields for audit attributes). They have not yet been independently checked by a person. The project repository reserves the status "Verified finding" for claims that are "supported by authoritative records and independently checked" and requires a human-reviewed audit trail for AI-assisted work {c("REPO-STANDARDS","Finding statuses; AI use")}. Until a person has spot-checked the cited pages, items labelled Verified here should enter the repository as "Needs verification", hypotheses as "Hypothesis", and the document inventory as "Source collected". Corrections made during preparation are listed in the corrections log near the end of this report.')
P('')
P(tbl(['Label in this report','Repository status on intake','Repository status after a human spot-check of the cited page'],[
['Verified','Needs verification','Verified finding'],
['Verified (secondary source)','Needs verification','Needs verification until a primary record is obtained'],
['Hypothesis (H1 to H7)','Hypothesis','Hypothesis until the named record is obtained'],
['Unavailable','Needs verification (records request pending)','Unchanged until records are produced'],
['Document inventory rows','Source collected','Source collected'],
['Entries in the corrections log','Closed / corrected','Closed / corrected'],
]))
P('')
P('Three accounting bases appear and should not be mixed:')
P('')
P(tbl(['Basis','Where it comes from','Use in this report'],[
['State Schedule A (statutory basis)',f'Annual report the Town files with the Division of Local Services (DLS) {c("DLS-SCHA-GF")}','Longest consistent series (FY2016 to FY2026) and the only one comparable across towns. FY2026 is unaudited.'],
['Audited statements (GAAP)',f'Independent audits filed with the Federal Audit Clearinghouse, FY2016 to FY2025 {c("FAC-API")}','Fund balances, debt, pension and OPEB liabilities, enterprise fund results, budget-to-actual schedules.'],
['Town budget documents',f'"Schedule A" operating budget voted by Town Meeting {c("TOWN-BUDGET-PAGE")}','Department-level detail. Narrower than the state report because it excludes state and county assessments, transfers and separate warrant articles.'],
]))
P('')

# ---------- executive summary ----------
P('## Executive summary of verified findings')
P('')
P(f'Dartmouth\'s finances over the decade show strong reserves, falling debt, clean audit opinions and low spending relative to comparable towns. The principal pressures are long-term: retiree health (OPEB) and pension obligations, employee benefit costs growing faster than the budget, thin enterprise fund reserves, a tax levy at its legal limit, and a planning scenario of about $516.5 million in future borrowing. The main documented weaknesses are in financial reporting timeliness and public access to financial records. No evidence of misconduct was found, and none is asserted.')
P('')
S=[]
S.append(f'**Spending grew {pct(e(2016),e(2026)):.1f}% in nominal terms and {pct(realE[2016],realE[2026]):.1f}% after inflation.** General fund expenditures reported to the state rose from ${M(e(2016))}M in FY2016 to ${M(e(2026))}M in FY2026 (unaudited). In FY2026 dollars that is ${M(realE[2016],1)}M to ${M(realE[2026],1)}M; inflation-adjusted spending peaked in FY{peak} at ${M(realE[peak],1)}M. Per resident, real spending went from ${rpc[2016]:,.0f} to ${rpc[2026]:,.0f} {c("DLS-SCHA-GF")}; inflation adjustment is derived from the national consumer price index {c("BLS-CPI")}. Verified; real figures derived.')
S.append(f'**Education and employee benefits take a growing share; debt service a shrinking one.** Education rose from {fs(2016,EDU):.1f}% to {fs(2026,EDU):.1f}% of general fund spending, fixed costs (pensions, health insurance and other benefits) from {fs(2016,FIX):.1f}% to {fs(2026,FIX):.1f}%, and debt service fell from {fs(2016,DS):.1f}% to {fs(2026,DS):.1f}% {c("DLS-SCHA-GF")}. In the Town\'s own budget documents, FY2022 actual to FY2027 budget, the operating total grew {tcp("total"):.0f}% while Employee Benefits grew {tcp("Employee Benefits"):.0f}% (the Health and Life Insurance line {float(hl["change_fy2022_to_fy2027_pct"]):.0f}%), General Government {tcp("General Government"):.0f}% ({ggx:.0f}% excluding the Reserve Fund line), Public Safety {tcp("Public Safety"):.0f}% and Schools {tcp("Schools"):.0f}%, and Debt Service fell {abs(tcp("Debt Service")):.0f}% {c("TOWN-BUD-FY27","category summary lines")} {c("TOWN-BUD-FY25","FY2022 actual column")}. Verified.')
S.append(f'**The property tax levy is at its legal limit.** The levy grew from ${M(A("tax_levy_total",2016))}M to ${M(A("tax_levy_total",2026))}M ({pct(A("tax_levy_total",2016),A("tax_levy_total",2026)):.0f}%), with unused levy capacity never above ${max(A("levy_excess_capacity",y) for y in range(2016,2027)):,.0f} in any year {c("DLS-LEVY")}. New growth added to the levy fell from ${M(A("new_growth",2016))}M to ${M(A("new_growth",2026))}M {c("DLS-NG")}. The average single-family tax bill rose from ${bill16:,.0f} to ${bill26:,.0f} ({pct(real(bill16,2016),bill26):.1f}% after inflation, derived) while the residential rate fell from ${A("tax_rate_residential",2016):.2f} to ${A("tax_rate_residential",2026):.2f} per $1,000 as values rose {c("DLS-SFTB")} {c("DLS-RATE")}. State records show the last operating override questions on June 30, 2008 and the last debt exclusion (police station) on April 4, 2017 {c("DLS-VOTES")} {c("DLS-DEXCL")}. Verified.')
S.append(f'**Reserves have grown.** Certified free cash ranged from ${M(min(fc))}M to ${M(max(fc))}M every year and was ${M(A("free_cash_certified",2027))}M for FY2027, certified September 22, 2026 {c("DLS-FC")}. Stabilization funds grew from ${M(A("stabilization_total",2016))}M to ${M(A("stabilization_total",2026))}M {c("DLS-STAB")}. The audited unassigned general fund balance grew from ${M(A("audit_gf_fund_balance_unassigned",2016))}M to ${M(A("audit_gf_fund_balance_unassigned",2025))}M {AUD25(22)}. Verified.')
S.append(f'**Debt fell by almost half.** Long-term debt outstanding fell from ${M(A("debt_outstanding_schedA",2016))}M (FY2016) to ${M(A("debt_outstanding_schedA",2026))}M (FY2026), and general fund debt service from ${M(A("gf_debt_service_schedA",2016))}M to ${M(A("gf_debt_service_schedA",2026))}M {c("DLS-DEBT")}. The state lists Dartmouth\'s S&P rating as AAA in every year it reports from 2014 to 2026 {c("DLS-BOND")}. Verified.')
S.append(f'**Retiree obligations are the largest liabilities on the books.** At June 30, 2025 the net OPEB liability was ${M(A("audit_net_opeb_liability",2025))}M (trust assets ${M(A("audit_opeb_trust_assets",2025))}M against a total liability of ${M(A("audit_opeb_total_liability",2025))}M, {A("audit_opeb_trust_assets",2025)/A("audit_opeb_total_liability",2025)*100:.1f}% funded, derived) {AUD25(77)}. FY2025 contributions were ${opeb_gap[-1]:,.0f} below the actuarially determined amount, and were below it in each of the ten years {AUD25(84)}. The Town\'s share of the Bristol County net pension liability was ${M(A("audit_net_pension_liability",2025))}M, up from ${M(A("audit_net_pension_liability",2016))}M in FY2016 {AUD25(81)}. Governmental unrestricted net position was -${M(abs(A("audit_gov_unrestricted_net_position",2025)))}M (-${M(abs(A("audit_gov_unrestricted_net_position",2016)))}M in FY2016) {AUD25(19)}, which reflects these long-term obligations rather than a cash shortfall. Verified.')
S.append(f'**Actual results have beaten the budget.** On the audited budgetary basis, FY2025 revenues were ${M(bv[-1][1])}M above the final budget and expenditures ${M(bv[-1][2])}M below it {AUD25(85)}. Revenues exceeded the final budget in {rev_over} of the 10 audited years (by ${M(min(rv))}M to ${M(max(rv))}M). Verified; part of each year\'s expenditure variance may be carried forward rather than unspent.')
S.append(f'**Town officials nonetheless describe a structural gap.** The Director of Budget and Finance described "a structural revenue problem, where budget growth consistently outpaces the limits on revenue increases" {c("FINCOM-2026-03-05")}. The Finance Committee\'s FY2027 letter calls the ${M(tc["2027"]["total"])}M budget "break-even" and refers to a "structural deficit" {c("FINCOM-LETTER-FY27","FY2027 Budget Outlook and Budget Challenges sections")}. At the School Committee\'s May 4, 2026 discussion, Chris Oliver was reported as saying that "probably by FY28, the town\'s really going to need to consider an override" {c("WEEK-OVERRIDE","news report, secondary source")}. Verified as statements by officials; no multi-year forecast document was located (Unavailable).')
S.append(f'**Enterprise fund reserves have thinned and rates are rising.** The sewer fund reported an operating loss in {sew_loss} of 10 audited years, and its unrestricted net position fell from ${M(sewer["2016"]["unrestricted_net_position"])}M to ${M(sewer["2025"]["unrestricted_net_position"])}M; the water fund\'s unrestricted net position was ${water["2025"]["unrestricted_net_position"]:,.0f} at June 30, 2025 {AUD25(28)}. Combined certified retained earnings fell from ${M(ere(2016))}M ({erepct(2016):.1f}% of enterprise budgets) for FY2016 to ${M(ere(2026))}M ({erepct(2026):.1f}%) for FY2026 {c("DLS-ERE")}. For FY2027 the Town raised sewer rates 16%, water rates 7.5% and the annual solid waste fee from $110 to $140 {c("SB-RECAP-2026-08-03","rates item")}. Verified.')
S.append(f'**Audit opinions are clean, but every audit was filed late.** All ten audits (FY2016 to FY2025) carry unmodified opinions and the Federal Audit Clearinghouse records no findings {c("FAC-API")}. Every reporting package was accepted after the standard nine-month date, by 12 days (FY2016) to 1,020 days (FY2021); the FY2025 package was accepted July 22, 2026, 113 days after March 31 {c("ECFR-512","(a)(1)")}. The auditors reported that the Town did not qualify as a low-risk auditee in any of the ten years, which matches the Clearinghouse record {AUD25("97, Schedule of Findings and Questioned Costs, Section I")}; the year-by-year record with page numbers is in the audit timeline table below. Federal extensions during the pandemic applied to some of these years. Verified.')
S.append(f'**One audit disclosure is inconsistent.** The FY2025 package lists a prior-year finding numbered 2024-001, a material weakness in which the FY2024 schedule of federal awards omitted $1,143,085 of American Rescue Plan Act funds passed through Bristol County, marked resolved {AUD25(99)}. The FY2024 package as filed reports no findings {c("AUDIT-FY2024","PDF pp. 97 to 99")}, and minutes record the auditor stating there were no findings for FY2024 {c("JOINT-2025-07-28","p. 5")}. Verified inconsistency; the cause is not established.')
S.append(f'**A long-range scenario lists about $516.5 million of borrowing.** The Town\'s March 9, 2026 analysis lists general fund projects totalling $418.0M (derived sum of the listed items, led by a $150M middle and high school project in 2030 and three $75M school projects) and $98.5M of enterprise borrowing through 2050, with an estimated tax impact on the average home rising from $617.62 in 2030 to $1,406.08 in 2050; five further projects have no cost estimate {c("TOWN-DEBT-2026","project schedule and tax impact table")}. Verified as a planning scenario, not an authorization.')
S.append(f'**Dartmouth spends and taxes less than comparable towns.** For FY2025, general fund spending per resident was ${fl(dm["gf_total_per_capita"]):,.0f} against a median of ${fl(med["gf_total_per_capita"]):,.0f} for 11 statistical peers (${fl(adj["gf_total_per_capita"]):,.0f} when fire district levies are added, an estimate); the average single-family bill was ${fl(dm["avg_sf_tax_bill"]):,.0f} against ${fl(med["avg_sf_tax_bill"]):,.0f}; debt per resident ${fl(dm["debt_outstanding_per_capita"]):,.0f} against ${fl(med["debt_outstanding_per_capita"]):,.0f}; and state aid per resident ${fl(dm["state_aid_receipts_per_capita"]):,.0f}, the lowest of all 17 municipalities compared {c("DLS-PEERS")}. State per-pupil spending data show ${fl(dm["dese_pp_total_sy2025"]):,.0f} per pupil against a peer median of ${fl(med["dese_pp_total_sy2025"]):,.0f}, while in-district enrollment fell {abs(fl(dm["fte_pupils_change_pct_sy2016_sy2025"])):.1f}% from school year 2016 to 2025 {c("DESE-RADAR")}. Verified; per-resident figures derived.')
S.append(f'**Fire protection is financed outside the Town budget.** Three independent fire districts levy their own taxes, which rose from ${M(fire["2016"])}M to ${M(fire["2026"])}M ({pct(fire["2016"],fire["2026"]):.0f}%) between FY2016 and FY2026, compared with {pct(A("tax_levy_total",2016),A("tax_levy_total",2026)):.0f}% for the Town levy {c("DLS-DIST")}. They are not in the Town budget or the Town audit {c("FIRE-PAGE")}. Verified; district budgets and audits were not reviewed (Unavailable).')
S.append(f'**Key financial records are not published.** The audits are not posted on the Town website and no auditor management letters were located {c("ACCT-PAGE")}; no contract register, bid tabulations or award amounts are posted {c("BIDS-PAGE")}; the most recent external financial management review located dates from 2007 {c("DLS-FMR-2007","22 numbered recommendations")}. The Town launched a ClearGov budget portal in September 2026 {c("CLEARGOV-NEWS")} and states that its first phase "does not include enterprise fund data" for water, sewer, solid waste, DCTV and waterways {c("TOWN-BUDGET-PAGE","ClearGov dashboard note")}; the portal contents were not reviewed for this baseline. Verified absence as of November 10, 2026.')
for i,s in enumerate(S,1): P(f'{i}. {s}')
P('')

# ---------- year-by-year ----------
P('## Year-by-year financial comparison')
P('')
P('Dollar amounts are in millions unless the row says otherwise. "n/a" means the figure does not exist for that year or was not available. FY2026 state figures are unaudited; FY2027 shows budget or certified figures only. The full 96-metric table is `data/01_year_by_year_baseline_wide.csv`.')
P('')
H=['Measure']+[f'FY{y[2:]}' for y in YRS]; RT=list(range(1,13))
def row(label,fn,fmt='M'):
    out=[label]
    for y in YRS:
        try: v=fn(int(y))
        except Exception: v=None
        if v is None: out.append('n/a')
        elif fmt=='M': out.append(M(v))
        elif fmt=='M1': out.append(M(v,1))
        elif fmt=='D': out.append(Dl(v))
        elif fmt=='P': out.append(f'{v:.1f}%')
        elif fmt=='P2': out.append(f'{v:.2f}%')
        elif fmt=='R': out.append(f'{v:.2f}')
        else: out.append(str(v))
    return out
def K(k): return lambda y: A(k,y)
P('### General fund operations')
P('')
P(tbl(H,[
 row('Total revenues (state Schedule A)',K('schedA_gf_rev_total_revenues')),
 row('Total expenditures (state Schedule A)',K('schedA_gf_exp_total_expenditures')),
 row('Revenues less expenditures (derived)',lambda y: r(y)-e(y)),
 row('Expenditures in FY2026 dollars (derived)',lambda y: realE[y]),
 row('Population estimate (persons)',K('population_estimate'),'D'),
 row('Real expenditures per resident, $ (derived)',lambda y: rpc[y],'D'),
 row('Town budget document: actual operating total',lambda y: tc[str(y)]['total'] if y<=2025 else None),
 row('Town budget document: budgeted operating total',lambda y: tc[str(y)]['total'] if y>=2026 else A('town_schedA_budget_doc_budget_total',y)),
],RT))
P('')
P(f'Sources: {c("DLS-SCHA-GF")}; {c("DLS-POP")}; {c("BLS-CPI")}; Town budget documents FY2017 to FY2027 listed in the document inventory. Population is the Census estimate for the calendar year before the fiscal year, held at the 2024 estimate from FY2025 on. The state total is broader than the Town budget document total because it includes assessments, transfers and separately voted articles.')
P('')
P(f'![General fund spending, nominal and inflation-adjusted](charts/01_general_fund_spending_nominal_vs_real.png)')
P('')
P('### Tax base and revenue')
P('')
P(tbl(H,[
 row('Property tax levy',K('tax_levy_total')),
 row('Unused levy capacity, $',K('levy_excess_capacity'),'D'),
 row('New growth',K('new_growth')),
 row('Residential tax rate, $ per $1,000',K('tax_rate_residential'),'R'),
 row('Commercial tax rate, $ per $1,000',K('tax_rate_commercial'),'R'),
 row('Average single-family value, $',K('avg_single_family_value'),'D'),
 row('Average single-family tax bill, $',K('avg_single_family_tax_bill'),'D'),
 row('State aid receipts (cherry sheet)',K('state_aid_receipts')),
 row('State aid net of assessments',K('state_aid_net')),
 row('Budgeted local receipts',K('recap_local_receipts')),
 row('Tax receivables as % of levy',K('tax_receivables_total_pct_levy'),'P2'),
],RT))
P('')
P(f'Sources: {c("DLS-LEVY")}; {c("DLS-NG")}; {c("DLS-RATE")}; {c("DLS-SFTB")}; {c("DLS-AID")}; {c("DLS-REV")}; {c("DLS-REC")}. The Town tax rate and average bill exclude fire district taxes and the Community Preservation surcharge.')
P('')
P('### Reserves')
P('')
P(tbl(H,[
 row('Certified free cash (available in the year shown)',K('free_cash_certified')),
 row('Date free cash certified',K('free_cash_date_certified'),'S'),
 row('Free cash as % of prior budget',K('free_cash_pct_prior_budget'),'P'),
 row('Stabilization funds',K('stabilization_total')),
 row('Stabilization as % of budget',K('stabilization_total_pct_budget'),'P'),
 row('Unassigned general fund balance (audited)',K('audit_gf_fund_balance_unassigned')),
 row('Total general fund balance (audited)',K('audit_gf_fund_balance_total')),
 row('Enterprise retained earnings, all funds (certified)',K('enterprise_retained_earnings_certified')),
 row('Retained earnings as % of enterprise budgets (derived)',lambda y: erepct(y),'P'),
],RT))
P('')
P(f'Sources: {c("DLS-FC")}; {c("DLS-STAB")}; {c("DLS-ERE")}; audited balance sheets, page references in `data/02_audited_statements_fy2016_fy2025.csv`. The state file shows the same certification date for FY2019 and FY2020, which may be a data-entry duplicate.')
P('')
P('![Reserves](charts/03_reserves.png)')
P('')
P('### Debt and long-term obligations')
P('')
P(tbl(H,[
 row('Long-term debt outstanding (state report)',K('debt_outstanding_schedA')),
 row('Bonds outstanding, governmental (audited)',K('audit_bonds_outstanding_governmental')),
 row('Bonds outstanding, enterprise (audited, derived)',K('audit_bonds_outstanding_business_type')),
 row('General fund debt service',K('gf_debt_service_schedA')),
 row('Debt authorized but unissued',K('debt_authorized_unissued')),
 row('Net pension liability (Town share)',K('audit_net_pension_liability')),
 row('Bristol County system funded ratio',K('audit_pension_plan_funded_pct'),'P'),
 row('Total OPEB liability',K('audit_opeb_total_liability')),
 row('OPEB trust assets',K('audit_opeb_trust_assets')),
 row('Net OPEB liability',K('audit_net_opeb_liability')),
 row('OPEB employer contribution',K('audit_opeb_employer_contribution')),
 row('OPEB actuarially determined contribution',K('audit_opeb_actuarially_determined_contribution')),
 row('Governmental unrestricted net position',K('audit_gov_unrestricted_net_position')),
],RT))
P('')
P(f'Sources: {c("DLS-DEBT")}; {c("DLS-AUD")}; audited statements FY2016 to FY2025 (page references in `data/02_audited_statements_fy2016_fy2025.csv`). The FY2016 OPEB figures predate the current accounting standard and are not comparable with later years; the FY2018 audit records the restatement {c("AUDIT-FY2018","GASB 75 implementation note")}. The audited bond totals include items the state debt report presents differently, so the two series differ by ${M(min(A('audit_bonds_outstanding_total',y)-A('debt_outstanding_schedA',y) for y in range(2018,2026)))}M to ${M(max(A('audit_bonds_outstanding_total',y)-A('debt_outstanding_schedA',y) for y in range(2018,2026)))}M from FY2018 to FY2025.')
P('')
P('![Debt, pension and OPEB](charts/04_debt_pension_opeb.png)')
P('')
P('### Audited budget-to-actual results and federal awards')
P('')
P(tbl(H,[
 row('Revenues: final budget',K('budgetary_gf_rev_final_budget')),
 row('Revenues: actual',K('budgetary_gf_rev_actual')),
 row('Revenue variance (derived)',lambda y: A('budgetary_gf_rev_actual',y)-A('budgetary_gf_rev_final_budget',y)),
 row('Expenditures: final budget',K('budgetary_gf_exp_final_budget')),
 row('Expenditures: actual',K('budgetary_gf_exp_actual')),
 row('Expenditure variance, under budget (derived)',lambda y: A('budgetary_gf_exp_final_budget',y)-A('budgetary_gf_exp_actual',y)),
 row('General fund revenues (GAAP)',K('audit_gf_revenues_gaap')),
 row('General fund expenditures (GAAP)',K('audit_gf_expenditures_gaap')),
 row('Federal awards expended',K('federal_awards_expended')),
],RT))
P('')
P('Source: budgetary comparison schedules, governmental fund statements and schedules of federal awards in the FY2016 to FY2025 audit packages (page references in `data/02_audited_statements_fy2016_fy2025.csv`). The budgetary expenditure series steps up in FY2020 because of a change in how the schedule presents transfers and other uses, so variances before and after FY2020 are not strictly comparable. GAAP figures from FY2017 include pension payments the state makes on behalf of teachers.')
P('')
P('### Enterprise funds and workforce')
P('')
P(tbl(H,[
 row('Enterprise revenues, all funds (state report)',K('schedA_enterprise_rev_total_revenues')),
 row('Enterprise expenditures, all funds (state report)',K('schedA_enterprise_exp_total_expenditures')),
 row('Water expenditures',K('schedA_enterprise_exp_water')),
 row('Sewer expenditures',K('schedA_enterprise_exp_sewer')),
 row('Waterways expenditures',K('schedA_enterprise_exp_harbor')),
 row('Other enterprise expenditures (solid waste, DCTV)',K('schedA_enterprise_exp_other')),
 row('Employees (state personnel report, count)',K('employees_total'),'D'),
 row('Salaries and wages',K('salaries_wages_total')),
],RT))
P('')
P(f'Sources: {c("DLS-SCHA-ENT")}; {c("DLS-PERS")}. The FY2020 and FY2021 employee counts are identical in the state file.')
P('')

# ---------- department and fund-level ----------
P('## Department and fund-level spending analysis')
P('')
P('### General fund by function, FY2016 and FY2026')
P('')
rows=[]
for cat in cats:
    a=float(F[('2016',cat)]['amount_usd']); b=float(F[('2026',cat)]['amount_usd'])
    rows.append([cat,M(a),f'{fs(2016,cat):.1f}%',M(b),f'{fs(2026,cat):.1f}%',f'{pct(a,b):+.0f}%',f'{pct(real(a,2016),b):+.0f}%'])
P(tbl(['Function (state classification)','FY2016 $M','Share','FY2026 $M','Share','Nominal change','Real change (derived)'],rows,[1,2,3,4,5,6]))
P('')
fx16=float(F[('2016',FIX)]['amount_usd']); fx26=float(F[('2026',FIX)]['amount_usd'])
ed16=float(F[('2016',EDU)]['amount_usd']); ed26=float(F[('2026',EDU)]['amount_usd'])
P(f'Source: {c("DLS-SCHA-GF")}; FY2026 unaudited. Verified: fixed costs grew by ${M(fx26-fx16)}M and education by ${M(ed26-ed16)}M, together {((fx26-fx16)+(ed26-ed16))/(e(2026)-e(2016))*100:.0f}% of the ${M(e(2026)-e(2016))}M total increase (derived). After inflation, fixed costs are the only large function that grew substantially; debt service fell as older bonds were retired. All years are in `data/03_general_fund_by_function.csv`.')
P('')
P('### Town operating budget by category, FY2016 to FY2027')
P('')
CAT=['Schools','Employee Benefits','Public Safety','General Government','Public Works','Community Services','Debt Service','Property & Liability Insurance','total']
H2=['Category ($M)']+[f'FY{y[2:]}' for y in YRS]
P(tbl(H2,[[('Total' if k=='total' else k)]+[M(tc[y][k]) for y in YRS] for k in CAT],RT))
P('')
P(f'Sources: Town "Schedule A" operating budget documents {c("TOWN-SCHA-FY17")}, {c("TOWN-SCHA-FY19","PDF pp. 8 to 17")}, {c("TOWN-SCHA-FY21","PDF pp. 8 to 17")}, {c("TOWN-SCHA-FY23","PDF pp. 8 to 17")}, {c("TOWN-SCHA-FY24")}, {c("TOWN-BUD-FY25")}, {c("TOWN-BUD-FY26")}, {c("TOWN-BUD-FY27")}. FY2016 to FY2025 are actual expenditures; FY2026 is the revised budget and FY2027 the budget adopted at the June 2, 2026 Town Meeting. FY2017 to FY2021 figures were read from scanned documents and cross-footed to the printed totals. Schools includes Dartmouth Public Schools and the regional vocational and agricultural school assessments.')
P('')
P('![Town operating budget by category](charts/02_operating_budget_by_category.png)')
P('')
P('### Largest department changes, FY2022 actual to FY2027 budget')
P('')
dd=[x for x in dep if 'TOTAL' not in x['department']]
dd.sort(key=lambda x:-abs(float(x['change_fy2022_to_fy2027_usd'])))
tot_inc=float([x for x in dep if x['department'].startswith('GRAND')][0]['change_fy2022_to_fy2027_usd'])
rows=[[x['department'],x['section'],Dl(float(x['FY2022_actual'])),Dl(float(x['FY2025_actual'])),Dl(float(x['FY2026_budget_revised'])),Dl(float(x['FY2027_budget'])),Dl(float(x['change_fy2022_to_fy2027_usd'])),(f"{float(x['change_fy2022_to_fy2027_pct']):+.1f}%" if x['change_fy2022_to_fy2027_pct'] else 'n/a')] for x in dd[:16]]
P(tbl(['Department or line','Category','FY2022 actual $','FY2025 actual $','FY2026 budget $','FY2027 budget $','Change $','Change %'],rows,[2,3,4,5,6,7]))
P('')
dps=[x for x in dep if x['department']=='Dartmouth Public Schools'][0]; pol=[x for x in dep if x['department']=='Police Department'][0]; pen=[x for x in dep if x['department'].startswith('Pensions')][0]
P(f'Source: {c("TOWN-BUD-FY25","FY2022 and FY2023 actual columns")}, {c("TOWN-BUD-FY26","FY2024 actual column")}, {c("TOWN-BUD-FY27","FY2025 actual, FY2026 revised and FY2027 columns")}. All {len(dd)} departments and lines are in `data/04_department_budget_fy2022_fy2027.csv`.')
P('')
P(f'- **Verified.** Of the ${M(tot_inc)}M increase in the operating budget from FY2022 actual to FY2027 budget, Dartmouth Public Schools accounts for ${M(float(dps["change_fy2022_to_fy2027_usd"]))}M ({float(dps["change_fy2022_to_fy2027_usd"])/tot_inc*100:.0f}%), Health and Life Insurance ${M(float(hl["change_fy2022_to_fy2027_usd"]))}M ({float(hl["change_fy2022_to_fy2027_usd"])/tot_inc*100:.0f}%), the Police Department ${M(float(pol["change_fy2022_to_fy2027_usd"]))}M ({float(pol["change_fy2022_to_fy2027_usd"])/tot_inc*100:.0f}%) and the pension assessment ${M(float(pen["change_fy2022_to_fy2027_usd"]))}M ({float(pen["change_fy2022_to_fy2027_usd"])/tot_inc*100:.0f}%); debt service fell by ${M(abs(tc["2027"]["Debt Service"]-tc["2022"]["Debt Service"]))}M (shares derived).')
P('- **Verified.** The Health and Life Insurance line includes a $700,000 annual contribution to the OPEB trust and the Medicare surcharge, so it is not purely a premium cost.')
P('- **Caution.** These comparisons set an actual year against a budget year. Budgets that are not fully spent overstate growth. The Finance Committee Reserve Fund ($510,000) is budgeted under General Government but is only ever spent through transfers to other departments, so it appears as growth in that category with no matching actual.')
P('- **Unavailable.** Position counts by department, overtime and the cost of collective bargaining settlements are not published (records request R09). Department actuals before FY2022 were captured only at category level.')
P('')
P('### Enterprise funds (audited)')
P('')
EY=[str(y) for y in range(2016,2026)]
ef=rd('05_enterprise_funds_audited.csv')
def ev(fund,y,k):
    for x in ef:
        if x['fiscal_year']==y and x['fund'].startswith(fund): return float(x[k])
    return None
FUNDS=[('Sewer','Sewer'),('Water','Water'),('Solid Waste','Solid waste (separate fund from FY2023)'),('Nonmajor','Other enterprise funds (see note)')]
HE=['$ millions']+[f'FY{y[2:]}' for y in EY]
for title,k in [('Operating income (loss)','operating_income_loss'),('Unrestricted net position at year end','unrestricted_net_position'),('Operating revenues','operating_revenues')]:
    P(f'**{title}**'); P('')
    P(tbl(HE,[[lab]+[M(ev(f,y,k)) for y in EY] for f,lab in FUNDS],list(range(1,11)))); P('')
P(f'Source: proprietary fund statements in the FY2016 to FY2025 audit packages; page references and links for every figure are in `data/05_enterprise_funds_audited.csv` (FY2025: {AUD25(28)}). "Other enterprise funds" comprises solid waste, waterways and DCTV through FY2022 and waterways and DCTV from FY2023. Operating results include depreciation, so an operating loss does not by itself mean a cash deficit.')
P('')
P(f'- **Verified.** The sewer fund had an operating loss in {sew_loss} of 10 years, the largest being ${M(abs(min(sewer[y]["operating_income_loss"] for y in sewer)))}M in FY2021. In FY2025 it received a net transfer in of ${sewer["2025"]["transfers_net"]:,.0f}.')
P(f'- **Verified.** The water fund\'s unrestricted net position was negative at June 30, 2020 and it recorded an operating loss of ${abs(water["2023"]["operating_income_loss"]):,.0f} in FY2023 {c("AUDIT-FY2023","PDF p. 28")}. A mid-year water rate increase was adopted in December 2025 {c("WATER-RATE-2025-12")}.')
P(f'- **Verified.** In October 2022 the Capital Planning Committee reported that only $128,113 of sewer retained earnings remained {c("CPC-LETTER-2022")}.')
P(f'- **Verified.** The water fund overspent its FY2025 appropriation. The Fall 2025 Town Meeting warrant proposed transferring $102,823 from water retained earnings "to fund a prior year appropriation deficit" (Article 5) and $4,306 from solid waste retained earnings for the same purpose (Article 6). The Finance Committee wrote that water "expenses exceeded revenues in FY25 due to the purchase of water from the City of New Bedford" and that the transfer "is required by the Massachusetts Department of Revenue" {c("FATM-2025","Articles 5 and 6, PDF p. 6; Finance Committee comments, PDF p. 19")}.')
P(f'- **Verified (secondary source).** A news report states that Town Meeting approved Article 5 on October 21, 2025, that the Town Administrator attributed the additional purchases to Town wells that were out of service, and that a Finance Committee member estimated water retained earnings had fallen from about $2 million four or five years earlier to about $150,000 after the transfer {c("SCT-FATM-2025","news report")}. The retained earnings figures are a speaker\'s estimate; certified retained earnings by fund were not located (records request R05).')
P(f'- **Verified.** FY2027 enterprise budgets total $19,141,147, of which $3,047,783 is transferred to the general fund for indirect costs such as health insurance and retirement; the Finance Committee states that user fees were "adjusted to cover increased costs, resulting in a 13% increase over FY26" and that a DPW Business Manager position was added for enterprise fund oversight {c("FINCOM-LETTER-FY27","FY2027 Budget Outlook; Key Initiatives")}.')
P(f'- **Verified (secondary source).** A news report states the Town pays a landfill tipping fee of about $25.15 per ton against a market rate of about $110 {c("WEEK-RATES","news report")}.')
P('- **Unavailable.** Retained earnings by individual fund, rate studies, the indirect cost allocation method and enterprise capital plans (records request R05).')
P('')
P('![Enterprise funds](charts/05_enterprise_funds.png)')
P('')
P('### Fire districts')
P('')
fd=rd('09_fire_district_levies.csv'); FY11=[str(y) for y in range(2016,2027)]
names=[]; 
for x in fd:
    if x['district'] not in names: names.append(x['district'])
def fv(nm,y,k='total_levy'):
    for x in fd:
        if x['district']==nm and x['fiscal_year']==y: return x[k]
P(tbl(['Tax levy ($M)']+[f'FY{y[2:]}' for y in FY11],[[nm.replace('Dartmouth Fire #','Fire District ').replace('All three Dartmouth fire districts (sum)','All three districts (derived)')]+[M(float(fv(nm,y))) for y in FY11] for nm in names],list(range(1,12))))
P('')
r26=[fv(nm,'2026','residential_rate_per_1000') for nm in names[:3]]
P(f'Source: {c("DLS-DIST")}; district descriptions {c("FIRE-PAGE")}; rates {c("TAX-RATE-HIST")}. FY2026 residential district rates are ${float(r26[0]):.2f}, ${float(r26[1]):.2f} and ${float(r26[2]):.2f} per $1,000 for Districts 1, 2 and 3. Verified: District 1\'s levy rose from ${float(fv(names[0],"2025")):,.0f} in FY2025 to ${float(fv(names[0],"2026")):,.0f} in FY2026. The reason is not documented in the sources reviewed (Unavailable).')
P('')
P('![Fire district levies](charts/08_fire_district_levies.png)')
P('')
P('### Federal awards')
P('')
P(tbl(['']+[f'FY{y[2:]}' for y in EY],[['Federal awards expended ($M)']+[M(fed(int(y))) for y in EY]],list(range(1,11))))
P('')
fa=[x for x in rd('10_federal_awards_by_program.csv') if x['audit_year']=='2025']; fa.sort(key=lambda x:-float(x['amount_expended']))
P(f'Source: schedules of expenditures of federal awards and Clearinghouse award data {c("FAC-API")}. The largest FY2025 programs were Coronavirus State and Local Fiscal Recovery Funds (${float(fa[0]["amount_expended"]):,.0f} received directly and ${float(fa[1]["amount_expended"]):,.0f} passed through Bristol County), special education grants (${float(fa[2]["amount_expended"]):,.0f}) and the National School Lunch Program (${float(fa[3]["amount_expended"]):,.0f}) {AUD25(94)}. Program-level detail for every year is in `data/10_federal_awards_by_program.csv`.')
P('')

# ---------- governance ----------
P('## Who is responsible for what')
P('')
gov=rd('17_town_governance_map.csv')
P(tbl(['Body or office','Type','How constituted','Financial responsibilities','Notes','Sources'],[[x['body_or_office'],x['type'],x['composition_or_appointment'],x['financial_responsibilities'],x['notes'],links(x['source_ids'])] for x in gov]))
P('')
P(f'Budget sequence under the Charter: the Town Administrator submits the proposed operating budget to the Finance Committee (s. 5-3); the Finance Committee holds open meetings and reports its recommendations at least seven days before Town Meeting acts (s. 5-6); Representative Town Meeting appropriates {c("CHARTER-2025","ss. 2-2, 5-3, 5-6")}. Verified: no audit committee is identified in the Town\'s board handbook {c("HANDBOOK","pp. 5 to 24")}. Source dates for every row are in `data/17_town_governance_map.csv` and the document inventory.')
P('')

# ---------- peers ----------
P('## Comparison with similar Massachusetts municipalities')
P('')
P(f'**Peer selection (author\'s method).** State data for FY2025 were screened for municipalities with a population of 24,000 to 45,000, state-reported income per resident between 75% and 130% of Dartmouth\'s, and equalized property value per resident between 65% and 145% of Dartmouth\'s. The 11 towns that passed and do not have a city form of government are the "statistical peers". Five South Coast neighbors are shown for local context but are smaller and are not in the median. Other reasonable peer sets would give different medians.')
P('')
def pv(x,k,f='{:,.0f}'):
    v=fl(x[k]); return 'n/a' if v is None else f.format(v)
PC=[('population_2024','Population','{:,.0f}'),('income_per_capita','Income per resident $','{:,.0f}'),('gf_total_per_capita','General fund spending per resident $','{:,.0f}'),('gf_non_education_per_capita','Non-education spending per resident $','{:,.0f}'),('avg_sf_tax_bill','Average single-family bill $','{:,.0f}'),('debt_outstanding_per_capita','Debt per resident $','{:,.0f}'),('state_aid_receipts_per_capita','State aid per resident $','{:,.0f}'),('employees_per_1000_pop','Employees per 1,000 residents','{:.1f}'),('dese_pp_total_sy2025','Spending per pupil $ (school year 2025)','{:,.0f}'),('free_cash_pct_budget','Free cash % of budget','{:.1f}'),('stabilization_pct_budget','Stabilization % of budget','{:.1f}')]
P(tbl(['Municipality','Group']+[p[1] for p in PC],[[('**'+x['municipality']+'**' if x['peer_group'] in('Dartmouth','Summary') else x['municipality']),x['peer_group']]+[pv(x,k,f) for k,_,f in PC] for x in peers],list(range(2,13))))
P('')
P(f'Sources: {c("DLS-PEERS")}; {c("DLS-POP")}; {c("DLS-SFTB")}; {c("DLS-DEBT")}; {c("DLS-AID")}; {c("DLS-PERS")}; {c("DLS-FC")}; {c("DLS-STAB")}; {c("DESE-RADAR")}. Fiscal year 2025 unless stated. Per-resident figures are derived using the 2024 Census estimate. All {len(peers[0])-2} comparison fields are in `data/06_peer_comparison_fy2025.csv`, and FY2016 to FY2026 series in `data/07_peer_timeseries_long.csv` and `data/08_school_per_pupil_dese.csv`.')
P('')
P('![Peer comparison](charts/06_peer_comparison.png)')
P('')
G=[('gf_total_real_per_capita_growth_pct_fy2016_fy2025','Real general fund spending per resident, FY2016 to FY2025'),('avg_sf_tax_bill_real_growth_pct','Real average single-family bill, FY2016 to FY2025'),('fte_pupils_change_pct_sy2016_sy2025','In-district pupils (full-time equivalent), school year 2016 to 2025'),('pp_total_real_growth_pct_sy2016_sy2025','Real spending per pupil, school year 2016 to 2025')]
P(tbl(['Change over the period (derived)','Dartmouth','Median of 11 statistical peers'],[[lab,f'{fl(dm[k]):+.1f}%',f'{fl(med[k]):+.1f}%'] for k,lab in G],[1,2]))
P('')
P('**What the comparison shows (verified, with derived per-resident figures).**')
P('')
P(f'- Dartmouth\'s general fund spending per resident (${fl(dm["gf_total_per_capita"]):,.0f}) is the second lowest of the 12 towns in the statistical group and stays below the peer median (${fl(med["gf_total_per_capita"]):,.0f}) after adding fire district levies (${fl(adj["gf_total_per_capita"]):,.0f}, an estimate).')
P(f'- Non-education spending per resident (${fl(dm["gf_non_education_per_capita"]):,.0f}) and employees per 1,000 residents ({fl(dm["employees_per_1000_pop"]):.1f}) are the lowest of all 17 municipalities; state aid per resident (${fl(dm["state_aid_receipts_per_capita"]):,.0f}) is also the lowest.')
P(f'- The average single-family bill (${fl(dm["avg_sf_tax_bill"]):,.0f}) and debt per resident (${fl(dm["debt_outstanding_per_capita"]):,.0f}) are the lowest in the statistical group. Free cash ({fl(dm["free_cash_pct_budget"]):.1f}% of budget) and stabilization ({fl(dm["stabilization_pct_budget"]):.1f}%) are mid-range.')
P(f'- Spending per pupil (${fl(dm["dese_pp_total_sy2025"]):,.0f}) is the fourth lowest of the 12; the school department reports that Dartmouth\'s FY2023 per-pupil spending of $18,364.92 ranked 270th of 322 districts against a state average of $21,116.44 {c("SCHOOL-FY26-BUDGET","per-pupil comparison section")}.')
P(f'- The Town\'s own comparison states that comparable communities\' average tax rate is $10.63 against Dartmouth\'s $8.03 and estimates "budget capacity to align with average tax rate" at $26,200,000 {c("TOWN-DEBT-2026","comparable communities comparison")}. That is the Town\'s statement, using its own comparison group.')
P('')
P('**Normalization limits.**')
P('')
P('- Services differ. Dartmouth has no fire department in its general fund; water, sewer and solid waste are in enterprise funds; several peers run municipal electric utilities or belong to regional school districts. The fire district adjustment adds levies, not actual district spending, and is an estimate.')
P('- Lower spending is not the same as greater efficiency. It can also reflect lower service levels, deferred capital investment or deferred funding of retiree obligations. The capital scenario and OPEB figures above are relevant to that reading.')
P('- Employees per 1,000 residents comes from a state personnel report that towns complete differently, and Dartmouth\'s count excludes fire district staff.')
P(f'- General fund education spending divided by pupils (${fl(dm["gf_education_per_fte_pupil"]):,.0f} for Dartmouth against a peer median of ${fl(med["gf_education_per_fte_pupil"]):,.0f}) is not a reliable comparison because towns record school employee benefits and regional assessments in different functions. The state education department\'s per-pupil series is the better measure and is used above.')
P('- Inflation adjustment uses the national consumer price index, not a municipal cost index; health insurance and construction costs have risen faster.')
P('')

# ---------- audits ----------
P('## Independent audits and external reviews')
P('')
P(tbl(['Fiscal year','Auditor','Financial statements dated','Accepted by Clearinghouse','Days after standard due date','Opinion','Low-risk auditee','Findings recorded','Report'],
 [[f'FY{x["fiscal_year"]}',x['auditor'],x['financial_statement_report_date'],x['fac_accepted_date'],x['days_after_standard_due_date'],x['opinion'],x['low_risk_auditee'],x['findings_in_fac'],f'[PDF]({x["report_pdf_url"]})'] for x in aud],[4,7]))
P('')
P(f'Sources: {c("FAC-API")}; due date rule {c("ECFR-512","(a)(1): the earlier of 30 days after the auditor\'s report or nine months after year end")}; low-risk criteria {c("ECFR-520","(a)")}. Federal pandemic guidance allowed extensions for fiscal years ending through June 30, 2021, so the day counts for FY2019 to FY2021 are measured against the unextended date. The low-risk answers match the Clearinghouse data field and were confirmed on the page image of each auditor\'s summary (page numbers in `data/11_audit_filing_timeline.csv`).')
P('')
P('![Audit timeliness](charts/07_audit_timeliness.png)')
P('')
P(f'- **Verified.** All ten opinions are unmodified. The Clearinghouse records zero findings for every year, and the Director of Budget and Finance described the FY2024 audit as performed "in a timely and collaborative manner" {c("JOINT-2025-07-28","p. 3")}. The Town\'s recap of the August 31, 2026 Select Board meeting reports that the auditor presented the FY2025 audit and that the Town received a clean opinion; it gives no figures {c("SB-RECAP-2026-08-31","audit item")}.')
P('- **Unavailable.** No management letters or communications to those charged with governance were located for any year (records request R01).')
P(f'- **Verified.** The only external financial management review located is the state\'s 2007 review, which made 22 recommendations including a multi-year forecast, limits on the use of one-time revenue, a purchase order process and quarterly projections {c("DLS-FMR-2007","recommendation list")}. No status report on those recommendations was located (Unavailable). The policy documents posted by the Town cover the Finance Committee Reserve Fund {c("RESERVE-POLICY")} and one-time revenue {c("ONETIME-POLICY")}; no written target for free cash or stabilization balances was located (Unavailable).')
P(f'- **Verified.** The Select Board\'s 2025 to 2026 goals call for an annual efficiency review, a Budget Advisory Group, operational studies, records request protocols and an online budget portal {c("SB-GOALS","goals 1.1, 1.3, 4.1, 5.2, 5.3")}.')
P('')

# ---------- concerns ----------
P('## Documented financial-management concerns')
P('')
P('Each item below is documented in a primary record or is a documented absence. None is a finding of misconduct. Classification distinguishes a verified fact, a statement by a Town official or committee, a verified inconsistency whose cause is not established, and records not located.')
P('')
con=rd('13_documented_concerns.csv')
P(tbl(['ID','Area','Documented concern','Classification','Evidence (document date)','Page or section','Context and limits'],[[x['concern_id'],x['category'],x['documented_concern'],x['classification'],links(x['source_ids'],True),x['page_or_section'],x['context_and_limits']] for x in con]))
P('')
P('Machine-readable version with direct URLs: `data/13_documented_concerns.csv`.')
P('')

# ---------- hypotheses ----------
P('## Hypotheses that are not yet established')
P('')
P('These are reasonable readings of the verified record. Each needs the named records before it can be treated as a finding.')
P('')
HY=[
['H1','Revenue estimates are consistently conservative, and the resulting recurring free cash offsets part of the structural gap that officials describe.',f'Budgetary revenues exceeded the final budget in {rev_over} of 10 audited years; free cash was certified at ${M(min(fc))}M to ${M(max(fc))}M every year; reserves grew.','R06, R13'],
['H2','The FY2024 federal awards schedule omission was identified after the FY2024 audit package was issued, which would explain why that package reports no findings.','FY2025 package lists finding 2024-001 as a resolved prior-year material weakness; FY2024 package as filed and the July 28, 2025 minutes report none.','R02, R12'],
['H3','Sewer rates were set below the full cost of service, including depreciation, for most of the decade, and the FY2027 increase is a correction.',f'Operating losses in {sew_loss} of 10 years; unrestricted net position down from ${M(sewer["2016"]["unrestricted_net_position"])}M to ${M(sewer["2025"]["unrestricted_net_position"])}M; 16% rate increase for FY2027.','R05'],
['H4','Part of Dartmouth\'s low per-resident spending reflects services financed outside the general fund and deferred obligations, not only efficient operations.',f'Fire districts add about ${fl(adj["gf_total_per_capita"])-fl(dm["gf_total_per_capita"]):,.0f} per resident (estimate); OPEB contributions below the actuarially determined amount in every year; $516.5M capital scenario.','R03, R07, R11'],
['H5','School staffing and building capacity have not adjusted in proportion to the enrollment decline.',f'In-district pupils fell {abs(fl(dm["fte_pupils_change_pct_sy2016_sy2025"])):.1f}% from school year 2016 to 2025 while real spending per pupil rose {fl(dm["pp_total_real_growth_pct_sy2016_sy2025"]):.1f}%; teachers per 100 pupils {fl(dm["dese_teachers_per_100_sy2025"]):.1f} against a peer median of {fl(med["dese_teachers_per_100_sy2025"]):.1f}. Per-pupil spending is nevertheless below the peer median, so this may not indicate savings potential.','R10'],
['H6','Shared services or consolidation among the three fire districts could lower cost.','Three separate governments with separate budgets and tax rates; combined levy up 90% in ten years. No study was located and district budgets were not reviewed.','R11'],
['H7','The health insurance change will reduce Town cost by about $1 million a year.','Stated by the Town; the supporting analysis is not published, and the FY2027 Health and Life Insurance budget line is higher than FY2026.','R04'],
]
P(tbl(['ID','Hypothesis','Verified basis','Records that would test it'],HY))
P('')

# ---------- top 10 ----------
P('## Top 10 opportunities warranting further investigation')
P('')
P('Ranking method: each area is scored 1 to 5 for financial scale (the size of the documented dollar base) and 1 to 5 for evidence quality (how much rests on primary records already in hand). The priority score is the product; ties are ordered by financial scale and then by dollar base. The "illustrative sensitivity" column is arithmetic on the documented base. It is not a savings estimate, and no savings figure in this report has been verified.')
P('')
opp=rd('14_top10_opportunities.csv')
P(tbl(['Rank','Opportunity','Documented dollar base','Scale (1-5)','Evidence (1-5)','Score','Related requests'],[[x['rank'],x['opportunity'],x['documented_dollar_base'],x['financial_scale_score_1to5'],x['evidence_quality_score_1to5'],x['priority_score'],x['related_records_requests'].replace(' ;',',')] for x in opp],[3,4,5]))
P('')
for x in opp:
    P(f'### {x["rank"]}. {x["opportunity"]}'); P('')
    P(f'- **Documented dollar base:** {x["documented_dollar_base"]}.')
    P(f'- **Illustrative sensitivity:** {x["illustrative_sensitivity"]}.')
    P(f'- **Evidence status:** {x["evidence_status"]}')
    P(f'- **Questions to investigate:** {x["questions_to_investigate"]}')
    P(f'- **Sources:** {links(x["source_ids"],True)}.')
    P(f'- **Records requests:** {x["related_records_requests"].replace(" ;",",")}.')
    P('')

# ---------- gaps ----------
P('## Significant gaps in public financial information')
P('')
gaps=rd('16_information_gaps.csv')
P(tbl(['ID','Area','Gap','Significance','Workaround used here','Related request','Evidence'],[[x['gap_id'],x['area'],x['gap_description'],x['significance'],x['workaround_used_in_this_baseline'],x['related_records_request'] or 'none',links(x['source_ids'])] for x in gaps]))
P('')

# ---------- records requests ----------
P('## Recommended next public-records requests')
P('')
rr=rd('15_records_requests.csv')
P(f'Requests are listed in priority order. Each is framed to ask for existing records, in electronic form, under the state public records law, which requires a response within 10 business days {c("MGL-66-10","(a) and (b)")}. None duplicates the two requests logged in the project repository on November 10, 2026: the financial records request, which covers accounts-payable and general-ledger transactions, vendor payment registers, the vendor master list and enterprise fund expenditures {c("REPO-PRR-2026-11-10")}, and the Department of Public Works staffing and payroll request, which covers that department\'s roster, authorized, filled and vacant positions, and base, overtime and gross pay for FY2022 to FY2026 {c("REPO-PRR-DPW-2026-11-10")}. Request R09 therefore excludes the Department of Public Works. The fire districts are separate public bodies and must be asked directly.')
P('')
P(tbl(['ID','Topic','Records to request','Period','Likely custodian','Format','Why needed','Supports'],[[x['request_id'],x['topic'],x['records_to_request'],x['period'],x['likely_custodian'],x['preferred_format'],x['why_needed'],x['related_concerns_and_opportunities']] for x in rr]))
P('')
P('Suggested sequencing: R01 to R03 first (small, specific, and likely to exist as single documents); R05 to R07 and R13 next (the records that test the largest dollar areas); the remainder as capacity allows. Narrow requests for named documents are less likely to incur fees or extensions than broad ones.')
P('')

# ---------- inventory ----------
P('## Inventory of original public documents')
P('')
inv=[x for x in rd('12_source_inventory.csv') if x['source_type']!='Alias']
order=['Independent audit','Town of Dartmouth record','State financial management review','State or federal data / regulation','News report (secondary)','Project repository']
P(f'{len(inv)} documents and datasets were used. Titles link directly to the original. The same list with plain URLs is `data/12_source_inventory.csv`.')
P('')
for t in order:
    sub=[x for x in inv if x['source_type']==t]
    if not sub: continue
    P(f'### {t} ({len(sub)})'); P('')
    P(tbl(['ID','Title (direct link)','Publisher','Document date','Pages or section used','Notes'],[[x['source_id'],f'[{x["title"]}]({x["url"]})',x['publisher'],x['document_date'],x['pages_or_section'],x['notes']] for x in sub]))
    P('')
assert sum(1 for x in inv if x['source_type'] in order)==len(inv)

# ---------- methods ----------
P('## Methods, conventions and limits')
P('')
ML=[
'**Sources.** Primary records only for figures: Town documents, audited financial statements filed with the Federal Audit Clearinghouse, and state and federal datasets. News reports are used only for attributed statements and are marked secondary.',
'**Verification.** Every audited figure in `data/02_audited_statements_fy2016_fy2025.csv` carries the PDF page and a check that the literal value appears in the report text on that page. Scanned budget documents were read by optical character recognition, checked visually and cross-footed to printed totals.',
'**Inflation.** Fiscal-year average of the national consumer price index for all urban consumers (series CUUR0000SA0), expressed in FY2026 dollars.',
'**Population.** Census estimate for the calendar year before the fiscal year, as published by the state, held at the 2024 estimate from FY2025 on.',
'**Free cash labelling.** Free cash is labelled by the fiscal year in which it becomes available to appropriate; it is certified as of the preceding July 1.',
'**Fire districts.** District tax levies are added to Dartmouth in one comparison row as an estimate of fire protection cost; district spending was not reviewed.',
'**FY2026 and FY2027.** FY2026 state figures are as filed by the Town and unaudited. FY2027 figures are the adopted budget, certified free cash and certified retained earnings only.',
'**Small differences.** The FY2027 budget total is $113,389,515 in the Finance Committee letter and the budget summary; summing the department lines captured in table 04 gives $113,389,265; the $250 difference is in Community Services, where one small line was not separately captured (the same category differs by $115 to $250 in other years). The FY2023 audit shows two net OPEB figures (concern C16); the note figure is used.',
'**Not done.** No transaction-level review, no review of school line items, no review of fire district finances, no legal analysis of procurement compliance, and no interviews. The two records requests already logged in the repository address transaction-level data and Department of Public Works staffing and payroll.',
'**Human review.** Extraction and drafting were done by an AI research assistant. No person has yet re-checked the figures against the cited pages; see the review status note under "How to read this report".',
'**Standard of care.** Unusual figures are described as facts with their documented context. Where a cause is not documented, the report says so. Nothing here should be read as an allegation of misconduct.',
]
for m_ in ML: P(f'- {m_}')
P('')
P('## Corrections log')
P('')
P('Corrections made while this baseline was being prepared. They are recorded here rather than silently rewritten, as the repository standard requires. No version of the report containing the earlier statements was published.')
P('')
P(tbl(['Date','Item','Earlier draft statement','Corrected statement','How the error was found','Evidence'],[
['2026-11-10','Low-risk auditee status (concern C02, table 11, executive summary)','The Town did not qualify as a low-risk auditee in six of ten years','The auditor\'s summary reports that the Town did not qualify as a low-risk auditee in all ten years, FY2016 to FY2025','Text extraction of the audit PDFs drops check marks. The answer was re-read from the page image of each auditor\'s summary and compared with the Clearinghouse structured field',f'{lk("FAC-API")}; PDF page of each summary is in `data/11_audit_filing_timeline.csv`'],
['2026-11-11','Board of Public Works size and vacancies (concern C21, governance map)','Two of the three seats on the Board of Public Works were vacant in August 2026','The Board was expanded from three to five members effective July 1, 2026. The two vacancies reported on August 3, 2026 were the newly created seats and were filled that day. The item is now a governance transition note','The Department of Public Works page, used for the earlier statement, still describes a three-person board. The Fall 2025 Town Meeting article, the Town notice seeking applicants and the Board of Public Works page show five',f'{lk("FATM-2025")} (Article 9, PDF p. 9); {lk("BPW-APPLICANTS-2026")}; {lk("BPW-PAGE")}; {lk("SB-RECAP-2026-08-03")}; {lk("DPW-PAGE")}'],
['2026-11-11','Records request R09 (positions and payroll)','R09 covered all departments','R09 excludes the Department of Public Works, whose staffing and payroll were requested separately on November 10, 2026','Second request log found in the repository after R09 was drafted',lk("REPO-PRR-DPW-2026-11-10")],
['2026-11-11','ClearGov portal description (gaps G05 and G07)','The portal was described as periodic budget uploads','The Town describes budget, revenue, expenditure and line-item data updated monthly, with enterprise funds excluded in the first phase. The portal contents were not reviewed','Budget Information page re-read on November 11, 2026',lk("TOWN-BUDGET-PAGE")],
]))
P('')
P('## Repository contents')
P('')
P(tbl(['Path','Contents'],[
['`README.md`','Data dictionary, methods and conventions'],
['`data/01_year_by_year_baseline_wide.csv`, `..._long.csv`','96 metrics by fiscal year, FY2016 to FY2027'],
['`data/02_audited_statements_fy2016_fy2025.csv`','Audited figures with PDF page and text-match check'],
['`data/03_general_fund_by_function.csv`','State function and Town category spending by year, nominal, real and per resident'],
['`data/04_department_budget_fy2022_fy2027.csv`','Department totals, FY2022 actual to FY2027 budget'],
['`data/05_enterprise_funds_audited.csv`','Audited enterprise fund results'],
['`data/06_peer_comparison_fy2025.csv`, `07_peer_timeseries_long.csv`, `08_school_per_pupil_dese.csv`','Peer comparison snapshot and time series'],
['`data/09_fire_district_levies.csv`','Fire district levies and rates'],
['`data/10_federal_awards_by_program.csv`, `11_audit_filing_timeline.csv`','Federal awards and audit filing record'],
['`data/12_source_inventory.csv`','Document inventory with direct URLs'],
['`data/13_documented_concerns.csv` to `17_town_governance_map.csv`','Concerns, opportunities, records requests, information gaps, governance map'],
['`charts/`','Eight charts generated from the tables above'],
['`scripts/`','The Python scripts that built the tables, charts and report (they read cached downloads that are not included)'],
]))
P('')
out='\n'.join(O)
import re
assert not re.search(r'(?<![\*\w])\*(?!\*)[^*\n]+\*(?!\*)',out), 'italic found'
open(f'{D}/dartmouth-municipal-financial-baseline-fy2016-fy2027.md','w').write(out)
print('chars',len(out),'lines',out.count('\n'),'links',out.count(']('))
