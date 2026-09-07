---
type: change_log
scope: session
created: 2026-06-27
updated: 2026-06-27
area: "[[Symphony]]"
project: "[[Echo Forge]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge]]"
related:
  - "[[80-agents/journal/sessions/2026-06-27-echo-forge-retester-concurrency-failure-summary]]"
aliases:
  - echo forge retester concurrency failure resolved
confidence: verified
source_session: 4af42ce7-35ef-4f46-9445-a0a05872312a
load_policy: manual
indexable: false
index_priority: never
tags:
  - app/echo-forge
  - app/echoforge
  - area/symphony
  - kind/changelog
  - project/echo-forge
  - project/echoforge
  - scope/session
---
# echo forge retester concurrency failure resolved

## Cambio

- **Tipo:** modified
- **Archivo(s):**
  - `/Users/rjara/go/src/github.com/xKoRx/symphony/sqx/activities/worker/pipeline/step.go` (modified)
  - `/Users/rjara/go/src/github.com/xKoRx/symphony/sqx/activities/worker/steps/steps.go` (modified)
  - `/Users/rjara/go/src/github.com/xKoRx/symphony/sqx/activities/worker/pipeline/hooks/cleanup_databanks.go` (modified)
  - `/Users/rjara/go/src/github.com/xKoRx/symphony/deploy/manifest.json` (modified)

## Motivo

- Corregir el bug de concurrencia física (race condition) en los workers que provocaba que los subflujos paralelos por tipo lógico sobreescribieran y purgaran el mismo directorio del Retester (`02_retester_full`).

## Fuentes usadas

- Logs del worker Zeus y ejecuciones en Temporal.

## Resolución aplicada

- Aislamiento físico de los directorios locales del disco del worker concatenando el tipo lógico en la firma del nombre del proyecto SQX.
- Bumping de versión a `0.1.24`, empaquetado, sync con MinIO y reinicio del worker Zeus.

## Validación

- Tests unitarios de go ejecutados y aprobados (`go test ./sqx/...`).
- Reinicio exitoso del servicio `symphony-worker.service` en el host remoto y confirmación de la versión `0.1.24`.
