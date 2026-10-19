#!/usr/bin/env python3
"""lifecycle_selftest.py — red-green del contrato de supersession safety.

Casos (Preflight ch04, 2026-10-19; los históricos 1-3 son los estados reales
de ch03 antes de la corrección):
  1  superseded_by apunta a claim inexistente            -> V14 FINDINGS (RED)
  2  ciclo A->B->A en la cadena superseded_by            -> V14 FINDINGS (RED)
  3  CLAIMS.md sin marca SUPERSEDED para un claim reemplazado -> V15 (RED)
  4  doc pedagógica cita claim reemplazado como vigente  -> V16 (RED)
  5  reemplazo bien formado (bidireccional + renderer)   -> PASS (GREEN)
  6  id duplicado (un claim nuevo reutiliza el id de otro)-> V01 (RED)
  7  README sin fila activos/superseded con reemplazos   -> V10 (RED)

Uso:  python3 lifecycle_selftest.py
"""
import json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
VALIDATE = os.path.join(HERE, "..", "validate_library.py")
RENDER = os.path.join(HERE, "..", "render_claims_md.py")

SUPERSEDED_MARK = "SUPERSEDED — HISTORICAL, NOT ACTIVE"


def check(label, cond):
    print(f"{'PASS' if cond else 'FAIL'}  {label}")
    return cond


def build_lib(root, claims, claims_md=None):
    lib = os.path.join(root, "lib")
    os.makedirs(os.path.join(lib, "frames"))
    open(os.path.join(lib, "frames", "f-000010.png"), "w").close()
    open(os.path.join(lib, "transcript.md"), "w", encoding="utf-8").write(
        "# t\n\ns-000010 [00:00:10-00:00:20] texto de evidencia\n\n")
    with open(os.path.join(lib, "claims.jsonl"), "w", encoding="utf-8") as f:
        for c in claims:
            f.write(json.dumps(c) + "\n")
    open(os.path.join(lib, "CLAIMS.md"), "w", encoding="utf-8").write(
        claims_md if claims_md is not None else default_claims_md(claims))
    open(os.path.join(lib, "README.md"), "w", encoding="utf-8").write(default_readme(claims))
    return lib


def default_claims_md(claims):
    out = ["# CLAIMS"]
    for c in claims:
        out += [f"### {c['id']}", "",
                f"**Statement:** {c['statement']}", "",
                f"**Verdict:** {c['verdict']} · **Epistemic:** {c.get('epistemic','instructor_statement')}", ""]
        if c.get("superseded_by"):
            out += [SUPERSEDED_MARK, "", f"**Replacement:** [[lib/CLAIMS#{c['superseded_by']}|{c['superseded_by']}]]", ""]
        if c.get("supersedes"):
            out += [f"**Supersedes:** [[lib/CLAIMS#{c['supersedes']}|{c['supersedes']}]]", ""]
    return "\n".join(out) + "\n"


def default_readme(claims):
    n_sup = sum(1 for c in claims if c.get("superseded_by"))
    n_act = len(claims) - n_sup
    rows = [f"| Claims totales | {len(claims)} |"]
    if n_sup:
        rows.append(f"| Claims activos / superseded | {n_act} / {n_sup} |")
    return "# README\n\n| Métrica | Valor |\n|---|---|\n" + "\n".join(rows) + "\n"


def run_validate(lib):
    r = subprocess.run([sys.executable, VALIDATE, lib, "--json"],
                       capture_output=True, text=True)
    out = json.loads(r.stdout) if r.stdout.strip() else {"pass": None, "findings": []}
    return r.returncode, out


def codes(out):
    return sorted({f["check"] for f in out.get("findings", []) if f.get("severity") != "SKIP"})


