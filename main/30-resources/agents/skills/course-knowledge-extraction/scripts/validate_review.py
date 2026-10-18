#!/usr/bin/env python3
"""validate_review.py — cardinalidad y contrato de un review por minuto.

Uso:
    validate_review.py <payload.json> <review.json>

Payload:  {"minute": N, "transcript": "texto con ids s-...", "claims": [{"key": "..."}]}
Review:   {"minute": N, "results": [{"key": "...", "verdict": "...", "verified_evidence": ["s-...", ...], ...}]}

Chequeos:
  R01  cardinalidad: exactamente un resultado por claim de entrada, sin extras ni duplicados
  R02  veredictos en vocabulario
  R03  SUPPORTED exige verified_evidence no vacío
  R04  refs de verified_evidence que sean s- resuelven en el transcript del payload

Exit 0 = VALID, 1 = MINUTE_REVIEW INVALID, 2 = uso/IO.
"""
import json, re, sys


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    payload = json.load(open(sys.argv[1], encoding="utf-8"))
    review = json.load(open(sys.argv[2], encoding="utf-8"))
    findings = []

    want = [c["key"] for c in payload.get("claims", []) if "key" in c] or \
           [c["id"] for c in payload.get("claims", [])]
    results = review.get("results", [])
    got = [r.get("claim_key") or r.get("key") for r in results]

    dupes = sorted({k for k in got if got.count(k) > 1})
    missing = sorted(set(want) - set(got))
    extra = sorted(set(got) - set(want))
    if len(got) != len(want) or missing or extra or dupes:
        findings.append(f"R01 MINUTE_REVIEW INVALID: entrada={len(want)} salida={len(got)} "
                        f"missing={missing} extra={extra} duplicados={dupes}")

    vocab = {"SUPPORTED", "UNCERTAIN", "UNVERIFIED"}
    sids = set(re.findall(r"s-\d{6}[a-z]?", payload.get("transcript", "")))
    for r in results:
        if r.get("verdict") not in vocab:
            findings.append(f"R02 {r.get('key')}: veredicto fuera de vocabulario: {r.get('verdict')!r}")
        ve = r.get("verified_evidence", [])
        if r.get("verdict") == "SUPPORTED" and not ve:
            findings.append(f"R03 {r.get('key')}: SUPPORTED sin verified_evidence")
        for e in ve or []:
            if e.startswith("s-") and e not in sids:
                findings.append(f"R04 {r.get('key')}: verified_evidence cita segmento fuera del payload: {e}")

    for f in findings:
        print(f"[ERROR] {f}")
    print(f"MINUTE_REVIEW = {'VALID' if not findings else 'INVALID'}  ({len(want)} claims entrada, {len(got)} resultados)")
    sys.exit(0 if not findings else 1)


if __name__ == "__main__":
    main()
