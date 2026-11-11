import csv, json, re, io, collections, os
W='/home/user/workspace/work'; OUT='/home/user/workspace/dartmouth-financial-baseline/data'
def num(s):
    if s is None: return None
    s=str(s).strip().replace('$','').replace(',','').replace('%','')
    if s in ('','-','--'): return None
    try: return float(s)
    except: return None
def rd(path):
    txt=open(path,encoding='utf-8-sig',errors='ignore').read().replace('\r','')
    lines=txt.split('\n'); rows=[]; hdr=None; alt=None
    for ln in lines:
        if not ln.strip(): continue
        if ln.startswith('HDR:'):
            h,rest=ln[4:].split(',',1)
            ah=h.split('|'); r=next(csv.reader([rest]))
            rows.append(dict(zip([x.strip() for x in ah],r))); continue
        r=next(csv.reader([ln]))
        if hdr is None: hdr=[x.strip() for x in r]; continue
        rows.append(dict(zip(hdr,r)))
    return rows
D=lambda n: rd(f'{W}/raw/dls/dartmouth__{n}.csv')
Y=list(range(2016,2028))
T=collections.defaultdict(dict)   # metric -> {fy: value}
META={}
def put(metric,fy,val,unit='USD',basis='',src=''):
    if val is None: return
    T[metric][int(fy)]=val; META[metric]=(unit,basis,src)
# population (calendar-year estimates)
pop=D('population')[0]; POP={int(k):num(v) for k,v in pop.items() if k.isdigit()}
for fy in Y:
    cy=min(fy-1,2024); put('population_estimate',fy,POP.get(cy),'persons','US Census estimate for calendar year FY-1 (capped at 2024), as published by DLS','DLS-POP')
# CPI fiscal-year average
cpi={}
for ln in open(f'{W}/bls/allitems.txt'):
    p=ln.split('\t')
    if p[0].strip()=='CUUR0000SA0' and p[2].strip().startswith('M') and p[2].strip()!='M13':
        try: cpi[(int(p[1]),int(p[2].strip()[1:]))]=float(p[3])
        except: pass
CPI={}
for fy in Y:
    ms=[(fy-1,m) for m in range(7,13)]+[(fy,m) for m in range(1,7)]
    v=[cpi[k] for k in ms if k in cpi]
    if len(v)>=11: CPI[fy]=sum(v)/len(v)
for fy,v in CPI.items(): put('cpi_u_us_fiscal_year_avg',fy,round(v,3),'index 1982-84=100','BLS CPI-U US city average, NSA, mean of July-June months','BLS-CPI')
json.dump({'CPI':CPI,'last':max(cpi)},open(f'{W}/out/cpi.json','w'))
# Schedule A general fund
for r in D('schedA_general_fund'):
    fy=int(r['Fiscal Year'])
    if fy<2016: continue
    if r.get('islAmountType')=='Revenues':
        for k in ['Taxes','Service Charges','Licenses and Permits','Federal Revenue','State Revenue','Special Assessments','Fines and Forfeitures','Miscellaneous','Other Financing Sources','Transfers','Total Revenues']:
            put('schedA_gf_rev_'+re.sub(r'\W+','_',k.lower()),fy,num(r[k]),'USD','DLS Schedule A, general fund revenues (cash/statutory basis)','DLS-SCHA-GF')
    else:
        for k in ['General Government','Public Safety','Education','Public Works','Human Services','Culture and Recreation','Fixed Costs','Intergov Assessments','Other Expenditures','Debt Service','Total Expenditures']:
            put('schedA_gf_exp_'+re.sub(r'\W+','_',k.lower()),fy,num(r[k]),'USD','DLS Schedule A, general fund expenditures (statutory basis)','DLS-SCHA-GF')
