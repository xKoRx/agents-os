---
type: change_log
schema_version: 1
scope: session
created: "2026-10-06"
updated: "2026-10-06"
area: "[[Echo]]"
project: "[[Echo Futures]]"
application:
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

# BTG-S01 S2 bars forensics — change log

## Cambio

Creado [[BTG-S01-S2-1M-FORENSICS]] y [[2026-10-06-codex-gpt-6.1-sol-btg-s01-s2-bars-forensics]].

## Motivo

Mandato One-Shot del Manager: documentar seam mínimo para histórico NQ1m real bajo baseline S2/MM actual.

## Fuentes usadas

[[BTG-PLAN]], [[BTG-S01-SUBMANAGER-PROMPT]], [[Echo Futures — BT-S01 Backtester V1 Design]], [[Echo Futures — BT-S04 Final Remediation and Certification]], D4-B1/D4-B2 y source certificado Echo cd451972.

## Resolución aplicada

Se distingue soporte heredado, propuesta OHLC nativa y ambigüedad intrabar pendiente; no product code ni reinterpretación de baseline.

## Validación

Diez regresiones heredadas PASS; targeted schema lint y git diff check.

## Compartibilidad

Scope local; sin secretos, logs pesados ni paths de máquina en evidencia canónica.

## Rollback

Revertir commit documental de esta rama; sin efectos sobre runtime o dataset.
