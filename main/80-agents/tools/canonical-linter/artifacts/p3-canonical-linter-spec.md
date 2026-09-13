---
type: doc
schema_version: 1
status: active
scope: project
project: "[[AGENTS OS]]"
area: "[[Personal]]"
created: 2026-09-13
updated: 2026-09-13
description: Spec vinculante del parent para la tool canonical-linter (PHASE 3) — ratifica el modelo de P3-A (checks CL-01..CL-20, hot path en 4 clases), decide las ambiguities A1-A10, fija write scope, verificación y output schema.
aliases:
  - p3-canonical-linter-spec
tags:
  - kind/doc
  - project/agentsos
  - tech/agents-os
---

# P3 — Canonical / Deprecation Linter: Spec del Parent (binding para P3-B)

- Entrada: [[80-agents/tools/canonical-linter/artifacts/p3-canonical-model.md|p3-canonical-model]] (P3-A), reconciliado contra las autoridades vigentes sin contradicciones factuales. Este spec es la única autoridad de implementación junto con el modelo; lo no fijado aquí queda como está en el modelo.
- Principios: no duplicar tooling existente (validate_schema_contract/lint.py/doctor/harness L0/context-budget M16/M14); toda regla cita autoridad; sólo MACHINE-DETERMINISTIC produce FAIL; findings se registran, nunca se auto-corrigen; KISS stdlib; importar el harness como librería (fork prohibido, precedente context-budget).

## 1. Decisiones del parent sobre ambiguities (A1-A10, vinculantes)

- A1 — `archive/` raíz: el linter lo cubre vía CL-10 (WARN report-only con inventario). NO se migra, excluye ni declara nada en este proyecto: la decisión de migración/exclusión pertenece al owner; se registra como hallazgo de sistema para el reporte final.
- A2 — Archivos sueltos en raíz (`cmd/`, `main/`, `output/`, `Sin título.md`, etc.): SIN check (no existe autoridad que fije el layout de raíz). Quedan como limitación declarada; check futuro sólo si el owner declara el layout.
- A3 — Runbooks federados con `status` (caso signals-code-review): el linter NO re-clasifica ni re-emite lo que lint.py cubre (forbidden-field/bad-status). CL-03 emite WARN fuera de memory/internal y cita el vacío. La decisión contrato-vs-corpus es del owner (hallazgo de sistema).
- A4 — Mapa de estructura de agents-os.md: NO normativo para checks de layout. Ningún check FAIL de estructura de directorios en P3.
- A5 — Clase unificada "no-vigente": RATIFICADA como decisión de diseño de la tool: `no_vigente = memory_state ∈ {superseded, archived} ∪ status ∈ {archived, superseded}` (siempre dentro del enum por tipo resuelto vía `load_contract()`); `deprecated`/`deprecating` = sub-clase "en retiro" (vigente pero no autoridad final). La clase debe quedar declarada en el record (`model` o `thresholds`) para comparabilidad.
- A6 — Vocabulario `load_policy`: NO re-emitir (WARN ya declarado del harness C09). Los checks sólo CONSUMEN el valor cuando su regla lo necesita.
- A7 — Copias con `load_policy: always` bajo `40-archive/`: visibles vía CL-09 (WARN). No se normaliza frontmatter de archivo alguno.
- A8 — Fixtures del schema: el linter EXCLUYE explícitamente `80-agents/skills/_shared/fixtures/` del corpus (además de las exclusiones de `iter_vault_md`) y registra la diferencia con `.graphifyignore` como observación del record (hallazgo de sistema, no auto-correctible).
- A9 — Algoritmo de resolución de wikilinks: RATIFICADO: (1) path relativo exacto desde el archivo origen; (2) basename exacto case-sensitive único; (3) si no hay match único, basename casefold único; (4) alias declarado exacto (frontmatter `aliases`); múltiples candidatos → hallazgo WARN "ambiguo" con la lista de candidatos. Targets antes de `#` y `|`; `^block` y vacíos se ignoran. Algoritmo declarado en el README citando hygiene-review y graphify-contract.
- A10 — Doble registro de skills (INDEX ↔ 00-index): permanece WARN declarado (DUAL-REGISTRY-DOMAIN-SYNC); CL-14/15/16 lo citan y jamás lo convierten en FAIL.

## 2. Checks ratificados

Se ratifican CL-01..CL-20 del modelo con su categoría, autoridad, clasificación, severidad y evidencia tal como están definidos en su tabla (sección 4). Recordatorios duros: FAIL sólo en los checks MACHINE-DETERMINISTIC marcados (CL-01, CL-02 [agent_memory y source], CL-04, CL-06, CL-07, CL-11, CL-14, CL-15, CL-16 [destino archive/inexistente], CL-17, CL-18); CL-02 fuera de agent_memory/source y CL-16 en su variante estado-no-vigente son WARN; CL-03, CL-05, CL-08, CL-09, CL-10, CL-12, CL-13, CL-19, CL-20 como máximo WARN. Desduplicación obligatoria por scope (sección 6 del modelo): no re-emitir continuity bajo memory/internal (doctor Check 7), INDEX↔disco de skills (harness L0 REGISTRY-DISK-PARITY + doctor), club always (L0 + doctor Check 3), enums/required/tags (lint.py), frontmatter de archivos del set fijo (CTX-12/M16).

