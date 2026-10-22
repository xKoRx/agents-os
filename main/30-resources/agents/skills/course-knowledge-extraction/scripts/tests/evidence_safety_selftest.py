#!/usr/bin/env python3
"""evidence_safety_selftest.py — red-green del contrato de evidencia visual del
integrador (defecto real ch10: integrate_reviews.py dropeaba refs f- adjudicadas
por targeted review tras la integración; METHODOLOGY-FEEDBACK CH10 LEARNED #4).

Clases de evidencia (contrato vigente):
  PROPOSED_EVIDENCE            f-* propuesto por el extractor en el pool
  REVIEWER_VERIFIED_EVIDENCE   f-*/s-* en verified_evidence del review
  TARGETED_ADJUDICATED_EVIDENCE refs adjudicadas con prueba en
                               <run>/evidence-adjudications.json
  CANONICAL_EVIDENCE           resultado en claims.jsonl

Sólo las verificadas (reviewer o targeted-adjudicadas con prueba) entran al
canónico. Las propuestas no verificadas se excluyen (documentado, no silencio).

Casos:
  1  frame verificado por el reviewer: se conserva
  2  frame propuesto por el extractor y NO verificado: se excluye
  3  frame posteriormente adjudicado (evidence-adjudications.json con proof):
     se conserva aunque el reviewer no lo haya listado
  4  reintegración completa: no pierde evidencia válida ni duplica refs
     (adjudicada = verificada -> aparece una sola vez)
  5  integración parcial: jamás sobrescribe el canónico (con adjudications presente)

Uso:  python3 evidence_safety_selftest.py
"""
import json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
INTEGRATE = os.path.join(HERE, "..", "integrate_reviews.py")
VALIDATE = os.path.join(HERE, "..", "validate_review.py")

TRANSCRIPT = "s-000010 [00:00:10-00:00:20] texto uno\n"
# k1 propone DOS frames: f-000111 (el reviewer lo verifica) y f-000222 (no lo verifica)
CLAIMS = [
    {"key": "k1", "id": "c-0001", "minute": 0, "statement": "x",
     "evidence": ["s-000010", "f-000111", "f-000222"]},
]
REVIEWS = {
    0: {"minute": 0, "results": [
        {"claim_key": "k1", "verdict": "SUPPORTED",
         "verified_evidence": ["s-000010", "f-000111"],
         "reason": "ok", "unresolved_questions": []},
    ]},
}


def build_run(root):
    run = os.path.join(root, "run")
    lib = os.path.join(root, "lib")
    os.makedirs(os.path.join(run, "reviews"))
    os.makedirs(lib)
    with open(os.path.join(run, "claims-pool.jsonl"), "w", encoding="utf-8") as f:
        for c in CLAIMS:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    pp = os.path.join(run, "reviews", "payload-min0.json")
    rp = os.path.join(run, "reviews", "review-min0.json")
    json.dump({"minute": 0, "transcript": TRANSCRIPT, "claims": CLAIMS},
              open(pp, "w", encoding="utf-8"))
    json.dump(REVIEWS[0], open(rp, "w", encoding="utf-8"))
    return run, lib


def run_integrate(run, lib):
    return subprocess.run([sys.executable, INTEGRATE, "--run", run, "--lib", lib,
                           "--validate", VALIDATE, "0"],
                          capture_output=True, text=True)


