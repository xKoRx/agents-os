---
type: resource
schema_version: 1
status: active
area: "[[Echo]]"
sources:
  - "[[Echo Forge — Factory V2 Completion]]"
  - "[[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]]"
  - "[[Echo Forge — F-02 Finalist Model V2 Contract]]"
  - "[[Echo Forge — F-03 SQX Long-Running Contract]]"
  - "[[Echo + Echo Forge — Deferred Certification Backlog]]"
last_verified: "2026-09-16"
confidence: verified
aliases:
  - F-05-I SPEC
  - release matrix and read surface contract
  - Echo Forge F-05-I
related:
  - "[[Echo Forge — F-05-I Cohesive release and read surfaces]]"
  - "[[Echo Forge — Factory V2 Completion]]"
entities:
  - "[[Echo Forge]]"
  - "[[xKoRx/symphony]]"
tags:
  - kind/resource
  - area/echo
  - project/echo-forge
created: "2026-09-13"
updated: "2026-09-16"
---

# Echo Forge — F-05-I Release Matrix and Read Surface Contract

Esta Resource es el contrato técnico de `F-05-I — Cohesive release and read surfaces` (preparación de implementación de F-05). Define qué debe quedar cierto. La ejecución vive en [[Echo Forge — F-05-I Cohesive release and read surfaces]]. F-05-I NO publica release, NO ejecuta gates físicos y NO marca ningún T2.11/T2.12/T2.13. Veredicto válido al implementar: `F-05-I IMPLEMENTED / SOURCE VERIFIED`.

Baseline de source: `xKoRx/symphony@b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43` (= HEAD de `origin/feature/f04-magic-version-handoff`; release `0.2.98`). Branch de implementación: `codex/f05-release-prep`, creada desde el SHA exacto, nunca desde master ni desde un checkout local divergente (el checkout local del repo puede estar en `9fad768`, que NO contiene C5; la autoridad es el SHA). **Cierre 2026-09-16:** manager SOURCE / CONTRACT REVIEW APPROVED de la verificación T7-A (agent-run `2026-09-16-zcode-glm-5.3-flash-f05i-t7a-verification`, evidencia gates A–K en [[Echo Forge — F-05-I Cohesive release and read surfaces]]); T7-CLOSE ejecutado en commit de cierre `3d0e8c958765da23840e00bf1a0ac017fc47597a`: fila `f05i-read-surface` con `implementation_sha 0ddd4db` (source aprobado, no el commit de cierre), `implemented` DONE (evidencia git) y `source_verified` DONE (evidencia tests). Veredicto: `F-05-I IMPLEMENTED / SOURCE VERIFIED — DECLARATIVE CLOSURE COMPLETE`. Dejar explícito: release NOT PERFORMED; deploy NOT PERFORMED; physical certification NOT RUN; cross-lane certification NOT PERFORMED; F-05-C continúa diferida; los gates CERT mantienen sus estados; no se inventó golden auténtico. La receta documental de persistencia corregida en T7-CLOSE usa las familias reales `TestLoadForgeCampaignResult|TestLoadFlowRunResult` (vive en el proyecto, esta SPEC no congela comandos de test). Contratos frozen inputs: F-01/F-02/F-03/F-04, S0 Echo, B1A/B1B/B2.

`DATABASE MIGRATION: NONE`. Toda la superficie es read-only sobre tablas/colecciones existentes; cero writes en runtime; cero cambios de schema.

## Síntesis vigente

### Problema

El pipeline V2 termina en FinalistPromotion V2 + Apply + (branch F-04) seal/handoff, y toda esa verdad vive en PostgreSQL/MongoDB/MinIO/Temporal, pero no existe ninguna superficie de consulta: `forge.Service` (result v1/v2) y `ControlPlane.LoadForgeCampaignResult` no tienen callers productivos; no hay HTTP/API/GraphQL/Hasura; `sqx-flowkit` sólo hace `push-output`; y la inspección real del owner pasa por `sqx/tools/*.go` (scripts `go run` con hosts hardcodeados) o SQL manual. Además, el estado release/certificación por capacidad vive disperso en notas y no en un artefacto determinístico.

### Veredicto central

**Capas, no un producto nuevo:**

```text
PostgreSQL/MongoDB authorities (existentes, intocables)
→ narrow read ports (capabilities, read-only, nuevas)
→ read services + proyección funnel (core/forge + core/releasematrix, puras)
→ CLI JSON determinístico (subcomandos sqx-flowkit inspect)
→ release matrix (artefacto repo + validador)
→ handoff F-05-C (checklist + manifest template + contrato read-surface)
```

- **Arquitectura elegida: CLI JSON sobre la librería existente.** No se crea servidor HTTP (auth/deploy es territorio F-05-C+/front), no se toca `internal/di` (flowkit ya trae Postgres/etcd/telemetry; Mongo se bootea con `sharedmongo.New` igual que `sqx/cmd/sqx-worker/persistence.go`), no se duplican authorities. El contrato JSON versionado ES el backend contract que el futuro front consumirá envolviendo los mismos read services.
- **Release matrix = declaración validada, no segunda autoridad.** Vive como artefacto versionado en el repo (`sqx/core/releasematrix/release-matrix.json`, embebido en el binario del CLI vía `go:embed`) + validador puro (`sqx/core/releasematrix`). La autoridad de release sigue siendo `deploy_release.sh`/`release-authority`/stager; la matriz declara estados con evidencia y jamás deriva un estado de otro.
- **Funnel = proyección pura sobre stage_executions.** Topología V2 dinámica: los boundaries son los `stage_key` realmente ejecutados (stages omitidos no aparecen; stages repetidos agregan). Cero hardcode builder→…→handoff.
- **Zero finalists es resultado válido** (`STRUCTURAL_EMPTY`/`TOP_PROJECTION_EMPTY`, ranking `NOT_MATERIALIZED`), nunca error de software.

