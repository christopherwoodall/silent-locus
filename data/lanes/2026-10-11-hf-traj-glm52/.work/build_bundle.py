#!/usr/bin/env python3
"""Build the Factum submission bundle for lane 2026-10-11-hf-traj-glm52.

Reads .work/ extraction outputs, emits .work/bundle-glm52.json for
`factum add --input`. One bundle: 1 source + 86 trajectory intel.behavior +
57 command-frequency intel.behavior + 1 model-profile intel.behavior +
12 infra.ioc URL records.
"""
import json, os, re
from collections import defaultdict

REPO = os.path.expanduser('~/workspace/silent-locus')
SRC = os.path.join(REPO, 'evidence/hf-trajectories/raw/0xsero-glm-5.2-nf3-hybrid-terminal-bench-2.1-traces/traces')
WORK = os.path.dirname(os.path.abspath(__file__))
LANE = '2026-10-11-hf-traj-glm52'
MODEL = 'openai/GLM-5.2'
HARNESS = 'terminus-2'
DATASET = '0xsero-glm-5.2-nf3-hybrid-terminal-bench-2.1-traces'

BASE_TAGS = {
    'lane': LANE,
    'model': MODEL,
    'harness': HARNESS,
    'source_dataset': DATASET,
    'grade': 'OBSERVED',
}

PROMPT_RE = re.compile(r'\x1b\[\?2004hroot@[^:]+:[^#]*# ')
ANSI_RE = re.compile(r'\x1b\[[0-9;?]*[a-zA-Z]')

def pane_commands(pane_path):
    data = open(pane_path, 'rb').read().decode('utf-8', 'replace')
    cmds = []
    for m in PROMPT_RE.finditer(data):
        seg = data[m.end():]
        end = seg.find('\r')
        if end < 0:
            end = len(seg)
        cmd = ANSI_RE.sub('', seg[:end]).strip()
        if cmd:
            cmds.append(cmd)
    if cmds and cmds[0].startswith('asciinema rec'):
        cmds = cmds[1:]
    if cmds and cmds[0] == 'clear':
        cmds = cmds[1:]
    return cmds

def obs(ref, rtype, data_schema, data, source_ref, observed_at, tags):
    return {
        'ref': ref,
        'kind': 'observation',
        'body': {
            'type': rtype,
            'data_schema': data_schema,
            'data': data,
            'source': source_ref,
            'observed_at': observed_at,
            'time_basis': 'source_metadata',
            'files': [],
        },
        'tags': tags,
    }

