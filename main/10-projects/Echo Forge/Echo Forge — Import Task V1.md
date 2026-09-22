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

- **PUBLISHED (branch en origin) + TESTED (cero regresiones vs baseline `745bc8b`); PHYSICAL CERT (G7) BLOQUEADO a autoridad runtime del owner.** Branch `feature/sqx-import-task-v1` publicada 2026-09-21 @ origin `5e495ae` (5 commits íntegros; merge-base con `master` = `745bc8b` — nació exactamente del master consolidado, sin rebase; scan de secretos/accidentales limpio antes del push). `master` @ `745bc8b` == release `0.2.105` (consolidación git 2026-09-21; sin commits de Import en master). SPEC congelada + 2 amendments de contratos frozen con manager review PENDIENTE (MR-1, MR-2). Campaña B especificada, NO ejecutar. Política post-consolidación: esta es la ÚNICA rama de desarrollo activa del repo.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/symphony | `feature/sqx-import-task-v1` @ origin `5e495ae` | `745bc8b` (== `master` consolidado, release 0.2.105) | Mandato owner 2026-09-21 (IMPORT V1) | `specs/FEAT-SQX-IMPORT-TASK-V1/SPEC.md` + amendments | PUBLISHED · tests nuevos verdes · G6 sin regresiones · G7 pendiente RT-1 |

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. %%
> - [x] G0/G1: auditoría contratos + topología hosts + SPEC freeze + amendments #owner/agent #type/dev
> - [x] G2–G5: task import, registro de productores, ranking per-type, selection_snapshot_v1 #owner/agent #type/dev
> - [x] G6: tests §14 nuevos + regresión completa (23 fallos pre-existentes idénticos al baseline, 0 nuevos) #owner/agent #type/dev
> - [x] Review independiente ronda 1 (2026-09-22, agentes verificadores contexto fresco): MR-1 **APPROVED**; MR-2 **CHANGES_REQUIRED** (MAJOR H-1: recovery import validaba MetricSet con constantes Builder ⇒ retry post-crash roto; sin test) #owner/agent #type/pr-review
> - [x] Correcciones ronda 2 @ `bed8d31`: Fix A recovery por contrato de productor + tests recovery/evidencia import + binding databank plugin (input para import / output para builder) + mensajes por contrato; regresión = fail-set baseline idéntico; re-review ronda 2 en curso #owner/agent #type/dev
> - [x] Preflight control-plane (RO): Temporal `sqx-dev` OK / flota=`sqx-prop`+`sqx-main-queue` (ETCD production), 0 pollers en cola por defecto; ETCD DEV 40 keys (PG 192.168.31.220/trading_systems, Mongo forge, MinIO 192.168.31.92:9000); MinIO: 11 estrategias .sqx auténticas en `running/wave_2/xau/base/` + convención `00_configs/` con .cfx por stage (sin `EchoForgeImportExporter.cfx` aún — paso owner); canales caídos: aranea-ssh 503 y Mongo RO session-not-found ⇒ preflight host-level (licencia, JAR, passed local, proceso flota) PENDING #owner/agent #type/dev
> - [x] MR-1/MR-2 veredicto formal ronda 2: **APPROVED ambos** (K1–K8 PASS, sin BLOCKER/MAJOR; run `dwfrun-3d728aaa`); headers de amendments actualizados (INDEPENDENT REVIEW APPROVED / RATIFICACIÓN OWNER PENDIENTE) @ `329ee94` #owner/me #type/pr-review
> - [x] Solicitud RT-1 precisa emitida: `specs/FEAT-SQX-IMPORT-TASK-V1/RT1-REQUEST-G7-OPCION-B.md` (host kronos propuesto, cola sqx-import-cert-v1@sqx-dev, prefix ETCD dedicado, lista cerrada de recursos, ≤2 h, teardown/rollback, condiciones previas) #owner/me #type/dev
> - [ ] G7: BLOCKED a RT-1 (CONFIRMED del owner) + condiciones previas (canal aranea-ssh restaurado o checklist host-level, .cfx subido, 8 estrategias copiadas); será certificación PARCIAL de un host #blocked
> - [ ] G8 cierre: merge owner + release según gates (push hecho 2026-09-21) #owner/me #type/dev
> - [ ] Campaña B: congelar parámetros OOS/MT5 y ejecutar tras G7 #owner/me #type/dev

## 📆 Bitácora

