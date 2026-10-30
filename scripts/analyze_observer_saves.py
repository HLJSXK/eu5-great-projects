"""Read-only, streaming-per-snapshot ED audit of plaintext EU5 debug saves.

Uses the save writer's record indentation, retains byte offsets, and decodes
Jomini numeric variables as signed 64-bit fixed point (100000 units).
No dependency on another mod checkout. Run with the direct EU5 interpreter.
"""
from __future__ import annotations
import argparse
import csv
import json
import mmap
import re
from collections import Counter, defaultdict
from pathlib import Path
import yaml

REC = re.compile(rb'^(\d+)=\{\r?\n(.*?)^\}', re.M | re.S)
LOC = re.compile(rb'^\t\t(\d+)=\{\r?\n(.*?)^\t\t\}', re.M | re.S)
VAR = re.compile(rb'flag=([\w.]+)\s+(?:tick=\d+\s+)?data=\{\s+type=(\w+)(?:\s+(?:identity|location)=(\d+))?')
CAMP = 'tv_wonder_labor_camp'
SHOP = 'tv_wonder_material_dispatch_point'
GOODS = ['tv_wonder_materials','tools','lumber','stone','marble','clay','sand','coal','masonry','iron','steel','paper','fiber_crops']
SCHEMA = 2

def building_category(typ, pmname, finals):
    if typ == CAMP: return 'camp'
    if typ == SHOP: return 'workshop'
    if typ in finals: return 'final'
    if typ.endswith(('_foundation', '_body', '_function', '_decoration')): return 'module'
    if '_shell_' in pmname or pmname == 'tv_wonder_module_maintenance': return 'shell'
    return 'other'

def scalar(b, key, indent=1, default=0):
    m = re.search(rb'^' + b'\t'*indent + re.escape(key.encode()) + rb'=([^\r\n{]+)', b, re.M)
    if not m: return default
    v=m[1].strip().strip(b'"').decode('utf8',errors='replace')
    try: return float(v) if '.' in v else int(v)
    except ValueError: return v

def block(b, key, indent=1):
    m=re.search(rb'^'+b'\t'*indent+re.escape(key.encode())+rb'=\{(.*?)^'+b'\t'*indent+rb'\}',b,re.M|re.S)
    return m[1] if m else b''

def values(b):
    out={}
    for m in VAR.finditer(b):
        n=int(m[3] or 0)
        if m[2]==b'value': n=(n-(1<<64) if n>=1<<63 else n)/100000
        out[m[1].decode()]=n
    return out

def array(b,key,indent=2):
    m=re.search(rb'^'+b'\t'*indent+key.encode()+rb'=\{([^{}]*)\}',b,re.M)
    return [float(x) for x in m[1].split()] if m else []

def csvwrite(path, rows):
    if not rows: return
    fields=list(dict.fromkeys(k for row in rows for k in row))
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

