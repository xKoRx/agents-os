#!/usr/bin/env python3
"""wikilink_docs.py — convierte referencias de claim/frame/segmento en wikilinks.

Modos:
  --all-tokens  : transforma todo token c-/f-/s- del documento (docs pedagógicos)
  --bracketed   : sólo tokens dentro de corchetes [...] (registros/prosa)

Nombres en .deprecated_frame_names nunca se enlazan (historical_invalid_name).
Los tokens ya enlazados o dentro de [[...]] no se re-procesan. Idempotente.

Uso:  wikilink_docs.py <vault_root> <library_dir> <doc.md> [--bracketed]
"""
import os, re, sys

CID = re.compile(r"(?<!\[)\bc-\d{4}\b")
FID = re.compile(r"(?<!\[)\bf-\d{6}\b")
SID = re.compile(r"(?<!\[)\bs-\d{6}[a-z]?\b")
WIKI = re.compile(r"\[\[[^\]]+\]\]")
# cita simple de uno o más tokens solos: [c-0001] / [c-0001, c-0002] — los
# corchetes se absorben en el link (colapsa la doble anidación [[[...]]])
CITE = re.compile(r"\[((?:[cfs]-\d{4,6}[a-z]?(?:,\s*)?)+)\]")


def protect(text):
    """Sustituye regiones a no tocar por marcadores y devuelve la lista.

    El código inline se protege ANTES que los wikilinks: un link dentro de
    backticks debe quedar dentro de UNA sola región salvada (proteger el link
    primero y el código después anidaba marcadores y `restore` dejaba basura
    \x00N\x00, destruyendo el link)."""
    saved = []

    def keep(m):
        saved.append(m.group(0))
        return f"\x00{len(saved)-1}\x00"

    text = re.sub(r"`[^`]*`", keep, text)  # código inline
    text = WIKI.sub(keep, text)          # wikilinks existentes
    return text, saved


def restore(text, saved):
    for _ in range(10):
        if "\x00" not in text:
            break
        text = re.sub(r"\x00(\d+)\x00", lambda m: saved[int(m.group(1))], text)
    return text


def main():
    vault, lib, doc = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]), sys.argv[3]
    mode = "--bracketed" if "--bracketed" in sys.argv else "--all-tokens"
    rel = os.path.relpath(lib, vault)
    dep = set()
    dep_path = os.path.join(lib, ".deprecated_frame_names")
    if os.path.exists(dep_path):
        dep = {l.split("#", 1)[0].strip() for l in open(dep_path, encoding="utf-8") if l.split("#", 1)[0].strip()}

    text = open(doc, encoding="utf-8").read()
    text, saved = protect(text)

    def link_c(m):
        t = m.group(0)
        return f"[[{rel}/CLAIMS#{t}|{t}]]"

    def link_f(m):
        t = m.group(0)
        if t in dep:
            return t
        return f"[[{rel}/frames/{t}.png|{t}]]"

    def link_s(m):
        t = m.group(0)
        return f"[[{rel}/transcript#^{t}|{t}]]"

    if mode == "--all-tokens":
        def link_cite(m):
            # [c-0001, c-0002] -> links con separador '·' (corchetes absorbidos)
            toks = re.findall(r"[cfs]-\d{4,6}[a-z]?", m.group(1))
            outs = []
            for t in toks:
                if t.startswith("c-"):
                    outs.append(f"[[{rel}/CLAIMS#{t}|{t}]]")
                elif t.startswith("f-"):
                    outs.append(t if t in dep else f"[[{rel}/frames/{t}.png|{t}]]")
                else:
                    outs.append(f"[[{rel}/transcript#^{t}|{t}]]")
            return " · ".join(outs)
        text = CITE.sub(link_cite, text)
        text = CID.sub(link_c, text)
        text = FID.sub(link_f, text)
        text = SID.sub(link_s, text)
    else:
        def bracket(m):
            inner = m.group(0)
            inner = CID.sub(link_c, inner)
            inner = FID.sub(link_f, inner)
            inner = SID.sub(link_s, inner)
            return inner
        text = re.sub(r"\[[^\[\]\n]+\]", bracket, text)

    text = restore(text, saved)
    open(doc, "w", encoding="utf-8").write(text)
    print(f"{os.path.basename(doc)} ({mode}) enlazado")


if __name__ == "__main__":
    main()
