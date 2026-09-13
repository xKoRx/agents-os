---
agent: llm-wiki-documentarian
role: Wiki Consolidation Design
task_id: KBC-F
status: COMPLETE
baseline: echo f7ddea18 · symphony 9fad768c · vault 12d250a
inputs: artifacts 01-05, resource-wiki contract
scope: propuesta completa de documentación canonical (draft-only)
started_at: 2026-09-13T01:35:00-03:00
updated_at: 2026-09-13T02:20:00-03:00
---

# KBC-F — Wiki Draft Plan

## Assignment

Convertir los evidence packs verificados de las fases B/C/D y el manifest de la fase E en la propuesta COMPLETA de documentación canonical para el subdominio `30-resources/applications/echo/`, siguiendo la topología aprobada (artifact 01), el contrato de `agents-os-resource-wiki` + `30-resources/00-RESOURCE-WIKI.md`, y respetando el Handoff restrictivo de la fase D (lista de lo que la wiki NO debe afirmar). Draft-only: este archivo es la única escritura; nada se publica en `30-resources/` ni en repos. La promoción canonical es fase de publicación explícita (H/P) tras Fase G PASS.

## Baseline

- Vault Agents-OS: HEAD reconfirmado al escribir este artifact = `12d250a` (master). Cadena de drift de campaña: planner `9a5299f1` → A observó `09746b3` → D `9d4b311` → E `a87aa62` → F `12d250a`. Es avance post-baseline del vault, no contradicción; la fase H reconcilia contra HEAD vigente al publicar.
- `xKoRx/echo` @ `f7ddea18` (branch `feature/e02-control-safety-journal-recovery`, clean; master `a99f9a63`). `xKoRx/symphony` @ `9fad768c` (branch `feature/f04-magic-version-handoff`; master `0b9742b0`; 1 dirty file `phase4_performance.json`, no tocar). Ambos coinciden con el baseline de campaña; no verifiqué git en esta fase (fases B/C/D/E ya lo hicieron contra los mismos SHAs declarados); la verificación adversarial es de Fase G.
- Reglas cargadas: `80-agents/skills/agents-os-resource-wiki/SKILL.md`, `30-resources/00-RESOURCE-WIKI.md` (dominios, corte estable/volátil, provenance `type: source`, lifecycle supersedes, escalado de índices), `90-system/convenciones.md` (naming canónico = nombre de archivo = destino de links), template `70-templates/application.md` (corte estable/volátil nativo), notas vigentes del dominio (`applications/00-index.md`, `log.md`, `echo-core.md`, `echo-forge.md`, F-04, Fuentes 2026-09-06).
- Creación canónica: las páginas nuevas se materializan con `80-agents/skills/_shared/scripts/materialize_schema_note.py` según `note-types.md`; el frontmatter propuesto aquí replica la salida del template correspondiente y el publisher NO debe copiarlo a mano.

## Document Set

Orden de publicación = orden de la lista (pasos 1–3 del manifest E en un solo cambio; contenido en pasos siguientes; supersedes sólo tras G PASS).

| # | Target path (rel. VAULT_ROOT) | Acción | Propósito |
|---|---|---|---|
| 1 | `30-resources/applications/echo/00-index.md` | CREATE | Sub-índice curado del subdominio Echo (una fila vigente por página + fila histórica) |
| 2 | `30-resources/applications/echo/echo-core.md` | UPDATE-MOVE | Página canónica de Echo (repo `xKoRx/echo`), reescritura con evidencia B; misma identidad, no copia |
| 3 | `30-resources/applications/echo/echo-forge.md` | UPDATE-MOVE | Página canónica de Echo Forge (módulo `sqx/` de `xKoRx/symphony`), reescritura con evidencia C; corrige la contradicción de entrega a Echo |
| 4 | `30-resources/applications/echo/echo-forge-integration-boundary.md` | CREATE | Página compartida de la frontera Forge→Echo: contrato vigente, estado implementado, gaps; enlaza contratos, no los repite |
| 5 | `30-resources/applications/echo/echo-core-changelog.md` | MOVE | Bitácora de cambios de Echo Core, intacta |
| 6–9 | `30-resources/applications/echo/Echo Forge — F-01…F-04 … Contract.md` (4) | MOVE | Contratos frozen, source-of-record; no se re-derivan ni corrigen |
| 10 | `30-resources/applications/echo/Echo SDK — Canonical Forge Integration and Analytics Contract V1.md` | MOVE | Contrato compartido SDK vigente |
| 11 | `30-resources/applications/echo/Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1.md` | MOVE | Contrato de ingestión/Live Authority vigente (autoridad del SPEC E-04) |
| 12–13 | `30-resources/applications/echo/Echo — Fuentes … 2026-09-06.md` y `Echo Forge — Fuentes … 2026-09-06.md` | MOVE | Ledgers de provenance históricos (type: source), intactos |
| 14 | `30-resources/applications/echo/Echo — Fuentes de implementación 2026-09-12 (f7ddea18).md` | CREATE | Nota source nueva por baseline Echo (fase B) |
| 15 | `30-resources/applications/echo/Echo Forge — Fuentes de implementación 2026-09-12 (9fad768c).md` | CREATE | Nota source nueva por baseline Symphony (fase C) |
| 16–20 | 3 auditorías 2026-09-06 + 2 Fable reviews | MOVE, luego SUPERSEDE | Retención histórica; pierden autoridad al verificarse páginas 2/3/4 (gate: Fase G PASS) |

