#!/usr/bin/env python3
"""source_first_selftest.py — red-green del chequeo SOURCE-FIRST de términos.

Casos (el primero es el defecto REAL de ch03, 2026-10-18):
  1  transcript "al DOL" / claim "al DXY" -> MATERIAL FINDING (caso c-0121)
  2  transcript "el DXY está bearish" / claim "el DXY" -> PASS (DXY genuino no se toca)
  3  claim superseded con statement equivocado -> no se flaggea (historia preservada)
  4  garble preservado "doble [ASR]" (ni DOL ni DXY en statement) -> PASS
  5  grupo extendido por --groups funciona

Uso:  python3 source_first_selftest.py
"""
import json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHECK = os.path.join(HERE, "..", "check_term_sources.py")


def check(label, cond):
    print(f"{'PASS' if cond else 'FAIL'}  {label}")
    return cond


def build_lib(root, claims):
    lib = os.path.join(root, "lib")
    os.makedirs(os.path.join(lib, "frames"))
    open(os.path.join(lib, "frames", "f-000010.png"), "w").close()
    open(os.path.join(lib, "transcript.md"), "w", encoding="utf-8").write(
        "# t\n\ns-000010 [00:00:10-00:00:20] es muy normal que se llegue al DOL utilizando esa volatilidad\n\n"
        "s-000020 [00:00:20-00:00:30] si el DXY está bearish el precio va a seguir\n\n"
        "s-000030 [00:00:30-00:00:40] cuando hay día de NCP o algo así\n")
    with open(os.path.join(lib, "claims.jsonl"), "w", encoding="utf-8") as f:
        for c in claims:
            f.write(json.dumps(c) + "\n")
    return lib


def run(lib, extra=()):
    r = subprocess.run([sys.executable, CHECK, lib, *extra, "--json"],
                       capture_output=True, text=True)
    return r.returncode, json.loads(r.stdout)


def main():
    tmp = tempfile.mkdtemp(prefix="cke-term-")
    ok = True
    try:
        # 1: el caso real c-0121 — transcript "al DOL", claim "al DXY"
        lib = build_lib(tmp, [
            {"id": "c-0001", "statement": "es muy normal que se llegue al DXY utilizando esa volatilidad",
             "evidence": ["s-000010"], "verdict": "SUPPORTED"}])
        rc, out = run(lib)
        ok &= check("1 'al DOL' publicado como 'al DXY' -> MATERIAL FINDING",
                    rc == 1 and out["findings"][0]["severity"] == "MATERIAL"
                    and out["findings"][0]["claim"] == "c-0001" and out["findings"][0]["published"] == "DXY")

        # 2: mención genuina de DXY con respaldo en fuente -> no se sustituye ni se flaggea
        lib2 = build_lib(tmp + "2", [
            {"id": "c-0001", "statement": "si el DXY está bearish, el precio va a seguir",
             "evidence": ["s-000020"], "verdict": "SUPPORTED"}])
        rc2, out2 = run(lib2)
        ok &= check("2 DXY genuino citado de fuente -> PASS", rc2 == 0 and out2["findings"] == [])

        # 3: claim superseded -> excluido del chequeo (historia preservada)
        lib3 = build_lib(tmp + "3", [
            {"id": "c-0001", "statement": "llega al DXY", "evidence": ["s-000010"],
             "verdict": "SUPPORTED", "superseded_by": "c-0002"}])
        rc3, out3 = run(lib3)
        ok &= check("3 claim superseded excluido", rc3 == 0 and out3["checked"] == 0)

        # 4: garble preservado sin término canónico en statement -> PASS
        lib4 = build_lib(tmp + "4", [
            {"id": "c-0001", "statement": "se llega al doble [ASR] con esa volatilidad",
             "evidence": ["s-000010"], "verdict": "SUPPORTED"}])
        rc4, out4 = run(lib4)
        ok &= check("4 garble preservado -> PASS", rc4 == 0 and out4["findings"] == [])

        # 5: grupo extendido
        lib5 = build_lib(tmp + "5", [
            {"id": "c-0001", "statement": "cuando hay día de NFP es muy normal", "evidence": ["s-000030"],
             "verdict": "SUPPORTED"}])
        rc5, out5 = run(lib5, ("--groups", '[["DOL","DXY"],["NFP","NCP"]]'))
        ok &= check("5 grupo extendido detecta sustitución", rc5 == 1
                    and out5["findings"][0]["published"] == "NFP")
    finally:
        shutil.rmtree(tmp)
    print("SOURCE_FIRST_SELFTEST =", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
