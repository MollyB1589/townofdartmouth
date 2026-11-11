import csv, json, re, collections, statistics as st
exec(open('build1.py').read().split("D=lambda")[0])
OUT='/home/user/workspace/dartmouth-financial-baseline/data'
P=lambda n: rd(f'{W}/raw/dls_peers/peers__{n}.csv')
CPI={int(k):v for k,v in json.load(open(f'{W}/out/cpi.json'))['CPI'].items()}
peers=[n for c,n in json.load(open(f'{W}/raw/dls_peers/peers.json'))]
core=peers[:12]; south=peers[12:]
group={n:('Dartmouth' if n=='Dartmouth' else 'Statistical peer' if n in core else 'South Coast neighbor') for n in peers}
pop={}
for r in P('population'):
    pop[r['Municipality']]={int(k):num(v) for k,v in r.items() if k.isdigit()}
def popfy(m,fy): return pop[m][min(fy-1,2024)]
M=collections.defaultdict(dict)  # (muni,fy) -> metrics
def load(name,ycol,cols):
    for r in P(name):
        try: fy=int(r[ycol])
        except: continue
        for src,dst in cols.items():
            v=num(r.get(src))
            if v is not None: M[(r['Municipality'],fy)][dst]=v
load('gf_expenditures_by_function','Fiscal Year',{'General Govenment':'gf_general_government','Public Safety':'gf_public_safety','Education':'gf_education','Public Works':'gf_public_works','Human Services':'gf_human_services','Culture and Recreation':'gf_culture_recreation','Debt Service':'gf_debt_service','Unclassified':'gf_fixed_costs_unclassified','Transfers /Other':'gf_transfers_other','Total Expenditures':'gf_total'})
load('avg_single_family_tax_bill','Fiscal Year',{'Average Single-Family Value':'avg_sf_value','Single-Family Tax Bill':'avg_sf_tax_bill','DOR Income Per Capita':'income_per_capita','Average Tax Bill as a % of Income':'bill_pct_income','Rank':'bill_rank'})
load('free_cash_pct_budget','Fiscal Year',{'Certified Free Cash as of 7/1':'free_cash','Certified Free Cash as a % of the Budget':'free_cash_pct_budget'})
load('levy_limit_excess_capacity','Fiscal Year',{'Total Tax Levy':'tax_levy','Excess Levy Capacity':'excess_capacity','Excess as a % of Maximum Levy':'excess_pct_max_levy','Total Assessed Value':'assessed_value'})
load('long_term_debt','Fiscal Year',{'Total Outstanding Debt (Schedule A Part 10)':'debt_outstanding','Equalized Values (EQV)':'eqv','Total Budget':'total_budget','Debt Service as a % of Budget':'debt_service_pct_budget'})
load('personnel_fte_wages','Fiscal Year',{'Total Employees':'employees','Total Salaries & Wages':'wages'})
load('stabilization_funds','Schedule A Fiscal Year',{'Total Stabilization Fund Balance':'stabilization_total','Stabilization Fund Balance':'stabilization_general','Total Stabilization as % of Budget':'stab_pct_budget','Operating Budget':'operating_budget'})
load('state_aid_net','Fiscal Year',{'Receipts':'state_aid_receipts','Net State Aid':'state_aid_net'})
load('tax_rates_by_class','Fiscal Year',{'Residential':'res_rate','Commercial':'com_rate'})
# DESE
dese=json.load(open(f'{W}/raw/dese/dese_expenditures.json')); E=collections.defaultdict(dict)
for r in dese:
    v=num(r.get('ind_value'))
    if v is None: continue
    E[(r['dist_name'],int(r['sy']))][(r['ind_cat'],r['ind_subcat'])]=v
