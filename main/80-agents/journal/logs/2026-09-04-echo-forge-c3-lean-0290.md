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
  - "[[2026-09-04-echo-forge-c3-lean-0290-blocked-mt5-build]]"
  - "[[2026-09-04-mt5-terminal-build-unsupported]]"
  - "[[2026-09-04-reretester-single-artifact-contract]]"
aliases: []
confidence: verified
source_session: ECHO-FORGE-RELEASE-0.2.90-AND-C3-LEAN-RECERT-NORMAL
source_feedbacks:
  - "[[2026-09-04-echo-forge-release-0290-c3-lean-recert-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-04-echo-forge-c3-lean-0290

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated
- **Archivo(s):** decisión `2026-09-04-echo-forge-c3-lean-0290-blocked-mt5-build`, known-error `2026-09-04-mt5-terminal-build-unsupported` (nuevo), known-error `2026-09-04-reretester-single-artifact-contract` (Resolución actualizada), checkpoint del proyecto Echo Forge, agent run, feedback y este change log.

## Motivo

- Cerrar la misión con veredicto y evidencia: CERT-A 0.2.90 falló en `mt5_reconcile_v1` por build MT5 6140 no soportado por el parser congelado; DEFECT RULE obliga a preservar evidencia, no parchear y volver al lead.

## Fuentes usadas

- git/`go version -m` sobre artefactos 0.2.90; MinIO manifest publicado; DescribeTaskQueue pre/post; describe/history Temporal de parent y Generic; PostgreSQL `sqx.forge_campaigns`/`flow_runs`/`stage_executions`; `LoadForgeCampaignResult`; SSH físico a los 4 hosts (binarios, procesos, terminal MT5); probe DI read-only de la sesión (eliminado al cierre).

## Resolución aplicada

- GATES 0–4 PASS; CERT-A nueva `baeb747d…` lanzada y fallida de forma determinista en MT5 reconcile; redelivery idempotente PASS; verified read PASS; topología PASS; sin huérfanos; C3 `BLOCKED / CLOSED`; sin parches, sin release extra, sin writes manuales.

## Validación

- Veredicto soportado por: failure ev=210/220 exacto, terminal físico `5.0.0.6140` (mtime 2026-09-02), `SupportedBuild=6090` en source congelado, smoke 0.2.88 sin reconcile de éxito. Estado del worktree al cierre = dirty preexistente + `deploy/manifest.json` (0.2.90, esperado); probe y worktree de replay eliminados.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- No aplica: la release 0.2.90 es correcta y permanece publicada; las campañas históricas permanecen terminal como evidencia. El desenrollado del terminal MT5 es decisión del lead.