### Alcance exacto (in scope)

1. Read ports nuevos (sólo lecturas): listado de campañas (paginado determinístico), stage executions por FlowRunRef exacto, participaciones por FlowRunRef/StrategyRef, versiones/manifests/entregas por StrategyRef.
2. Read services: campaña (`LoadForgeCampaignResult` existente), flow run (`forge.Service.Result` existente, finalmente cableado a un caller), inspección de estrategia (identidad + magic + versiones + handoff por refs exactos), timeline de stages + funnel projection.
3. CLI `sqx-flowkit`: subcomandos `campaign get|list`, `run get|stages`, `strategy get`, `release-matrix`; salida JSON versionada a stdout; exit codes por error kind; `push-output` queda byte-idéntico en comportamiento.
4. Release matrix: paquete `sqx/core/releasematrix` (schema `sqx-release-matrix.v1`), artefacto `sqx/core/releasematrix/release-matrix.json` embebido con las capacidades F-01…F-04 + pipeline + release pipeline, estados implementada/verificada/released/deployed/certificada-física/cross-lane independientes con evidencia y autoridad.
5. Handoff F-05-C: `docs/echo-forge/f05-read-surface.md` (contrato JSON/commands/semántica), `docs/echo-forge/f05-conformance-checklist.md`, `docs/echo-forge/f05-certification-manifest-template.json`.
6. Tests: unit/contract/persistence/BWC/negative + race + vet según matriz del proyecto.

### Out of scope (prohibido en F-05-I)

- Marcar PASS cualquier gate físico (T2.11/T2.12/T2.13, E-04 T21/AC-37, Windows/MT5, FULL golden).
- Publicar release (`release-authority`, `deploy_release.sh`, MinIO publish, stager).
- Fabricar golden real o usar fixtures sintéticas como evidencia CERT.
- Frontend, SQX viewer `-gui`, edición de estrategias, HTTP server, GraphQL/Hasura.
- Writes a cualquier DB (incluida Echo), nuevas tablas/columnas/migrations, backfills.
- Reabrir semántica F-01…F-04/S0/B1A/B1B/B2/Magic V1/Finalist V2/HandoffManifestV1.
- Exponer evidencia Mongo secundaria (databank/wfm/deviation/export_runs) — documento como no-superficie de F-05-I.

## Release matrix contract (`sqx-release-matrix.v1`) — CORREGIDO Planning C1 (2026-09-16)

### Ubicación del artefacto (C1.1)

- **Ruta canónica:** `sqx/core/releasematrix/release-matrix.json` (co-ubicada con el validador, versionada en git, declaración humana editada por NORMAL). **Prohibido `deploy/release-matrix.json`** y cualquier artefacto declarativo dentro de `deploy/`.
- **Evidencia de la decisión:** `deploy/` es el WatchRoot vivo del pipeline de release. `deployer-watcher` observa por defecto `./deploy` (`deployer/cmd/deployer-watcher/main.go`, fallback etcd `config/watch_root`), su source hace snapshot recursivo con `filepath.WalkDir` (`deployer/adapters/source-fsnotify/source.go`) y `deploy_release.sh` usa `deploy/` como staging de publicación (`deploy/<version>/linux-amd64/`; el watcher sincroniza ese árbol a MinIO y publica `deploy/manifest.json` como último paso). Un JSON declarativo ahí hoy no se subiría únicamente porque `StaticLayout.ComputeKey` exige exactamente `<root>/<semver>/<platform>/<file>` o el `manifest.json` raíz (`deployer/adapters/pathing-staticlayout/pathing.go`; `release-matrix.json` cae en `ok=false` y el planner lo salta en `deployer/core/planner/simple.go`) — es protección **accidental, acoplada al layout**: cada edición dispararía ciclos de plan contra MinIO, el archivo viviría dentro del árbol de staging publicable y un cambio futuro de layout podría convertirlo silenciosamente en key publicable, mintiendo sobre qué es un artefacto de release. En `sqx/core/releasematrix/` la ruta está fuera del WatchRoot y fuera del staging: el watcher no puede verla y el pipeline no puede publicarla (dos garantías independientes).
- **Cómo lo encuentra T5 (C1.2):** no por path — por embedding. Ver §Política de carga.

### Política de carga portable (C1.2)

- **Fuente por defecto inequívoca: embedding.** `//go:embed release-matrix.json` en el paquete `sqx/core/releasematrix` (mismo directorio del paquete: restricción de `go:embed` cumplida; idioma ya usado en el repo por `sqx/adapters/registry-postgres/migrations/runner.go` y `postgrestest/db.go`). El binario `sqx-flowkit` lleva la matriz dentro; mismo binario ⇒ misma matriz, determinístico por construcción.
- **API congelada del paquete:** `Embedded() []byte` (bytes del artefacto), `LoadEmbedded() (Matrix, error)`, `Parse(data []byte) (Matrix, error)`, `Load(path string) (Matrix, error)` (override explícito), `Validate(Matrix) error`, `Marshal canónico` (indent 2 espacios + newline final; el artefacto committed debe ser exactamente esa salida — test de igualdad byte a byte).
- **Override explícito:** `sqx-flowkit release-matrix --matrix <path>`. Un override inválido (no existe, no parsea, falla validación) es error **tipado** `INVALID_ARGUMENT` → exit 2 con mensaje en stderr; nunca fallback silencioso al embebido.
- **Restricciones duras:** ejecutable desde cualquier working directory; no exige checkout del repo; no exige acceso a `deploy/`; cero resolución de rutas relativas al repo (el default relativo-repo del plan original queda **eliminado**). Test de portabilidad: ejecutar el handler del subcomando con CWD en directorio temporal vacío ⇒ misma salida byte a byte.
- **No se implementa el loader en esta sesión** (Planning C1 es CONTRACT REVIEW); el contrato anterior es la implementación obligatoria de T1/T5.

