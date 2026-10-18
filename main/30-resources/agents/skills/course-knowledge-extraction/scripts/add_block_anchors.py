#!/usr/bin/env python3
"""add_block_anchors.py — hace direccionables los segmentos de transcript.md.

Añade ` ^s-HHMMSS` al final de la línea de cada segmento (block id de Obsidian).
Idempotente: si el anchor ya existe, no toca la línea. No cambia el texto
transcrito ni las identidades de segmentos.

Uso:  add_block_anchors.py <transcript.md>
"""
import re, sys

pat = re.compile(r"^(s-\d{6}[a-z]?) \[\d{2}:\d{2}:\d{2}-\d{2}:\d{2}:\d{2}\] .+?( ?\^s-\d{6}[a-z]?)?$")


def main():
    path = sys.argv[1]
    lines = open(path, encoding="utf-8").read().splitlines()
    out, added, seen = [], 0, {}
    for line in lines:
        m = re.match(r"^(s-\d{6}[a-z]?) \[\d{2}:\d{2}:\d{2}-\d{2}:\d{2}:\d{2}\] ", line)
        if m:
            sid = m.group(1)
            if sid in seen:
                sys.exit(f"FATAL: segmento duplicado {sid}")
            seen[sid] = True
            if not line.rstrip().endswith("^" + sid):
                line = line.rstrip() + " ^" + sid
                added += 1
        out.append(line)
    open(path, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(f"anchors: {len(seen)} segmentos, {added} añadidos (idempotente)")


if __name__ == "__main__":
    main()
