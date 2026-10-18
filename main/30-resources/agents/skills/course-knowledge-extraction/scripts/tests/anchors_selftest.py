#!/usr/bin/env python3
"""anchors_selftest.py — red-green de add_block_anchors.py (contrato v1.2+).

Contrato: cada segmento del transcript queda como BLOQUE Markdown independiente
(anchor `^s-` al final de su propio párrafo, con línea en blanco/heading antes
y después), texto y timestamps intactos, idempotente byte a byte.

Casos:
  1  transcript crudo (segmentos consecutivos, sin anchors) -> anchors + separación
  2  texto y timestamps preservados byte a byte fuera del whitespace añadido
  3  idempotencia: segunda ejecución produce los mismos bytes
  4  anchors ya presentes -> 0 añadidos, sólo separa lo que falte
  5  segmento antes de un heading no inserta línea en blanco redundante
  6  segmento duplicado -> FATAL (exit != 0)
  7  el validador acepta el resultado (W05 verde sobre el vault mínimo)

Uso:  python3 anchors_selftest.py
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ANCHORS = os.path.join(HERE, "..", "add_block_anchors.py")
VALIDATOR = os.path.join(HERE, "..", "validate_library.py")

RAW = """# transcript

s-000010 [00:00:10-00:00:20] texto uno
s-000030 [00:00:30-00:00:40] texto dos
s-000040 [00:00:40-00:00:50] texto tres

## notas

s-000050 [00:00:50-00:01:00] texto cuatro
"""

EXPECTED = """# transcript

s-000010 [00:00:10-00:00:20] texto uno ^s-000010

s-000030 [00:00:30-00:00:40] texto dos ^s-000030

s-000040 [00:00:40-00:00:50] texto tres ^s-000040

## notas

s-000050 [00:00:50-00:01:00] texto cuatro ^s-000050
"""


def run_anchors(path):
    return subprocess.run([sys.executable, ANCHORS, path], capture_output=True, text=True)


def check(label, cond):
    print(f"{'PASS' if cond else 'FAIL'}  {label}")
    return cond


def main():
    tmp = tempfile.mkdtemp(prefix="cke-anchors-")
    ok = True
    try:
        t = os.path.join(tmp, "transcript.md")
        open(t, "w", encoding="utf-8").write(RAW)

        r = run_anchors(t)
        got = open(t, encoding="utf-8").read()
        ok &= check("1 anchors + separación de párrafos", r.returncode == 0 and got == EXPECTED)

        def normalized(s):
            out_l = []
            for l in s.splitlines():
                l = re.sub(r" \^s-\d{6}[a-z]?$", "", l.rstrip())
                if l.strip():
                    out_l.append(l)
            return out_l
        ok &= check("2 texto/timestamps preservados", normalized(got) == normalized(RAW))

        r2 = run_anchors(t)
        ok &= check("3 idempotente (2ª pasada byte-idéntica)",
                    r2.returncode == 0 and open(t, encoding="utf-8").read() == EXPECTED)

        t2 = os.path.join(tmp, "pre-anchored.md")
        open(t2, "w", encoding="utf-8").write(
            "s-000010 [00:00:10-00:00:20] texto uno ^s-000010\n"
            "s-000030 [00:00:30-00:00:40] texto dos ^s-000030\n")
        r3 = run_anchors(t2)
        got3 = open(t2, encoding="utf-8").read()
        ok &= check("4 anchors existentes: 0 añadidos, separa lo que falte",
                    r3.returncode == 0 and "0 añadidos" in r3.stdout
                    and got3.count("\n\n") >= 1 and "^s-000010" in got3)

        t3 = os.path.join(tmp, "heading.md")
        open(t3, "w", encoding="utf-8").write(
            "s-000010 [00:00:10-00:00:20] texto uno\n\n## notas\n")
        r4 = run_anchors(t3)
        got4 = open(t3, encoding="utf-8").read()
        ok &= check("5 heading tras segmento: sin línea en blanco redundante",
                    r4.returncode == 0 and got4 ==
                    "s-000010 [00:00:10-00:00:20] texto uno ^s-000010\n\n## notas\n")

        t4 = os.path.join(tmp, "dup.md")
        open(t4, "w", encoding="utf-8").write(
            "s-000010 [00:00:10-00:00:20] a\ns-000010 [00:00:15-00:00:20] b\n")
        r5 = run_anchors(t4)
        ok &= check("6 segmento duplicado -> FATAL", r5.returncode != 0)

        # 7: el validador (W05) acepta un transcript con este formato
        v = os.path.join(tmp, "vault")
        lib = os.path.join(v, "lib")
        os.makedirs(os.path.join(lib, "frames"))
        os.makedirs(os.path.join(v, "80-agents", "agents-os"))
        open(os.path.join(v, "80-agents", "agents-os", "agents-os.md"), "w").close()
        shutil.copy(t, os.path.join(lib, "transcript.md"))
        open(os.path.join(lib, "frames", "f-000010.png"), "w").close()
        with open(os.path.join(lib, "claims.jsonl"), "w", encoding="utf-8") as f:
            f.write('{"id":"c-0001","minute":0,"kind":"rule","statement":"x",'
                    '"evidence":["s-000010"],"verdict":"SUPPORTED","notes":"",'
                    '"epistemic":"instructor_statement"}\n')
        rv = subprocess.run([sys.executable, VALIDATOR, lib, "--duration-seconds", "120", "--json"],
                            capture_output=True, text=True)
        import json
        out = json.loads(rv.stdout)
        ok &= check("7 validador: W05 verde sobre el formato producido",
                    rv.returncode == 0 and out["pass"])
    finally:
        shutil.rmtree(tmp)
    print("ANCHORS_SELFTEST =", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