for r in D('schedA_enterprise_funds'):
    fy=int(r['Fiscal Year'])
    if fy<2016: continue
    t='rev' if r.get('islAmountType')=='Revenues' else 'exp'
    tk='Total Revenues' if t=='rev' else 'Total Expenditures'
    for k in ['Water','Sewer','Harbor','Other',tk]:
        kk=k if k in r else k+' '
        put(f'schedA_enterprise_{t}_'+re.sub(r'\W+','_',k.lower()),fy,num(r.get(kk)),'USD','DLS Schedule A, enterprise funds','DLS-SCHA-ENT')
for r in D('free_cash_pct_budget'):
    fy=int(r['Fiscal Year']); 
    if fy>=2016:
        put('free_cash_certified',fy,num(r['Certified Free Cash as of 7/1']),'USD','Certified as of July 1 preceding the labelled fiscal year start per DLS table','DLS-FC')
        T['free_cash_date_certified'][fy]=r['Date Certified']; META['free_cash_date_certified']=('date','DLS','DLS-FC')
        put('free_cash_pct_prior_budget',fy,num(r['Certified Free Cash as a % of the Budget']),'percent','DLS','DLS-FC')
for r in D('stabilization_funds'):
    fy=int(r['Schedule A Fiscal Year'])
    if fy>=2016:
        put('stabilization_general',fy,num(r['Stabilization Fund Balance']),'USD','DLS Schedule A balance at fiscal year end','DLS-STAB')
        put('stabilization_special_purpose',fy,num(r['Special Purpose Stabilization Fund Balance']),'USD','DLS','DLS-STAB')
        put('stabilization_total',fy,num(r['Total Stabilization Fund Balance']),'USD','DLS','DLS-STAB')
        put('dls_operating_budget',fy,num(r['Operating Budget']),'USD','DLS "operating budget" (tax recap total less enterprise/CPA)','DLS-STAB')
        put('stabilization_total_pct_budget',fy,num(r['Total Stabilization as % of Budget']),'percent','DLS','DLS-STAB')
for r in D('long_term_debt'):
    fy=int(r['Fiscal Year'])
    if fy>=2016:
        put('debt_outstanding_schedA',fy,num(r['Total Outstanding Debt (Schedule A Part 10)']),'USD','DLS Schedule A Part 10, all funds, fiscal year end','DLS-DEBT')
        put('equalized_valuation',fy,num(r['Equalized Values (EQV)']),'USD','DLS','DLS-DEBT')
        put('gf_debt_service_schedA',fy,num(r['GF Debt Service (Schedule A Part 2)']),'USD','DLS','DLS-DEBT')
for r in D('authorized_unissued_debt'):
    fy=int(r['Fiscal Year'])
    if fy>=2016: put('debt_authorized_unissued',fy,num(r['Unissued Debt']),'USD','DLS','DLS-AUD')
for r in D('levy_limit_excess_capacity'):
    fy=int(r['Fiscal Year'])
    if fy>=2016:
        for k,m in [('Levy Limit w/o Debt & Capital Exclusions','levy_limit'),('Maximum Levy Limit','levy_max_allowable'),('Total Tax Levy','tax_levy_total'),('Excess Levy Capacity','levy_excess_capacity'),('Override Capacity','levy_override_capacity'),('Total Assessed Value','assessed_value_total')]:
            put(m,fy,num(r[k]),'USD','DLS tax recap','DLS-LEVY')
for r in D('new_growth_pct_levy_limit'):
    fy=int(r['Fiscal Year'])
    if fy>=2016: put('new_growth',fy,num(r['Total New Growth']),'USD','DLS','DLS-NG')
for r in D('tax_rates_by_class'):
    fy=int(r['Fiscal Year'])
    if fy>=2016:
        put('tax_rate_residential',fy,num(r['Residential']),'USD per $1,000','DLS; Town rate only, excludes fire district rate','DLS-RATE'); put('tax_rate_commercial',fy,num(r['Commercial']),'USD per $1,000','DLS','DLS-RATE')
