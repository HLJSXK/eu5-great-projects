"""Audit construction migration using only peasants_free_peasantry countries.

Read-only plaintext save extraction. Population is summed from actual pop sizes,
not the location population_ratio field (which can describe capacity).
"""
from __future__ import annotations
import argparse
import json
import mmap
import re
import statistics
from collections import defaultdict
from pathlib import Path
if __package__:
    from .analyze_observer_saves import LOC, REC, block, scalar, values, csvwrite
else:
    from analyze_observer_saves import LOC, REC, block, scalar, values, csvwrite

MOD='tv_wonder_construction_migration_attraction_location_modifier'
PRIV='peasants_free_peasantry'
TYPES=['peasants','laborers','nobles','clergy','burghers','soldiers','tribesmen','slaves']
FLOW=['MigrationIn','MigrationOut','Reproduction','Starvation','PromotionIn','PromotionOut','DemotionIn','DemotionOut']
PIDS=re.compile(rb'^\t{4}pops=\{([^}]+)\}',re.M)

def has_migration_right(b):
    government=block(b,'government')
    match=re.search(rb'^\t{2}implemented_privileges=\{',government,re.M)
    if not match:return False
    start=match.end();depth=1;end=start
    # The privilege list closes with compact `}}`, unlike ordinary save blocks.
    for token in re.finditer(rb'[{}]',government[start:]):
        depth += 1 if token[0]==b'{' else -1
        if depth==0:end=start+token.start();break
    if depth:raise ValueError('Unclosed implemented_privileges')
    privileges=government[start:end]
    return bool(re.search(rb'\bobject='+PRIV.encode()+rb'(?:\s|$)',privileges))

def population_flows(pb):
    row={}
    for typ in TYPES:
        tb=block(pb,typ,5);cb=block(tb,'changes',6)
        row[typ+'_unemployed']=scalar(tb,'unemployed',6)
        for key in FLOW:row[typ+'_'+key]=scalar(cb,key,7)
    return row

