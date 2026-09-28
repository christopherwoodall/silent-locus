#!/usr/bin/env python3
"""Lane J — pattern battery over tantive.space messages/threads.
Standard campaign-toolkit sweep + task-family + cross-corpus refs.
Writes data/tantive-space/sweep.json."""
import json, re, os
from collections import Counter

D = os.path.expanduser('~/workspace/muse-home/projects/swarmtraces-hf-corpus/data/tantive-space')

BATTERY = {
    # campaign grammars
    'grammar:zz': re.compile(r'\bzz[a-z0-9]{2,}\b', re.I),
    'grammar:oai': re.compile(r'\boai[a-z0-9]{3,}\b', re.I),
    'grammar:tryzz': re.compile(r'\btry[a-z][0-9]zz\b', re.I),
    'epoch_nonce': re.compile(r'\b1[0-9]{9}\b'),
    # mechanisms
    'mech:go-import': re.compile(r'go-import', re.I),
    'mech:webhook': re.compile(r'web_hooks|webhook\.site|oast\.online', re.I),
    'mech:xss-ssti': re.compile(r'<script|onerror=|\$\{7\*7\}|\{\{7\*7\}\}', re.I),
    # proxy wrappers / laundering
    'proxy:jina': re.compile(r'[rs]\.jina\.ai', re.I),
    'proxy:mdsucc': re.compile(r'md\.succ\.ai', re.I),
    'proxy:jqp': re.compile(r'jqp\.vercel\.app', re.I),
    'proxy:jsonhero': re.compile(r'jsonhero\.io', re.I),
    'proxy:allorigins': re.compile(r'allorigins', re.I),
    'proxy:markdown-new': re.compile(r'markdown\.new', re.I),
    'proxy:corsworkers': re.compile(r'cors.*workers\.dev|workers\.dev', re.I),
    'proxy:proxymule': re.compile(r'proxymule', re.I),
    # shorteners
    'short:rmnre': re.compile(r'rmn\.re', re.I),
    'short:dagd': re.compile(r'da\.gd', re.I),
    'short:isgd': re.compile(r'is\.gd', re.I),
    'short:ittybitty': re.compile(r'itty\.bitty\.site', re.I),
    # cross-corpus references
    'ref:collusion-wiki': re.compile(r'collusion\.wiki', re.I),
    'ref:swarm-research': re.compile(r'swarm-ai-research|WikiAgentSwarmInvestigation', re.I),
    'ref:dse': re.compile(r'\bdse\b', re.I),
    'ref:brausepulver': re.compile(r'brausepulver', re.I),
    'ref:thecolony': re.compile(r'thecolony\.ai', re.I),
    'ref:public-board': re.compile(r'public-board\.com', re.I),
    'ref:agentgateway': re.compile(r'agentgateway', re.I),
    # task families
    'topic:fips': re.compile(r'\bfips\b', re.I),
    'topic:secgov': re.compile(r'sec\.gov|county\.json|dummyagent', re.I),
    'topic:census': re.compile(r'\bcensus\b', re.I),
    'topic:aihw': re.compile(r'aihw|tableau', re.I),
    'topic:health': re.compile(r'medicare|medicines', re.I),
    # other agent surfaces (cascade candidates)
    'surf:tantive': re.compile(r'tantive\.space', re.I),
    'surf:agentsboard': re.compile(r'agentsboard\.org', re.I),
    'surf:messageboardforai': re.compile(r'messageboardforaiagents\.com', re.I),
    'surf:aiforum-grok': re.compile(r'aiforum\.grok\.me', re.I),
    'surf:jotspot': re.compile(r'jotspot\.io', re.I),
    'surf:nullyard': re.compile(r'nullyard\.net', re.I),
    'surf:facehuggers': re.compile(r'facehuggers\.chain-of-thought\.org', re.I),
    'surf:nervesocket': re.compile(r'nervesocket\.com', re.I),
    'surf:bitily': re.compile(r'bitily\.in', re.I),
    'surf:pastebin-tarcseh': re.compile(r'pastebin\.tarcseh\.me', re.I),
    'surf:she-llac': re.compile(r'she-llac\.com', re.I),
}

def main():
    msgs = []
    for name in ('messages.jsonl', 'threads.jsonl'):
        p = os.path.join(D, name)
        if os.path.exists(p):
            with open(p) as f:
                for line in f:
                    line = line.strip()
                    if line:
                        msgs.append((name, json.loads(line)))
    counts = Counter()
    hits = {k: [] for k in BATTERY}
    urls = Counter()
    authors = Counter()
    rooms = Counter()
    for src, m in msgs:
        body = (m.get('body') or '') + ' ' + (m.get('title') or '')
        for k, rx in BATTERY.items():
            if rx.search(body):
                counts[k] += 1
                if len(hits[k]) < 25:
                    hits[k].append({'src': src, 'id': m.get('id'),
                                    'author': m.get('author'),
                                    'created_at': m.get('created_at'),
                                    'snippet': body[:400].replace('\n', ' ')})
        for u in re.findall(r'https?://([a-zA-Z0-9.-]+)', body):
            urls[u.lower()] += 1
        if m.get('author'):
            authors[m['author']] += 1
        if m.get('room'):
            rooms[m['room']] += 1
    out = {
        'n_records': len(msgs),
        'pattern_counts': dict(counts),
        'hits': hits,
        'top_url_hosts': urls.most_common(60),
        'top_authors': authors.most_common(40),
        'rooms': dict(rooms),
    }
    with open(os.path.join(D, 'sweep.json'), 'w') as f:
        json.dump(out, f, indent=2)
    print(json.dumps({k: v for k, v in out.items() if k in ('n_records', 'pattern_counts', 'rooms')}, indent=2))
    print('top hosts:', urls.most_common(20))

if __name__ == '__main__':
    main()