Impactos declarados (sin mover archivos): `applications/00-index.md` (UPDATE mismo cambio que los MOVE), `applications/log.md` (APPEND por operación), `30-resources/00-RESOURCE-WIKI.md` (declarar subdominio activo `applications/echo/`). Sin cambio: `stager-app.md`, `runbooks/`, `dashboards/echo-forge/`, `methodologies/sdd/sources/`, `LLM Wiki.md`, filas Meli.

Decisiones de contenido cargantes (resolución de contradicciones de la fase E):

1. **Claim falso "Forge entrega finalistas a Echo Core mediante su API"** (echo-forge.md + fila del índice raíz): se reemplaza por el estado implementado real — el pipeline Forge termina en FinalistPromotion V2 + Apply Selected Run; la capacidad de handoff existe a nivel librería pero NO está cableada y no hay transporte (G1). El draft de echo-forge.md lista explícitamente qué texto se reemplaza.
2. **Solapamiento contratos V1 (#10/#11) vs página frontera (#4):** contratos = source-of-record frozen (no se editan); la frontera documenta ESTADO IMPLEMENTADO y GAPS y enlaza los contratos sin citar sus cláusulas operativas más que por referencia. Regla: si un hecho vive en un contrato frozen, la frontera linkea; si vive en código/tests, la frontera lo sintetiza con baseline.
3. **Divergencia branch/master asimétrica:** Echo ya tiene el receptor E-01/E-04 en master (`a99f9a63`) pero E-02 (auth de actores) es branch-only; Symphony tiene F-04 completo branch-only (`9fad768c`). Las páginas citan branch + SHA y marcan qué es branch-only; jamás simetrizan los dos repos.
4. **Naming de la frontera:** archivo `echo-forge-integration-boundary.md` (kebab, consistente con las páginas de app del subdominio), aliases `Echo — Forge Integration Boundary V1` / `Echo Forge Integration Boundary` para que los links históricos y las referencias de los artifacts D/E resuelvan.
5. **Auditorías históricas:** se mueven con identidad preservada y quedan en fila "histórico" del sub-índice; el marcado `status: superseded` (metadata propuesta en sección Supersedes) se ejecuta SÓLO tras Fase G PASS, con verificación previa de que los claims únicos (32 deudas, hitos, matrices C-1…C-7 / FR-1…FR-5) quedan cubiertos o referenciados.

## Page Drafts

### P2 — `30-resources/applications/echo/echo-core.md` (UPDATE-MOVE, reescritura)

- **Purpose:** página canónica de Echo (plataforma v3 del repo `xKoRx/echo`): qué es, qué contratos expone, qué está implementado hoy y qué no.
- **Source evidence:** artifact 02 (§1–§10, Implemented vs Spec-Only, Handoff); artifact 04 (lado Echo de la frontera); artifact 05 (fila echo-core.md: thin, path de máquina obsoleto).
- **Freshness:** secciones "Implementación" y "Estado y gaps conocidos" son volátiles (`last_verified: 2026-09-12`, contra `f7ddea18`); deben revalidarse contra HEAD antes de publicar (E-02 puede haberse mergeado; SPECS.md es el índice de estado por feature).
- **Supersedes:** contenido de la versión 2026-07-03 (49 líneas) — la identidad de la página se preserva (MOVE); el `path` de máquina `/Users/rodrigojara/...` se elimina; la descripción textual de una línea se migra al índice actualizada.

Propuesta de contenido (materializar desde `70-templates/application.md`; frontmatter = salida del template con estos valores):

```markdown
---
type: application
schema_version: 1
status: active
area: "[[Echo]]"
lang: Go
github: "https://github.com/xKoRx/echo"
path: "xKoRx/echo (árbol activo v3/)"
last_verified: "2026-09-12"
confidence: verified
aliases:
  - Echo Core
  - echo-core
  - xKoRx/echo
tags:
  - application
  - kind/application
created: 2026-07-03
updated: 2026-09-13
---

# Echo Core

%% Naming: echo-core es el link canónico de la aplicación; aliases puede incluir repo, nombre viejo o sistema externo; tags/slugs no reemplazan links. %%

> [!info]+ Echo Core
> **Rol:** plataforma de ejecución y registro de trading (runtime v3) · **Área:** [[Echo]] · **Lang:** Go (+ EAs MQL, front Vue)
> **Repo:** `xKoRx/echo` · **Baseline citado:** `xKoRx/echo@f7ddea18` (branch `feature/e02-control-safety-journal-recovery`; master `a99f9a63`)

## 🎯 Responsabilidad (estable)

- Ejecutar el ciclo de trading de extremo a extremo: EAs MT4/MT5 → Echo Bridge (Windows, named pipes) → Kafka → Core (Flink StateFun: StrategyConfig → ExecutionPlanner → MMEngine → TradeJournal) → Kafka `echo.core-commands.v1` → Bridge → EA de ejecución. El Gateway queda FUERA del hot path de trading (webhooks, control, automation, boundary Forge).
- Mantener el diario de operaciones durable (Trade Journal en PostgreSQL, esquema `echo`) con cuarentena determinística de payloads en conflicto y CLI de recuperación sin Kafka (`v3/tools/journalctl`).
- Ser el RECEPTOR de la frontera Forge→Echo: expone `POST/GET /api/v1/forge/promotions` para ingestión de `HandoffManifestV1`; la ingesta produce sólo receipt `INGESTED` y nunca activación (ver [[echo-forge-integration-boundary]]).
- Poseer la identidad canónica compartida: contratos frozen en `v3/sdk/contracts` (identidad ≤1024 bytes, HandoffManifestV1, receipt único INGESTED); Echo nunca asigna ni recicla magic (ownership Forge).

## 🔌 Contratos e interacciones (semi-estable)

- **Expone:** Gateway HTTP (puerto 8082): `/health`, auth hook Hasura, webhooks de config (account-config, symbol-mapping, automation-profiles, execution-policy), `POST /api/v1/close-positions`, `POST /api/v1/admin/republish`, boundary Forge (`POST /api/v1/forge/promotions` + 2 GET de reconciliación).
- **Consume/produce:** 18 topics Kafka canónicos declarados en `xKoRx/echo: v3/sdk/domain/snapshots.go` + topic por cuenta `echo.commands.<account>.v1`; productor durable `PublishSync` para facts de trading.
- **Persistencia:** PostgreSQL único esquema de app `echo` (migraciones 001..062: núcleo, identidad BWC 061, cuarentena 062); etcd para config por servicio+env; Hasura como único GraphQL del front.
- **Forge:** receptor del boundary — detalles, matriz de errores y gaps en [[echo-forge-integration-boundary]]; contrato vigente en [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]] y contratos F-0x.
- **Observabilidad:** OpenTelemetry OTLP (logs/metrics/traces) con semconv por servicio.

## 🧩 Implementación (volátil · last_verified: 2026-09-12)

- **Stack:** Go v3 (Core/Gateway/Bridge/SDK/lab-worker/toolkit), Flink StateFun vía HTTP (la orquestación NO es Temporal: cero dependencias `go.temporal`), PostgreSQL, Kafka (Sarama), etcd, Hasura, front Vue 3 + Vite, EAs MQL MT4/MT5 + DLLs.
- **Auth por 4 actores (E-02, BRANCH-ONLY en `f7ddea18`, no en master `a99f9a63`):** `front_read`, `config_operator`, `control_operator`, `service_hasura_webhook`; tokens por env/etcd, fail-closed, 401 vs 403, hook Hasura emite sólo roles `readonly`/`config_operator`; front con session tokens por actor, sin admin secret en bundle.
- **Resilience:** productor síncrono durable Bridge→Kafka; cuarentena de journal (`echo.journal_quarantine`, razones POISON_PAYLOAD/CLOSE_WITHOUT_OPEN/conflictos) con ACK a Flink; `journalctl` (`quarantine list/show/resolve/discard`, `replay-facts` PG→PG garantizado sin Kafka por `deps_guard_test.go`); replay idempotente de ingestión Forge (200 exact-replay / 409 conflictos).
- **Legacy conviviente:** binario `v3/core/cmd/echo-functions` DEPRECATED; topics `echo.account-snapshots.v1`/`echo.instrument-snapshots.v1` DEPRECATED; módulos v1/v2 aún en `go.work` (el activo es v3).

## 🚨 Estado y gaps conocidos (volátil · last_verified: 2026-09-12)

- E-02 está en el branch como código + tests CONTRACT PASS pero PHYSICAL_PARTIAL: compose Flink/PG/Kafka/Hasura real no ejecutado (T14/T15); el branch no está mergeado a master.
- Receptor Forge E-01/E-04: integrado en master, E-04 INTEGRATED pero FINAL CLOSED = NO (T21/AC-37 CROSS_LANE GOLDEN pending, `FORGE_GOLDEN_FIXTURE_PENDING`).
- Sin backend de artefactos en V1: producción usa `unavailableArtifactSource` (503 fail-closed) → ningún primer accept end-to-end posible hoy (gap G3 del boundary).
- Post-INGESTED no hay consumidores: cero provisioning/activación/capital/Kafka (impuesto por tests de non-effects y REVOKE en DB); E-06+ es frontera futura.
- La wiki no decide producto: estos gaps se documentan, no se resuelven aquí.

## 📌 Provenance

- **Repo:** `xKoRx/echo` (path: `v3/`; README, `v3/docs/ARCHITECTURE|DATA_MODEL|FLOWS|OBSERVABILITY|TROUBLESHOOTING.md`, `docs/adr/`, `specs/SPECS.md` como índice de estado por feature).
- **Sources:** [[Echo — Fuentes de implementación 2026-09-12 (f7ddea18)]] · [[Echo — Fuentes de arquitectura y producto 2026-09-06]] (provenance histórica master 04c16bd).
- `last_verified: 2026-09-12` · `confidence: verified` (contraste directo contra `f7ddea18`, artifact 02).

## 🔗 Links

- [[echo-core-changelog|Bitácora de Cambios (Changelog)]] · [[echo-forge]] (fábrica cuantitativa upstream) · [[echo-forge-integration-boundary]] (frontera) · [[Echo]] (área madre)
- Índice del subdominio: [[30-resources/applications/echo/00-index|Echo — Índice]]
```

### P3 — `30-resources/applications/echo/echo-forge.md` (UPDATE-MOVE, reescritura)

- **Purpose:** página canónica de Echo Forge (módulo `sqx/` de `xKoRx/symphony`): pipeline implementado, invariante de ejecución SQX, y el estado REAL de la relación con Echo (corrige la contradicción detectada en fase E).
- **Source evidence:** artifact 03 (§1–§15, Implemented vs Spec-Only, Handoff to Echo); artifact 04 (Contractual Truth CT-3, Implemented lado Forge, G1/G2/G4/G5/G6); artifact 05 (fila echo-forge.md: claim de entrega contradicho, 10 inbound links, claims únicos a migrar: distinción echo-forge vs SQX tool, invariante 1 VM, links a PRD/RFC).
- **Freshness:** secciones "Implementación" y "Estado y gaps" volátiles (`last_verified: 2026-09-13`, contra `9fad768c`); F-04 es branch-only — cualquier merge a master cambia el estado y exige revalidación.
- **Reemplazos respecto de la versión vigente (2026-08-14):** (a) se ELIMINA "entrega únicamente las estrategias aprobadas (finalistas) a Echo Core mediante su API" y "Echo Core: destino downstream de estrategias finalistas aprobadas" — contradichos por G1/G3 (artifacts 04 §Gaps, §End-to-End); (b) los links `file:///Users/rjara/...` a SPECS/PRD/RFC se reemplazan por paths repo-relativos; (c) se conserva y migra la nota de distinción echo-forge vs [[strategyquant-x]] y la sección de invariante 1 VM = 1 worker = 1 task (sigue vigente, binding, con su fuente canónica).

Propuesta de contenido:

````markdown
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

- **Temporal:** motor confirmado de workflows de Forge (`sqx/go.mod` SDK v1.44.1; 5 workflows + ~40 activities en `sqx-worker`); el módulo root de symphony (Zeebe/Camunda/goka, feeds) es el sistema legacy de feeds, NO Forge.
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
````

### P4 — `30-resources/applications/echo/echo-forge-integration-boundary.md` (CREATE)

- **Purpose:** página canónica compartida de la frontera Forge→Echo: qué contrato rige, qué está implementado en cada lado (con baseline), qué gaps existen, y qué esta wiki NO afirma. Enlaza los contratos #6–11, no los repite.
- **Source evidence:** artifact 04 completo (Boundary Matrix, Gaps G1–G7, End-to-End Flow, Ownership, Handoff restrictivo); corroborado por artifacts 02 (§6) y 03 (§Handoff to Echo); contratos F-04/V1 en el vault.
- **Freshness:** TODO el estado implementado es volátil por definición (`last_verified: 2026-09-13`); el contrato frozen es estable salvo nueva versión de `IngestionContractVersion`.
- **Materialización:** desde template resource (como F-04, `type: resource`), vía script.

Propuesta de contenido:

````markdown
---
type: resource
schema_version: 1
status: active
area: "[[Echo]]"
last_verified: "2026-09-13"
confidence: verified
sources:
  - "[[Echo — Fuentes de implementación 2026-09-12 (f7ddea18)]]"
  - "[[Echo Forge — Fuentes de implementación 2026-09-12 (9fad768c)]]"
  - "[[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]]"
  - "[[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]]"
  - "[[Echo SDK — Canonical Forge Integration and Analytics Contract V1]]"
aliases:
  - Echo — Forge Integration Boundary V1
  - Echo Forge Integration Boundary
  - frontera Forge Echo
entities:
  - "[[Echo Forge]]"
  - "[[xKoRx/echo]]"
  - "[[xKoRx/symphony]]"
tags:
  - kind/resource
  - area/echo
created: 2026-09-13
updated: 2026-09-13
---

# Echo Forge → Echo Integration Boundary

Página compartida de la frontera Forge→Echo. Los contratos frozen son el source-of-record ([[Echo SDK — Canonical Forge Integration and Analytics Contract V1]], [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]], [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]] y F-01…F-03); esta página documenta el ESTADO IMPLEMENTADO y los GAPS contra esos contratos, con baseline por repo. No crea un tercer producto ni un track paralelo.