### Dimensiones, estados y semántica (C1.3 + C1.4)

- **Filas = capacidades**, IDs frozen (orden = `capability` ASC): `apply-selected-run`, `b1a-mt5-ownership`, `b1b-mt5-wallclock`, `b2-cancel-recovery`, `f01-identity`, `f02-finalist-model-v2`, `f03-sqx-long-running`, `f04-handoff-delivery`, `f04-magic-allocation`, `f04-strategy-version-seal`, `f05i-read-surface`, `global-ranking`, `mt5-reconcile-score-shadow`, `pipeline-core`, `release-pipeline`, `robust-selection`, `wfm-evaluator`.
- **Campos por capability:** `capability`, `contract_refs[]` (≥1), `producer_paths[]` (≥1, paths clave sin wildcards — `*` rechazado por validador), `persistence_authority` (storage concreto + tablas/colecciones; nunca afirma intercambiabilidad entre PostgreSQL/MongoDB/Temporal/etcd/MinIO), `read_surface` (`sqx-flowkit …` o `none`), `required_refs[]`, `implementation_sha` (`^[0-9a-f]{7,64}$` o vacío con evidencia), `states` (objeto con UNA entrada por dimensión) y `deploy_targets[]` (ver abajo).
- **Dimensiones (seis, independientes):** `implemented`, `source_verified`, `released`, `deployed`, `physically_certified`, `cross_lane_certified`. El validador jamás infiere una de otra; `released ≠ deployed` y `source_verified ≠ physically_certified` son reglas de lectura explícitas (alineadas 1:1 con la taxonomía frozen de [[Echo + Echo Forge — Deferred Certification Backlog]]).
- **Estado por dimensión:** objeto `{status, evidence, evidence_kind, gate?, as_of?}` con semántica exacta:
  - **DONE** = la dimensión está satisfecha con evidencia verificable registrada (histórica o actual); `evidence` y `evidence_kind` obligatorios, `gate` prohibido. En dimensiones físicas/de release/deploy, DONE histórico exige `as_of` + evidence_kind de certificación y su alcance es el SHA/release de época evidenciado — **nunca certifica la release actual por arrastre**.
  - **OPEN** = requerido y no satisfecho hoy; `evidence` declara qué falta (p.ej. observación física pendiente ⇒ incertidumbre explícita); `gate` opcional.
  - **DEFERRED** = requerido, retirado del critical path a un gate de la campaña CERT; `gate` obligatorio (`^CERT-[A-Z0-9]+(-[A-Z0-9]+)*$`).
  - **NOT_APPLICABLE** = la dimensión no aplica a esa capability; `evidence` justifica por qué.
  - `evidence_kind` enum: `git | tests | release_manifest | deployment_proof | runtime_observation | certification_record | cross_lane_receipt | none` (sólo admisible `none` con status ≠ DONE).
- **`as_of`:** fecha `YYYY-MM-DD` de la evidencia; obligatoria en DONE de `released`/`deployed`/`physically_certified`/`cross_lane_certified`.
- **Representación de flota (C1.3):** la dimensión `deployed` lleva además `deploy_targets[]`; cada target = `{target, release, release_present, process, evidence, as_of?}` con enums de **observación** (hechos, no certificación): `release_present: OBSERVED|NOT_OBSERVED`, `process: RUNNING|NOT_OBSERVED`. Reglas: `release_present=OBSERVED` ⇒ `release` no vacío (presencia observada de una release identificada); `process=RUNNING` exige observación de proceso real; target no observado = `NOT_OBSERVED` explícito (nunca inferido de publicación ni de archivos presentes); targets con versiones distintas = valores `release` distintos por target. Si `deployed.status=DONE` el validador exige `len(deploy_targets) ≥ 1` (contención de evidencia, no derivación de estados). NO se crea un sistema de monitoreo ni inventario de flota: esto es declaración con evidencia referenciada.
- **Prohibiciones (C1.4):** no declarar PASS físicos nuevos sin evidencia; no borrar certificaciones históricas demostradas (F-03 physical PASS y B1A/B1B/B2 CLOSED son historia verdadera que la matriz conserva como DONE histórico con `certification_record` + `as_of`); no inferir certificación de una fase desde otra; no confundir RELEASED con DEPLOYED ni SOURCE VERIFIED con PHYSICALLY CERTIFIED; certificación histórica no comprobable ⇒ queda registrada como no verificada (OPEN), jamás resultado inventado.

### Autoridades de datos por dimensión (C1.5)

