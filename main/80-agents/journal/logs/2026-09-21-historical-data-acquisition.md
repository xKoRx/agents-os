---
type: change_log
schema_version: 1
scope: session
created: "2026-09-22"
updated: "2026-09-22"
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
application:
entities:
  - "[[Polymarket Engine — MVP]]"
related:
  - "[[Research — Historical Data Acquisition ADDENDUM 2026-09-21]]"
  - "[[2026-09-21-historical-research-m0]]"
  - "[[2026-09-21-historical-backtest-readiness]]"
  - "[[2026-09-21-zcode-glm-5.3-flash-historical-data-acquisition]]"
aliases:
  - "Historical data acquisition 2026-09-21"
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

# 2026-09-21-historical-data-acquisition

## Cambio

- **Tipo:** created (nota addendum + dataset durable + este change log + agent run) + updated (MVP, Continuidad Five-POC).
- **Archivo(s):**
  - `10-projects/Personal/Polymarket Engine/Research — Historical Data Acquisition ADDENDUM 2026-09-21.md`
  - `10-projects/Personal/Polymarket Engine/Polymarket Engine — MVP.md`
  - `10-projects/Personal/Polymarket Engine/Polymarket Engine — Continuidad Five-POC 2026-09-20.md`
  - dataset `xKoRx/polymarket-engine-datasets/hist-acq-20260921/` (raw + extracciones + gamma/clob/mlb + benchmark + MANIFEST + SHA256SUMS)

## Motivo

- Mandato owner one-shot: resolver adquisición y persistencia de datos históricos con pruebas físicas y ADDENDUM correctivo del Deep Research, sin tocar Sports Week ni el OOS.

## Fuentes usadas

- `archive.pendulumflow.com/v3` horas 2026-09-01T21 y T22 (descarga completa, sha256 local = publicador), documentación del archivo (llms.txt, LICENSE.txt, formats/v3, start, faq) y probes de límite inferior.
- `gamma-api` sin hits por slug/condition; CLOB `GET /markets/{condition_id}` ×4 (game_start_time, tick, fee params, tokens); statsapi schedule ×4 (gameDate 22:40:00Z, Final).
- pmdata.dev (docs + pricing), polymarketdata.co (home + pricing + probes anónimos 404).
- Contratos existentes: `internal/histimport` @ master `66486ac`, `COHORT.json`, journals `historical-m0`.

## Resolución aplicada

- `HISTORICAL_DATA_ACQUISITION_RESULT` con cadena de custodia completa: bytes → extracción independiente (multiset idéntico) → import+replay (digests COHORT 4/4, `{1}`==`{32,7,1}`).
- Certificación L2: snapshot-only admisible; reconstrucción por deltas descartada con métrica (66–85% mismatch BBA por intervalo).
- Persistencia: decisión A Parquet+DuckDB; equivalencia demostrada con ClickHouse efímero (digests idénticos p1–p4); TimescaleDB no medible (sin root/docker) con exacto faltante documentado.
- Sin compras; sin cambios de arquitectura ni código de producción; OOS sellado intacto; Sports Week sólo probe read-only (`sports-week-capture.service` running).
- Servicios efímeros del benchmark terminados (SYSTEM SHUTDOWN); nada permanente instalado.

## Validación

- SHA256SUMS.txt del dataset; MANIFEST.json con hashes verificados por script contra SUMS.
- digests benchmark: p1 `8c6c5554…`, p2 `72e62aec…`, p3 `67efe361…`, p4 `30d78294…` idénticos A==C.
- `reconstruction_cert.json` por mercado; resultados por fase en `benchmark/results/*.json`.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos; direcciones de donación del archivo NO copiadas al vault.

## Rollback

- Revertir las tres notas del vault y borrar `hist-acq-20260921/` del repo de datasets; nada del repo engine fue modificado (builds a scratch only).