def analyze(path, finals):
    with path.open('rb') as f, mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ) as m:
        # Section names below are unique writer-owned top-level markers.
        sections=['variables','language_manager','loan_manager','construction_manager','tutorial_manager','countries','market_manager','disaster_manager','building_manager','population','international_organization_manager','weather','locations','expedition_manager']
        offsets={s:m.find(('\n'+s+'={').encode())+1 for s in sections}
        def sect(a,z):
            assert offsets[a]>0 and offsets[z]>offsets[a],(a,z)
            return m[offsets[a]:offsets[z]]
        date=re.search(rb'\bdate=([\d.]+)',m[:200]).group(1).decode()
        header=m[:offsets['variables']]
        names=re.search(rb'\n\t\tlocations=\{([^}]+)\}',header).group(1).split()
        global_vars=values(sect('variables','language_manager'))
        locs={}; territories=Counter()
        for r in LOC.finditer(sect('locations','expedition_manager')):
            b=r[2];owner=scalar(b,'owner',3,-1)
            if owner!=-1: territories[owner]+=1
            locs[int(r[1])]={'owner':owner,'market':scalar(b,'market',3,-1),'access':scalar(b,'market_access',3), 'control':scalar(b,'control',3),'prosperity':scalar(b,'prosperity',3),'tax':scalar(b,'tax',3),'name':names[int(r[1])-1].decode() if 0<int(r[1])<=len(names) else '?'}
        countries=[]; bycid={}
        for r in REC.finditer(sect('countries','market_manager')):
            cid=int(r[1]);b=r[2]
            if cid not in territories:continue
            v=values(block(b,'variables'));e=block(b,'economy');c=block(b,'currency_data');balance=array(e,'recent_balance');income=scalar(e,'income',2)
            row={'date':date,'country':cid,'tag':scalar(b,'definition'),'locations':territories[cid],'country_offset':offsets['countries']+r.start(),'gold':scalar(c,'gold',2),'income':income,'expense':scalar(e,'expense',2),'balance':balance[-1] if balance else 0,'balance_120_mean':sum(balance)/len(balance) if balance else 0,'negative_months':sum(x<0 for x in balance),'balance_months':len(balance),'coin_minting':scalar(e,'coin_minting',2),'stability':scalar(c,'stability',2),'inflation':scalar(b,'inflation'),'war_exhaustion':scalar(c,'war_exhaustion',2),'stage':v.get('tv_wonder_stage',-1),'vars':v}
            row['tag'] = row['tag'] or f'#{cid}'
            row['balance_identity_error']=round(row['balance']-(income-row['expense']),5)
            countries.append(row);bycid[cid]=row
        ios={}
        for r in REC.finditer(sect('international_organization_manager','weather')):
            if scalar(r[2],'type')=='tv_engineering_department':ios[scalar(r[2],'leader')]=values(r[2])
        buildings=[]; bybid={}
        for r in REC.finditer(sect('building_manager','population')):
            b=r[2];typ=scalar(b,'type')
            if not isinstance(typ,str) or not typ.startswith('tv_wonder_'):continue
            lid=scalar(b,'location');loc=locs.get(lid,{})
            pm=re.search(rb'^\t(tv_wonder_\w+)=\{',b,re.M)
            pmname=pm[1].decode() if pm else ''
            missing=block(block(b,pmname),'missing',2) if pmname else b''
            miss={k.decode():float(v) for k,v in re.findall(rb'^\t\t\t(\w+)=(-?[\d.]+)',missing,re.M)}
            typcat=building_category(typ, pmname, finals)
            row={'date':date,'id':int(r[1]),'offset':offsets['building_manager']+r.start(),'type':typ,'category':typcat,'location':lid,'location_name':loc.get('name'),'owner':scalar(b,'owner'),'market':loc.get('market',-1),'level':scalar(b,'level'),'employed':scalar(b,'employed'),'open':scalar(b,'open',default='omitted'),'upkeep':scalar(b,'upkeep'),'profit':scalar(b,'last_months_profit'),'pm':pmname,'input_saved':scalar(block(b,pmname),'input',2,None) if pmname else None,'missing_materials':miss.get('tv_wonder_materials',0),'missing_tools':miss.get('tools',0),'missing_goods':miss}
            buildings.append(row);bybid[row['id']]=row
        queues=[]
        for r in REC.finditer(sect('construction_manager','tutorial_manager')):
            b=r[2];bid=scalar(b,'building',default=-1);bd=bybid.get(bid)
            if not bd:continue
            q={'date':date,'id':int(r[1]),'offset':offsets['construction_manager']+r.start(),'building':bid,'type':bd['type'],'category':bd['category'],'owner':scalar(b,'country'),'location':scalar(b,'location'),'paid':scalar(block(b,'actual_currency_spent'),'gold',2),'progress':scalar(b,'progress'),'total':scalar(b,'total')}
            queues.append(q)
        loans=defaultdict(float)
        for r in REC.finditer(sect('loan_manager','construction_manager')):loans[scalar(r[2],'borrower')]+=scalar(r[2],'amount')
        markets=[]; bymarket={}
        for r in REC.finditer(sect('market_manager','disaster_manager')):
            b=r[2];mid=int(r[1]);center=scalar(b,'center')
            for good in GOODS:
                gb=block(b,good,2)
                if not gb:continue
                row={'date':date,'market':mid,'center':center,'center_name':locs.get(center,{}).get('name'),'good':good}
                for k in ['price','supply','demand','total_taken','stockpile','possible','extra_supply_from_stockpile']:row[k]=scalar(gb,k,3)
                for group in ['supplied','demanded','taken']:
                    for k,v in re.findall(rb'^\t\t\t\t(\w+)=(-?[\d.]+)',block(gb,group,3),re.M):row[group+'_'+k.decode()]=float(v)
                markets.append(row);bymarket[mid,good]=row
        for row in countries:
            cid=row['country'];owned=[b for b in buildings if b['owner']==cid]
            row['debt']=loans[cid]
            for cat in ['camp','workshop','final','shell','module','other']:
                bs=[b for b in owned if b['category']==cat]
                row[cat+'_levels']=sum(b['level'] for b in bs)
                row[cat+'_upkeep']=sum(b['upkeep'] for b in bs)
            row['wonder_upkeep']=sum(b['upkeep'] for b in owned if b['category']!='workshop')
        projects=[]
        for c in countries:
            if c['stage']<0:continue
            v=c['vars'];iv=ios.get(c['country'],{});site=v.get('tv_wonder_site',-1);loc=locs.get(site,{})
            row={k:val for k,val in c.items() if k!='vars'}
            row.update({k.removeprefix('tv_wonder_'):val for k,val in v.items() if k.startswith('tv_wonder_')})
            row.update({'io_'+k.removeprefix('tv_wonder_'):val for k,val in iv.items()})
            row.update({'site_name':loc.get('name'),'site_owner':loc.get('owner'),'market':loc.get('market',-1),'market_access':loc.get('access'),'site_control':loc.get('control')})
            camps=[b for b in buildings if b['type']==CAMP and b['location']==site and b['owner']==c['country']]
            row['site_camps']=sum(b['level'] for b in camps);row['site_employed']=sum(b['employed'] for b in camps)
            row['site_closed_camps']=sum(b['level'] for b in camps if b['open']=='no')
            row['site_queued_camps']=sum(q['category']=='camp' and q['owner']==c['country'] and q['location']==site for q in queues)
            row['camp_missing_materials']=sum(b['missing_materials'] for b in camps);row['camp_missing_tools']=sum(b['missing_tools'] for b in camps)
            for good in ['tv_wonder_materials','tools']:
                for k,val in bymarket.get((row['market'],good),{}).items():
                    if k not in ['date','good','market']:row[good+'_'+k]=val
            projects.append(row)
        summary={'schema':SCHEMA,'date':date,'file':str(path.resolve()),'bytes':path.stat().st_size,'countries':len(countries),'ed_countries':len(projects),'log_count':global_vars.get('cmf_log_count'),'ai_enabled':global_vars.get('tv_engineering_department_ai_enabled')}
        summary.update({'stage_'+str(i):sum(c['stage']==i for c in countries) for i in range(6)})
        for cat in ['camp','workshop','final','shell','module','other']:
            bs=[b for b in buildings if b['category']==cat]
            summary[cat+'_count']=sum(b['level']>0 for b in bs);summary[cat+'_levels']=sum(b['level'] for b in bs);summary[cat+'_employed']=sum(b['employed'] for b in bs);summary[cat+'_upkeep']=sum(b['upkeep'] for b in bs)
        for c in countries:c.pop('vars')
        return {'snapshot':summary,'countries':countries,'projects':projects,'buildings':buildings,'markets':markets,'queues':queues}