**Baselines:** `xKoRx/echo@f7ddea18` (branch `feature/e02-control-safety-journal-recovery`; master `a99f9a63`) · `xKoRx/symphony@9fad768c` (branch `feature/f04-magic-version-handoff`; master `0b9742b0`; F-04 branch-only). Pin compartido: `sqx/go.mod` → `xKoRx/echo/v3/sdk/contracts v0.0.0-20260910031519-91671f6f46ff`, superficie idéntica al baseline Echo (diff = 1 línea de test).

## Contrato vigente (estable)

- Autoridad S0 compartida: paquete `v3/sdk/contracts` — `IngestionContractVersion = "forge-echo-ingestion.v1"`, `IdentityModelVersion = 2`, `HandoffManifestV1` (bloques producer/strategy/version/promotion; cross-checks G08–G12), receipt con único estado `INGESTED` ("never an activation"), recetas frozen `IdempotencyKey`/`PayloadDigest`/`StrategyVersionRef`.
- Receptor (SPEC E-04 v1.0.2, Spec-Active): endpoints frozen `POST /api/v1/forge/promotions` + GET by-key/by-receipt, auth `forge:ingest` con namespace `forge-live` desde credencial (nunca del body), orden §9 (replay lookup antes de artifact I/O, transacción única), matriz de errores (201/200/400/403/404/409×3/413/422×7/503), non-effects §11, separaciones `INGESTED ≠ PROVISIONED ≠ ACTIVE` y `INGESTION ≠ PROVISIONING ≠ OBSERVATION ≠ ELIGIBILITY ≠ CAPITAL ≠ ACTIVATION`. Detalle normativo: [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]].
- Productor (F-04 frozen en branch): producer `echo-forge-handoff` 1.0.0, membership exclusivamente estructural desde Decision `FINALIST_PROMOTION` V2 (rank/score nunca leídos, F-02), cero finalistas ⇒ cero manifests (G22), puerto `HandoffIngress` y máquina de estados `DeliverHandoff` (write-once, byte-equality gate, `UNKNOWN_RECEIPT` sin re-POST). Detalle: [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]].

