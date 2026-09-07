---
type: change_log
schema_version: 1
scope: session
created: 2026-08-10
updated: 2026-08-10
area: "[[Personal]]"
project: "[[AGENTS OS - Fase 3]]"
entities:
  - "[[AGENTS OS]]"
  - "[[AGENTS OS - Fase 3]]"
related:
  - "[[executable-schema-contract-versioning]]"
  - "[[2026-08-10-agents-os-g1-enforcement-session-feedback]]"
  - "[[2026-08-10-agents-os-g1-scoped-materializer-raw]]"
aliases: []
confidence: verified
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - project/agents-os
  - change/created
  - change/updated
---

# AGENTS OS Fase 3 — F1 contrato versionado y templates

## Cambio

- **Tipo:** created / updated.
- **Autoridad:** `80-agents/skills/_shared/schema-contract.md`.
- **Gates:** validator/resolver en `80-agents/skills/_shared/scripts/`.
- **Templates:** `70-templates/` y `80-agents/templates/`.
- **Guías/runtime:** metadata schema, note types, convenciones, lifecycle y
  comentario de transición del lint legacy.
- **Estado:** [[AGENTS OS - Fase 3]] y su tarea puente en [[AGENTS OS]].

## Motivo

Ejecutar T1.1–T1.5: eliminar contratos paralelos, versionar schema/templates,
cubrir todo tipo creable y hacer que lifecycle/create falle cerrado antes de
la fase de lint preventivo.

## Fuentes usadas

- [[AGENTS OS - Fase 3]], Fase 1 y G1.
- `80-agents/skills/_shared/metadata-schema.md` anterior.
- `80-agents/skills/_shared/note-types.md`.
- `90-system/convenciones.md`.
- Templates S1/S2 y lint legacy aceptado en Fase 2.

## Resolución aplicada

- Se creó un contrato JSON v1 dentro de Markdown con semántica current,
  legacy read-only, future reject y migradores explícitos.
- Se definieron envelope común, extensiones S1/S2, tipos de datos, campos
  required/optional/forbidden, status, tags y secciones mínimas.
- Se mapearon 43 tipos a 42 templates canónicos; `scratch` quedó exento como
  derivado. Dos templates derivados y un fragmento quedaron justificados.
- Se agregaron 12 templates faltantes y `schema_version: 1` a todos los
  templates con frontmatter.
- Se agregaron fixtures current v1, legacy sin versión y future v2 inválida.
- Lifecycle/create ahora resuelve tipo→template+versión y rechaza tipos
  desconocidos, exentos o contratos inválidos.
- Tras review del owner, se centralizó la creación en
  `materialize_schema_note.py`: no sobrescribe, valida contrato y materializa
  desde el mapping. El validator exige que 13 skills creadoras deleguen ahí.
- [[Economía de Tokens]] quedó como invariante explícita: resolver y validar es
  local/programático; el contrato no se agregó al always-load ni al hot path.
- Una auditoría del índice detectó ruido residual: `299` nodos de templates y
  `10` de fixtures. `.graphifyignore` ahora excluye ambos inputs; el
  materializador y el validator siguen leyéndolos directamente del filesystem.
  La regla quedó durable como R25/D15 en el proyecto.
- Durante la verificación, una edición concurrente migró el template
  `application` a la separación estable/semi-estable/volátil sin cambiar el
  mapping contractual. Se reconcilió el perfil v1, incluyendo
  `last_verified`/`confidence`, y se agregó `schema_version: 1` a las 10
  aplicaciones RIO recién creadas; las aplicaciones antiguas permanecen
  legacy unversioned read-only.
- El feedback de cierre Stager reveló que el materializador ejecutaba el
  auditor global antes de resolver el tipo pedido. Se separó validación scoped
  para create de validación global para contrato/Doctor/release; no existe
  bypass y el tipo solicitado sigue fallando cerrado.
- El lint all-vault conserva su baseline legacy hasta F2, donde debe consumir
  el contrato sin duplicar constantes.
- La elección de formato y semántica de compatibilidad se persistió en
  [[executable-schema-contract-versioning]].

## Validación

- Contract validator: `version=1`, `types=43`, `canonical_templates=42`,
  `derived=2`, `fragments=1`, `fixtures=3`, `creation_entrypoints=13`,
  `errors=0`.
- Resolver: `project` y `storage` resuelven; `scratch` y tipo desconocido se
  rechazan.
- Lint dirigido: `ERROR=0 WARN=0`, 51 fuentes.
- Doctor estricto: `HIGH=0 MEDIUM=0 LOW=0`, startup≈5199.
- Lint dirigido del lote: `0 ERROR / 0 WARN`. Baseline all-vault al cierre:
  `41 ERROR / 81 WARN`; el delta `40→41` proviene de
  `30-resources/methodologies/data-mesh.md` (`sources` ausente), nota externa
  al lote F1. No se corrige ni atribuye a AGENTS OS sin autorización.
- Graphify update final verde; contrato y Fase 3 resuelven por título canónico.
- Reindex anti-ruido: `5287/6076` → `4978/5774` nodos/edges; `0` nodos de
  templates y `0` de fixtures. El contrato tiene grado `4` y el materializador
  grado `6`; no se crearon hubs ni nodos de facets `type`, `schema_version`,
  `project` o `kind/*`. Un diff entre reindexaciones atribuyó la variación
  global posterior a ediciones concurrentes de dos notas RIO; el gate estable
  es `0` por los paths excluidos, no el total mutable del vault.
- Reconciliación concurrente: validator pasó transitoriamente a `errors=2` y
  volvió a `errors=0`; lint dirigido de template + 10 aplicaciones RIO +
  proyecto/log quedó en `0 ERROR / 0 WARN`. Dry-run/stdout del materializador
  `application` resolvió el template y renderizó `schema_version: 1` con la
  nueva estructura.
- Regresión scoped: `unrelated_drift=isolated` y
  `requested_type_drift=blocked`; validator global `errors=0`, validator
  `--type change_log` `errors=0` y dry-run del materializador resolvió S1 sin
  escribir. G1 fue aceptado explícitamente por el owner.

## Compartibilidad

- **Scope:** local.
- No contiene secretos ni paths absolutos persistidos.

## Rollback

- Restaurar autoridades y templates previos junto con el lint legacy.
- Eliminar contrato, validator/resolver, fixtures y templates nuevos como un
  solo lote; no dejar mappings parcialmente revertidos.
- Devolver G1 a `pending` y la tarea puente a WIP si el owner rechaza el gate.