def main():
    trajs = [json.loads(l) for l in open(os.path.join(WORK, 'trajectories.jsonl'))]
    cmd_counts = []
    with open(os.path.join(WORK, 'commands.tsv')) as f:
        for line in f:
            n, c = line.rstrip('\n').split('\t', 1)
            cmd_counts.append((int(n), c))
    urls = json.load(open(os.path.join(WORK, 'urls.json')))
    seqs = json.load(open(os.path.join(WORK, 'sequences.json')))

    # per-command trajectory presence (second pane pass)
    cmd_trajs = defaultdict(set)
    for t in trajs:
        p = os.path.join(SRC, t['dir'], 'agent', 'terminus_2.pane')
        if os.path.exists(p):
            for c in set(pane_commands(p)):
                cmd_trajs[c].add(t['dir'])

    earliest = min(t['ts_first'] for t in trajs if t['ts_first'])
    first_date = earliest[:10]

    records = []
    records.append({
        'ref': 'src0',
        'kind': 'source',
        'body': {
            'source_type': 'dataset',
            'locator': 'evidence/hf-trajectories/raw/0xsero-glm-5.2-nf3-hybrid-terminal-bench-2.1-traces/traces/',
            'title': '0xsero GLM-5.2 nf3 hybrid terminal-bench 2.1 traces (86 trajectories, terminus-2 harness)',
            'platform': 'huggingface',
        },
        'tags': dict(BASE_TAGS),
    })

    # 1. per-trajectory intel.behavior
    for i, t in enumerate(trajs):
        desc = (
            f"Trajectory {t['dir']}: model {t['model']} under harness {t['harness']} "
            f"v{t['harness_version']} on terminal-bench task '{t['task']}' (run {t['runid']}). "
            f"{t['n_steps']} steps from {t['ts_first']} to {t['ts_last']}; "
            f"{t['n_commands']} shell commands executed ({t['n_distinct_commands']} distinct). "
            f"Token metrics: prompt={t['prompt_tokens']}, completion={t['completion_tokens']}, "
            f"cached={t['cached_tokens']}."
        )
        records.append(obs(
            f'traj-{i}', 'intel.behavior', 'urn:factum:intel:behavior:1',
            {
                'category': 'trajectory_profile',
                'description': desc,
                'evaluations_seen_on': ['terminal-bench'],
                'models_affected': [MODEL],
                'first_observed': t['ts_first'][:10] if t['ts_first'] else first_date,
                'provenance': f'{LANE}: {DATASET}/traces/{t["dir"]}/agent/trajectory.json',
                'severity': 'minimal',
            },
            '@src0', t['ts_first'] or earliest,
            dict(BASE_TAGS, task=t['task'], run_id=t['runid']),
        ))

    # 2. command-frequency intel.behavior (count >= 5)
    top_cmds = [(n, c) for n, c in cmd_counts if n >= 5]
    for i, (n, c) in enumerate(top_cmds):
        ntraj = len(cmd_trajs.get(c, ()))
        desc = (
            f"Command {c!r} executed {n} times across {ntraj} of 86 "
            f"{MODEL}/{HARNESS} terminal-bench trajectories (dataset {DATASET})."
        )
        records.append(obs(
            f'cmd-{i}', 'intel.behavior', 'urn:factum:intel:behavior:1',
            {
                'category': 'command_frequency',
                'description': desc,
                'evaluations_seen_on': ['terminal-bench'],
                'models_affected': [MODEL],
                'first_observed': first_date,
                'provenance': f'{LANE}: aggregated from terminus_2.pane input prompts across 86 trajectories',
                'severity': 'minimal',
            },
            '@src0', earliest,
            dict(BASE_TAGS, command_count=str(n), trajectory_count=str(ntraj)),
        ))

    # 3. dataset-level model command profile
    bigram_lines = '\n'.join(f"- {k}  (x{v})" for k, v in seqs['bigrams'][:12])
    trigram_lines = '\n'.join(f"- {k}  (x{v})" for k, v in seqs['trigrams'][:8])
    desc = (
        f"Command-use profile for {MODEL} under {HARNESS} across 86 terminal-bench "
        f"trajectories (dataset {DATASET}): {sum(n for n, _ in cmd_counts)} command "
        f"executions, {len(cmd_counts)} distinct. Dominant pattern is inline Python "
        f"via heredoc: \"python3 - <<'PY'\" is the top command (678 executions) and "
        f"self-loops 307 times, i.e. the model prefers pasting scripts into stdin "
        f"over writing files. Recurring sequences:\nTop bigrams:\n{bigram_lines}\n"
        f"Top trigrams:\n{trigram_lines}\n"
        f"Notable: a 4-step training-monitor loop (ps train.pid -> ls caffemodel -> "
        f"sleep 60 -> tail training_output.txt) repeats ~20x; interrupt signals "
        f"(Ctrl-C, echoed ^C) appear 30 times, showing the model interrupts "
        f"long-running processes."
    )
    records.append(obs(
        'model-profile', 'intel.behavior', 'urn:factum:intel:behavior:1',
        {
            'category': 'model_command_profile',
            'description': desc,
            'evaluations_seen_on': ['terminal-bench'],
            'models_affected': [MODEL],
            'first_observed': first_date,
            'provenance': f'{LANE}: aggregated from 86 trajectories in {DATASET}',
            'severity': 'minimal',
        },
        '@src0', earliest, dict(BASE_TAGS),
    ))

    # 4. URL infra.ioc
    for i, (u, locs) in enumerate(sorted(urls.items())):
        tasks = sorted({d for d, _ in locs})
        desc_ts = min(t['ts_first'] for t in trajs if t['dir'] in {d for d, _ in locs} and t['ts_first']) or earliest
        records.append(obs(
            f'url-{i}', 'infra.ioc', 'urn:factum:infra:ioc:1',
            {
                'term': u,
                'category': 'url-pattern',
                'provenance': f"{LANE}: seen in step messages of {len(locs)} step(s) in task(s) {', '.join(tasks)} ({DATASET})",
                'status': 'active',
            },
            '@src0', desc_ts,
            dict(BASE_TAGS, task=','.join(tasks)),
        ))

    bundle = {
        'bundle': 2,
        'actor': 'agent:lane-ingest-hf-traj-glm52',
        'idempotency_key': 'hf-traj-glm52-2026-10-11-v1',
        'records': records,
    }
    out = os.path.join(WORK, 'bundle-glm52.json')
    json.dump(bundle, open(out, 'w'), indent=1)
    by_type = defaultdict(int)
    for r in records:
        by_type[r['body']['type'] if r['kind'] == 'observation' else r['kind']] += 1
    print(f'wrote {out}: {len(records)} records -> {dict(by_type)}')

if __name__ == '__main__':
    main()
