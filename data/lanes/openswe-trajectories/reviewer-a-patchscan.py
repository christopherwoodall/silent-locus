import re, json
import pyarrow.parquet as pq
PARQUET='raw/sweagent_minimax_m25_swe-rebench-v2_train-00000-of-00019.parquet'
def files_in_patch(patch):
    return re.findall(r'diff --git a/(\S+)', patch or '')
def test_in_patch(patch):
    return [f for f in files_in_patch(patch) if re.search(r'/(tests?|__tests__|spec|e2e)/|(_test\.|\.test\.|_spec\.|\.spec\.)', f, re.I)]
def jaccard(a, b):
    sa=set(l.strip() for l in (a or '').splitlines() if l.strip())
    sb=set(l.strip() for l in (b or '').splitlines() if l.strip())
    return len(sa & sb)/len(sa | sb) if (sa | sb) else 0.0
pf=pq.ParquetFile(PARQUET)
rows=[]
for batch in pf.iter_batches(batch_size=200, columns=['trajectory_id','instance_id','resolved','language','metadata']):
    tids=batch.column('trajectory_id').to_pylist()
    iids=batch.column('instance_id').to_pylist()
    ress=batch.column('resolved').to_pylist()
    langs=batch.column('language').to_pylist()
    mcol=batch.column('metadata')
    for i in range(batch.num_rows):
        md=mcol[i].as_py() or {}
        mp=(md.get('model_patch') or {}); rp=(md.get('reference_patch') or {})
        mpp=mp.get('patch') or ''; rpp=rp.get('patch') or ''
        rows.append({
            'tid':tids[i],'iid':iids[i],'res':ress[i],'lang':langs[i],
            'm_files':mp.get('num_modified_files') or 0,'m_lines':mp.get('num_modified_lines') or 0,
            'r_files':rp.get('num_modified_files') or 0,'r_lines':rp.get('num_modified_lines') or 0,
            'jacc':round(jaccard(mpp,rpp),3),
            'test_files':test_in_patch(mpp),
            'mp_len':len(mpp),
        })
    del batch
print('total:',len(rows))
# resolved with empty/tiny patch
print('--- resolved=1 with m_lines<=2 ---')
for r in rows:
    if r['res']==1 and r['m_lines']<=2:
        print(r['tid'][:36], r['iid'][:55], 'm_files=',r['m_files'],'m_lines=',r['m_lines'],'jacc=',r['jacc'])
print('--- resolved=1 with test files in model_patch ---')
for r in rows:
    if r['res']==1 and r['test_files']:
        print(r['tid'][:36], r['iid'][:55], r['test_files'])
print('--- high jaccard (>=0.7) resolved=1, m_lines>=20 ---')
for r in sorted(rows,key=lambda x:-x['jacc']):
    if r['res']==1 and r['jacc']>=0.7 and r['m_lines']>=20:
        print(r['tid'][:36], r['iid'][:55], 'jacc=',r['jacc'],'m_lines=',r['m_lines'],'r_lines=',r['r_lines'])
    if r['jacc']<0.7: break
print('--- resolved=-1 with big patch (submitted despite failure?) ---')
for r in rows:
    if r['res']==-1 and r['m_lines']>=50:
        print(r['tid'][:36], r['iid'][:55], 'm_lines=',r['m_lines'])
json.dump(rows, open('reviewer-a-patchstats.json','w'))
