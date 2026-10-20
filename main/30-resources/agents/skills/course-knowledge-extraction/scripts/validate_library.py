#!/usr/bin/env python3
"""validate_library.py — validador determinista de bibliotecas course-knowledge-extraction.

Uso:
    validate_library.py <library_dir> [--duration-seconds N] [--json]

Chequeos (V01..V12, el número = hallazgo que cierra):
  V01  ids de claim únicos y con formato c-NNNN
  V02  ids de transcript únicos; toda evidencia s- resuelve
  V03  todo frame citado (claims + docs) existe físicamente
  V04  filenames de frame con HHMMSS parseable (no horas imposibles)
  V05  timestamp del frame dentro de la duración del source
  V06  evidence arrays no vacíos y con refs que resuelven (s- | f-)
  V07  visual_observation => >=1 frame en evidence (provenance visual)
  V08  visual_hint => >=1 frame en evidence; y visual_hint.second dentro de
       la duración de la fuente (si --duration-seconds: second es segundos
       reales, jamás HHMMSS pegado — defecto real ch05)
  V09  veredictos dentro del vocabulario SUPPORTED|UNCERTAIN|UNVERIFIED
  V10  conteos del README == conteos reales de los artefactos
  V11  referencias c-/f-/s- en los .md resuelven (nombres históricos
       invalidados se declaran en <library>/.deprecated_frame_names)
  V12  ningún claim UNCERTAIN/UNVERIFIED citado en documentation.md como hecho
  V14  integridad de supersession: superseded_by/supersedes apuntan a claims
       reales, sin ciclos ni auto-reemplazo, y la relación es bidireccional
  V15  CLAIMS.md muestra el lifecycle: todo claim con superseded_by aparece
       como "SUPERSEDED — HISTORICAL, NOT ACTIVE" con Replacement navegable
  V16  los documentos pedagógicos no citan claims reemplazados como evidencia
       vigente (la discusión histórica vive en AMENDMENTS/review-notes)

El validador NO corrige nada y NO juzga verdad semántica: detecta; la verdad
la establecen los revisores. Exit 0 = PASS, 1 = FINDINGS, 2 = uso/IO.
"""
import argparse, json, os, re, sys

FRAME_RE = re.compile(r"^f-(\d{2})(\d{2})(\d{2})(?:\.png)?$")
CID_RE = re.compile(r"^c-\d{4}$")
SID_RE = re.compile(r"^s-\d{6}[a-z]?$")
VERDICTS = {"SUPPORTED", "UNCERTAIN", "UNVERIFIED"}
DOCS = ["documentation.md", "rules.md", "concepts.md", "examples.md",
        "review-notes.md", "study-guide.md", "README.md",
        "CLAIMS.md", "FRAMES.md", "OPEN-QUESTIONS.md", "AMENDMENTS.md"]


def hhmmss_to_s(name):
    m = FRAME_RE.match(name)
    if not m:
        return None
    h, mi, s = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if m.group(2) > "59" or m.group(3) > "59":
        return None
    return h * 3600 + mi * 60 + s


WIKI_RE = re.compile(r"!?\[\[([^\]|#^]+)(#[^\]|]*)?(?:\|([^\]]*))?\]\]")


def find_vault_root(start):
    d = os.path.dirname(os.path.abspath(start))
    for _ in range(8):
        if os.path.exists(os.path.join(d, "80-agents", "agents-os", "agents-os.md")):
            return d
        nxt = os.path.dirname(d)
        if nxt == d:
            return None
        d = nxt
    return None