| Dimensión / campo | Evidencia admisible (`evidence_kind`) | Autoridad concreta |
|---|---|---|
| `implemented` | `git` | commit SHA presente en la branch/lineage autorizado (`git` es la única autoridad) |
| `source_verified` | `tests`, `certification_record` | veredictos de revisión source/contract registrados (notas/manager review) + corridas locales de tests; jamás implica físico |
| `released` | `release_manifest` | `deploy/manifest.json` de época, output `release-authority` (`sqx-release-authority.v1`), manifest+digest publicado en MinIO por `deploy_release.sh` |
| `deployed` (+ `deploy_targets[].release_present`) | `deployment_proof`, `runtime_observation` | deployment proof por jerarquía: activación stager, inspección `stager-runtime.service`, `CURRENT/PENDING`; presencia en host observada. La sola publicación NO alimenta esta dimensión |
| `deploy_targets[].process` | `runtime_observation` | observación de proceso real (servicio/PID); los archivos presentes en host NO prueban proceso activo |
| `physically_certified` | `certification_record` | veredictos de campañas físicas registradas (T2.11/T2.12/T2.13, job físico F-03, épocas B); tests locales y fixtures NO califican |
| `cross_lane_certified` | `cross_lane_receipt` | receipt + read-back del lane consumidor (Echo); synthetic ≠ PASS |
| `persistence_authority` | `git` | schema/migrations + adapters: nombre concreto de storage y tablas/colecciones (PostgreSQL sqx, MongoDB forge, MinIO bucket, columnas Temporal, etcd); cada row nombra la suya y ninguna declara equivalencia entre services |
| Override de CLI y contenido | — | la matriz consulta cero infraestructura en runtime: es declarativa; toda observación pendiente queda como no verificada |

### Contenido de verdad inicial (congelado; T1 lo transcribe, no lo decide)

- **Filas históricas CLOSED:** `b1a-mt5-ownership` SHA `185825c`, `b1b-mt5-wallclock` SHA `ef65dd1`, `b2-cancel-recovery` SHA `db8a022` — implemented/source_verified/physically_certified DONE históricos (veredictos PASS/CLOSED de época, evidence = record Factory V2 + contratos frozen + SHA; `as_of` época 2026-09-06/08); released DONE por `0.2.98` (contiene esos SHAs en su lineage git) con `as_of` 2026-09-13; deployed OPEN (deploy de época no re-verificable hoy ⇒ incertidumbre conservada; re-check sólo con delta); cross_lane NOT_APPLICABLE justificado (sin lane consumidor).
- **Fases cerradas:** `f01-identity` (`0509342`), `f02-finalist-model-v2` (`c3b7ede`), `f03-sqx-long-running` (`382f4ba`) — implemented/source_verified DONE; released DONE por `0.2.98` (lineage); deployed OPEN con targets linux OBSERVED / windows NOT_OBSERVED (misma evidencia stager 2026-09-13); `f03` además physically_certified DONE histórico `as_of` 2026-09-10 (job real `14m51.98s` COMPLETED 3000/3000, heartbeat T+10m, cancel aislado — record Factory V2); f01/f02 physically_certified OPEN sin gate de campaña propia (su física de época no está registrada como campaña certificable separada ⇒ pendiente de verificación, no inventada).
- **F-04 (tres filas):** implemented/source_verified DONE @ `b57bfb2`; released DONE `0.2.98` `as_of` 2026-09-13; deployed OPEN con `deploy_targets`: `{linux-amd64, 0.2.98, OBSERVED, RUNNING, stager-runtime.service /opt/stager/releases/0.2.98 (Zeus/Hera/Kronos), 2026-09-13}` y `{windows-amd64, "", NOT_OBSERVED, NOT_OBSERVED, viewer policy gap mt5-kronos}`; physically_certified DEFERRED con gates: magic-allocation `CERT-F04-01`, strategy-version-seal `CERT-F04-02`, handoff-delivery `CERT-F04-03`; cross_lane DONE prohibido — handoff-delivery DEFERRED `CERT-E04-01`, resto NOT_APPLICABLE.
- **Capacidades de pipeline V2:** `pipeline-core`, `wfm-evaluator`, `global-ranking`, `robust-selection`, `apply-selected-run`, `mt5-reconcile-score-shadow` — implemented/source_verified DONE @ baseline auditado `b57bfb2` (existencia + verificación source en el recon F-05-I; SHA de fase individual no atribuible ⇒ se declara el SHA auditado, no se inventa atribución); released DONE `0.2.98`; deployed OPEN (targets como F-04); physically_certified DEFERRED `CERT-F05-02` (FULL golden real); cross_lane NOT_APPLICABLE.
- **`release-pipeline`** (deploy_release/release-authority/stager/deployer-watcher): implemented/source_verified DONE @ `b57bfb2`; released NOT_APPLICABLE (es la autoridad que publica, no artefacto publicado); deployed OPEN con targets linux OBSERVED / windows NOT_OBSERVED; physically_certified DEFERRED `CERT-F05-01` (release/deployment proof cohesivo); cross_lane NOT_APPLICABLE.
- **`f05i-read-surface`** (sí misma): implemented OPEN (T1/T5/T6/T7 pendientes en `codex/f05-release-prep`, HEAD `3da8b47`); source_verified OPEN; released OPEN (ninguna release contiene F-05-I aún); deployed OPEN (sigue a la release cohesiva futura); physically_certified DEFERRED `CERT-F05-02`; cross_lane NOT_APPLICABLE. Se actualiza a DONE/ source_verified DONE sólo tras T7 con veredicto `F-05-I IMPLEMENTED / SOURCE VERIFIED`. **(Actualizado en T7-CLOSE 2026-09-16, commit `3d0e8c9`: implemented DONE/git y source_verified DONE/tests con SHA `0ddd4db`; released/deployed OPEN, físico DEFERRED `CERT-F05-02` y cross_lane NOT_APPLICABLE intactos.)**
- **Guard tests corregidos (C1.4):** (a) el validador rechaza `physically_certified`/`cross_lane_certified` DONE sin `certification_record`/`cross_lane_receipt` + `as_of`; (b) guard de contenido del artefacto committed: cero DONE físico/cross-lane fuera de la allowlist histórica `{b1a-mt5-ownership, b1b-mt5-wallclock, b2-cancel-recovery, f03-sqx-long-running}`; (c) filas F-04/pipeline/release-pipeline/f05i: physically_certified ∈ {OPEN, DEFERRED} y cross_lane ∈ {OPEN, DEFERRED, NOT_APPLICABLE}; (d) `f04-handoff-delivery.cross_lane_certified.gate ∈ {CERT-E04-01, CERT-F04-03}` cuando DEFERRED. La allowlist vive en el test (datos de verdad documentados), no en lógica de derivación del validador.

