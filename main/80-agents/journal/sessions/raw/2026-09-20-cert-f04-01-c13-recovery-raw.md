---
type: raw-session
schema_version: 1
created: "2026-09-20"
updated: "2026-09-20"
area: "[[Echo]]"
project: "[[Echo Forge]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo + Echo Forge — Deferred Certification Backlog]]"
related:
  - "[[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash (zai-individual-coding-plan/GLM-5.3-Flash)
load_policy: manual
indexable: false
index_priority: never
source_session:
tags:
  - kind/raw-session
  - scope/session
---

# Raw Session — 2026-09-20 cert-f04-01-c13-recovery

Mandato MAESTRO F05C-CERT-F04-01-C13: publicar fix aprobado `25a5122` (defecto #6), recuperar RERUN-6 sin reiniciarla y completar CERT-F04-01. Bootstrap Agents OS ejecutado (cold start, entidad Echo Forge, router aranea).

G0: thist gRPC fresco — ambos workflows Running (campaign `sqx-forge-campaign-v1-4cdf96fc…`/run `01a0bce5-0b8e…`, main `sqx-main-v1-6fd4912a…`/run `01a0bce5-0cee…`), únicos en sqx-prop; `forge_seal_handoff_v1` pending Scheduled attempt 16 (retry unlimited 1m/2.0/30m; sched_to_close 0, start_to_close 100y), last_failure = firma defecto #6 sobre `7508a66c…`; MinIO effective-inputs sólo de `7508a66c` (08:22:29Z) → loop fail-fast, miembros 2–5 estado A; ETCD echo 0 keys; MT5_PROCS=0 (Windows sólo sqx-mt5-worker 3828); Kronos sin screens/watcher; Mongo apply evals de los 5 miembros con magias exactas 013/014/016/017/018 y refs == request ev640.

G1: ensayo realista en worktree `seal-fix` (arnés temporal `g1_rerun6_recovery_test.go`, env-gated SQX_G1_RERUN6, ELIMINADO sin residuo). 20 artefactos (SQX/MQ5/EX5/log ×5) por presign GET + curl, SHA256 == refs durables de 10 evaluaciones Mongo (`_id` exactos). Fase 0 reprodujo 0.2.103 (ingress legado sin sentinela): fail-fast miembro 1, 1 versión + 1 manifest + fila UNAVAILABLE, y **effective-inputs regenerado byte-idéntico al objeto real `33937102…`** (ancla de determinismo). Fase 1 (FailClosedIngress real `NewFailClosedIngress("echo ingest base url / bearer not configured")` envuelto en observador): 5/5 HANDOFF_CREATED ingested=false, UNAVAILABLE→CREATED con last_error registrado, 5 Deliver todas rechazadas, 5/5/5 sin duplicación, VersionRef/IdempotencyKey originales del miembro preexistente. Fase 2 replay convergente (10 calls, 0 POST). Fase 3 same-key/different-payload → CONTRACT_CONFLICT preservando fila y digest. Suites: seal 20/20, magic-readback (fixture `9ac377b9…`), echo-handoff, core PASS; gate 6182 obligatorio PASS coverage 99.1% (`21917e14…` en `~/aranea/work/f04-cert-f04-01-c6/artifact/`); `mt5-export.htm` restaurado byte-exacto desde `b5c71d5` (`090ca4d1…`); baseline gemelo `2993da0`: 21 fallos workflows idénticos por nombre (sólo timing), worker 0; gofmt/vet limpios en archivos del fix; anti-masking aditivo 44+/1−.

G2: FF `--ff-only 25a5122` en checkout principal (`~/go/src/github.com/xKoRx/symphony`), push + read-back origin == 25a5122; authority preflight CONSISTENT candidate 0.2.104 (en vivo); `deploy_release.sh --release-only ""` + deployer screen (vivo desde 17/09); MinIO confirmó manifest 0.2.104; authority post-publish CONSISTENT (candidate 0.2.105); 6/6 SHA256 == manifest (symphony `a81aa5a1…`, watcher `c4417993…`, start-sh `9f956384…`, run-symphony `8f240eb2…`, promtail `eaa4e1b2…`, exe `c250d7dd…`); `vcs.revision=25a5122` ambos binarios (vcs.modified=true por dirty operacional no-Go, igual que 0.2.103); históricas 0.2.99–0.2.103 intactas; cero FlowRuns nuevos.

G3: rollout Stager automático 4/4: Zeus PID 2839157 (14:08:48Z), Hera 1421854 (14:10:30Z), Kronos 1383514→1383513 (14:09:57Z), Windows 40192 (14:09:02Z) — SHA==manifest ×4 (Windows exe_sha256 EXACT 37249024 B, evidence SYSTEM 14:13:06Z partial=false errors=[], padre stager-runtime Running/Automatic, poller ESTAB, singleton); pollers Temporal frescos con PIDs nuevos 14:14–14:15Z; MT5_PROCS=0. Compatibilidad demostrada: diff no toca `sqx/workflows/**`, actividad sin cambio de firma, worker model plano sin versioning, único cambio semántico = clasificación del terminal de entrega.

G4: attempt 16 disparó 13:53:32Z en worker viejo (fallo benigno esperado); **attempt 17 a 14:23:32Z atendido por workers 0.2.104 → main workflow Completed en segundos**. Payload físico del seal: 5/5 HANDOFF_CREATED ingested=false — `7508a66c`→`6d3cab1a…`/`718c4aeda…`, `960d39f8`→`04ab1176…`/`9f79226c…`, `9a7e5cbb`→`d41f3468…`/`2f76cc56…`, `ce307453`→`491c2094…`/`2686db6e…`, `ddef83aa`→`eefefdbd…`/`b8451d84…`; campaña `f50e5cdb…` `{"status":"COMPLETED","stop_reason":"TARGET_REACHED","effective_unique_finalists":5,"waves_started":1,"waves_completed":1}`; Running=0; MinIO con exactamente 5 effective-inputs (el de 7508a66c byte-inmutable, etag intacto); ETCD echo 0 keys fresco; 0 backtests adicionales.

G5: lectura literal SPEC (backlog + F-04): 4 criterios PASS satisfechos — SHA homogéneo 4/4 por instante (productoras `2993da0`, seal/delivery `25a5122`, atribución por etapa), flujo completo sin bypass (HANDOFF_CREATED ×5 = terminal F-04 §11 con Echo sin configurar; INGESTED → CERT-E04-01/F04-03), evidencia verificable, cardinality-safe; criterio "release cohesiva" pertenece a CERT-F05-01; retry post-UNAVAILABLE autorizado por failure matrix + convergencia write-once content-addressed. `CERT_F04_01_PASS`. G6: MT5_PROCS=0 fresco, 0 Running inesperados, allocations 001–018 intactas, write-once íntegro. G7: RERUN-7 NOT_REQUIRED (cero campañas nuevas). Limpieza: worktree baseline eliminado, arnés eliminado.

G8: backlog delta C13 (estado de entrada + delta completo + próxima tarea única → CERT-F04-02), bitácora Echo Forge, agent-run, change_log, feedback, L0/L1.
