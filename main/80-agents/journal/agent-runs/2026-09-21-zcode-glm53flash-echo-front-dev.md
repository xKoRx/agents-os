---
type: agent_run
schema_version: 1
scope: session
created: "2026-09-22"
updated: "2026-09-22"
area: "[[Aranea]]"
project: "[[Echo]]"
application:
entities:
  - "[[Echo + Echo Forge — Environment Contract]]"
related:
  - "[[ZCode]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
model_source: host
task_type: coding
task_complexity: medium
outcome: success
verification: verified
evaluator: agent
user_rework: unknown
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-run
  - scope/session
---

# Agent Run — 2026-09-21-zcode-glm53flash-echo-front-dev

## Trabajo

- **Objetivo:** levantar el front DEV (echo-backoffice) en Daedalus como parte del ambiente de desarrollo Echo, con endpoints DEV correctos y acceso LAN.
- **Alcance atribuible a esta combinación superficie×modelo:** reconciliación de contrato, build del front con override por proceso, escritura aditiva ETCD DEV (`gateway/cors_allowed_origins`), restart controlado de `echo-gateway-dev.service`, unidad `systemd --user` `echo-front-dev.service` (vite preview :4173), smoke HTTP + browser, actualización del contrato AS-BUILT (§5.7).
- **Artefactos afectados:** `~/.config/systemd/user/echo-front-dev.service` (nuevo, en Daedalus, fuera del vault); ETCD DEV key `/echo/development/gateway/cors_allowed_origins`; `v3/front/dist` rebuild en `xKoRx/echo` @ `5dd998f1` (repo quedó limpio); [[Echo + Echo Forge — Environment Contract]] §5.7.

## Evidencia

- **Validaciones ejecutadas:** health Gateway `:8090` y Core `:9090` 200 pre/post restart; `forge_ingest_misconfigured=false` en journal post-restart; preflight CORS OPTIONS 204 con `Access-Control-Allow-Origin` reflejado; front `:4173/` y SPA fallback `/watchtower` 200 por LAN; screenshot browser con shell del backoffice renderizado (nav completa, reloj UTC vivo, system log).
- **Resultado observable:** `echo-front-dev` active+enabled, RSS ~119 MB; Core MainPID 2479388 intacto; Gateway nuevo MainPID 3056377.
- **Limitaciones de la evidencia:** data plane GraphQL inoperante (Hasura DEV sin auth webhook hacia `/api/v1/auth/hasura` y sin token de operador ingresado) — gap declarado, no bloquea el serve layer. Reboot físico del host no ejecutado.

## Evaluación

- **Correctness:** 5 — todos los gates verificados en la capa dueña de la semántica (HTTP, journal, browser).
- **Autonomy:** 5 — decisión dev-vs-build resuelta con evidencia (swap lleno, endpoints horneados a build) sin bloquear al owner.
- **Efficiency:** 4 — 6 pasos con verificación intermedia; sin reintentos.
- **Tool use:** 5 — MCP RO para read-back ETCD, browser para smoke visual, curl/etcd API v3 para escritura puntual.

## Resultado

- **Outcome:** DEV_OPERATIONAL — delta 2026-09-22 (2): reparado el plano de auth/propagación que el owner reportó (503 en Republish Configs + bridge sin cuentas nuevas). Causas raíz: (a) sin tokens `gateway/auth/*` en ETCD DEV ⇒ 503 AUTH_MISCONFIG en todo endpoint autenticado; (b) 6 event triggers de Hasura DEV apuntando al Gateway muerto `.211` y sin Bearer ⇒ configs nunca publicadas (topic con datos stale de mayo). Fixes: 4 tokens aleatorios en ETCD (file 600 fuera del vault), `replace_metadata` con backup (triggers → `.161` + Bearer), commit local `3596fc48` (amplía `269fefc3` con `VITE_GATEWAY_CONTROL_TOKEN`). Aprendizaje clave: Hasura no emite evento cuando ninguna columna monitoreada cambia de valor (el no-op update fue un test inválido); el protocolo WS `graphql-ws` de este Hasura exige la secret en `connection_init.payload.headers`.
- **Rework posterior:** owner decide push/revert de `3596fc48`; rotar secret/tokens DEV si la exposición por LAN no se acepta; endurecer a Bearer requiere cablear auth webhook en el Hasura DEV.
- **Aprendizaje para comparar herramientas:** el override de env por proceso en `vite build` permite desplegar DEV sin tocar `.env` trackeado; verificar el formato exacto de auth WS por protocolo antes de asumir el documentado; un 503 AUTH_MISCONFIG siempre precede al 401 — revisar la config del server antes que la credencial del cliente.
