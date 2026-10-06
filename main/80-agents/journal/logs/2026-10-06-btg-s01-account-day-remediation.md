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
related:
  - "[[BTG-S01-ACCOUNT-DAY-REMEDIATION]]"
  - "[[BTG-S01-SUBMANAGER-PROMPT]]"
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

# 2026-10-06-btg-s01-account-day-remediation

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created
- **Archivo(s):**
  - `xKoRx/echo:v3/backtester/run.go` — resolución inicial de la fecha del account-day contenedor.
  - `xKoRx/echo:v3/backtester/account_day_identity_regression_test.go` — protección native/legacy.
  - `xKoRx/echo:specs/btg-s01-account-day-remediation/` — SPEC, PLAN, TASKS y VERIFICATION.

## Motivo

- BT2-F08 reproducido independientemente: un inicio parcial antes del reset 17:00 CT abre el día civil incorrecto; el boundary natural recibe el mismo ID y falla `ACCOUNT_DAY_FAILED`.

## Fuentes usadas

- Finding BT2-F08 y revisión independiente local de BTG-S01; calendario funcional NQ con Chicago 17:00.

## Resolución aplicada

- `openInitialAccountDay` calcula el intervalo contenedor desde la timezone y reset instalados, usando los helpers civiles existentes y `AddDate`; mantiene el timestamp de apertura observado, los boundaries naturales, el plan ordinal, la ventana caller y los bytes/paths fuera del seam autorizado.

## Validación

- Source branch `codex/btg-s01-account-day-remediation`, freeze `171fc712e56d731493befeef5c54a2620f25d31a` (tree `aee767d446428fa1223f7f7f0a682e0df53e604c`), publicado y limpio.
- Regresión native/legacy y bordes reset/year/DST/horizon: PASS; S04/Driver/plan/native OHLC seleccionados con race: PASS; `go vet ./v3/backtester`: PASS; changed-block coverage 8/8: PASS; `git diff --check`: PASS.
- Digests SHA-256 de logs/profiles en el bundle externo `work/btg-s01-20261006/reports/account-day-remediation/`: baseline red `cea4aa5cb1b4c550a7db7bf3e5211e6ad6d5e46734de04aeeb16e621841b7095`, targeted race `fcb09ba31d15515dd9eb226467cfab7044241b768a7f89e1e21de5524647eef6`, vet vacío/pass `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`, coverage `8161e26c22c7804140abd54f2c8d71b5593edd1a26acacd19b6ef67d7f2f8a11`.
- Datos originales de historia: `POLICY_DENIED / NOT_ACQUIRED`; rerun histórico no ejecutado. Revisión independiente TOP nueva pendiente; el worker no acepta el gate ni cierra el programa.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir únicamente mediante un commit de revert del freeze si el review encuentra un defecto; no reescribir ni force-push la historia publicada.