## Estado implementado (volátil · last_verified: 2026-09-13)

- **Forge (emisor):** capacidad completa a nivel librería, SÓLO en branch F-04: `BuildHandoffManifest`, `DeliverHandoff`, stores PG 015 (`sqx.handoff_manifests` write-once G24, `sqx.handoff_deliveries` 6 estados), `SealStrategyVersion` (sin caller), `FakeConsumerIngress` (única ingress, in-process, tests CONTRACT). Pipeline cableado termina en FinalistPromotion V2 + Apply; magic V1 cableado en EXACTAMENTE un punto (Apply, opt-in `UseDurableMagicAllocation`, namespace `forge-live`, estampado en config del EA — no viaja en ningún handoff emitido).
- **Echo (receptor):** operable en reposo y presente también en master: rutas montadas al spec, Bearer constant-time, misconfig 503 fail-closed, `IngestionService.Ingest` con orden §9 completo y transacción única, copy de artefactos con allowlist + `FilesystemStore`, DB write-once (`echo.promotion_records` CHECK INGESTED, UNIQUEs G24, REVOKE), 30+ tests CONTRACT + non-effects.
- **Producción HOY:** ningún byte de handoff cruza la frontera. La única integración real es el pin del módulo `contracts` (tipos y recetas compartidas).

