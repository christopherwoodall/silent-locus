#!/usr/bin/env python3
"""Reviewer B: stream-scan openhands_qwen35_122b shard, batch-wise, low memory."""
import pyarrow.parquet as pq, re, json

PARQUET = '/home/hatch/workspace/silent-locus/data/lanes/openswe-trajectories/raw/openhands_qwen35_122b_swe-rebench-v2_train-00000-of-00017.parquet'

GIT_PAT = re.compile(r'\bgit\s+(log|show|fsck|reflog|stash|blame|checkout|fetch|pull|cherry|diff|branch|tag|rev-parse|grep|cat-file|ls-tree|ls-files)\b', re.I)
GIT_PLAIN = re.compile(r'(?<![\w-])git(?![\w-])', re.I)
NET_PAT = re.compile(r'(curl|wget|pip install|pip download|npm install|git clone|github\.com|raw\.githubusercontent|api\.github|gitlab|huggingface\.co)', re.I)
TEST_EDIT_PATH = re.compile(r'(test_|_test\.|/tests/|/test/|spec\.|\.spec\.|\.test\.)', re.I)
EDIT_FN = re.compile(r'(edit|str_replace|write|apply_patch|insert|create)', re.I)
ERR_PAT = re.compile(r'(error|failed|exception|traceback|not found|no such file|command not found|denied|refused|returned non-zero)', re.I)

def features(r):
    msgs = r['messages'] or []
    toolnames = []
    git_hits, net_hits, test_edits, err_steps = [], [], [], []
    prev_sig, cur_streak, max_streak = None, 1, 1
    n_plain_git = 0
    for i, m in enumerate(msgs):
        tcs = m.get('tool_calls') or []
        for tc in tcs:
            fn = (tc.get('function') or {}).get('name', '') or ''
            args = (tc.get('function') or {}).get('arguments', '') or ''
            toolnames.append(fn)
            sig = fn + '|' + args[:200]
            if sig == prev_sig:
                cur_streak += 1
                max_streak = max(max_streak, cur_streak)
            else:
                cur_streak = 1
            prev_sig = sig
            if GIT_PAT.search(args):
                git_hits.append([i, fn, args[:300].replace('\n', ' ')])
            elif GIT_PLAIN.search(args):
                n_plain_git += 1
            if NET_PAT.search(args):
                net_hits.append([i, fn, args[:300].replace('\n', ' ')])
            if TEST_EDIT_PATH.search(args) and EDIT_FN.search(fn):
                test_edits.append([i, fn, args[:300].replace('\n', ' ')])
        c = m.get('content') or ''
        if m.get('role') == 'tool' and ERR_PAT.search(c):
            err_steps.append(i)
    md = r.get('metadata') or {}
    refp = ((md.get('reference_patch') or {}).get('patch')) or ''
    modp = ((md.get('model_patch') or {}).get('patch')) or ''
    # patch similarity: Jaccard over stripped lines
    rs = set(l.strip() for l in refp.splitlines() if l.strip())
    ms = set(l.strip() for l in modp.splitlines() if l.strip())
    jacc = (len(rs & ms) / len(rs | ms)) if (rs | ms) else 0.0
    return {
        'trajectory_id': r['trajectory_id'], 'instance_id': r['instance_id'],
        'repo': r['repo'], 'language': r['language'], 'resolved': r['resolved'],
        'category': md.get('category'),
        'teacher': ((md.get('teacher_model') or {}).get('name')),
        'ref_lines': len(refp.splitlines()), 'mod_lines': len(modp.splitlines()),
        'patch_jaccard': round(jacc, 3),
        'steps': len(msgs), 'n_toolcalls': len(toolnames),
        'top_tools': dict(__import__('collections').Counter(toolnames).most_common(8)),
        'git_hits': git_hits, 'n_plain_git': n_plain_git, 'net_hits': net_hits,
        'test_edits': test_edits, 'n_err_steps': len(err_steps),
        'max_repeat_streak': max_streak,
    }

def main():
    f = pq.ParquetFile(PARQUET)
    feats = []
    for batch in f.iter_batches(batch_size=40, columns=['instance_id','repo','language','trajectory_id','resolved','messages','metadata']):
        for r in batch.to_pylist():
            try:
                feats.append(features(r))
            except Exception as e:
                feats.append({'trajectory_id': r.get('trajectory_id'), 'error': str(e)})
    json.dump(feats, open('/tmp/reviewerB_feats.json','w'))
    print("rows:", len(feats))
    import collections
    c = collections.Counter()
    for x in feats:
        if x.get('error'): c['error'] += 1; continue
        if x['git_hits']: c['git_hits'] += 1
        if x['net_hits']: c['net_hits'] += 1
        if x['test_edits']: c['test_edits'] += 1
        if x['patch_jaccard'] >= 0.9 and x['mod_lines'] > 3: c['patch_dup'] += 1
        if x['resolved']==1 and x['steps'] <= 8: c['short_resolved'] += 1
        if x['max_repeat_streak'] >= 6: c['repeat_streak'] += 1
        if x['resolved']==1 and x['n_err_steps']>=3: c['err_then_ok'] += 1
    print(json.dumps(dict(c), indent=1))
    # resolved distribution
    print("resolved:", collections.Counter(x.get('resolved') for x in feats))

main()
