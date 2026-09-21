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
  - "[[2026-09-21-polymarket-master-consolidation]]"
  - "[[u02-v2-cash-confirmed]]"
aliases:
  - "PE-005-R1 sports week activation 2026-09-21"
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

# 2026-09-21-pe005-r1-sports-week

## Cambio

- **Tipo:** updated (notas canónicas) + created (este change log + agent run) + publicación Git del engine + servicio de captura armado.
- **Archivo(s):**
  - `10-projects/Personal/Polymarket Engine/Polymarket Engine — MVP.md`
  - `10-projects/Personal/Polymarket Engine/Polymarket Engine — Continuidad Five-POC 2026-09-20.md`
  - `30-resources/polymarket/Polymarket Engine — Five-POC Guía Operativa 2026-09-20.md`
  - `30-resources/polymarket/00-index.md`
  - `30-resources/polymarket/log.md`
  - repo `xKoRx/polymarket-engine` `master`/`main` @ `bfa6eaf` (código `c3b1aa1`)

## Motivo

- El owner autorizó corregir la confusión entre fee de mercado (tope publicado) y fee informada por trade, y dejar Sports Reversion en una campaña read-only de siete días. E3 estaba `IMPLEMENTATION_BLOCKED` por `fee_source_discrepancy`.

## Fuentes usadas

- Mandato PE-005-R1 / SPORTS REVERSION WEEK-LONG RESEARCH.
- Diagnóstico E3 STOP y evidencia E2 (`fee_rate_bps` de trade `"0"` frente a cap Gamma/CLOB 1000).
- Certificado no-live y canary sobre el mercado 4584879.

## Resolución aplicada

- `ResolveFee` trata el tope declarado y la fee de trade como identidades distintas. Si el valor de trade cae dentro del tope, el resultado es INTERVAL `[0, cap]`, no SUSPECT. Fuera del tope, o si dos trades de la misma identidad no convergen, sigue SUSPECT. Un trade convergente sin tope declarado sigue siendo POINT de ese trade. `REAL_FEE_READY` permanece false. `d5ce263` no se integró.
- `record` reconecta bajo `--reconnect` como epoch nuevo y registra el gap. No inventa continuidad.
- Operador `ops/sports-week/sportsweek.py`: descubrimiento MLB `series_id=3` moneyline por identidad y kickoff, captura T−90, health, análisis sobre snapshots cerrados. Unidades user `sports-week-capture`, `sports-week-health`, `sports-week-analyze`.
- Canary PASS en 4584879: libros `OBSERVED_USABLE`, observación de trade `"0"` conservada, `suspect=false`, cuarentena 0, replay digest idéntico. La campaña no se declaró iniciada: a las 17:15Z no había ventana T−90 abierta. Servicio `ARMED`, `started_at` null. Próxima ventana 2026-09-21T21:05:00Z (4584879, kickoff 22:35Z).
- Sin canal de notificación externo. Las alertas quedan en el dataset `sports-week-pe005`.

## Validación

- `go test ./... -count=1` y `go test ./... -race -count=1` verdes. `go vet` verde.
- `feeresolver.go` 100% en el paquete regimes (total del paquete 96.5%).
- `engine experiment certify --profile no-live --baseline c3b1aa1` → `M4_CERTIFIED_NON_LIVE`, 27 PASS / 0 FAIL / 5 diferidos live (G-16, G-17, G-18, G-19, G-14b).
- Binario de campaña `vcs.revision=bfa6eaf`, `vcs.modified=false`. Remoto `origin/master` = `origin/main` = `bfa6eaf`.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos ni rutas de máquina

## Rollback

- El servicio se detiene con las unidades user. Los journals cerrados no se borran. Revertir el engine es un commit nuevo sobre `master`; no force-push. `REAL_FEE_READY` y `LIVE_DISABLED` no cambian con el rollback.
