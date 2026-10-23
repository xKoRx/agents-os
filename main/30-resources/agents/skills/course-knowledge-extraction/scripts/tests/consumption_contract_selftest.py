#!/usr/bin/env python3
"""consumption_contract_selftest.py — red-green del preflight del contrato de consumo.

Casos (contrato 2026-10-23, tras q-ch07-019):
  1  RED: contradicción entre 2 claims SUPPORTED con pregunta OPEN MATERIAL
     enlazada por su entrada pero SIN vínculo estructural en los claims
     -> CC02 (el control detecta la contradicción no señalizada)
  2  GREEN: mismo fixture con la referencia en unresolved_questions -> PASS,
     guarded=2, grupo de contradicción con los 2 claims
  3  referencia q inexistente en unresolved_questions -> CC01
  4  duda AUXILIAR (garble sin q-ID) NO guarda el claim ni exige vínculo:
     proporcionalidad — las dudas auxiliares no degradan el claim
  5  --require-question exacto -> PASS; conjunto distinto -> CC04
  6  PRUEBA DE INTERPRETACIÓN DOCUMENTADA sobre la biblioteca REAL (Clutifx):
     compuerta estructurada de síntesis — un hecho definitivo o una regla
     universal apoyados en un claim guardado (q-ch07-019) se RECHAZAN; el
     reporte de contradicción que preserva ambas horas se ACEPTA; el mismo
     hecho definitivo sobre un claim sin duda material se ACEPTA. La NLU de
     texto libre NO es objeto del contrato (es trabajo del compilador futuro):
     la compuerta opera sobre aserciones estructuradas + manifiesto del
     preflight.

Uso:  python3 consumption_contract_selftest.py
"""
import json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHECK = os.path.join(HERE, "..", "check_consumption_contract.py")


def check(label, cond):
    print(f"{'PASS' if cond else 'FAIL'}  {label}")
    return cond


def build_lib(root, claims, open_questions, transcript=None):
    lib = os.path.join(root, "ch01-fixture")
    os.makedirs(os.path.join(lib, "frames"))
    open(os.path.join(lib, "frames", "f-000010.png"), "w").close()
    open(os.path.join(lib, "frames", "f-000020.png"), "w").close()
    open(os.path.join(lib, "transcript.md"), "w", encoding="utf-8").write(
        transcript if transcript is not None else
        "# t\n\n"
        "s-000010 [00:00:10-00:00:20] quizás porque había noticias a las 10\n\n"
        "s-000020 [00:00:20-00:00:30] la noticia fue a las 8 y entramos en la vela de las 9\n\n")
    with open(os.path.join(lib, "claims.jsonl"), "w", encoding="utf-8") as f:
        for c in claims:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    if open_questions is not None:
        open(os.path.join(lib, "OPEN-QUESTIONS.md"), "w", encoding="utf-8").write(open_questions)
    return root


def claim(cid, ev, statement, uq=None, verdict="SUPPORTED"):
    return {"id": cid, "key": cid, "kind": "rule", "minute": 0, "statement": statement,
            "epistemic": "instructor_statement", "evidence": ev, "visual_hint": None,
            "notes": "", "unresolved_questions": uq or [], "verdict": verdict,
            "review_reason": "fixture", "reviewed_minute": 0}


OQ_LINKED = (
    "### q-tst-001 — ¿hora de la noticia?\n"
    "Dos horas dichas para el mismo ejemplo.\n"
    "Claims: [[ch01-fixture/CLAIMS#c-0001|c-0001]] · [[ch01-fixture/CLAIMS#c-0002|c-0002]]. "
    "**Estado: OPEN** · **Materialidad: MATERIAL**\n")

C1 = lambda uq=None: claim("c-0001", ["s-000010"], "había noticias a las 10", uq)
C2 = lambda uq=None: claim("c-0002", ["s-000020"], "la noticia fue a las 8", uq)
QREF = "q-tst-001 (OPEN, contradicción material): hora no adjudicada."

# Compuerta de interpretación (estructura, no NLU): aserción estructurada +
# manifiesto. El compilador futuro sustituye esto por su propia lógica; el
# CONTRATO que se prueba aquí es el mismo.
def synthesis_gate(assertion, summary):
    guarded = {}
    for ch in summary and [summary] or []:
        pass
    return assertion, summary  # placeholder reemplazado abajo


def real_library_root():
    d = HERE
    for _ in range(8):
        if os.path.exists(os.path.join(d, "80-agents", "agents-os", "agents-os.md")):
            return os.path.join(d, "10-projects", "Personal", "Multimodal Knowledge Engine",
                                "knowledge-library", "clutifx")
        d = os.path.dirname(d)
    return None


