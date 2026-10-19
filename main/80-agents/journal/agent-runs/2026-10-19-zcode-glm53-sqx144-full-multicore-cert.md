---
type: agent_run
schema_version: 1
scope: session
created: "2026-10-19"
updated: "2026-10-19"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge — Operación Real V2]]"
related:
  - "[[2026-10-18-zcode-glm53-sqx144-multicore-p0]]"
  - "[[2026-10-18-zcode-glm53-sqx144-cpu-utilization]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM 5.3 Flash (account:zai-individual-coding-plan/GLM-5.3-Flash)
model_source: system
task_type: physical_certification_campaign
task_complexity: high
outcome: success
verification: physical_measurement
evaluator: agent
user_rework: none
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-run
  - scope/session
---

# agent-run — SQX144 FULL MULTICORE CERTIFICATION (mandato owner vía GPT-6, ONE-SHOT)

## Encargo

Mandato P0 de certificación física E2E: demostrar o refutar que Builder, Retester y Optimizer de SQX 144 aprovechan múltiples cores en las TRES VMs de la flota (Zeus/Hera/Kronos), con agrupaciones ≥10 estrategias, prueba integrada Builder→Retester→Optimizer con continuidad, medición OS real (core-seconds, threads, fases), 1 instancia SQX por VM, y veredictos separados + global. Sin investigación teórica, sin cambios de producto.

## Ejecución

- Bootstrap + router aranea + contrato de entornos; preflight completo (hosts idle 3/3, sqcli 7d312106 idéntico en 3 hosts, licencia OK en runtime, datos UTC02/darwinex presentes, clon @ 492a271e, workflow ajeno wave3f atascado a nivel workflow-task sin actividades — no interferido).
- Harness candidate-local nuevo `/home/echo-dev/forge-cert-20261018/` en los 3 hosts (instalación productiva intacta): workspace lean (user sin History + symlinks), proyectos fc-build/fc-retest/fc-opt desde fuentes de campaña selladas por SHA, samplers /proc 200 ms (group jiffies, CLK_TCK=100 verificado) + per-tid 1 s + poller de consola 2 s + time -v, guard de singleton con 0 violaciones, driver por etapas con gates resumibles.
- Defectos de harness corregidos en vuelo (documentados): sftp-upload MCP corrompe base64 → staging por HTTP+SHA; cwd relativo del runner tras seed_one (paths absolutos); verificador "Task finished in" vs formatos por tarea; databank Output/Results del builder v5; marcador task_end del analizador sin duración.
- Iteración del builder: v2 (Builder_G1 darwinex→UTC02) = 100% de rechazo (957.570 generadas / 0 aceptadas en ~3 h a plena máquina) → stop inalcanzable → detenida (procesos propios, SIGKILL documentado) y sustituida por v5 = `builder_test.cfx` del repo @ 492a271e (builder de los flujos E2E), que completa con stop funcional "Build finished because databank is full" (20 estrategias, cap MaxStrategies=20 interno).
- Campaña completa 3/3 hosts: smoke → ladder retest N=10/30/90/300/600 (lote físico en 1 sqcli) → grupo optimizer 10×WFO (1 estrategia/SQX, 10 procesos secuenciales) → builder con stop funcional → cadena integrada cohort10 (sello SHA 0 faltantes ×3) → análisis.

## Resultado

`SQX144_FULL_MULTICORE_CERTIFIED` con exclusión de alcance explícita (CustomAnalysis del builder de producción: NOT_APPLICABLE aquí; evidencia previa la muestra secuencial). Genético: picos 68,1/72, 51,7/60, 26,95/27 + maratón v2 ~3 h a ~100% (observación viva). Retester: throughput monotónico 4,7→37,1 / 4,8→42,4 / 11,9→52,8 str/s, picos 73,3/61,5/25,2. Optimizer: 30/30 runs con cálculo multicore (medias calc hasta 94% de la máquina). Integrada: PASS con continuidad SHA en cada salto. `PRODUCT_MUTATIONS: NONE`.

## Evidencia

- Entrega: `10-projects/Echo Forge — Operación Real V2/artifacts/SQX144-FULL-MULTICORE-CERTIFICATION/` (9 archivos: EXECUTIVE-VERDICT, BUILDER/RETESTER/OPTIMIZER-CPU-PROOF, INTEGRATED-RUN, HOST-CPU-MATRIX.csv, THREAD-UTILIZATION.csv, WORKLOAD-PROVENANCE, ACCEPTANCE).
- Crudo por host: `/home/echo-dev/forge-cert-20261018/{rec,analysis,state,logs}` (zeus/hera/kronos).

## Rework / pendientes

- Cero cambios a repo/ETCD/PG/MinIO/flota/release; wave3f intacta; servidores HTTP de staging apagados.
- Pendiente owner/Manager: decidir certificación futura de la fase CustomAnalysis (requiere un CFX real con CA habilitada preservado); integración S01/S02 del exporter (fuera de mandato).
