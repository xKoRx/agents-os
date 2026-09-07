---
type: change_log
scope: project
created: 2026-07-31
updated: 2026-07-31
area: "[[Echo]]"
project: "[[Echo Forge - Cierre de Etapa 4]]"
entities:
  - "[[Echo Forge - Cierre de Etapa 4]]"
  - "[[BuildMinIOPath]]"
  - "[[2026-07-29-sqx-trade-list-exporter-source-order-count-zero]]"
related:
  - "[[2026-07-31-echo-forge-tradelist-triple-defect-fix]]"
  - "[[2026-07-31-minio-storage-path-must-be-deterministic-by-logical-identity]]"
  - "[[2026-07-31-storage-path-deterministic-by-logical-identity]]"
confidence: verified
load_policy: never
indexable: false
index_priority: never
tags:
  - kind/changelog
  - scope/project
  - project/echo-forge
  - area/echo
  - change/updated
  - change/created
---

# Change log — EF-G27: rollback `BuildMinIOPath` a path plano

## Qué cambió

- **L3 known-error actualizado**: [[2026-07-29-sqx-trade-list-exporter-source-order-count-zero]]
  — causa raíz corregida. El diagnóstico previo (plugin Java como raíz) era
  incorrecto; la raíz real es `BuildMinIOPath` inyectando `requestID` con
  resolución inconsistente entre watcher/worker/uploader.
- **L3 learning creado**: [[2026-07-31-minio-storage-path-must-be-deterministic-by-logical-identity]]
  — anti-patrón de inyectar IDs de ejecución en paths de storage compartido.
- **L3 decisión creada**: [[2026-07-31-storage-path-deterministic-by-logical-identity]]
  — `BuildMinIOPath` plano, sin `ctx` ni `requestID`.
- **Especificación**: `specs/FEAT-SQX-STRATEGY-EVALUATION/G6_HANDOFF.md` §10.3 (EF-G27).
- **Código symphony (working tree, sin commit)**: `paths.go` + 9 callers +
  4 archivos de test. `go build`/`go vet`/`go test` verdes.

## Motivo

Owner pidió reevaluar el diagnóstico del agente auditor (que apuntaba al
plugin Java) y aplicar fix definitivo. La reevaluación con la traza de
correcciones reveló que el bug mutaba porque cada parche 0.2.x atacaba
síntomas downstream sin tocar la causa generadora.

## Validación

- `go build ./core/... ./adapters/... ./activities/... ./cmd/...` OK.
- `go vet` (módulo sqx sin `tools/`) limpio.
- `go test $(go list ./... | grep -v '/tools')` todo verde.
- ReadLints limpio en los 10 archivos editados.
- `graphify-personal update .` ejecutado (9189 nodos, grafo actualizado).

## Pendiente

- Commit + bump de versión (0.2.11).
- Deploy a Zeus y smoke test end-to-end con `example_flow_50`.
- Purga de carpetas huérfanas con `cfgID`/`RunID` en `sqx-strategies/`.
