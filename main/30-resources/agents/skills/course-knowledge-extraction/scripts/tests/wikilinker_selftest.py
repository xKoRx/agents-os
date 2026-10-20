#!/usr/bin/env python3
"""wikilinker_selftest.py — red-green del script wikilink_docs.py.

Derivado del incidente real de ch07 (2026-10-20): --all-tokens producía doble
anidación al re-enlazar tokens pegados a corchetes de cita (`[c-0001]` →
`[[[path|c-0001]]]`, 69 enlaces rotos) y destruía links dentro de backticks
(fuga de marcadores \x00N\x00). Contrato probado:

  1. citas de sólo tokens se absorben ([c-0001, c-0002] → links con '·')
  2. tokens pegados a '[' en citas mixtas ([c-0001 [ASR]]) NO se enlazan
     (texto plano válido, nunca [[[)
  3. links existentes (con corchete en el display o dentro de backticks)
     se preservan byte a byte
  4. idempotencia: first_run_output == second_run_output

Uso:  python3 wikilinker_selftest.py
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LINKER = os.path.join(HERE, "..", "wikilink_docs.py")

DOC = """Caso 1: display con corchete [[lib/CLAIMS#c-0001|c-0001 [ASR]]] y bare c-0002.

Caso 2: backticks con link `abierto [[lib/CLAIMS#c-0003|c-0003]] y cierro` y c-0004.

Caso 3: cita mixta [c-0005 [ASR]] y bare c-0006.

Caso 4: cita simple [c-0007], multi [c-0008, c-0009], de segmento [s-000010] y frame [f-000030].
"""


def run_linker(vault, lib, doc):
    r = subprocess.run([sys.executable, LINKER, vault, lib, doc],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(f"FAIL  linker rc={r.returncode}: {r.stderr.strip()[:120]}")
        return False
    return True


def main():
    tmp = tempfile.mkdtemp(prefix="cke-wikilinker-")
    vault = os.path.join(tmp, "vault")
    lib = os.path.join(vault, "lib")
    os.makedirs(os.path.join(lib, "frames"))
    os.makedirs(os.path.join(vault, "80-agents", "agents-os"))
    open(os.path.join(vault, "80-agents", "agents-os", "agents-os.md"), "w").close()
    open(os.path.join(lib, "frames", "f-000030.png"), "w").close()
    doc = os.path.join(lib, "doc.md")
    open(doc, "w", encoding="utf-8").write(DOC)

    ok = True
    if not run_linker(vault, lib, doc):
        ok = False
    first = open(doc, encoding="utf-8").read()

    # 4. idempotencia
    if not run_linker(vault, lib, doc):
        ok = False
    second = open(doc, encoding="utf-8").read()
    idem = first == second
    print(f"{'PASS' if idem else 'FAIL'}  idempotencia: first_run == second_run")
    ok &= idem

    def check(label, cond):
        nonlocal ok
        print(f"{'PASS' if cond else 'FAIL'}  {label}")
        ok &= bool(cond)

    # 1. absorción de citas de sólo tokens
    check("cita simple [c-0007] absorbida en link",
          "[[lib/CLAIMS#c-0007|c-0007]]" in first and "[c-0007]" not in first)
    check("cita multi [c-0008, c-0009] absorbida con separador '·'",
          "[[lib/CLAIMS#c-0008|c-0008]] · [[lib/CLAIMS#c-0009|c-0009]]" in first)
    check("cita de segmento [s-000010] absorbida",
          "[[lib/transcript#^s-000010|s-000010]]" in first)
    check("cita de frame [f-000030] absorbida",
          "[[lib/frames/f-000030.png|f-000030]]" in first)
    # 2. sin triple corchete / citas mixtas intactas
    check("sin doble anidación [[[ en todo el documento", "[[[" not in first)
    check("cita mixta [c-0005 [ASR]] preservada en texto plano",
          "[c-0005 [ASR]]" in first)
    # 3. preservación de links existentes
    check("link con corchete en display preservado",
          "[[lib/CLAIMS#c-0001|c-0001 [ASR]]]" in first)
    check("link dentro de backticks preservado (sin fuga de marcadores)",
          "`abierto [[lib/CLAIMS#c-0003|c-0003]] y cierro`" in first and "\x00" not in first)
    # bare tokens enlazados
    check("token bare c-0006 enlazado", "[[lib/CLAIMS#c-0006|c-0006]]" in first)

    shutil.rmtree(tmp)
    print("WIKILINKER_SELFTEST =", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
