---
type: change_log
schema_version: 1
scope: session
created: "2026-09-04"
updated: "2026-09-04"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities: []
related:
  - "[[2026-09-04-echo-forge-mt5-report-6140-compatible-allowlist]]"
  - "[[2026-09-04-mt5-terminal-build-unsupported]]"
  - "[[2026-09-04-echo-forge-c3-lean-0290-blocked-mt5-build]]"
aliases: []
confidence: verified
source_session: ECHO-FORGE-MT5-REPORT-BUILD-COMPATIBILITY-AND-ALLOWLIST-RCA-V1-TOP
source_feedbacks:
  - "[[2026-09-04-echo-forge-mt5-6140-compat-rca-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-04-echo-forge-mt5-6140-compat-rca

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated
- **Archivo(s):** decisión `2026-09-04-echo-forge-mt5-report-6140-compatible-allowlist` (nueva); known-error `2026-09-04-mt5-terminal-build-unsupported` (mitigación + HTM durable); decisión C3 0.2.90 (related + camino de desbloqueo, veredicto C3 intacto); checkpoint interno C3 0.2.90; tarea puente del proyecto Echo Forge; agent run; feedback; este change log.

## Motivo

- Cerrar el RCA TOP de compatibilidad 6090 vs 6140: el HTM físico CERT-A es `mt5-report.v1` no certificado; la autoridad de builds debe ser allow-list explícita; C3 sigue BLOCKED/CLOSED.

## Fuentes usadas

- symphony HEAD `32d0740`; SPEC-PARSER + CORPUS 4 fixtures; Temporal/PostgreSQL/MinIO read-only (Campaign `baeb747d…`, HTM SHA `efbd37e4…`); probe de Parse/Normalize con bypass exclusivo del gate de build.

## Resolución aplicada

- Decisión: `COMPATIBLE_WITH_MT5_REPORT_V1` + `EXPLICIT_CERTIFIED_BUILD_ALLOWLIST` + OPTION B (no pin). Sin source, sin release, sin mutar C3.

## Validación

- `Parse(6140)` = `ErrBuildNotSupported`; bypass heading único → Parse nil, 7 crosschecks PASS, Normalize COMPLETE 43 trades. Dirty preexistente del repo symphony no tocado.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- No aplica: no hubo mutación de producto. Las notas de vault pueden revertirse si el lead rechaza la allow-list; la evidencia física 6140 permanece en MinIO.
