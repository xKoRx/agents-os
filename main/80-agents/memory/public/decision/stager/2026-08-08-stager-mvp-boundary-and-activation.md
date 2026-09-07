---
type: decision
scope: application
created: 2026-08-08
updated: 2026-08-10
area: "[[Echo]]"
project: "[[Stager]]"
application: "[[stager-app]]"
entities:
  - "[[Stager]]"
  - "[[stager-app]]"
  - "[[echo-forge]]"
related:
  - "[[Echo Forge - Cross-Platform Stager]]"
  - "[[2026-08-08-stager-independent-project-and-core-created]]"
  - "[[2026-08-10-stager-product-boundary-and-durable-activation]]"
aliases:
  - stager mvp architecture decision
  - stager pending-next activation
confidence: verified
source_session:
load_policy: when_application_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/application
  - area/echo
  - project/stager
  - app/stager-app
  - tech/deployment
  - tech/go
---

# Stager MVP boundary and recoverable activation

## Contexto

- Symphony necesita staging Linux/Windows, pero copiar el Bash a PowerShell mantendría dos implementaciones y mezclaría integración con producto.
- El caso real sólo exige MinIO, manifest, plataforma exacta, releases versionadas, selección local y una señal de upgrade.
- Una IA validadora independiente, sin acceso al código, aprobó la frontera y recomendó detener nuevo diseño hasta demostrar la integración real.

## Decisión

- `github.com/xKoRx/stager` es una aplicación/repositorio Go independiente, hermano de `symphony`, `echo` y `sdk`.
- Stager es one-shot: lock → recovery → manifest → plataforma exacta → download/verify → release versionada → activación → exit.
- MinIO es el único source productivo del MVP; Symphony es primera integración, nunca dependencia del core.
- Estado mínimo: `CURRENT`, `PENDING.next`, `PENDING`, `stager.lock` y `releases/<version>`.
- Activación: escribir `PENDING.next`, reemplazar atómicamente `CURRENT`, escribir/reemplazar `PENDING` y borrar el intent. Recovery local ocurre antes de MinIO.
- El manifest preserva top-level legacy y agrega `entrypoint` + `files[].path/object_key/size/sha256/executable`. Está diseñado para migración aditiva compatible; no es compatible hasta que Symphony produzca esos campos.
- El core exige la plataforma local sin fallback, pero no obliga ambas plataformas. Symphony congela en su gate si una release de flota requiere Linux+Windows o acepta subconjunto explícito.
- No se agregan scopes, control plane, DB, daemon ni estados adicionales antes de MinIO real, shadow Linux y E2E Windows ocupado.

## Vigencia

- Esta decisión conserva autoridad sobre el alcance y rationale del MVP completado.
- La evidencia productiva posterior del bridge `0.2.40` promueve la evolución de activación y runtime a [[2026-08-10-stager-product-boundary-and-durable-activation]]; el congelamiento de estados y la consecuencia de dejar todo lifecycle fuera de Stager ya no gobiernan el producto posterior al MVP.

## Rationale

- `PENDING.next` cierra la única ventana crítica conocida con una primitiva filesystem pequeña; un journal general no aporta al caso actual.
- `files[].path` preserva el layout Linux real (`bin/`, runner y configuración) sin lógica Symphony-specific.
- Scheduling y supervisión quedan en systemd/Task Scheduler/SCM; Stager no mantiene procesos ni conoce drain.
- La integración concentra la complejidad correcta: publisher Symphony, quiesce Temporal/MT5 y lifecycle Windows.

## Consecuencias

- Stager puede evolucionar por configuración; hoy una config equivale a un deployment target.
- El Bash Linux permanece como rollback hasta demostrar paridad.
- El MVP core queda congelado salvo bugs descubiertos por integración.
- El próximo trabajo ocurre en Symphony y Windows host, no en nuevo diseño de plataforma.

## Alternativas descartadas

- Bash + PowerShell duplicados.
- Binario dentro del módulo Symphony.
- Daemon, API, DB, cola, control plane o distributed lock.
- `ACTIVATION.json`, `PREVIOUS`, `RUNNING` y auto-rollback para el MVP.
- Manifest/protocolo nuevo incompatible o adapters anticipados para otros artifact sources.
