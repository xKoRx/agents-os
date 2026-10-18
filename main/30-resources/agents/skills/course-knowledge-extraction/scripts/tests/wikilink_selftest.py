#!/usr/bin/env python3
"""wikilink_selftest.py — red-green de los checks W del validador.

Construye un mini-vault (con marker de AGENTS OS) con una biblioteca mínima
navegable y 11 variantes defectuosas; assertiona que el validador detecte cada
defecto con el check esperado y que la base pase. Cubre: links rotos, headings
y block ids inexistentes, PNG ambiguo, anchors duplicados y sin bloque propio,
proyección CLAIMS.md stale (heading/verdict/statement/epistemic) y wikilinks
desequilibrados.

Uso:  python3 wikilink_selftest.py
"""
import json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
VALIDATOR = os.path.join(HERE, "..", "validate_library.py")

TRANSCRIPT = """# t

s-000010 [00:00:10-00:00:20] texto uno ^s-000010

s-000030 [00:00:30-00:00:40] texto dos ^s-000030
"""
CLAIMS = [
    {"id": "c-0001", "minute": 0, "kind": "rule", "statement": "regla hablada",
     "evidence": ["s-000010"], "verdict": "SUPPORTED", "notes": "",
     "epistemic": "instructor_statement"},
    {"id": "c-0002", "minute": 0, "kind": "observation", "statement": "se ve un rango",
     "evidence": ["s-000030", "f-000010"], "verdict": "SUPPORTED", "notes": "",
     "epistemic": "visual_observation", "visual_hint": {"second": 30, "what": "rango"}},
]


def claims_md(claims, missing=None, wrong_verdict=False, wrong_statement=False,
              wrong_epistemic=False):
    out = []
    for c in claims:
        if c["id"] == missing:
            continue
        v = "UNCERTAIN" if (wrong_verdict and c["id"] == "c-0002") else c["verdict"]
        st = "otra cosa" if (wrong_statement and c["id"] == "c-0001") else c["statement"]
        ep = "model_inference" if (wrong_epistemic and c["id"] == "c-0002") else c["epistemic"]
        out.append(f"### {c['id']}\n\n**Statement:** {st}\n\n**Verdict:** {v} ·"
                   f" **Epistemic:** {ep}\n")
    return "# CLAIMS\n\n" + "\n".join(out) + "\n"


def frames_md():
    return "# FRAMES\n\n- [[lib/frames/f-000010.png|f-000010]] · 00:00:10\n"


def build_base(root):
    lib = os.path.join(root, "lib")
    os.makedirs(os.path.join(lib, "frames"))
    os.makedirs(os.path.join(root, "80-agents", "agents-os"))
    open(os.path.join(root, "80-agents", "agents-os", "agents-os.md"), "w").close()
    open(os.path.join(lib, "frames", "f-000010.png"), "w").close()
    open(os.path.join(lib, "transcript.md"), "w", encoding="utf-8").write(TRANSCRIPT)
    with open(os.path.join(lib, "claims.jsonl"), "w", encoding="utf-8") as f:
        for c in CLAIMS:
            f.write(json.dumps(c) + "\n")
    open(os.path.join(lib, "rules.md"), "w", encoding="utf-8").write(
        "**R1** [00:10, c-0001]\n")
    open(os.path.join(lib, "CLAIMS.md"), "w", encoding="utf-8").write(claims_md(CLAIMS))
    open(os.path.join(lib, "FRAMES.md"), "w", encoding="utf-8").write(frames_md())
    return lib


