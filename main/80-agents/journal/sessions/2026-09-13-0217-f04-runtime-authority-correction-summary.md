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
aliases: []
confidence: high
source_session: 2026-09-13-0217-f04-runtime-authority-correction
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

%% Filename: YYYY-MM-DD[-HHMM]-<human-topic>-summary.md. Never use UUIDs/hashes as visible names; put external IDs in source_session. %%

# F-04 Runtime Authority Correction — 2026-09-13

> [!info]+ Session summary L1
> Resumen operativo. Para beta queda fuera del corpus normal de Graphify.

## Objetivo

- Corregir la interpretación del intento anterior y probar la autoridad Stager real de `0.2.98` sin republish ni cambio de product code.

## Contexto cargado

- Agents OS, router Aranea, `aranea-ssh`, `sqx-deployer`, `deployment-proof`, runtime proof, release certification, F-04 SPEC/proyecto y cierres físicos previos.

## Trabajo realizado

- Baseline remoto PASS: `origin/feature/f04-magic-version-handoff == b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43`.
- Release integrity PASS: `0.2.98`, seis artefactos con tamaños/SHA256 coincidentes y `vcs.revision` exacta; no se construyó ni publicó otra vez.
- Autoridad real Linux PASS: Zeus, Hera y Kronos ejecutan `/opt/stager/releases/0.2.98/bin/symphony` bajo `stager-runtime.service`, con Stager `CURRENT/PENDING=0.2.98`, activación `phase=committed` y poller `sqx-main-queue`.
- Corrección: `/opt/symphony/CURRENT`, `/opt/symphony/current` y `/var/lib/symphony/PENDING` son legacy/no-authoritative; la conclusión previa `0.2.98 absent` no fue probada.
- Windows no probado: `mt5-kronos` viewer rechazó lecturas simples con `POLICY_DENIED`; no se usó operator sólo para inspección.

## Artifacts creados o modificados

- Proyecto F-04 y padre actualizados con la autoridad corregida; resumen, agent run, change log y feedback materializados.

## Memoria propuesta o creada

- No se creó memoria L3: el hallazgo se registra como actualización de proyecto y evidencia de sesión.

## Decisiones

- No generar WorkflowID/RunID/FlowRunRef ni avanzar a LICENSE/T2.12/T2.11 mientras Windows permanezca UNKNOWN.
- No ejecutar recuperación Stager: Linux ya está activo y el estado Windows no es observable con autoridad viewer.

## Pendiente

- `ROLLOUT_PROOF: INCONCLUSIVE`; `PHYSICAL BLOCKED — ENVIRONMENT — RUNTIME_AUTHORITY_GAP`.
- Habilitar una lectura viewer admisible para `mt5-kronos`, repetir rollout proof y sólo con los cuatro runtimes probados continuar LICENSE → T2.12 → T2.11. T2.13 permanece OPEN/fuera de scope.