## 3. Semántica de veredictos

- PASS / FAIL / WARN / SKIP idénticos al harness; SKIP siempre con motivo; UNKNOWN nunca se convierte en PASS. Sin gate entre checks (todos estáticos) salvo pre-flight: marker VAULT_ROOT ausente → exit 2; schema-contract o `rules.py` no importables → todos los checks dependientes SKIP con motivo. `--check <id>` es run dirigido por el operador.
- Cada finding conserva: check_id, category, status (veredicto), severity, path, line/ref cuando exista, observed, expected, evidence, confidence (EXACT/INFERRED con regla declarada; el linter no usa ESTIMATED), recommended_action (propuesta, nunca ejecutada), authority.

## 4. Write scope de P3-B (paths permitidos, todo lo demás prohibido)

- `80-agents/tools/canonical-linter/canonical_linter.py` — motor + CLI (`--vault-root`, `--json`, `--check <id>`, `--category <cat>`; exit 0 sin FAIL / 1 con FAIL / 2 sin VAULT_ROOT).
- `80-agents/tools/canonical-linter/selftest.py` — fixtures temporales fuera del vault; cubrir al menos: cada check con caso positivo y negativo, links con heading/bloque/alias/ambigüedad, frontmatter multilínea y quoting, fixture-exclusión, determinismo, marker ausente, input malformado → SKIP/WARN motivado.
- `80-agents/tools/canonical-linter/README.md` — qué chequea, cómo correrlo, qué NO chequea, semántica, cómo agregar un check, limitaciones.
- `80-agents/tools/canonical-linter/results/run-<timestamp>.json` — única escritura del motor.
- `80-agents/tools/canonical-linter/artifacts/p3-implementation-notes.md` — decisiones, evidencia de verificación, resultados de la primera ejecución sobre el vault real, limitaciones.
- PROHIBIDO: modificar autoridades, skills, memorias, corpus, harness, lint.py, doctor, context-budget, el proyecto, AGENTS.md, o los artifacts de otros agents; auto-corregir findings; crear daemons/DB/servicios; persistir paths absolutos de máquina.

## 5. Requisitos de verificación (gate antes de entregar)

(1) Suite completa ejecutada sobre el vault real con counts y findings por check; (2) casos negativos/inyección en tempdir que demuestren FAIL donde corresponde (al menos CL-01, CL-06, CL-14, CL-18) y WARN donde corresponde (al menos CL-08, CL-10, CL-12, CL-19); (3) input malformado → SKIP/WARN motivado, nunca traceback; (4) determinismo — dos runs idénticos salvo run/timestamp/results_file; (5) baseline `git_head` informativo resuelto en VAULT_ROOT; (6) `git status` final limpio fuera del write scope; (7) desduplicación demostrada: ningún finding que solape un check ya cubierto por lint.py/doctor/L0/M16 sin cita al check-id correspondiente.

## 6. Output schema (machine-readable)

```json
{
  "run": "<timestamp>",
  "tool": "canonical-linter",
  "git_head": "<sha informativo en VAULT_ROOT>",
  "vault_root_arg": "<arg o null>",
  "model": {"no_vigente": {"memory_state": ["superseded", "archived"], "status": ["archived", "superseded"]},
            "en_retiro": {"status": ["deprecated", "deprecating"]},
            "wikilink_resolution": "path-relativo > basename exacto > casefold único > alias; ambiguo -> WARN"},
  "checks": [
    {"check_id": "CL-01", "category": "STATUS", "verdict": "PASS|FAIL|WARN|SKIP", "severity": "FAIL|WARN|report",
     "findings": [{"path": "...", "line": 12, "observed": "...", "expected": "...", "evidence": "...",
                   "confidence": "EXACT", "recommended_action": "...", "authority": "..."}],
     "skip_reason": null, "dedup_cites": ["doctor:check_internal_memory_lifecycle"]}
  ],
  "counts": {"pass": 0, "fail": 0, "warn": 0, "skip": 0, "findings": 0},
  "observations": ["A8 fixtures excluidos explícitamente", "..."],
  "ambiguities": []
}
```

- Enmienda del parent (2026-09-13, post-P3-B, ratificada): CL-01 se aplica sólo a `superseded_by` no vacío + estado active (FAIL). Un valor no vacío de `supersedes` junto a `active` es sucesión canónica legítima (00-RESOURCE-WIKI: "la nueva puede enlazar supersedes") y NO es hallazgo; los pares `supersedes`/`superseded_by` siguen verificándose como links en CL-04.
- Los valores de `model` son ilustrativos: la clase unificada y el algoritmo de resolución se declaran en cada record (A5/A9). Compatibilidad futura `agents-os doctor`: campos `check_id/category/verdict/severity/confidence/authority` suficientes para agregación sin abstracción compartida (YAGNI).
