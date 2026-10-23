#!/usr/bin/env python3
"""check_consumption_contract.py — preflight determinista del contrato de consumo.

Contrato (hardening 2026-10-23, tras q-ch07-019): SUPPORTED acredita FIDELIDAD
a la fuente, no verdad objetiva ni ausencia de contradicciones. El compilador/
síntesis sólo trata como hecho fundamentado un claim:

    CONSUMIBLE = ACTIVE (sin superseded_by) AND verdict = SUPPORTED
                 AND evidencia resuelta (s- en transcript, f-.png en frames/)

y todo consumible lleva adjuntas sus DUDAS MATERIALES: las preguntas
q-<curso>-NNN con Estado OPEN y Materialidad MATERIAL que el claim referencia
en `unresolved_questions` (marcador de materialidad declarado en
OPEN-QUESTIONS.md; sin marcador la pregunta es AUXILIAR y no guarda el claim —
garbles y deícticos no bloquean). Una pregunta MATERIAL con ≥2 claims ligados
es un GRUPO DE CONTRADICCIÓN: sus claims se consumen preservando ambas
versiones dichas; NINGUNA puede presentarse como confirmada.

Chequeos (exit 1 = violación):
  CC01  q-* referenciada en unresolved_questions no existe en el curso
  CC02  referencia a pregunta MATERIAL vigente ausente: toda pregunta OPEN
        MATERIAL debe estar referenciada en el unresolved_questions de TODOS
        los claims que su entrada enlaza (vínculo estructural en ambos
        sentidos; detecta la contradicción sin señalizar en los claims)
  CC03  evidencia rota en un claim consumible
  CC04  --require-question: la pregunta no es OPEN MATERIAL o el conjunto de
        claims ligados no es exactamente el esperado

Uso:
    check_consumption_contract.py <library_root> [--json]
        [--require-question q-ch07-019=c-0143,c-0181,c-0182]

El validador NO juzga verdad semántica: verifica la estructura del contrato.
La interpretación libre (NLU sobre síntesis) no es objeto de este script; la
prueba de interpretación documentada vive en
scripts/tests/consumption_contract_selftest.py.
"""
import argparse, json, os, re, sys

QID_RE = re.compile(r"\bq-[a-z0-9]+-\d{3}\b")
CLAIM_WIKI_RE = re.compile(r"\[\[[^\]]*CLAIMS#c-(\d{4})[^\]]*\]\]")
ESTADO_RE = re.compile(r"\*\*Estado:\s*([A-Z]+)")
MATERIALIDAD_RE = re.compile(r"\*\*Materialidad:\s*(MATERIAL|AUXILIAR)\*\*")


def load_open_questions(path):
    """q_id -> {estado, materialidad, linked_claims} desde OPEN-QUESTIONS.md."""
    out = {}
    if not os.path.exists(path):
        return out
    text = open(path, encoding="utf-8").read()
    secs = re.split(r"^#{2,3} (q-\S+?)\s*(?:—.*)?$", text, flags=re.M)
    for i in range(1, len(secs) - 1, 2):
        qid, body = secs[i].strip(), secs[i + 1]
        est = ESTADO_RE.search(body)
        mat = MATERIALIDAD_RE.search(body)
        out[qid] = {
            "estado": est.group(1) if est else "OPEN",
            "materialidad": mat.group(1) if mat else "AUXILIAR",
            "linked_claims": sorted(set(CLAIM_WIKI_RE.findall(body))),
            "chapter_file": path,
        }
    return out


