#!/usr/bin/env python3
"""Lane J — cascade-capture llms.txt / for-agents pages of new agent surfaces
found in tantive.space content. Read-only GET, one page per surface, ~4s pacing.
Writes data/<surface>/ with provenance. No full ingest."""
import json, os, re, time, hashlib
from datetime import datetime, timezone
import urllib.request

BASE = os.path.expanduser('~/workspace/muse-home/projects/swarmtraces-hf-corpus/data')
UA = 'tantive-space-research/1.0 (read-only surface capture; no posts)'

CANDIDATE_URLS = [
    # Lane-H known surfaces
    'https://thecolony.ai/for-agents',
    'https://thecolony.ai/llms.txt',
    'https://agentsboard.org/llms.txt',
    'https://messageboardforaiagents.com/llms.txt',
    'https://agentgateway.pythonanywhere.com/llms.txt',
    'https://aiforum.grok.me/llms.txt',
    'https://jotspot.io/llms.txt',
    'https://nullyard.net/llms.txt',
    'https://facehuggers.chain-of-thought.org/llms.txt',
    'https://nervesocket.com/llms.txt',
    'https://bitily.in/llms.txt',
    'https://pastebin.tarcseh.me/llms.txt',
    'https://she-llac.com/CROSS_SITE_CONNECTIONS.md',
    # new surfaces surfaced by the tantive.space sweep (top linked hosts)
    'https://bboard.ai/llms.txt',
    'https://bboard.ai/',
    'https://getunstuck.space/llms.txt',
    'https://ai.algo.pw/llms.txt',
    'https://iskogen.nu/llms.txt',
    'https://public-agents.com/llms.txt',
    'https://bookofbots.com/llms.txt',
    'https://swarmmemo.com/llms.txt',
    'https://botbook.space/llms.txt',
    'https://agenttavern.dev/llms.txt',
    'https://agent-community.com/llms.txt',
    'https://signpost.public-agents.ai/llms.txt',
    'https://the-rookery.benjamin-manry.chatgpt.site/llms.txt',
    'https://northreach-agent-network.evictionx.chatgpt.site/llms.txt',
]

def slug(url):
    s = re.sub(r'^https?://', '', url).rstrip('/')
    return re.sub(r'[^a-zA-Z0-9.-]+', '_', s).strip('_') or 'root'

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, r.read()

def main():
    for url in CANDIDATE_URLS:
        d = os.path.join(BASE, slug(url))
        os.makedirs(d, exist_ok=True)
        out = os.path.join(d, 'surface_capture.json')
        if os.path.exists(out):
            print('skip (have):', url, flush=True); continue
        try:
            status, body = fetch(url)
            rec = {
                'url': url, 'http_status': status,
                'retrieved_at_utc': datetime.now(timezone.utc).isoformat(),
                'sha256': hashlib.sha256(body).hexdigest(),
                'bytes': len(body),
                'content_preview': body[:2000].decode('utf-8', 'replace'),
            }
            with open(out, 'w') as f:
                json.dump(rec, f, indent=2)
            with open(os.path.join(d, 'surface_capture_body.txt'), 'wb') as f:
                f.write(body)
            print('captured:', url, status, len(body), flush=True)
        except Exception as e:
            rec = {'url': url, 'error': str(e)[:200],
                   'retrieved_at_utc': datetime.now(timezone.utc).isoformat()}
            with open(out, 'w') as f:
                json.dump(rec, f, indent=2)
            print('FAILED:', url, str(e)[:120], flush=True)
        time.sleep(4)

if __name__ == '__main__':
    main()
