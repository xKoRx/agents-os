---
type: change_log
schema_version: 1
scope: session
created: "2026-09-21"
updated: "2026-09-21"
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
application:
entities:
  - "[[Polymarket Engine — MVP]]"
related:
  - "[[Polymarket Engine — Continuidad Five-POC 2026-09-20]]"
  - "[[Polymarket Engine — Five-POC Guía Operativa 2026-09-20]]"
  - "[[2026-09-21-pe005-r1-sports-week]]"
  - "[[2026-09-21-cursor-grok-4.7-historical-research-m0]]"
aliases:
  - "Historical research M0 2026-09-21"
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
  - area/personal
  - project/polymarket-engine
---

# 2026-09-21-historical-research-m0

## Cambio

- **Tipo:** updated (notas canónicas) + created (este change log + agent run) + publicación Git del engine.
- **Archivo(s):**
  - `10-projects/Personal/Polymarket Engine/Polymarket Engine — MVP.md`
  - `10-projects/Personal/Polymarket Engine/Polymarket Engine — Continuidad Five-POC 2026-09-20.md`
  - `30-resources/polymarket/Polymarket Engine — Five-POC Guía Operativa 2026-09-20.md`
  - repo `xKoRx/polymarket-engine`: `internal/histimport`, `cmd/engine/historical.go`, recibo `testdata/research-master/`

## Motivo

- Hacer que PE-005-R1 pueda consumir un flujo histórico real por el journal de Capture, sin un segundo simulador y sin declarar la hipótesis validada.

## Fuentes usadas

- PendulumFlow v3, horas 2026-09-01T21 y T22, lectura remota por market id. Manifiesto del publicador conservado; el sha256 del objeto completo no se recalculó en local.
- Gamma y CLOB consultados el 2026-09-21 sólo como contraste posterior, no como hecho point-in-time.
- MLB statsapi del mismo día, coincidente con `gameStartTime` de Gamma en la cohorte. Autoridad: `SCHEDULE_CORROBORATED_POSTHOC`.

## Resolución aplicada

- Cohorte exploratoria congelada: cuatro moneylines con kickoff 2026-09-01T22:40:00Z (SD, NYM, TOR, SF). OOS 22:45Z (ATL, SEA) sellado y no analizado.
- `engine historical import` admite NDJSON ordenado por receive time. `engine historical describe` es descriptivo y no es el SCREEN.
- No se escribió tick ni fee inventados. Calidad restringida `SYNCING`. Economía `ECONOMICS_UNCERTIFIED`.
- SCREEN `cuts=30` queda `SCREEN_BLOCKED_INBOX`. La grilla `cuts=400` está etiquetada `EXECUTION_GRID_NOT_FROZEN`.
- M4 no-live recertificado en `56195c9`. Recibo `de33d7d`. `master` y `main` fast-forward. El binario de Sports Week sigue en `bfa6eaf`.

## Validación

- `go test ./...` PASS. `go test -race` de `internal/histimport` y `cmd/engine` PASS.
- Replay `{1}` y `{32,7,1}` con el mismo digest en los cuatro journals.
- Shadow sobre el binario `56195c9`: `INCONCLUSIVE`, 0 oportunidades, 0 fills, fee `UNRESOLVED`, digest `fc3927ce…;records=15420`.
- Servicio Sports Week activo, `started_at` null, mismo `ExecMainStartTimestamp`.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos ni paths absolutos de máquina

## Rollback

- Revertir `56195c9` y `de33d7d` en `xKoRx/polymarket-engine` no toca el dataset ni el binario de la semana Sports. No borrar `historical-m0` ni `sports-week-pe005` para liberar disco.