def resolve_evidence(claims, seg_ids, frames):
    """(rota, total_refs) — s- resuelve en transcript, f-.png existe."""
    broken = []
    for c in claims:
        for e in c.get("evidence", []):
            if e.startswith("s-") and e not in seg_ids:
                broken.append((c["id"], e))
            elif e.startswith("f-") and e not in frames:
                broken.append((c["id"], e))
    return broken


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("library_root")
    ap.add_argument("--require-question", action="append", default=[],
                    help="qID=c1,c2,... — exige OPEN MATERIAL y ese conjunto exacto")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    root = os.path.abspath(args.library_root)

    chapters, violations, qreg = {}, [], {}
    for name in sorted(os.listdir(root)):
        ch = os.path.join(root, name)
        cj = os.path.join(ch, "claims.jsonl")
        tr = os.path.join(ch, "transcript.md")
        fr = os.path.join(ch, "frames")
        if not (name.startswith("ch") and os.path.isdir(ch)
                and os.path.exists(cj) and os.path.exists(tr) and os.path.isdir(fr)):
            continue
        for qid, q in load_open_questions(os.path.join(ch, "OPEN-QUESTIONS.md")).items():
            if qid in qreg:
                violations.append(("CC01", f"{qid} declarada en dos capítulos: {name}"))
            qreg[qid] = dict(q, chapter=name)

        claims, seg_ids = [], set()
        for line in open(cj, encoding="utf-8"):
            if line.strip():
                claims.append(json.loads(line))
        t = open(tr, encoding="utf-8").read()
        seg_ids = set(re.findall(r"^(s-\d{6}[a-z]?) \[", t, re.M))
        frames = {f[:-4] for f in os.listdir(fr) if f.endswith(".png")}
        chapters[name] = {"claims": claims, "seg_ids": seg_ids, "frames": frames}

    manifest = {}
    guarded_total = consumable_total = 0
    for name, data in sorted(chapters.items()):
        rows = []
        for c in data["claims"]:
            cid = c.get("id", "?")
            if c.get("superseded_by"):
                status = "EXCLUDED_SUPERSEDED"
            elif c.get("verdict") == "UNCERTAIN":
                status = "EXCLUDED_UNCERTAIN"
            elif c.get("verdict") == "UNVERIFIED":
                status = "EXCLUDED_UNVERIFIED"
            else:
                status = "CONSUMABLE"
            material_qs, info_qs = [], []
            for m in QID_RE.finditer(json.dumps(c.get("unresolved_questions") or [], ensure_ascii=False)):
                qid = m.group(0)
                q = qreg.get(qid)
                if q is None:
                    violations.append(("CC01", f"{name}/{cid}: q inexistente {qid}"))
                elif q["estado"] == "OPEN" and q["materialidad"] == "MATERIAL":
                    material_qs.append(qid)
                elif q["estado"] == "RESOLVED":
                    info_qs.append(qid)
            material_qs = sorted(set(material_qs))
            if status == "CONSUMABLE":
                if material_qs:
                    status = "CONSUMABLE_WITH_MATERIAL_QUESTION"
                    guarded_total += 1
                else:
                    consumable_total += 1
            rows.append({"id": cid, "status": status, "material_questions": material_qs,
                         "resolved_question_refs": sorted(set(info_qs))})
        broken = resolve_evidence(data["claims"], data["seg_ids"], data["frames"])
        for cid, e in broken:
            violations.append(("CC03", f"{name}/{cid}: evidencia rota {e}"))
        manifest[name] = {"rows": rows, "broken_evidence": broken}

    # CC02: toda pregunta OPEN MATERIAL debe estar referenciada por TODOS los
    # claims que su propia entrada enlaza (vínculo estructural bidireccional).
    groups = {}
    for qid, q in sorted(qreg.items()):
        if q["estado"] != "OPEN" or q["materialidad"] != "MATERIAL":
            continue
        ch_name = q["chapter"]
        refd = {r["id"] for r in manifest[ch_name]["rows"] if qid in r["material_questions"]}
        linked = set(q["linked_claims"])
        if linked - refd:
            violations.append(("CC02", f"{qid} (OPEN MATERIAL) sin vínculo estructural en "
                                       f"{sorted(linked - refd)} — los claims que la entrada "
                                       f"enlaza deben referenciarla en unresolved_questions"))
        if len(linked) >= 2:
            groups[qid] = {"chapter": ch_name, "claims": sorted(linked)}

    # CC04: exigencias exactas por pregunta
    for req in args.require_question:
        qid, _, cl = req.partition("=")
        want = sorted(x for x in cl.split(",") if x)
        q = qreg.get(qid)
        if not q or q["estado"] != "OPEN" or q["materialidad"] != "MATERIAL":
            violations.append(("CC04", f"{qid}: no es OPEN MATERIAL"))
            continue
        rows = manifest[q["chapter"]]["rows"]
        got = sorted(r["id"] for r in rows if qid in r["material_questions"])
        linked = sorted(q["linked_claims"])
        if want != got or want != linked:
            violations.append(("CC04", f"{qid}: esperado {want}; referencia=({got}) entrada=({linked})"))

    n_claims = sum(len(d["claims"]) for d in chapters.values())
    summary = {
        "library_root": root,
        "chapters": len(chapters),
        "claims": n_claims,
        "consumable": consumable_total,
        "consumable_with_material_question": guarded_total,
        "excluded": {
            "SUPERSEDED": sum(1 for d in chapters.values() for c in d["claims"] if c.get("superseded_by")),
            "UNCERTAIN": sum(1 for d in chapters.values() for c in d["claims"] if c.get("verdict") == "UNCERTAIN"),
            "UNVERIFIED": sum(1 for d in chapters.values() for c in d["claims"] if c.get("verdict") == "UNVERIFIED"),
        },
        "material_contradiction_groups": groups,
        "violations": [{"check": k, "msg": m} for k, m in violations],
        "pass": not violations,
    }
    if args.json:
        print(json.dumps({"summary": summary, "manifest": manifest}, ensure_ascii=False, indent=1))
    else:
        for k, m in violations:
            print(f"[{k}] {m}")
        print(f"CONSUMPTION_CONTRACT_PREFLIGHT = {'PASS' if not violations else 'FAIL'}  "
              f"chapters={len(chapters)} claims={n_claims} consumible={consumable_total} "
              f"consumible_con_duda_material={guarded_total} grupos_contradiccion={len(groups)}")
    sys.exit(0 if not violations else 1)


if __name__ == "__main__":
    main()
