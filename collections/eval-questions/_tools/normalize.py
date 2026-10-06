#!/usr/bin/env python3
"""W2-DOWNLOADS normalizer: raw eval files -> questions.jsonl per eval.
Schema: {eval, eval_org, question_id, question, topic, license, retrieved}
Raw files are never modified; only read.
"""
import csv, json, sys, os, ast, re

ROOT = os.path.expanduser('~/workspace/silent-locus/collections/eval-questions')
RETRIEVED = '2026-10-05'
sys.path.insert(0, os.path.join(ROOT, '_tools'))
from pqdec import decode_column as pq_decode_column

def emit(eval_dir, rows):
    """rows: list of (question_id, question, topic). Writes questions.jsonl, returns count."""
    path = os.path.join(ROOT, eval_dir, 'questions.jsonl')
    with open(path, 'w') as f:
        for qid, q, topic in rows:
            f.write(json.dumps({
                'eval': EVAL, 'eval_org': ORG, 'question_id': qid,
                'question': q, 'topic': topic or '',
                'license': LICENSE, 'retrieved': RETRIEVED,
            }, ensure_ascii=False) + '\n')
    return len(rows)

def norm_ws(s):
    return re.sub(r'\s+', ' ', s).strip() if s else ''

# ---------------- openai-simpleqa ----------------
def do_simpleqa():
    global EVAL, ORG, LICENSE
    EVAL, ORG, LICENSE = 'openai-simpleqa', 'OpenAI', 'MIT (simple-evals repo)'
    rows = []
    with open(f'{ROOT}/openai-simpleqa/raw/simple_qa_test_set.csv', newline='') as f:
        for i, r in enumerate(csv.DictReader(f)):
            try:
                meta = ast.literal_eval(r['metadata'])
            except Exception:
                meta = {}
            topic = meta.get('topic', '') if isinstance(meta, dict) else ''
            rows.append((f'simpleqa-{i:05d}', norm_ws(r['problem']), norm_ws(str(topic))))
    return emit('openai-simpleqa', rows)

# ---------------- google-facts-grounding ----------------
def do_facts():
    global EVAL, ORG, LICENSE
    EVAL, ORG, LICENSE = 'google-facts-grounding', 'Google DeepMind', 'cc-by-4.0'
    csv.field_size_limit(sys.maxsize)
    rows = []
    with open(f'{ROOT}/google-facts-grounding/raw/examples.csv', newline='') as f:
        for i, r in enumerate(csv.DictReader(f)):
            rows.append((f'facts-{i:04d}', norm_ws(r['user_request']), ''))
    return emit('google-facts-grounding', rows)

# ---------------- google-frames ----------------
def do_frames():
    global EVAL, ORG, LICENSE
    EVAL, ORG, LICENSE = 'google-frames', 'Google', 'apache-2.0'
    rows = []
    with open(f'{ROOT}/google-frames/raw/test.tsv', newline='') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            topic = r.get('reasoning_types', '')
            rows.append((f'frames-{len(rows):04d}', norm_ws(r['Prompt']), norm_ws(topic)))
    return emit('google-frames', rows)

# ---------------- assistantbench ----------------
def do_assistantbench():
    global EVAL, ORG, LICENSE
    EVAL, ORG, LICENSE = 'assistantbench', 'Academic (Yoran et al.)', 'apache-2.0'
    rows = []
    with open(f'{ROOT}/assistantbench/raw/assistant_bench_v1.0_test.jsonl') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            d = json.loads(line)
            rows.append((d['id'], norm_ws(d['task']), norm_ws(str(d.get('difficulty') or ''))))
    return emit('assistantbench', rows)

# ---------------- mind2web ----------------
def stream_json_array(fp):
    """Yield top-level objects from a large JSON array file without full json.load."""
    dec = json.JSONDecoder()
    buf = open(fp, encoding='utf-8').read()
    assert buf[0] == '[' and buf.rstrip().endswith(']'), fp
    idx, L = 1, len(buf)
    while idx < L:
        while idx < L and buf[idx] in ' \t\r\n,': idx += 1
        if idx >= L or buf[idx] == ']': break
        obj, idx = dec.raw_decode(buf, idx)
        yield obj

def do_mind2web():
    global EVAL, ORG, LICENSE
    EVAL, ORG, LICENSE = 'mind2web', 'Academic (OSU NLP)', 'cc-by-4.0'
    import glob
    rows = []
    # NOTE: train_* only. test.zip is password-protected (password `mind2web`, public)
    # and the authors ask "Please DO NOT redistribute the unzipped data files online",
    # so test questions are verified by count but not banked in questions.jsonl.
    for fp in sorted(glob.glob(f'{ROOT}/mind2web/raw/train_*.json')):
        for t in stream_json_array(fp):
            q = t.get('confirmed_task') or t.get('task') or ''
            topic = t.get('subdomain') or t.get('domain') or ''
            qid = t.get('annotation_id') or f"m2w-{len(rows):05d}"
            rows.append((qid, norm_ws(q), norm_ws(str(topic))))
    return emit('mind2web', rows)

