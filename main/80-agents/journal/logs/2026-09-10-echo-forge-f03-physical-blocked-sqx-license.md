---
type: change_log
schema_version: 1
scope: session
created: "2026-09-10"
updated: "2026-09-10"
area: "[[Echo]]"
project: "[[Echo Forge — F-03 SQX long-running]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge — F-03 SQX long-running]]"
related:
  - "[[Echo Forge — F-03 SQX Long-Running Contract]]"
  - "[[2026-09-10-symphony-sqx-trial-license-fleet-expired]]"
  - "[[2026-09-10-zcode-glm-5.3-flash-f03-physical-cert]]"
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

# 2026-09-10-echo-forge-f03-physical-blocked-sqx-license

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo Forge — F-03 SQX long-running.md`
  - `80-agents/memory/internal/known-errors/2026-09-10-symphony-sqx-trial-license-fleet-expired.md` (nuevo)
  - `80-agents/journal/agent-runs/2026-09-10-zcode-glm-5.3-flash-f03-physical-cert.md` (nuevo)

## Motivo

- Registrar el intento de certificación PHYSICAL F-03 sobre `382f4ba` en lab real (Hera), su veredicto `BLOCKED / CLOSED` por licencia SQX trial expirada, y el estado durable del lab aprovisionado para el reintento.

## Fuentes usadas

- SPEC §Certification #5 ([[Echo Forge — F-03 SQX Long-Running Contract]]); git state del repo (`382f4ba`, CLEAN, 2 ahead/0 behind); logs del worker/watcher candidatos en Hera; `temporal workflow show/list` (ns `sqx-prop`); ETCD `maintenance/state` y salidas directas de `sqcli` en Hera/Zeus.

## Resolución aplicada

- `Estado actual` + tabla de entrega + bitácora de la nota F-03 actualizados con el veredicto, los hashes de los binarios del commit, el aislamiento de lab (scopes `f03cert`, cola `f03-cert-queue`) y la evidencia del fallo de licencia; known-error nuevo por recurrencia del blocker; agent_run del segmento de certificación.

## Validación

- Gates iniciales git verdes; workflow de prueba `CANCELED` sin reanudación; fallo de `sqcli` reproducido manualmente en ambos hosts con las tres claves históricas; cero modificaciones de source en el repo y cero toques a `deploy/manifest.json` o releases.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir el delta en la nota F-03, archivar el known-error y borrar este log si el owner descarta el intento de certificación.
