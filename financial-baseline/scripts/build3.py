import csv, json, re, collections, datetime as dt
W='/home/user/workspace/work'; OUT='/home/user/workspace/dartmouth-financial-baseline/data'
FAC={2016:('2016-06-CENSUS-0000148019','Melanson Heath','2017-03-22','2017-03-22','2017-04-12'),
2017:('2017-06-CENSUS-0000148019','Melanson Heath','2019-01-10','2019-07-03','2019-07-08'),
2018:('2018-06-CENSUS-0000148019','Melanson Heath','2019-05-29','2019-07-03','2019-07-08'),
2019:('2019-06-CENSUS-0000148019','Melanson','2021-08-13','2021-10-15','2021-10-27'),
2020:('2020-06-CENSUS-0000148019','Melanson','2022-01-19','2022-02-28','2022-03-16'),
2021:('2021-06-GSAFAC-0000350357','Melanson (financial statements); Marcum LLP (single audit)','2023-02-06','2024-12-30','2025-01-14'),
2022:('2022-06-GSAFAC-0000350403','Marcum LLP','2024-01-12','2024-12-30','2025-01-14'),
2023:('2023-06-GSAFAC-0000350526','Marcum LLP','2024-09-11','2025-01-09','2025-01-15'),
2024:('2024-06-GSAFAC-0000370338','CBIZ CPAs P.C.','2025-05-22','2025-05-22','2025-06-03'),
2025:('2025-06-GSAFAC-0000424769','CBIZ CPAs P.C.','2026-07-21','2026-07-21','2026-07-22')}
json.dump({str(k):v for k,v in FAC.items()},open(f'{W}/out/fac_meta.json','w'))
A={y:json.load(open(f'{W}/fac/extract_{y}.json'))['result'] for y in FAC}
# Low-risk status: Clearinghouse structured field, checked against the page image of each auditor's summary (text extraction drops the check marks).
LOWRISK={int(r['audit_year']):r['is_low_risk_auditee'] for r in json.load(open(f'{W}/fac/town_general.json'))}
SUMPAGE={2016:10,2017:10,2018:10,2019:10,2020:10,2021:13,2022:9,2023:95,2024:97,2025:97}
D=lambda s: dt.date.fromisoformat(s)
with open(f'{OUT}/11_audit_filing_timeline.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['fiscal_year','fiscal_year_end','fac_report_id','auditor','financial_statement_report_date','single_audit_report_date','fac_accepted_date','months_fye_to_fs_report','months_fye_to_fac_acceptance','standard_9_month_due_date','days_after_standard_due_date','opinion','low_risk_auditee','findings_in_fac','federal_awards_expended','report_pdf_url','fac_summary_url','auditors_summary_pdf_page','note'])
    for y,(rid,aud,fs,sa,acc) in FAC.items():
        fye=dt.date(y,6,30); due=dt.date(y+1,3,31); r=A[y]['summary_of_auditor_results']
        note=''
        if y in (2019,2020): note='OMB COVID-19 guidance (M-20-17, M-20-26, M-21-20) allowed extensions of single-audit deadlines for fiscal years ending through June 30, 2021; lateness relative to any extended date not computed.'
        if y==2021: note='Same extension caveat applies to FYE June 30, 2021; filed about 42 months after year end.'
        w.writerow([y,fye,rid,aud,fs,sa,acc,round((D(fs)-fye).days/30.44,1),round((D(acc)-fye).days/30.44,1),due,(D(acc)-due).days,A[y]['opinion_type'],LOWRISK[y],0,r.get('total_federal_expenditures'),f'https://app.fac.gov/dissemination/report/pdf/{rid}',f'https://app.fac.gov/dissemination/summary/{rid}',SUMPAGE[y],note])
# audited statements table w/ pages
keys=[('net_position_total','net_position_page'),('net_position_governmental','net_position_page'),('net_position_business_type','net_position_page'),('unrestricted_net_position_governmental','net_position_page'),('general_fund_total_fund_balance','balance_sheet_page'),('general_fund_unassigned_fund_balance','balance_sheet_page'),('general_fund_committed','balance_sheet_page'),('general_fund_assigned','balance_sheet_page'),('general_fund_restricted','balance_sheet_page'),('general_fund_total_revenues','revenues_expenditures_statement_page'),('general_fund_total_expenditures','revenues_expenditures_statement_page'),('general_fund_net_change_in_fund_balance','revenues_expenditures_statement_page'),('bonds_outstanding_total','debt_page'),('bonds_outstanding_governmental','debt_page'),('net_pension_liability_total','pension_page'),('pension_plan_funded_ratio_pct','pension_page'),('total_opeb_liability','opeb_page'),('opeb_plan_fiduciary_net_position','opeb_page'),('opeb_discount_rate_pct','opeb_page'),('opeb_employer_contribution','opeb_page'),('opeb_actuarially_determined_contribution','opeb_page')]
_T={}
def found(y,val,pg):
    """Return (page_to_cite, check_note). Page is where the literal value actually appears in the report text."""
    if y not in _T: _T[y]=open(f'{W}/fac/{y}_compact.txt',errors='ignore').read()
    t=_T[y]
    s=f"{abs(int(val)):,}" if isinstance(val,(int,float)) and abs(val)>=1000 else None
    if not s:
        if isinstance(val,(int,float)) and val!=0 and pg:
            m=re.search(r'\[\[PDF PAGE %d\]\](.*?)(\[\[PDF PAGE|$)'%pg,t,re.S); body=m.group(1) if m else ''
            cands={f'{val:g}',f'{val:.1f}',f'{val:.2f}'}
            if any(re.search(r'(?<![\d.])'+re.escape(c)+r'0?\s*%',body) for c in cands): return pg,'literal percentage found on this page'
            hits=[int(p) for p,b in re.findall(r'\[\[PDF PAGE (\d+)\]\](.*?)(?=\[\[PDF PAGE|$)',t,re.S) if any(re.search(r'(?<![\d.])'+re.escape(c)+r'0?\s*%',b) for c in cands)]
            if hits: b=min(hits,key=lambda p:abs(p-pg)); return b,'literal percentage found on this page (page corrected by text search)'
            return pg,'percentage not matched as a literal string; treat as unverified extraction'
        return pg,'zero or non-numeric; not text-checked'
    pages=[int(re.findall(r'\[\[PDF PAGE (\d+)\]\]',t[:m.start()])[-1]) for m in re.finditer(re.escape(s),t) if re.findall(r'\[\[PDF PAGE (\d+)\]\]',t[:m.start()])]
    if not pages: return pg,'derived or rounded value; not found as a literal string in report text'
    if pg in pages: return pg,'literal value found on this page'
    best=min(pages,key=lambda p:abs(p-(pg or p)))
    return best,'literal value found on this page (page corrected by text search)'
def inpage(y,val,pg): return found(y,val,pg)[1]
with open(f'{OUT}/02_audited_statements_fy2016_fy2025.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['fiscal_year','item','value','pdf_page','text_match_check','report_pdf_url'])
    for y in FAC:
        a=A[y]; url=f'https://app.fac.gov/dissemination/report/pdf/{FAC[y][0]}'
        for k,pk in keys:
            if a.get(k) is None: continue
            w.writerow([y,k,a[k],*found(y,a[k],a.get(pk)),url])
        for fn,lst in (('gf_expenditure','general_fund_expenditures_by_function'),('gf_revenue','general_fund_revenues_by_source')):
            for x in a.get(lst,[]):
                lab=x.get('function') or x.get('source'); w.writerow([y,f'{fn}: {lab}',x['amount'],*found(y,x['amount'],a.get('revenues_expenditures_statement_page')),url])
        bv=a['budget_vs_actual']
        for k in ['final_budget_total_revenues','actual_total_revenues','final_budget_total_expenditures','actual_total_expenditures']:
            if bv.get(k) is not None: w.writerow([y,'budgetary_basis_'+k,bv[k],*found(y,bv[k],bv.get('page')),url])
# enterprise
def norm(n):
    n=n.lower()
    return 'Sewer' if 'sewer' in n else 'Water' if 'water' in n else 'Solid Waste' if 'solid' in n else 'Nonmajor (FY2016-22: solid waste, waterways, DCTV; FY2023+: waterways, DCTV)' if 'nonmajor' in n else None
ENT=collections.defaultdict(dict)
with open(f'{OUT}/05_enterprise_funds_audited.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['fiscal_year','fund','operating_revenues','operating_expenses','operating_income_loss','transfers_net','change_in_net_position','ending_net_position','unrestricted_net_position','pdf_page','text_match_check','report_pdf_url'])
    for y in FAC:
        a=A[y]; url=f'https://app.fac.gov/dissemination/report/pdf/{FAC[y][0]}'; pg=a.get('enterprise_statement_page')
        for x in a['enterprise_funds']:
            fn=norm(x['fund'])
            if not fn: continue
            chk=[inpage(y,x.get(k),pg) for k in ('operating_revenues','operating_expenses','ending_net_position')]
            ok='verified in report text' if all(c.startswith('literal') for c in chk) else '; '.join(chk)
            w.writerow([y,fn,x.get('operating_revenues'),x.get('operating_expenses'),x.get('operating_income_loss'),x.get('transfers_net'),x.get('change_in_net_position'),x.get('ending_net_position'),x.get('unrestricted_net_position'),pg,ok,url])
            ENT[fn[:8]][y]=x
json.dump({k:{str(y):v for y,v in d.items()} for k,d in ENT.items()},open(f'{W}/out/ent.json','w'))
# federal awards
fa=json.load(open(f'{W}/fac/federal_awards.json'))
with open(f'{OUT}/10_federal_awards_by_program.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['audit_year','assistance_listing','federal_program_name','cluster_name','amount_expended','is_major_program','is_direct','passthrough_to_subrecipients','fac_report_id','source_id'])
    for r in sorted(fa,key=lambda r:(r['audit_year'],-r['amount_expended'])):
        w.writerow([r['audit_year'],f"{r['federal_agency_prefix']}.{r['federal_award_extension']}",r['federal_program_name'],r['cluster_name'],r['amount_expended'],r['is_major'],r['is_direct'],r['passthrough_amount'] or '',r['report_id'],'FAC-API'])
tot=collections.defaultdict(int); big=collections.defaultdict(lambda: collections.defaultdict(int))
for r in fa: tot[r['audit_year']]+=r['amount_expended']; big[r['audit_year']][f"{r['federal_agency_prefix']}.{r['federal_award_extension']} {r['federal_program_name'][:40]}"]+=r['amount_expended']
for y in sorted(tot): print(y,tot[y],A[int(y)]['summary_of_auditor_results']['total_federal_expenditures'],sorted(big[y].items(),key=lambda x:-x[1])[:3])
# dept budget table
rows=list(csv.DictReader(open(f'{W}/out/dept_totals_raw.csv',encoding='utf-8-sig')))
fix={'OPEB (Retirement Health Insurance Liability New Employees)':'Health & Life Insurance (includes $700,000 OPEB trust contribution and Medicare surcharge)','Finance Committee':'Finance Committee Reserve Fund (budget only; transfers are spent in receiving departments)','Pensions & Retirement':'Pensions & Retirement (Bristol County Retirement assessment and non-contributory pensions)'}
with open(f'{OUT}/04_department_budget_fy2022_fy2027.csv','w',newline='') as f:
    cols=['FY2022_actual','FY2023_actual','FY2024_actual','FY2025_actual','FY2026_budget_revised','FY2027_budget']
    w=csv.writer(f); w.writerow(['section','department']+cols+['change_fy2022_to_fy2027_usd','change_fy2022_to_fy2027_pct','source_id'])
    sec=collections.defaultdict(lambda:[0]*6)
    for r in rows:
        v=[float(r[c]) for c in cols]
        if sum(v)==0: continue
        for i in range(6): sec[r['section']][i]+=v[i]
        w.writerow([r['section'].title(),fix.get(r['department'],r['department'])]+[round(x) for x in v]+[round(v[5]-v[0]),round((v[5]/v[0]-1)*100,1) if v[0]>0 else '', 'TOWN-BUD-FY25/FY26/FY27'])
    g=[0]*6
    for s,v in sec.items():
        w.writerow([s.title(),'SECTION TOTAL (sum of departments)']+[round(x) for x in v]+[round(v[5]-v[0]),round((v[5]/v[0]-1)*100,1),'derived']); g=[a+b for a,b in zip(g,v)]
    w.writerow(['All','GRAND TOTAL (sum of departments)']+[round(x) for x in g]+[round(g[5]-g[0]),round((g[5]/g[0]-1)*100,1),'derived'])
    print('grand',[round(x) for x in g]); 
    for s,v in sec.items(): print(s,[round(x) for x in v])
