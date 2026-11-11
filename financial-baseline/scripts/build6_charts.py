import json, csv, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
W='/home/user/workspace/work'; O='/home/user/workspace/dartmouth-financial-baseline'
C=json.load(open(f'{W}/out/core.json'))['T']
def s(m,ys): return [C[m].get(str(y)) for y in ys]
NAVY='#1f3a5f'; TEAL='#2a9d8f'; ORANGE='#e76f51'; GOLD='#e9b44c'; GREY='#8d99ae'; LIGHT='#cfd8e3'; PURPLE='#6d597a'; GREEN='#588157'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10.5,'axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,'grid.color':'#e6e9ee','grid.linewidth':0.8,'axes.axisbelow':True,'axes.titlesize':13,'axes.titleweight':'bold','axes.titlelocation':'left','figure.dpi':150,'savefig.bbox':'tight','legend.frameon':False})
mil=FuncFormatter(lambda v,p: f'${v/1e6:,.0f}M')
def foot(fig,t): fig.text(0.01,-0.02,t,fontsize=8,color='#555',ha='left',va='top')
def fy(ys): return [f'FY{str(y)[2:]}' for y in ys]

# 1 GF spending nominal vs real
ys=list(range(2016,2027)); exp=s('schedA_gf_exp_total_expenditures',ys); cpi=s('cpi_u_us_fiscal_year_avg',ys)
real=[e*cpi[-1]/c for e,c in zip(exp,cpi)]
fig,ax=plt.subplots(figsize=(9,4.8))
ax.plot(fy(ys),exp,marker='o',color=NAVY,lw=2.2,label='Nominal dollars')
ax.plot(fy(ys),real,marker='o',color=ORANGE,lw=2.2,label='Constant FY2026 dollars (CPI-U)')
ax.yaxis.set_major_formatter(mil); ax.set_ylim(60e6,125e6)
for i in (0,len(ys)-1):
    ax.annotate(f'${exp[i]/1e6:.1f}M',(i,exp[i]),textcoords='offset points',xytext=(0,-15),ha='center',color=NAVY,fontsize=9)
ax.annotate(f'${real[0]/1e6:.1f}M',(0,real[0]),textcoords='offset points',xytext=(0,9),ha='center',color=ORANGE,fontsize=9)
ax.set_title('General fund expenditures, FY2016-FY2026'); ax.legend(loc='upper left')
foot(fig,'Source: Massachusetts Division of Local Services, Schedule A general fund expenditures (statutory basis; FY2026 unaudited); BLS CPI-U fiscal-year averages.\nIncludes state assessments, transfers and article spending, so totals exceed the Town operating budget document.')
fig.savefig(f'{O}/charts/01_general_fund_spending_nominal_vs_real.png'); plt.close(fig)

# 2 category stacked
tc=json.load(open(f'{W}/out/town_cats.json')); ys=list(range(2016,2028))
cats=['Schools','Employee Benefits','Public Safety','General Government','Public Works','Community Services','Debt Service','Property & Liability Insurance']
cols=[NAVY,TEAL,ORANGE,GOLD,PURPLE,GREEN,GREY,'#b56576']
fig,ax=plt.subplots(figsize=(10,5.4)); bot=[0]*len(ys)
for c,col in zip(cats,cols):
    v=[tc[str(y)][c] for y in ys]
    bars=ax.bar(fy(ys),v,bottom=bot,color=col,label=c,width=0.72,edgecolor='white',linewidth=0.5)
    for b,y in zip(bars,ys):
        if y>=2026: b.set_hatch('///'); b.set_alpha(0.8)
    bot=[a+b for a,b in zip(bot,v)]
for i,t in enumerate(bot): ax.text(i,t+1.0e6,f'{t/1e6:.1f}',ha='center',fontsize=8.5,color='#333')
ax.yaxis.set_major_formatter(mil); ax.set_ylim(0,125e6)
ax.set_title('Town operating budget by category, FY2016-FY2027')
ax.legend(ncol=4,loc='upper center',bbox_to_anchor=(0.5,-0.08),fontsize=9)
foot(fig,'\n\n\nSource: Town of Dartmouth "Schedule A" operating budget documents (FY2017, FY2019, FY2021, FY2023, FY2024 and FY2025-FY2027 editions). Totals in $ millions.\nFY2016-FY2025 are actual expenditures; FY2026 (revised budget) and FY2027 (budget) are hatched. FY2016-FY2020 were read from scanned pages and cross-footed to printed totals.')
fig.savefig(f'{O}/charts/02_operating_budget_by_category.png'); plt.close(fig)

# 3 reserves
ys=list(range(2016,2028))
fig,ax=plt.subplots(figsize=(9,4.8))
for m,l,col in [('audit_gf_fund_balance_unassigned','Unassigned general fund balance (audited, June 30)',NAVY),('stabilization_total','Stabilization funds (June 30)',TEAL),('free_cash_certified','Certified free cash (available for the fiscal year)',ORANGE)]:
    v=s(m,ys); xs=[f for f,x in zip(fy(ys),v) if x is not None]; vv=[x for x in v if x is not None]
    ax.plot(fy(ys),[x if x is not None else float('nan') for x in v],marker='o',lw=2.2,color=col,label=l)
    ax.annotate(f'${vv[-1]/1e6:.1f}M',(xs[-1],vv[-1]),textcoords='offset points',xytext=(8,0),va='center',color=col,fontsize=9)
