#!/usr/bin/env python3
"""render_frames_md.py — inventario navegable de frames/ (FRAMES.md).

Generado desde el directorio frames/ + el índice inverso de claims. Bytes
estables ante inputs idénticos (sin fecha del día: misma entrada => mismos
bytes cualquier día). Los frames sin claims quedan como evidencia contextual
(no se fuerzan relaciones).

Clasificación base/bajo demanda: la autoridad es el manifiesto de capturas
reales `frames/.base_frames` (un stem `f-HHMMSS` por línea, `#` comentarios),
escrito por quien ejecutó las capturas. El renderer NO deduce la clase desde
el nombre (un frame bajo demanda puede caer en :59 y un base puede ser el fin
parcial del último minuto). Sin manifiesto falla cerrado.

Uso:  render_frames_md.py <vault_root> <library_dir>
"""
import json, os, sys


def read_base_manifest(frames_dir):
    path = os.path.join(frames_dir, ".base_frames")
    if not os.path.exists(path):
        sys.exit(f"FATAL: falta {path} — declara las capturas base ejecutadas "
                 f"(un f-HHMMSS por línea); el renderer no adivina clases desde nombres")
    base = set()
    for line in open(path, encoding="utf-8"):
        line = line.split("#", 1)[0].strip()
        if line:
            base.add(line)
    return base


def main():
    vault, lib = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    rel = os.path.relpath(lib, vault)
    frames = sorted(f for f in os.listdir(os.path.join(lib, "frames")) if f.endswith(".png"))
    base_manifest = read_base_manifest(os.path.join(lib, "frames"))
    unknown = sorted(base_manifest - {f[:-4] for f in frames})
    if unknown:
        sys.exit(f"FATAL: el manifiesto declara frames inexistentes: {unknown}")

    cited = {}
    for line in open(os.path.join(lib, "claims.jsonl"), encoding="utf-8"):
        if not line.strip():
            continue
        c = json.loads(line)
        for e in c["evidence"]:
            if e.startswith("f-"):
                cited.setdefault(e, []).append(c["id"])

    L = ["# FRAMES — inventario navegable", ""]
    L.append("> Generado deterministamente por `render_frames_md.py` desde `frames/` +"
             " `frames/.base_frames` (autoridad de la clase base)."
             " Timestamp codificado en el nombre (f-HHMMSS.png)."
             " \"Contextual\" = sin claims asociados; no se fuerzan relaciones.")
    L.append("")
    for f in frames:
        stem = f[:-4]
        h, m, s = int(stem[2:4]), int(stem[4:6]), int(stem[6:8])
        ts = f"{h:02d}:{m:02d}:{s:02d}"
        kind = "base (fin de minuto)" if stem in base_manifest else "bajo demanda"
        who = ", ".join(f"[[{rel}/CLAIMS#{cid}|{cid}]]" for cid in cited.get(stem, []))
        L.append(f"- [[{rel}/frames/{f}|{stem}]] · {ts} · {kind} · "
                 + (f"citado por: {who}" if who else "contextual"))
    out = os.path.join(lib, "FRAMES.md")
    open(out, "w", encoding="utf-8").write("\n".join(L) + "\n")
    n_base = sum(1 for f in frames if f[:-4] in base_manifest)
    print(f"FRAMES.md: {len(frames)} frames ({n_base} base por manifiesto, "
          f"{len(cited)} citados) -> {out}")


if __name__ == "__main__":
    main()
