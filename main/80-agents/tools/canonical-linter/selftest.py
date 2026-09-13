#!/usr/bin/env python3
"""Selftest del Canonical / Deprecation Linter (P3-B).

Cubre los requisitos de verificación del spec (sección 5) y del modelo
(sección 8):
- cada check CL-01..CL-20 con caso positivo y negativo;
- demos FAIL obligatorias (CL-01, CL-06, CL-14, CL-18) y demos WARN
  obligatorias (CL-08, CL-10, CL-12, CL-19);
- links con heading/bloque/alias/ambigüedad;
- frontmatter multilínea, quoting y campos vacíos;
- exclusión de fixtures sintéticas (A8);
- determinismo: dos runs idénticos salvo run/timestamp/results_file;
- marker VAULT_ROOT ausente -> exit 2;
- input malformado -> veredictos normales (SKIP/WARN motivado), nunca traceback.

Las fixtures viven en tempdirs FUERA del vault; cleanup con rmtree en finally.
Read-only sobre el vault real: sólo copia archivos de infraestructura hacia
los tempdirs. Sin red, sin daemon, sin DB. Python 3.9+ stdlib only.
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import traceback

sys.dont_write_bytecode = True  # sin __pycache__ fuera del write scope

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
REAL_ROOT = os.path.dirname(HERE)  # .../80-agents/tools -> VAULT_ROOT
while not os.path.isfile(os.path.join(REAL_ROOT, "80-agents/agents-os/agents-os.md")):
    parent = os.path.dirname(REAL_ROOT)
    if parent == REAL_ROOT:
        raise SystemExit("VAULT_ROOT no encontrado desde %s" % HERE)
    REAL_ROOT = parent

import canonical_linter as cl  # noqa: E402

VAULTS = []
INFRA_FILES = [
    ("80-agents/tools/conformance-harness/rules.py", "rules.py"),
    ("80-agents/tools/conformance-harness/agents_os_conformance.py", "agents_os_conformance.py"),
    ("80-agents/skills/_shared/scripts/validate_schema_contract.py", "validate_schema_contract.py"),
    ("80-agents/skills/_shared/schema-contract.md", "schema-contract.md"),
]


def new_vault(with_infra: bool = True) -> str:
    tmp = tempfile.mkdtemp(prefix="cl-selftest-")
    VAULTS.append(tmp)
    os.makedirs(os.path.join(tmp, "80-agents/agents-os"), exist_ok=True)
    with open(os.path.join(tmp, "80-agents/agents-os/agents-os.md"), "w", encoding="utf-8") as fh:
        fh.write("# agents-os map (fixture)\n")
    if with_infra:
        for rel, _src in INFRA_FILES:
            src = os.path.join(REAL_ROOT, rel)
            dst = os.path.join(tmp, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if rel.endswith(".md"):
                # stub sin wikilinks: el modulo del contract se precalienta
                # desde el vault REAL (contenido estable); la copia en el
                # tempdir solo existe por fidelidad estructural y para no
                # meter enlaces reales al corpus del fixture.
                with open(dst, "w", encoding="utf-8") as fh:
                    fh.write("# schema-contract (stub de selftest, sin wikilinks)\n")
            else:
                shutil.copyfile(src, dst)
    return tmp


def write_note(root: str, rel: str, text: str) -> str:
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return rel


def run(root: str, only_ids=None, only_categories=None) -> dict:
    doc = cl.run_suite(root, only_ids=only_ids, only_categories=only_categories, write=False)
    return doc


def by_id(doc: dict) -> dict:
    return {c["check_id"]: c for c in doc["checks"]}


def findings_of(doc: dict, cid: str):
    return by_id(doc)[cid]["findings"]


def assert_true(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


# ---------------------------------------------------------------------------
# Fixtures: vault positivo con un caso por check
# ---------------------------------------------------------------------------
def build_positive_vault() -> str:
    r = new_vault()
    # Nota base activa con alias y links de destino.
    write_note(r, "Destino.md", """---