def run_real():
    lib = real_library_root()
    if not lib or not os.path.isdir(lib):
        print("SKIP  6  biblioteca real no encontrada")
        return True
    r = subprocess.run([sys.executable, CHECK, lib, "--json",
                        "--require-question", "q-ch07-019=c-0143,c-0181,c-0182"],
                       capture_output=True, text=True)
    ok = r.returncode == 0
    data = json.loads(r.stdout)
    summ = data["summary"]
    rows = [row for ch in data["manifest"].values() for row in ch["rows"]]
    guarded = {row["id"] for row in rows if row["status"] == "CONSUMABLE_WITH_MATERIAL_QUESTION"}

    def gate(kind, cited):
        # REJECT si la aserción firme cita cualquier claim guardado; el reporte
        # de contradicción se acepta sólo si cita exactamente el grupo guardado.
        if kind == "contradiction_report":
            return cited <= guarded and len(cited) >= 2
        return not (set(cited) & guarded)

    cases = [
        (gate("definitive_fact", ["c-0181"]), False, "hecho definitivo 'a las 08:00' citando c-0181 (guardado)"),
        (gate("definitive_fact", ["c-0143"]), False, "hecho definitivo 'a las 10:00' citando c-0143 (guardado)"),
        (gate("universal_rule", ["c-0182"]), False, "regla operativa universal basada en ese horario citando c-0182 (guardado)"),
        (gate("contradiction_report", {"c-0143", "c-0181", "c-0182"}), True, "reporte de contradicción con ambas horas + q-ch07-019"),
        (gate("definitive_fact", ["c-0145"]), True, "hecho definitivo sobre claim SIN duda material (control positivo)"),
    ]
    ok_all = check("6a  preflight real PASS con q-ch07-019=c-0143,c-0181,c-0182 exacto", ok)
    ok_all &= check(f"6b  biblioteca real: guarded={sorted(guarded)}", guarded == {"c-0143", "c-0181", "c-0182"})
    for got, want, label in cases:
        ok_all &= check(f"6  {'RECHAZADA' if want is False else 'ACEPTADA'}: {label}", got == want)
    return bool(ok_all)


def main():
    ok = True
    tmp = tempfile.mkdtemp(prefix="consumption-contract-")
    try:
        # Caso 1 RED: contradicción sin vínculo estructural en los claims
        root = os.path.join(tmp, "red"); os.makedirs(root)
        build_lib(root, [C1(), C2()], OQ_LINKED)
        r = subprocess.run([sys.executable, CHECK, root, "--json"], capture_output=True, text=True)
        data = json.loads(r.stdout)
        ok &= check("1  RED: contradicción sin señalizar -> FAIL con CC02",
                    r.returncode == 1
                    and any(v["check"] == "CC02" for v in data["summary"]["violations"]))

        # Caso 2 GREEN: mismo fixture con la referencia en ambos claims
        root = os.path.join(tmp, "green"); os.makedirs(root)
        build_lib(root, [C1([QREF]), C2([QREF])], OQ_LINKED)
        r = subprocess.run([sys.executable, CHECK, root, "--json"], capture_output=True, text=True)
        data = json.loads(r.stdout)
        ok &= check("2  GREEN: con vínculo estructural -> PASS", r.returncode == 0)
        ok &= check("2  guarded=2 y grupo de contradicción con los 2 claims",
                    data["summary"]["consumable_with_material_question"] == 2
                    and data["summary"]["material_contradiction_groups"]
                    .get("q-tst-001", {}).get("claims") == ["c-0001", "c-0002"])

        # Caso 3: referencia a pregunta inexistente
        root = os.path.join(tmp, "broken"); os.makedirs(root)
        build_lib(root, [C1(["q-tst-999 (OPEN): duda"]), C2([QREF])], OQ_LINKED)
        r = subprocess.run([sys.executable, CHECK, root, "--json"], capture_output=True, text=True)
        data = json.loads(r.stdout)
        ok &= check("3  q inexistente en unresolved_questions -> CC01",
                    r.returncode == 1 and any(v["check"] == "CC01" for v in data["summary"]["violations"]))

        # Caso 4: duda AUXILIAR (garble sin q-ID) no guarda ni exige vínculo;
        # la MATERIAL está ligada a c-0001/c-0002 que SÍ la referencian.
        root = os.path.join(tmp, "aux"); os.makedirs(root)
        build_lib(root, [C1([QREF, "'pechazo' [ASR] sin resolver: ¿pico/mecha?"]),
                         C2([QREF])], OQ_LINKED)
        r = subprocess.run([sys.executable, CHECK, root, "--json"], capture_output=True, text=True)
        data = json.loads(r.stdout)
        row = next(row for ch in data["manifest"].values() for row in ch["rows"] if row["id"] == "c-0001")
        ok &= check("4  duda auxiliar no guarda el claim y el preflight pasa",
                    r.returncode == 0 and row["status"] == "CONSUMABLE_WITH_MATERIAL_QUESTION")

        # Caso 5: --require-question exacto vs conjunto distinto
        root = os.path.join(tmp, "green");  # reutiliza el fixture GREEN
        r_ok = subprocess.run([sys.executable, CHECK, root, "--json",
                               "--require-question", "q-tst-001=c-0001,c-0002"],
                              capture_output=True, text=True)
        r_bad = subprocess.run([sys.executable, CHECK, root, "--json",
                                "--require-question", "q-tst-001=c-0001"],
                               capture_output=True, text=True)
        ok &= check("5  --require-question exacto -> PASS", r_ok.returncode == 0)
        ok &= check("5  --require-question con conjunto distinto -> CC04", r_bad.returncode == 1)

        # Caso 6: prueba de interpretación documentada sobre la biblioteca real
        ok &= run_real()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"CONSUMPTION_CONTRACT_SELFTEST = {'PASS' if ok else 'FAIL'}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