ax.yaxis.set_major_formatter(mil); ax.set_ylim(0,27e6); ax.set_title('General fund reserves, FY2016-FY2027'); ax.legend(loc='upper left',fontsize=9)
foot(fig,'Sources: audited financial statements (Federal Audit Clearinghouse); Massachusetts Division of Local Services free cash and stabilization reports.\nFY2026 stabilization is unaudited; FY2027 free cash was certified 9/22/2026.')
fig.savefig(f'{O}/charts/03_reserves.png'); plt.close(fig)

# 4 long-term obligations
ys=list(range(2016,2026))
fig,ax=plt.subplots(figsize=(9,4.8))
opeb=s('audit_net_opeb_liability',ys); pen=s('audit_net_pension_liability',ys); debt=s('audit_bonds_outstanding_total',ys)
x=range(len(ys)); w=0.27
ax.bar([i-w for i in x],debt,w,color=GREY,label='Bonds outstanding (all funds)')
ax.bar([i for i in x],pen,w,color=TEAL,label='Net pension liability (Town share)')
ax.bar([i+w for i in x],[o if o else 0 for o in opeb],w,color=ORANGE,label='Net OPEB liability')
ax.set_xticks(list(x)); ax.set_xticklabels(fy(ys)); ax.yaxis.set_major_formatter(mil)
ax.set_title('Bonded debt, net pension liability and net OPEB liability, FY2016-FY2025'); ax.legend(loc='upper center',bbox_to_anchor=(0.5,-0.08),ncol=3,fontsize=9); ax.set_ylim(0,85e6)
foot(fig,'\n\nSource: audited financial statements, FY2016-FY2025 (Federal Audit Clearinghouse). \nNet OPEB liability is shown from FY2017, the first year the audit reports it on the current basis.')
fig.savefig(f'{O}/charts/04_debt_pension_opeb.png'); plt.close(fig)

# 5 enterprise
E=json.load(open(f'{W}/out/ent.json')); ys=list(range(2016,2026))
fig,(a1,a2)=plt.subplots(1,2,figsize=(11.5,4.6))
x=range(len(ys)); w=0.38
sw=[E['Sewer'][str(y)]['operating_income_loss'] for y in ys]; wa=[E['Water'][str(y)]['operating_income_loss'] for y in ys]
a1.bar([i-w/2 for i in x],sw,w,color=NAVY,label='Sewer'); a1.bar([i+w/2 for i in x],wa,w,color=TEAL,label='Water')
a1.axhline(0,color='#333',lw=0.8); a1.set_xticks(list(x)); a1.set_xticklabels(fy(ys),fontsize=8.5)
a1.yaxis.set_major_formatter(FuncFormatter(lambda v,p:('-' if v<0 else '')+f'${abs(v)/1e6:.1f}M')); a1.set_title('Operating income (loss), audited',fontsize=11.5); a1.legend(loc='lower left',fontsize=9)
ys2=list(range(2016,2028)); re=s('enterprise_retained_earnings_certified',ys2)
a2.plot(fy(ys2),re,marker='o',color=ORANGE,lw=2.2); a2.yaxis.set_major_formatter(FuncFormatter(lambda v,p:f'${v/1e6:.0f}M')); a2.set_ylim(0,8e6)
a2.tick_params(axis='x',labelsize=8.5)
a2.set_title('Certified retained earnings, all enterprise funds',fontsize=11.5)
a2.annotate(f'${re[0]/1e6:.2f}M',(0,re[0]),textcoords='offset points',xytext=(6,6),fontsize=9,color=ORANGE); a2.annotate(f'${re[-1]/1e6:.2f}M',(len(re)-1,re[-1]),textcoords='offset points',xytext=(-34,9),fontsize=9,color=ORANGE)
foot(fig,'Sources: audited proprietary fund statements, FY2016-FY2025 (operating results include depreciation); Massachusetts Division of Local Services certified retained earnings.')
fig.tight_layout(); fig.savefig(f'{O}/charts/05_enterprise_funds.png'); plt.close(fig)

# 6 peers
P=[r for r in csv.DictReader(open(f'{O}/data/06_peer_comparison_fy2025.csv'))]
def hb(ax,key,title,fmt):
    rows=[(float(r[key]),r['municipality'],r['peer_group']) for r in P if r[key] and r['peer_group'] in('Dartmouth','Statistical peer','South Coast neighbor','Dartmouth adjusted')]
    rows.sort()
    cols=[ORANGE if g=='Dartmouth' else ('#f4a988' if g=='Dartmouth adjusted' else (NAVY if g=='Statistical peer' else LIGHT)) for v,n,g in rows]
    names=[n.replace('Dartmouth + fire district levies (estimate)','Dartmouth + fire districts (est.)') for v,n,g in rows]
    ax.barh(names,[v for v,n,g in rows],color=cols); ax.set_title(title,fontsize=11.5); ax.grid(axis='y',visible=False)
    for i,(v,n,g) in enumerate(rows): ax.text(v,i,' '+fmt(v),va='center',fontsize=8)
    ax.set_xlim(0,max(v for v,n,g in rows)*1.16); ax.tick_params(axis='y',labelsize=8.5); ax.xaxis.set_major_formatter(FuncFormatter(lambda v,p:f'${v:,.0f}'))
