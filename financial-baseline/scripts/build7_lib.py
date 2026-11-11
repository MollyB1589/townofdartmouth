import json,csv,sys
W='/home/user/workspace/work'; D='/home/user/workspace/dartmouth-financial-baseline'
sys.path.insert(0,W)
from sources import SRC
core=json.load(open(f'{W}/out/core.json')); T=core['T']; META=core['META']
tc=json.load(open(f'{W}/out/town_cats.json')); ent=json.load(open(f'{W}/out/ent.json')); fire=json.load(open(f'{W}/out/fire.json'))
def rd(name): return list(csv.DictReader(open(f'{D}/data/{name}',encoding='utf-8-sig')))
YRS=[str(y) for y in range(2016,2028)]
cpi=T['cpi_u_us_fiscal_year_avg']
def real(v,y): return v*cpi['2026']/cpi[str(y)]
LBL={
'DLS-SCHA-GF':'DLS Schedule A general fund report','DLS-GFEXP':'DLS general fund expenditures report','DLS-SCHA-ENT':'DLS Schedule A enterprise fund report',
'DLS-FC':'DLS certified free cash report','DLS-STAB':'DLS stabilization fund report','DLS-DEBT':'DLS long-term debt report','DLS-AUD':'DLS authorized and unissued debt report',
'DLS-LEVY':'DLS levy limit report','DLS-NG':'DLS new growth report','DLS-RATE':'DLS tax rate report','DLS-SFTB':'DLS average single-family tax bill report',
'DLS-AID':'DLS state aid report','DLS-ERE':'DLS enterprise retained earnings report','DLS-PERS':'DLS personnel report','DLS-REV':'DLS revenue by source report',
'DLS-OVL':'DLS overlay report','DLS-REC':'DLS outstanding receivables report','DLS-POP':'DLS population report','DLS-VOTES':'DLS override vote records',
'DLS-DEXCL':'DLS debt exclusion vote records','DLS-BOND':'DLS bond rating report','DLS-PENS':'DLS pension liability report','DLS-DIST':'DLS district levy and rate reports',
'DLS-PEERS':'DLS peer municipality reports','BLS-CPI':'BLS consumer price index series','DESE-RADAR':'DESE per-pupil expenditure data',
'ECFR-512':'2 CFR 200.512','ECFR-520':'2 CFR 200.520','MGL-66-10':'M.G.L. c. 66, s. 10','FAC-API':'Federal Audit Clearinghouse records',
'TOWN-BUD-FY27':'FY2027 Town operating budget','TOWN-BUD-FY26':'FY2026 Town operating budget','TOWN-BUD-FY25':'FY2025 Town operating budget',
'TOWN-SCHA-FY24':'FY2024 Town operating budget','TOWN-SCHA-FY23':'FY2023 Town budget (scan)','TOWN-SCHA-FY21':'FY2021 Town operating budget (scan)',
'TOWN-SCHA-FY19':'FY2019 Town operating budget (scan)','TOWN-SCHA-FY17':'FY2017 Town budget','TOWN-BUDGET-PAGE':'Town Budget Information page',
'TOWN-DEBT-2026':'Proposed Long Term Debt Analysis','FINCOM-LETTER-FY27':'FY27 Finance Committee letter','FINCOM-2026-03-05':'Finance Committee minutes, March 5, 2026',
'FINCOM-2026-02-12':'Finance Committee minutes, February 12, 2026','FINCOM-2024-03-28':'Finance Committee minutes, March 28, 2024',
'JOINT-2025-07-28':'joint Finance Committee and Select Board minutes','SB-2026-03-23':'Select Board minutes, March 23, 2026',
'SB-RECAP-2026-08-31':'Select Board recap, August 31, 2026','SB-RECAP-2026-08-03':'Select Board recap, August 3, 2026','WATER-RATE-2025-12':'Town water rate notice',
'TOWN-NEWS':'Town news items','CLEARGOV-NEWS':'Town ClearGov announcement','SB-GOALS':'Select Board Strategic Goals 2025-2026',
'DLS-FMR-2007':'2007 DLS Financial Management Review','RESERVE-POLICY':'Reserve Fund Policy and Practices','ONETIME-POLICY':'One-Time Revenue Policy',
'CPC-LETTER-2022':'Capital Planning Committee report','SP-REPORT':'S&P rating report (scan)','SATM-2025':'2025 Spring Town Meeting packet','FATM-2025':'2025 Fall Town Meeting packet',
'WARRANTS':'Town Meeting warrant archive','TOWN-REPORTS':'Annual Town Reports archive','FINCOM-PAGE':'Finance Committee page','TREAS-PAGE':'Treasurer page',
'ACCT-PAGE':'Accounting Department page','BIDS-PAGE':'Bid Postings page','TA-PAGE':'Town Administrator page','DPW-PAGE':'Public Works page',
'HANDBOOK':'Board and Committee Handbook','CHARTER-2025':'Town Charter text (2025 voter booklet)','LRCP-PAGE':'Long Range Capital Planning Committee page',
'ASSESSOR-PAGE':'Assessor page','SB-PAGE':'Select Board page','CPA-PLAN-FY27':'Community Preservation plan for FY2027','PROFILE':'Community Profile page',
'SC-MIN-2025-04-14':'School Committee minutes, April 14, 2025','FIRE-PAGE':'Fire Districts page','TAX-RATE-HIST':'Town Tax Rate History page',
'SCHOOL-FY26-BUDGET':'Dartmouth Public Schools FY26 budget book','PERAC-2024':'PERAC 2024 Bristol County profile','PERAC-VAL-2024':'Bristol County 2024 actuarial valuation',
'OPEB-STATE-2026':'state OPEB summary report','WEEK-RATES':'Dartmouth Week rates article','WEEK-OVERRIDE':'Dartmouth Week override article',
'WEEK-PRELIM':'Dartmouth Week budget article','WEEK-GOALS':'Dartmouth Week goals article','SCT-FY27':'SouthCoast Today budget article',
'REPO-PRR-2026-11-10':'financial records request log','REPO-PRR-DPW-2026-11-10':'DPW staffing and payroll request log','REPO-STANDARDS':'repository research standards',
'BPW-PAGE':'Board of Public Works page','BPW-APPLICANTS-2026':'Town notice seeking Board of Public Works applicants','SCT-ELECTION-2026':'SouthCoast Today election report','SCT-FATM-2025':'SouthCoast Today Town Meeting report',
}
for y in range(2016,2026): LBL[f'AUDIT-FY{y}']=f'FY{y} audit package'
def dt(sid):
    d=SRC[sid][2]
    return d if d.startswith(('accessed','current','undated')) else f'dated {d}'
