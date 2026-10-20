#!/usr/bin/env python3
"""fixtures_selftest.py — red-green del validador sobre bibliotecas mínimas.

Construye una biblioteca mínima válida y 7 variantes con defectos inyectados,
ejecuta validate_library.py sobre cada una y assertiona el resultado esperado.
Los frames son placeholders vacíos: el validador comprueba existencia, naming
y timestamps, no contenido.

Uso:  python3 fixtures_selftest.py
Exit 0 = todos los casos como se esperaba.
"""
import json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
VALIDATOR = os.path.join(HERE, "..", "validate_library.py")

README_TMPL = """# fixture

| Métrica | Valor |
|---|---|
| Claims totales | {claims} |
| Rules / concepts / examples documentados | {rules} / 1 / 1 |
| Frames base (fin de minuto) | 1 |
| Frames bajo demanda | 0 |
"""


def build_base(root):
    os.makedirs(os.path.join(root, "frames"))
    open(os.path.join(root, "frames", "f-000010.png"), "w").close()
    open(os.path.join(root, "transcript.md"), "w", encoding="utf-8").write(
        "# t\n\ns-000010 [00:00:10-00:00:20] texto uno\n"
        "s-000030 [00:00:30-00:00:40] texto dos\n")
    claims = [
        {"id": "c-0001", "minute": 0, "kind": "rule", "statement": "regla hablada",
         "evidence": ["s-000010"], "verdict": "SUPPORTED", "notes": "",
         "epistemic": "instructor_statement"},
        {"id": "c-0002", "minute": 0, "kind": "observation", "statement": "se ve un rango",
         "evidence": ["s-000030", "f-000010"], "verdict": "SUPPORTED", "notes": "",
         "epistemic": "visual_observation", "visual_hint": {"second": 30, "what": "rango"}},
    ]
    with open(os.path.join(root, "claims.jsonl"), "w", encoding="utf-8") as f:
        for c in claims:
            f.write(json.dumps(c) + "\n")
    open(os.path.join(root, "rules.md"), "w").write("**R1 · regla** [00:10, c-0001]\n")
    open(os.path.join(root, "concepts.md"), "w").write("## Concepto\nalgo\n")
    open(os.path.join(root, "examples.md"), "w").write("## E1 ejemplo\nalgo\n")
    open(os.path.join(root, "README.md"), "w", encoding="utf-8").write(
        README_TMPL.format(claims=2, rules=1))
    return claims


def variant(base, name, mutate):
    dst = os.path.join(os.path.dirname(base), name)
    shutil.copytree(base, dst)
    mutate(dst)
    return dst


def run(lib, extra=()):
    r = subprocess.run([sys.executable, VALIDATOR, lib, "--duration-seconds", "60", "--json"],
                       capture_output=True, text=True)
    return r.returncode, json.loads(r.stdout)


def expect(label, lib, want_pass, want_checks=()):
    rc, out = run(lib)
    checks = {f["check"] for f in out["findings"]}
    ok = (rc == 0 and out["pass"]) if want_pass else (rc == 1 and not out["pass"] and set(want_checks) <= checks)
    print(f"{'PASS' if ok else 'FAIL'}  {label}: rc={rc} checks={sorted(checks)} (esperaba {'PASS' if want_pass else sorted(want_checks)})")
    return ok


def main():
    tmp = tempfile.mkdtemp(prefix="cke-fixtures-")
    base = os.path.join(tmp, "base")
    build_base(base)
    ok = True

    ok &= expect("base válida", base, True)

    def m_missing_frame(d):
        p = os.path.join(d, "claims.jsonl")
        t = open(p, encoding="utf-8").read().replace("f-000010", "f-999999")
        open(p, "w", encoding="utf-8").write(t)
    ok &= expect("A/B frame inexistente", variant(base, "bad-missing-frame", m_missing_frame), False, {"V03"})

    def m_invalid_names(d):
        open(os.path.join(d, "frames", "f-12345678.png"), "w").close()   # V04
        open(os.path.join(d, "frames", "f-124400.png"), "w").close()     # V05 (12:44:00 > 60s)
    ok &= expect("nombres inválidos / fuera de duración", variant(base, "bad-names", m_invalid_names), False, {"V04", "V05"})

    def m_visual_no_frame(d):
        p = os.path.join(d, "claims.jsonl")
        t = open(p, encoding="utf-8").read().replace('"s-000030", "f-000010"', '"s-000030"')
        open(p, "w", encoding="utf-8").write(t)
    ok &= expect("A claim visual sin frame", variant(base, "bad-visual-no-frame", m_visual_no_frame), False, {"V07", "V08"})

    def m_broken_ev(d):
        p = os.path.join(d, "claims.jsonl")
        t = open(p, encoding="utf-8").read()
        open(p, "w", encoding="utf-8").write(t.replace("s-000010", "s-999999"))
    ok &= expect("evidencia inexistente", variant(base, "bad-broken-evidence", m_broken_ev), False, {"V02"})

    def m_dup(d):
        p = os.path.join(d, "claims.jsonl")
        open(p, "a", encoding="utf-8").write(open(p, encoding="utf-8").readlines()[0])
    ok &= expect("id duplicado", variant(base, "bad-dup-id", m_dup), False, {"V01"})

    def m_readme(d):
        p = os.path.join(d, "README.md")
        open(p, "w", encoding="utf-8").write(README_TMPL.format(claims=2, rules=5))
    ok &= expect("F conteo README incorrecto", variant(base, "bad-readme-count", m_readme), False, {"V10"})

    def m_historical(d):
        open(os.path.join(d, "review-notes.md"), "w").write("histórico: f-044000 estaba mal\n")
    lib_hist = variant(base, "bad-historical-undeclared", m_historical)
    ok &= expect("B nombre histórico sin declarar", lib_hist, False, {"V11"})
    open(os.path.join(lib_hist, ".deprecated_frame_names"), "w").write("f-044000\n")
    ok &= expect("B nombre histórico declarado", lib_hist, True)

    def m_inference(d):
        p = os.path.join(d, "claims.jsonl")
        t = open(p, encoding="utf-8").read().replace('"epistemic": "instructor_statement"', '"epistemic": "model_inference"')
        open(p, "w", encoding="utf-8").write(t)
    ok &= expect("E model_inference SUPPORTED sin adjudicar", variant(base, "bad-inference", m_inference), False, {"V13"})

    def m_hint_seconds(d):
        # defecto real ch05 (DV-04): HHMMSS pegado como segundos crudos
        p = os.path.join(d, "claims.jsonl")
        t = open(p, encoding="utf-8").read().replace('"visual_hint": {"second": 30,', '"visual_hint": {"second": 1635,')
        open(p, "w", encoding="utf-8").write(t)
    ok &= expect("G visual_hint.second fuera de duración (HHMMSS pegado)", variant(base, "bad-hint-seconds", m_hint_seconds), False, {"V08"})

    shutil.rmtree(tmp)
    print("FIXTURES_SELFTEST =", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