for r in D('avg_single_family_tax_bill'):
    fy=int(r['Fiscal Year'])
    if fy>=2016:
        put('avg_single_family_value',fy,num(r['Average Single-Family Value']),'USD','DLS','DLS-SFTB'); put('avg_single_family_tax_bill',fy,num(r['Single-Family Tax Bill']),'USD','DLS; Town tax only, excludes fire district tax','DLS-SFTB')
        put('avg_sf_tax_bill_state_rank',fy,num(r['Rank']),'rank (1=highest)','DLS','DLS-SFTB'); put('dor_income_per_capita',fy,num(r['DOR Income Per Capita']),'USD','DLS','DLS-SFTB')
for r in D('state_aid_net'):
    fy=int(r['Fiscal Year'])
    if fy>=2016:
        put('state_aid_receipts',fy,num(r['Receipts']),'USD','DLS cherry sheet','DLS-AID'); put('state_aid_assessments',fy,num(r['Charges / Assessments']),'USD','DLS','DLS-AID'); put('state_aid_net',fy,num(r['Net State Aid']),'USD','DLS','DLS-AID')
for r in D('enterprise_retained_earnings'):
    fy=int(r['Fiscal Year'])
    if fy>=2016:
        put('enterprise_retained_earnings_certified',fy,num(r['Enterprise Free Cash (Retained Earnings)']),'USD','DLS certified, all enterprise funds combined','DLS-ERE'); put('enterprise_budget_total_dls',fy,num(r['Enterprise Funds Total']),'USD','DLS','DLS-ERE')
for r in D('personnel_fte_wages'):
    fy=int(r['Fiscal Year'])
    if fy>=2016:
        put('employees_total',fy,num(r['Total Employees']),'count','DLS Schedule A personnel; FY2020 and FY2021 values are identical in source','DLS-PERS'); put('salaries_wages_total',fy,num(r['Total Salaries & Wages']),'USD','DLS','DLS-PERS')
for r in D('revenue_by_source_budget'):
    fy=int(r['Fiscal Year'])
    if fy>=2016:
        for k,m in [('Tax Levy','recap_tax_levy'),('State Aid','recap_state_aid'),('Local Receipts','recap_local_receipts'),('All Other','recap_all_other'),('Enterprise & CPA Funds','recap_enterprise_cpa')]:
            put(m,fy,num(r[k]),'USD','DLS tax recap budgeted revenue by source','DLS-REV')
for r in D('overlay_pct_levy'):
    fy=int(r['Fiscal Year'])
    if fy>=2016: put('overlay',fy,num(r['Overlay Appropriation']),'USD','DLS','DLS-OVL')
for r in D('outstanding_receivables_pct_levy'):
    fy=int(r['Fiscal Year'])
    if fy>=2016: put('tax_receivables_total_pct_levy',fy,num(r['Total Receivables as % of Tax Levy']),'percent','DLS','DLS-REC')