type: doc
schema_version: 1
status: active
aliases:
  - destino-alias
tags:
  - kind/doc
---

# Destino

Cuerpo vigente.
""")
    write_note(r, "30-resources/vigente.md", """---
type: doc
schema_version: 1
status: active
tags:
  - kind/doc
---

Vigente.
""")
    # CL-01: active + superseded_by -> FAIL; y negative local: supersedes+active.
    write_note(r, "cl01-reemplazada.md", """---
type: doc
schema_version: 1
status: active
superseded_by: "[[no-existe-cl01]]"
tags:
  - kind/doc
---

Sigue activa pese a declarar su reemplazo.
""")
    write_note(r, "cl01-sucesion-canónica.md", """---
type: doc
schema_version: 1
status: active
supersedes: "[[vieja]]"
tags:
  - kind/doc
---

Sucesión canónica: la nueva enlaza supersedes (00-RESOURCE-WIKI).
""")
    # CL-02 pos1: agent_memory superseded sin superseded_by (fuera de memory/internal) -> FAIL.
    write_note(r, "cl02-memoria.md", """---
type: agent_memory
schema_version: 1
memory_state: superseded
superseded_by:
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/agent-memory
---

Memoria reemplazada sin puntero (superseded_by vacío = ausente).
""")
    # CL-02 pos2: source superseded -> FAIL; pos3: doc con quoting -> WARN.
    write_note(r, "cl02-source.md", """---
type: source
schema_version: 1
status: superseded
tags:
  - kind/source
---

Fuente reemplazada sin superseded_by.
""")
    write_note(r, "cl02-doc.md", """---
type: doc
schema_version: 1
status: "superseded"
tags:
  - kind/doc
---

Doc superseded con status quoted -> WARN (autoridad parcial).
""")
    # CL-02 dedup: agent_memory bajo memory/internal -> el doctor lo cubre.
    write_note(r, "80-agents/memory/internal/cl02-interna.md", """---
type: agent_memory
schema_version: 1
memory_state: superseded
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/agent-memory
---

Debe ser omitida por dedup con doctor:check_internal_memory_lifecycle.
""")
    # CL-03: en retiro + índice máximo -> WARN; variante low -> nada.
    write_note(r, "cl03-app.md", """---
type: application
schema_version: 1
status: deprecated
indexable: true
index_priority: high
area: "[[Personal]]"
related:
  - "[[Destino]]"
tags:
  - kind/application
---

App en retiro con preferencia de índice máxima.
""")
    write_note(r, "cl03-app-low.md", """---
type: application
schema_version: 1
status: deprecated
indexable: true
index_priority: low
area: "[[Personal]]"
related:
  - "[[Destino]]"
tags:
  - kind/application
---

App en retiro con prioridad baja (cumple).
""")
    # CL-04: sucesión rota -> FAIL; ambigua -> WARN.
    write_note(r, "cl04-rota.md", """---
type: source
schema_version: 1
status: superseded
superseded_by: "[[no-existe-cl04]]"
tags:
  - kind/source
---

Sucesión hacia nota inexistente.
""")
    write_note(r, "cl04-ambigua.md", """---
type: source
schema_version: 1
status: superseded
superseded_by: "[[Amb]]"
tags:
  - kind/source
---

Sucesión hacia basename ambiguo.
""")
    write_note(r, "dir1/Amb.md", "# Amb uno\n")
    write_note(r, "dir2/Amb.md", "# Amb dos\n")
    # CL-05: resource en retiro sin puntero -> WARN; con related -> nada.
    write_note(r, "cl05-recurso.md", """---
type: resource
schema_version: 1
status: deprecated
tags:
  - kind/resource
---

Recurso en retiro sin puntero estructurado.
""")
    write_note(r, "cl05-recurso-ok.md", """---
type: resource
schema_version: 1
status: deprecated
related:
  - "[[Destino]]"
tags:
  - kind/resource
---

