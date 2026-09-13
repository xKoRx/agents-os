---
type: application
schema_version: 1
status: active
area: "[[Echo]]"
lang: Go, Java
github: "https://github.com/xKoRx/symphony"
path: "xKoRx/symphony (módulo sqx/)"
last_verified: "2026-09-13"
confidence: verified
aliases:
  - Echo Forge
  - echo-forge
  - sqx
tags:
  - area/echo
  - kind/application
created: 2026-06-27
updated: 2026-09-13
---

# echo-forge

%% Naming: echo-forge es el link canónico de la aplicación; aliases puede incluir repo, nombre viejo o sistema externo; tags/slugs no reemplazan links. %%

> [!info]+ echo-forge
> **Rol:** fábrica cuantitativa adaptativa de estrategias (pipeline Temporal sobre el motor SQX) · **Área:** [[Echo]] · **Lang:** Go, Java (plugin SQX)
> **Repo:** `xKoRx/symphony` (módulo `sqx/`) · **Baseline citado:** `xKoRx/symphony@9fad768c` (branch `feature/f04-magic-version-handoff`; master `0b9742b0`)
> **Diferencia con SQX (StrategyQuant X):** echo-forge es el programa propio (Go + Java) que orquesta SQX; SQX es la tool comercial que genera las estrategias. echo-forge NO reemplaza a SQX. Ver [[strategyquant-x]].

## 🎯 Responsabilidad (estable)

- Ejecutar la campaña multi-wave de generación/validación de estrategias: `ForgeCampaignWorkflow` (waves con WorkflowID determinista y stop policy) → `GenericSQXWorkflow` secuencial por tasks declarativas (Builder/Retester/Optimizer/FinalReretester por predicado Type/Stage, no por folder) con gates `verify_*` read-only.
- Evaluar y seleccionar: WFM durable (fan-out export+seal, evaluador de vecindario 6x9/3x3 con scoring determinista), ranking global congelado `score_descending.v1` y per-type `weighted_combination_minmax.v1`, selección robusta `stage4.v1`, Apply Selected Run validado contra Decision `OPTIMIZER_SELECTION` ENFORCE, FinalistPromotion V2 (membership estructural, zero-supply permitido).
- Ser el OWNER de la identidad que comparte con Echo: crea CanonicalStrategyID/StrategyRef, sella versiones (receta S0) y asigna Magic V1 (formato `YYMMIIIDSSS`, 1:1 StrategyRef↔magic sin reciclaje, catálogo inmutable de instrumentos, namespace `forge-live`); Echo nunca asigna magic.
- Orquestar MT5 real: compilación/backtest como child workflows dedicados, runner con `tester.ini`, reconciliación estructural SQX↔MT5 y score shadow con tolerancia.

## 🚫 Frontera con Echo (estado real — reemplaza el claim de entrega previo)

- > [!warning] El pipeline NO entrega nada a Echo hoy. La versión anterior de esta página afirmaba que echo-forge "entrega las estrategias finalistas a Echo Core mediante su API": eso es FALSO al baseline `9fad768c`. No existe transporte Forge→Echo (cero cliente HTTP/Kafka; `grep forge/promotions` en `sqx/` = 0) y ningún workflow/activity de producción invoca `SealStrategyVersion`, `BuildHandoffManifest` ni `DeliverHandoff` (sólo tests).
- El pipeline cableado TERMINA en FinalistPromotion V2 + Apply Selected Run (con magic asignado y estampado localmente en la config del EA cuando el flow hace opt-in `UseDurableMagicAllocation`).
- La capacidad de handoff existe a nivel librería, sólo en el branch F-04 (no en master): `BuildHandoffManifest` (producer frozen `echo-forge-handoff` 1.0.0, valida contra el contrato congelado y produce body canónico + digest + idempotency key), `DeliverHandoff` (máquina de estados write-once con stores PG `sqx.handoff_manifests`/`sqx.handoff_deliveries`, gate de byte-equality, park `UNKNOWN_RECEIPT` sin re-POST) y `FakeConsumerIngress` (única `HandoffIngress`, in-process, sólo tests CONTRACT).
- Detalle completo, matriz de gaps (G1–G6) y qué falta para cerrar: [[echo-forge-integration-boundary]]. Contrato productor: [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]].

## 🚨 Invariante de ejecución SQX

> [!danger]+ Contrato obligatorio
> **1 VM = 1 worker = 1 task en ejecución.** Cada worker procesa una sola activity/task a la vez; la concurrencia solo existe entre VMs/workers distintos.

