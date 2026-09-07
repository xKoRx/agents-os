---
type: known_error
schema_version: 1
scope: project
created: "2026-09-01"
updated: "2026-09-01"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities: []
related:
  - "[[2026-09-01-release-version-authority]]"
  - "[[2026-09-01-release-authority-stale-manifest-rollback]]"
aliases:
  - release-authority stdout contamination
confidence: verified
source_session: ECHO-FORGE-C3-RELEASE-CONVERGENCE-RECOVERY-NORMAL
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/project
  - project/echo-forge
---

# Echo Forge C3 release-authority SDK stdout contamination

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Estado actual

- RESUELTO en source: el debug accidental del SDK fue eliminado y el boundary de `release-authority` reserva stdout exclusivamente para el JSON de autoridad; la recuperación física de C3-B permanece pendiente y fuera del alcance de esta sesión.

## Síntoma

- `SQX_RELEASE_AUTHORITY_ACK_MAX=0.2.83 ./deploy_release.sh` aborta en el primer authority preflight con `jq: parse error: Invalid numeric literal at line 1, column 13`.

## Causa

- El módulo declarado fija `github.com/xKoRx/sdk v0.0.0-20260827204048-ea09cc1bb8b3` con replace local `../sdk`; el código resuelto imprime `RESPUESTAAAA: ...` a stdout desde `pkg/shared/etcd/cache.go:121`; además, el logger de inicialización escribe eventos a stdout.
- `deploy_release.sh` captura stdout de `go run ./cmd/release-authority` como un único JSON y `jq` no puede parsear la salida contaminada.

## Impacto

- La publicación canónica no alcanza build ni `kick_release_for_upload`; no se publicó `0.2.84` y no se inició CERT-A/B.
- El recovery físico queda `BLOCKED / CLOSED` porque el límite está en infraestructura source-level y la sesión no está autorizada para parchearla.

## Detección

- Separar stdout/stderr del authority real en production mostró 5.599 bytes en stdout: la línea `RESPUESTAAAA`, eventos de telemetría y sólo al final el objeto `sqx-release-authority.v1` válido.
- La ejecución directa con el mismo DI/ETCD/MinIO y ACK exacto produjo el JSON esperado, pero el wrapper canónico no puede extraerlo; tras el aborto, MinIO continuó en published `0.2.78`, remote line max `0.2.83`, `INCONSISTENT`, candidate `0.2.84`.

## Mitigación

- No usar `SQX_RELEASE_AUTHORITY_TEST_JSON`, `SQX_RELEASE_AUTHORITY_TEST_BIN` ni otro bypass; no parchear source durante la certificación.
- Preservar evidencia y retornar al lead para un nuevo commit que corrija el boundary de salida; luego repetir el ciclo completo con nueva release y nuevas identities físicas.

## Evidencia

- Repositorio `xKoRx/symphony` en `ee61d3d0b3b53416e80b231522342482322e556e`; `git status` conservó únicamente los dos dirty foreign preexistentes.
- `deploy/manifest.json` permaneció SHA256 `c4102e3446d44216f8e2b69b5a0aec2044e04667090399fcc1ecf5639ba70dfa`, versión `0.2.78`; `input/example/config.json` permaneció SHA256 `ae0fe31c0362bec9f41549a54dc567638915a235a41caef9805f178e8c849b77`.
- No existe materialización local `deploy/0.2.84`; el preflight posterior confirmó `0.2.84` `AVAILABLE` y la autoridad no cambió.

## Resolución — 2026-09-01 — ECHO-FORGE-RELEASE-AUTHORITY-STDOUT-ISOLATION-FIX-NORMAL

- SDK `c85594440f6755443ceb97ec4e333cd0ddb5b0ed` elimina exclusivamente `fmt.Printf("RESPUESTAAAA...` de `pkg/shared/etcd/cache.go`; pseudo-version canónico `v0.0.0-20260902001205-c85594440f67`.
- Symphony `02fabffe958854ab30e017301a8c30aaada527ac` conserva `telemetry.NewJSONLogger` global y aísla localmente el CLI: `machineOut := os.Stdout`, `os.Stdout = os.Stderr` durante init/evaluate/close y JSON final después de close.
- M1-M6, tests/race/vet, harness S1-S10 y smoke production read-only pasan; stdout es exactamente un JSON con newline, y los diagnósticos permanecen en stderr.
- C3-B no se certificó físicamente ni se publicó `0.2.84`; la autoridad observada sigue `0.2.78` publicada, `0.2.83` remoto/local, candidate `0.2.84`, `INCONSISTENT`, target `AVAILABLE`.