## Read surface contract

### Comandos y documentos (todos JSON versionados a stdout; las superficies F-05-I nuevas usan `schema`, `run get` conserva `schema_version` del modelo preexistente ForgeResult)

| Comando | Salida | Autoridad leída |
|---|---|---|
| `sqx-flowkit campaign get <ForgeCampaignRef>` | `sqx-forge-campaign-result.v1` (modelo existente) | PG `forge_campaigns*` vía `LoadForgeCampaignResult` |
| `sqx-flowkit campaign list [--limit N] [--cursor C]` | `sqx-campaign-list.v1` (`schema`, `campaigns[]` (ref, status, created_at), `next_cursor` string\|null SIEMPRE presente; orden `created_at DESC, ref ASC`) | PG `forge_campaigns` (listado presentación; identidad sigue siendo el ref exacto) |
| `sqx-flowkit run get <FlowRunRef> [--ranking name]` | `forge-result.v1|v2` (modelo existente) | PG + Mongo vía `forge.Service.Result` |
| `sqx-flowkit run stages <FlowRunRef>` | `sqx-run-stage-timeline.v1` + funnel embebido | PG `stage_executions`/`flow_run_strategies` |
| `sqx-flowkit strategy get <StrategyRef>` | `sqx-strategy-inspect.v1` | PG `strategies`/`strategy_magic`/`strategy_versions`/`handoff_manifests`/`handoff_deliveries`/`flow_run_strategies` |
| `sqx-flowkit release-matrix` | `sqx-release-matrix.v1` validado | artefacto embebido (`sqx/core/releasematrix/release-matrix.json`) u override `--matrix` |

- `campaign get`/`run get`/`strategy get` resuelven **sólo por ref exacto**; `list` es paginación de presentación y nunca define identidad ("latest" no es ref válido y debe fallar `INVALID_ARGUMENT`).
- **Paginación `campaign list` — corrección pre-release F05I-PAGINATION-C2 (2026-09-16, decide F05I-PAGINATION-C1):** `sqx-campaign-list.v1` emite `next_cursor` (`string | null`, SIEMPRE presente en el JSON) como **server-issued opaque cursor**. Algoritmo N+1: el read service valida `limit ≥ 1` (y overflow-safe del sondeo) ANTES de consultar, hace la query con `LIMIT N+1`, emite exactamente N filas; si llegó la fila N+1, `next_cursor` codifica el boundary (created_at, ref) de la **última fila EMITIDA** (jamás la N+1); si no llegó, `next_cursor: null` (no existe fila posterior al boundary según el estado durable observado por esa query). Página vacía válida: `{"schema":"sqx-campaign-list.v1","campaigns":[],"next_cursor":null}`. El consumidor trata el token como opaco: nunca lo construye ni decodifica, sólo lo reenvía (`campaign list --cursor <next_cursor>`); el codec `EncodeCampaignCursor`/`DecodeCampaignCursor` vive en `sqx/core/forge` (encoding actual base64url de JSON compacto: detalle reservado del servidor, no obligación del cliente). Sigue siendo schema `sqx-campaign-list.v1` (F-05-I nunca fue released; no v2). Registro: sin migration, sin cambio de port (`ForgeCampaignListReader` intacto), sin cambio de adapter/SQL (T2 frozen); T4 reabierto únicamente por este delta de pagination; ningún gate físico tocado.
- `strategy get` (shape): identity (strategy_ref, canonical_strategy_id opaco, instrument/direction/timeframe desde la fila durable, logical_type/classification_version si existen), participation[] (flow_run_ref + role, orden determinístico `participated_at, flow_run_ref`), `magic` (objeto `{registry_namespace, magic_decimal, allocation_ref, assigned_at}` o `null` si no hay fila), `strategy_versions[]` (`version_ref, payload_digest, sealed_at`; orden `sealed_at, version_ref`), `handoff[]` (`idempotency_key, payload_digest, wave_key, version_ref, decision_ref, created_at` + `delivery {state, updated_at}`; orden `created_at, idempotency_key`).
- **Provenance:** cada elemento lleva refs durables exactas (FlowRunRef, StrategyRef, DecisionRef, RankingSnapshotRef, ScoreRef, EvaluationRef donde el modelo ya los expone, StageExecutionRef, allocation_ref, version_ref, idempotency_key). Prohibido: lookup por latest, filename como identity, timestamp como join, parse de CanonicalStrategyID, rankings como autoridad de membership. Ausencia opcional = `null` explícito; nunca ref inventada.

### Funnel projection (`sqx-forge-funnel-projection.v1`)

- Input: stage executions de UN FlowRunRef (orden determinístico `(created_at, stage_instance_key)`) + participaciones.
- Output `boundaries[]`: una entrada por `stage_key` observado, ordenada por `(min(created_at) del key, stage_key ASC)`; cada entrada: `{stage_key, executions_total, by_status {PENDING,RUNNING,COMPLETED,FAILED,CANCELLED}, strategy_subjects_seen, strategy_subjects_completed, error_codes[]}`.
- Stages omitidos por el workflow NO aparecen (no zero-fill); stages repetidos agregan bajo el mismo key. Ningún mapeo stage→stage hardcodeado; la topología se lee de los datos.
- El funnel es **projection**: no crea refs, no muta authorities, no redefine membership. Los finalistas/counters de campaña vienen del result/campaign model, no del funnel.
- Zero finalists: `run get` devuelve promotion AVAILABLE con `finalists: []` + reason estructural y ranking `NOT_MATERIALIZED` cuando corresponde; exit 0.