## Cadena end-to-end tal como está hoy

Builder→…→FinalistPromotion V2→Apply (Forge, operativo) → ✂ ROTURA 1: seal→manifest sin cablear → ✂ ROTURA 2: sin transporte de red (sólo FakeConsumer in-process) → receptor Echo completo y esperando (con ROTURA 3 en el primer accept: `unavailableArtifactSource` 503, G3) → tras INGESTED: NADA (cero consumidores downstream, E-06+ futuro).

## Gaps conocidos (la wiki los documenta, no los resuelve)

- **G1 (central):** no existe transporte real Forge→Echo; cierre requiere cablear seal→manifest→deliver en el pipeline Forge (ubicación hoy desconocida), cliente E-04 real que implemente `HandoffIngress`, y merge de F-04 a symphony master.
- **G2:** `SealStrategyVersion` sin caller — el manifest no puede construirse con datos sellados reales en producción.
- **G3 (bloqueante E2E):** Echo V1 sin backend de artefactos (`unavailableArtifactSource` 503 fail-closed); ningún primer accept posible aunque G1 se cierre. Forge tiene los artefactos en MinIO `sqx-strategies`; Echo no integra MinIO en V1.
- **G4:** reconciliación `UNKNOWN_RECEIPT` sin consumidor en Forge (el GET idempotente de Echo ya existe).
- **G5 (gate):** `FORGE_GOLDEN_FIXTURE_PENDING` — corpus S0 synthetic, producer del corpus `forge` ≠ `echo-forge-handoff`; T21/AC-37 CROSS_LANE GOLDEN no puede declararse PASS; E-04 INTEGRATED pero FINAL CLOSED = NO.
- **G6 (documental, repo-side):** spec conceptual `FEAT-SQX-ECHO-INGESTION` diverge del frozen (superseded de facto, citar sólo como historia); `FEAT-SQX-ECHO-DEPLOYMENT-LINK` (LinkDemoDeployment) sin receptor ni contrato.
- **G7 (unknown):** observability cross-boundary sin traza/métrica compartida definida. Nota de diseño (no gap): el header `Idempotency-Key` deberá derivarlo el cliente HTTP real vía `contracts.IdempotencyKey`.

## Lo que esta wiki NO afirma

- Que Forge publique/envíe estrategias a Echo (falso hoy). Que exista un flujo automático post-FinalistPromotion (no cableado). Que Echo pueda ingerir end-to-end (fallaría en artifact fetch, G3). Que CROSS_LANE/GOLDEN o el join Forge esté certificado (T21/AC-37 PENDING). Que el spec conceptual Forge describa el contrato real (superseded de facto). Que magic sea asignado o validado por Echo (Forge-only). Simetría de integración entre repos (receptor en master Echo; productor branch-only en symphony). Que INGESTED implique activación, provisioning, capital o eligibility en cualquier grado.

## 🔗 Links

- Páginas: [[echo-forge]] · [[echo-core]] · [[echo-core-changelog]] · Índice: [[30-resources/applications/echo/00-index|Echo — Índice]]
- Contratos: F-01 · F-02 · F-03 · [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]] · [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]] · [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]]
- Repos (paths citables): `xKoRx/echo: v3/sdk/contracts/promotion.go` · `xKoRx/echo: v3/gateway/internal/forge_ingest_handler.go` · `xKoRx/echo: v3/sdk/postgres/ingestion_service.go` (+ `ingestion_service_test.go` / `ingestion_noneffects_test.go` como corpus de gates) · `xKoRx/symphony: sqx/core/forge/handoff_producer.go` · `xKoRx/symphony: sqx/core/capabilities/handoff.go` (+ `delivery_test.go` / `handoff_producer_test.go`).
````

### P1 — `30-resources/applications/echo/00-index.md` (CREATE)

