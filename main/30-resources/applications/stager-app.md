---
type: application
status: active
slug: stager
area: "[[Echo]]"
lang: Go
github:
path: ~/go/src/github.com/xKoRx/stager
aliases:
  - stager application
  - xKoRx/stager
  - deployment stager
tags:
  - kind/application
  - area/echo
  - app/stager
created: 2026-08-08
updated: 2026-08-10
---

# stager-app

%% Naming: stager-app distingue la aplicación del proyecto de implementación [[Stager]]. El slug y repo son `stager`. %%

> [!info]+ Stager
> **Lenguaje:** Go · **Área:** [[Echo]]
> **GitHub:** remote pendiente · **Path local:** `~/go/src/github.com/xKoRx/stager`
> **Módulo:** `github.com/xKoRx/stager`

## 📝 Descripción

- Reconciliador one-shot de deployment local. Lee un manifest desde MinIO, selecciona la plataforma exacta, descarga y verifica artefactos, instala una release versionada, actualiza `CURRENT`, emite `PENDING` y termina.
- Es independiente del software desplegado. [[echo-forge]] es su primera integración, pero el core no conoce Symphony, SQX, MT5, Temporal, workers ni supervisores.

## 🔧 Datos útiles

- **Repo:** `xKoRx/stager` — repositorio Git local; remote y commit inicial pendientes de decisión humana.
- **Path local:** `~/go/src/github.com/xKoRx/stager`
- **Producción:** Stager Go desplegado en Zeus/Hera/Kronos desde el cutover Symphony `0.2.40`; un bridge legacy no versionado permanece como compatibilidad temporal.
- **Trabajo activo:** [[Stager - Cross-Platform Deployment Lifecycle]] gobierna activación durable, runtime Linux/Windows y retiro del bridge.
- **Módulo:** `github.com/xKoRx/stager`
- **Stack / notas:** Go 1.24, MinIO SDK, filesystem local, locks Unix/Windows, SHA-256 y releases versionadas.
- **Estado MVP:** core y documentación listos para Review; integración productiva aún pendiente.

## 🤖 Contexto para agentes

- **Rol de la aplicación:** deployment local genérico; una ejecución y configuración equivalen hoy a un deployment target.
- **Cómo se relaciona con el trabajo activo:** [[Stager]] controla implementación y roadmap; [[Echo Forge]] patrocina el primer caso; [[echo-forge]] debe producir el manifest aditivo y consumir `CURRENT`/`PENDING`.
- **Instrucciones locales:** leer `AGENTS.md` del repo antes de editar.
- **Comandos seguros de validación:** `go test ./...`, `go vet ./...`, builds `CGO_ENABLED=0` para `linux-amd64` y `windows-amd64`.
- **Dependencias o aplicaciones relacionadas:** MinIO como único source del MVP; [[echo-forge]] como primera integración.
- **Fuentes canónicas a consultar:** `specs/STAGER-MVP/SPEC.md`, `docs/SYMPHONY.md`, `internal/manifest/`, `internal/staging/`.

## Contratos e invariantes

- `RunOnce`: lock → recovery local → manifest → plataforma exacta → stage/verify → activación → exit.
- Estado mínimo: `CURRENT`, `PENDING.next`, `PENDING`, `stager.lock` y `releases/<version>`.
- El manifest está **diseñado para una migración aditiva compatible**; Symphony todavía no produce los campos nuevos.
- `files[].path` conserva layout relativo, incluyendo `bin/` y configuración; no instala todo plano.
- El Stager exige la plataforma local y no hace fallback. La política de release Symphony completa —ambas plataformas o subconjunto explícito— se decide en el gate de integración.
- No seguir ampliando arquitectura antes de probar MinIO real, shadow Linux y E2E Windows con MT5 ocupado.

## Arquitectura del sistema

```mermaid
flowchart LR
    Publisher["Publisher del consumer"] -->|"artifacts primero"| MinIO["MinIO bucket + manifest"]
    MinIO --> Stager["Stager RunOnce"]
    Stager --> Release["releases/version verificada"]
    Release --> State["PENDING.next → CURRENT → PENDING"]
    State --> Consumer["Consumer decide drain"]
    Consumer --> Supervisor["Supervisor externo reinicia"]
```

- El manifest remoto expresa la release deseada.
- `CURRENT` local expresa la release seleccionada para el próximo arranque, no la que necesariamente corre ahora.
- `PENDING` es un mensaje filesystem opaco. Stager no sabe quién lo consume ni cómo drena.
- Una falla remota no muta el estado activo. Una activación local incompleta se recupera antes de volver a MinIO.

## Estado implementado versus integración pendiente

