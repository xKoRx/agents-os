#!/usr/bin/env python3
"""render_frames_md.py — inventario navegable de frames/ (FRAMES.md).

Generado desde el directorio frames/ + el índice inverso de claims. Bytes
estables ante inputs idénticos. Los frames sin claims quedan como evidencia
contextual (no se fuerzan relaciones).

Uso:  render_frames_md.py <vault_root> <library_dir>
"""
import json, os, re, sys, datetime


def main():
    vault, lib = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    rel = os.path.relpath(lib, vault)
    frames = sorted(f for f in os.listdir(os.path.join(lib, "frames")) if f.endswith(".png"))
    cited = {}
    for line in open(os.path.join(lib, "claims.jsonl"), encoding="utf-8"):
        if not line.strip():
            continue
        c = json.loads(line)
        for e in c["evidence"]:
            if e.startswith("f-"):
                cited.setdefault(e, []).append(c["id"])

    L = ["# FRAMES — inventario navegable", ""]
    L.append(f"> Generado deterministamente por `render_frames_md.py`"
             f" ({datetime.date.today().isoformat()})."
             f" Timestamp codificado en el nombre (f-HHMMSS.png)."
             f" \"Contextual\" = sin claims asociados; no se fuerzan relaciones.")
    L.append("")
    base_re = re.compile(r"^f-\d{6}59\.png$")
    for f in frames:
        stem = f[:-4]
        h, m, s = int(stem[2:4]), int(stem[4:6]), int(stem[6:8])
        ts = f"{h:02d}:{m:02d}:{s:02d}"
        kind = "base (fin de minuto)" if base_re.match(f) or stem == "f-001703" and h == 0 and m == 17 else "bajo demanda"
        who = ", ".join(f"[[{rel}/CLAIMS#{cid}|{cid}]]" for cid in cited.get(stem, []))
        L.append(f"- [[{rel}/frames/{f}|{stem}]] · {ts} · {kind} · "
                 + (f"citado por: {who}" if who else "contextual"))
    out = os.path.join(lib, "FRAMES.md")
    open(out, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"FRAMES.md: {len(frames)} frames ({len(cited)} citados) -> {out}")


if __name__ == "__main__":
    main()
