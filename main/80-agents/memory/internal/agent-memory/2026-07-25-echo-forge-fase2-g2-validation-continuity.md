---
type: agent_memory
scope: internal
created: 2026-07-25
updated: 2026-09-09
memory_state: archived
project: "[[Echo Forge - Cierre de Etapa 4]]"
entities:
  - "[[Echo Forge]]"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-memory
  - scope/project
  - project/echo-forge
---

# Echo Forge Fase 2 — validación G2 + fix-pack (cierre 2026-07-25 ~21:40 CLT)

## Veredicto vigente

**G2 listo para firma del owner (`review → accepted`).** El pase `b2848d7` entregó F2; el fix-pack `5c186a3` cerró los 4 blockers. Revalidación owner (Cursor) independiente: build OK, JUnit 5/5, smoke `compressed_bytes` reales, SHA 39/39 OK exit 0, sin import `Directions`, `verify_build.sh` OK, mapping Go de 5 tipos presente. Smoke SQX Build 142 real queda como **defer firmado** en `G2_HANDOFF.md`.

## Commits

- `b2848d7` — F2 inicial (EchoForgeTradeListExporter + kernel F1).
- `5c186a3` — fix G2 blockers (+1176/−184, 12 files). HEAD actual.

## Blockers (histórico → cerrado)

1. SHA falso / productivos F2 sin firma → regenerado `SHA256SUMS.txt` + `regenerate_sha256sums.sh` → 39/39 OK.
2. `_SUCCESS` con `compressed_bytes=0` + rewrite externo → API `writeScopeArtifacts` arma manifest/export_run con sizes reales **antes** de `_SUCCESS`.
3. `OD-P2.1` mentía (import `Directions`) → reflexión + cache `DIRECTIONS_BOTH`.
4. DoD: `docs/ROLLBACK.md`, `scripts/verify_build.sh`, `ResolveLocalProjectNameByType` con 5 types + test; smoke SQX real defer firmado.

## No re-objetar

- Plugin productivos ya existen; no hay más “crear plugin”.
- G2 sigue `review` hasta firma owner. F3 no habilitada.
- Overview/WFM no migran al kernel en F2 (decisión explícita).
- `phase1/G1_HANDOFF.md` ya trackeado en `5c186a3`.

## Caveat entorno validador

`go test ./sqx/core/runtime/...` puede fallar aquí por deps privadas (`api-persist` / fury proxy). No invalidar el mapping: está en `config.go` L148–156 y test `TestResolveLocalProjectNameByType_FixedProjects`.

## Próximo paso

Owner: promover G2 `review → accepted` en `G2_HANDOFF.md` + nota del proyecto si acepta el defer SQX real. Sólo entonces despachar F3.