def lk(sid,label=None): return f'[{label or LBL.get(sid,SRC[sid][0])}]({SRC[sid][3]})'
def c(sid,where=None,label=None):
    p=[lk(sid,label),dt(sid)]
    if where: p.append(where)
    return '('+', '.join(p)+')'
def links(ids,dates=False):
    out=[]
    for s in [x.strip() for x in ids.replace(',',';').split(';') if x.strip()]:
        if s in SRC: out.append(lk(s)+(f' ({dt(s)})' if dates else ''))
        else: out.append(s)
    return '; '.join(out)
def esc(s): return str(s).replace('|','\\|').replace('\n',' ').strip()
def tbl(h,rows,right=None):
    right=right or []
    o=['| '+' | '.join(h)+' |','|'+'|'.join('---:' if i in right else '---' for i in range(len(h)))+'|']
    for r in rows: o.append('| '+' | '.join(esc(x) for x in r)+' |')
    return '\n'.join(o)
def M(v,n=2): return 'n/a' if v is None else f'{v/1e6:,.{n}f}'
def Dl(v): return 'n/a' if v is None else (f'-{abs(v):,.0f}' if v<0 else f'{v:,.0f}')
def g(k,y): return T[k].get(str(y))
def pct(a,b): return (b/a-1)*100
