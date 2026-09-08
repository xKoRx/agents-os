---
type: known_error
schema_version: 1
scope: application
created: "2026-08-16"
updated: "2026-09-08"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge]]"
  - "[[Symphony]]"
related:
  - "[[2026-08-16-echo-forge-a2-top-implemented]]"
  - "[[2026-08-16-echo-forge-a2-top-post-review-correction]]"
aliases:
  - sqx global tests mutate fixtures
  - sqx tools multiple main build failure
  - symphony sqx verification non-hermetic
confidence: verified
source_session:
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/application
  - application/echoforge
  - area/echo
  - tech/symphony
  - tech/go
---

# symphony-sqx-global-verification-non-hermetic

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- En hosts sin `libzmq.pc`, el baseline root `go test -race -cover ./...` falla en `github.com/pebbe/zmq4` antes de recorrer todo el workspace.
- En repo `xKoRx/symphony`, `go vet ./...` y `go test -race -cover ./...` fallan al compilar `sqx/tools` porque varios archivos del mismo package declaran `main`.
- La suite global también puede reescribir fixtures versionados de Strategy Evaluation con timestamps/benchmark actuales, dejando el working tree sucio aunque los tests funcionales pasen.
- La suite `./sqx/adapters/registry-postgres` completa falla en hosts macOS donde el Postgres embebido del harness no logra `initdb` (shared memory insufficient): todos los tests DB-backed (ControlPlane, AdoptStrategy v2, UpsertStrategyV2, StageProducerOutput, OutputNamespaceOwnership, Migration006) reportan `failed to start isolated PostgreSQL` tras ~12–76s cada uno.

## Causa

- `sqx/tools` agrupa múltiples programas one-shot como archivos del mismo `package main` sin build tags ni subdirectorios por comando.
- Tests/benchmarks de Strategy Evaluation escriben evidencia generada directamente sobre archivos versionados en vez de usar un output temporal o comparar sin mutación.
- El harness de PostgreSQL embebido (`postgrestest`) depende de límites de shared memory del host que `initdb` no alcanza; el bloqueo es de entorno, no del delta de código.

## Impacto

- El comando canónico global no entrega un exit code verde aunque los paquetes impactados estén sanos, y una sesión puede mezclar cambios de fixtures no autorizados con el delta real.
- Un agente puede atribuir erróneamente el fallo a su feature o preservar benchmarks/timestamps accidentales.
- La certificación G34 de persistencia (unique v2, producer-output, ownership) queda sin evidencia ejecutada en ese host y debe declararse DEGRADED, nunca PASS con mocks.

## Detección

- Antes y después de la suite global ejecutar `git status --short`; el fallo muestra `main redeclared in this block` para `sqx/tools`.
- Revisar diffs de `specs/FEAT-SQX-STRATEGY-EVALUATION/fixtures/phase4_performance.json` y `sqx/core/evaluation/warnings/artifacts/f5_warning_example.json`.
- Mensaje `unable to init database ... initdb -A password ... exit status 1` con nota de shared memory en el output de `go test ./sqx/adapters/registry-postgres`.

## Mitigación

- Verificar primero si `pkg-config --exists libzmq`; si falta, registrar el bloqueo de host por separado y no atribuirlo al delta.
- Ejecutar primero vet/tests con race sobre los paquetes impactados y registrar el bloqueo global como baseline separado.
- Si se ejecuta la suite global, restaurar solo los fixtures que estaban limpios al inicio y verificar byte-a-byte que no queden cambios laterales.
- Para el harness Postgres: comprobar preexistencia ejecutando el mismo test en un `git worktree` del commit base limpio; si reproduce, declarar DEGRADED con la evidencia del baseline y no fingir PASS.
- Corrección duradera pendiente: separar cada tool en su propio subdirectorio/comando o aplicar build tags válidos, hacer que la generación de artifacts use rutas temporales salvo un comando explícito de actualización, y ajustar (o documentar) los límites de shared memory del host para `initdb`.

## Evidencia

- Reconfirmado durante la corrección post-review A2-TOP: baseline root bloqueado por `libzmq` ausente; baseline SQX volvió a mutar los mismos fixtures y reprodujo los múltiples `main` de `sqx/tools`.
- Observado durante A2-TOP: todos los packages ejecutados pasaron salvo `sqx/tools`; la suite cambió benchmark/timestamps de los dos fixtures indicados y esos cambios fueron restaurados antes del cierre.
- El scope A2-TOP quedó verde con `go vet ./core/domain ./core/capabilities ./adapters/registry-postgres/migrations` y `go test -race -cover` sobre los mismos packages.
- Reconfirmado en F-01 (2026-09-08, host macOS darwin 25.5.0): `TestStageProducerOutput_*`, `TestAdoptStrategy_V2Cutover_*`, `TestUpsertStrategyV2_*`, `TestControlPlane_*` y `TestOutputNamespaceOwnership_*` fallan por `failed to start isolated PostgreSQL`; el mismo test reproduce el fallo idéntico en worktree del baseline `db8a022`, descartando atribución al delta.
