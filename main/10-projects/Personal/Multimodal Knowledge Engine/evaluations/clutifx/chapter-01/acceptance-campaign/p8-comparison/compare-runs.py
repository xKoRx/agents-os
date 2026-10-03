#!/usr/bin/env python3
"""P8: comparación fuente-grounded old (full-live-v2 @ ef53530) vs new (rerun @ 19b44c1)."""
import json, sys, os
from collections import Counter

OLD = '/home/kor/secondbrain/main/10-projects/Personal/Multimodal Knowledge Engine/evaluations/clutifx/chapter-01/full-live-v2'
NEW = sys.argv[1] if len(sys.argv) > 1 else '/home/kor/mke/clutifx-ch01-rerun-20261003/run-rerun'
OUT = sys.argv[2] if len(sys.argv) > 2 else '/home/kor/secondbrain/main/10-projects/Personal/Multimodal Knowledge Engine/evaluations/clutifx/chapter-01/acceptance-campaign/p8-comparison'

def load_claims(path):
    claims, rels, header = {}, {}, None
    with open(path) as f:
        for l in f:
            o = json.loads(l)
            if o.get('record_type') == 'claim': claims[o['claim']['id']] = o['claim']
            elif o.get('record_type') == 'claim_relation': rels[o['relation']['id']] = o['relation']
            else: header = o
    return header, claims, rels

def pub(c): return c.get('publication','')
def norm(s): return ' '.join(s.split()).lower()

report = []
def emit(s=''): report.append(s)

oh, oc, orl = load_claims(OLD + '/claims.jsonl')
nh, nc, nrl = load_claims(NEW + '/claims.jsonl')

emit('# P8 — COMPARACIÓN EXHAUSTIVA OLD vs NEW')
emit()
emit(f"| Dimensión | OLD (ef53530) | NEW (19b44c1) |")
emit(f"|---|---|---|")
emit(f"| claims canónicos | {len(oc)} | {len(nc)} |")
emit(f"| relations canónicas | {len(orl)} | {len(nrl)} |")
emit(f"| supported claims | {sum(1 for c in oc.values() if pub(c).startswith('SUPPORTED'))} | {sum(1 for c in nc.values() if pub(c).startswith('SUPPORTED'))} |")
emit(f"| non-supported claims | {sum(1 for c in oc.values() if pub(c).startswith('UNSUPPORTED'))} | {sum(1 for c in nc.values() if pub(c).startswith('UNSUPPORTED'))} |")
emit(f"| supported relations | {sum(1 for c in orl.values() if pub(c).startswith('SUPPORTED'))} | {sum(1 for c in nrl.values() if pub(c).startswith('SUPPORTED'))} |")
emit(f"| non-supported relations | {sum(1 for c in orl.values() if pub(c).startswith('UNSUPPORTED'))} | {sum(1 for c in nrl.values() if pub(c).startswith('UNSUPPORTED'))} |")
emit()

# statement-level containment: how many OLD statements survive in NEW
old_stmts = {norm(c['statement']): cid for cid, c in oc.items()}
new_stmts = {norm(c['statement']): cid for cid, c in nc.items()}
kept = set(old_stmts) & set(new_stmts)
emit(f"## Contenido")
emit(f"- statements norm-iguales OLD∩NEW: **{len(kept)}** de {len(old_stmts)} old / {len(new_stmts)} new")
emit(f"- sólo en OLD: {len(set(old_stmts)-set(new_stmts))} · sólo en NEW: {len(set(new_stmts)-set(old_stmts))}")
emit()

# window disposition diff
owc = json.load(open(OLD + '/window-coverage.json'))['coverage']
nwc_path = NEW + '/window-coverage.json'
if os.path.exists(nwc_path):
    nwc = json.load(open(nwc_path))['coverage']
    odisp = {w['window']: w['disposition'] for w in owc}
    ndisp = {w['window']: w['disposition'] for w in nwc}
    flips = [(w, odisp[w], ndisp[w]) for w in odisp if odisp[w] != ndisp.get(w)]
    emit(f"## Ventanas")
    emit(f"- OLD: {Counter(odisp.values())}")
    emit(f"- NEW: {Counter(ndisp.values())}")
    emit(f"- flips de disposición: {len(flips)}")
    for w, a, b in flips: emit(f"  - {w}: {a} → {b}")
    emit()

# SKOs
for tag, root in (('OLD', OLD), ('NEW', NEW)):
    p = root + '/skos.jsonl'
    n = sum(1 for l in open(p) if l.strip()) if os.path.exists(p) else -1
    emit(f"- SKOs {tag}: {n}")
emit()

# grounding outcome distribution
def gdist(cs):
    c = Counter()
    for x in cs.values(): c[pub(x)] += 1
    return dict(c)
emit('## Grounding')
emit(f"- OLD claims: {gdist(oc)}")
emit(f"- NEW claims: {gdist(nc)}")
emit(f"- OLD relations: {gdist(orl)}")
emit(f"- NEW relations: {gdist(nrl)}")
emit()

open(OUT + '/P8-COMPARE.md', 'w').write('\n'.join(report) + '\n')
print('\n'.join(report[:40]))
print('...')
print('written:', OUT + '/P8-COMPARE.md')
