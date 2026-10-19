#!/usr/bin/env python3
"""source_first_selftest.py — red-green del chequeo SOURCE-FIRST de términos.

Casos (1 y 6/7 son defectos REALES; ch03 2026-10-18 y ch02 2026-10-19):
  1  transcript "al DOL" / claim "al DXY" -> MATERIAL FINDING (caso c-0121 ch03)
  2  transcript "el DXY está bearish" / claim "el DXY" -> PASS (DXY genuino no se toca)
  3  claim superseded con statement equivocado -> no se flaggea (historia preservada)
  4  garble preservado "doble [ASR]" (ni DOL ni DXY en statement) -> PASS
  5  grupo extendido por --groups funciona (formato legacy)
  6  CASO REAL ch02 c-0089: fuente "a por tu dol" (minúscula) / claim "tu DXY"
     -> MATERIAL (el lado fuente es case-insensitive)
  7  CASO REAL ch02 c-0066: fuente "el doble ... el dol" / claim "DXY"
     -> MATERIAL (el "dol" de la fuente es canónico del grupo)
  8  fuente SÓLO "el doble" (garble ambiguo) / claim "DXY" sin [ASR]
     -> TERM_DISAMBIGUATION_REQUIRED (REVIEW; el chequeo no decide el término)
  9  fuente "el doble" / claim "DOL [ASR: 'el doble']" -> PASS (adjudicado)
  10 aliases custom por --groups (formato rico) funcionan

Uso:  python3 source_first_selftest.py
"""
import json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHECK = os.path.join(HERE, "..", "check_term_sources.py")


def check(label, cond):
    print(f"{'PASS' if cond else 'FAIL'}  {label}")
    return cond


def build_lib(root, claims, transcript=None):
    lib = os.path.join(root, "lib")
    os.makedirs(os.path.join(lib, "frames"))
    open(os.path.join(lib, "frames", "f-000010.png"), "w").close()
    open(os.path.join(lib, "transcript.md"), "w", encoding="utf-8").write(
        transcript if transcript is not None else
        "# t\n\n"
        "s-000010 [00:00:10-00:00:20] es muy normal que se llegue al DOL utilizando esa volatilidad\n\n"
        "s-000020 [00:00:20-00:00:30] si el DXY está bearish el precio va a seguir\n\n"
        "s-000030 [00:00:30-00:00:40] cuando hay día de NCP o algo así\n\n")
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

        # 5: grupo extendido (formato legacy lista de listas)
        lib5 = build_lib(tmp + "5", [
            {"id": "c-0001", "statement": "cuando hay día de NFP es muy normal", "evidence": ["s-000030"],
             "verdict": "SUPPORTED"}])
        rc5, out5 = run(lib5, ("--groups", '[["DOL","DXY"],["NFP","NCP"]]'))
        ok &= check("5 grupo extendido detecta sustitución", rc5 == 1
                    and out5["findings"][0]["published"] == "NFP")

        # 6: CASO REAL ch02 (c-0089) — fuente "a por tu dol" minúscula, claim "tu DXY"
        tr6 = ("# t\n\n"
               "s-001401 [00:14:01-00:14:15] Esto se puede aplicar a todo. Si tú vas a 8 horas, "
               "lo que vas a querer ver en 8 horas es lo mismo. Ver cómo tienes un rango a favor "
               "para ir a por tu tendencia, a por tu dol, perdón, a por tu objetivo.\n\n")
        lib6 = build_lib(tmp + "6", [
            {"id": "c-0089", "statement": "Esto se puede aplicar a todo: en 8 horas lo que vas a querer "
                                          "ver es lo mismo, un rango a favor para ir a por tu tendencia "
                                          "—a por tu DXY, perdón, a por tu objetivo—.",
             "evidence": ["s-001401"], "verdict": "SUPPORTED"}], transcript=tr6)
        rc6, out6 = run(lib6)
        ok &= check("6 ch02 real: 'tu dol' publicado 'tu DXY' -> MATERIAL",
                    rc6 == 1 and out6["findings"][0]["severity"] == "MATERIAL"
                    and out6["findings"][0]["published"] == "DXY"
                    and out6["findings"][0]["source_has"] == ["DOL"])

        # 7: CASO REAL ch02 (c-0066) — fuente "el doble ... el dol", claim "DXY"
        tr7 = ("# t\n\n"
               "s-001005 [00:10:05-00:10:10] pues seguramente va a tomar el low de este y si el doble "
               "está veris va a seguir para abajo y si el\n\n"
               "s-001010 [00:10:10-00:10:17] dol está bullish va a tomar el low crear un rango bullish "
               "y subir vale yo que estoy en short desde\n\n")
        lib7 = build_lib(tmp + "7", [
            {"id": "c-0066", "statement": "A las 5 seguramente va a tomar el low de este y, si el DXY "
                                          "está bearish, va a seguir para abajo; si el DXY está bullish, "
                                          "va a tomar el low, crear un rango bullish y subir.",
             "evidence": ["s-001005", "s-001010"], "verdict": "SUPPORTED"}], transcript=tr7)
        rc7, out7 = run(lib7)
        ok &= check("7 ch02 real: 'el doble/el dol' publicado 'DXY' -> MATERIAL",
                    rc7 == 1 and out7["findings"][0]["severity"] == "MATERIAL"
                    and out7["findings"][0]["source_has"] == ["DOL"])

        # 8: fuente SÓLO garble ambiguo, claim canónico SIN [ASR] -> TERM_DISAMBIGUATION_REQUIRED
        tr8 = ("# t\n\n"
               "s-000010 [00:00:10-00:00:20] si el doble está veris va a seguir para abajo\n\n")
        lib8 = build_lib(tmp + "8", [
            {"id": "c-0001", "statement": "si el DXY está bearish, va a seguir para abajo",
             "evidence": ["s-000010"], "verdict": "SUPPORTED"}], transcript=tr8)
        rc8, out8 = run(lib8)
        f8 = out8["findings"][0] if out8["findings"] else {}
        ok &= check("8 garble ambiguo sin adjudicación -> TERM_DISAMBIGUATION_REQUIRED (REVIEW)",
                    rc8 == 1 and f8.get("severity") == "REVIEW"
                    and f8.get("type") == "TERM_DISAMBIGUATION_REQUIRED")

        # 9: misma fuente con la marca de adjudicación del protocolo -> PASS
        lib9 = build_lib(tmp + "9", [
            {"id": "c-0001", "statement": "si el DOL [ASR: 'el doble'] está bearish, va a seguir para abajo",
             "evidence": ["s-000010"], "verdict": "SUPPORTED"}], transcript=tr8)
        rc9, out9 = run(lib9)
        ok &= check("9 adjudicación [ASR] explícita -> PASS", rc9 == 0 and out9["findings"] == [])

        # 10: aliases custom con formato rico por --groups
        lib10 = build_lib(tmp + "10", [
            {"id": "c-0001", "statement": "el NFP lleva el precio con esa volatilidad",
             "evidence": ["s-000030"], "verdict": "SUPPORTED"}])
        rc10, out10 = run(lib10, ("--groups",
                                  json.dumps([{"term": "NFP", "aliases": ["en cepe"]}])
                                  .replace("en cepe", "NCP")))
        ok &= check("10 aliases custom (formato rico) -> MATERIAL",
                    rc10 == 1 and out10["findings"][0]["published"] == "NFP")
    finally:
        shutil.rmtree(tmp)
    print("SOURCE_FIRST_SELFTEST =", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
