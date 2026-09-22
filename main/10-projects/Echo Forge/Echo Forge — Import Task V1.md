---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P0
area: "[[Personal]]"
parent: "[[Echo Forge]]"
sprint:
start: 2026-09-21
due:
progress: 75
repo: xKoRx/symphony
jira:
prs:
aliases: []
tags:
  - kind/project
  - area/personal
created: "2026-09-21"
updated: "2026-09-21"
---

# Echo Forge — Import Task V1

## 🎯 Objetivo

- Incorporar estrategias SQX ya retesteadas (databank `Retester/databanks/import` en Zeus/Hera/Kronos) al pipeline durable de Forge SIN ejecutar Builder, mediante cuatro responsabilidades independientes: IMPORT (productor) → CLASSIFICATION (capacidad) → RANKING (capacidad) → SELECTION (task con `source_folder=01_import`), con evidencia durable y certificación física por archivos auténticos. Extensión funcional posterior a Factory V2; no reabre F05.

## 📊 Estado actual

- **IMPLEMENTED + TESTED (cero regresiones vs baseline `745bc8b`); PHYSICAL CERT (G7) BLOQUEADO a autoridad runtime del owner.** Branch `feature/sqx-import-task-v1` (local, sin push). SPEC congelada + 2 amendments de contratos frozen con manager review PENDIENTE (MR-1, MR-2). Campaña B especificada, NO ejecutar.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/symphony | `feature/sqx-import-task-v1` | `codex/f05-release-prep` @ `745bc8b` (release 0.2.105) | Mandato owner 2026-09-21 (IMPORT V1) | `specs/FEAT-SQX-IMPORT-TASK-V1/SPEC.md` + amendments | IMPLEMENTED · tests nuevos verdes · G6 sin regresiones · G7 pendiente RT-1 |

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. %%
> - [x] G0/G1: auditoría contratos + topología hosts + SPEC freeze + amendments #owner/agent #type/dev
> - [x] G2–G5: task import, registro de productores, ranking per-type, selection_snapshot_v1 #owner/agent #type/dev
> - [x] G6: tests §14 nuevos + regresión completa (23 fallos pre-existentes idénticos al baseline, 0 nuevos) #owner/agent #type/dev
> - [r] MR-1/MR-2: manager review de amendments a CLASSIFICATION-EVIDENCE y EARLY-PER-TYPE-RANKING #owner/me #type/pr-review
> - [ ] G7: certificación física vertical slice (runbook listo; requiere Opción A flota o Opción B runtime aislado) #blocked
> - [ ] G8 cierre: push branch + merge owner + release según gates #owner/me #type/dev
> - [ ] Campaña B: congelar parámetros OOS/MT5 y ejecutar tras G7 #owner/me #type/dev

## 📆 Bitácora

- **2026-09-21** — Sesión ZCode/GLM: G0–G6 completos en worktree `/home/kor/go/src/github.com/xKoRx/symphony-import-v1` (4 commits). Flota con worker 0.2.105 corriendo en Zeus ⇒ G7 requiere owner gate. Runbook y receta de config listos.

## 🧭 Decisiones

- D1 desacople por REGISTRO de productores (builder|import), no por relajar el `if` de stage. D2 `IMPORTED` activado como rol origin (reservado por CROSS-FLOWRUN-REUSE). D3 extractor único: plugin Java EchoForgeOverviewExporter modo databank. D4 métricas import = `IMPORTED_HISTORICAL_RESULT` (nunca evaluación Forge). D5 filenames/carriers `builder_*` congelados en V1. D6 selection = task control-plane con snapshot durable insert-once. Detalle: `specs/FEAT-SQX-IMPORT-TASK-V1/TOP-DECISIONS.md`.

## 🔗 Docs / Links

- Parent: [[Echo Forge]] · Entorno: [[Echo + Echo Forge — Environment Contract]]
- Repo specs: `specs/FEAT-SQX-IMPORT-TASK-V1/` (SPEC, TOP-DECISIONS, RUNBOOK G7), `specs/FEAT-SQX-IMPORT-CAMPAIGN-B/SPEC.md`
- Amendments manager review: `FEAT-SQX-DURABLE-CLASSIFICATION-EVIDENCE/AMENDMENT-IMPORT-PRODUCER.md`, `FEAT-SQX-DURABLE-EARLY-PER-TYPE-RANKING/AMENDMENT-IMPORT-PRODUCER.md`
