---
type: change_log
schema_version: 1
scope: session
created: "2026-08-10"
updated: "2026-08-10"
area: "[[Personal]]"
project: "[[AGENTS OS - Fase 3]]"
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[AGENTS OS Executable Schema Contract]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - project/agents-os
  - change/updated
---

# AGENTS OS Fase 3 — F2 lint contractual y gate no-new-debt

## Cambio

- **Tipo:** created / updated.
- **Autoridad:** `80-agents/skills/_shared/schema-contract.md` incorporó la política ejecutable del lint, baseline, strict y reglas semánticas.
- **Lint:** `80-agents/skills/agents-os-entity-lifecycle/scripts/lint.py` fue refactorizado para consumir el contrato sin constantes de schema paralelas.
- **Baseline:** `80-agents/skills/agents-os-entity-lifecycle/lint-baseline-v1.json` registra fingerprints SHA-256 determinísticos del corpus.
- **Fixtures:** se agregaron casos v1 de tipos de datos, routing, tags, secciones y una regresión E2E read-only/no-new-debt.
- **Integración:** `95-graphify/dist/graphify-obsidian` y su copia instalada ejecutan el gate antes de `update` y fallan cerrado ante deuda nueva o ausencia del lint.
- **Estado:** [[AGENTS OS - Fase 3]] quedó con F2 completa y G2 aceptado por el owner; F3 está habilitada sin iniciar y su tarea puente en [[AGENTS OS]] volvió Review→WIP para T3.1/G3.

## Motivo

Ejecutar T2.1–T2.5: detener deuda nueva antes del retrofit, exigir schema actual a notas nuevas o modificadas y mantener Graphify operativo sobre la deuda heredada sin depender de Git.

## Fuentes usadas

- [[AGENTS OS - Fase 3]], Fase 2 y G2.
- `80-agents/skills/_shared/schema-contract.md` y sus fixtures de versión.
- `80-agents/skills/agents-os-entity-lifecycle/scripts/lint.py` legacy y el gate pre-execute aceptado en Fase 2.
- `90-system/convenciones.md` y `80-agents/skills/agents-os-entity-lifecycle/SKILL.md`.

## Resolución aplicada

- El lint deriva tipos, lifecycle, requeridos/prohibidos, tipos de datos, tags, routing, secciones, fronteras y reglas semánticas desde el bloque JSON canónico.
- `--strict <path...>` bypassa exclusiones, exige la versión actual y cero findings sobre rutas explícitas; no necesita detectar cambios mediante Git.
- `--gate` calcula fingerprints de todos los findings y permite sólo que el set actual sea subconjunto del baseline; un warning o error nuevo bloquea.
- `--emit-baseline` imprime un candidato determinístico a stdout y mantiene el lint completamente read-only.
- Los escalares opcionales vacíos materializados por templates son válidos; los campos requeridos vacíos continúan fallando. Esta regresión cubre la paridad materializador→strict.
- El baseline contractual inicial quedó en `94 ERROR / 81 WARN`: 35 unknown-type, 32 missing-field, 12 missing-tag, 11 missing-section, 3 bad-status, 1 bad-owner, 78 no-frontmatter y 3 no-type.
- El delta frente al lint legacy `41/81` no es regresión del corpus: son reglas v1 que el lint anterior no aplicaba a notas ya marcadas `schema_version: 1`; el retrofit F6 se amplió con esos findings.
- Las autoridades modificadas en F2 fueron regularizadas y pasan lint strict `0/0`.
- El wrapper conserva consultas sin reindex y sólo ejecuta el gate en `update`; la copia instalada quedó byte-identical a la fuente del vault.

## Validación

- Contract validator: `version=1`, `types=43`, `canonical_templates=42`, `fixtures=3`, `creation_entrypoints=13`, `errors=0`.
- Gate all-vault: `ERROR=94 WARN=81 baseline_ERROR=94 baseline_WARN=81 new=0 resolved=0`, GO.
- Lint strict dirigido sobre contrato, lifecycle, convenciones, cockpit y planificador: `0 ERROR / 0 WARN`.
- Regresión: fixtures válidas e inválidas, campo opcional vacío, legacy read-only, versión futura, tipos de datos, routing, tag prohibido, sección faltante, hash read-only, baseline decreciente y deuda nueva: verdes.
- Wrapper: fuente canónica y copia instalada idénticas; `bash -n` verde.
- E2E `graphify-obsidian update`: exit 0, `5041 nodes / 5890 edges / 499 communities`; el gate corrió antes del extractor con `new=0`.
- Retrieval: `explain` resolvió [[AGENTS OS - Fase 3]] y [[AGENTS OS Executable Schema Contract]].
- Aceptación humana: el owner aceptó G2 el 2026-08-10 y autorizó el handoff a un agente fresco para F3.

## Compartibilidad

- **Scope:** local.
- **Redacción revisada:** no contiene secretos ni paths absolutos persistidos.
- El baseline es portable y no depende de timestamps, Git, IDE, modelo ni cliente.

## Rollback

- Restaurar el lint legacy, retirar el bloque `lint` del contrato y eliminar baseline/fixtures como un único lote.
- Restaurar el wrapper warn-first tanto en la fuente canónica como en la copia instalada.
- Devolver G2 a `pending`, T2.1–T2.5 a su estado anterior y la tarea puente a WIP.