def run(lib):
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
    tmp = tempfile.mkdtemp(prefix="cke-wiki-")
    base = build_base(tmp)
    ok = True
    ok &= expect("base navegable válida", base, True)

    def m_broken_link(d):
        p = os.path.join(d, "rules.md")
        open(p, "w", encoding="utf-8").write("ver [[lib/CLAIMS#c-9999|c-9999]]\n")
    ok &= expect("broken wikilink (heading inexistente)", variant(base, "bad-broken-link", m_broken_link), False, {"W02"})

    def m_missing_heading(d):
        open(os.path.join(d, "CLAIMS.md"), "w", encoding="utf-8").write(claims_md(CLAIMS, missing="c-0002"))
    ok &= expect("stale projection: heading de claim ausente", variant(base, "bad-missing-heading", m_missing_heading), False, {"W04"})

    def m_missing_block(d):
        p = os.path.join(d, "rules.md")
        open(p, "w", encoding="utf-8").write("ver [[lib/transcript#^s-999999|s-999999]]\n")
    ok &= expect("missing transcript block", variant(base, "bad-missing-block", m_missing_block), False, {"W03"})

    def m_missing_png(d):
        open(os.path.join(d, "FRAMES.md"), "w", encoding="utf-8").write(
            frames_md() + "- [[lib/frames/f-999999.png|f-999999]] · 99:99\n")
    ok &= expect("missing PNG", variant(base, "bad-missing-png", m_missing_png), False, {"W01"})

    def m_dup_anchor(d):
        p = os.path.join(d, "transcript.md")
        t = open(p, encoding="utf-8").read().replace("^s-000030", "^s-000010")
        open(p, "w", encoding="utf-8").write(t)
    ok &= expect("duplicate anchor", variant(base, "bad-dup-anchor", m_dup_anchor), False, {"W05"})

    def m_ambiguous_png(d):
        # mismo basename en OTRO capítulo del vault + link por basename
        other = os.path.join(os.path.dirname(d), "lib2", "frames")
        os.makedirs(other)
        open(os.path.join(other, "f-000010.png"), "w").close()
        open(os.path.join(d, "rules.md"), "w", encoding="utf-8").write("mira [[f-000010.png]]\n")
    ok &= expect("ambiguous frame path", variant(base, "bad-ambiguous-png", m_ambiguous_png), False, {"W07"})

    def m_stale_verdict(d):
        open(os.path.join(d, "CLAIMS.md"), "w", encoding="utf-8").write(claims_md(CLAIMS, wrong_verdict=True))
    ok &= expect("stale claims projection (verdict)", variant(base, "bad-stale-verdict", m_stale_verdict), False, {"W09"})

    def m_stale_statement(d):
        open(os.path.join(d, "CLAIMS.md"), "w", encoding="utf-8").write(claims_md(CLAIMS, wrong_statement=True))
    ok &= expect("stale claims projection (statement)", variant(base, "bad-stale-statement", m_stale_statement), False, {"W09"})

    def m_stale_epistemic(d):
        open(os.path.join(d, "CLAIMS.md"), "w", encoding="utf-8").write(claims_md(CLAIMS, wrong_epistemic=True))
    ok &= expect("stale claims projection (epistemic)", variant(base, "bad-stale-epistemic", m_stale_epistemic), False, {"W09"})

    def m_unbalanced(d):
        open(os.path.join(d, "rules.md"), "w", encoding="utf-8").write("ver [[lib/CLAIMS#c-0001|c-0001 y [[sin cerrar\n")
    ok &= expect("wikilink desequilibrado (anidado)", variant(base, "bad-unbalanced", m_unbalanced), False, {"W10"})

    def m_unseparated(d):
        p = os.path.join(d, "transcript.md")
        open(p, "w", encoding="utf-8").write(
            "# t\n\ns-000010 [00:00:10-00:00:20] texto uno ^s-000010\n"
            "s-000030 [00:00:30-00:00:40] texto dos ^s-000030\n")
    ok &= expect("anchors sin bloque propio (sin línea en blanco)", variant(base, "bad-unseparated", m_unseparated), False, {"W05"})

    shutil.rmtree(tmp)
    print("WIKILINK_SELFTEST =", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


def variant(base, name, mutate):
    dst = os.path.join(os.path.dirname(base), name)
    shutil.copytree(base, dst)
    mutate(dst)
    return dst


if __name__ == "__main__":
    main()
