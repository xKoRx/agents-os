---
type: change_log
schema_version: 1
scope: session
created: "2026-08-27"
updated: "2026-08-27"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related:
  - "[[2026-08-27-zcode-glm-5-3-sqx-cross-flowrun-historical-source-fanout-rca-top]]"
aliases: []
confidence: verified
source_session: SQX-CROSS-FLOWRUN-HISTORICAL-SOURCE-FANOUT-RCA-TOP
source_feedbacks:
  - "[[2026-08-27-sqx-historical-fanout-hidden-cardinality-test-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - project/echo-forge
---

# 2026-08-27-sqx-cross-flowrun-historical-source-fanout-rca

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** conflict-resolution
- **Archivo(s):**
  - `10-projects/Echo Forge/agentes/Echo Forge - Arquitectura de Datos y Migración de Persistencia.md` (checkpoint append-only con el challenge/amendment del INSERTION_POINT y la corrección mínima F1–F23).

## Motivo

Un review independiente del commit `fd042fb` (feat(sqx): resolve historical durable sources) descubrió un defecto material de cardinalidad/orquestación: el step `resolve_historical_source` dentro de ProjectActivity resuelve el cohort histórico completo (N StrategyArtifacts) en un único InputBatch, pero `prepareDurableRetesterInput` y `prepareDurableOptimizerInput` exigen exactamente 1 upstream strategy y el subject STRATEGY de StageExecution se deriva de un único StrategyRef. La capa de datos de la resolución histórica (RCA @`2b73dc3`) sigue válida; el defecto es del boundary de orquestación.

## Fuentes usadas

- Repo `xKoRx/symphony` @ `fd042fb` (read-only; 4 auditorías subagente paralelas + spot-checks verbatim padre); specs `FEAT-SQX-CROSS-FLOWRUN-REUSE/{SPEC,TOP-DECISIONS}.md` §12/§8 (amendments de `fd042fb`); certificaciones previas E2E 0.2.73/0.2.74 (cohorts BUILDER 20, RETESTER 12+3 empty) citadas desde checkpoints.

## Resolución aplicada

Challenge autorizado al INSERTION_POINT «step dentro de ProjectActivity antes de prepare_input» ACEPTADO y AMENDADO: la resolución del cohort histórico pasa a una Activity estrecha e independiente (`resolve_historical_cohort`) invocada UNA vez por GenericSQXWorkflow en el boundary del grupo durable cuando el batch inicia vacío y se declara SourceFolder histórico, reemplazando `list_strats` para ese caso; devuelve `ActivityResponse[runtime.StratBatch]` con Keys+Origin+StrategyArtifacts exactos (orden `_id ASC`); el fan-out usa el chunking `batch_size` existente con proyección exacta per-slice (patrón `batchKeysForExactArtifacts`); membership REPROCESSED se registra cohort-level una vez por estrategia antes del fan-out; el step de ProjectActivity se REMUEVE para garantizar una sola ruta canónica; Retester/Optimizer conservan cardinalidad 1 y contracts intactos; SOURCEFOLDER_STILL_SUFFICIENT YES con USER_CONFIG_CHANGE STRUCTURAL_ONLY (group+batch_size existentes, sin campos nuevos); regression gate futuro DURABLE_HISTORICAL_LIST_STRATS_CALLS: ZERO.

## Validación

- PASS: doble incompatibilidad N→1 demostrada por código (guardas `len(bindings) != 1` en steps.go:470-471/557-558 y `ResolveSubject` subject.go:103); mecanismo de fan-out real identificado (chunking de grupo en GenericSQXWorkflow, no GroupSQXWorkflow ni ProjectActivity); happy-path test previo eludía el desacuerdo recortando el cohort a `[:1]`; HEAD == baseline real (typo SHA de 39 chars en handoff anterior confirmado); repo sin cambios por diseño read-only.
- Nota: proofs F13/F14 son analíticos sobre cohorts ya certificados físicamente en sesiones previas; la certificación runtime queda para el E2E posterior a la corrección.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

Reversible documentalmente: revertir el checkpoint append; no se tocó código, schema, migraciones ni specs del repo.
