---
type: skill
schema_version: 1
name: echo-production-operational-audit
description: Auditoría operacional E2E read-only de Echo PROD (host .71, bridges Windows, PG .220, Kafka .247-249, etcd /echo/production/, ARGUS) tras una ventana de cambios; gates G1-G10 con evidencia física, veredicto OPERATIONAL_* y comparación contra auditorías previas. Cargar para auditar funcionamiento real de Echo en producción, nunca para desarrollar ni desplegar.
scope: area
created: "2026-09-21"
updated: "2026-09-21"
area: "[[Aranea]]"
entities:
  - "[[Echo]]"
  - "[[Aranea]]"
related:
  - "[[30-resources/agents/skills/aranea-agent-dev/SKILL.md|aranea-agent-dev]]"
  - "[[30-resources/agents/skills/aranea-mcps-expert/SKILL.md|aranea-mcps-expert]]"
  - "[[Echo + Echo Forge — Environment Contract]]"
  - "[[Echo — Access & Physical Capability Matrix]]"
  - "[[30-resources/runbooks/aranea-ssh-mcp|aranea-ssh-mcp]]"
  - "[[30-resources/runbooks/aranea-etcd-mcp|aranea-etcd-mcp]]"
  - "[[30-resources/agents/skills/readonly-production-probe/SKILL.md|readonly-production-probe]]"
  - "[[30-resources/agents/skills/operational-healthcheck-policy/SKILL.md|operational-healthcheck-policy]]"
aliases:
  - echo prod audit
  - auditoria operacional echo
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - scope/area
  - area/aranea
  - area/echo
  - tech/mcp
  - action/audit
---

# echo-production-operational-audit

## Purpose

Ejecutar una auditoría operacional read-only de Echo PROD que responda, con evidencia física y persistencia, si el sistema funciona de verdad tras una ventana de cambios: qué corre, con qué versión, qué cambió, si hay regresiones, si el flujo E2E procesa y persiste eventos, si el trading está íntegro y los controles de riesgo operativos. Prohíbe inferir salud desde health 200, procesos vivos, ACKs o ausencia de errores; exige trazar operaciones reales existentes hasta evidencia de broker y persistencia, y emite gates G1–G10 + veredicto `OPERATIONAL_PASS | OPERATIONAL_DEGRADED | OPERATIONAL_FAIL | INSUFFICIENT_EVIDENCE`. El camino exacto que ya funcionó (comandos, queries, límites y failure modes reales del 2026-09-21) está registrado aquí; el informe tipo queda en `10-projects/Echo/Echo — Production Operational Audit 2026-09-21.md`.

## Minimal Read

1. Router `30-resources/agents/skills/aranea-agent-dev/SKILL.md` y [[Echo + Echo Forge — Environment Contract]] — límite DEV/PROD y qué NO es PROD (Daedalus es DEV; el Gateway de certificación E-04 NO es el de producción).
2. `30-resources/agents/skills/aranea-mcps-expert/SKILL.md` — capabilities RO vigentes y sus límites por ambiente.
3. Esta skill (Procedure trae los comandos exactos).
4. Al redactar el informe, la plantilla: `10-projects/Echo/Echo — Production Operational Audit 2026-09-21.md` (secciones A–N).
5. Sólo si cambia el plano de acceso: runbooks `30-resources/runbooks/aranea-ssh-mcp.md`, `aranea-postgres-mcp.md`, `aranea-etcd-mcp.md`, `aranea-observability-mcp.md`.

## Procedure