def main():
    p=argparse.ArgumentParser();p.add_argument('--archive',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--year');a=p.parse_args()
    finals=set()
    for fn,key in [('wonders.yaml','wonders'),('unique_wonders.yaml','unique_wonders')]:
        for w in yaml.safe_load((Path('data')/fn).read_text('utf8'))[key]:
            if w.get('final_building'):finals.add(w['final_building'])
            finals.update(w.get('final_buildings',{}).values() if isinstance(w.get('final_buildings'),dict) else w.get('final_buildings',[]))
    a.out.mkdir(parents=True,exist_ok=True)
    allrows=defaultdict(list)
    for path in sorted(a.archive.glob((a.year or '')+'*.eu5')):
        cache=a.out/(path.name.split('_')[0]+'.json')
        result=json.loads(cache.read_text('utf8')) if cache.exists() else None
        if not result or result['snapshot'].get('schema') != SCHEMA or result['snapshot']['bytes'] != path.stat().st_size or result['snapshot']['file'] != str(path.resolve()):
            result=analyze(path,finals)
            cache.write_text(json.dumps(result,ensure_ascii=False),encoding='utf8')
        for k,v in result.items():allrows[k].extend([v] if k=='snapshot' else v)
        print(json.dumps(result['snapshot'],ensure_ascii=True),flush=True)
    for k,rows in allrows.items():csvwrite(a.out/(k+'.csv'),rows)

if __name__=='__main__':main()