dk={'pp_total':('Expenditures Per Pupil','Total Expenditures'),'pp_in_district':('Expenditures Per Pupil','Total In-District Expenditures'),'pp_teachers':('Expenditures Per Pupil','Teachers'),'pp_admin':('Expenditures Per Pupil','Administration'),'pp_insurance_retirement':('Expenditures Per Pupil','Insurance, Retirement Programs and Other'),'pp_operations_maintenance':('Expenditures Per Pupil','Operations and Maintenance'),'pp_pupil_services':('Expenditures Per Pupil','Pupil Services'),'fte_pupils_total':('Student Enrollment','Total FTE Pupils'),'fte_pupils_in_district':('Student Enrollment','In-District FTE Pupils'),'avg_teacher_salary':('Teacher Salaries','Average Teacher Salary'),'teachers_per_100':('Teacher Salaries','Teachers per 100 FTE students'),'low_income_pct':('Student Demographics','Low-Income % Headcount'),'swd_pct':('Student Demographics','Students with disabilities % Headcount'),'headcount':('Student Demographics','Student Headcount')}
for (m,sy),d in E.items():
    for k,key in dk.items():
        if key in d: M[(m,sy)]['dese_'+k]=d[key]
# fire districts
fire=collections.defaultdict(float); firerows=[]
for r in rd(f'{W}/raw/districts/fire_levy.csv'):
    fy=int(r['Fiscal Year']); tl=num(r['Total Levy']); fire[fy]+=tl
    firerows.append([fy,r['DOR Code'],r['Name'],int(num(r['Residential Levy'])),int(num(r['Commercial Levy'])),int(num(r['Industrial Levy'])),int(num(r['Personal Property Levy'])),int(tl)])
frates={}
for r in rd(f'{W}/raw/districts/fire_rates.csv'):
    if 'Dartmouth' in r['Name']: frates[(int(r['Fiscal Year']),r['DOR Code'])]=(num(r['Residential']),num(r['Commercial']))
