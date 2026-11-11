import csv, json, collections
from sources import SRC, W
OUT='/home/user/workspace/dartmouth-financial-baseline/data'
C=json.load(open(f'{W}/out/core.json')); T=C['T']
CPI=T['cpi_u_us_fiscal_year_avg']; POP=T['population_estimate']
def real(v,y): return v*CPI['2026']/CPI[str(y)] if str(y) in CPI else None
def wr(name,header,rows):
    with open(f'{OUT}/{name}','w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(header); w.writerows(rows)
    print(name,len(rows))

# ---------- 03 general fund by function ----------
rows=[]
FN=[('general_government','General government'),('public_safety','Public safety (police, dispatch, inspections; fire is in separate districts)'),('education','Education'),('public_works','Public works'),('human_services','Human services'),('culture_and_recreation','Culture and recreation'),('debt_service','Debt service'),('fixed_costs','Fixed costs (pensions, health insurance, other benefits)'),('intergov_assessments','Intergovernmental assessments'),('other_expenditures','Other expenditures'),('total_expenditures','TOTAL general fund expenditures')]
for y in range(2016,2027):
    tot=T['schedA_gf_exp_total_expenditures'][str(y)]
    for k,lab in FN:
        v=T['schedA_gf_exp_'+k].get(str(y))
        if v is None: continue
        rows.append([y,'DLS Schedule A function',lab,'actual (statutory basis, as reported to DLS; unaudited)',round(v),round(v/tot*100,1),round(real(v,y)),round(real(v,y)/POP[str(y)]),'DLS-SCHA-GF','sum of functions equals reported total' if k=='total_expenditures' else ''])
# check sum
for y in range(2016,2027):
    s=sum(T['schedA_gf_exp_'+k].get(str(y),0) for k,_ in FN[:-1]); t=T['schedA_gf_exp_total_expenditures'][str(y)]
    assert abs(s-t)<=5,(y,s,t)
CATS=['General Government','Public Safety','Schools','Public Works','Community Services','Debt Service','Employee Benefits','Property & Liability Insurance']
TOWN={ # year:(values..., grand_total, basis, source, validation)
2014:([3569166.17,6212927.64,39685479.69,2809672.24,2728002.91,4788716.02,10791896.68,705652.25],71291513.60,'actual','TOWN-SCHA-FY17','text layer'),
2015:([3897077.60,6327935.71,40664525.01,3064194.70,2737056.29,4821500.52,10861238.35,702587.74],73076115.92,'actual','TOWN-SCHA-FY17','text layer'),
2016:([3603824.01,7063333.35,42634658.85,2916181.93,2480883.34,4506101.53,10396210.35,724179.51],74325372.87,'actual','TOWN-SCHA-FY19','read from scanned image (OCR plus visual check)'),
2017:([3630325.32,7480366.31,44646848.97,2825964.07,2480495.12,4686238.07,11224260.55,835822.55],77810320.96,'actual','TOWN-SCHA-FY19','read from scanned image (OCR plus visual check)'),
2018:([3684644.30,7521642.70,46214279.79,3003348.21,2662387.35,4264491.30,11903658.70,795325.41],80049777.76,'actual','TOWN-SCHA-FY21','read from scanned image (OCR plus visual check)'),
2019:([3610099.87,7496698.09,47739237.60,3064297.68,2718006.00,4929610.49,12480980.46,780550.53],82819480.72,'actual','TOWN-SCHA-FY21','read from scanned image (OCR plus visual check)'),
2020:([3743404.35,7313618.86,48842574.02,3255994.28,2651020.17,5206016.52,12659432.98,789148.00],84461209.18,'actual','TOWN-SCHA-FY23','read from scanned image (OCR plus visual check)'),
2021:([3688899.81,7887134.59,50181823.48,3290617.59,2775974.38,5096121.03,13385014.75,886516.73],87192102.36,'actual','TOWN-SCHA-FY24','text layer; also matches scanned FY2023 document'),
2022:([3958531.16,8403179.10,52555101.23,3686429.64,3035729.23,4994047.27,14019316.39,894982.57],91547316.59,'actual','TOWN-BUD-FY25','text layer'),
2023:([4227433.18,8740645.81,55421764.12,3282652.00,3117833.57,2530788.19,14733271.13,1001423.05],93055811.05,'actual','TOWN-BUD-FY26','text layer'),
2024:([4745706.66,8573406.10,57166291.76,3753802.63,3141077.38,2465057.54,15376750.51,1116134.60],96338227.18,'actual','TOWN-BUD-FY27','text layer'),
2025:([5305286.47,9634984.82,59331955.99,3693341.11,3156637.71,2094378.77,17144813.56,1231366.11],101592764.54,'actual','TOWN-BUD-FY27','text layer'),
2026:([6155968.00,10814318.00,61988512.00,4495032.00,3554332.00,2101164.00,18070649.00,1320057.00],108500032.00,'budget (revised)','TOWN-BUD-FY27','text layer'),
2027:([6663996.00,11158382.00,64605917.00,4748757.00,3609114.00,1919896.00,19255072.00,1428381.00],113389515.00,'budget (Finance Committee recommendation, adopted June 2, 2026)','TOWN-BUD-FY27','text layer'),
}
town_out={}
for y,(vals,gt,basis,sid,how) in TOWN.items():
    s=sum(vals); ok=abs(s-gt)<1.0
    assert ok,(y,s,gt)
    cy=min(y,2026)
    for cname,v in list(zip(CATS,vals))+[('GRAND TOTAL (Town Schedule A operating budget)',gt)]:
        rv=real(v,y) if str(y) in CPI else None
        rows.append([y,'Town budget category (Schedule A operating budget document)',cname,basis,round(v),round(v/gt*100,1),round(rv) if rv else '',round(rv/POP[str(y)]) if rv and str(y) in POP else '',sid,f'{how}; eight categories sum to the printed grand total within $1'])
    town_out[y]=dict(zip(CATS,vals)); town_out[y]['total']=gt
json.dump(town_out,open(f'{W}/out/town_cats.json','w'))
wr('03_general_fund_by_function.csv',['fiscal_year','classification','category','basis','amount_usd','share_of_total_pct','amount_fy2026_dollars','per_capita_fy2026_dollars','source_id','validation_note'],rows)

# ---------- 12 source inventory ----------
alias=[('AUDIT','Alias used in tables 01 and 05: audited financial statements; see AUDIT-FY2016 to AUDIT-FY2025 for the year-specific report','','','https://app.fac.gov/dissemination/search/','',''),
('TOWN-BUD','Alias used in table 01: Town Schedule A operating budget documents; see TOWN-BUD-FY25, TOWN-BUD-FY26, TOWN-BUD-FY27','','','https://www.dartmouthma.gov/617/Budget-Information','',''),
('TOWN-BUD-FY25/FY26/FY27','Alias used in table 04: the three Town budget documents TOWN-BUD-FY25, TOWN-BUD-FY26, TOWN-BUD-FY27','','','https://www.dartmouthma.gov/617/Budget-Information','','')]
def typ(sid):
    if sid.startswith(('DLS-','BLS','DESE','FAC','ECFR','PERAC','OPEB','MGL')) and sid!='DLS-FMR-2007': return 'State or federal data / regulation'
    if sid.startswith('AUDIT'): return 'Independent audit'
    if sid.startswith(('WEEK','SCT')): return 'News report (secondary)'
    if sid.startswith('REPO'): return 'Project repository'
    if sid=='DLS-FMR-2007': return 'State financial management review'
    return 'Town of Dartmouth record'
inv=[[sid,typ(sid),*t] for sid,t in SRC.items()]+[[a[0],'Alias',*a[1:]] for a in alias]
wr('12_source_inventory.csv',['source_id','source_type','title','publisher','document_date','url','pages_or_section','notes'],inv)
used=set()
import glob
for f in glob.glob(f'{OUT}/*.csv'):
    for r in csv.DictReader(open(f,encoding='utf-8-sig')):
        if 'source_id' in r: used.add(r['source_id'])
known=set(SRC)|{a[0] for a in alias}|{'derived','DLS-DIST (derived)'}
print('unknown source ids:',sorted(u for u in used if u not in known and not all(p.strip() in known for p in u.replace(';',',').split(','))))
