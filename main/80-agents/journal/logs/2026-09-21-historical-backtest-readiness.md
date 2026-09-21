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
  - "[[2026-09-21-historical-research-m0]]"
  - "[[2026-09-21-cursor-grok-4.7-historical-backtest-readiness]]"
aliases:
  - "Historical backtest readiness 2026-09-21"
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

# 2026-09-21-historical-backtest-readiness

## Cambio

- **Tipo:** updated (notas canónicas) + created (este change log + agent run) + publicación Git del engine.
- **Archivo(s):**
  - `10-projects/Personal/Polymarket Engine/Polymarket Engine — MVP.md`
  - `10-projects/Personal/Polymarket Engine/Polymarket Engine — Continuidad Five-POC 2026-09-20.md`
  - `30-resources/polymarket/Polymarket Engine — Five-POC Guía Operativa 2026-09-20.md`
  - repo `xKoRx/polymarket-engine`: `internal/frames`, `cmd/engine/screen.go`, `internal/experiment/experiment.go`, `internal/histimport`, recibo `testdata/research-master/`

## Motivo

- El backtest causal de PE-005-R1 seguía bloqueado por tick, kickoff, paridad de libros y `SCREEN_BLOCKED_INBOX`. Había que resolver lo que el contrato existente permite, o dejar evidencia del dato que no existe.

## Fuentes usadas

- PendulumFlow v3, horas `2026-08-18T06` a `2026-09-02T12` inclusive, 367 horas, 0 errores de consulta. Predicado remoto `tick_size_change` y `new_market` sobre las cuatro condition ids exploratorias. Los parquet completos no se guardaron.
- El sha256 del objeto horario completo sigue siendo el del publicador, no recalculado en local. El rango de tick de la hora 21 ya había coincidido con el sha256 de producto, y no es un parquet autónomo.
- `new_market` trae question, slug, outcomes y assets. No trae `gameStartTime` ni tick.
- Wayback CDX de Gamma y de MLB respondió 503. No hay snapshot point-in-time recuperado en esta pasada.

## Resolución aplicada

- Decisión `DESCRIPTIVE_ONLY`. No se declara `BACKTEST_PASS`, `OOS_PASS` ni `HYPOTHESIS_VALIDATED`.
- El primer `tick_size_change` de cada mercado es posterior al kickoff y dice `old_tick_size=0.0100`, `new_tick_size=0.0010`. Entre el `new_market` del 2026-08-26T13Z y ese cambio no hay otro `tick_size_change`. El reducer congelado sella `new_tick_size` en el instante del evento y no rellena los libros anteriores. No se cambió el modelo de calidad.
- El kickoff sigue en `SCHEDULE_CORROBORATED_POSTHOC`. El OOS 22:45Z no se abrió.
- `RouteAvailable` espera un hueco del inbox antes de `RouteRecord`. No se subió `MaxInboxDepth` ni se cambió `cuts=30`. `RouteRecord` sigue consumiendo la secuencia si se le llama con el inbox lleno.
- SCREEN `cuts=30` entregó 30/30 frames, 0 inelegibles y 0 oportunidades en los cuatro mercados, dos pasadas con el mismo digest. Replay `{1}` y `{32,7,1}` coinciden. Shadow `INCONCLUSIVE`, 0 oportunidades, 0 fills, fee `UNRESOLVED`.
- M4 no-live recertificado en `66486ac`. Recibo `09e8c76`. `master` y `main` fast-forward. El binario de Sports Week sigue en `bfa6eaf`. El servicio no se reinició. Durante la pasada la campaña entró sola en `CAPTURING` a las 2026-09-21T21:05:20Z.

## Validación

- `gofmt`, `go vet`, `go test -count=1 ./...` PASS. `go test -count=1 -race ./...` PASS en máquina desocupada.
- `histimport` coverage 95.0% de sentencias. Las pruebas nuevas cubren fallas de lectura, parseo, store ausente y el orden real del tick de archivo.
- `engine journal verify` de los cuatro journals canónicos: CRC, contigüidad y frontera OK. `account_fact` queda `DEGRADED` porque el journal de investigación no tiene hechos de cuenta.
- `engine experiment certify --profile no-live --baseline 66486ac` → `M4_CERTIFIED_NON_LIVE`, 27 PASS / 0 FAIL / 0 in-scope NOT_RUN / 5 diferidos live.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos ni paths absolutos de máquina

## Rollback

- Revertir `66486ac` y `09e8c76` en `xKoRx/polymarket-engine` no toca el dataset ni el binario de la semana Sports. No borrar `historical-m0` ni `sports-week-pe005` para liberar disco.