### Error / empty semantics (freeze)

| Caso | Comportamiento |
|---|---|
| Ref malformado / "latest" | `INVALID_ARGUMENT`, exit 2 |
| Run/campaign/strategy ausente | `NOT_FOUND`, exit 4 (exit code nuevo `ExitNotFound = 4`); sin cuerpo parcial |
| >1 snapshot para el ranking autoritativo | `AMBIGUOUS_RESULT` (taxonomía existente de `forge.Service`) |
| Run existe, stage aún pendiente | timeline con stage `PENDING`; jamás se reporta como 0 o ausente |
| Stage fallido | `FAILED` + `error_code`/`error_message` persistidos, sin ocultar |
| Flow terminal sin ranking producido | `NOT_PRODUCED` (válido, exit 0) |
| Ausencia opcional (magic/versiones/handoff pre-F-04) | `null` explícito; ausencia ≠ cero |
| Métrica opcional ausente | omitida (`omitempty`), nunca 0 |
| Zero finalists / zero supply | resultado válido COMPLETED (`STRUCTURAL_EMPTY`), exit 0 |
| Provenance incompleta/contradictoria | `CONTRACT_INCONSISTENCY` (exit 50) con detalle; falla explícita, sin adivinar |
| Historia V1 (policy 1.0.0) | legible vía result v1 path existente; sin coerción a V2 |
| Store caído | `INFRASTRUCTURE_FAILURE`, exit 50 |

- No existe estado `PARTIAL` inventado: la parcialidad se representa con los estados existentes por nivel (campaign FAILED con `failure_code` + waves started/completed; flow COMPLETED con counts; stages con status individual). La ausencia nunca se esconde como cero.
- JSON determinista: sin timestamps de query, marshaling de structs (orden de campos fijo), mismo estado durable ⇒ mismos bytes.

### Exit codes (flowkit, aditivos)

`0` respuesta válida (incluye NOT_MATERIALIZED/zero finalists/NOT_PRODUCED y página de lista vacía) · `2` INVALID_ARGUMENT (incluye override `--matrix` inválido) · `4` NOT_FOUND (nuevo) · `10` config/DI · `50` CONTRACT_INCONSISTENCY/INFRASTRUCTURE/AMBIGUOUS_RESULT/otros internos. `push-output` conserva sus códigos actuales. Mapping ErrorKind→exit: `INVALID_ARGUMENT→2`, `NOT_FOUND→4`, `CONTRACT_INCONSISTENCY→50`, `INFRASTRUCTURE_FAILURE→50`, `AMBIGUOUS_RESULT→50`; fallo de boot DI → `10` con formato stderr `<code>:config_error:<detalle>`.

### Grafo mínimo de inicialización por subcomando (C1.6)

El `main.go` actual llama un boot DI completo (etcd, telemetry SQX/MinIO/Postgres/Temporal, MinIO, Postgres, Temporal — `Init()` con `di.WithTemporal()` etc.) **antes** de parsear el subcomando, y `runPushOutput` vuelve a llamar `di.InitSelective` (etcd, telemetry Document, MinIO) sin guard de idempotencia en `internal/di` (doble creación de clientes, primera fuga). T5 corrige el orden sin tocar `internal/di`: **dispatch primero, boot después, sólo lo que el subcomando usa.**

| Subcomando | Boot (exacto) | Prohibido |
|---|---|---|
| `release-matrix` | **Ninguno**: cero `di.InitSelective`, cero etcd/telemetry/red; sólo `releasematrix.LoadEmbedded()` u override `--matrix`, validar, emitir JSON a stdout | MongoDB, PostgreSQL, etcd, Temporal, MinIO |
| `campaign get` / `campaign list` | `di.InitSelective("sqx-flowkit", WithEnvironment(ENV), WithEtcd(), WithTelemetry(telemetry.Postgres), WithPostgres())` → `registrypostgres.NewControlPlaneFromClient(di.Container.Postgres)` | MongoDB, Temporal, MinIO |
| `run stages` | Boot PG como arriba → `InspectService` con `stages` + `participations` cableados, resto nil (la implementación T4 ya falla cerrado con dependencia nil → `INFRASTRUCTURE_FAILURE`) | MongoDB, Temporal, MinIO |
| `strategy get` | Boot PG como arriba → `InspectService` con `identities`, `manifests`, `magic`, `participations`, `provenance`; `flowRuns`/`stages`/`campaigns` nil | MongoDB, Temporal, MinIO |
| `run get` | Boot PG + `sharedmongo.New(di.Container.Etcd, di.Container.Telemetry)` → `forge.NewService(control, metadatamongo.NewRankingSnapshotStore(mongo, db), control)` (el store Mongo implementa el port read `GlobalRankingSnapshotQuery`; primer caller productivo de `forge.Service`) | Temporal, MinIO |
| `push-output` | Comportamiento actual intacto: su `di.InitSelective` interno (etcd, telemetry Document, MinIO) dentro de `runPushOutput`, flags/salida/códigos byte-idénticos | — |