Recurso en retiro con puntero en frontmatter.
""")
    # CL-06: colisión casefold.
    write_note(r, "rio/RIO.md", "# RIO\n")
    write_note(r, "otro/rio.md", "# rio\n")
    # CL-07: slug duplicado.
    write_note(r, "cl07-a.md", "---\ntype: doc\nschema_version: 1\nstatus: active\nslug: dup-slug\ntags:\n  - kind/doc\n---\n\nA\n")
    write_note(r, "cl07-b.md", "---\ntype: doc\nschema_version: 1\nstatus: active\nslug: dup-slug\ntags:\n  - kind/doc\n---\n\nB\n")
    # CL-08: alias duplicado entre notas S2 (aliases multilínea).
    write_note(r, "cl08-a.md", """---
type: doc
schema_version: 1
status: active
aliases:
  - Compartido
  - otro-alias-a
tags:
  - kind/doc
---

A con alias duplicado.
""")
    write_note(r, "cl08-b.md", """---
type: doc
schema_version: 1
status: active
aliases:
  - Compartido
tags:
  - kind/doc
---

B con el mismo alias.
""")
    # CL-09: copias archivadas con always / índice máximo -> WARN.
    write_note(r, "40-archive/drafts/cl09-always.md", """---
type: doc
schema_version: 1
status: active
load_policy: always
tags:
  - kind/doc
---

Copia archivada de ex-autoridad con always.
""")
    write_note(r, "40-archive/drafts/cl09-index.md", """---
type: doc
schema_version: 1
status: active
indexable: true
index_priority: critical
tags:
  - kind/doc
---

Copia archivada con preferencia de índice máxima.
""")
    # CL-10: directorio con forma de archive fuera de 40-archive -> WARN.
    write_note(r, "archive/legacy/cl10.md", "---\ntype: doc\nschema_version: 1\nstatus: active\ntags:\n  - kind/doc\n---\n\nNota en archive raíz no declarado.\n")
    # CL-11: campo de routing roto -> FAIL; campo válido -> nada.
    write_note(r, "cl11-roto.md", """---
type: doc
schema_version: 1
status: active
project: "[[fantasma-cl11]]"
tags:
  - kind/doc
---

Campo project hacia nota inexistente.
""")
    write_note(r, "cl11-ok.md", """---
type: doc
schema_version: 1
status: active
project: "[[Destino]]"
tags:
  - kind/doc
---

Campo project válido.
""")
    # CL-12: cuerpo con roto / heading / bloque / alias / ambiguo.
    write_note(r, "cl12-cuerpo.md", """---
type: doc
schema_version: 1
status: active
tags:
  - kind/doc
---

