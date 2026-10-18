---
type: agent_run
schema_version: 1
scope: session
created: "2026-10-18"
updated: "2026-10-18"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge — Operación Real V2]]"
related:
  - "[[2026-10-18-zcode-glm53-forge-030-release-e2e]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM 5.3 Flash (account:zai-individual-coding-plan/GLM-5.3-Flash)
model_source: system
task_type: performance_diagnosis
task_complexity: high
outcome: success_expected_behavior_confirmed
verification: production_evidence
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

# Agent Run — 2026-10-18-zcode-glm53-sqx144-cpu-utilization

## Trabajo

- **Objetivo:** mandato GPT-6 one-shot — diagnosticar y corregir (si hubiera causa demostrada) la subutilización de CPU de SQX 144 en Zeus/Hera/Kronos, con evidencia física, sin repetir el E2E 0.3.1 ni tocar producción, y dictamen independiente del incidente Hera 05:05:43Z.
- **Alcance atribuible:** diagnóstico read-only 3/3 hosts (lscpu/nproc/cgroups/cpuset/steal, unidad systemd + drop-in, settings.xml y .config de 142 y 144, logs launcher/StrategyQuant de hoy y del 14-oct, logs worker del E2E w10 completo, sar/sysstat de la ventana del builder, `last -x`/auth del reboot, ETCD maintenance/control), forense del incidente Hera, reconstrucción del contrato de lanzamiento JVM desde source (`sqx_executor.go`, `process_nonwindows.go`, `postProcessCFX` en steps.go sobre baseline 492a271e clonado limpio) y 7 entregables de evidencia en el vault.

## Evidencia

- **Veredicto `SQX144_CPU_EXPECTED_BEHAVIOR`**: sin restricción accidental (sin cpu.max/cpuset/throttle/nice/affinity; JVM ve 28/64/76 cores; %steal ~0; RSS ~12 GB). Builder w10 Kronos 69,2 min = genético 126 s (76 executors preparados) + **CustomAnalysis Forge secuencial ~60 min a ~1,05 core** + sync 145 s; retests 17–30 s c/u con ~10–15 s de boot fijo, seriales por host, paralelos entre hosts.
- **Config owner demostrada en CLI**: settings.xml 3/3 `coreUsage=100%`+`highPriority=true`; correlaciones en vivo log↔archivo ('−1'→27/63/75, '100%'→60/76; "High priority: ON" Hera 03:21 local). GUI y CLI comparten el mismo archivo; cada run sqcli es JVM nueva.
- **Incidente Hera**: reboot iniciado por owner (SSH kor@.162 05:05 local; quiesce ETCD+file 05:05:43Z; LINUX RESTART 05:07:08Z en sysstat; /var/crash vacío); retry 05:09:25Z fast-fail 2,1 s ("Project stopped" como error marker); retry en Kronos 05:11:27Z completó 4154640 ms. `maintenance/control` hoy `{}` (sin quiesce residual).
- Entregables: `10-projects/Echo Forge — Operación Real V2/artifacts/SQX144-CPU-UTILIZATION-20261018/` (CPU-ROOT-CAUSE, HOST-RESOURCE-MATRIX.csv, JVM-LAUNCH-CONTRACT, GUI-VS-HEADLESS, SQX-142-VS-144, STAGE-PROFILING.csv, HERA-LIFECYCLE-INCIDENT, REMEDIATION-PLAN; BENCHMARK no aplica, justificado).

## Desviación y rework

- Ninguna mutación de flota, repo ni configuración (mandato read-first; no existió causa que corregir). BENCHMARK-BEFORE-AFTER omitido por cláusula "si aplica": no hay candidato de configuración; cualquier candidato real exige cambiar el snippet Forge (fuera de alcance). Sin rework del owner.

## Lecciones operativas

1. **El "Builder" de Forge es un proyecto de 2 tareas**: la genética es corta y paralela; el tiempo lo domina la CustomAnalysis inyectada (overview producer) que itera estrategias en secuencia a ~1 core. Cualquier optimización de throughput de builder pasa por ahí, no por configuración de flota.
2. **`JAVA_TOOL_OPTIONS` del drop-in systemd es parte del contrato JVM de sqcli**: heredado íntegro por el env, pisado por `sqcli.config` en los duplicados (-Xms4g gana a -Xms34g por orden). Verificar heap efectivo con RSS, no con la unidad.
3. **Los logs SQX por host prueban config sin abrir la GUI**: la línea "Using: N cores, core usage configuration: 'X'" + "High priority: ON/OFF" correlaciona 1:1 con settings.xml — método replicable de verificación GUI/CLI.
4. sysstat (sar) retenido en los 3 hosts fue la evidencia decisiva de CPU histórica; Prometheus no cubre la flota (sólo se scrapea a sí mismo) — considerar node_exporter si se quiere monitorizar uso por fase.
