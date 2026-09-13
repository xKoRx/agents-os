---
type: session
schema_version: 1
scope: session
created: "2026-09-13"
updated: "2026-09-13"
area: "[[Echo]]"
project: "[[Echo Forge — F-04 Magic allocation, version seal and handoff]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[Aranea]]"
related:
  - "[[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]]"
  - "[[aranea-ssh-mcp]]"
aliases: []
confidence: high
source_session: 2026-09-13-f04-mt5-viewer-policy-gap
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

%% Filename: YYYY-MM-DD[-HHMM]-<human-topic>-summary.md. Never use UUIDs/hashes as visible names; put external IDs in source_session only. %%

# F-04 MT5 Viewer Policy Gap — 2026-09-13

> [!info]+ Session summary L1
> Resumen operativo. Para beta queda fuera del corpus normal de Graphify.

## Objetivo

- Cerrar únicamente el gap Windows mt5-kronos sobre la release 0.2.98, sin product code, republish ni bypass de autoridad.

## Contexto cargado

- Agents OS bootstrap/constitution/profile/continuity, router Aranea, aranea-mcps-expert, aranea-ssh-mcp, capability plane, Echo Forge WFM troubleshooting, deployment-proof, e2e-gated-validation, F-04 project/SPEC y D16/D17/D18.

## Trabajo realizado

- Baseline remoto PASS: git ls-remote origin refs/heads/feature/f04-magic-version-handoff = b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43; checkout local dirty y worktrees ajenos preservados.
- Discovery MCP PASS: aranea-ssh expone mt5-kronos como profile viewer; hostname devolvió worker-kronos y whoami devolvió worker-kronos\echo-dev.
- Las operaciones únicas Get-Service -Name StagerRuntime, sc.exe query StagerRuntime, ver, tasklist.exe /FI "IMAGENAME eq sqx-mt5-worker.exe", Get-Process -Name sqx-mt5-worker, Get-ChildItem C:\ProgramData\Stager y where.exe sqx-mt5-worker.exe devolvieron exactamente POLICY_DENIED: Profile "mt5-kronos" is read-only, so "safe" commands are refused. Clear readOnly on the profile to allow them.
- La evidencia de servicio, proceso, effective path, release y poller es read-only; el perfil mt5-kronos es el viewer contractual y las formas mínimas admisibles intentadas fueron policy-denied. Se confirma PHYSICAL BLOCKED — ARANEA MCP POLICY GAP — MT5 VIEWER.

## Artifacts creados o modificados

- Proyecto F-04 y padre actualizados sólo con la corrección de estado; este summary, feedback y change log creados. No se modificó product code, release, input ni configuración remota.

## Memoria propuesta o creada

- No se generó WorkflowID, RunID, FlowRunRef, StrategyRef, Magic, EvaluationRef, StrategyVersionRef, DecisionRef ni HandoffManifest; LICENSE, T2.12 y T2.11 no iniciaron. T2.13 permanece OPEN y fuera de scope.

## Decisiones

- No usar mt5-kronos-operator sólo para inspección. No declarar effective release Windows ni ROLLOUT 0.2.98 PASS.

## Pendiente

- Owner/Manager debe corregir la allowlist viewer Windows o exponer un probe read-only equivalente; después repetir sólo rollout proof sobre 0.2.98, sin republish.

## SESSION CLOSE

- Cierre persistido; resultado exacto: PHYSICAL BLOCKED — ARANEA MCP POLICY GAP — MT5 VIEWER.

## FEEDBACK

- Feedback event-driven persistido por la policy viewer que no permite la evidencia mínima de runtime Windows.