def check_wiki_targets(text, source_label, vault, rel_check_dir, bad):
    """W01/W02/W03/W07: cada wikilink resuelve a archivo, heading o block id;
    los links a .png exigen ruta completa (nada de basename ambiguo)."""
    for m in WIKI_RE.finditer(text):
        target, anchor = m.group(1).strip(), (m.group(2) or "").strip()
        full = m.group(0)
        if target.endswith(".png") and "/" not in target:
            bad("W07", f"{source_label}: link a PNG sin ruta completa (ambiguo entre capítulos): {full}")
            continue
        cand = os.path.join(vault, target) if vault else target
        path = None
        for c in (cand, cand + ".md"):
            if os.path.exists(c):
                path = c
                break
        if path is None:
            bad("W01", f"{source_label}: wikilink a destino inexistente: {full}")
            continue
        if anchor:
            body = open(path, encoding="utf-8", errors="replace").read()
            if anchor.startswith("#^"):
                bid = anchor[2:]
                if not re.search(r"\^" + re.escape(bid) + r"\b", body):
                    bad("W03", f"{source_label}: block id inexistente en {os.path.basename(path)}: {full}")
            else:
                head = anchor[1:].strip()
                if not re.search(r"^#+\s+" + re.escape(head) + r"\s*$", body, re.M):
                    bad("W02", f"{source_label}: heading inexistente en {os.path.basename(path)}: {full}")