- No diseñar locks, mutexes, semáforos, slots ni workspaces/scopes para una supuesta concurrencia dentro del worker. El fan-out Temporal usa la task queue normal.
- Cualquier cambio a esta regla exige una decisión arquitectónica separada y aprobación explícita del owner. Fuente canónica y consecuencias: [[2026-08-14-echo-forge-one-vm-one-worker-one-task]].

## 🔌 Contratos e interacciones (semi-estable)

- **Temporal:** motor confirmado de workflows de Forge (`sqx/go.mod` SDK v1.35.0; 5 workflows + ~40 activities en `sqx-worker`); el módulo root de symphony (Zeebe/Camunda/goka, feeds) es el sistema legacy de feeds, NO Forge.
- **SQX:** ejecución local vía etcd + CommandExecutor con markers de fin; plugin Java de exporters dentro de SQX (`EchoForge*Exporter.java`) que escriben outputs que el watcher sube a MinIO.
- **Persistencia:** PostgreSQL autoridad durable (migraciones 001–016 con runner propio), MongoDB evidencia/metadata, MinIO bucket `sqx-strategies` artefactos, etcd coordinación de campaña.
- **Echo:** única dependencia cruzada de código = pin `github.com/xKoRx/echo/v3/sdk/contracts v0.0.0-20260910031519-91671f6f46ff` en `sqx/go.mod` (superficie idéntica al baseline Echo `f7ddea18`); ver [[echo-forge-integration-boundary]].

## 🧩 Implementación (volátil · last_verified: 2026-09-13)

- **Stack:** Go 1.24 (módulo `sqx/`), Temporal, PostgreSQL/MongoDB/MinIO/etcd, Java (plugin CustomAnalysis de SQX), workers dedicados (`sqx-worker`, `sqx-mt5-worker` Windows singleton, `sqx-watcher` fsnotify→MinIO→dispatch).
- **F-04 [BRANCH-ONLY]:** Magic V1 allocator + StrategyVersion seal + handoff + migraciones 015/016, presentes en el runner del branch; `SealStrategyVersion` implementado SIN caller de producción; no hay fixture auténtica committed del producer (testdata = copia byte-equal del corpus S0 Echo).
- **Legado cerrado dentro de Forge:** task `wfm_exporter` (error explícito), `legacy_apply_selected_run_disabled`, `overview_exporter` skip.

## 🚨 Estado y gaps conocidos (volátil · last_verified: 2026-09-13)

- G1: sin transporte real hacia Echo (ver sección Frontera). G2: seal sin caller → el manifest no puede construirse con datos sellados reales en el flujo productivo. G4: reconciliación `UNKNOWN_RECEIPT` sin consumidor del read idempotente que Echo ya provee. G5: `FORGE_GOLDEN_FIXTURE_PENDING` (T21/AC-37). G6: el spec conceptual `FEAT-SQX-ECHO-INGESTION` (repo) diverge del contrato frozen implementado y está superseded de facto — citarlo sólo como historia.
- Ubicación futura del cableado seal→manifest→deliver: desconocida (no hay TODO ni wiring en código); la wiki no decide producto.

## 📌 Provenance

- **Repo:** `xKoRx/symphony`, módulo `sqx/` (fuente primaria: `sqx/README.md` operación, `docs/prd/SQX_Adaptive_E2E_Pipeline_PRD.md` PRD canónico, `specs/` SDD FEAT-SQX-*, `specs/SPECS.md`).
- **Sources:** [[Echo Forge — Fuentes de implementación 2026-09-12 (9fad768c)]] · [[Echo Forge — Fuentes de arquitectura y producto 2026-09-06]] (provenance histórica Symphony a10c26c).
- `last_verified: 2026-09-13` · `confidence: verified` (contraste directo contra `9fad768c`, artifact 03).

## 🔗 Links

- **[[strategyquant-x]]** — la tool SQX que echo-forge orquesta (tool vs programa).
- **[[echo-forge-integration-boundary]]** — frontera Forge→Echo (contrato, estado, gaps). · [[echo-core]] — plataforma receptora.
- **[[2026-08-14-echo-forge-one-vm-one-worker-one-task]]** — invariante vinculante de serialización por worker.
- [[../../aranea/02-servicios/ml-ia|sqx-ulab VMs]] — infraestructura SQX en Aranea.
- [[Echo Forge]] — proyecto en `10-projects/` (vista de programa). · Índice: [[30-resources/applications/echo/00-index|Echo — Índice]].
- Repo paths citables: `xKoRx/symphony: specs/SPECS.md` (estado por feature) · `xKoRx/symphony: docs/prd/SQX_Adaptive_E2E_Pipeline_PRD.md` · `xKoRx/symphony: docs/prd/SQX_Adaptive_E2E_Pipeline_RFC.md` · `xKoRx/symphony: sqx/README.md`.
