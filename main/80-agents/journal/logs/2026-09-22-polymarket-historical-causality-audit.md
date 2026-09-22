---
type: change_log
schema_version: 1
scope: session
created: "2026-09-22"
updated: "2026-09-22"
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
application:
entities: []
related:
  - "[[Polymarket Engine — Historical Causality Architecture Audit]]"
  - "[[2026-09-22-codex-unknown-polymarket-historical-causality-audit]]"
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

# 2026-09-22-polymarket-historical-causality-audit

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated / conflict-resolution
- **Archivo(s):**
  - [[Polymarket Engine — Historical Causality Architecture Audit]], entrega solicitada por owner.
  - [[Polymarket Engine — MVP]], enlace y estado vigente, sin editar M1/M2 congelado.
  - [[Polymarket Engine — Continuidad Five-POC 2026-09-20]], §17 y aclaración del diagnóstico L2 supersedido.
  - [[2026-09-22-codex-unknown-polymarket-historical-causality-audit]], registro de revisión/tests.

## Motivo

Auditar si el camino histórico impide información futura y estados inválidos; entregar SPEC acotada y mandato de implementación sin modificar código ni ejecutar búsqueda de señales.

## Fuentes usadas

MVP M0/M1 Astra-Fable/reconciliación/freeze/M2; informes históricos y forense; checkout físico `xKoRx/polymarket-engine master@09e8c76`, código `66486ac`, SHA remoto confirmado; fuentes C01–C16/F01 de la auditoría.

## Resolución aplicada

Dictamen `NOT_CERTIFIABLE_END_TO_END`, nueve findings con límites explícitos. Se diferencia salida terminal de Qualities de la ruta real de Strategy; set/delete del engine correcto. Lectura as-of es cumplimiento M1 pendiente, no nueva autorización de modelo. No se resucita drift 66–85% supersedido. SPEC HCA-1 S1–S6, gates H01–H11, cinco decisiones owner abiertas. Resultados físicos de datos permanecen reportados/UNVERIFIED en este shot.

## Validación

Lectura física y seis suites existentes con `GOPROXY=off GOSUMDB=off go test -count=1 ./internal/histimport ./internal/books ./internal/marketview ./internal/regimes ./internal/frames ./internal/replay`: 6/6 PASS (Go 1.27.1). Nuevos gates NOT_RUN. Sin patch/commit/push de código, sin backtest, sin OOS ni infraestructura. Validación documental targeted y comparación de sección M1/M2 contra versión anterior antes de entregar.

Lint estricto de los cinco documentos: ERROR=0, WARN=0; `git diff --check` limpio. Se añadieron sólo los encabezados canónicos ausentes Propósito/Contenido a continuidad. Sufijo congelado del MVP desde `## M1 — ASTRA Architecture Proposal` idéntico byte a byte a `ddfd28a2`, SHA-256 `889d08dd164d7a04ca99d5c06b94c29e587771956237577be6394eef8c9dd633`. El sync automático del vault creó checkpoints intermedios de la entrega; no se alteró ni configuró ese mecanismo.

## Compartibilidad

- **Scope:** local.
- **Redacción revisada:** sin secretos ni payloads raw; referencias internas necesarias al proyecto, código y evidencia.

## Rollback

Revertir sólo esta entrega documental y sus enlaces por archivo/hunk, preservando cambios concurrentes. No revertir el proyecto entero ni modificar el repo del engine.