- **Purpose:** sub-índice curado del subdominio; una fila vigente por entidad + fila histórica; materializar desde `70-templates/index.md`.
- **Freshness:** las filas de estado heredan la de cada página; revalidar al publicar.

Propuesta de cuerpo (frontmatter = salida del template index; `area: "[[Echo]]"`; `updated` = fecha de publicación):

```markdown
# 📂 Echo — Índice

> [!info] Subdominio de [[30-resources/applications/00-index|Applications]]
> Páginas canónicas de Echo (plataforma) y Echo Forge (fábrica), sus contratos vigentes y la frontera compartida. Reglas: [[30-resources/00-RESOURCE-WIKI|Resource Wiki]] · Bitácora compartida: `../log.md`.

## Aplicaciones

| Página | Una línea | Baseline citado |
|---|---|---|
| [[echo-core]] | Plataforma de ejecución y Trade Journal de Echo (Bridge/Core Flink StateFun/Gateway); receptor de la frontera Forge. | echo `f7ddea18` |
| [[echo-forge]] | Fábrica cuantitativa sobre SQX (Temporal): campaña multi-wave → WFM → ranking → FinalistPromotion V2 + Apply; handoff NO cableado. | symphony `9fad768c` |

## Frontera

| Página | Una línea |
|---|---|
| [[echo-forge-integration-boundary]] | Frontera Forge→Echo: contrato frozen vigente, estado implementado por lado (con baseline), gaps G1–G7 y lo que la wiki no afirma. |

## Bitácora

| Página | Una línea |
|---|---|
| [[echo-core-changelog]] | Bitácora de cambios de [[echo-core]]. |

## Contratos vigentes (source-of-record, frozen — no re-derivar)

| Contrato | Una línea |
|---|---|
| [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]] | Contrato compartido SDK/analytics/handoff; autoridad congelada del lado Echo. |
| [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]] | Ingestión, identidad runtime y Live Authority; autoridad del SPEC E-04. |
| [[Echo Forge — F-01 Canonical Generation Concurrency Contract]] | CanonicalStrategyID puro + `ExecutionIntentKey` como discriminator de publication. |
| [[Echo Forge — F-02 Finalist Model V2 Contract]] | Membership estructural ≠ Top N; Promotion 2.0.0. |
| [[Echo Forge — F-03 SQX Long-Running Contract]] | elapsed ≠ failure; ceiling `MaxInt64ns−1s`; cancel de process-tree. |
| [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]] | Magic V1, seal write-once, HandoffManifestV1; C4/C5 verificados 2026-09-12. |

## Provenance (notas source)

| Nota | Cubre |
|---|---|
| [[Echo — Fuentes de implementación 2026-09-12 (f7ddea18)]] | Baseline Echo de campaña (fase B). |
| [[Echo Forge — Fuentes de implementación 2026-09-12 (9fad768c)]] | Baseline Symphony de campaña (fase C). |
| [[Echo — Fuentes de arquitectura y producto 2026-09-06]] | Provenance histórica Echo master 04c16bd. |
| [[Echo Forge — Fuentes de arquitectura y producto 2026-09-06]] | Provenance histórica Symphony a10c26c. |

## Histórico (retención; autoridad vigente en las páginas de arriba tras verificación)

[[Echo + Echo Forge — Arquitectura de producto, gaps y roadmap de cierre 2026]] · [[Echo + Echo Forge — Independent Reality Check and Time-to-Value Plan]] · [[Echo + Echo Forge — Evidencia de revisión independiente 2026-09-06]] · [[Echo + Echo Forge — Architecture Durability and Contract Review — Fable 5.1]] · [[Echo SDK — Canonical Contract Final Freeze Review — Fable 5.1]]
```

### P14/P15 — Notas source nuevas (CREATE, materializar desde `70-templates/source.md`)

- **`Echo — Fuentes de implementación 2026-09-12 (f7ddea18).md`:** `type: source`, `repo: "xKoRx/echo"`, `path: "v3/; specs/"`, commit `f7ddea18cab51db72c9765aa74381328134d7ce7`, branch `feature/e02-control-safety-journal-recovery`, master `a99f9a63`, `captured: 2026-09-12`. Cuerpo: referencia al artifact 02 (`10-projects/Echo/agentes/kb-consolidation/artifacts/02-echo-cartography.md`) como evidence pack; alcance (entrypoints, contratos SDK, migraciones 001–062, Gateway/E-02, Kafka, observability, tests); límite: E-02 branch-only, PHYSICAL_PARTIAL.
- **`Echo Forge — Fuentes de implementación 2026-09-12 (9fad768c).md`:** `type: source`, `repo: "xKoRx/symphony"`, `path: "sqx/"`, commit `9fad768ccd1f9d25ebb535a2d26edb3d74556c10`, branch `feature/f04-magic-version-handoff`, master `0b9742b0`, `captured: 2026-09-13`. Cuerpo: referencia al artifact 03; alcance (pipeline Temporal, WFM, ranking/promotion, MT5, migraciones 001–016, handoff librería); límite: F-04 branch-only, dirty file `phase4_performance.json` intocado.

### Páginas MOVE intactas (5–13)

Sin edición de contenido; conservan frontmatter, links y `created/updated`. Único ajuste permitido al mover: nada (los wikilinks son por nombre y sobreviven al MOVE). El changelog `echo-core-changelog.md` recibe append futuro normal; no se toca en la publicación salvo la entrada de log del propio movimiento.

## Moves (identity-preserving)