# ---------------- webvoyager ----------------
def do_webvoyager():
    global EVAL, ORG, LICENSE
    EVAL, ORG, LICENSE = 'webvoyager', 'Academic (Microsoft et al.)', 'apache-2.0'
    rows = []
    with open(f'{ROOT}/webvoyager/raw/WebVoyager_data.jsonl') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            d = json.loads(line)
            rows.append((d['id'], norm_ws(d['ques']), norm_ws(d.get('web_name', ''))))
    return emit('webvoyager', rows)

# ---------------- webarena ----------------
def do_webarena():
    global EVAL, ORG, LICENSE
    EVAL, ORG, LICENSE = 'webarena', 'Academic (CMU)', 'apache-2.0'
    rows = []
    for t in json.load(open(f'{ROOT}/webarena/raw/test.raw.json')):
        sites = t.get('sites') or []
        rows.append((f"webarena-{t.get('task_id'):04d}", norm_ws(t.get('intent', '')),
                     norm_ws(','.join(sites))))
    return emit('webarena', rows)

# ---------------- tau-bench ----------------
def do_taubench():
    global EVAL, ORG, LICENSE
    EVAL, ORG, LICENSE = 'tau-bench', 'Academic (Sierra Research)', 'MIT'
    rows = []
    base = f'{ROOT}/tau-bench/raw/tau-bench/tau_bench/envs'
    for domain in ('airline', 'retail', 'telecom'):
        fp = os.path.join(base, domain, 'tasks.py')
        if not os.path.exists(fp):
            continue
        ns = {}
        exec(open(fp).read(), ns)
        for i, t in enumerate(ns['tasks']):
            rows.append((f'tau-{domain}-{i:03d}', norm_ws(t['instruction']), domain))
    return emit('tau-bench', rows)

# ---------------- sealqa ----------------
def do_sealqa():
    global EVAL, ORG, LICENSE
    EVAL, ORG, LICENSE = 'sealqa', 'Academic (Virginia Tech, vtllms)', 'apache-2.0'
    rows = []
    for split in ('seal-0', 'seal-hard', 'longseal'):
        fp = f'{ROOT}/sealqa/raw/{split}.parquet'
        qs = pq_decode_column(fp, ('question',))
        ts = pq_decode_column(fp, ('topic',))
        for i, (q, t) in enumerate(zip(qs, ts)):
            q = q.decode('utf-8', 'replace') if isinstance(q, bytes) else q
            t = t.decode('utf-8', 'replace') if isinstance(t, bytes) else (t or '')
            rows.append((f'{split}-{i:04d}', norm_ws(q), norm_ws(t)))
    return emit('sealqa', rows)

# ---------------- webwalkerqa ----------------
def do_webwalkerqa():
    global EVAL, ORG, LICENSE
    EVAL, ORG, LICENSE = 'webwalkerqa', 'Alibaba-NLP', 'apache-2.0'
    rows = []
    with open(f'{ROOT}/webwalkerqa/raw/main-00000-of-00001.jsonl') as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line: continue
            d = json.loads(line)
            rows.append((f'webwalkerqa-{i:04d}', norm_ws(d.get('question', d.get('Question', ''))), ''))
    return emit('webwalkerqa', rows)

# ---------------- openai-mle-bench ----------------
def do_mlebench():
    global EVAL, ORG, LICENSE
    EVAL, ORG, LICENSE = 'openai-mle-bench', 'OpenAI', 'MIT'
    rows = []
    base = f'{ROOT}/openai-mle-bench/raw/mle-bench/mlebench/competitions'
    for comp in sorted(os.listdir(base)):
        if comp.startswith('__'): continue
        fp = os.path.join(base, comp, 'description.md')
        if not os.path.exists(fp): continue
        text = open(fp, encoding='utf-8', errors='replace').read()
        rows.append((comp, norm_ws(text), ''))
    return emit('openai-mle-bench', rows)

FUNCS = {
    'openai-simpleqa': do_simpleqa,
    'google-facts-grounding': do_facts,
    'google-frames': do_frames,
    'assistantbench': do_assistantbench,
    'mind2web': do_mind2web,
    'webvoyager': do_webvoyager,
    'webarena': do_webarena,
    'tau-bench': do_taubench,
    'sealqa': do_sealqa,
    'webwalkerqa': do_webwalkerqa,
    'openai-mle-bench': do_mlebench,
}

if __name__ == '__main__':
    EVAL = ORG = LICENSE = ''
    for name in sys.argv[1:]:
        n = FUNCS[name]()
        print(f'{name}: banked {n}')
