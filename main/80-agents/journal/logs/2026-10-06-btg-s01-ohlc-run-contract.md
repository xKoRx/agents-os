---
type: change_log
schema_version: 1
scope: session
created: "2026-10-06"
updated: "2026-10-06"
area: "[[Echo]]"
project: "[[Echo Futures]]"
application:
entities:
  - "[[Echo Futures]]"
related: []
aliases: []
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
---

# BTG-S01 — cápsula OHLC de implementación

## Cambio

Creado [[BTG-S01-OHLC-RUN-CONTRACT]] con contrato propuesto B/C de SourceBar/parser/RunSpec y driver/venue, ownership disjunto, modelo intrabar fail-visible, seam MarketContext sin fake trade/quote y autoridad pendiente de configuración para dos EVAL días.

## Motivo y fuentes

Mandato ONE-SHOT arquitecto/forensics de BTG-S01; authorities Owner, SDK407 y reporte de configuración instalada. Paths source relativos a xKoRx/echo y refs source se conservan en el artifact. No cambios de producto, runtime, infra, master o sync.

## Validación

Schema materializer y strict lint de artifact/run/log, git diff --check y source clean HEAD407. Sin suites de producto por slice de diseño sin implementation. Worker aplica session-close por mandato, feedback/reusable candidates NONE, PRO_CHAT_POOL_DELTA0; Root no se cierra.

## Reconciliación de handoff

Root confirmó modelo gpt-6.1-sol por harness; registro corregido a model_source host. Se precisó que ACCOUNT_ECONOMICS alcanza TP/protección pero no adds, FILL/ORDER_FINAL sí evalúan adds, y ExecutableQuoteSource no admite fake modeled quote. C se clasifica diagnostic port; seam ModelPrice C2 propuesto, fuera de permiso actual, requiere freeze e intrabar policy sólo ante caso real.

## Rollback

Revertir sólo el commit documental de esta rama; no modifica baselines de producto ni gates Owner.