Todos los MOVE son renames de path dentro del mismo commit de publicación (links por nombre canónico no se rompen; riesgo único: `applications/00-index.md` debe actualizarse en el mismo cambio).

| Origen (`30-resources/applications/`) | Destino (`30-resources/applications/echo/`) |
|---|---|
| `echo-core.md` | `echo/echo-core.md` (+ reescritura P2) |
| `echo-forge.md` | `echo/echo-forge.md` (+ reescritura P3) |
| `echo-core-changelog.md` | `echo/echo-core-changelog.md` |
| `Echo Forge — F-01 Canonical Generation Concurrency Contract.md` | `echo/` (igual nombre) |
| `Echo Forge — F-02 Finalist Model V2 Contract.md` | `echo/` (igual nombre) |
| `Echo Forge — F-03 SQX Long-Running Contract.md` | `echo/` (igual nombre) |
| `Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract.md` | `echo/` (igual nombre) |
| `Echo SDK — Canonical Forge Integration and Analytics Contract V1.md` | `echo/` (igual nombre) |
| `Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1.md` | `echo/` (igual nombre) |
| `Echo — Fuentes de arquitectura y producto 2026-09-06.md` | `echo/` (igual nombre) |
| `Echo Forge — Fuentes de arquitectura y producto 2026-09-06.md` | `echo/` (igual nombre) |
| `Echo + Echo Forge — Arquitectura de producto, gaps y roadmap de cierre 2026.md` | `echo/` (igual nombre; supersede tras G) |
| `Echo + Echo Forge — Independent Reality Check and Time-to-Value Plan.md` | `echo/` (igual nombre; supersede tras G) |
| `Echo + Echo Forge — Evidencia de revisión independiente 2026-09-06.md` | `echo/` (igual nombre; ARCHIVE-histórico) |
| `Echo + Echo Forge — Architecture Durability and Contract Review — Fable 5.1.md` | `echo/` (igual nombre; supersede tras G) |
| `Echo SDK — Canonical Contract Final Freeze Review — Fable 5.1.md` | `echo/` (igual nombre; supersede tras G) |

## Index & Log Updates

### `30-resources/applications/00-index.md` (mismo cambio que los MOVE)

- Sección "📂 Catálogo": eliminar las filas `[[echo-core]]` y `[[echo-forge]]`; insertar UNA fila puntero: `| [[30-resources/applications/echo/00-index|Echo (subdominio)]] | Plataforma de ejecución + fábrica cuantitativa + frontera: ver sub-índice. | [[Echo]] | Go, Java |`. `[[stager-app]]` permanece.
- Sección "Arquitectura de producto": mover TODAS las filas Echo (2 contratos V1, 3 auditorías, 2 Fuentes, F-01…F-04, 2 Fable reviews = 11 filas) al sub-índice (secciones Contratos vigentes / Provenance / Histórico); la sección raíz queda sin filas Echo.
- Contadores: "Páginas: 16 aplicaciones" → actualizar (14 apps en catálogo raíz + subdominio echo); "Última ingesta" → fecha de publicación con nota "consolidación KBC → subdominio echo/".
- Sección "🔗 Links": la línea de `echo-core-changelog` puede quedarse (resuelve por nombre) pero se recomienda moverla al sub-índice y dejar el puntero.
- Fila corregida por la contradicción E: la frase "entrega finalistas a Echo Core" desaparece con la fila de echo-forge (cubierta por el puntero).

### `30-resources/applications/log.md` (append propuesto)

```
## [YYYY-MM-DD de publicación] ingest | KBC — consolidación del subdominio applications/echo/
- Creado `applications/echo/00-index.md`; MOVE de 16 páginas desde `applications/` (identidad preservada) en el mismo cambio.
- Reescritas [[echo-core]] (evidencia `xKoRx/echo@f7ddea18`) y [[echo-forge]] (evidencia `xKoRx/symphony@9fad768c`): corte estable/volátil, eliminado el claim falso "Forge entrega finalistas a Echo Core vía API" (ver [[echo-forge-integration-boundary]]).
- Creada [[echo-forge-integration-boundary]] (estado implementado + gaps G1–G7) y 2 notas source por baseline (f7ddea18 / 9fad768c).
- Índice raíz: filas Echo reemplazadas por puntero único al sub-índice. Cambio canónico: [[2026-09-1X-kbc-echo-subdomain-publication]].
```

Segundo append (SÓLO tras Fase G PASS): `## [fecha] ingest | KBC — supersede histórico Echo` listando las 5 piezas con `superseded_by`.

### `30-resources/00-RESOURCE-WIKI.md` (impacto declarado)

- En "Dominios activos" (línea ~107): declarar `applications/echo/` como subdominio activo (sub-índice propio, comparte `applications/log.md`), alineado con el mecanismo de escalado ya descrito en el mismo doc.

## Supersedes Metadata

Pares bidireccionales; se aplican SÓLO tras Fase G PASS (paso 9 del manifest E). En cada pieza histórica: `status: superseded`, campo `superseded_by` (lista de links); en la página reemplazante: campo `supersedes` listando la histórica. Antes de marcar, confirmar cobertura de claims únicos (32 deudas / hitos → cubiertos como estado volátil con baseline en las páginas nuevas o referenciados al histórico; matrices C-1…C-7 y FR-1…FR-5 → quedan referenciadas desde los contratos que ya existen, el histórico se conserva).

