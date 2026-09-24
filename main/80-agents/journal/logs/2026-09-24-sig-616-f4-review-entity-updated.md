---
type: change_log
schema_version: 1
scope: session
created: "2026-09-24"
updated: "2026-09-24"
area: "[[Meli]]"
project: "[[SIG-616 — Autorización de operaciones por equipo]]"
application: "[[rio-playmaker]]"
entities:
  - "[[SIG-616 — Autorización de operaciones por equipo]]"
  - "[[rio-playmaker]]"
related:
  - "[[SPEC técnica — Slice 4 — Relaciones y pipelines]]"
  - "[[SPEC técnica — Slice 5 — Actions restantes]]"
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
---

# SIG-616 — resolución del review de F4

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated / conflict-resolution
- **Archivo(s):**
  - `10-projects/Meli/SIG-616 — Autorización de operaciones por equipo/SIG-616 — Autorización de operaciones por equipo.md`
  - `10-projects/Meli/SIG-616 — Autorización de operaciones por equipo/SPEC técnica — Slice 4 — Relaciones y pipelines.md`
  - `10-projects/Meli/SIG-616 — Autorización de operaciones por equipo/SPEC técnica — Slice 5 — Actions restantes.md`
  - `10-projects/Meli/SIG-616 — Autorización de operaciones por equipo/Descripción PR — rio-playmaker — Slice 4.md`

## Motivo

- La nota F4 previa preservaba relaciones cross-DP y el precheck ACME del delete de Data Products sin equipo. El owner resolvió aplicar la regla same-DP de SIG-616 y omitir ACME cuando el DP no tiene `teamName`.
- Estas son decisiones vigentes del proyecto y comportamiento implementado, no aprendizaje genérico de agentes.

## Fuentes usadas

- Instrucciones del owner en esta sesión, comentarios de David en [PR #1181](https://github.com/melisource/fury_rio-playmaker/pull/1181), SIG-616/SIG-621 y diff local `40d5f9b22`.
- `./scripts/run-agentic-testing-contract.sh`, `./gradlew check --rerun-tasks --no-daemon --no-build-cache` y JaCoCo pasaron localmente.

## Resolución aplicada

- Se reemplazó la compatibilidad cross-DP anterior por validación same-DP en create/update/delete. Update conserva cambios de endpoints dentro de un solo Data Product; los datos cross-DP persistidos requieren auditoría antes del rollout.
- En cascade sin equipo se omiten precheck ACME heredado y guard F4; con equipo y sin proyecto se mantiene el precheck heredado.
- Se dejó en F5 sólo la evaluación futura de un helper para los dos métodos de `ActionAuthorizationService`, conservando lookup exacto y wildcard como políticas distintas.

## Validación

- 20 selectores focalizados y 2 checks L0/LOCAL_STACK con cleanup pasaron; 4.009 tests, 0 fallas, 2 skips; 97,07% de cobertura global. `GenerateDocTest` pasó sin diff de OpenAPI. GitHub confirmó push, descripción y nueve respuestas inline. CI #5496 y checks asociados pasaron; review humano, sub-SPEC y smoke siguen pendientes.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Si el owner revierte estas decisiones, restaurar las reglas en código, tests y notas mediante un cambio revisado; no borrar el historial de esta resolución.