def extract(path, project_cache):
    previous=json.loads(project_cache.read_text('utf8'))
    project_by_country={p['country']:p for p in previous['projects']}
    countries={};locs={};pop_location={}
    with path.open('rb') as f,mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ) as m:
        date=re.search(rb'\bdate=([\d.]+)',m[:200])[1].decode()
        names=re.search(rb'\n\t\tlocations=\{([^}]+)\}',m[:m.find(b'\nvariables={')])[1].split()
        ca=m.find(b'\ncountries={');cz=m.find(b'\nmarket_manager={',ca)
        for r in REC.finditer(m,ca,cz):
            cid=int(r[1]);b=r[2]
            if not has_migration_right(b) or cid not in project_by_country:continue
            p=project_by_country[cid]
            countries[cid]={'country':cid,'tag':p['tag'],'stage':p['stage'],'site':p.get('site',-1),'locked':p.get('locked',0),'offset':r.start(),'gold':p['gold'],'balance':p['balance']}
        a=m.find(b'\nlocations={');z=m.find(b'\nexpedition_manager={',a)
        for r in LOC.finditer(m,a,z):
            b=r[2];owner=scalar(b,'owner',3,-1)
            if owner not in countries:continue
            lid=int(r[1]);pb=block(b,'population',3);tm=block(b,'timed_modifiers',3)
            found=re.search(rb'modifier='+MOD.encode()+rb'\s+start_date=([\d.]+)',tm)
            row={'date':date,'location':lid,'name':names[lid-1].decode(),'owner':owner,'tag':countries[owner]['tag'],'rank':scalar(b,'rank',3),'market':scalar(b,'market',3,-1),'controller':scalar(b,'controller',3,-1),'development':scalar(b,'development',3),'prosperity':scalar(b,'prosperity',3),'control':scalar(b,'control',3),'offset':r.start(),'construction_attraction':bool(found),'modifier_start':found[1].decode() if found else '', 'current_site':countries[owner]['stage']==3 and countries[owner]['site']==lid}
            row.update(population_flows(pb));row.update({t+'_size':0 for t in TYPES})
            for pid in (PIDS.search(pb)[1].split() if PIDS.search(pb) else []):
                pid=int(pid);assert pid not in pop_location;pop_location[pid]=lid
            locs[lid]=row
        a=m.find(b'\npopulation={');z=m.find(b'\nsubunit_manager={',a);matched=0
        for r in REC.finditer(m,a,z):
            lid=pop_location.get(int(r[1]))
            if lid is None:continue
            b=r[2];typ=scalar(b,'type');size=scalar(b,'size');locs[lid][str(typ)+'_size']=locs[lid].get(str(typ)+'_size',0)+size;matched+=1
        assert matched==len(pop_location),(matched,len(pop_location))
        for row in locs.values():
            row['population']=sum(row.get(t+'_size',0) for t in TYPES)
            for k in ['size','unemployed']+FLOW:row['commoners_'+k]=row['peasants_'+k]+row['laborers_'+k]
            row['commoners_net_migration']=row['commoners_MigrationIn']+row['commoners_MigrationOut']
            row['net_migration']=sum(row[t+'_MigrationIn']+row[t+'_MigrationOut'] for t in TYPES)
        rows=[];summary={'date':date,'source':str(path.resolve()),'bytes':path.stat().st_size,'eligible_countries':len(countries),'eligible_locations':len(locs),'matched_pops':matched}
        for cid,c in countries.items():
            own=[x for x in locs.values() if x['owner']==cid];c['population']=sum(x['population'] for x in own);c['commoners_size']=sum(x['commoners_size'] for x in own);c['inflow']=sum(x['commoners_MigrationIn'] for x in own);c['outflow']=sum(x['commoners_MigrationOut'] for x in own)
            for loc in own:
                if not loc['construction_attraction'] and not loc['current_site']:continue
                row=dict(loc);p=project_by_country[cid]
                for k in ['stage','locked','level','site_camps','site_employed','site_closed_camps','site_queued_camps','monthly_construction_progress','io_domestic_support']:row[k]=p.get(k)
                controls=[x for x in own if not x['construction_attraction'] and x['location']!=loc['location'] and x['rank']==loc['rank']]
                row.update({'country_population':c['population'],'country_commoners':c['commoners_size'],'country_inflow':c['inflow'],'country_outflow':c['outflow'],'country_locations':len(own),'control_count':len(controls)})
                row['inflow_rank']=1+sum(x['commoners_MigrationIn']>loc['commoners_MigrationIn']+.000001 for x in own)
                for k in ['commoners_MigrationIn','commoners_net_migration','population']:
                    row['control_median_'+k]=statistics.median(x[k] for x in controls) if controls else None
                row['inflow_share']=row['commoners_MigrationIn']/c['inflow'] if c['inflow']>0 else None
                row['population_share']=row['population']/c['population'] if c['population']>0 else None
                row['monthly_inflow_per_1000']=1000*row['commoners_MigrationIn']/row['commoners_size'] if row['commoners_size']>0 else None
                row['commoners_unemployment_rate']=row['commoners_unemployed']/row['commoners_size'] if row['commoners_size']>0 else None
                rows.append(row)
        summary.update({'eligible_stage3':sum(c['stage']==3 for c in countries.values()),'sites':len(rows),'modified_locations':sum(x['construction_attraction'] for x in rows),'modifier_outside_active_site':sum(x['construction_attraction'] and not x['current_site'] for x in rows)})
        return {'summary':summary,'countries':list(countries.values()),'sites':rows,'locations':list(locs.values())}

def main():
    p=argparse.ArgumentParser();p.add_argument('--archive',type=Path,required=True);p.add_argument('--project-cache',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--year',default='');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    for path in sorted(a.archive.glob(a.year+'*.eu5')):
        key=path.name.split('_')[0];target=a.out/(key+'.json')
        if target.exists():r=json.loads(target.read_text('utf8'))
        else:
            r=extract(path,a.project_cache/(key+'.json'));target.write_text(json.dumps(r,ensure_ascii=False),encoding='utf8')
        print(json.dumps(r['summary']),flush=True)

if __name__=='__main__':main()