def main():
    fails = []

    # Casos 1+2: verificado se conserva; propuesto-no-verificado se excluye
    with tempfile.TemporaryDirectory() as root:
        run, lib = build_run(root)
        r = run_integrate(run, lib)
        if r.returncode != 0:
            fails.append(f"caso1/2: exit {r.returncode}: {r.stdout}{r.stderr}")
        else:
            c1 = [json.loads(l) for l in open(os.path.join(lib, "claims.jsonl"), encoding="utf-8")][0]
            ev = c1["evidence"]
            if "f-000111" not in ev:
                fails.append(f"caso1: frame verificado por reviewer perdido: {ev}")
            if "f-000222" in ev:
                fails.append(f"caso2: frame propuesto NO verificado entró al canónico: {ev}")

    # Caso 3: adjudicación targeted con prueba conserva el frame
    with tempfile.TemporaryDirectory() as root:
        run, lib = build_run(root)
        adj = {"k1": {"refs": ["f-000222"],
                      "proof": "workers/spool-targeted/review.json (verificación visual targeted)"}}
        json.dump(adj, open(os.path.join(run, "evidence-adjudications.json"), "w",
                            encoding="utf-8"))
        r = run_integrate(run, lib)
        if r.returncode != 0:
            fails.append(f"caso3: exit {r.returncode}: {r.stdout}{r.stderr}")
        else:
            c1 = [json.loads(l) for l in open(os.path.join(lib, "claims.jsonl"), encoding="utf-8")][0]
            if "f-000222" not in c1["evidence"]:
                fails.append(f"caso3: frame targeted-adjudicado perdido: {c1['evidence']}")

    # Caso 4: reintegración completa no duplica refs ni pierde evidencia
    with tempfile.TemporaryDirectory() as root:
        run, lib = build_run(root)
        adj = {"k1": {"refs": ["f-000111.png", "f-000222"], "proof": "spool"}}
        json.dump(adj, open(os.path.join(run, "evidence-adjudications.json"), "w",
                            encoding="utf-8"))
        r = run_integrate(run, lib)
        if r.returncode != 0:
            fails.append(f"caso4: exit {r.returncode}: {r.stdout}{r.stderr}")
        else:
            c1 = [json.loads(l) for l in open(os.path.join(lib, "claims.jsonl"), encoding="utf-8")][0]
            ev = c1["evidence"]
            if ev.count("f-000111") != 1:
                fails.append(f"caso4: ref duplicada (adjudicada = verificada): {ev}")
            if ev[:1] != ["s-000010"] or ev != ["s-000010", "f-000111", "f-000222"]:
                fails.append(f"caso4: orden/dedup inesperados: {ev}")
            # re-ejecutar la integración completa: el resultado es idempotente
            r2 = run_integrate(run, lib)
            c1b = [json.loads(l) for l in open(os.path.join(lib, "claims.jsonl"), encoding="utf-8")][0]
            if r2.returncode != 0 or c1b["evidence"] != ev:
                fails.append(f"caso4: reintegración no idempotente: {c1b['evidence']}")

    # Caso 5: integración parcial jamás sobrescribe el canónico
    with tempfile.TemporaryDirectory() as root:
        run, lib = build_run(root)
        adj = {"k1": {"refs": ["f-000222"], "proof": "spool"}}
        json.dump(adj, open(os.path.join(run, "evidence-adjudications.json"), "w",
                            encoding="utf-8"))
        r = run_integrate(run, lib)
        canon = os.path.join(lib, "claims.jsonl")
        full = open(canon, "rb").read()
        # ejecutar como parcial: añadir un review de otro minuto no aplicado
        CLAIMS_M1 = [{"key": "k2", "id": "c-0002", "minute": 1, "statement": "y",
                      "evidence": ["s-000010"]}]
        with open(os.path.join(run, "claims-pool.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(CLAIMS_M1[0], ensure_ascii=False) + "\n")
        json.dump({"minute": 1, "transcript": TRANSCRIPT, "claims": CLAIMS_M1},
                  open(os.path.join(run, "reviews", "payload-min1.json"), "w", encoding="utf-8"))
        json.dump({"minute": 1, "results": [
            {"claim_key": "k2", "verdict": "SUPPORTED", "verified_evidence": ["s-000010"],
             "reason": "ok m1", "unresolved_questions": []}]},
            open(os.path.join(run, "reviews", "review-min1.json"), "w", encoding="utf-8"))
        r = subprocess.run([sys.executable, INTEGRATE, "--run", run, "--lib", lib,
                            "--validate", VALIDATE, "1"],
                           capture_output=True, text=True)
        if r.returncode == 0:
            fails.append("caso5: integración parcial con exit 0")
        if open(canon, "rb").read() != full:
            fails.append("caso5: canónico ALTERADO por integración parcial")
        if not os.path.exists(os.path.join(lib, "claims.jsonl.partial")):
            fails.append("caso5: falta claims.jsonl.partial")

    if fails:
        print("FAIL")
        for f in fails:
            print(" -", f)
        sys.exit(1)
    print("PASS (5 casos)")


if __name__ == "__main__":
    main()
