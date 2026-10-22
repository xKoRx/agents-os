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
  - evidence <- CANONICAL_EVIDENCE = s-originales + REVIEWER_VERIFIED_EVIDENCE
    + TARGETED_ADJUDICATED_EVIDENCE (normalizando refs f-NNNNNN.png -> f-NNNNNN,
    sin duplicados). Las clases de evidencia:
      PROPOSED_EVIDENCE             f-* propuesto por el extractor en el pool:
                                    NO entra al canónico salvo verificación
                                    (el validador V03 caza el frame sin archivo)
      REVIEWER_VERIFIED_EVIDENCE    verified_evidence del review: entra
      TARGETED_ADJUDICATED_EVIDENCE refs de <run>/evidence-adjudications.json
                                    ({"<claim_key>": {"refs": [...], "proof":
                                    "<spool/razón de la adjudicación>"}}): entran
                                    — defecto real ch10: las refs f- adjudicadas
                                    por targeted review se perdían en la fusión
      CANONICAL_EVIDENCE            resultado en claims.jsonl
  - unresolved_questions <- unión sin duplicados
  - review_reason <- results[i].reason (recortado a 1500)
  - reviewed_minute <- minuto
  - corrections_suggested se LISTAN en stdout para que el integrador las
    revise y las aplique al pool (nunca se aplican automáticamente al statement).

Seguridad de integración parcial (defecto real ch08: un run de un solo minuto
sobrescribió claims.jsonl desde el pool, perdiendo las reviews del resto). La
escritura canónica exige INTEGRACIÓN COMPLETA: los minutos aplicados deben
cubrir todos los reviews presentes en el run Y todos los claims del pool. Una
ejecución parcial es sólo --dry-run (no escribe) o escribe un resultado
PROVISIONAL separado (claims.jsonl.partial) sin tocar el canónico.

Exit 0 = integración completa aplicada (o --dry-run); 1 = algún review
inválido o integración parcial (no reemplaza el canónico).
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


def discovered_minutes(run):
    return sorted({int(m[len("review-min"):-5].lstrip("0") or "0")
                   for m in os.listdir(os.path.join(run, "reviews"))
                   if m.startswith("review-min") and m.endswith(".json")})


def load_adjudications(run, explicit=None):
    """TARGETED_ADJUDICATED_EVIDENCE: refs f- adjudicadas con prueba
    ({"<claim_key>": {"refs": [...], "proof": "..."}}). Ausente = vacío."""
    path = explicit or os.path.join(run, "evidence-adjudications.json")
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return {k: v for k, v in data.items() if isinstance(v, dict) and v.get("refs")}


def integrate(run, lib, minutes, dry=False, validate="validate_review.py",
              adjudications_file=None):
    pool_path = os.path.join(run, "claims-pool.jsonl")
    pool = {}
    with open(pool_path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rec = json.loads(line)
                pool[rec["key"]] = rec
    adjudications = load_adjudications(run, adjudications_file)
    present = discovered_minutes(run)
    partial = bool(minutes) and set(minutes) != set(present)
    applied, invalid, corrections, normalized = 0, [], [], 0
    adj_applied = 0
    applied_keys = set()
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
            applied_keys.add(res["claim_key"])
            c["verdict"] = res["verdict"]
            raw = [e for e in res.get("verified_evidence", []) if e]
            ve = [_normalize_ref(e) for e in raw]
            normalized += sum(1 for a, b in zip(raw, ve) if a != b)
            base = [e for e in c.get("evidence", []) if e.startswith("s-")]
            merged = list(base)
            for e in ve:
                if e.startswith("s-") and e in merged:
                    continue
                if e not in merged:
                    merged.append(e)
            # TARGETED_ADJUDICATED_EVIDENCE: con prueba de la adjudicación
            adj = adjudications.get(res["claim_key"], {})
            for e in adj.get("refs", []):
                e = _normalize_ref(e)
                if e and e not in merged:
                    merged.append(e)
                    adj_applied += 1
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
    print(f"aplicados: {applied} | invalid: {invalid} | refs f-.png normalizadas: {normalized} | refs targeted-adjudicadas: {adj_applied}")
    for ck, corr in corrections:
        print(f"CORRECCIÓN {ck}: {corr[:200]}")
    if invalid:
        return 1
    coverage_ok = applied_keys == set(pool)
    if not coverage_ok:
        missing = sorted(set(pool) - applied_keys)
        print(f"COBERTURA INCOMPLETA: {len(applied_keys)}/{len(pool)} claims del pool "
              f"sin review aplicado ({', '.join(missing[:8])}...) — no es canónico.")
    if dry:
        if partial or not coverage_ok:
            print("INTEGRACIÓN PARCIAL (dry-run): no escribe nada. "
                  "Re-ejecutar con la lista COMPLETA de minutos para publicar.")
            return 1
        return 0
    out = os.path.join(lib, "claims.jsonl")
    if partial or not coverage_ok:
        out = os.path.join(lib, "claims.jsonl.partial")
        print(f"INTEGRACIÓN PARCIAL: minutos {minutes} de {present}; escrito "
              f"PROVISIONAL {out} — el canónico NO se reemplaza (re-ejecutar con "
              f"la lista COMPLETA de minutos).")
    with open(out, "w", encoding="utf-8") as f:
        for key in sorted(pool):
            f.write(json.dumps(pool[key], ensure_ascii=False) + "\n")
    print(f"escrito {out} ({len(pool)} claims)")
    return 0 if not (partial or not coverage_ok) else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True, help="run dir con claims-pool.jsonl y reviews/")
    ap.add_argument("--lib", required=True, help="biblioteca del capítulo (destino claims.jsonl)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--validate", default=None, help="ruta a validate_review.py")
    ap.add_argument("--adjudications", default=None,
                    help="evidence-adjudications.json (default: <run>/evidence-adjudications.json)")
    ap.add_argument("minutes", nargs="*", type=int)
    a = ap.parse_args()
    validate = a.validate
    if not validate:
        here = os.path.dirname(os.path.abspath(__file__))
        validate = os.path.join(here, "validate_review.py")
    minutes = a.minutes if a.minutes else discovered_minutes(a.run)
    sys.exit(integrate(a.run, a.lib, minutes, dry=a.dry_run, validate=validate,
                       adjudications_file=a.adjudications))


if __name__ == "__main__":
    main()