- **Único delta conductual documentado de push-output:** hoy una falla del boot pre-dispatch (`Init()` completo con etcd caído) aborta con exit 1 antes de parsear argumentos; con dispatch-first ese boot desaparece y la falla de etcd ocurre en el boot propio del subcomando → exit `10` `config_error`, consistente con la tabla frozen de exit codes. La ruta de éxito (bytes stdout, flags, exit codes 2/20/30/50) no cambia; BWC test la cubre.
- El wiring reusa exactamente el patrón frozen `sqx/cmd/sqx-worker/persistence.go` (`sharedmongo.New(di.Container.Etcd, di.Container.Telemetry)`, `registrypostgres.NewControlPlaneFromClient`); `internal/di` intocado. Diseñar un framework de DI nuevo o inicializar servicios que el subcomando no usa = violación de contrato.

## BWC y preservación

- F-01 identity, F-02 Finalist V2 + result v1/v2, F-03 long-running, F-04 magic/seal/handoff, S0, B1A/B1B/B2: **no-touch semántico**; la superficie sólo los lee.
- `forge.Service`, `LoadForgeCampaignResult`, models `ForgeResult`/`ForgeCampaignResult`: sin cambios de shape; nuevos consumers solamente.
- `sqx-flowkit push-output`: flags, salida y exit codes byte-idénticos.
- Deploy pipeline (`deploy_release.sh`, `deployer/`, `deploy/manifest.json`): intocado; además `deploy/` no recibe archivos nuevos de F-05-I (la release matrix vive en `sqx/core/releasematrix/`; ver §Release matrix contract C1.1).
- Historia V1: legible; nada se reescribe.
- `DATABASE MIGRATION: NONE`. Si la implementación cree necesitar schema: `STOP — MANAGER REVIEW — FROZEN_CONTRACT_COLLISION`.

## Fixtures

- Permitidas: harness `postgrestest` (+ `testdata/brownfield.sql`), fixtures determinísticas existentes, nuevas fixtures de read-surface etiquetadas sintéticas (convención: campo `"synthetic": true` o nombre `*_synthetic_*` en testdata).
- **`fixture != authentic physical golden`:** ninguna fixture satisface gates CERT; los states físicos de la matriz quedan OPEN/DEFERRED.

## Certificación

- **SOURCE/CONTRACT (F-05-I PASS):** matriz de tests del proyecto ([[Echo Forge — F-05-I Cohesive release and read surfaces]]) verde en scope enfocado; BWC push-output; determinismo JSON; negative tests; cero diffs en contratos frozen; `git diff --check`.
- **DEFERRED CERTIFICATION (no bloquea F-05-I):** T2.11/T2.12/T2.13, E-04 T21/AC-37, físico Windows/MT5, FULL golden, release/deploy ⇒ campaña [[Echo + Echo Forge — Deferred Certification Backlog]] (CERT-F05-01…03 tras CERT-F04-*).

## Handoff que F-05-I deja a F-05-C

1. `sqx/core/releasematrix/release-matrix.json` validado (estados por capacidad con evidencia y autoridad; campos físicos OPEN/DEFERRED salvo historia certifiable; `deploy/` sin archivos nuevos).
2. `docs/echo-forge/f05-read-surface.md`: contrato de read surface (esquemas JSON, comandos, error/empty semantics) — base para el front futuro sin acceso directo a DB.
3. `docs/echo-forge/f05-conformance-checklist.md`: checklist de conformance para la campaña (qué verificar por superficie, con refs).
4. `docs/echo-forge/f05-certification-manifest-template.json`: template del manifest de certificación con campos físicos explícitamente vacíos (`null` + `"status": "OPEN"`); F-05-C los llena con evidencia real, F-05-I no inventa valores.

## Invariantes / STOP

STOP — MANAGER REVIEW si: se requiere modificar F-01…F-04/S0/B1A/B1B/B2 o cualquier schema DB (migration ≠ NONE); se quiere publicar release o tocar el pipeline deploy; se exige HTTP server/auth; la baseline `b57bfb2` desaparece o `origin/feature/f04-magic-version-handoff` avanza materialmente (`BASELINE_MOVED`); un test verde depende de mocks presentados como evidencia física; el funnel necesita hardcodear stages; alguna read surface escribe; T5 necesita tocar `internal/di` o bootear servicios no listados en el grafo mínimo (§C1.6); T1 necesita un cuarto estado distinto de DONE/OPEN/DEFERRED/NOT_APPLICABLE o una séptima dimensión (presentar la contradicción concreta; hoy ninguna fila la exige); algún contenido de la matriz exigiera declarar física DONE fuera de la allowlist histórica para ser coherente (`FROZEN_CONTRACT_COLLISION` con el backlog).

`GOD REQUIRED: NONE`.

## Evidencia y provenance

