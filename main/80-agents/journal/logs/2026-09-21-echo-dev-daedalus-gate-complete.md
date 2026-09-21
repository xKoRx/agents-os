---
type: change_log
schema_version: 1
scope: session
created: 2026-09-21
updated: 2026-09-21
area: "[[Personal]]"
project: "[[Echo — Producto Integrado]]"
application:
entities:
  - "[[Echo]]"
  - "[[Aranea]]"
related:
  - "[[Echo + Echo Forge — Environment Contract]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-21 — Gate Echo DEV Daedalus completo: credencial PG resuelta y causa raíz (seed tests)

## Cambio

- **Tipo:** updated (Environment Contract §2/§5.1/§7) + updated (bitácora de `10-projects/Echo/Echo — Producto Integrado.md`) + updated (agent-run del mismo día).
- **Archivo(s):** `main/30-resources/aranea/07-integration/Echo + Echo Forge — Environment Contract.md`; `main/10-projects/Echo/Echo — Producto Integrado.md`; `main/80-agents/journal/agent-runs/2026-09-21-zcode-glm-5.3-flash-echo-dev-daedalus.md`; este change_log.
- **Fuera del vault:** `systemctl --user start/restart echo-core-dev` y restart de `echo-gateway-dev` tras la rotación de credencial aplicada por el owner; verificaciones de salud/restart/kill y lectura del grupo Kafka. Ningún binario recompilado (misma release `5dd998f1`).

## Motivo

- Owner resolvió el bloqueo de credencial (`echo_user` en PG DEV, misma credencial rotada para DEV y PROD, valor ETCD corregido) y pidió re-verificar el arranque del Core con `ENV=development` e identificar qué test del repo escribía la credencial de prueba en ETCD.

## Contenido

- Causa raíz identificada por grep de `SetVar` en `*_test.go`: `v3/sdk/etcd/echo_seed_test.go` (`TestSeedEchoConfig_Development` :115 y `TestSeedEchoConfig_Production` :167) y el mismo patrón en `v1` (:97, dev) y `v2` (:129/:182, dev+prod) escriben el mapa completo de config —incluida `postgres/password` con la credencial de prueba— al clúster ETCD real de los namespaces `/echo/development/` y `/echo/production/`, sin guardas (`testing.Short`/env). `v3/sdk/postgres/scratch_query_test.go` mantiene además la credencial versionada en un connStr; los scratch tests raíz y de telemetry sólo leen.
- Core DEV verificado operativo: `postgresql connected` a `.220/echo-develop`, kache consumiendo `echo.account-configs.v1`, automation_evaluator 5 perfiles, HTTP `:9090` health 200 local+LAN, restart controlado y recuperación ante SIGKILL con reconexión PG completa.
- Grupo `echo-core-v3` en `STABLE` con único miembro (`echo-core-kache-daedalus` desde `.161`, 5 particiones) ⇒ aislamiento confirmado en runtime.
- Gateway DEV tras restart: `PostgreSQL connected`, `automation handler` + `job scheduler` habilitados (degradación previa por diseño), health 200.
- AS-BUILT y reconciliación actualizados; pendiente registrado: blindar/eliminar seed tests (manager/owner Echo) y no ejecutar `go test ./...` desde la raíz hasta entonces.

## Impacto

- Gate `ECHO_CORE_GATEWAY_DEV_SYSTEMD_PASS` completo a nivel de ambiente; no certifica producto ni join Forge→Echo. PROD, workers compartidos, Flink/Kafka infra y screen `deployer` intactos. La credencial rotada nunca se persistió en vault, journal ni reporte.