- **2026-09-22 (mandato cierre II)** — Reviews independientes y correcciones: ronda 1 por dos agentes verificadores adversariales de contexto fresco sobre `3d04d68` (run `dwfrun-aa80d4e6`): **MR-1 APPROVED** (10/10 claims PASS; F1/F2 MINOR, F3–F7 NOTE) y **MR-2 CHANGES_REQUIRED** (MAJOR H-1: `recovery.go` validaba el MetricSet de la recovery import con constantes Builder ⇒ retry post-crash de etapa import COMPLETED fallaba con CONTRACT_CONFLICT; sin test; además H-2 sin test del branch import del ranking). Fixes en rama `3d04d68 → 6ad247a → bed8d31` (push FF): recovery por contrato de productor (fail-closed no registrados; ruta Builder byte-idéntica), tests de recovery/evidencia import, binding del databank de entrada del plugin (`input` import / `output` builder — defecto de integración que habría dejado el plugin leyendo un databank vacío en G7), mensajes de error por contrato; fixture del benchmark restaurado tras efecto lateral. Regresión post-fix: fail-set idéntico al baseline (21 nombres) y dominio/binding/steps/runtime en 0. Re-review ronda 2 del delta en curso (`dwfrun-3d728aaa`). Preflight G7-B control-plane verificado RO (Temporal sqx-dev OK, flota sqx-prop/sqx-main-queue, MinIO con 11 .sqx auténticos y convención 00_configs; canales aranea-ssh 503 y Mongo RO caídos ⇒ preflight host-level pendiente); nada arrancado, flota intocada.
- **2026-09-21 (mandato cierre)** — Review y cierre físico preparado: branch actualizada `5e495ae → 3d04d68` (1 commit, push FF; master intacto `745bc8b`). Review técnica MR-1/MR-2 limpia con evidence pack; correcciones documentales: autoridad proyecto/plugin (`EchoForgeImportExporter` proyecto SQX local + plugin `EchoForgeOverviewExporter`; SPEC §4.1/4.2/§12 corregidas, runbook ya consistente), receta runbook con `custom_analysis_plugin` (fallo cerrado sin él), gap multi-host declarado con tests de binding single-FlowRun (SPEC §4.3 + D7 precisada + runbook §5: G7 de un host = parcial). Anexo runtime candidato DEV opción B (`RUNBOOK-DEV-AISLADO-OPCION-B.md`, PREPARED/PENDING_RT1; verificado RO: namespace Temporal `sqx-dev` existe, ETCD `/symphony/development/` 40 keys, cola compartida `sqx-main-queue` excluida para el candidato). Nada arrancado ni desplegado; flota 0.2.105 intocada.
- **2026-09-21** — Consolidación git previa a G7 (mandato owner): branch publicada en origin `5e495ae` (5 commits íntegros, push tras scan de secretos limpio); `master` promovido por FF puro a `745bc8b` (merge-base de esta rama == nuevo master, historia sin rebase); verificado vía GitHub API (`ahead=5 behind=0 merge_base=745bc8b`; sin commits de Import en master). G7 sigue bloqueado a runtime aislado del owner; MR-1/MR-2 siguen en review.
- **2026-09-21** — Sesión ZCode/GLM: G0–G6 completos en worktree `/home/kor/go/src/github.com/xKoRx/symphony-import-v1` (4 commits). Flota con worker 0.2.105 corriendo en Zeus ⇒ G7 requiere owner gate. Runbook y receta de config listos.

## 🧭 Decisiones

- D1 desacople por REGISTRO de productores (builder|import), no por relajar el `if` de stage. D2 `IMPORTED` activado como rol origin (reservado por CROSS-FLOWRUN-REUSE). D3 extractor único: plugin Java EchoForgeOverviewExporter modo databank. D4 métricas import = `IMPORTED_HISTORICAL_RESULT` (nunca evaluación Forge). D5 filenames/carriers `builder_*` congelados en V1. D6 selection = task control-plane con snapshot durable insert-once. Detalle: `specs/FEAT-SQX-IMPORT-TASK-V1/TOP-DECISIONS.md`.

## 🔗 Docs / Links

- Parent: [[Echo Forge]] · Entorno: [[Echo + Echo Forge — Environment Contract]]
- Repo specs: `specs/FEAT-SQX-IMPORT-TASK-V1/` (SPEC, TOP-DECISIONS, RUNBOOK G7), `specs/FEAT-SQX-IMPORT-CAMPAIGN-B/SPEC.md`
- Amendments manager review: `FEAT-SQX-DURABLE-CLASSIFICATION-EVIDENCE/AMENDMENT-IMPORT-PRODUCER.md`, `FEAT-SQX-DURABLE-EARLY-PER-TYPE-RANKING/AMENDMENT-IMPORT-PRODUCER.md`