# audits
AUD={}
for y in range(2016,2026):
    d=json.load(open(f'{W}/fac/extract_{y}.json'))['result']; AUD[y]=d
    b='Audited financial statements (GAAP)'; s=f'AUDIT-FY{y}'
    put('audit_net_position_total',y,d['net_position_total'],'USD',b,'AUDIT')
    put('audit_gov_unrestricted_net_position',y,d['unrestricted_net_position_governmental'],'USD',b,'AUDIT')
    put('audit_gf_fund_balance_total',y,d['general_fund_total_fund_balance'],'USD',b,'AUDIT')
    put('audit_gf_fund_balance_unassigned',y,d['general_fund_unassigned_fund_balance'],'USD',b,'AUDIT')
    put('audit_gf_revenues_gaap',y,d['general_fund_total_revenues'],'USD',b+'; FY2017+ includes state on-behalf teacher pension','AUDIT')
    put('audit_gf_expenditures_gaap',y,d['general_fund_total_expenditures'],'USD',b+'; FY2017+ includes state on-behalf teacher pension','AUDIT')
    put('audit_bonds_outstanding_total',y,d['bonds_outstanding_total'],'USD',b,'AUDIT')
    put('audit_bonds_outstanding_governmental',y,d['bonds_outstanding_governmental'],'USD',b,'AUDIT')
    put('audit_bonds_outstanding_business_type',y,d['bonds_outstanding_total']-d['bonds_outstanding_governmental'],'USD',b+' (derived: total less governmental)','AUDIT')
    put('audit_net_pension_liability',y,d['net_pension_liability_total'],'USD',b,'AUDIT')
    put('audit_pension_plan_funded_pct',y,d['pension_plan_funded_ratio_pct'],'percent','Bristol County Retirement System plan fiduciary net position as % of total pension liability','AUDIT')
    put('audit_opeb_total_liability',y,d['total_opeb_liability'],'USD',b+('; FY2016 actuarial accrued liability under GASB 45' if y==2016 else ''),'AUDIT')
    put('audit_opeb_trust_assets',y,d['opeb_plan_fiduciary_net_position'],'USD',b,'AUDIT')
    if y>=2017: put('audit_net_opeb_liability',y,d['total_opeb_liability']-d['opeb_plan_fiduciary_net_position'],'USD',b+' (total OPEB liability less plan fiduciary net position, per OPEB note)','AUDIT')
    put('audit_opeb_employer_contribution',y,d['opeb_employer_contribution'],'USD',b,'AUDIT')
    put('audit_opeb_actuarially_determined_contribution',y,d['opeb_actuarially_determined_contribution'],'USD',b,'AUDIT')
    bv=d['budget_vs_actual']
    for k,m in [('final_budget_total_revenues','budgetary_gf_rev_final_budget'),('actual_total_revenues','budgetary_gf_rev_actual'),('final_budget_total_expenditures','budgetary_gf_exp_final_budget'),('actual_total_expenditures','budgetary_gf_exp_actual')]:
        put(m,y,bv.get(k),'USD','Audit RSI budgetary comparison schedule (budgetary basis; includes other financing uses where presented)','AUDIT')
    put('federal_awards_expended',y,d['summary_of_auditor_results']['total_federal_expenditures'],'USD','Schedule of Expenditures of Federal Awards','AUDIT')
# town budget docs
for fy,v in {2022:91547317,2023:93055811,2024:96338227,2025:101592765}.items(): put('town_schedA_budget_doc_actual_total',fy,v,'USD','Town "Schedule A" general fund operating budget document, actual expenditures column','TOWN-BUD')
for fy,v in {2025:104553491,2026:108500032,2027:113389515}.items(): put('town_schedA_budget_doc_budget_total',fy,v,'USD','Town "Schedule A" operating budget document, revised/approved budget','TOWN-BUD')
json.dump({'T':{k:{str(a):b for a,b in v.items()} for k,v in T.items()},'META':META},open(f'{W}/out/core.json','w'))
# write long + wide
with open(f'{OUT}/01_year_by_year_baseline_long.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['fiscal_year','metric','value','unit','basis_note','source_id'])
    for m in T:
        for fy in sorted(T[m]): 
            v=T[m][fy]; w.writerow([fy,m,int(v) if isinstance(v,float) and v.is_integer() else v,*META[m]])
with open(f'{OUT}/01_year_by_year_baseline_wide.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['metric','unit','source_id']+[f'FY{y}' for y in Y])
    for m in T:
        w.writerow([m,META[m][0],META[m][2]]+[ (int(T[m][y]) if isinstance(T[m].get(y),float) and T[m][y].is_integer() else T[m].get(y,'')) for y in Y])
print(len(T),'metrics'); print({k:round(v,1) for k,v in CPI.items()}, max(cpi))
for m in ['population_estimate','schedA_gf_exp_total_expenditures','schedA_gf_rev_total_revenues','audit_net_opeb_liability','audit_bonds_outstanding_business_type','tax_levy_total','levy_excess_capacity','new_growth','debt_authorized_unissued','tax_receivables_total_pct_levy','overlay']:
    print(m,[T[m].get(y) for y in Y])