| Pieza histórica (`…/echo/…`) | `superseded_by` |
|---|---|
| Echo + Echo Forge — Arquitectura de producto, gaps y roadmap de cierre 2026 | [[echo-core]] · [[echo-forge]] · [[echo-forge-integration-boundary]] |
| Echo + Echo Forge — Independent Reality Check and Time-to-Value Plan | [[echo-core]] · [[echo-forge]] · [[echo-forge-integration-boundary]] |
| Echo + Echo Forge — Architecture Durability and Contract Review — Fable 5.1 | [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]] · [[echo-forge-integration-boundary]] |
| Echo SDK — Canonical Contract Final Freeze Review — Fable 5.1 | [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]] |
| Echo + Echo Forge — Evidencia de revisión independiente 2026-09-06 | sin supersede (ARCHIVE-histórico: fotografía física datada; sólo `status: archived` si el tipo lo permite, sino fila histórica) |

Notas sin cambio de estado: los 2 specs repo-side superseded de facto (`FEAT-SQX-ECHO-INGESTION`, `FEAT-SQX-ECHO-DEPLOYMENT-LINK`) NO se tocan (cero escritura en repos); quedan documentados como deuda repo-side para fase posterior. `GUIA_WORKER_TEMPORAL_MT5.md` y `30-resources/sqx/` + `Diagrama visual…` (archive/MERGE) quedan FUERA de este draft: su gate es la verificación G del manifest E (pasos 7–8), no de esta tarea.

## Conflicts / Unknowns

- Vault baseline declarado en mi tarea (`a87aa62`) vs HEAD real reconfirmado (`12d250a`): drift post-baseline de avances del vault, no contradicción de verdad; la fase H reconcilia contra HEAD vigente.
- La tabla de la topología A nombraba la frontera `Echo — Forge Integration Boundary V1.md` (provisional) y mi asignación usa `echo-forge-integration-boundary.md`: resuelto con kebab + aliases (decisión 4); si el publisher prefiere el nombre Title Case, los aliases ya lo cubren pero debe elegirse UNO como nombre de archivo.
- `last_verified` propuesto (2026-09-12/13) refleja la fecha de verificación de las fases B/C/D, no la de publicación; la fase H debe re-validar lo DOCUMENTATION_RELEVANT contra HEAD antes de publicar y actualizar ese campo sólo si re-verifica de verdad (regla: `last_verified` = verificación real).
- El conteo de tests front (33) y la semántica fina del circuit breaker de sesión heredan Confidence MEDIUM de la fase B: no los incluí como afirmación cargante en las páginas (los gaps listados no dependen de ellos).
- Números de página/inbound links provienen del manifest E (grep, sin Graphify); el reindex de Graphify al cierre del batch puede revelar huérfanos o backlinks no contabilizados.
- No incluí el draft del nuevo runbook GUIA_WORKER_TEMPORAL_MT5 (paso 7 del manifest E): depende de verificación contra `sqx/cmd/sqx-mt5-worker` que corresponde a G/H, no a F.

## Recommendations

- Publicar en un solo cambio los pasos: crear sub-índice + 16 MOVEs + update del índice raíz + append de log (ventana anti-drift); luego reescrituras/creates de contenido; luego (tras G PASS) supersedes; reindex Graphify al cierre; impacto declarado en 00-RESOURCE-WIKI.
- Verificar antes de publicar que ninguna edición rompe el gate "una sola fila vigente por entidad" en ambos índices (raíz y subdominio).
- Reportar al orchestrator el hallazgo de seguridad de la fase E (`APIs.md` con credenciales en texto plano) — sigue pendiente de decisión humana, fuera de KBC.
- Fase posterior repo-side (I/K): marcar superseded los 2 specs Forge desactualizados y corregir los AGENTS.md de ambos repos (paths de máquina).

## Handoff

**Para Fase G (documentation-verifier):** refutar adversarialmente, contra los repos reconciliados, en este orden: (1) el estado de la frontera según la página P4 (que G1–G6 sigan siendo ciertos a HEAD; que el pin de contracts siga vigente; que F-04 siga branch-only en symphony); (2) las afirmaciones branch-only de P2 (E-02 no mergeado) y P3 (F-04 branch-only, pipeline sin cableado); (3) que no quedó ninguna otra instancia del claim "Forge entrega a Echo" (buscar en runbook `symphony-zeus-troubleshooting` y memory notes); (4) vigencia de la invariante 1 VM conservada en P3; (5) los dos unknowns que bloquean supersede: cobertura de los 32 deudas/hitos de la auditoría maestra y exactitud de `GUIA_WORKER_TEMPORAL_MT5` contra el worker MT5 real. PASS habilita la publicación y los supersedes.

**Para la publicación H/P (ejecución):** (1) resolver el naming final de la frontera (kebab propuesto); (2) materializar P1/P4/P14/P15 con `materialize_schema_note.py` (nada de frontmatter a mano) y aplicar los drafts de P2/P3 como cuerpo sobre las páginas movidas; (3) ejecutar los MOVEs + índice raíz + log en un solo commit; (4) actualizar `updated` y `last_verified` (sólo con re-verificación real contra HEAD); (5) tras PASS, aplicar la metadata de Supersedes en pares y el segundo append de log; (6) reindex Graphify; (7) impacto declarado en `00-RESOURCE-WIKI.md`; (8) cero escrituras en `xKoRx/echo`/`xKoRx/symphony` (symphony conserva su dirty file). Este draft es propuesta: ninguna superficie canonical fue escrita por esta fase.