with open(f'{OUT}/09_fire_district_levies.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['fiscal_year','dls_district_code','district','residential_levy','commercial_levy','industrial_levy','personal_property_levy','total_levy','residential_rate_per_1000','commercial_rate_per_1000','source_id'])
    for r in sorted(firerows): w.writerow(r+list(frates.get((r[0],r[1]),('','')))+['DLS-DIST'])
    for fy in sorted(fire): w.writerow([fy,'423-425','All three Dartmouth fire districts (sum)','','','','',int(fire[fy]),'','','DLS-DIST (derived)'])
json.dump({str(k):v for k,v in fire.items()},open(f'{W}/out/fire.json','w'))
# time series tidy
fields=sorted({k for d in M.values() for k in d})
with open(f'{OUT}/07_peer_timeseries_long.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['municipality','peer_group','fiscal_year','metric','value','source_id'])
    for (m,fy),d in sorted(M.items()):
        if fy<2016 or m not in group: continue
        for k in sorted(d): w.writerow([m,group[m],fy,k,d[k],'DESE-RADAR' if k.startswith('dese_') else 'DLS-PEERS'])
        if (m,fy) in M and fy-1 in range(2014,2026): w.writerow([m,group[m],fy,'population_estimate_fy_minus_1',popfy(m,fy),'DLS-POP'])
# FY2025 snapshot
FY=2025; rows=[]
def g(m,fy,k): return M.get((m,fy),{}).get(k)
for m in peers:
    p=popfy(m,FY); d=M[(m,FY)]; r={'municipality':m,'peer_group':group[m],'population_2024':int(p),'income_per_capita':d.get('income_per_capita'),'eqv_per_capita':round(d['eqv']/p) if d.get('eqv') else None}
    for k in ['gf_total','gf_general_government','gf_public_safety','gf_education','gf_public_works','gf_human_services','gf_culture_recreation','gf_debt_service','gf_fixed_costs_unclassified','gf_transfers_other']:
        r[k+'_per_capita']=round(d[k]/p) if d.get(k) is not None else None
    r['gf_non_education_per_capita']=round((d['gf_total']-d['gf_education'])/p)
    r['avg_sf_tax_bill']=d.get('avg_sf_tax_bill'); r['avg_sf_value']=d.get('avg_sf_value'); r['bill_pct_income']=d.get('bill_pct_income'); r['res_rate']=d.get('res_rate'); r['com_rate']=d.get('com_rate')
    r['tax_levy_per_capita']=round(d['tax_levy']/p); r['excess_capacity_pct_max_levy']=d.get('excess_pct_max_levy')
    r['state_aid_receipts_per_capita']=round(d['state_aid_receipts']/p)
    r['debt_outstanding_per_capita']=round(d['debt_outstanding']/p) if d.get('debt_outstanding') else None
    r['debt_service_pct_budget']=d.get('debt_service_pct_budget')
    r['free_cash_pct_budget']=d.get('free_cash_pct_budget'); r['stabilization_pct_budget']=d.get('stab_pct_budget')
    r['employees_per_1000_pop']=round(d['employees']/p*1000,1) if d.get('employees') else None
    r['wages_per_capita']=round(d['wages']/p) if d.get('wages') else None
    # growth 2016-2025 real per capita
    d0=M[(m,2016)]; p0=popfy(m,2016)
    r['gf_total_per_capita_fy2016']=round(d0['gf_total']/p0)
    r['gf_total_real_per_capita_growth_pct_fy2016_fy2025']=round(((d['gf_total']/p)/(d0['gf_total']/p0)/(CPI[2025]/CPI[2016])-1)*100,1)
    r['avg_sf_tax_bill_fy2016']=d0.get('avg_sf_tax_bill'); r['avg_sf_tax_bill_real_growth_pct']=round((d['avg_sf_tax_bill']/d0['avg_sf_tax_bill']/(CPI[2025]/CPI[2016])-1)*100,1) if d.get('avg_sf_tax_bill') and d0.get('avg_sf_tax_bill') else None
    for sy in (2025,):
        for k in ['pp_total','pp_in_district','pp_teachers','pp_admin','pp_insurance_retirement','pp_operations_maintenance','pp_pupil_services','fte_pupils_total','avg_teacher_salary','teachers_per_100','low_income_pct','swd_pct']:
            r[f'dese_{k}_sy{sy}']=g(m,sy,'dese_'+k)
    e0=g(m,2016,'dese_fte_pupils_total'); e1=g(m,2025,'dese_fte_pupils_total')
    r['fte_pupils_change_pct_sy2016_sy2025']=round((e1/e0-1)*100,1) if e0 and e1 else None
    a0=g(m,2016,'dese_pp_total'); a1=g(m,2025,'dese_pp_total')
    r['pp_total_real_growth_pct_sy2016_sy2025']=round((a1/a0/(CPI[2025]/CPI[2016])-1)*100,1) if a0 and a1 else None
    r['gf_education_per_fte_pupil']=round(d['gf_education']/g(m,2025,'dese_fte_pupils_total')) if g(m,2025,'dese_fte_pupils_total') else (round(d['gf_education']/e1) if e1 else None)
    rows.append(r)
# Dartmouth adjusted for fire districts
dr=[r for r in rows if r['municipality']=='Dartmouth'][0]; p=dr['population_2024']
adj=dict(dr); adj['municipality']='Dartmouth + fire district levies (estimate)'; adj['peer_group']='Dartmouth adjusted'
fpc=round(fire[2025]/p)
adj['gf_public_safety_per_capita']=dr['gf_public_safety_per_capita']+fpc; adj['gf_total_per_capita']=dr['gf_total_per_capita']+fpc; adj['gf_non_education_per_capita']=dr['gf_non_education_per_capita']+fpc
adj['tax_levy_per_capita']=dr['tax_levy_per_capita']+fpc
for k in list(adj):
    if k.startswith(('dese_','fte_','pp_','gf_total_real','gf_total_per_capita_fy2016','avg_sf','bill_','res_rate','com_rate','employees','wages','free_cash','stab','debt','excess','state_aid','income','eqv','gf_education_per_fte')): adj[k]=None
rows.insert(1,adj)
cols=list(rows[0].keys())
def med(k,grp): 
    v=[r[k] for r in rows if r['peer_group']==grp and r.get(k) is not None]; return round(st.median(v),1) if v else None
medrow={'municipality':'Median of 11 statistical peers','peer_group':'Summary'}
for k in cols[2:]: medrow[k]=med(k,'Statistical peer')
rows.append(medrow)
with open(f'{OUT}/06_peer_comparison_fy2025.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)
json.dump(rows,open(f'{W}/out/peer_snapshot.json','w'))
# print compact
def show(keys):
    print(' | '.join(['muni']+keys))
    for r in rows: print(r['municipality'][:26].ljust(26),' | '.join(str(r.get(k)) for k in keys))
import sys
show(['dese_pp_total_sy2025','dese_pp_in_district_sy2025','dese_pp_teachers_sy2025','dese_pp_admin_sy2025','dese_pp_insurance_retirement_sy2025','dese_pp_operations_maintenance_sy2025','dese_pp_pupil_services_sy2025','dese_fte_pupils_total_sy2025','dese_avg_teacher_salary_sy2025','dese_teachers_per_100_sy2025','dese_low_income_pct_sy2025','dese_swd_pct_sy2025','fte_pupils_change_pct_sy2016_sy2025','pp_total_real_growth_pct_sy2016_sy2025','gf_education_per_fte_pupil'])
show(['population_2024','gf_total_per_capita','gf_non_education_per_capita','gf_public_safety_per_capita','gf_general_government_per_capita','gf_public_works_per_capita','gf_fixed_costs_unclassified_per_capita','gf_debt_service_per_capita','gf_education_per_capita'])
show(['avg_sf_tax_bill','bill_pct_income','res_rate','tax_levy_per_capita','excess_capacity_pct_max_levy','state_aid_receipts_per_capita','debt_outstanding_per_capita','free_cash_pct_budget','stabilization_pct_budget','employees_per_1000_pop'])
show(['dese_pp_total_sy2025','dese_pp_in_district_sy2025','dese_pp_teachers_sy2025','dese_pp_admin_sy2025','dese_pp_insurance_retirement_sy2025','dese_pp_operations_maintenance_sy2025','dese_fte_pupils_total_sy2025','dese_avg_teacher_salary_sy2025','fte_pupils_change_pct_sy2016_sy2025','pp_total_real_growth_pct_sy2016_sy2025','gf_total_real_per_capita_growth_pct_fy2016_fy2025','avg_sf_tax_bill_real_growth_pct'])
print('fire',dict(fire)); print('dese 2025 pp?', g('Dartmouth',2025,'dese_pp_total'), g('Dartmouth',2025,'dese_fte_pupils_total'))

# DESE tidy
with open(f'{OUT}/08_school_per_pupil_dese.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['district','peer_group','school_year_ending','category','indicator','value','source_id'])
    for (m,sy),d in sorted(E.items()):
        if sy<2016 or m not in group: continue
        for (c,s2),v in sorted(d.items()): w.writerow([m,group[m],sy,c,s2,v,'DESE-RADAR'])
# Dartmouth real series
T=json.load(open(f'{W}/out/core.json'))['T']
print('FY  nominalGFexp  realGFexp(2026$)  perCap  realPerCap  enroll  ppTotal realPP')
for fy in range(2016,2027):
    e=T['schedA_gf_exp_total_expenditures'][str(fy)]; p=T['population_estimate'][str(fy)]; c=CPI[2026]/CPI[fy]
    en=g('Dartmouth',fy,'dese_fte_pupils_total'); pp=g('Dartmouth',fy,'dese_pp_total')
    print(fy,int(e),int(e*c),int(e/p),int(e*c/p),en,pp,int(pp*c) if pp else None)
