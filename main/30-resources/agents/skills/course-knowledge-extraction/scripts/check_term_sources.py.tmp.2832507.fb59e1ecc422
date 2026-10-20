#!/usr/bin/env python3
"""check_term_sources.py — chequeo SOURCE-FIRST de normalizaciones de términos.

Contrato añadido tras la remediation ch03 (2026-10-18): una normalización de
términos especializados NO está soportada por el hecho de aparecer en el
glosario. Si el statement publica un término canónico de un grupo crítico
(p.ej. DOL vs DXY, significados distintos) y la evidencia citada NO contiene
ese término pero SÍ otro miembro del grupo, la sustitución es un MATERIAL
FINDING: el claim publicó una palabra que la fuente no dice.

Chequeo por claim (excluye los superseded, que son historia preservada):
    término publicado en statement
    → segmentos citados en evidence
    → ¿la fuente contiene el término publicado? ¿contiene otro del grupo?
    → sustitución sin respaldo = FINDING

No es una ontología: sólo grupos críticos declarados. Uso:
    check_term_sources.py <library_dir> [--groups JSON] [--json]
    (default --groups: [["DOL","DXY"]])

Exit 0 = PASS, 1 = FINDINGS, 2 = uso/IO.
"""
import argparse, json, os, re, sys

DEFAULT_GROUPS = [["DOL", "DXY"]]
WORD = lambda t: re.compile(r"\b" + re.escape(t) + r"\b")  # case-sensitive: siglas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("library")
    ap.add_argument("--groups", default=None, help="JSON: lista de grupos de términos mutuamente no sustituibles")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    lib = args.library
    groups = json.loads(args.groups) if args.groups else DEFAULT_GROUPS

    segs = {}
    for line in open(os.path.join(lib, "transcript.md"), encoding="utf-8"):
        m = re.match(r"^(s-\d{6}[a-z]?) \[[^\]]+\] (.*)$", line)
        if m:
            segs[m.group(1)] = m.group(2)

    findings = []
    n_checked = 0
    for line in open(os.path.join(lib, "claims.jsonl"), encoding="utf-8"):
        if not line.strip():
            continue
        c = json.loads(line)
        if c.get("superseded_by"):
            continue
        n_checked += 1
        statement = c.get("statement", "")
        cited_texts = [segs[e] for e in c.get("evidence", []) if e in segs]
        for group in groups:
            in_stmt = [t for t in group if WORD(t).search(statement)]
            if len(in_stmt) < 1:
                continue
            for t_pub in in_stmt:
                src_pub = any(WORD(t_pub).search(s) for s in cited_texts)
                if src_pub:
                    continue
                others = [g for g in group if g != t_pub]
                src_other = sorted({g for g in others for s in cited_texts if WORD(g).search(s)})
                if src_other:
                    findings.append({
                        "claim": c["id"], "severity": "MATERIAL",
                        "published": t_pub, "source_has": src_other,
                        "detail": f"el statement publica '{t_pub}' pero la evidencia citada dice {src_other} "
                                  f"— normalización sin respaldo en la fuente",
                    })

    if args.json:
        print(json.dumps({"pass": not findings, "checked": n_checked, "findings": findings},
                         ensure_ascii=False, indent=1))
    else:
        for f in findings:
            print(f"[{f['severity']}] {f['claim']}: {f['detail']}")
        print(f"TERM_SOURCE_CHECK = {'PASS' if not findings else 'FINDINGS'} "
              f"({n_checked} claims vivos, {len(findings)} findings)")
    sys.exit(0 if not findings else 1)


if __name__ == "__main__":
    main()
