#!/usr/bin/env python3
"""P8: construye el corpus source-grounded por ventana (formato P1) desde un run
terminal del pipeline (claims.jsonl + window-coverage.json) + media-run.

Uso:
  build_corpus.py <run-out-dir> <media-run-dir> <transcript.json> <out-dir>

Salida: <out-dir>/wNNNN.json + <out-dir>/REJECTED-WINDOWS.json
"""
import json, os, sqlite3, sys

def main():
    run_dir, media_dir, transcript_path, out_dir = sys.argv[1:5]
    os.makedirs(out_dir, exist_ok=True)

    claims_by_id = {}
    rels_by_id = {}
    with open(os.path.join(run_dir, 'claims.jsonl')) as f:
        for line in f:
            o = json.loads(line)
            if o.get('record_type') == 'claim':
                claims_by_id[o['claim']['id']] = o['claim']
            elif o.get('record_type') == 'claim_relation':
                rels_by_id[o['relation']['id']] = o['relation']

    wc = json.load(open(os.path.join(run_dir, 'window-coverage.json')))
    coverage = wc['coverage']

    # media-run evidence: canonical frames
    frames = []
    con = sqlite3.connect(f'file:{os.path.join(media_dir, "run.db")}?mode=ro', uri=True)
    for r in con.execute(
        "SELECT evidence_id, pts, time_base_num, time_base_den, rel_path FROM evidence "
        "WHERE kind='frame' AND extraction_profile='canonical-v1' ORDER BY pts"):
        eid, pts, tb_num, tb_den, rel = r
        frames.append({
            'evidence_id': eid,
            'pts_ms': int(pts * tb_num * 1000 / tb_den),
            'path': os.path.join(media_dir, rel),
        })

    t = json.load(open(transcript_path))
    segments = t['segments']

    rejected = []
    for w in coverage:
        wid = w['window']
        start_ms, end_ms = w['start_ms'], w['end_ms']
        introduced = [x.split('@')[0] for x in w.get('records_introduced', [])]
        wclaims = [claims_by_id[c] for c in introduced if c in claims_by_id]
        wrels = [rels_by_id[c] for c in introduced if c in rels_by_id]
        cited = {e for c in wclaims for e in c.get('evidence_ids', [])}
        cited |= {e for r_ in wrels for e in r_.get('evidence_ids', [])}
        segs = [s for s in segments if s['start_ms'] < end_ms and s['end_ms'] > start_ms]
        wframes = []
        for fr in frames:
            if start_ms <= fr['pts_ms'] <= end_ms:
                wframes.append({
                    'evidence_id': fr['evidence_id'],
                    'pts_ms': fr['pts_ms'],
                    'path': fr['path'],
                    'exists': os.path.exists(fr['path']),
                    'cited_by_claim': fr['evidence_id'] in cited,
                })
        unresolved = w.get('unresolved_record_ids') or []
        doc = {
            'window': wid,
            'start': w['start'],
            'end': w['end'],
            'start_ms': start_ms,
            'end_ms': end_ms,
            'disposition': w['disposition'],
            'rejection_category': w.get('rejection_category'),
            'claims': wclaims,
            'relations': wrels,
            'unresolved_record_ids': unresolved,
            'transcript': segs,
            'frames': wframes,
        }
        with open(os.path.join(out_dir, f'{wid}.json'), 'w') as f:
            json.dump(doc, f, ensure_ascii=False, indent=1)
        if w['disposition'] != 'accepted':
            rejected.append({
                'window': wid,
                'start': w['start'],
                'end': w['end'],
                'category': w.get('rejection_category'),
            })
    with open(os.path.join(out_dir, 'REJECTED-WINDOWS.json'), 'w') as f:
        json.dump(rejected, f, ensure_ascii=False, indent=1)
    print(f'windows: {len(coverage)} · rejected: {len(rejected)} · claims: {len(claims_by_id)} · relations: {len(rels_by_id)}')
    print('written:', out_dir)

if __name__ == '__main__':
    main()
