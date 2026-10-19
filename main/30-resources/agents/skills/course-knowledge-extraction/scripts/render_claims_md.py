#!/usr/bin/env python3
"""render_claims_md.py — proyección Markdown navegable de claims.jsonl.

CLAIMS.md NO es una segunda fuente de verdad: se genera desde claims.jsonl y se
regenera con el mismo comando. Bytes estables ante inputs idénticos; conserva
los IDs; no reescribe conocimiento semántico.

Uso:  render_claims_md.py <vault_root> <library_dir>
"""
import json, os, re, sys

V = "{}"


def parse_transcript(path):
    segs = {}
    for line in open(path, encoding="utf-8"):
        m = re.match(r"(s-\d{6}[a-z]?) \[(\d{2}):(\d{2}):(\d{2})-(\d{2}):(\d{2}):(\d{2})\]", line)
        if m:
            st = int(m.group(2)) * 3600 + int(m.group(3)) * 60 + int(m.group(4))
            en = int(m.group(5)) * 3600 + int(m.group(6)) * 60 + int(m.group(7))
            segs[m.group(1)] = (st, en)
    return segs


def mmss(sec):
    return f"{sec // 60:02d}:{sec % 60:02d}"


def main():
    vault, lib = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    rel = os.path.relpath(lib, vault)
    claims = sorted((json.loads(l) for l in open(os.path.join(lib, "claims.jsonl"), encoding="utf-8") if l.strip()),
                    key=lambda c: c["id"])
    segs = parse_transcript(os.path.join(lib, "transcript.md"))

    L = []
    L.append("# CLAIMS — proyección navegable")
    L.append("")
    L.append(f"> Generado deterministamente desde `claims.jsonl` por"
             f" `render_claims_md.py` (sin fecha dinámica: misma entrada => mismos bytes)."
             f" NO es una segunda fuente de verdad: para scripts y agentes la autoridad es el JSONL.")
    L.append("> Navegación: cada claim enlaza sus segmentos de transcript (anchors `^s-`) y sus frames.")
    L.append("")
    for c in claims:
        cid = c["id"]
        srefs = [e for e in c["evidence"] if e.startswith("s-")]
        frefs = [e for e in c["evidence"] if e.startswith("f-")]
        times = [segs[s] for s in srefs if s in segs]
        t0, t1 = (min(a for a, _ in times), max(b for _, b in times)) if times else (None, None)
        L.append(f"### {cid}")
        L.append("")
        # Lifecycle: un claim con superseded_by es historia preservada, no
        # conocimiento vigente. La marca va PRIMERO, antes del statement, y el
        # reemplazo es siempre navegable. (superseded_by => SUPERSEDED; no hay
        # campo de lifecycle redundante.)
        if c.get("superseded_by"):
            sup = c["superseded_by"]
            L.append("**SUPERSEDED — HISTORICAL, NOT ACTIVE**")
            L.append("")
            L.append(f"**Replacement:** [[{V.format(rel)}/CLAIMS#{sup}|{sup}]]")
            L.append("")
        if c.get("supersedes"):
            prev = c["supersedes"]
            L.append(f"**Supersedes:** [[{V.format(rel)}/CLAIMS#{prev}|{prev}]]"
                     f" (versión histórica preservada)")
            L.append("")
        L.append(f"**Statement:** {c['statement']}")
        L.append("")
        L.append(f"**Verdict:** {c['verdict']} · **Epistemic:** {c.get('epistemic','')} ·"
                 f" **Kind:** {c.get('kind','')} · **Minute:** {c.get('minute','')}"
                 f" · **Source key:** {c.get('source_key','')}")
        L.append("")
        if t0 is not None:
            L.append(f"**Tiempo:** [{mmss(t0)}–{mmss(t1)}]")
            L.append("")
        if srefs:
            links = " · ".join(f"[[{V.format(rel)}/transcript#^{s}|{mmss(segs[s][0]) if s in segs else s}]]" for s in srefs)
            L.append(f"**Transcript:** {links}")
            L.append("")
        if frefs:
            links = " · ".join(f"[[{V.format(rel)}/frames/{f}.png|{f}]]" for f in frefs)
            L.append(f"**Frames:** {links}")
            L.append("")
        if c.get("visual_hint"):
            vh = c["visual_hint"]
            sec = vh.get("second", "")
            mm, ss = int(sec) // 60, int(sec) % 60
            L.append(f"**Visual hint:** {mm:02d}:{ss:02d} — {vh.get('what','')}")
            L.append("")
        if c.get("notes"):
            L.append(f"**Notes:** {c['notes']}")
            L.append("")
    out = os.path.join(lib, "CLAIMS.md")
    open(out, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"CLAIMS.md: {len(claims)} claims -> {out}")


if __name__ == "__main__":
    main()
