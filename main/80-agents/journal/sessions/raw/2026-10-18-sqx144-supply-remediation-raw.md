---
type: raw_session
schema_version: 1
scope: session
created: "2026-10-18"
updated: "2026-10-18"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
application:
entities:
  - "[[Echo Forge — Operación Real V2]]"
related:
  - "[[aranea-agent-dev]]"
  - "[[Echo + Echo Forge — Environment Contract]]"
aliases: []
confidence: verified
source_session: sess_e3fecb7d-c091-4204-b558-ffd8511317b3 (ZCode)
load_policy: never
indexable: false
index_priority: never
tags:
  - kind/raw-session
  - scope/session
---

# 2026-10-18-sqx144-supply-remediation-raw

> [!warning]+ Raw session L0
> Archivo de auditoría y retrofit. Excluido del retrieval normal y de Graphify.

## Contexto

- Agente: ZCode / account:zai-individual-coding-plan/GLM-5.3-Flash, LOCAL TOP, ONE-SHOT. Manager: GPT-6 (Primary).
- Proyecto o entidad: [[Echo Forge — Operación Real V2]] — SQX144 supply remediation (sucesor del defecto certificado en SQX144-MULTICORE-EXECUTION-P0).
- Objetivo: resolver SOLO el defecto de suministro (batch_size:1 + source secuencial) sin repetir benchmarks; reconstruir contratos, proponer UNA corrección mínima o demostrar que la granularidad se mantiene. Invariantes: 1 root FlowRun, groups internos, 1 sqcli/host, optimizer exactly-one-upstream, Final Reretester y SelectionSnapshot intactos, sin cambios a CFX/Strategy/MM/ranking. Sin cambios productivos ni campañas.

## Transcript

```
[Bootstrap] Cold start: constitución + perfil rjara + continuidad global + INDEX skills + domain registry. Entidad Echo Forge (area [[Echo]]) → router aranea → MUST READ Echo+Forge Environment Contract (§0: Forge = ambiente operacional único; esta sesión = forense local, sin mutación infra).

[Workspace] Clone fresco xKoRx/symphony @ origin/master 492a271 (0.3.1) en ~/aranea/work/sqx144-supply-remediation-20261018/symphony; clon perf/overview-s02 @ f4755c3 usado de apoyo. P0 artifacts NO encontrados ni en vault (10-projects/Echo Forge) ni en master git — reconstrucción del estado P0 desde memoria durable (PASS_WITH_SUPPLY_DEFECT + mediciones Kronos).

[Forense contratos — archivos clave]
- generic_workflow.go:165 runGenericSQXWorkflow; :343 case group → handleGroupTask; :1527 ranking_snapshot → handleEarlyRankingSnapshotGroupTask (particiones en paralelo vía workflow.Go, chunks secuenciales dentro de partición); :1626-1648 chunking por BatchSize (default <=0 = partición completa); :1790-1800 groupParallelChildrenEnabled = GetVersion + max_parallel>1 + source==nil (groups con source fail-closed a secuencial); :1754 runRetesterSnapshotsForGroupOutput (snapshot del producer una vez por group, grano cohort); :2203-2380 runFinalReretesterFanout (precedente fan-out/fan-in per-arteacto, mismo taskPath, subjects distintos); :2384 GroupSQXWorkflow (child).
- config.go:400-419 IsDurable{Builder,Retester,FinalReretester,Optimizer}Task = type=project + stage=X.
- steps.go:344 prepareDurableRetesterInput — "N upstreams are the batch contract: one physical SQX run retests the whole upstream databank"; :433 prepareDurableOptimizerInput + :2855 exactOptimizerUpstream — len!=1 ⇒ "sqx-optimizer.v1 requires exactly one upstream strategy" (3 capas fail-closed con binding/subject.go:46-62,102-108).
- retester binding: subject.go:100-112 (N upstreams OK; subject = primer upstream del batch en orden de rango); persist.go:63-146 (evidence per-estrategia bajo 1 StageExecution del batch); steps.go:2715-2824 (binding output→upstream por canonical ID + fallback carrier; batch parcial = evento visible sqx_retester_batch_partial).
- wfm_durable.go:19-80 y durable_select_workflow.go:16-120 — fan-out PER-ARTEFACTO interno; toleran N carriers.
- early_ranking_group_activity.go:46-134 — route desde snapshots per-logical-type durables; unicidad StrategyRef/EvaluationRef entre particiones; la decisión de selección vive en el snapshot durable, el group sólo enruta.
- sqx-worker main.go:476 MaxConcurrentActivityExecutionSize:1 hard-coded (+ test) = invariante 1 sqcli/host materializado.
- Spec real w10 (~/aranea/work/forge-030-e2e-20261018/spec/config-w10.json): group e2e-group batch_size:1, max_parallel:3 (inerte), subtasks [retester, optimizer, evaluate_wfm, evaluate_strategy, select_robust_run]; apply_selected_run y final_reretester en root.

[Demostración del problema] Subir batch_size del group (recomendación P0 60-150) entrega N>1 al subtask optimizer ⇒ prepareDurableOptimizerInput falla cerrado ⇒ FlowRun falla. Objeción del Manager CONFIRMADA en source. Cohort máximo = TopNPerLogicalType(5) × particiones (w10 ≤25) ⇒ 60-150 además innecesario.

[Diseño SUPPLY-REMEDIATION-R1] Retester a grano de partición (usa su contrato N-batch nativo, incluido partial visible); optimizer redistribuido a ejecuciones 1-upstream DENTRO del mismo child/FlowRun vía fan-out/fan-in espejo del Final Reretester, gate replay-safe GetVersion "group-optimizer-fanout-batch". Identidad de StageExecution del optimizer por estrategia = idéntica a la de batch_size:1 (FlowRun+taskPath+subject+inputs+gen 1). Spec: batch_size 1→5 (o eliminar). Snapshot del retester producer se sigue emitiendo una vez por group sobre el merged (mismo grano que hoy). Descartes razonados: Vía 2 max_parallel en groups con source (sin efecto con chunk=partición), subir MaxConcurrent (viola 1 sqcli/host), split en dos groups (cambia grano de snapshot y abre path list_strats en zero-supply — riesgo innecesario).

[CPU esperado vs medido] Medido P0: retest 4,5→36,7 str/s N=10→600, pico 74,1; optimizer 1 estr pico 72,6. Esperado R1 (NO medido): fase retest 25 ejecuciones→5, ~6-15 cores flota vs 1-3; optimizer sin cambio; 30-70× NO alcanzable con cap 5/tipo (cohort ≤25). Medición real = replay E2E w10, campaña aparte.

[Entregable] ~/aranea/work/sqx144-supply-remediation-20261018/DESIGN-SQX144-SUPPLY-REMEDIATION.md (9 secciones + FINAL STATUS json). FINAL STATUS: SUPPLY_REMEDIATION_READY. Sin cambios productivos, sin campañas, cero mutación de flota/ETCD/MinIO/PG.
```

## Evidencia externa

- Repo: xKoRx/symphony @ 492a271 (master, limpio). Líneas citadas en el diseño §1.
- Spec w10: repo workspace forge-030-e2e-20261018/spec/config-w10.json.
- P0: SQX144-MULTICORE-EXECUTION-P0 PASS_WITH_SUPPLY_DEFECT (cierre 2026-10-18, memoria durable; deliverable no localizado en vault ni master — feedback registrado).
