#!/usr/bin/env python3
"""add_block_anchors.py — hace direccionables los segmentos de transcript.md.

Añade ` ^s-HHMMSS` al final de la línea de cada segmento (block id de Obsidian)
y garantiza que cada segmento sea un BLOQUE Markdown independiente: en Obsidian,
un block id sólo es resolvable al final de un párrafo; dos segmentos en líneas
consecutivas dejan los anchors intermedios como texto literal. Por eso este
script inserta una línea en blanco antes y después de cada segmento cuando la
línea vecina no es ya un límite de párrafo (vacía, EOF o heading).

Idempotente: re-ejecutar sobre un transcript ya procesado produce salida
idéntica byte a byte. No cambia el texto transcrito ni las identidades de
segmentos; el whitespace entre bloques es formato, no contenido.

Uso:  add_block_anchors.py <transcript.md>
"""
import re, sys

SEG = re.compile(r"^(s-\d{6}[a-z]?) \[\d{2}:\d{2}:\d{2}-\d{2}:\d{2}:\d{2}\] ")
HEADING = re.compile(r"^#{1,6} ")


def is_paragraph_break(line):
    """Una línea vecina que ya termina/abre párrafo: vacía, EOF o heading."""
    return line is None or line.strip() == "" or HEADING.match(line)


def main():
    path = sys.argv[1]
    lines = open(path, encoding="utf-8").read().splitlines()
    out, added, separated, seen = [], 0, 0, {}
    for i, line in enumerate(lines):
        m = SEG.match(line)
        if m:
            sid = m.group(1)
            if sid in seen:
                sys.exit(f"FATAL: segmento duplicado {sid}")
            seen[sid] = True
            if not line.rstrip().endswith("^" + sid):
                line = line.rstrip() + " ^" + sid
                added += 1
            # bloque independiente: línea en blanco antes si la anterior no es
            # límite de párrafo, y después si la siguiente no lo es.
            if out and not is_paragraph_break(out[-1]):
                out.append("")
                separated += 1
            out.append(line)
            nxt = lines[i + 1] if i + 1 < len(lines) else None
            if not is_paragraph_break(nxt):
                out.append("")
                separated += 1
            continue
        out.append(line)
    open(path, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(f"anchors: {len(seen)} segmentos, {added} añadidos, "
          f"{separated} separaciones de párrafo (idempotente)")


if __name__ == "__main__":
    main()
