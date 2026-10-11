#!/usr/bin/env python3
"""Extract behavioral indicators from 0xsero GLM-5.2 terminal-bench traces.

Source: evidence/hf-trajectories/raw/0xsero-glm-5.2-nf3-hybrid-terminal-bench-2.1-traces/traces/
Each dir <task>__<runid>/agent/ contains trajectory.json + terminus_2.pane.

Command source: the terminal pane stream. Each executed command is typed
after a readline prompt marked by ESC[?2004h (bracketed-paste mode enable).
Heredoc/stdin bodies never match the prompt pattern, so this yields exactly
the executed command lines. The first two pane commands in every trajectory
are harness-typed (asciinema rec wrapper; a `clear` issued ~0.5s in, minutes
before the agent's first response) and are excluded.

Outputs (into this lane's .work/):
  commands.tsv      - count TAB command (model-wide, most common first)
  urls.json         - distinct URLs -> [[task, step_id], ...]
  sequences.json    - top command bigrams/trigrams
  trajectories.jsonl- per-trajectory summary rows
  progress.json     - resumable progress marker
"""
import json, os, re
from collections import Counter, defaultdict

REPO = os.path.expanduser('~/workspace/silent-locus')
SRC = os.path.join(REPO, 'evidence/hf-trajectories/raw/0xsero-glm-5.2-nf3-hybrid-terminal-bench-2.1-traces/traces')
WORK = os.path.dirname(os.path.abspath(__file__))

URL_RE = re.compile(r'https?://[^\s"\'<>)\]`]+')
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
    # drop the two harness-typed prefix commands (asciinema rec, clear)
    if cmds and cmds[0].startswith('asciinema rec'):
        cmds = cmds[1:]
    if cmds and cmds[0] == 'clear':
        cmds = cmds[1:]
    return cmds

def main():
    dirs = sorted(d for d in os.listdir(SRC) if os.path.isdir(os.path.join(SRC, d)))
    progress_path = os.path.join(WORK, 'progress.json')
    done = set()
    if os.path.exists(progress_path):
        try:
            done = set(json.load(open(progress_path)).get('files_processed', []))
        except Exception:
            pass

    trajs = []
    cmd_counter = Counter()
    seq_bigram = Counter()
    seq_trigram = Counter()
    urls = defaultdict(set)
    processed = list(done)

    for d in dirs:
        if d in done:
            continue
        tpath = os.path.join(SRC, d, 'agent', 'trajectory.json')
        ppath = os.path.join(SRC, d, 'agent', 'terminus_2.pane')
        if not os.path.exists(tpath):
            continue
        t = json.load(open(tpath, encoding='utf-8', errors='replace'))
        task = d.split('__')[0]
        runid = d.split('__', 1)[1] if '__' in d else ''
        steps = t.get('steps', [])
        ts = [s.get('timestamp') for s in steps if s.get('timestamp')]
        fm = t.get('final_metrics', {}) or {}
        agent = t.get('agent', {}) or {}

        for s in steps:
            msg = s.get('message', '')
            if not isinstance(msg, str):
                continue
            for u in URL_RE.findall(msg):
                u = u.rstrip('.,;:!?)')
                if u and u != 'https://':
                    urls[u].add((d, s.get('step_id')))

        cmds = pane_commands(ppath) if os.path.exists(ppath) else []
        for c in cmds:
            cmd_counter[c] += 1
        for a, b in zip(cmds, cmds[1:]):
            seq_bigram[(a, b)] += 1
        for a, b, c in zip(cmds, cmds[1:], cmds[2:]):
            seq_trigram[(a, b, c)] += 1

        trajs.append({
            'dir': d, 'task': task, 'runid': runid,
            'model': agent.get('model_name'), 'harness': agent.get('name'),
            'harness_version': agent.get('version'),
            'n_steps': len(steps),
            'ts_first': min(ts) if ts else None,
            'ts_last': max(ts) if ts else None,
            'prompt_tokens': fm.get('total_prompt_tokens'),
            'completion_tokens': fm.get('total_completion_tokens'),
            'cached_tokens': fm.get('total_cached_tokens'),
            'n_commands': len(cmds),
            'n_distinct_commands': len(set(cmds)),
        })
        processed.append(d)
        json.dump({'files_processed': processed,
                   'n_trajectories': len(processed),
                   'n_dirs_total': len(dirs)},
                  open(progress_path, 'w'))

    out = {
        'n_dirs': len(dirs),
        'n_processed_this_run': len(trajs),
        'n_distinct_commands': len(cmd_counter),
        'n_command_executions': sum(cmd_counter.values()),
        'n_distinct_urls': len(urls),
        'n_bigrams': len(seq_bigram),
    }
    json.dump(out, open(os.path.join(WORK, 'extract_stats.json'), 'w'), indent=1)
    with open(os.path.join(WORK, 'commands.tsv'), 'w') as f:
        for c, n in cmd_counter.most_common():
            f.write(f'{n}\t{c}\n')
    json.dump({u: sorted(v) for u, v in urls.items()},
              open(os.path.join(WORK, 'urls.json'), 'w'), indent=1)
    json.dump({'bigrams': [[' -> '.join(k), v] for k, v in seq_bigram.most_common(100)],
               'trigrams': [[' -> '.join(k), v] for k, v in seq_trigram.most_common(100)]},
              open(os.path.join(WORK, 'sequences.json'), 'w'), indent=1)
    with open(os.path.join(WORK, 'trajectories.jsonl'), 'w') as f:
        for r in trajs:
            f.write(json.dumps(r) + '\n')
    print(json.dumps(out, indent=1))

if __name__ == '__main__':
    main()