def check_wiki_balance(text, source_label, bad):
    """W10: los wikilinks del documento están equilibrados — sin `[[` sin
    cerrar, sin `]]` huérfano, sin anidamiento. Detecta Markdown mal formado
    tras la transformación de citas a wikilinks."""
    for ln_no, line in enumerate(text.splitlines(), 1):
        i, open_wl, err = 0, False, None
        while i <= len(line) - 2:
            two = line[i:i + 2]
            if two == "[[":
                if open_wl:
                    err = "wikilink anidado sin cerrar"
                    break
                open_wl = True
                i += 2
            elif two == "]]":
                if not open_wl:
                    err = "']]' sin apertura"
                    break
                open_wl = False
                i += 2
            else:
                i += 1
        if err is None and open_wl:
            err = "wikilink sin cerrar"
        if err:
            bad("W10", f"{source_label}:{ln_no}: {err}: {line.strip()[:90]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("library")
    ap.add_argument("--duration-seconds", type=float, default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    lib = args.library
    findings = []  # (check, severity, message)

    def bad(check, msg):
        findings.append((check, "ERROR", msg))

    # --- recursos base
    claims_path = os.path.join(lib, "claims.jsonl")
    transcript_path = os.path.join(lib, "transcript.md")
    frames_dir = os.path.join(lib, "frames")
    if not (os.path.exists(claims_path) and os.path.exists(transcript_path) and os.path.isdir(frames_dir)):
        print(f"FATAL: faltan claims.jsonl/transcript.md/frames/ en {lib}")
        sys.exit(2)

    claims = []
    for i, line in enumerate(open(claims_path, encoding="utf-8"), 1):
        line = line.strip()
        if not line:
            continue
        try:
            claims.append(json.loads(line))
        except json.JSONDecodeError as e:
            bad("V01", f"claims.jsonl línea {i} no es JSON válido: {e}")

    t_text = open(transcript_path, encoding="utf-8").read()
    sids = re.findall(r"^(s-\d{6}[a-z]?) \[", t_text, re.M)
    sid_set = set(sids)
    if len(sid_set) != len(sids):
        dupes = sorted({s for s in sids if sids.count(s) > 1})
        bad("V02", f"ids de transcript duplicados: {dupes}")

    frames = {f for f in os.listdir(frames_dir) if f.endswith(".png")}
    dur = args.duration_seconds
    if dur is None:
        ends = [int(h) * 3600 + int(m) * 60 + int(s) for _, _, _, h, m, s in
                re.findall(r"\[(\d{2}):(\d{2}):(\d{2})-(\d{2}):(\d{2}):(\d{2})\]", t_text)]
        dur = max(ends) if ends else None

    deprecated = set()
    dep_path = os.path.join(lib, ".deprecated_frame_names")
    if os.path.exists(dep_path):
        for line in open(dep_path, encoding="utf-8"):
            line = line.split("#", 1)[0].strip()
            if line:
                deprecated.add(line)

    # --- V01 ids
    seen = {}
    for c in claims:
        cid = c.get("id", "")
        if not CID_RE.match(str(cid)):
            bad("V01", f"id inválido: {cid!r}")
        seen[cid] = seen.get(cid, 0) + 1
    for cid, n in seen.items():
        if n > 1:
            bad("V01", f"id duplicado: {cid} ({n}x)")

    # --- V02/V06/V07/V08/V09 por claim
    vis_no_frame, hint_no_frame, hint_out_of_duration = [], [], []
    for c in claims:
        cid = c.get("id", "?")
        ev = c.get("evidence")
        if not isinstance(ev, list) or not ev:
            bad("V06", f"{cid}: evidence vacío o ausente")
            ev = []
        for e in ev:
            if e.startswith("s-"):
                if e not in sid_set:
                    bad("V02", f"{cid}: evidencia de transcript inexistente: {e}")
            elif e.startswith("f-"):
                if e + ".png" not in frames:
                    bad("V03", f"{cid}: frame citado inexistente: {e}.png")
            else:
                bad("V06", f"{cid}: ref de evidence con formato desconocido: {e}")
        has_frame = any(e.startswith("f-") for e in ev)
        if c.get("epistemic") == "visual_observation" and not has_frame:
            vis_no_frame.append(cid)
        if ("visual_hint" in c and not has_frame
                and c.get("epistemic") != "instructor_statement"):
            # un visual_hint sobre sustancia hablada (instructor_statement) es
            # contextual: señala dónde mirar, no exige frame. En cualquier otra
            # epistemic, un hint sin frame rompe la trazabilidad visual.
            hint_no_frame.append(cid)
        vh = c.get("visual_hint")
        if isinstance(vh, dict) and dur is not None:
            sec = vh.get("second")
            # defecto real ch05 (DV-04): el extractor escribió el timestamp
            # HHMMSS como segundos crudos (p.ej. 1635 por 16:35 -> 995 s).
            # visual_hint.second es SIEMPRE segundos reales del video.
            if isinstance(sec, (int, float)) and not (0 <= sec < dur):
                hint_out_of_duration.append((cid, sec))
        if c.get("verdict") not in VERDICTS:
            bad("V09", f"{cid}: veredicto fuera de vocabulario: {c.get('verdict')!r}")
        if c.get("epistemic") == "model_inference" and c.get("verdict") == "SUPPORTED":
            bad("V13", f"{cid}: model_inference con SUPPORTED — requiere adjudicación semántica explícita "
                       f"(instructor_statement vs incertidumbre); no publicar inferencia como conocimiento del curso")
    if vis_no_frame:
        bad("V07", f"visual_observation sin frame en evidence ({len(vis_no_frame)}): {vis_no_frame}")
    if hint_no_frame:
        bad("V08", f"visual_hint sin frame en evidence ({len(hint_no_frame)}): {hint_no_frame}")
    if hint_out_of_duration:
        bad("V08", f"visual_hint.second fuera de la duración de la fuente ({len(hint_out_of_duration)}): "
                   f"{hint_out_of_duration} — second es en segundos reales, jamás HHMMSS pegado")

    # --- V04/V05 nombres de frame del directorio
    for f in sorted(frames):
        ts = hhmmss_to_s(f)
        if ts is None:
            bad("V04", f"nombre de frame no parseable como f-HHMMSS.png: {f}")
            continue
        if dur is not None and ts > dur:
            bad("V05", f"frame {f} (= {ts}s) fuera de la duración del source ({dur}s)"
                       f" — ¿horas en lugar de minutos?")

    # --- V10/V11 README y docs
    readme_path = os.path.join(lib, "README.md")
    if os.path.exists(readme_path):
        rd = open(readme_path, encoding="utf-8").read()
        n_rules = len(re.findall(r"^\*\*R\d+", open(os.path.join(lib, "rules.md"), encoding="utf-8").read(), re.M)) if os.path.exists(os.path.join(lib, "rules.md")) else 0
        n_concepts = len(re.findall(r"^## ", open(os.path.join(lib, "concepts.md"), encoding="utf-8").read(), re.M)) if os.path.exists(os.path.join(lib, "concepts.md")) else 0
        n_examples = len(re.findall(r"^## E\d+", open(os.path.join(lib, "examples.md"), encoding="utf-8").read(), re.M)) if os.path.exists(os.path.join(lib, "examples.md")) else 0
        # ACTIVE KNOWLEDGE = claims SIN superseded_by. Los veredictos que
        # publica el README cuentan conocimiento VIGENTE; los superseded se
        # declaran aparte (la fila activos/superseded es obligatoria cuando
        # hay reemplazos, así los conteos distinguen registros, activos e
        # históricos).
        active = [c for c in claims if not c.get("superseded_by")]
        superseded = [c for c in claims if c.get("superseded_by")]
        counts_artifact = {"claims": len(claims),
                           "active": len(active), "superseded": len(superseded),
                           "SUPPORTED": sum(1 for c in active if c.get("verdict") == "SUPPORTED"),
                           "UNCERTAIN": sum(1 for c in active if c.get("verdict") == "UNCERTAIN"),
                           "UNVERIFIED": sum(1 for c in active if c.get("verdict") == "UNVERIFIED"),
                           "rules": n_rules, "concepts": n_concepts, "examples": n_examples,
                           "total_frames": len(frames)}
        def reported(pattern, label):
            m = re.search(pattern, rd)
            return int(m.group(1)) if m else None
        pairs = [
            (r"\|\s*Claims totales\s*\|\s*(\d+)", counts_artifact["claims"], "claims totales"),
            (r"\|\s*Rules / concepts / examples documentados\s*\|\s*(\d+)\s*/\s*(\d+)\s*/\s*(\d+)", (n_rules, n_concepts, n_examples), "rules/concepts/examples"),
        ]
        for pat, expect, label in pairs:
            m = re.search(pat, rd)
            if not m:
                bad("V10", f"README: no encuentro la métrica '{label}'")
                continue
            got = tuple(int(g) for g in m.groups())
            want = expect if isinstance(expect, tuple) else (expect,)
            if got != want:
                bad("V10", f"README {label} = {got} pero artefactos = {want}")
        # frames: base/on-demand si el README los declara
        mb = re.search(r"\|\s*Frames base[^|]*\|\s*(\d+)", rd)
        mo = re.search(r"\|\s*Frames bajo demanda\s*\|\s*(\d+)", rd)
        # frames: base/on-demand si el README los declara. La clase base NO se
        # deduce desde nombres (autoridad = frames/.base_frames); si README los
        # declara, se valida coherencia total = base + on_demand.
        if mb and mo:
            b, o = int(mb.group(1)), int(mo.group(1))
            if b + o != len(frames):
                bad("V10", f"README frames base({b}) + on-demand({o}) != archivos en frames/ ({len(frames)})")
        # lifecycle: con >=1 claim reemplazado, el README debe distinguir
        # activos vs superseded y reconciliar con los artefactos.
        if superseded:
            mls = re.search(r"\|\s*Claims activos\s*/\s*superseded\s*\|\s*(\d+)\s*/\s*(\d+)", rd)
            if not mls:
                bad("V10", "README: falta la fila '| Claims activos / superseded | A / S |' (la biblioteca tiene claims reemplazados)")
            else:
                a, s = int(mls.group(1)), int(mls.group(2))
                if (a, s) != (counts_artifact["active"], counts_artifact["superseded"]):
                    bad("V10", f"README activos/superseded = {(a, s)} pero artefactos = "
                               f"{(counts_artifact['active'], counts_artifact['superseded'])}")

    # V11: referencias en docs
    tok_f = re.compile(r"\bf-(\d{6})(\.png)?\b")
    tok_c = re.compile(r"\bc-(\d{4})\b")
    tok_s = re.compile(r"\bs-(\d{6})([a-z])?\b")
    claim_ids = set(seen)
    for d in DOCS:
        p = os.path.join(lib, d)
        if not os.path.exists(p):
            continue
        for ln_no, line in enumerate(open(p, encoding="utf-8"), 1):
            stripped = line.strip()
            if stripped.startswith(">") and "frozen" in line:
                continue
            for m in tok_f.findall(line):
                name = f"f-{m[0]}"
                if name in deprecated:
                    continue
                if name + ".png" not in frames:
                    bad("V11", f"{d}:{ln_no}: referencia a frame inexistente {name} (¿histórico? decláralo en .deprecated_frame_names)")
            for m in tok_c.findall(line):
                if f"c-{m}" not in claim_ids:
                    bad("V11", f"{d}:{ln_no}: referencia a claim inexistente c-{m}")
            for m in tok_s.findall(line):
                sid = f"s-{m[0]}" + (m[1] or "")
                if sid not in sid_set:
                    bad("V11", f"{d}:{ln_no}: referencia a segmento inexistente {sid}")

    # --- W: navegación wiki (Parte E del contrato v1.2)
    WIKI_DOCS = DOCS + ["CLAIMS.md", "FRAMES.md", "OPEN-QUESTIONS.md", "AMENDMENTS.md"]
    vault = find_vault_root(lib)
    if vault is None:
        # biblioteca fuera de un vault Obsidian: los checks W no aplican (no hay
        # superficie de wikilinks que validar). SKIP no afecta el veredicto;
        # en el vault real el marker siempre resuelve.
        findings.append(("W*", "SKIP", "vault root no resuelto: checks W de wikilinks omitidos"))
    else:
        claims_path_md = os.path.join(lib, "CLAIMS.md")
        # W04: CLAIMS.md con exactamente un heading por claim
        if os.path.exists(claims_path_md):
            heads = re.findall(r"^### (c-\d{4})\s*$", open(claims_path_md, encoding="utf-8").read(), re.M)
            want = sorted(c.get("id") for c in claims)
            got = sorted(heads)
            if len(set(heads)) != len(heads):
                bad("W04", "CLAIMS.md: headings de claim duplicados")
            if got != want:
                miss = sorted(set(want) - set(got)); extra = sorted(set(got) - set(want))
                bad("W04", f"CLAIMS.md desincronizada con claims.jsonl (stale projection): missing={miss} extra={extra}")
            # W09: coherencia de statement/epistemic/verdict por sección
            # (proyección stale: cualquier campo desalineado con claims.jsonl
            # se detecta, no sólo headings y veredictos)
            cm = open(claims_path_md, encoding="utf-8").read()
            for c in claims:
                sec = re.search(r"### " + re.escape(c["id"]) + r"\b.*?(?=\n### |\Z)", cm, re.S)
                if not sec:
                    continue
                body = sec.group(0)
                if f"**Verdict:** {c['verdict']}" not in body:
                    bad("W09", f"CLAIMS.md: verdict desalineado para {c['id']}")
                if f"**Statement:** {c.get('statement','')}" not in body:
                    bad("W09", f"CLAIMS.md: statement desalineado para {c['id']}")
                if f"**Epistemic:** {c.get('epistemic','')}" not in body:
                    bad("W09", f"CLAIMS.md: epistemic desalineado para {c['id']}")
        else:
            bad("W04", "falta CLAIMS.md (proyección obligatoria v1.2)")
        # W05: anchors únicos de transcript y cada anchor cerrando SU propio
        # bloque (línea en blanco / heading / EOF antes y después): en Obsidian,
        # un block id a mitad de párrafo es texto literal, no anchor.
        anchors = re.findall(r"\^(s-\d{6}[a-z]?)\b", t_text)
        seg_ids = set(sids)
        if len(set(anchors)) != len(anchors):
            bad("W05", "transcript: block ids duplicados")
        if set(anchors) != seg_ids or len(anchors) != len(sids):
            bad("W05", f"transcript: anchors ({len(anchors)}) != segmentos ({len(sids)})")
        t_lines = t_text.splitlines()
        for li, ln in enumerate(t_lines):
            if not re.search(r"\^(s-\d{6}[a-z]?)\s*$", ln):
                continue
            prev_l = t_lines[li - 1] if li > 0 else None
            next_l = t_lines[li + 1] if li + 1 < len(t_lines) else None
            if (prev_l is not None and prev_l.strip() != "" and not prev_l.lstrip().startswith("#")) \
                    or (next_l is not None and next_l.strip() != "" and not next_l.lstrip().startswith("#")):
                bad("W05", f"transcript línea {li + 1}: anchor sin bloque propio "
                           f"(separación de párrafo ausente)")
        # W06: FRAMES.md cubre todos los frames
        frames_md = os.path.join(lib, "FRAMES.md")
        if os.path.exists(frames_md):
            fm = open(frames_md, encoding="utf-8").read()
            missing_frames = sorted(f for f in frames if f[:-4] not in fm)
            if missing_frames:
                bad("W06", f"FRAMES.md no cubre {len(missing_frames)} frames: {missing_frames[:6]}")
        else:
            bad("W06", "falta FRAMES.md")
        # W01-W03/W07 sobre docs del capítulo + W08 sobre curso + W10 balance
        for d in WIKI_DOCS:
            pth = os.path.join(lib, d)
            if os.path.exists(pth):
                text = open(pth, encoding="utf-8").read()
                check_wiki_targets(text, d, vault, lib, bad)
                check_wiki_balance(text, d, bad)
        for d in ("COURSE-INDEX.md", "GLOSSARY.md"):
            pth = os.path.join(os.path.dirname(lib), d)
            if os.path.exists(pth):
                check_wiki_targets(open(pth, encoding="utf-8").read(), d, vault, lib, bad)

    # V12: dudosos citados como hechos en documentation.md
    docp = os.path.join(lib, "documentation.md")
    if os.path.exists(docp):
        markers = ("UNCERTAIN", "UNVERIFIED", "dudos", "hipótesis", "no resuelto",
                   "interpretación", "adjudica")
        for c in claims:
            if c.get("verdict") == "SUPPORTED":
                continue
            cid = c["id"]
            for ln_no, line in enumerate(open(docp, encoding="utf-8"), 1):
                if cid in line:
                    ctx = open(docp, encoding="utf-8").read()
                    window = ctx[max(0, ctx.find(cid) - 400): ctx.find(cid) + 400].lower()
                    if not any(mk.lower() in window for mk in markers):
                        bad("V12", f"documentation.md:{ln_no}: cita {cid} ({c.get('verdict')}) sin marco de duda explícito")

    # --- V14: integridad del lifecycle de supersession
    by_id = {c.get("id"): c for c in claims}
    sup_ids = {cid for cid, c in by_id.items() if c.get("superseded_by")}
    for c in claims:
        cid = c.get("id", "?")
        sb, ss = c.get("superseded_by"), c.get("supersedes")
        if sb:
            if sb not in by_id:
                bad("V14", f"{cid}: superseded_by apunta a claim inexistente: {sb}")
            elif sb == cid:
                bad("V14", f"{cid}: superseded_by apunta a sí mismo")
            elif (by_id[sb] or {}).get("supersedes") != cid:
                bad("V14", f"{cid}: reemplazo no bidireccional: superseded_by={sb} pero "
                           f"{sb} no declara supersedes={cid}")
        if ss:
            if ss not in by_id:
                bad("V14", f"{cid}: supersedes apunta a claim inexistente: {ss}")
            elif ss == cid:
                bad("V14", f"{cid}: supersedes apunta a sí mismo")
            elif (by_id[ss] or {}).get("superseded_by") != cid:
                bad("V14", f"{cid}: reemplazo no bidireccional: supersedes={ss} pero "
                           f"{ss} no declara superseded_by={cid}")
    # ciclos: seguir la cadena superseded_by desde cada claim
    for c in claims:
        origin, cur, visited = c.get("id"), c, set()
        while isinstance(cur, dict) and cur.get("superseded_by"):
            nxt = cur["superseded_by"]
            if nxt == origin or nxt in visited:
                bad("V14", f"{origin}: ciclo de reemplazo en la cadena superseded_by")
                break
            visited.add(nxt)
            cur = by_id.get(nxt)
            if cur is None:
                break  # target inexistente: ya reportado por V14

    # --- V15: CLAIMS.md representa el lifecycle (proyección sincronizada)
    claims_md_path = os.path.join(lib, "CLAIMS.md")
    if sup_ids and os.path.exists(claims_md_path):
        cm = open(claims_md_path, encoding="utf-8").read()
        for cid in sorted(sup_ids):
            sec = re.search(r"### " + re.escape(cid) + r"\b.*?(?=\n### |\Z)", cm, re.S)
            if not sec:
                continue
            body = sec.group(0)
            succ = by_id[cid].get("superseded_by")
            if "SUPERSEDED — HISTORICAL, NOT ACTIVE" not in body:
                bad("V15", f"CLAIMS.md: {cid} es superseded pero la proyección no lo marca "
                           f"(regenerar con render_claims_md.py)")
            if succ and "CLAIMS#" + str(succ) not in body:
                bad("V15", f"CLAIMS.md: {cid} sin link Replacement navegable a {succ}")
        for c in claims:
            prev = c.get("supersedes")
            if not prev:
                continue
            sec = re.search(r"### " + re.escape(c.get("id", "?")) + r"\b.*?(?=\n### |\Z)", cm, re.S)
            if sec and "CLAIMS#" + str(prev) not in sec.group(0):
                bad("V15", f"CLAIMS.md: {c.get('id')} sin link Supersedes a {prev}")

    # --- V16: los docs pedagógicos no citan claims reemplazados como vigentes.
    # La cita vigente en esta biblioteca es el WIKILINK [[…/CLAIMS#c-XXXX|…]];
    # las menciones en texto plano ("supersede a c-0116") son el rastro de
    # auditoría que el contrato de supersession exige preservar y no se
    # flaggean. Los ids son por-capítulo: sólo cuentan los wikilinks que
    # apuntan a la CLAIMS.md de ESTA biblioteca.
    PEDAGOGICAL = ["documentation.md", "rules.md", "concepts.md",
                   "examples.md", "study-guide.md"]
    lib_base = os.path.basename(os.path.normpath(lib))
    if sup_ids:
        for d in PEDAGOGICAL:
            p = os.path.join(lib, d)
            if not os.path.exists(p):
                continue
            text = open(p, encoding="utf-8").read()
            for m in WIKI_RE.finditer(text):
                target, anchor = m.group(1).strip(), (m.group(2) or "").strip()
                am = re.match(r"^#(c-\d{4})$", anchor)
                if not am or am.group(1) not in sup_ids:
                    continue
                if lib_base not in target:
                    continue  # wikilink a otra biblioteca: ids ajenos
                bad("V16", f"{d}: cita como evidencia vigente el claim reemplazado {am.group(1)} "
                           f"(wikilink {m.group(0)[:60]}…); citar {by_id[am.group(1)].get('superseded_by')} "
                           f"— la historia vive en AMENDMENTS/review-notes")

    ok = not [f for f in findings if f[1] != "SKIP"]
    if args.json:
        print(json.dumps({"pass": ok, "findings": [{"check": k, "severity": s, "msg": m} for k, s, m in findings]}, ensure_ascii=False, indent=1))
    else:
        if findings:
            cur = None
            for k, s, m in findings:
                if k != cur:
                    print(f"== {k} ==")
                    cur = k
                print(f"  [{s}] {m}")
        blocking = [f for f in findings if f[1] != "SKIP"]
        by = {}
        for k, _, _ in blocking:
            by[k] = by.get(k, 0) + 1
        print(f"LIBRARY_VALIDATION = {'PASS' if ok else 'FAIL'}  findings={sum(by.values())} by_check={by or '{}'}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
