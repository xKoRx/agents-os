---
type: change_log
schema_version: 1
scope: session
created: 2026-08-15
updated: 2026-08-15
area: "[[Echo]]"
project: "[[Echo Forge]]"
application:
entities:
  - "[[Symphony]]"
related:
  - "[[sqx-custom-analysis-loads-snippets-jar]]"
  - "[[2026-08-15-echo-forge-mt5-mmlots-session-feedback]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-08-15-echo-forge-mt5-mmlots-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-08-15 echo-forge mt5 mmlots change log

## Cambio

- **Tipo:** created
- **Archivo(s):**
  - `80-agents/memory/public/known-error/sqx-custom-analysis-loads-snippets-jar.md`
  - `80-agents/journal/feedback/system-1/2026-08-15-echo-forge-mt5-mmlots-session-feedback.md`
  - `80-agents/journal/agent-runs/2026-08-15-cursor-grok-4-6-mt5-mmlots-export.md`

## Motivo

- El deploy del plugin SQX al JAR de packaging no cambia el Custom Analysis headless; hay que persistir el error conocido.

## Fuentes usadas

- Canary Zeus 2026-08-15 (log sqcli + `.mq5`)
- `specs/FEAT-SQX-JAVA-EXPORTER-PLUGIN/VERIFICATION.md`

## Resolución aplicada

- Known error indexable + feedback de sesión + agent run.

## Validación

- El known_error describe síntoma, causa y mitigación verificados en el canary.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Borrar las tres notas si se rechaza el close.
