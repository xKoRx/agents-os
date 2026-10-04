#!/usr/bin/env python3
"""P8: extrae métricas de operación del journal durable de un run mke pipeline.

Uso: journal_audit.py <run.db> [--json out.json]
"""
import json, sqlite3, sys
from collections import Counter


def main():
    db = sys.argv[1]
    con = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
    cur = con.cursor()
    out = {}

    out['pipeline_state'] = dict(cur.execute("SELECT key, value FROM pipeline_state"))

    out['tasks'] = dict(cur.execute("SELECT task, COUNT(*) FROM provider_invocations GROUP BY task"))
    out['response_states'] = dict(cur.execute(
        "SELECT COALESCE(NULLIF(response_state,''),'(no-state)'), COUNT(*) FROM provider_invocations GROUP BY 1"))
    out['error_classes'] = dict(cur.execute(
        "SELECT COALESCE(NULLIF(error_class,''),'(none)'), COUNT(*) FROM provider_invocations GROUP BY 1"))

    fatals = []
    for iid, task, target, err, at in cur.execute(
            "SELECT invocation_id, task, target, error_detail, at_utc FROM provider_invocations WHERE error_class='fatal' ORDER BY at_utc"):
        fatals.append({'invocation_id': iid, 'task': task, 'target': target, 'error': err, 'at': at})
    out['fatals'] = fatals
    out['fatal_class_counts'] = dict(Counter(f['error'].split(']: ')[-1][:80] if f['error'] else '(unknown)' for f in fatals))

    # reconstruction dispositions per window (last invocation per target wins)
    recon = {}
    for target, state, detail in cur.execute(
            "SELECT target, response_state, substr(response_json,1,200) FROM provider_invocations "
            "WHERE task='claims.reconstruction' ORDER BY at_utc, rowid"):
        recon[target] = {'state': state, 'detail': detail}
    out['recon_windows'] = len(recon)
    out['recon_states'] = dict(Counter(v['state'] for v in recon.values()))

    # identity: equivalence reviews outcome
    eq = []
    for target, state, at in cur.execute(
            "SELECT target, response_state, at_utc FROM provider_invocations "
            "WHERE task='claims.equivalence_review' ORDER BY at_utc"):
        eq.append({'target': target, 'state': state, 'at': at})
    out['equivalence_reviews'] = len(eq)
    out['equivalence_states'] = dict(Counter(e['state'] for e in eq))
    out['equivalence_divergent'] = [e for e in eq if e['state'] == 'REJECTED']

    # budget totals
    out['budget'] = {k: dict(cur.execute(
        "SELECT state, SUM(delta) FROM budget_ledger WHERE kind=? GROUP BY state", (k,)))
        for k in ('vlm_call', 'vlm_image', 'vlm_token')}
    out['wall'] = cur.execute("SELECT MIN(at_utc), MAX(at_utc) FROM provider_invocations").fetchone()

    # retry topology: targets with >1 invocation
    out['targets_multi_invoke'] = dict(cur.execute(
        "SELECT cnt, COUNT(*) FROM (SELECT target, COUNT(*) cnt FROM provider_invocations GROUP BY target) GROUP BY 1"))

    j = json.dumps(out, ensure_ascii=False, indent=1)
    if '--json' in sys.argv:
        path = sys.argv[sys.argv.index('--json') + 1]
        open(path, 'w').write(j + '\n')
        print('written:', path)
    print(j[:3000])


if __name__ == '__main__':
    main()
