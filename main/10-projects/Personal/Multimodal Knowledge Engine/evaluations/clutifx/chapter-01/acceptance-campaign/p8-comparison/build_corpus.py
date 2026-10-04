#!/usr/bin/env python3
"""P8: construye el corpus source-grounded por ventana (formato P1) desde un run
terminal del pipeline (claims.jsonl + window-coverage.json) + config de ventanas
+ media-run + transcript.

Uso:
  build_corpus.py <run-out-dir> <config.json> <media-run-dir> <transcript.json> <out-dir> [coverage-json-path]

Salida: <out-dir>/wNNNN.json + <out-dir>/REJECTED-WINDOWS.json
"""
import json, os, sqlite3, sys


def main():
    run_dir, config_path, media_dir, transcript_path, out_dir = sys.argv[1:6]
    coverage_path = sys.argv[6] if len(sys.argv) > 6 else os.path.join(run_dir, 'window-coverage.json')
    os.makedirs(out_dir, exist_ok=True)

    claims_by_id, rels_by_id = {}, {}
    with open(os.path.join(run_dir, 'claims.jsonl')) as f:
        for line in f:
            o = json.loads(line)
            if o.get('record_type') == 'claim':
                claims_by_id[o['claim']['id']] = o['claim']
            elif o.get('record_type') == 'claim_relation':
                rels_by_id[o['relation']['id']] = o['relation']

    wc = json.load(open(coverage_path))
    coverage = {w['window']: w for w in wc['coverage']}

    cfg = json.load(open(config_path))

    frames_meta = {}
    con = sqlite3.connect(f'file:{os.path.join(media_dir, "run.db")}?mode=ro', uri=True)
    for eid, pts, tb_num, tb_den, rel in con.execute(
            "SELECT evidence_id, pts, time_base_num, time_base_den, rel_path FROM evidence WHERE kind='frame'"):
        frames_meta[eid] = {
            'pts_ms': int(pts * tb_num * 1000 / tb_den),
            'path': os.path.join(media_dir, rel),
        }

    segments = json.load(open(transcript_path))['segments']

    rejected = []
    for cw in cfg['windows']:
        wid = cw['window_id']
        w = coverage[wid]
        introduced = [x.split('@')[0] for x in w.get('records_introduced', [])]
        wclaims = [claims_by_id[c] for c in introduced if c in claims_by_id]
        wrels = [rels_by_id[c] for c in introduced if c in rels_by_id]
        known = set(claims_by_id) | set(rels_by_id)
        unresolved = [c for c in introduced if c not in known]
        cited = {e for c in wclaims for e in c.get('evidence_ids', [])}
        cited |= {e for r_ in wrels for e in r_.get('evidence_ids', [])}

        wframes = []
        pts_list = []
        seen = set()
        for eid in cw['evidence_ids']:
            m = frames_meta.get(eid)
            if m is None:
                continue
            pts_list.append(m['pts_ms'])
            seen.add(eid)
            wframes.append({'evidence_id': eid, 'pts_ms': m['pts_ms'],
                            'path': m['path'], 'exists': os.path.exists(m['path']),
                            'cited_by_claim': eid in cited})
        for eid in sorted(cited - seen):
            m = frames_meta.get(eid)
            if m is None:
                continue
            wframes.append({'evidence_id': eid, 'pts_ms': m['pts_ms'],
                            'path': m['path'], 'exists': os.path.exists(m['path']),
                            'cited_by_claim': True})
        start_ms = min(pts_list) if pts_list else 0
        end_ms = max(pts_list) if pts_list else 0
        segs = [s for s in segments if s['start_ms'] < end_ms and s['end_ms'] > start_ms]

        doc = {'window': wid, 'start': w['start'], 'end': w['end'],
               'start_ms': start_ms, 'end_ms': end_ms,
               'disposition': w['disposition'], 'rejection_category': w.get('rejection_category'),
               'claims': wclaims, 'relations': wrels,
               'unresolved_record_ids': unresolved,
               'transcript': segs, 'frames': wframes}
        with open(os.path.join(out_dir, f'{wid}.json'), 'w') as f:
            json.dump(doc, f, ensure_ascii=False, indent=1)
        if w['disposition'] != 'accepted':
            rejected.append({'window': wid, 'start': w['start'], 'end': w['end'],
                             'category': w.get('rejection_category')})

    with open(os.path.join(out_dir, 'REJECTED-WINDOWS.json'), 'w') as f:
        json.dump(rejected, f, ensure_ascii=False, indent=1)
    print(f'windows: {len(coverage)} · rejected: {len(rejected)} · claims: {len(claims_by_id)} · relations: {len(rels_by_id)}')
    print('written:', out_dir)


if __name__ == '__main__':
    main()
