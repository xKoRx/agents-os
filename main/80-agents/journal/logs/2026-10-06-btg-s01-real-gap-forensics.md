---
type: change_log
schema_version: 1
scope: session
created: "2026-10-06"
updated: "2026-10-06"
area: "[[Echo]]"
project: "[[Echo Futures]]"
application: "[[Echo]]"
entities: []
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

# BTG-S01 — real gap forensics

## Cambio

Created [[BTG-S01-REAL-GAP-FORENSICS]] y agent_run atribuible Codex/gpt-6.1-sol. Artifact propio; no cambios al plan, findings ni resultado Root.

## Motivo

Gap real detuvo el primer smoke. Distinguir ausencia física, calendario y bug de diagnóstico, dejando visibles los límites materiales de13exports y candidatos seleccionados sólo por calidad/warmup.

## Fuentes usadas

[[Echo Futures — BT-S01 Backtester V1 Design]], [[Echo Futures — BT-S04 Final Remediation and Certification]], [[BTG-S01-OHLC-RUN-CONTRACT]]; fuente y snapshotSDK/Echo fb210ac4; originales Owner y artifacts sellados Root; corrección mínima970f1d52.

## Resolución aplicada

Strict halt correcto; UNKNOWN causa de omisiones/outside prints. F12reporting corregido con realrerun/reproduce. F13summarycounts abierto, sin esconderlo como límite. Tres exports insuficientes bajo51H4; no fakebars, PnLsum/reset ni overrides inventados.

## Validación

CalendarResolver/SessionGrid compartidos sobrebytes reales, SHA y source refs; RED/GREEN/race/vet directos offline; dos failedreal reruns+freshreproduceIDENTICAL. Sin autorización ampliada de infra, trading niPROD.

## Compartibilidad

Scope local; sin secretos, dumps pesados ni paths absolutos de vault. Feedback y reusablebehaviorNONE.

## Rollback

Revertir sólo este commit documental; Root conserva su propio state y no se altera código/data desde esta rama.
