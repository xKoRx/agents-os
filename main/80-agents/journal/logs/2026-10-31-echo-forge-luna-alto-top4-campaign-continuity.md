---
type: change_log
schema_version: 1
scope: session
created: "2026-10-31"
updated: "2026-10-31"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
application:
entities:
  - "[[Echo Forge — Operación Real V2]]"
related:
  - "[[Echo + Echo Forge — Environment Contract]]"
aliases: []
confidence: verified
source_feedbacks:
  - "[[2026-10-31-zcode-minimax-echo-forge-luna-alto-mt5-lifecycle-friction]]"
source_session: "2026-10-31-luna-alto-forge-top4"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Change Log — Campaña física "LUNA ALTO" (Forge Top 4 → Echo REGISTER_ONLY)

## Qué cambió

- **Interfaz Echo v2 habilitada en Echo DEV** (Daedalus): el `echo-gateway` desplegado era un binario stale de `fa0acabd`, sin `loadLabV4Config`, por lo que `POST /api/v2/strategy-ingestions` respondía **404**; se reconstruyó desde `3eaed4d2` (release `labv4-3eaed4d2-20261031`, `vcs.modified=false`) y la ruta monta y admite la identidad `producer_ingest`. Rollback documentado en su `BUILD.md`.
- **Perfil de destino Forge→Echo v2 sembrado en ETCD** (`/sqx-worker/production/echo/ingest/v2/*`): destino, namespace, writer (= `principal_ref` de la identidad), `source_instance_ref`, `base_url` (Gateway DEV), bearer (derivado de la identidad existente, **nunca impreso ni persistido en el vault**) y timeout.
- **Cuatro contratos corregidos en `xKoRx/symphony`** con release y rollout 4/4 verificado por SHA en cada host: `84088bb` (release 0.6.1, `Origin` del subflujo dynamic-groups), `3a30155` (0.6.2, accessor `GetTelemetry()` del request de `verify_mt5_ex5_lineage_v1`), `4a4c1bb` (0.6.3, acreditación del lineage EX5 por ancestría durable), `d3069ee` (0.6.4, `RoundtripExact` acepta el fin de ventana inclusivo que MT5 representa con midnight exclusivo). Test nuevo `TestRoundtripExact_AcceptsBothEndConventions`; sin regresión en `go test ./workflows/` ni `go test ./core/domain/`.
- **Continuidad del proyecto actualizada**: [[Echo Forge — Operación Real V2]] registra la campaña, la evidencia física lograda, la frontera que bloquea el cierre y la prueba mínima para cerrarla.
- **Agente registrado**: `80-agents/journal/agent-runs/2026-10-31-zcode-minimax-m3.1-flash-echo-forge-luna-alto-top4.md`.
- **Seguimiento automatizado**: tarea programada `automation-ae1c1041` (cada 15 min) que vigila el FlowRun `a5eafeb7-da3a-4986-9bfb-e2b005da2144` y ejecuta la verificación final (oráculo de ranking + igualdad de conjuntos en Echo) cuando cierre.

## Por qué

La topología pedida por el owner — Builder real → group por `logical_type` con Top 4 sobre el `MetricSet` del `final-reretester` → MT5 dentro del group → ingesta `echo_ingestion_v2` — **nunca se había ejecutado físicamente**: `w11`_certificado tenía el MT5 a nivel root y sin ingesta; la cadena C1 terminaba en `final-reretester`; y la config `w12V` quedó `SPEC_VALID` pero nunca despachada. La primera ejecución en frío lmana cuatro contratos rotos que sólo aparecen corriendo, y la interfaz Echo v2 no existía en ningún despliegue.

## Límites

- El backtest MT5 quedó **colgado en el terminal Windows** (señal: `terminal64` con 9,7 s de CPU y 16 MB RSS, sin artefactos nuevos en 84 min); la causa raíz **no** quedó aislada. Sin Top 4 materializado ni historia en Echo, el veredicto de la campaña es **`NO_GO`** con frontera exacta y prueba mínima para cerrarla.
- La verificación de rollout por `verify_rollout.sh` no puede autenticarse por SSH desde Daedalus (limitación pre-existente); el rollout se acreditó por lectura física de SHA en los 4 hosts.
- Sin impacto en dinero real: no se habilitó ninguna EA, cuenta ni capital.
