---
type: runbook
schema_version: 1
scope: application
created: "2026-08-29"
updated: "2026-08-29"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Symphony]]"
related:
  - "[[deployment-proof]]"
  - "[[evidence-channel-discovery]]"
  - "[[symphony-release-certification]]"
aliases:
  - prueba de workers Symphony
  - matriz de canales de evidencia Echo Forge
confidence: verified
source_session: DURABLE-ARTIFACT-VERIFIED-READS-FINAL-E2E-NORMAL
load_policy: when_application_loaded
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/application
  - project/echo-forge
---

# symphony-worker-runtime-proof

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Propósito

- Aplicar `deployment-proof` sobre la flota Symphony (workers Linux Zeus/Hera/Kronos y worker Windows MT5 `worker-kronos`), con la matriz real de canales de evidencia vigente (verificada 2026-08-29).

## Precondiciones

- Release publicada con sha256 por artefacto ([[symphony-release-certification]]); probe read-only operativo ([[symphony-prod-probe]]) con modo `queue`.

## Matriz de canales (verificada 2026-08-29)

| Pregunta | Canal | Authority | Limitación |
| --- | --- | --- | --- |
| ¿worker vivo y en cola? | Temporal `DescribeTaskQueue` (probe modo queue) | alta | no prueba qué binario corre |
| ¿qué proceso corre ahora? | rotación de identity/PID de pollers (pre vs post deploy) | media | reinicio ≠ binario nuevo, exige combinar |
| ¿qué binario se publicó? | manifest MinIO `deploy` (`worker/sqx/manifest.json`) | alta | no prueba proceso activo |
| ¿qué commit contiene el binario? | `go version -m` sobre el artefacto del manifest | alta | requiere binario local |
| ¿el host aplicó el release? | stager (systemd + `/opt/stager/releases/<v>/bin/symphony`) + SSH on-host `echo-forge-worker` (path del binario + sha256 comparado contra el manifest) | alta (verificada 2026-08-30) | SSH `kronos` fue intermitente (2/6 timeouts transitorios); reintentar |
| logs de worker | Loki `http://192.168.31.60:3100` | ninguna | workers no llegan ahí (sin streams) |
| versión declarada en telemetría | etcd key `version` → `app.version` | ninguna | estática (`0.0.21`), no identifica release |
| traces runtime | Jaeger `http://192.168.31.60:16686` | baja | sin trazas recientes retenidas |
| acceso a hosts | SSH `kor@192.168.31.x` vía wrapper canónico `echo-forge-worker` (credencial owner-approved en el vault; sshpass, no-interactivo OK) | alta (verificada 2026-08-30; corrige la entrada 2026-08-29 que la daba por no disponible) | sólo lectura/diagnóstico sin autorización explícita de mutación |
| MinIO/PG/Mongo | probe `di` producción | alta (lectura) | read-only |

## Procedimiento

1. PRE: capturar identidades de pollers por cola con el probe (`queue`): `sqx-main-queue` (activity+workflow) y `sqx-mt5-queue`; registrar PIDs por host (formato `pid@hostname`).
2. Publicar la release ([[symphony-release-certification]]); el manifest es la autoridad del contenido entregado (sha256 por archivo).
3. POST (≥2-5 min): repetir `queue`; por host requerido demostrar rotación: identidad PRE desapareció e identidad POST aparece tras el timestamp de publicación del manifest. Windows MT5 rota en `sqx-mt5-queue` (host `worker-kronos`).
4. Clasificar por worker: `ON_NEW_RELEASE: YES` (rotación + manifest pineado + stager canónico), `UNKNOWN` (sin rotación), `NO`. Un worker UNKNOWN que participa en el gate ⇒ PARTIAL/FAIL y documentarlo.
5. Verificar ausencia de mezcla: identidades PRE no deben sobrevivir más allá del drenaje; si persisten >10 min, tratarlas como procesos viejos vivos (mezcla).

## Validación

- `ALL_REQUIRED_WORKERS_ON_NEW_RELEASE: PASS` sólo con los 4 requeridos (Zeus, Hera, Kronos Linux, worker-kronos Windows) con prueba. Sesión 2026-08-29: 3/4 rotaron; Kronos `710524` no rotó en ~2h — ante esto, verificar stager/timer del host (requiere acceso interactivo) antes del próximo E2E.

## Rollback / recuperación

- Los workers no rotados aplicarán el release cuando su stager corra; no forzar por MinIO (re-publicar la misma versión es no-op por diseño del manifest). Mejora pendiente (feedback 2026-08-29): readout de versión por worker o envío real de logs a Loki.

## Evidencia

- [[2026-08-29-durable-artifact-verified-reads-final-e2e-normal]] (decisión) y feedback [[2026-08-29-symphony-worker-observability-session-feedback]].