Enlace roto: [[nota-fantasma]].
Con heading: [[Destino#Sección]].
Con bloque: [[Destino#^abc123]].
Con alias: [[destino-alias]].
Ambiguo: [[Amb]].
Ilustrativo en código: `[[ilustracion]]`.
""")
    # CL-13: link a archivada (path) y a superseded (estado) -> WARN.
    write_note(r, "40-archive/old/archivada.md", "---\ntype: doc\nschema_version: 1\nstatus: completed\ntags:\n  - kind/doc\n---\n\nRetención histórica por path.\n")
    write_note(r, "vieja.md", """---
type: doc
schema_version: 1
status: archived
superseded_by: "[[Destino]]"
tags:
  - kind/doc
---

Nota viva en estado superseded.
""")
    write_note(r, "cl13-origen.md", """---
type: doc
schema_version: 1
status: active
tags:
  - kind/doc
---

Enlaza [[archivada]] y [[vieja]] y [[Destino]].
""")
    # CL-14/CL-15: 00-index de dominio wiki activo.
    write_note(r, "30-resources/wiki/retirada.md", """---
type: application
schema_version: 1
status: deprecated
related:
  - "[[Destino]]"
tags:
  - kind/application
---

Página en retiro listada en el índice.
""")
    write_note(r, "30-resources/wiki/00-index.md", """---
type: index
schema_version: 1
status: active
tags:
  - kind/index
---

# Wiki de prueba

| Página | Una línea |
|---|---|
| [[Destino]] | Vigente. |
| [[no-existe-cl14]] | Fila rota. |
| [[assets/datos.csv]] | Asset no-.md existente. |
| [[retirada]] | Página en retiro. |
| [[vigente]] | Otra vigente. |
""")
    write_note(r, "30-resources/wiki/assets/datos.csv", "col\n1\n")
    # CL-16: INDEX.md de skills con destino archive citado y fila federada inexistente.
    write_note(r, "80-agents/skills/okskill/SKILL.md", """---
type: skill
name: okskill
schema_version: 1
scope: global
description: skill de prueba
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/skill
---

Skill ok.
""")
    write_note(r, "80-agents/skills/INDEX.md", """---
type: doc
schema_version: 1
status: active
tags:
  - kind/doc
---

# Registro

## Catálogo core

| Skill | Uso |
|---|---|
| [[80-agents/skills/okskill/SKILL|okskill]] | transversal |

### Dominio y transversales

| Skill | Uso |
|---|---|
| [[30-resources/agents/skills/nofede/SKILL|nofede]] | transversal |

Cita: `40-archive/agents-os-drafts/AGENTS.md`
""")
    # CL-17: bootstrap cita un path existente y uno inexistente.
    write_note(r, "80-agents/agents-os/agent-constitution.md", "# Constitución (fixture)\n\nCita `30-resources/vigente.md`.\n")
    write_note(r, "80-agents/skills/agents-os-bootstrap/SKILL.md", """# Bootstrap (fixture)

Carga `80-agents/agents-os/agent-constitution.md` y `70-templates/falta-cl17.md`.
""")
    # CL-18: router con Minimal Read hacia página en retiro -> FAIL.
    write_note(r, "30-resources/agents/skills/meli-agent-dev/SKILL.md", """---
type: skill
name: meli-agent-dev
schema_version: 1
scope: area
description: router de prueba
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/skill
---

Minimal Read: [[retirada]] y [[vigente]].
""")
    # CL-19: resource active sin last_verified -> WARN; con last_verified -> nada.
    write_note(r, "cl19-sin.md", """---
type: resource
schema_version: 1
status: active
tags:
  - kind/resource
---

Recurso activo sin freshness.
""")
    write_note(r, "cl19-con.md", """---
type: resource
schema_version: 1
status: active
last_verified: 2026-09-01
tags:
  - kind/resource
---

Recurso activo con freshness.
""")
    # CL-20: memory_state en tipo != agent_memory -> WARN.
    write_note(r, "cl20-doc.md", """---
type: doc
schema_version: 1
status: active
memory_state: archived
tags:
  - kind/doc
---

Uso informal de memory_state.
""")
    return r


def build_clean_vault() -> str:
    r = new_vault()
    write_note(r, "Unica.md", """---
type: doc
schema_version: 1
status: active
tags:
  - kind/doc
---

Única nota, sin defectos.
""")
    return r


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def test_positivos_por_check() -> None:
    r = build_positive_vault()
    doc = run(r)
    ids = {c["check_id"] for c in doc["checks"]}
    assert_true(ids == {c[0] for c in cl.CHECKS}, "deben correr los 20 checks: %s" % sorted(ids))

    f1 = findings_of(doc, "CL-01")
    assert_true(any(f["path"] == "cl01-reemplazada.md" and f["status"] == "FAIL" for f in f1),
                "CL-01: active + superseded_by debe ser FAIL: %s" % f1)
    assert_true(not any("sucesion" in f["path"] or "sucesión" in f["path"] for f in f1),
                "CL-01: supersedes+active es sucesión canónica, sin hallazgo: %s" % f1)

    f2 = findings_of(doc, "CL-02")
    paths2 = {f["path"]: f["status"] for f in f2}
    assert_true(paths2.get("cl02-memoria.md") == "FAIL", "CL-02 agent_memory fuera de memory/internal -> FAIL: %s" % paths2)
    assert_true(paths2.get("cl02-source.md") == "FAIL", "CL-02 source -> FAIL: %s" % paths2)
    assert_true(paths2.get("cl02-doc.md") == "WARN", "CL-02 doc -> WARN (y status quoted detectado): %s" % paths2)
    assert_true("80-agents/memory/internal/cl02-interna.md" not in paths2,
                "CL-02: nota bajo memory/internal omitida por dedup: %s" % paths2)
    assert_true(any("doctor:check_internal_memory_lifecycle" in c for c in by_id(doc)["CL-02"]["dedup_cites"]),
                "CL-02: dedup_cites cita al doctor: %s" % by_id(doc)["CL-02"]["dedup_cites"])

    f3 = findings_of(doc, "CL-03")
    assert_true([f["path"] for f in f3] == ["cl03-app.md"], "CL-03: sólo la app con priority high: %s" % f3)

    f4 = findings_of(doc, "CL-04")
    st4 = {f["path"]: f["status"] for f in f4}
    assert_true(st4.get("cl04-rota.md") == "FAIL", "CL-04 sucesión inexistente -> FAIL: %s" % st4)
    assert_true(st4.get("cl04-ambigua.md") == "WARN", "CL-04 sucesión ambigua -> WARN con candidatos: %s" % st4)

    f5 = findings_of(doc, "CL-05")
    assert_true([f["path"] for f in f5] == ["cl05-recurso.md"], "CL-05: sólo el recurso sin puntero: %s" % f5)
    assert_true(all(f["status"] == "WARN" for f in f5), "CL-05 nunca FAIL: %s" % f5)

    f6 = findings_of(doc, "CL-06")
    grp = [f for f in f6 if "rio/RIO.md" in f["evidence"] and "otro/rio.md" in f["evidence"]]
    assert_true(grp and grp[0]["status"] == "FAIL", "CL-06: colisión RIO/rio -> FAIL: %s" % f6)

    f7 = findings_of(doc, "CL-07")
    assert_true(any("dup-slug" in f["observed"] and f["status"] == "FAIL" for f in f7),
                "CL-07 slug duplicado -> FAIL: %s" % f7)

    f8 = findings_of(doc, "CL-08")
    assert_true(any("'Compartido'" in f["observed"] and f["status"] == "WARN" for f in f8),
                "CL-08 alias duplicado -> WARN: %s" % f8)
    assert_true(by_id(doc)["CL-08"]["severity"] == "WARN", "CL-08 severidad máxima WARN")

    f9 = findings_of(doc, "CL-09")
    p9 = {f["path"] for f in f9}
    assert_true("40-archive/drafts/cl09-always.md" in p9 and "40-archive/drafts/cl09-index.md" in p9,
                "CL-09: always y índice máximo bajo 40-archive -> WARN: %s" % f9)

    f10 = findings_of(doc, "CL-10")
    assert_true(any(f["path"] == "archive/legacy/" and f["status"] == "WARN" for f in f10),
                "CL-10: archive/ fuera de 40-archive -> WARN: %s" % f10)

    f11 = findings_of(doc, "CL-11")
    assert_true(any(f["path"] == "cl11-roto.md" and f["status"] == "FAIL" for f in f11),
                "CL-11 routing roto -> FAIL: %s" % f11)
    assert_true(not any(f["path"] == "cl11-ok.md" for f in f11), "CL-11: campo válido sin hallazgo")

    f12 = findings_of(doc, "CL-12")
    obs12 = {f["observed"]: f for f in f12}
    assert_true(any("nota-fantasma" in o for o in obs12), "CL-12: link roto -> WARN: %s" % list(obs12))
    assert_true(any("[[Amb]]" in o and "ambiguo" in o for o in obs12), "CL-12: ambiguo con candidatos: %s" % list(obs12))
    assert_true(not any("Destino#" in o for o in obs12), "CL-12: heading/bloque resuelven por su nota: %s" % list(obs12))
    assert_true(not any("destino-alias" in o for o in obs12), "CL-12: alias resuelve: %s" % list(obs12))
    assert_true(not any("ilustracion" in o for o in obs12), "CL-12: inline code no cuenta como enlace: %s" % list(obs12))

    f13 = findings_of(doc, "CL-13")
    src13 = [f for f in f13 if f["path"] == "cl13-origen.md"]
    assert_true(len(src13) == 2, "CL-13: link a archivada (path) y a vieja (estado): %s" % f13)

    f14 = [f for f in findings_of(doc, "CL-14") if f["status"] == "FAIL"]
    assert_true(len(f14) == 1 and "no-existe-cl14" in f14[0]["observed"],
                "CL-14: una fila rota -> FAIL (el asset csv no cuenta): %s" % f14)

    f15 = findings_of(doc, "CL-15")
    assert_true(len(f15) == 1 and "retirada" in f15[0]["observed"] and f15[0]["status"] == "FAIL",
                "CL-15: fila hacia página en retiro -> FAIL: %s" % f15)

    f16 = findings_of(doc, "CL-16")
    assert_true(len([f for f in f16 if f["status"] == "FAIL"]) == 1 and "40-archive" in f16[0]["observed"],
                "CL-16: cita a 40-archive -> FAIL; fila federada inexistente deduplicada: %s" % f16)

    f17 = findings_of(doc, "CL-17")
    assert_true(any("70-templates/falta-cl17.md" in f["observed"] and f["status"] == "FAIL" for f in f17),
                "CL-17: path citado inexistente -> FAIL: %s" % f17)
    assert_true(not any("30-resources/vigente.md" in f["observed"] for f in f17),
                "CL-17: path existente sin hallazgo")

    f18 = findings_of(doc, "CL-18")
    assert_true(any("retirada" in f["observed"] and f["status"] == "FAIL" for f in f18),
                "CL-18: destino de router en retiro -> FAIL: %s" % f18)
    assert_true(not any("vigente.md" in (f["observed"] + f["evidence"]) for f in f18),
                "CL-18: destino vigente sin hallazgo: %s" % f18)

    f19 = findings_of(doc, "CL-19")
    assert_true([f["path"] for f in f19] == ["cl19-sin.md"] and all(f["status"] == "WARN" for f in f19),
                "CL-19: sólo el recurso sin last_verified, WARN: %s" % f19)

    f20 = findings_of(doc, "CL-20")
    assert_true(any(f["path"] == "cl20-doc.md" and f["status"] == "WARN" for f in f20),
                "CL-20: memory_state fuera de agent_memory -> WARN: %s" % f20)


def test_d1_fila_indice_multilink() -> None:
    """D1 (verificación adversarial P3-C): `_index_rows` debe verificar TODOS
    los wikilinks de cada fila de índice, no sólo el primero. Una fila con dos
    links rotos produce 2 findings; una fila cuyo primer link resuelve y cuyo
    segundo está roto produce 1 finding (el falso negativo del repro
    `30-resources/aranea/00-index.md:125` -> agent-project-08)."""
    r = new_vault()
    write_note(r, "Destino.md", """---
type: doc
schema_version: 1
status: active
tags:
  - kind/doc
---

Destino vigente.
""")
    write_note(r, "30-resources/multi/00-index.md", """---
type: index
schema_version: 1
status: active
tags:
  - kind/index
---

# Multi

| Página | Nota |
|---|---|
| [[Destino]] | Fila vigente. |
| [[roto-d1-b]] a [[roto-d1-c]] | Fila con DOS links rotos. |
| [[Destino]] y [[roto-d1-a]] | Fila cuyo primer link resuelve y el segundo no. |
""")
    doc = run(r)
    f14 = [f for f in findings_of(doc, "CL-14") if f["status"] == "FAIL"]
    obs14 = " | ".join(f["observed"] for f in f14)
    assert_true(len(f14) == 3, "CL-14: 3 links rotos en total (2 + 1): %s" % f14)
    assert_true("roto-d1-b" in obs14 and "roto-d1-c" in obs14,
                "D1: la fila con dos links rotos produce 2 findings: %s" % f14)
    assert_true("roto-d1-a" in obs14,
                "D1: el segundo link de una fila cuyo primero resuelve también se reporta: %s" % f14)
    misma_fila = [f for f in f14 if "roto-d1-b" in f["observed"] or "roto-d1-c" in f["observed"]]
    assert_true(len(misma_fila) == 2 and misma_fila[0]["line"] == misma_fila[1]["line"],
                "D1: los dos findings de la misma fila comparten línea: %s" % misma_fila)
    assert_true(not findings_of(doc, "CL-15"),
                "CL-15: las filas inexistentes son territorio de CL-14: %s" % findings_of(doc, "CL-15"))


def test_negativos_vault_limpio() -> None:
    r = build_clean_vault()
    doc = run(r)
    for c in doc["checks"]:
        assert_true(c["verdict"] == "PASS" and not c["findings"],
                    "%s debe pasar en vault limpio: %s %s" % (c["check_id"], c["verdict"], c["findings"]))
    counts = doc["counts"]
    assert_true(counts["pass"] == 20 and counts["fail"] == 0 and counts["warn"] == 0,
                "20 PASS en vault limpio: %s" % counts)


def test_exclusion_fixtures() -> None:
    r = new_vault()
    write_note(r, "80-agents/skills/_shared/fixtures/ghost.md", """---
type: doc
schema_version: 1
status: superseded
memory_state: archived
indexable: true
index_priority: high
tags:
  - kind/doc
---

Fixture sintética: nunca debe reportarse.
""")
    write_note(r, "80-agents/skills/agents-os-entity-lifecycle/scripts/fixtures/valid/otra.md",
               "---\ntype: doc\nschema_version: 1\nstatus: superseded\ntags:\n  - kind/doc\n---\n\nFixture del entity-lifecycle.\n")
    # Colisión premeditada: una nota viva con el MISMO basename que la fixture.
    write_note(r, "ghost.md", "---\ntype: doc\nschema_version: 1\nstatus: active\ntags:\n  - kind/doc\n---\n\nViva.\n")
    doc = run(r)
    f6 = findings_of(doc, "CL-06")
    assert_true(len(f6) == 0, "CL-06: la fixture no participa en colisiones: %s" % f6)
    for cid in ("CL-02", "CL-03", "CL-20"):
        for f in findings_of(doc, cid):
            assert_true("fixtures/" not in f["path"], "%s reportó una fixture: %s" % (cid, f))


def test_determinismo() -> None:
    r = build_positive_vault()
    d1 = run(r)
    d2 = run(r)
    for d in (d1, d2):
        d.pop("run", None)
        d.pop("results_file", None)
    assert_true(json.dumps(d1, sort_keys=True, ensure_ascii=False) ==
                json.dumps(d2, sort_keys=True, ensure_ascii=False),
                "dos runs deben ser idénticos salvo run/timestamp/results_file")


def test_marker_ausente_exit_2() -> None:
    r = new_vault(with_infra=False)
    os.remove(os.path.join(r, "80-agents/agents-os/agents-os.md"))
    code = cl.main(["--vault-root", r])
    assert_true(code == 2, "marker ausente debe producir exit 2, obtuve %s" % code)


def test_check_y_category_filters() -> None:
    r = build_positive_vault()
    doc = run(r, only_ids=["CL-06"])
    assert_true([c["check_id"] for c in doc["checks"]] == ["CL-06"], "run dirigido --check CL-06")
    doc2 = run(r, only_categories=["METADATA"])
    assert_true({c["check_id"] for c in doc2["checks"]} == {"CL-19", "CL-20"}, "filtro --category METADATA")
    code = cl.main(["--vault-root", r, "--check", "CL-99"])
    assert_true(code == 2, "check desconocido -> exit 2, obtuve %s" % code)


def test_input_malformado() -> None:
    r = new_vault()
    # frontmatter sin cerrar
    write_note(r, "bad1.md", "---\ntype: doc\nstatus: active\nsin cerrar\n")
    # binario/basura
    with open(os.path.join(r, "bad2.md"), "wb") as fh:
        fh.write(b"\x00\x01\xff\xfe[[roto\x9c]]\n---\n\xca\xfe")
    # frontmatter con líneas raras y wikilink sin cerrar en el cuerpo
    write_note(r, "bad3.md", "---\n- lista suelta\n  sangrado: [unclosed\nstatus: : :\n---\n\nCuerpo con [[sin-cerrar y `codigo`.\n")
    doc = run(r)  # no debe lanzar
    for c in doc["checks"]:
        assert_true(c["verdict"] in ("PASS", "FAIL", "WARN", "SKIP"),
                    "%s veredicto válido ante malformado: %s" % (c["check_id"], c["verdict"]))
        if c["verdict"] == "SKIP":
            assert_true(c["skip_reason"], "SKIP siempre motivado")
    assert_true(doc["counts"]["skip"] == 0, "malformado simple no debe anular checks: %s" % doc["counts"])


def test_git_head_y_schema_record() -> None:
    r = build_clean_vault()
    doc = run(r)
    assert_true(doc["tool"] == "canonical-linter", "tool en el record")
    assert_true("git_head" in doc, "git_head informativo presente")
    assert_true("no_vigente" in doc["model"] and "wikilink_resolution" in doc["model"], "modelo declarado (A5/A9)")
    assert_true(set(doc["counts"].keys()) == {"pass", "fail", "warn", "skip", "findings"}, "counts del spec sección 6")
    for c in doc["checks"]:
        for key in ("check_id", "category", "verdict", "severity", "findings", "skip_reason", "dedup_cites"):
            assert_true(key in c, "check %s sin key %s" % (c["check_id"], key))
        for f in c["findings"]:
            for key in ("check_id", "category", "status", "severity", "path", "observed", "expected",
                        "evidence", "confidence", "recommended_action", "authority"):
                assert_true(key in f, "finding de %s sin key %s" % (c["check_id"], key))
            assert_true(f["confidence"] in ("EXACT", "INFERRED"), "confidence EXACT/INFERRED: %s" % f["confidence"])


TESTS = [
    ("positivos_por_check (CL-01..CL-20 con FAIL/WARN demos)", test_positivos_por_check),
    ("d1_fila_indice_multilink (D1: todos los links de una fila de índice)", test_d1_fila_indice_multilink),
    ("negativos_vault_limpio (20 PASS)", test_negativos_vault_limpio),
    ("exclusion_fixtures (A8)", test_exclusion_fixtures),
    ("determinismo (dos runs idénticos)", test_determinismo),
    ("marker_ausente (exit 2)", test_marker_ausente_exit_2),
    ("check_y_category_filters (run dirigido + exit 2)", test_check_y_category_filters),
    ("input_malformado (nunca traceback)", test_input_malformado),
    ("git_head_y_schema_record (spec sección 6)", test_git_head_y_schema_record),
]


def main() -> int:
    print("=" * 72)
    print("CANONICAL LINTER SELFTEST (P3-B)")
    print("=" * 72)
    # Precalienta el cache de módulos desde el vault REAL (rutas estables que
    # nunca se borran): los tempdirs copian la infraestructura por fidelidad
    # estructural, pero Python reutiliza el primer módulo importado.
    cl.build_ctx(REAL_ROOT)
    passed = 0
    failed = 0
    try:
        for name, fn in TESTS:
            try:
                fn()
            except Exception:
                failed += 1
                print("FAIL %s" % name)
                for line in traceback.format_exc().strip().splitlines()[-6:]:
                    print("     %s" % line)
            else:
                passed += 1
                print("PASS %s" % name)
    finally:
        for tmp in VAULTS:
            shutil.rmtree(tmp, ignore_errors=True)
    print("-" * 72)
    print("selftest: %d/%d PASS" % (passed, len(TESTS)))
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
