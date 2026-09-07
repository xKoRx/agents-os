---
type: agent_run
schema_version: 1
scope: session
created: "2026-08-27"
updated: "2026-08-27"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3
model_source: builtin:zai-coding-plan/GLM-5.3
task_type: review
task_complexity: high
outcome: success
verification: verified
evaluator: agent
user_rework: unknown
source_session: DURABLE-ARTIFACT-VERIFIED-READS-RCA-TOP
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-run
  - scope/session
---

# Agent Run — 2026-08-27-zcode-glm-5-3-durable-artifact-verified-reads-rca-top

## Trabajo

- **Objetivo:** RCA/DESIGN read-only en `xKoRx/symphony` @ `5e3c2b39a62f1d953035281bb38146551a79dc0d` + `xKoRx/sdk` @ `ea09cc1bb8b34e661c8f31f887dce58613b0475a`: auditar TODOS los read paths del durable Artifact Plane (F1–F41) y congelar el diseño de `ARTIFACT_VERIFIED_READS` sin modificar código.
- **Alcance atribuible a esta combinación superficie×modelo:** delegación paralela a 4 subagentes mm-scout (primitivas storage; carriers de estrategia/resolvers; MT5/apply/payloads; WFM/domain/errors) + verificación parent de los hechos que decidían clasificaciones (robust legacy sin wiring productivo — sólo `sqx/tools/test_apply_selected.go`; `apply_selected_run` del workflow genérico usa el path durable; MT5 artifact durable mode ignora listing; `ExportMT5EAResult` sin digest; `project_activity` mapea `ErrContractConflict`→NonRetryable; AdaptiveSQXWorkflow sin dispatcher en repo) + decisiones/contratos congelados + persistencia Agents OS completa.
- **Artefactos afectados:** ninguno del repo (read-only, foreign dirty preservado); en vault: decisión symphony, checkpoint de proyecto, change_log, agent-run, continuidad.

## Evidencia

- **Validaciones ejecutadas:** HEADs verificados == baselines exactos; tabla de readers con callers/evidencia file:line completa; traza hop-a-hop Mongo doc (size+sha256 persistidos `evidence_documents.go:20-28`) → resolver (ref completo) → carrier (drop en `historical_cohort_activity.go:162`) → `DownloadToCustom(keys)`; confirmación FetchDurable/VerifyArtifactStream/DownloadNDJSON/ReconcileApplySelectedRun verifican; greps directos para despachadores legacy y modos MT5.
- **Resultado observable:** PASS/CLOSED. Payload/TradeSet/WFM-seal/apply/MT5-exporter YA verificados; STRATEGY_SQX (histórico, builder templates, same-flow) y WFM physical input y MT5 portable NO (carrier key-only + descarga sin verificar); primitiva verified-to-file inexistente; diseño congelado (`FetchDurableToPath` temp+rename streaming, `StrategyArtifact.Artifact`, `DownloadDurableToCustom` aditiva, sin schema nuevo, sin SDK, sin centinelas nuevos); slicing S1/S2/S3; NEXT EXACT SLICE1.
- **Limitaciones de la evidencia:** clasificación «AdaptiveSQXWorkflow sin dispatcher» cubre el repo Go (watcher/job_config/workflows) — un starter externo por client SDK no puede excluirse 100% desde código, pero ningún config productivo actual lo referencia; sin E2E ni tests (sesión read-only); línea exacta de funciones puede moverse con el worktree dirty (sólo archivos runtime tocados, no fuentes Go).

## Evaluación

- **Correctness:** 5
- **Autonomy:** 5
- **Efficiency:** 5
- **Tool use:** 5
- **Overall:** 5

## Resultado

- **Outcome:** PASS / CLOSED; NEXT EXACT DURABLE-ARTIFACT-VERIFIED-READS-SLICE1-NORMAL.
- **Rework posterior:** unknown.
- **Aprendizaje para comparar herramientas:** mismo patrón eficiente que el RCA write-once: 4 scouts mm-scout paralelos (~7-8 min total, evidencia file:line completa) + verificación parent selectiva sólo de hechos que invertían clasificación (productivo vs legacy); la verificación de wiring/registration en `cmd/*/main.go` resultó el discriminador clave para no sobreestimar la superficie legacy.