| Capability | Estado | Fuente |
|---|---|---|
| Parser/validator manifest | implementado y testeado | `internal/manifest/manifest.go` |
| MinIO ArtifactSource | implementado | `internal/source/minio.go` |
| RunOnce/idempotencia | implementado y testeado | `internal/staging/runner.go` |
| Size/SHA-256/path safety | implementado y testeado | `internal/staging/runner.go` |
| Lock Unix/Windows | implementado; cross-build PASS | `lock_unix.go`, `lock_windows.go` |
| Atomic replace Unix/Windows | implementado; VM Windows aún pendiente | `state_unix.go`, `state_windows.go` |
| Publisher/MinIO/shadow Symphony | completado; cutover `0.2.40` | [[Stager - Symphony Publisher Integration]] |
| Bridge legacy Linux | productivo, no versionado; contención P0 | [[Stager - Cross-Platform Deployment Lifecycle]] |
| Activación durable + ack | plan activo F1 | mismo proyecto |
| Runtime systemd/SCM + launcher | plan activo F2 | mismo proyecto |
| Quiesce Windows/MT5 + retiro legacy | plan activo F3; app sólo implementa shutdown/health estándar | mismo proyecto |

## Contrato manifest resumido

- `version`: identificador de release y segmento de path seguro; downgrade es válido.
- `artifacts[platform]`: plataforma exacta, sin fallback.
- `entrypoint`: path relativo y miembro de `files[]`.
- `files[].path`: destino relativo dentro de la release; preserva `bin/`/`etc/`.
- `files[].object_key`: key dentro del bucket configurado.
- `files[].size` y `sha256`: obligatorios; verificación antes de promotion.
- `executable`: aplica mode executable sólo donde corresponde.

Distinción crítica para Symphony:

```text
STAGER_BUCKET=deploy
object_key nuevo = worker/sqx/<version>/<platform>/<file>
legacy mc path    = deploy/worker/sqx/<version>/<platform>/<file>
```

Los detalles y JSON completo viven en `docs/MANIFEST.md` del repo. No copiar `deploy/` al `object_key` nuevo.

## Configuración y operación

| Variable | Uso |
|---|---|
| `MINIO_ENDPOINT` | URL MinIO con esquema |
| `MINIO_ACCESS_KEY` / `MINIO_SECRET_KEY` | secret injection; nunca versionar |
| `STAGER_BUCKET` | bucket separado de object keys |
| `STAGER_MANIFEST_KEY` | key del manifest dentro del bucket |
| `STAGER_ROOT` | instalación/state local |
| `STAGER_PLATFORM` | override sólo test/debug; default runtime |

Resultado CLI actual: imprime `staged` o `noop`; error retorna exit no-cero. Scheduling permanece externo.

## Fallos esperados

| Fallo | Comportamiento fail-safe |
|---|---|
| MinIO/manifest inaccesible | release actual intacta |
| Plataforma ausente | error explícito |
| Download/hash/size | temp eliminado; `CURRENT` intacto |
| Crash con `PENDING.next` | recovery local completa activación en siguiente RunOnce |
| Lock ocupado | segunda ejecución no muta |
| CURRENT corrupto | error de integridad; no noop silencioso |

## Mapa del repositorio

```text
cmd/stager/                 CLI/config
internal/manifest/          wire contract
internal/source/            MinIO
internal/staging/           RunOnce, filesystem, locks, activation
docs/ARCHITECTURE.md        fronteras y fallos
docs/MANIFEST.md            contrato exacto publisher/consumer
docs/SYMPHONY.md            integración inicial
specs/STAGER-MVP/           SPEC/PLAN/TASKS del MVP
```

## Roadmap controlado

1. [[Stager - Symphony Publisher Integration]]: completado; publisher, MinIO/shadow y cutover `0.2.40`.
2. [[Stager - Cross-Platform Deployment Lifecycle]]: activo; baseline/contención, activación durable, runtime Linux/Windows y retiro legacy.
3. Sólo ante señales reales: [[2026-08-08-stager-deployment-system]] para targets/scopes/control plane pequeño.

No mezclar estos tres niveles.

## Handoff para futuras IAs

- Para bugs/core de Stager: leer `AGENTS.md`, `docs/ARCHITECTURE.md`, `docs/MANIFEST.md`, SPEC y tests focales.
- Para publisher Symphony histórico: usar [[Stager - Symphony Publisher Integration]] como evidencia cerrada.
- Para activación/runtime Linux-Windows: usar [[Stager - Cross-Platform Deployment Lifecycle]] como planificador único y abrir sólo la fase activa.
- No reutilizar credenciales visibles en documentos legacy de Symphony; tratarlas como comprometidas.
- No rediseñar scopes/targets antes de las señales de promoción documentadas en la idea.

## ✅ Tareas relacionadas

```tasks
sort by priority
not done
description includes stager-app
short mode
hide task count
```

## 🔗 Links

- [[Stager]] — proyecto de implementación y planificador.
- [[Echo Forge]] — programa patrocinador.
- [[echo-forge]] — primera aplicación consumidora.
- [[Echo Forge - Cross-Platform Stager]] — discovery precursor.
- [[2026-08-08-stager-mvp-boundary-and-activation]] — decisión histórica del MVP.
- [[2026-08-10-stager-product-boundary-and-durable-activation]] — frontera vigente del producto.
- [[Stager - Symphony Publisher Integration]] — integración/cutover completados.
- [[Stager - Cross-Platform Deployment Lifecycle]] — implementación activa.
- [[2026-08-08-stager-deployment-system]] — backlog/idea de evolución futura.
