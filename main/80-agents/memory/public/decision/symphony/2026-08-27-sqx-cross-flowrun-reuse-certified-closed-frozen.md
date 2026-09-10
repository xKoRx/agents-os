---
type: decision
schema_version: 1
scope: project
created: "2026-08-27"
updated: "2026-08-27"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
related:
  - "[[2026-08-27-builder-historical-templates-certified-closed]]"
  - "[[2026-08-27-zcode-glm-5-3-sqx-cross-flowrun-reuse-final-closure-top]]"
aliases: []
confidence: verified
source_session: SQX-CROSS-FLOWRUN-REUSE-FINAL-CLOSURE-TOP
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - tech/sqx
  - tech/temporal
  - scope/public
  - scope/project
---

# FEAT-SQX-CROSS-FLOWRUN-REUSE certificada cerrada y congelada

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- Cierre arquitectónico FINAL read-only sobre `xKoRx/symphony` @ `7d2199a55a844a1bf83c04c27a9fe9ebc0754587` (HEAD == origin/master), reconciliando SPEC/TOP-DECISIONS con el código real y los E2E físicos 0.2.73–0.2.76.
- Los ocho contratos C0–C8 (identity v2, builder retry recovery, FlowRun lifecycle, ownership single-owner + fan-out, historical resolution, downstream reuse, cohort fanout, builder templates) están certificados por E2E físico.

## Decisión

- `FEAT-SQX-CROSS-FLOWRUN-REUSE`: **CERTIFIED_CLOSED / FROZEN**; no queda gap requerido de semántica de negocio.
- Invariantes congeladas: (1) un FlowRun nuevo puede leer outputs históricos de stage; (2) la Strategy downstream conserva su StrategyRef; (3) toda lectura histórica crea StageExecution/Evaluation nueva (provenance); (4) Builder template consume el cohort histórico como input REUSED; (5) la identidad de un candidate nace sólo de su canonical output; (6) los writes de un output namespace tienen un único FlowRun owner; (7) los namespaces históricos son read-only cross-flow; (8) ninguna identidad durable se infiere de filenames MinIO; (9) Mongo Evaluation + StrategyRef + ArtifactRef exacto son la autoridad de evidencia; (10) Temporal Reset no tiene rol de negocio en el reuse.
- Roles de membership congelados: PRODUCED (originada por este FlowRun), REPROCESSED (Strategy existente en stage downstream de otro FlowRun), REUSED (consumida como Builder template, no reprocesada como output); IMPORTED queda reservada sin writers.
- La anomalía «objetos ausentes en 05_retester» se clasifica como falso positivo del audit (la carpeta física es `05_reretester`; los 4 objetos existen con sha256 byte-exacto); no hay defecto de producto.

## Rationale

- Los 14 símbolos de contrato mapean a código verificado en `7d2199a` y cada capacidad tiene E2E físico con release conocido (ownership 0.2.73, fan-out 0.2.74, historical reuse 0.2.75, builder templates 0.2.76).
- La verificación física read-only de PG/Mongo/MinIO confirmó consistencia byte-exacta entre evidencia sellada y objetos físicos en el namespace cuestionado.

## Consecuencias

- Requerido antes de producción (plano de integridad, no semántica del feature): write-once físico del artifact plane (conditional create, SDK primero) y verificación digest/size en downloads históricos; Retester/Optimizer exact recovery queda gated tras el write-once.
- Diferido/hardening: pre-007, Final Reretester direct sourcing (NOT_REQUIRED, es DecisionRef-driven), automatización UX del binding CFX, lineage individual template→candidate, INPUT-role binding, fail-fast ante objetos ausentes.
- Existe deuda documental stale (FD-9 «MISSING» vs §14 implementado; §8 gaps agotados; fila SPECS.md desactualizada): se propone un NORMAL docs-only antes del siguiente track; el feature sigue CLOSED.

## Alternativas descartadas

- No se reabrió ningún contrato certificado: el challenge a la premisa de la anomalía 05_retester se resolvió con evidencia física (falso positivo) en vez de RCA/backlog.
- No se promovió hardening a semántica requerida del feature: write-once y digest verification quedan como items de producto pre-production, no como gaps del feature.
