---
type: session
schema_version: 1
scope: session
created: "2026-10-30"
updated: "2026-10-30"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
application:
entities: []
related: []
aliases: []
confidence: high
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

%% Filename: YYYY-MM-DD[-HHMM]-<human-topic>-summary.md. Never use UUIDs/hashes as visible names; put external IDs in source_session. %%

# Echo Forge 12X — release preflight y continuidad

> [!info]+ Session summary L1
> Resumen operativo. Para beta queda fuera del corpus normal de Graphify.

## Objetivo

- Ejecutar la release corregida de Echo Forge y lanzar 12X replicando la configuración efectiva de 12W, con Top 5, lotes de 4 y `max_parallel=50`; mantener Hefesto fuera del Builder y reincorporarlo sólo tras publicar outputs durables del Builder.

## Contexto cargado

- Agents-OS y rutas vigentes de Echo Forge, Aranea/SSH, Temporal, MinIO, release/Stager, dispatch, proyecto y cierre de sesión.
- Proyecto: [[Echo Forge — Operación Real V2]]. Source candidato Symphony `7be374689bbfeb9cbe0aa461ec92cc4aa7aa5aef`; SHA de código del manifest `08cec708921fd77d696c54566f3ad4360965b720`.
- Evidencia operacional cruda privada en `/tmp/echo-forge-12x-20261029/`; el worktree de Symphony quedó limpio, sin fixes ni commits nuevos.

## Trabajo realizado

- 12W `FlowRunRef=47540370-220e-4301-9a52-3bde26658b99`, `WorkflowID=sqx-main-v1-f0e572b7-d4c3-4e1d-a2b4-2f1548166651`, namespace `sqx-prop`. El spec de Temporal coincide con `sqx.configs.config_json`; PG indica `RUNNING`, pero Temporal lo reporta `TERMINATED` por usuario vía frontend el 2026-10-29 23:25:53 UTC. No se detuvo en esta sesión.
- 12X no está consumida: sin fila/config en PG ni objetos en sus prefijos MinIO. Spec preparado desde el request efectivo de Temporal, no desde la forma raw de MinIO. SHA256 spec 12W `86cded6bc90564fe4c40b5ad2e8874a441a76e6ee5f4d8a2943a973a4e17919c`; spec 12X `236e5f67925624d58eacd91333db68517d0d32897e7f76f97bcf22e1553cf197`; diff `085545bf3b2a88088c6890be8750267d40138ec6f46cc12c611eb831d843d540`.
- Diff estructural: cuatro campos únicamente — identidad `request_id`, `wave=12X`, `batch_size=4`, `max_parallel=50`. `top_n=5` ya estaba en 12W. Conservados tasks/subtasks, Builder, filtros, datos, fechas, CFX y ranking `weighted_combination_minmax.v1` desde `group-retester`, con elegibilidad `profit_factor metric_status_observed` y comparabilidad `same_window`. El Builder mantiene `PopulationSize=20`, `MaxGenerations=100`, `MaxStrategies=120`. No hay task Echo en 12W; 12X no certifica integración Echo.
- Parser estricto, validación profunda y chequeo de `max_parallel` preservado del candidato: `valid=true`; 4 tasks top-level; e2e-group batch=4/K=50/top=5. Es validación de config, no física.
- **Gate productivo bloqueante confirmado en source:**
  - `12e1620304b1fdee0fea00d1907fe64796c51295` cambia 32 marcadores `NonRetryable` en 17 archivos a reintentables y `MaximumAttempts=1→0` en `forge-campaign`/`mt5-artifact`. Actual: errores contractuales/permanentes pueden reintentarse indefinidamente. Esperado: errores permanentes terminan; sólo fallos técnicos justificados reintentan. Archivos afectados: `sqx/activities/worker/{classification_snapshot_activity.go,classify_and_rank.go,early_ranking_activity.go,evaluate_strategy.go,evaluate_strategy_retry_test.go,forge_seal_handoff.go,mt5_artifact_activities.go,mt5_compile_persist_activity.go,mt5_exporter_durable.go,mt5_ownership.go,mt5_reconcile_activity.go,mt5_score_shadow_activity.go,rank_snapshot_activity.go,selection_snapshot_activity.go,trade_list_exporter_activity.go,verify_metadata.go,wfm_durable_export_activity.go}` y `sqx/workflows/{forge_campaign_workflow.go,mt5_artifact_workflow.go,mt5_artifact_workflow_test.go}`.
  - `2d971e7627add77d4219f0d38ee8272fbc663887` cambia `sqx/cmd/sqx-worker/main.go` para reactivar un loop que aplica machine-id/licencia a instalaciones SQX ≥136. Contradice la prohibición del owner. En Hefesto sólo se observó error de `sudo` interactivo requerido; no hay evidencia de modificación de machine-id/licencia.
  - Corrección acotada para la siguiente integración revisada: restaurar clasificación terminal para errores permanentes y límites finitos donde corresponda, preservando heartbeat/retry técnico; retirar el loop automático de machine-id/licencia y mantener mantenimiento fuera del worker bajo autorización expresa. No se aplicó cambio: Symphony exige scope SDD/Allowed Files e integración revisada.