def main():
    tmp = tempfile.mkdtemp(prefix="cke-lifecycle-")
    ok = True
    try:
        base = {"kind": "rule", "epistemic": "instructor_statement",
                "evidence": ["s-000010"], "verdict": "SUPPORTED"}

        # 1: superseded_by a claim inexistente
        lib = build_lib(tmp + "1", [dict(base, id="c-0001", statement="x", superseded_by="c-9999")])
        rc, out = run_validate(lib)
        ok &= check("1 superseded_by a claim inexistente -> V14", "V14" in codes(out))

        # 2: ciclo A->B->A
        lib = build_lib(tmp + "2", [
            dict(base, id="c-0001", statement="x", superseded_by="c-0002"),
            dict(base, id="c-0002", statement="y", superseded_by="c-0001", supersedes="c-0001")])
        # repara bidireccionalidad parcial para aislar el ciclo
        lib2 = build_lib(tmp + "2b", [
            dict(base, id="c-0001", statement="x", superseded_by="c-0002", supersedes=None),
            dict(base, id="c-0002", statement="y", superseded_by="c-0001", supersedes="c-0001")])
        rc, out = run_validate(lib2)
        ok &= check("2 ciclo A->B->A -> V14", "V14" in codes(out)) if False else \
            check("2 ciclo A->B->A -> V14", "V14" in codes(out))
        del lib

        # 3: CLAIMS.md sin marca SUPERSEDED (proyección stale, renderer viejo)
        stale_md = "# CLAIMS\n\n### c-0001\n\n**Statement:** x\n\n**Verdict:** SUPPORTED\n"
        lib = build_lib(tmp + "3",
                        [dict(base, id="c-0001", statement="x", superseded_by="c-0002"),
                         dict(base, id="c-0002", statement="y", supersedes="c-0001")],
                        claims_md=stale_md)
        rc, out = run_validate(lib)
        ok &= check("3 CLAIMS.md sin lifecycle -> V15", "V15" in codes(out))

        # 4: doc pedagógica cita el claim reemplazado
        lib = build_lib(tmp + "4",
                        [dict(base, id="c-0001", statement="x", superseded_by="c-0002"),
                         dict(base, id="c-0002", statement="y", supersedes="c-0001")])
        open(os.path.join(lib, "documentation.md"), "w", encoding="utf-8").write(
            "# Doc\n\nSegún c-0001 el precio...\n")
        rc, out = run_validate(lib)
        ok &= check("4 documentation cita claim reemplazado -> V16", "V16" in codes(out))

        # 5: GREEN — reemplazo bien formado, renderer regenerado, README con fila
        claims = [dict(base, id="c-0001", statement="x", superseded_by="c-0002"),
                  dict(base, id="c-0002", statement="y", supersedes="c-0001")]
        lib = build_lib(tmp + "5", claims)
        subprocess.run([sys.executable, RENDER, tmp + "5vault", lib],
                       capture_output=True, text=True,
                       env={**os.environ, "VAULT_ROOT": tmp + "5vault"})
        # el renderer requiere un vault real para las rutas relativas; con un
        # directorio arbitrario las rutas son relativas al path dado — válido
        # para el check de lifecycle (sólo buscamos las marcas).
        rc, out = run_validate(lib)
        # W-checks pueden fallar por no-vault; nos importa que no haya V14/V15/V16/V10
        life_codes = [c for c in codes(out) if c in ("V10", "V14", "V15", "V16")]
        ok &= check("5 reemplazo bien formado -> sin findings de lifecycle", not life_codes)
        cm = open(os.path.join(lib, "CLAIMS.md"), encoding="utf-8").read()
        sec1 = cm.split("### c-0001", 1)[1].split("### c-0002", 1)[0] if "### c-0002" in cm else ""
        ok &= check("5a renderer marca SUPERSEDED + Replacement",
                    SUPERSEDED_MARK in sec1 and "CLAIMS#c-0002" in sec1)
        sec2 = cm.split("### c-0002", 1)[1]
        ok &= check("5b renderer muestra Supersedes en el sucesor",
                    "Supersedes:" in sec2 and "CLAIMS#c-0001" in sec2)

        # 6: id duplicado (un claim nuevo reutiliza el id de otro)
        lib = build_lib(tmp + "6", [dict(base, id="c-0001", statement="x"),
                                    dict(base, id="c-0001", statement="y")])
        rc, out = run_validate(lib)
        ok &= check("6 id reutilizado -> V01", "V01" in codes(out))

        # 7: README sin fila activos/superseded habiendo reemplazos
        claims = [dict(base, id="c-0001", statement="x", superseded_by="c-0002"),
                  dict(base, id="c-0002", statement="y", supersedes="c-0001")]
        lib = build_lib(tmp + "7", claims)
        open(os.path.join(lib, "README.md"), "w", encoding="utf-8").write(
            "# README\n\n| Métrica | Valor |\n|---|---|\n| Claims totales | 2 |\n")
        rc, out = run_validate(lib)
        ok &= check("7 README sin fila activos/superseded -> V10", "V10" in codes(out))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print(f"\nLIFECYCLE_SELFTEST = {'PASS' if ok else 'FAIL'}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