1. **Preconditions.** Verificar VPN Aranea activa; confirmar que la tarea es auditoría read-only y que existe ventaja de capacidades RO vigentes (`echo-runtime-prod` viewer, `aranea-postgres-ro`, `aranea-hasura-prod-ro`, `aranea-observability-ro`, `aranea-etcd-ro`). Kafka PROD y los hosts Windows de bridges NO tienen capability: sus verificaciones quedan `EVIDENCE_GAP` documentado, no se improvisan accesos.
2. **Discovery de ambiente (G1).** `aranea-ssh` profile `echo-runtime-prod`: `read-command hostname` (esperado `echo`), `id` (esperado `uid=1001(echo-dev)`), `ps aux` (buscar `echo-gateway`, `echo-core`, `echo-functions`, nginx, promtail; registrar PID, usuario, fecha de START, path del binario), `ss -tlnp` (listeners esperados 80/9080/9090/8080/8090; anotar extras). Confirmar que NO es DEV: hostname ≠ `daedalus`, namespace ETCD `/echo/production/` presente, telemetría con `deployment.environment=production`. Cero proceso `echo-bridge` en .71 es normal: los bridges corren en Windows (`mt4-ttp`, `mt4-ftmo`, `mt4-real`) y se observan por Loki/Prometheus.
3. **Runtime (G2).** Identidad binaria al máximo alcanzable: paths de `ps aux`, fechas de arranque (correlacionar con historial de despliegues del vault), `service.version` OTEL en logs. SHA/commit exacto = UNKNOWN con capabilities vigentes (viewer no lee `/home/kor/echo` ni ejecuta nada; Loki no retiene el arranque original): declararlo, no simularlo.
4. **Cambios de la ventana (G10).** Git local del repo (en Daedalus `~/go/src/github.com/xKoRx/echo`): `git log --all --since="<inicio ventana>" --pretty="%h %ad %d %s" --date=iso` + tip de `origin/master`; distinguir commit publicado / compilado / desplegado / corriendo. En PROD, "sin reinicio" se demuestra con fechas de START de `ps aux`; el lab-worker es transitorio: su actividad se demuestra con `echo.lab_job_runs` (ver paso 8), no con procesos.
5. **Config efectiva (G3).** `aranea-etcd-ro`: `etcd_list_keys /echo/production/` + `etcd_get_value` de keys no-secretas (postgres host/database/port/user/schema/sslmode/pool_*, kafka/brokers, gateway/port, gateway/core_internal_url, bridge/pipe_prefix, functions/enabled, telemetry/*). Las keys con nombre secreto (password/token/key) son excluidas por el MCP por diseño: su validez se demuestra FUNCIONALMENTE (auth PG fresca exitosa de lab-worker/core), nunca leyéndolas. Contrastar cada valor contra el comportamiento observado (logs, listeners). Buscar activamente filtración DEV→PROD (endpoints .44:19091, .161, echo-develop en namespace production = hallazgo).
6. **Servicios y dependencias (G4).** PG: `SELECT datname, numbackends, xact_commit, xact_rollback FROM pg_stat_database WHERE datname IN ('echo','echo-develop')` — `numbackends('echo')` ≥ 2 demuestra conexiones app vivas. Hasura: `get_version` + `get_inconsistent_metadata`. etcd y ARGUS ya demostrados por el hecho de consultarlos. Logs frescos por servicio en Loki (ver paso 9). `systemctl`/`docker ps`/`curl` están POLICY_DENIED en el viewer: no intentarlos.
7. **Transporte (G5).** Evidencia indirecta del camino bridge→Kafka→core→StateFun→PG: latencia `created_at − opened_at` en `echo.trade_journal` (1–2 s = flujo vivo); logs core `account_sync/position_sync/trade_journal: … arrived|persisted`; logs bridge `Unified batch processed`/`Snapshot published`; gateway `ClientConfig published to Kafka` (última ocurrencia). `echo_bridge_executions_connected` en Prometheus (instant) = terminales conectadas por cuenta. Lag directo de consumer groups PROD = EVIDENCE_GAP (sin capability).
8. **Datos y trading (G6/G7/G8).** Queries RO acotadas sobre db `echo` schema `echo` (identidad `mcp_echo_prod_ro`): recencia y volumen por día (`trade_journal` GROUP BY created_at::date — 0 filas sábados es mercado cerrado, no gap); duplicados (`GROUP BY trade_id, account_id HAVING count(*)>1` → vacío esperado); consistencia (`count(active_positions)` == legs OPEN de ejecución; max(updated_at) de `accounts` en segundos); estados (`status` CLOSED/OPEN/FAILED; FAILED con error_code 4109 = broker rechazó, ticket 0, son históricos acotables por fecha); re-touched sin crear filas = re-envío idempotente de terminales (benigno, documentar). E2E: elegir 1–2 trades reales de la ventana, seguir trade_id en journal (Reference + legs), tickets ≠ 0 = evidencia física de broker mediada por terminal; declarar inspección directa de terminal como no ejecutada. Riesgo: WARN de `execution_planner` excluyendo cuentas no-operativas, tablas `automation_*`/`risk_policy` presentes, exposición = balances agregados por status de `accounts` SIN calcular PnL/riesgo derivado.
9. **Observabilidad (G9).** Loki datasource `P8E80F9AEF21F6940`: `list_loki_label_names/values` (services: echo-core, echo-gateway, echo-bridge, echo-lab-worker), queries por servicio con ventanas acotadas (core emite ~15M líneas DEBUG/día: usar stream selector específico y ventana corta, o `query_loki_stats` antes). Errores: filtrar por atributo/error_code real, no por substring "error" (los INFO de journal lo contienen). Promediar retención: ~7 días (agosto no existe). Silencio del gateway ≥24 h es normal (event-driven): usar `lab_job_runs`/journal para actividad, no ausencia de logs. Prometheus `PBFA97CFB590B2093`: métricas `echo_bridge_*` vivas; `echo_agent_*` stale (exporter viejo).
10. **Gates y veredicto.** Completar G1–G10 con PASS/DEGRADED/FAIL/UNKNOWN/NOT_APPLICABLE (NOT_APPLICABLE exige demostrar que el componente no existe en runtime PROD); UNKNOWN jamás cuenta como PASS; sin `OPERATIONAL_PASS` si un gate crítico es FAIL/UNKNOWN o queda una degradación demostrada sin causa. Hallazgos con ID/SEVERIDAD/EVIDENCIA/IMPACTO/CAUSA(demostrada vs hipótesis)/OWNER/ACCIÓN/GATE DE REGRESIÓN. Escribir el informe en `10-projects/Echo/` (materializador, tipo `doc`) y actualizar bitácora del proyecto.
11. **Escalación inmediata.** Si aparece riesgo inmediato para operaciones o capital (exposición no explicada, posiciones huérfanas vivas, terminales desconectadas con legs abiertos, backlog creciente, password/auth rota en PROD): notificar al owner de inmediato sin esperar el informe y sin intentar remedio.
12. **Cierre.** Commits sólo de documentación/skill; read-back de informe, skill y referencias; registrar `agent_run`; dejar continuidad para la siguiente auditoría (regresión = comparación contra este informe).

## Output

```text
VERDICT:             OPERATIONAL_PASS | OPERATIONAL_DEGRADED | OPERATIONAL_FAIL | INSUFFICIENT_EVIDENCE
RUNTIME:             <procesos, hosts, PIDs, arranques, versión, SHA|UNKNOWN>
CHANGES:             <cambios de la ventana correlacionados, separando publicado/compilado/desplegado/corriendo>
E2E:                 <trades trazados con tickets/precios o E2E_NO_SAMPLE_AVAILABLE>
GATES:               <G1..G10 + una línea de justificación c/u>
FINDINGS:            <AUD-xx con severidad, evidencia, causa demostrada|hipótesis, owner, gate de regresión>
EVIDENCE_GAPS:       <lo no verificable con capabilities vigentes, explícito>
REPORT:              <ruta del doc materializado>
```

## Hard Rules

- READ ONLY absoluto: prohibido enviar órdenes, cerrar/modificar posiciones, cambiar config/riesgo/policies, reiniciar servicios, migrar, seedear, correr `go test` contra infra real, escribir ETCD/PG/Mongo, producir a Kafka o tocar offsets, alterar systemd, desplegar. Si una tool intenta escribir: STOP de esa tool. Sin identidades DEV para PROD y viceversa.
- No ejecutar endpoints/comandos cuyo carácter de lectura no esté demostrado; en `echo-runtime-prod` sólo el allowlist del viewer (`whoami/hostname/id/ps aux/ss -tlnp/cat/ls/journalctl`); compound/pipelines pueden ser denegados: dividir, no escalar.
- `pg_stat_activity` con rol RO oculta `client_addr/state` de backends ajenos: NO concluir "sin conexiones" desde esa vista; usar `pg_stat_database.numbackends` + recencia de datos. Análogo en Loki: `query_loki_stats` puede devolver 0 para entradas de hace segundos (lab-worker vivo con corrida de hace 32 s devolvió stats 0); para liveness del Lab la ground truth es `max(created_at) de echo.lab_job_runs` contra `now()` de PG, no Loki.
- No atribuir un defecto al cambio más reciente sin evidencia; sin despliegue en PROD, la correlación es con config/infra (ETCD, timers), no con código.
- Secretos jamás se leen, imprimen ni persisten; la validez de credenciales se demuestra por autenticación exitosa fresca, no por valor.
- No reconstruir PROD desde documentos históricos: la evidencia física del día manda; los docs del vault datan el baseline.
- Distinguir siempre PRODUCT_FAILURE / OBSERVABILITY_FAILURE / EVIDENCE_GAP; silencio de logs ≠ ausencia de problema (lab-worker 66 h sin logs ni filas = degradación real) y silencio de gateway = normalidad event-driven.
- Infra compartida no-Echo (workers SQX/MT5, screen `deployer` en Daedalus, namespaces flowkit/deployer/symphony): observar, no tocar; hallazgos adyacentes se reportan, no se remedian.
- Recovery de auditoría interrumpida: reanudar desde el informe parcial/continuidad; re-ejecutar sólo las lecturas faltantes; jamás repetir acciones de escritura (no las hay) ni ampliar permisos para completar gates; los gates incompletos quedan UNKNOWN.
- Validación de esta skill: ejecutar discovery (pasos 2–3) + una muestra segura por familia (1 query PG, 1 query Loki, 1 get ETCD) y los 3 casos de activación; si una ruta esencial no se pudo comprobar, declarar UNKNOWN y no `SKILL_VALIDATED`.