- Flota al muestreo: los cuatro `stager-runtime.service` ejecutan `/opt/stager/releases/0.4.7/bin/symphony`; SHA efectivo `5c5e8d9c75ba5b11855be189c01582c9ec449ceae113375738cefafadd083dc` en Zeus/Hera/Kronos/Hefesto. Los cuatro tienen hashes idénticos del template SQX `6b3ba4a7df7ef749575881ceda3e9118f475b389fbbfc920fc9bfad5203f0e89` y `EchoForgeAutomator.jar` `933cd2044fa4fc48d56eb72d757a60263693304d45d4995c5df98833d8fc9d3f`.
- Cadena de servicio: unidad `stager-runtime.service`, usuario/grupo `kor`, `WorkingDirectory=/var/lib/symphony`, wrapper `/usr/local/lib/stager/stager-runtime`, proceso Symphony versionado. El worker usa directamente el `sqcli` de la instalación SQX activa; `/home/kor/sqx/run_sqcli.sh` apunta a `142/run_sqcli.sh`, pero el servicio no lo ejecuta. Esa ruta y `144/run_sqcli.sh` están en modo 777; no se atribuye el reporte histórico de permisos a estos workers y no se cambió ningún modo.
- Cgroups del servicio: CPU `max`, memoria `max`; CPU allowed Zeus 0–25, Hera 0–57, Kronos 0–53, Hefesto 0–11. RAM disponible al muestreo: Zeus 64.3 GB, Hera 96.5 GB, Kronos 125.0 GB, Hefesto 5.6 GB. En Zeus se observó un `sqcli` físico ILT_CONT a ~368% CPU y 160 threads; esto demuestra uso multinúcleo en esa muestra, no certifica todas las etapas/hosts. No se ajustó cuota, afinidad, heap ni threads.
- Hefesto: servicio activo y nunca detenido; release 0.4.7. Zeus conserva un worker manual con poller `sqx-ilt-main-queue` y actividad física ILT_CONT; no se canceló ni interrumpió. Los cuatro pollers de `sqx-main-queue` aún son binarios viejos; no pueden recibir 12X. Perfil MT5 Windows desconectado y consumidores downstream no revalidados porque el gate cerró antes del rollout.
- Resultado: no se eligió número de release, no se empaquetó/publicó/deployó, no se puso input en watcher, no se detuvo Hefesto y no se despachó 12X. No hay WorkflowID/RunID/FlowRunRef de 12X. No se creó vigilancia de fondo.

## Artifacts creados o modificados

- Actualizado [[Echo Forge — Operación Real V2]] con checkpoint y siguiente paso.
- Nuevas notas: [[2026-10-30-echo-forge-12x-entity-updated]], [[2026-10-30-echo-forge-12x-release-preflight-session-feedback]] y [[2026-10-30-codex-unknown-echo-forge-12x-release-review]].
- Preflight privado local: `/tmp/echo-forge-12x-20261029/` (12W request/spec/CFX, diff y SHA256). No copiar payloads a memoria pública.
- Symphony candidate tree sin cambios; no nueva release, modificación de worker, commit de producto ni dispatch.

## Memoria propuesta o creada

- Continuidad actualizada directamente en el proyecto; no se creó un known-error público ni se modificó source fuera de un SDD revisado.
- Feedback de Sistema 1 por routing Temporal con namespace MCP obsoleto y truncamiento inicial de salida demasiado amplia.

## Decisiones

- Bloquear release y dispatch mientras los dos commits incompatibles formen parte del source candidato.
- Mantener K=50 en el spec preparado; no reducir X/Y/K ni alterar Builder. No reiniciar ni parar servicios/actividades existentes.
- No restaurar Hefesto: Builder no fue despachado; el servicio sigue activo, así que no requiere mecanismo de rejoin.
- No declarar 12W activa, 12X running, Builder complete ni integración Echo.

## Pendiente

- Abrir scope SDD/Allowed Files vigente para correcciones mínimas revisadas; preservar source SHA y commits previos como evidencia. No modificar candidato hasta que ese scope/integración esté autorizado.
- Después: verificar source/dependencias limpios, compatibilidad watcher/workers/consumidores, elegir la próxima release libre del registro y desplegar por mecanismo canónico. Sólo entonces detener Hefesto por su servicio, lanzar una vez y verificar Builder+outputs durables antes de reincorporarlo.
- Revalidar liberación de capacidad física Zeus sin cancelar ILT_CONT y revalidar MT5/Kronos y pollers al dispatch.