fig,(a1,a2)=plt.subplots(1,2,figsize=(12.5,5.8))
hb(a1,'gf_total_per_capita','General fund spending per resident, FY2025',lambda v:f'${v:,.0f}')
hb(a2,'dese_pp_total_sy2025','School spending per pupil, 2024-25 (all funds)',lambda v:f'${v:,.0f}')
from matplotlib.patches import Patch
fig.legend(handles=[Patch(color=ORANGE,label='Dartmouth'),Patch(color='#f4a988',label='Dartmouth plus fire district levies (estimate)'),Patch(color=NAVY,label='Statistical peer'),Patch(color=LIGHT,label='South Coast neighbor')],loc='lower center',ncol=4,fontsize=9,bbox_to_anchor=(0.5,-0.04))
foot(fig,'\n\n\nSources: Massachusetts Division of Local Services (general fund expenditures, population); Massachusetts Department of Elementary and Secondary Education per-pupil expenditures.\nServices differ: fire protection in Dartmouth is provided by three separate districts outside the general fund. Regional school members report less school spending in their own budgets.')
fig.tight_layout(); fig.savefig(f'{O}/charts/06_peer_comparison.png'); plt.close(fig)

# 7 audit timeliness
A=list(csv.DictReader(open(f'{O}/data/11_audit_filing_timeline.csv')))
fig,ax=plt.subplots(figsize=(9,4.6))
m1=[float(r['months_fye_to_fs_report']) for r in A]; m2=[float(r['months_fye_to_fac_acceptance']) for r in A]; lab=[f"FY{r['fiscal_year'][2:]}" for r in A]
x=range(len(A)); w=0.38
ax.bar([i-w/2 for i in x],m1,w,color=TEAL,label='Financial statement audit report date')
ax.bar([i+w/2 for i in x],m2,w,color=NAVY,label='Single audit accepted by Federal Audit Clearinghouse')
ax.axhline(9,color=ORANGE,lw=1.6,ls='--'); ax.text(len(A)-0.45,9,'9-month\nstandard',color=ORANGE,fontsize=9,ha='left',va='center',bbox=dict(facecolor='white',edgecolor='none',pad=1.5)); ax.set_xlim(-0.7,len(A)+0.75)
for i,v in enumerate(m2): ax.text(i+w/2,v+0.6,f'{v:.0f}',ha='center',fontsize=8.5,color=NAVY)
ax.set_xticks(list(x)); ax.set_xticklabels(lab); ax.set_ylabel('Months after fiscal year end'); ax.set_ylim(0,56)
ax.set_title('How long after year end the audits were completed and filed'); ax.legend(loc='upper left',fontsize=9)
foot(fig,'Source: Federal Audit Clearinghouse records for the Town of Dartmouth; 2 CFR 200.512(a)(1). Federal extensions applied to some pandemic-period audits.')
fig.savefig(f'{O}/charts/07_audit_timeliness.png'); plt.close(fig)

# 8 fire
F=list(csv.DictReader(open(f'{O}/data/09_fire_district_levies.csv'))); ys=list(range(2016,2027))
fig,ax=plt.subplots(figsize=(9,4.8)); bot=[0]*len(ys)
for d,col in [('Dartmouth Fire #1',NAVY),('Dartmouth Fire #2',TEAL),('Dartmouth Fire #3',GOLD)]:
    v=[float(next(r['total_levy'] for r in F if r['district']==d and int(r['fiscal_year'])==y)) for y in ys]
    ax.bar(fy(ys),v,bottom=bot,color=col,label=d.replace('Dartmouth Fire #','Fire District '),width=0.7,edgecolor='white',linewidth=0.5); bot=[a+b for a,b in zip(bot,v)]
for i,t in enumerate(bot): ax.text(i,t+0.08e6,f'{t/1e6:.2f}',ha='center',fontsize=8.5)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:f'${v/1e6:.0f}M')); ax.set_ylim(0,8e6)
tl=s('tax_levy_total',ys)
ax.set_title(f'Fire district tax levies, FY2016-FY2026 (up {(bot[-1]/bot[0]-1)*100:.0f}%; Town levy up {(tl[-1]/tl[0]-1)*100:.0f}%)'); ax.legend(loc='upper left',ncol=3,fontsize=9)
foot(fig,'Source: Massachusetts Division of Local Services, district tax levies by class (district codes 423, 424, 425). Totals in $ millions.\nThe fire districts are separate governments; their levies are not part of the Town budget or audit.')
fig.savefig(f'{O}/charts/08_fire_district_levies.png'); plt.close(fig)
print('charts done')