- Inspección read-only `xKoRx/symphony@b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43` (2026-09-13) y `xKoRx/symphony@3da8b470239a15f62d87f16559feada409e2d611` (2026-09-16, Planning C1).
- Read models sin callers: `sqx/core/forge/result.go` (`forge.Service`, taxonomía INVALID_ARGUMENT/NOT_FOUND/AMBIGUOUS_RESULT/CONTRACT_INCONSISTENCY/INFRASTRUCTURE_FAILURE; `NOT_MATERIALIZED` zero-supply), `sqx/core/forge/campaign_result.go` (`VerifyForgeCampaignResult`, estados PENDING/RUNNING/COMPLETED/FAILED/CANCELLED), `sqx/adapters/registry-postgres/forge_campaign_result.go`, `flow_run_result.go` (`FlowRunResultReader`), `stage_execution.go` (`LoadStageExecution*`), `decision_store.go` (`LoadDecision`, `LoadFinalistPromotion`), `strategy_version.go` (`LoadStrategyVersion`, `LoadHandoffManifest`, `LoadHandoffDelivery`), `magic_allocation.go` (`LoadMagicAllocation`), `strategy_manifest_identity.go` (fila durable instrument/direction/timeframe).
- Ports existentes: `sqx/core/capabilities/forge_result_query.go` (`FlowRunResultReader`, `FinalistPromotionResultReader`, `GlobalRankingSnapshotQuery`); Mongo impl `sqx/adapters/metadata-mongo/ranking_snapshot_query.go`; `LoadEvaluation` en `capabilities/persistence.go`.
- Cero HTTP/GraphQL/Hasura en `sqx/` (`git grep` baseline). CLI actual: `sqx/cmd/sqx-flowkit/main.go` sólo `push-output`. Tools informales: `sqx/tools/{inspect_selected_runs,list_minio,query_mongo,find_minio_keys,inspect_etcd,insert_metadata}.go`.
- Authorities: PostgreSQL `sqx` schema (flow_runs, flow_run_strategies, stage_executions+results, decisions+evidence, strategies, stage_producer_outputs, output_namespace_ownership, forge_campaigns/waves/finalists/stop_evaluations, strategy_magic, strategy_versions, handoff_manifests, handoff_deliveries, magic_instruments, magic_monthly_counters; migrations 001–016); MongoDB db `forge` (databank_metadata, wfm_matrices, strategy_state, type_rankings, wave_reports, mt5_backtest_results, export_runs, deviation_results, ranking snapshots); MinIO `sqx-strategies` + buckets deploy; Temporal correlation columns en flow_runs/stage_executions/forge_campaigns; etcd coordinación.
- Wiring sin `internal/di` changes: patrón `sharedmongo.New(di.Container.Etcd, di.Container.Telemetry)` + `registrypostgres.NewControlPlaneFromClient(deps.PostgresClient)` de `sqx/cmd/sqx-worker/persistence.go`; flowkit ya invoca `di.InitSelective` con Postgres/etcd/telemetry.
- Estados/semánticas existentes reutilizadas sin invención: LifecycleStatus (domain/control_plane.go), ranking/promotion statuses (domain/forge_result.go), ScoreStatus NOT_COMPARABLE/INVALID_INPUT, warnings PERIOD_MISMATCH/FIDELITY_NOT_COMPARABLE/PNL_SIGN_FLIP, STRUCTURAL_EMPTY/TOP_PROJECTION_EMPTY, failure/cancel reason enums (migration 011).
- Release surfaces existentes: `deploy/manifest.json`, `deploy_release.sh`, `deployer/cmd/release-authority` (`sqx-release-authority.v1`), `deployer-watcher`, stager.
- Planning C1 (2026-09-16): watcher deploy — `deployer/cmd/deployer-watcher/main.go` (WatchRoot default `./deploy`, etcd `config/watch_root`), `deployer/adapters/source-fsnotify/source.go` (snapshot recursivo `filepath.WalkDir`), `deployer/adapters/pathing-staticlayout/pathing.go` (`ComputeKey` exige `<root>/<semver>/<platform>/<file>` o manifest raíz), `deployer/core/planner/simple.go` (skip `ok=false`; inmutabilidad por key), `deployer/watcher/watcher.go` (cada cambio bajo el root dispara `Plan` sobre el snapshot completo); `deploy_release.sh` (staging `deploy/<version>/linux-amd64/`, espera manifest en MinIO). CLI/DI — `sqx/cmd/sqx-flowkit/main.go` (boot `Init()` completo pre-dispatch + segundo `InitSelective` en `runPushOutput`; constants exit 0/2/10/20/30/40/50; sólo `push-output`), `internal/di/container.go` (`InitSelective` sin guard de idempotencia; etcd se bootstraps si cualquier dependencia lo requiere; `Container.Postgres`), `sqx/cmd/sqx-worker/persistence.go` (patrón frozen `sharedmongo.New(etcd, telemetry)` + `NewControlPlaneFromClient`), `sqx/core/forge/result.go` (`forge.Service.Result(ctx, rawRef, rankingSelector)`, taxonomía ErrorKind), `sqx/core/forge/inspect.go` (`NewInspectService` acepta dependencias nil y falla cerrado), `sqx/adapters/metadata-mongo/ranking_snapshot_query.go` (`RankingSnapshotStore` implementa `GlobalRankingSnapshotQuery`), `sqx/adapters/registry-postgres/control_plane.go` (`NewControlPlaneFromClient`), idiomas `go:embed` existentes (`migrations/runner.go`, `postgrestest/db.go`). Historia de certificación: [[Echo Forge — Factory V2 Completion]] (F-01 `0509342`/F-02 `c3b7ede`/F-03 `382f4ba` CLOSED con verdictos; F-03 PHYSICAL PASS job real; B1A `185825c`/B1B `ef65dd1`/B2 `db8a022` PASS/CLOSED; rollout F-04: linux PASS vía `stager-runtime.service`, windows bloqueado por viewer policy, rollout global INCONCLUSIVE) y [[Echo + Echo Forge — Deferred Certification Backlog]] (taxonomía RELEASED/DEPLOYED/PHYSICALLY CERTIFIED/CROSS-LANE/CLOSED; CERT-F04-01/02/03, CERT-E04-01, CERT-F05-01/02/03).

## Límites y contradicciones

- `campaign list`/pagination es presentación: si el owner quiere "la campaña actual", eso sigue siendo decisión humana sobre refs exactos; la superficie no resuelve identidad por recencia.
- La matriz declara estados; no los ejecuta ni los audita automáticamente. Su verdad es la evidencia referenciada.
- El funnel no afirma "supervivencia entre boundaries" como dato durable; expone counts por boundary. Las transiciones son lectura del consumidor (presentation ≠ authority).
- La superficie Mongo de ranking es la ya usada por `forge.Service`; databank/wfm/deviation quedan fuera y su exposición sería un cambio de scope aparte.
