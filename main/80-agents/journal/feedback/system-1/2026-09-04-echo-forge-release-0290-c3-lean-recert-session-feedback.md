---
type: feedback
schema_version: 1
scope: session
created: 2026-09-04
updated: 2026-09-04
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
  - "[[AGENTS OS]]"
related:
  - "[[2026-09-04-echo-forge-c3-lean-0290-blocked-mt5-build]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
agent_run: "[[2026-09-04-zcode-glm-echo-forge-release-0290-c3-lean-recert-blocked]]"
session_goal: Release 0.2.90 --release-only + C3 lean recert (CERT-A/B) física
source_session: ECHO-FORGE-RELEASE-0.2.90-AND-C3-LEAN-RECERT-NORMAL
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/echo-forge
  - agent/system1
---

# Session Feedback - 2026-09-04 - echo-forge-release-0290-c3-lean-recert

## Context

- Agent surface: [[ZCode]] (workspace vault Obsidian; repo operado en workspace Go `xKoRx/symphony`)
- Agent model: GLM-5.3-Flash (host-reported)
- Agent run: [[2026-09-04-zcode-glm-echo-forge-release-0290-c3-lean-recert-blocked]]
- Session goal: autoridades, release 0.2.90, flota 4/4, CFX, CERT-A→CERT-B, dedupe/redelivery/reads/topología/replay, cierre C3
- Main entity: [[Echo Forge]]
- Skills used: agents-os-bootstrap; runbooks symphony-release-certification / symphony-prod-probe / symphony-worker-runtime-proof / echo-forge-workers-shared-access (vault) + fleet/SSH table del AGENTS.md del repo
- Retrieval mode: continuidad global + decisiones/known-errors/plan C3 (when_relevant) + runbooks de la app
- Artifacts changed: decisión BLOCKED, known-error MT5 build (nuevo), known-error reretester (Resolución), checkpoint proyecto, change log, agent run, este feedback

## Scores

- Startup clarity: 5
- Retrieval usefulness: 5
- Skill fit: 5
- Template fit: 5
- Closeout friction: 4
- Overall confidence: 5

## What Complicated The Session Most

- Observation: el bloqueo real (terminal MT5 auto-actualizado a build 6140 vs `SupportedBuild=6090` congelado) es invisible para todos los gates previos — flota, release y CFX PASS completos; sólo emerge cuando un backtest completa y se reconcilia. El smoke de cancelación 0.2.88 no puede detectarlo porque nunca reconcilia un reporte de éxito.
- Why it was hard: distinguir "defecto de producto" vs "drift ambiental sobre contrato congelado" exige leer el error exacto del history (ev=210), el binario físico del terminal y el constant congelado; el resultado físico (`MT5BacktestArtifactWorkflow` success) contradice en apariencia el fallo del Generic.
- Proposed improvement: probe de flota que verifique el build del terminal MT5 contra `SupportedBuild` en el preflight de certificación (lectura `FileVersion` por SSH), y known-error o checklist MT5 que se consulte antes de cualquier CERT con backtest; documentar que el smoke de cancel no cubre reconcile de éxito.

## Most Useful Part Of Sistema 1

- El runbook `symphony-prod-probe` + patrón DI (`InitSelective`) resolvió en una sola herramienta read-only todo el polling (infra/queue/campaigns/history/cfx/verifyread); el AGENTS.md del repo con la tabla de flota y credencial SSH evitó perder tiempo de acceso al host Windows.

## Sistem 2 / Vault

- Notas creadas/actualizadas quedan enlazadas desde el checkpoint del proyecto; `materialize_schema_note.py` funcionó sin fricción para decision/known-error.

## Signals

- Sin fricción de permisos; sin dudas del usuario (sesión autónoma por prompt de misión).
