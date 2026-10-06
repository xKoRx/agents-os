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

# BTG-S01 CLI cursor once independent review

## Cambio

Created [[BTG-S01-CLI-CURSOR-ONCE-FINAL-REVIEW]] y agent_run propio; evidencia heavy externa. Cierre worker autorizado acotado, sin cerrar Root/programa ni registrar aceptación histórica.

## Motivo

F11 exige Closeexactonce incluso EOF→re-admissionerror. Mismo probe REDbase→PASScandidato con errores/bytes retenidos; wrapper fix cumple gate local.

## Fuentes usadas

Repo xKoRx/echo source15422, parente632, tipread-onlye320; SPEC/PLAN/TASKS y pruebas aisladas. CapsuleSHAd67c84152821c973e0a8176a9f23c08cdb4f37b150a78533be8423dd99facfd1, external BTG-S01 workspace reports/cli-cursor-once-review.

## Validación

Race/vet/build/anti-maskingPASS, exactdelta3/3=100% sin exclusiones, SOURCE_CLOSE/repro/legacybytesPASS; originalNT/historicalNOT_RUN. Strictlint y diffcheck propios antescommit; sin paths del vault/secretos/dumps.

## Compartibilidad

Local; sólo fuente, veredictos y límites observables. FeedbackNONE.

## Rollback

Revert del commit docs propio; producto preservado. RootS01 sigue abierto.
