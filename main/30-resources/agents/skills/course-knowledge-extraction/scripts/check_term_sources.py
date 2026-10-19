#!/usr/bin/env python3
"""check_term_sources.py — chequeo SOURCE-FIRST de normalizaciones de términos.

Contrato añadido tras la remediation ch03 (2026-10-18): una normalización de
términos especializados NO está soportada por el hecho de aparecer en el
glosario. Si el statement publica un término canónico de un grupo crítico
(p.ej. DOL vs DXY, significados distintos) y la evidencia citada NO contiene
ese término pero SÍ otro miembro del grupo, la sustitución es un MATERIAL
FINDING: el claim publicó una palabra que la fuente no dice.

Extensión hardening ch04 (2026-10-19) — desambiguación de garbles:
  1. El lado FUENTE se compara case-insensitive: un ASR "dol" minúscula
     cuenta como el canónico DOL (c-0089 de ch02: fuente "tu dol", claim
     "tu DXY" → MATERIAL, el caso real de Chapter 02).
  2. TERM_DISAMBIGUATION_REQUIRED (severity REVIEW): la fuente contiene una
     EXPRESIÓN AMBIGUA del grupo (p.ej. "el doble", "doll", "dole" — garbles
     que no son canónicos de ningún miembro) y el statement publica un
     canónico SIN la marca de adjudicación "[ASR" del protocolo v1.2. El
     chequeo determinista detecta la NECESIDAD de revisión; NO decide cuál
     término es correcto — eso lo adjudica el reviewer SOURCE-FIRST con
     transcript, audio puntual, contexto y frames.

Chequeo por claim (excluye los superseded, que son historia preservada):
    término publicado en statement
    → segmentos citados en evidence
    → ¿la fuente contiene el término publicado? ¿contiene otro del grupo
      (case-insensitive)? ¿contiene un garble ambiguo sin adjudicación?

No es una ontología: sólo grupos críticos declarados. Uso:
    check_term_sources.py <library_dir> [--groups JSON] [--json]
    --groups acepta [["DOL","DXY"]] (legacy, sin aliases) o
    [{"term":"DOL","aliases":["el doble","doll","dole"]}, ...]
    (default: DOL con aliases ["el doble","doble","doll","dole","dolls"], DXY)

Exit 0 = PASS, 1 = FINDINGS (MATERIAL o REVIEW), 2 = uso/IO.
"""
import argparse, json, os, re, sys

DEFAULT_GROUPS = [
    {"term": "DOL", "aliases": ["el doble", "doble", "doll", "dole", "dolls"]},
    {"term": "DXY", "aliases": []},
]
WORD = lambda t: re.compile(r"\b" + re.escape(t) + r"\b")          # case-sensitive: siglas
WORD_I = lambda t: re.compile(r"\b" + re.escape(t) + r"\b", re.I)  # fuente: el ASR no capitaliza


def normalize_groups(raw):
    """Acepta [["DOL","DXY"]] y [{"term":..,"aliases":[..]}]; devuelve dicts."""
    out = []
    for g in raw:
        if isinstance(g, str):
            out.append({"term": g, "aliases": []})
        elif isinstance(g, list):
            out.extend({"term": t, "aliases": []} for t in g)
        elif isinstance(g, dict) and g.get("term"):
            out.append({"term": g["term"], "aliases": list(g.get("aliases", []))})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("library")
    ap.add_argument("--groups", default=None, help="JSON: grupos de términos mutuamente no sustituibles (con aliases opcionales)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    lib = args.library
    groups = normalize_groups(json.loads(args.groups)) if args.groups else DEFAULT_GROUPS

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
            terms = [group["term"]] + [g["term"] for g in groups if g is not group]
            in_stmt = [t for t in [group["term"]] if WORD(t).search(statement)]
            if len(in_stmt) < 1:
                continue
            for t_pub in in_stmt:
                src_pub = any(WORD_I(t_pub).search(s) for s in cited_texts)
                if src_pub:
                    continue
                siblings = [t for t in terms if t != t_pub]
                src_other = sorted({g for g in siblings for s in cited_texts if WORD_I(g).search(s)})
                if src_other:
                    findings.append({
                        "claim": c["id"], "severity": "MATERIAL",
                        "published": t_pub, "source_has": src_other,
                        "detail": f"el statement publica '{t_pub}' pero la evidencia citada dice {src_other} "
                                  f"— normalización sin respaldo en la fuente",
                    })
                    continue
                # sin canónico en fuente: ¿garble ambiguo del grupo sin adjudicación?
                aliases_hit = sorted({a for a in group.get("aliases", [])
                                      for s in cited_texts if WORD_I(a).search(s)})
                if aliases_hit and "[ASR" not in statement:
                    findings.append({
                        "claim": c["id"], "severity": "REVIEW",
                        "type": "TERM_DISAMBIGUATION_REQUIRED",
                        "published": t_pub, "source_has": aliases_hit,
                        "detail": f"el statement publica '{t_pub}' y la evidencia citada sólo contiene "
                                  f"la expresión ambigua {aliases_hit} sin marca de adjudicación "
                                  f"[ASR] — revisar transcript/audio/frames y registrar el término dicho",
                    })

    if args.json:
        n_mat = sum(1 for f in findings if f["severity"] == "MATERIAL")
        n_rev = sum(1 for f in findings if f["severity"] == "REVIEW")
        print(json.dumps({"pass": not findings, "checked": n_checked,
                          "material": n_mat, "disambiguation_required": n_rev,
                          "findings": findings}, ensure_ascii=False, indent=1))
    else:
        for f in findings:
            tag = f.get("type", f["severity"])
            print(f"[{f['severity']}] {f['claim']} ({tag}): {f['detail']}")
        n_mat = sum(1 for f in findings if f["severity"] == "MATERIAL")
        n_rev = sum(1 for f in findings if f["severity"] == "REVIEW")
        print(f"TERM_SOURCE_CHECK = {'PASS' if not findings else 'FINDINGS'} "
              f"({n_checked} claims vivos, {n_mat} MATERIAL, {n_rev} TERM_DISAMBIGUATION_REQUIRED)")
    sys.exit(0 if not findings else 1)


if __name__ == "__main__":
    main()
