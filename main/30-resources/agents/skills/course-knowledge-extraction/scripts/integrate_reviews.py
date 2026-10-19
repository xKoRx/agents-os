#!/usr/bin/env python3
"""integrate_reviews.py — aplica reviews válidos al pool y escribe claims.jsonl canónico.

Generalizado del run ch04 (2026-10-19): las rutas de run y biblioteca son
argumentos, no constantes. Sólo el integrador toca archivos canónicos. Cada
review debe pasar validate_review.py (cardinalidad R01-R04) antes de aplicarse.
Con --dry-run no escribe.

Uso:
    integrate_reviews.py --run <run_dir> --lib <lib_dir> [--dry-run] [minutos...]

Efectos por review válido (results[i] sobre claims-pool.jsonl[claim_key]):
  - verdict <- results[i].verdict
  - evidence <- s-originales + verified_evidence (normalizando refs f-NNNNNN.png -> f-NNNNNN)
  - unresolved_questions <- unión sin duplicados
  - review_reason <- results[i].reason (recortado a 1500)
  - reviewed_minute <- minuto
  - corrections_suggested se LISTAN en stdout para que el integrador las
    revise y las aplique al pool (nunca se aplican automáticamente al statement).

Exit 0 = aplicado (o --dry-run limpio); 1 = algún review inválido (no escribe).
"""
import argparse
import json
import os
import re
import subprocess
import sys

_F_PNG = re.compile(r"^(f-\d{6})\.png$")


def _normalize_ref(e):
    """Los reviewers a veces citan f-XXXXXX.png (con sufijo); el canónico es
    f-XXXXXX (defecto real ch04: 6 evidencias con sufijo)."""
    m = _F_PNG.match(e)
    return m.group(1) if m else e


def integrate(run, lib, minutes, dry=False, validate="validate_review.py"):
    pool_path = os.path.join(run, "claims-pool.jsonl")
    pool = {}
    with open(pool_path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rec = json.loads(line)
                pool[rec["key"]] = rec
    applied, invalid, corrections, normalized = 0, [], [], 0
    for m in minutes:
        rp = os.path.join(run, "reviews", f"review-min{m}.json")
        pp = os.path.join(run, "reviews", f"payload-min{m}.json")
        if not os.path.exists(rp):
            invalid.append((m, "falta review"))
            continue
        r = subprocess.run([sys.executable, validate, pp, rp],
                           capture_output=True, text=True)
        if r.returncode != 0:
            invalid.append((m, (r.stdout + r.stderr).strip()[:200]))
            continue
        rev = json.load(open(rp, encoding="utf-8"))
        for res in rev["results"]:
            c = pool[res["claim_key"]]
            c["verdict"] = res["verdict"]
            ve = [_normalize_ref(e) for e in res.get("verified_evidence", []) if e]
            base = [e for e in c.get("evidence", []) if e.startswith("s-")]
            merged = list(base)
            for e in ve:
                if e.startswith("s-") and e in merged:
                    continue
                if e not in merged:
                    if _F_PNG.match(e):
                        normalized += 1
                    merged.append(e)
            c["evidence"] = merged
            if res.get("corrections_suggested"):
                corrections.append((res["claim_key"], res["corrections_suggested"]))
            rq = res.get("unresolved_questions") or []
            if rq:
                seen = set(c.get("unresolved_questions") or [])
                c["unresolved_questions"] = sorted(seen | set(rq))
            reason = (res.get("reason") or "").strip()
            if reason:
                c["review_reason"] = reason[:1500]
            c["reviewed_minute"] = m
            applied += 1
    print(f"aplicados: {applied} | invalid: {invalid} | refs f-.png normalizadas: {normalized}")
    for ck, corr in corrections:
        print(f"CORRECCIÓN {ck}: {corr[:200]}")
    if invalid:
        return 1
    if not dry:
        out = os.path.join(lib, "claims.jsonl")
        with open(out, "w", encoding="utf-8") as f:
            for key in sorted(pool):
                f.write(json.dumps(pool[key], ensure_ascii=False) + "\n")
        print(f"escrito {out} ({len(pool)} claims)")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True, help="run dir con claims-pool.jsonl y reviews/")
    ap.add_argument("--lib", required=True, help="biblioteca del capítulo (destino claims.jsonl)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--validate", default=None, help="ruta a validate_review.py")
    ap.add_argument("minutes", nargs="*", type=int)
    a = ap.parse_args()
    validate = a.validate
    if not validate:
        here = os.path.dirname(os.path.abspath(__file__))
        validate = os.path.join(here, "validate_review.py")
    minutes = a.minutes
    if not minutes:
        minutes = sorted({int(m[7:-5].lstrip("0") or "0")
                          for m in os.listdir(os.path.join(a.run, "reviews"))
                          if m.startswith("review-min") and m.endswith(".json")})
    sys.exit(integrate(a.run, a.lib, minutes, dry=a.dry_run, validate=validate))


if __name__ == "__main__":
    main()
