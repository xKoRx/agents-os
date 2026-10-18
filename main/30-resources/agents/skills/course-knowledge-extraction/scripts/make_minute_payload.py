#!/usr/bin/env python3
"""make_minute_payload.py — payload de revisión por minuto con contexto de frontera.

Contrato (skill course-knowledge-extraction §Boundary context, hardening v1.1):
el payload de cada minuto contiene
    segmentos del minuto  UNION  todos los segmentos citados por sus claims
para no truncar evidencia en límites arbitrarios del minuto.

Uso:
    make_minute_payload.py <transcript.md> <claims.jsonl> <minute> <out.json>

claims.jsonl: una línea por claim con "minute" (int) y "evidence" (lista de s-ids).
"""
import json, re, sys


def parse_transcript(path):
    segs = []
    for line in open(path, encoding="utf-8"):
        m = re.match(r"(s-\d{6}[a-z]?) \[(\d{2}):(\d{2}):(\d{2})-(\d{2}):(\d{2}):(\d{2})\] (.*)", line.strip())
        if m:
            st = int(m.group(2)) * 3600 + int(m.group(3)) * 60 + int(m.group(4))
            en = int(m.group(5)) * 3600 + int(m.group(6)) * 60 + int(m.group(7))
            segs.append({"id": m.group(1), "start": st, "end": en, "text": m.group(8)})
    return sorted(segs, key=lambda s: (s["start"], s["end"]))


def main():
    if len(sys.argv) != 5:
        print(__doc__)
        sys.exit(2)
    t_path, c_path, minute, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
    segs = parse_transcript(t_path)
    claims = [json.loads(l) for l in open(c_path, encoding="utf-8") if l.strip()]
    mine = [c for c in claims if c.get("minute") == minute]

    lo, hi = minute * 60, (minute + 1) * 60
    inside = [s for s in segs if s["start"] < hi and s["end"] > lo]
    if not inside:
        inside = [s for s in segs if lo - 120 <= s["start"] < hi]
    in_ids = {s["id"] for s in inside}

    cited = set()
    for c in mine:
        for e in c.get("evidence", []):
            if e.startswith("s-"):
                cited.add(e)
    boundary = cited - in_ids
    by_id = {s["id"]: s for s in segs}

    # contexto: un segmento antes y después de cada tramo incluido
    include = set(in_ids) | boundary
    for i, s in enumerate(segs):
        if s["id"] in include:
            if i > 0:
                include.add(segs[i - 1]["id"])
            if i + 1 < len(segs):
                include.add(segs[i + 1]["id"])

    lines = []
    for s in segs:
        if s["id"] not in include:
            continue
        tag = "" if s["id"] in in_ids else (" [citado-frontera]" if s["id"] in boundary else " [contexto]")
        lines.append(f"{s['id']} [{s['start']//60:02d}:{s['start']%60:02d}-{s['end']//60:02d}:{s['end']%60:02d}]{tag} {s['text']}")

    payload = {
        "minute": minute,
        "video_seconds": [lo, hi],
        "boundary_segments_included": sorted(boundary),
        "transcript": "\n".join(lines),
        "claims": sorted(mine, key=lambda c: c["id"]),
    }
    json.dump(payload, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"minute {minute}: {len(mine)} claims, {len(in_ids)} segmentos del minuto, "
          f"{len(boundary)} citados-frontera {sorted(boundary)} -> {out}")


if __name__ == "__main__":
    main()
