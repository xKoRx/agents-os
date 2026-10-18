#!/usr/bin/env python3
"""review_pipeline_selftest.py — red-green del pipeline payload -> review -> validación.

Cubre el defecto encontrado en ch03 (2026-10-18): make_minute_payload.py debe
emitir `key` por claim (contrato del worker) y validate_review.py debe aceptar
`claim_key` o `key` en los resultados del reviewer.

Casos:
  1  payload contiene key == id para cada claim
  2  review con claim_key -> VALID
  3  review con key (compatibilidad ch02) -> VALID
  4  review con claves distintas -> INVALID (R01)
  5  review omite un claim -> INVALID (R01)

Uso:  python3 review_pipeline_selftest.py
"""
import json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PAYLOAD = os.path.join(HERE, "..", "make_minute_payload.py")
VALIDATE = os.path.join(HERE, "..", "validate_review.py")

TRANSCRIPT = """s-000010 [00:00:10-00:00:20] texto uno

s-000030 [00:00:30-00:00:40] texto dos
"""
CLAIMS = [
    {"id": "c-0001", "minute": 0, "statement": "x", "evidence": ["s-000010"]},
    {"id": "c-0002", "minute": 0, "statement": "y", "evidence": ["s-000030"]},
]


def check(label, cond):
    print(f"{'PASS' if cond else 'FAIL'}  {label}")
    return cond


def main():
    tmp = tempfile.mkdtemp(prefix="cke-review-")
    ok = True
    t = os.path.join(tmp, "transcript.md")
    open(t, "w", encoding="utf-8").write(TRANSCRIPT)
    c = os.path.join(tmp, "claims.jsonl")
    with open(c, "w", encoding="utf-8") as f:
        for cl in CLAIMS:
            f.write(json.dumps(cl) + "\n")
    p = os.path.join(tmp, "payload-00.json")
    subprocess.run([sys.executable, PAYLOAD, t, c, "0", p], check=True, capture_output=True)
    payload = json.load(open(p, encoding="utf-8"))

    ok &= check("1 payload: key == id en cada claim",
                [x.get("key") for x in payload["claims"]] == ["c-0001", "c-0002"])

    def validate(review_obj, name):
        r = os.path.join(tmp, name)
        json.dump(review_obj, open(r, "w", encoding="utf-8"))
        return subprocess.run([sys.executable, VALIDATE, p, r], capture_output=True, text=True)

    def result(k):
        return {"claim_key": k, "verdict": "SUPPORTED", "verified_evidence": ["s-000010"], "reason": ""}

    rv = validate({"minute": 0, "results": [result("c-0001"), result("c-0002")]}, "r1.json")
    ok &= check("2 review con claim_key -> VALID", rv.returncode == 0 and "VALID" in rv.stdout)

    rv2 = validate({"minute": 0, "results": [
        {"key": "c-0001", "verdict": "SUPPORTED", "verified_evidence": ["s-000010"]},
        {"key": "c-0002", "verdict": "UNCERTAIN", "verified_evidence": []}]}, "r2.json")
    ok &= check("3 review con key (compat) -> VALID", rv2.returncode == 0 and "VALID" in rv2.stdout)

    rv3 = validate({"minute": 0, "results": [result("c-0001"), result("c-9999")]}, "r3.json")
    ok &= check("4 claves distintas -> INVALID R01", rv3.returncode == 1 and "R01" in rv3.stdout)

    rv4 = validate({"minute": 0, "results": [result("c-0001")]}, "r4.json")
    ok &= check("5 claim omitido -> INVALID R01", rv4.returncode == 1 and "R01" in rv4.stdout)

    import shutil
    shutil.rmtree(tmp)
    print("REVIEW_PIPELINE_SELFTEST =", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
